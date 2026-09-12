"""Conservative normalization. Source evidence never becomes implicit defaults."""

import re
from urllib.parse import urlsplit


class Problem(Exception):
    def __init__(self, message: str, status: int = 422):
        self.message = message
        self.status = status
        super().__init__(message)


def image_id(url: str) -> str:
    try:
        parsed = urlsplit(url.strip())
        valid = (parsed.scheme == "https" and parsed.hostname in {"civitai.com", "www.civitai.com", "civitai.green"}
                 and parsed.port in {None, 443} and not parsed.username and not parsed.password)
    except ValueError:
        valid = False
    match = re.fullmatch(r"/images/([1-9][0-9]{0,17})/?", parsed.path) if valid else None
    if not match:
        raise Problem("Paste a Civitai image link, such as https://civitai.com/images/12345.")
    return match[1]


def numeric(value, *, integer=False, maximum=None):
    if isinstance(value, bool) or value is None:
        return None
    try:
        text = str(value).strip()
        if integer and not re.fullmatch(r"[0-9]+", text):
            return None
        result = int(text) if integer else float(text)
        if result < 0 or result != result or result == float("inf") or (maximum is not None and result > maximum):
            return None
        return result
    except (ValueError, TypeError, OverflowError):
        return None


def normalize(raw: dict) -> dict:
    meta = raw.get("meta") if isinstance(raw.get("meta"), dict) else {}
    aliases = {
        "prompt": ["prompt"], "negative_prompt": ["negativePrompt"],
        "seed": ["seed", "Seed"], "steps": ["steps", "Steps"],
        "cfg": ["cfgScale", "CFG scale"], "sampler": ["sampler", "Sampler"],
        "scheduler": ["scheduler", "Schedule type"], "clip_skip": ["clipSkip", "Clip skip"],
        "width": ["width"], "height": ["height"],
        "batch_position": ["Batch pos", "batchPosition"], "batch_size": ["Batch size", "batchSize"],
    }
    fields, provenance = {}, {}
    for field, keys in aliases.items():
        key = next((key for key in keys if key in meta), None)
        value = meta.get(key) if key else None
        if field in {"prompt", "negative_prompt", "sampler", "scheduler"}:
            value = value if isinstance(value, str) else None
        else:
            value = numeric(value, integer=field != "cfg", maximum=2**64 - 1 if field == "seed" else None)
        # Decimal strings cross JavaScript without loss of 64-bit seed precision.
        fields[field] = str(value) if field == "seed" and value is not None else value
        if key and value is not None:
            provenance[field] = f"meta.{key}"
    size = meta.get("Size")
    if isinstance(size, str) and (match := re.fullmatch(r"(\d+)x(\d+)", size.strip())):
        for field, value in zip(("width", "height"), match.groups()):
            if fields[field] is None:
                fields[field] = int(value)
                provenance[field] = "meta.Size"
    resources = []
    generation = raw.get("generation_data") if isinstance(raw.get("generation_data"), dict) else {}
    sources = [("meta.civitaiResources", meta.get("civitaiResources")),
               ("meta.resources", meta.get("resources")),
               ("generation_data.resources", generation.get("resources"))]
    for evidence, source in sources:
        if not isinstance(source, list):
            continue
        for item in source:
            if not isinstance(item, dict):
                continue
            resources.append({
                "name": str(item.get("name") or item.get("modelName") or "Unidentified resource"),
                "type": str(item.get("type") or item.get("modelType") or "unknown"),
                "model_id": item.get("modelId"),
                "version_id": item.get("modelVersionId") or item.get("versionId"),
                "file_id": item.get("fileId"), "hash": item.get("hash"),
                "weight": item.get("weight", item.get("strength")), "evidence": evidence,
                "base_model": item.get("baseModel"),
                "version_name": item.get("versionName"),
                "status": "unresolved",
            })
    # The page repeats a dependency in meta and generation_data. Coalesce only
    # complementary evidence for the same explicit version; retain conflicts.
    combined = []
    for resource in resources:
        match = next((old for old in combined if resource["version_id"] is not None
                      and str(old["version_id"]) == str(resource["version_id"])
                      and old["type"].lower() == resource["type"].lower()
                      and all(old[key] is None or resource[key] is None or old[key] == resource[key]
                              for key in ("model_id", "file_id", "hash", "weight", "base_model"))
                      and resource["evidence"] not in old["evidence_sources"]), None)
        if match is None:
            combined.append({**resource, "evidence_sources": [resource["evidence"]]})
        else:
            match["evidence_sources"].append(resource["evidence"])
            for key, value in resource.items():
                if match.get(key) is None or (key == "name" and match[key] == "Unidentified resource"):
                    match[key] = value
    resources = combined
    versions = raw.get("model_versions")
    for resource in resources:
        resource["files"] = []
        for version in versions if isinstance(versions, list) else []:
            if (isinstance(version, dict) and version.get("status") == "identified"
                    and resource["version_id"] is not None
                    and str(version.get("version_id")) == str(resource["version_id"])
                    and (resource["model_id"] is None or resource["model_id"] == version.get("model_id"))):
                resource["version_name"] = resource["version_name"] or version.get("name")
                resource["files"] = version.get("files", [])
                # A version's candidates do not prove which file created the source.
                # Reported source hash/file identity stays separate and unresolved.
    required = ("prompt", "negative_prompt", "seed", "steps", "cfg", "sampler", "scheduler", "width", "height")
    unknown = [key for key in required if fields[key] is None]
    return {"fields": fields, "provenance": provenance, "resources": resources, "unknown": unknown,
            "batch_strategy": "unknown", "readiness": "needs_resolution"}


def parse_parameters(text: str) -> dict:
    """Read common A1111 fields without guessing missing scheduler or dimensions."""
    match = re.search(r"(?:^|\n)Steps:\s*", text)
    if not match:
        return {"prompt": text}
    prompt = text[:match.start()].strip()
    parts = prompt.split("Negative prompt:", 1)
    result = {"prompt": parts[0].strip()}
    if len(parts) == 2:
        result["negativePrompt"] = parts[1].strip()
    tail = text[match.start():].strip()
    mapping = {"Steps": "steps", "Sampler": "sampler", "Schedule type": "scheduler", "CFG scale": "cfgScale",
               "Seed": "seed", "Size": "Size", "Clip skip": "clipSkip", "Batch pos": "Batch pos", "Batch size": "Batch size"}
    for source, dest in mapping.items():
        found = re.search(r"(?:^|,\s*)" + re.escape(source) + r":\s*([^,\n]+)", tail)
        if found:
            result[dest] = found[1].strip()
    return result
