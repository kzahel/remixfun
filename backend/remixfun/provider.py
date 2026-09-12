"""Read Civitai metadata from the requested image's dehydrated page queries.

Based on the user-supplied September 2026 findings. Page scripts never execute.
REST enriches preview URLs and exact model-version evidence, never settings.
"""

import asyncio
import html
from html.parser import HTMLParser
import json
import re
from urllib.parse import urljoin, urlsplit

import httpx

from .domain import Problem, image_id

MAX_IMAGE = 25 * 1024 * 1024
MAX_HTML = 10 * 1024 * 1024
MAX_JSON = 2 * 1024 * 1024
IMAGE_HOSTS = {"image.civitai.com", "blobs-b2.civitai.com"}
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
)


class NextData(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.scripts = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "__NEXT_DATA__":
            self.current = []

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.current is not None:
            self.scripts.append("".join(self.current))
            self.current = None


def same_id(value, requested):
    return type(value) in {int, str} and str(value) == str(requested)


def query_data(queries, method, requested):
    matches = []
    for query in queries:
        if not isinstance(query, dict):
            continue
        key = query.get("queryKey")
        if not isinstance(key, list) or len(key) != 2 or key[0] != ["image", method]:
            continue
        arguments = key[1]
        if not isinstance(arguments, dict) or not isinstance(arguments.get("input"), dict):
            continue
        if same_id(arguments["input"].get("id"), requested):
            matches.append(query)
    if len(matches) > 1:
        raise Problem("Civitai returned ambiguous metadata for this image. No recipe was imported.", 502)
    if not matches:
        return None
    state = matches[0].get("state")
    if not isinstance(state, dict) or state.get("status") == "error":
        raise Problem("Civitai could not load this image's metadata. Try again later.", 502)
    data = state.get("data")
    if data is not None and not isinstance(data, dict):
        raise Problem("Civitai returned an unreadable image record. No recipe was imported.", 502)
    return data


def safe_url(value, hosts):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        return (parsed.scheme == "https" and parsed.hostname in hosts
                and parsed.port in {None, 443} and not parsed.username
                and not parsed.password and not parsed.query and not parsed.fragment)
    except ValueError:
        return False


def page_preview(image_record, page):
    value = image_record.get("url")
    if safe_url(value, {"image.civitai.com"}):
        return value
    if not isinstance(value, str) or not re.fullmatch(r"[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}", value):
        return None
    # Observe the CDN account prefix; always use the requested image's UUID.
    text = html.unescape(page).replace(r"\/", "/")
    prefixes = set(re.findall(r"https://image\.civitai\.com/([A-Za-z0-9_-]+)/", text))
    if len(prefixes) != 1:
        return None
    return f"https://image.civitai.com/{prefixes.pop()}/{value}/original=true/{value}.jpeg"


def parse_page(page: str, requested: str):
    parser = NextData()
    parser.feed(page)
    if len(parser.scripts) != 1:
        raise Problem("Civitai did not return a readable image page. Its page format may have changed or the request was blocked.", 502)
    try:
        payload = json.loads(parser.scripts[0])
        queries = payload["props"]["pageProps"]["trpcState"]["json"]["queries"]
        if not isinstance(queries, list):
            raise ValueError("Invalid query cache")
    except (ValueError, KeyError, TypeError) as exc:
        raise Problem("Civitai's image-page metadata format was not recognized.", 502) from exc
    image_record = query_data(queries, "get", requested)
    if image_record is None:
        raise Problem("This Civitai image was not found in the returned page.", 404)
    if not same_id(image_record.get("id"), requested):
        raise Problem("Civitai returned a different image. No recipe was imported.", 502)
    generation = query_data(queries, "getGenerationData", requested)
    if generation is not None:
        for key in ("imageId", "id"):
            if key in generation and not same_id(generation[key], requested):
                raise Problem("Civitai returned metadata for a different image. No recipe was imported.", 502)
    meta = generation.get("meta") if generation is not None else None
    if meta is not None and not isinstance(meta, dict):
        raise Problem("Civitai returned an unsupported metadata structure.", 502)
    hidden = image_record.get("hideMeta") is True or (generation or {}).get("hideMeta") is True
    warnings = []
    if hidden:
        warnings.append("The creator has hidden generation metadata. Available resources are saved; missing settings remain unknown.")
    elif meta is None or not meta:
        warnings.append("This page contains no generation settings for this image. Available image details and resources are saved.")
    raw = {
        "id": int(requested), "meta": meta,
        "generation_data": generation, "image_record": image_record,
        "baseModel": image_record.get("baseModel") or (generation or {}).get("baseModel") or (meta or {}).get("baseModel"),
        "hideMeta": hidden,
        "acquisition": {"method": "page_next_data", "image_id": str(requested),
                        "image_query": ["image", "get"],
                        "generation_query": ["image", "getGenerationData"] if generation is not None else None},
    }
    return raw, page_preview(image_record, page), warnings


class Civitai:
    def __init__(self, transport=None, *, use_rest=True, resolve_versions=True, retries=2, timeout=25, sleep=asyncio.sleep):
        self.transport = transport
        self.use_rest = use_rest
        self.resolve_versions = resolve_versions
        self.retries = max(0, min(int(retries), 4))
        self.timeout = timeout
        self.sleep = sleep

    async def request(self, client, url, *, limit, hosts, params=None):
        """Bound response size and redirects; retry transient failures only."""
        for attempt in range(self.retries + 1):
            try:
                current, query = url, params
                for redirect in range(4):
                    if not safe_url(current, hosts):
                        raise Problem("Civitai supplied an unsupported download or redirect address.", 502)
                    async with client.stream("GET", current, params=query) as response:
                        if response.status_code in {301, 302, 303, 307, 308}:
                            location = response.headers.get("location")
                            if not location or redirect == 3:
                                raise Problem("Civitai returned an invalid redirect chain.", 502)
                            current = urljoin(str(response.url), location)
                            query = None
                            continue
                        response.raise_for_status()
                        chunks, size = [], 0
                        async for chunk in response.aiter_bytes():
                            size += len(chunk)
                            if size > limit:
                                raise Problem("Civitai's response exceeds the import size limit.", 502)
                            chunks.append(chunk)
                        return b"".join(chunks), response.headers.get("content-type", ""), current
            except (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError):
                if attempt == self.retries:
                    raise
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code not in {429, 500, 502, 503, 504} or attempt == self.retries:
                    raise
            await self.sleep(min(0.25 * 2**attempt, 2))

    async def model_versions(self, client, host, raw):
        """Retain file candidates for explicitly referenced versions, not gallery recipes."""
        from .domain import normalize

        identifiers = sorted({str(r["version_id"]) for r in normalize(raw)["resources"]
                              if re.fullmatch(r"[1-9][0-9]{0,17}", str(r["version_id"]))})
        evidence = []
        for identifier in identifiers[:16]:
            entry = {"version_id": identifier, "status": "unavailable"}
            try:
                body, _, _ = await self.request(client, f"https://{host}/api/v1/model-versions/{identifier}",
                                                limit=MAX_JSON, hosts={host})
                version = json.loads(body)
                if not isinstance(version, dict) or not same_id(version.get("id"), identifier):
                    raise ValueError("Mismatched version")
                files = [
                    {key: file[key] for key in ("id", "name", "type", "sizeKB", "hashes", "metadata", "primary") if key in file}
                    for file in version.get("files", []) if isinstance(file, dict)
                ]
                entry.update(status="identified", model_id=version.get("modelId"), files=files,
                             name=version.get("name"), base_model=version.get("baseModel"))
            except (httpx.HTTPError, Problem, ValueError, TypeError):
                pass
            evidence.append(entry)
        return evidence

    async def acquire(self, url: str):
        requested = image_id(url)
        host = urlsplit(url.strip()).hostname
        page_url = f"https://{host}/images/{requested}"
        async with httpx.AsyncClient(transport=self.transport, timeout=self.timeout, follow_redirects=False,
                                    headers={"User-Agent": USER_AGENT}) as client:
            try:
                content, _, final_url = await self.request(client, page_url, limit=MAX_HTML, hosts={host})
                if image_id(final_url) != requested:
                    raise Problem("Civitai redirected to a different image. No recipe was imported.", 502)
                raw, preview, warnings = parse_page(content.decode("utf-8"), requested)
                raw["acquisition"]["page_url"] = page_url
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if status in {401, 403}:
                    raise Problem("Civitai declined this image-page request. Retry later or import the original image file.", 502) from exc
                if status == 404:
                    raise Problem("This Civitai image was not found.", 404) from exc
                if status == 429:
                    raise Problem("Civitai is rate limiting requests. Try this import again later.", 503) from exc
                raise Problem("Civitai could not return the image page. Try again later.", 502) from exc
            except (httpx.HTTPError, UnicodeError, ValueError) as exc:
                raise Problem("Civitai could not be reached or returned an unreadable image page.", 502) from exc

            if self.use_rest:
                try:
                    body, _, _ = await self.request(client, f"https://{host}/api/v1/images", limit=MAX_JSON,
                                                   hosts={host}, params={"imageId": requested, "limit": 1})
                    data = json.loads(body)
                    items = data.get("items") if isinstance(data, dict) else None
                    matches = [item for item in items if isinstance(item, dict) and same_id(item.get("id"), requested)] if isinstance(items, list) else []
                    if len(matches) == 1 and safe_url(matches[0].get("url"), {"image.civitai.com"}):
                        preview = matches[0]["url"]
                        raw["acquisition"]["preview_source"] = "rest_image_url"
                    # REST metadata never replaces the page metadata.
                except (httpx.HTTPError, Problem, ValueError, TypeError):
                    pass
            raw["url"] = preview
            if self.resolve_versions:
                raw["model_versions"] = await self.model_versions(client, host, raw)
                if any(v["status"] == "unavailable" for v in raw["model_versions"]):
                    warnings.append("Some model-version details could not be retrieved. Their source identities are saved; retry the import later.")
            image = None
            if preview:
                raw["acquisition"].setdefault("preview_source", "page_cdn_reference")
                try:
                    image, content_type, final_image_url = await self.request(
                        client, preview, limit=MAX_IMAGE, hosts=IMAGE_HOSTS)
                    if content_type.split(";", 1)[0].strip().lower() not in {"image/png", "image/jpeg", "image/webp"}:
                        image = None
                    else:
                        raw["acquisition"]["download_url"] = final_image_url
                except (httpx.HTTPError, Problem):
                    image = None
            if image is None:
                warnings.append("Recipe saved; the source preview could not be downloaded.")
            return requested, redact(raw), image, " ".join(warnings) or None


def redact(value):
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items() if k.lower() not in {"token", "accesstoken", "apikey", "authorization"}}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str) and value.startswith(("https://", "http://")):
        try:
            parsed = urlsplit(value)
            if parsed.query or parsed.username or parsed.password:
                return "[transient URL omitted]"
        except ValueError:
            return "[invalid URL omitted]"
    return value
