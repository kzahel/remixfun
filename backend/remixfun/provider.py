"""Civitai acquisition. Only explicit Civitai hosts can be fetched."""

import httpx
from urllib.parse import urlsplit

from .domain import Problem, image_id

MAX_IMAGE = 25 * 1024 * 1024


class Civitai:
    def __init__(self, transport=None):
        self.transport = transport

    async def acquire(self, url: str):
        source_id = image_id(url)
        async with httpx.AsyncClient(transport=self.transport, timeout=25, follow_redirects=False,
                                    headers={"User-Agent": "Remixfun/0.1 (image recipe import)"}) as client:
            try:
                response = await client.get("https://civitai.com/api/v1/images",
                                            params={"imageId": source_id, "withMeta": "true", "limit": 1})
                if response.status_code in {401, 403}:
                    raise Problem("Civitai denied access. Save the original PNG from Civitai and import it here; authenticated imports are not available yet.", 502)
                if response.status_code == 429:
                    raise Problem("Civitai is rate limiting requests. Try this import again later.", 503)
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, dict) or not isinstance(data.get("items"), list):
                    raise ValueError("Invalid provider envelope")
                item = next((x for x in data["items"] if isinstance(x, dict) and str(x.get("id")) == source_id), None)
                if item is None:
                    raise Problem("This image is unavailable or private on Civitai. Try an original PNG instead.", 404)
                content, warning = None, None
                preview_url = item.get("url")
                if isinstance(preview_url, str):
                    parsed = urlsplit(preview_url)
                    if parsed.scheme == "https" and parsed.hostname == "image.civitai.com" and not parsed.query and not parsed.username and parsed.port in {None, 443}:
                        async with client.stream("GET", preview_url) as image:
                            if image.status_code == 200:
                                chunks, size = [], 0
                                async for chunk in image.aiter_bytes():
                                    size += len(chunk)
                                    if size > MAX_IMAGE:
                                        raise Problem("Source image exceeds the 25 MB import limit.")
                                    chunks.append(chunk)
                                content = b"".join(chunks)
                if content is None:
                    warning = "Recipe saved; the source preview could not be downloaded."
                # Signed URLs and provider credentials must not enter source exports.
                item = redact(item)
                return source_id, item, content, warning
            except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
                raise Problem("Civitai could not be reached or returned an unreadable response. Retry, or import an original PNG.", 502) from exc


def redact(value):
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items() if k.lower() not in {"token", "accesstoken", "apikey", "authorization"}}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str) and value.startswith(("https://", "http://")):
        parsed = urlsplit(value)
        if parsed.query or parsed.username or parsed.password:
            return "[transient URL omitted]"
    return value
