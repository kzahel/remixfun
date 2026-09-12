"""File-level dependency plans. No recipe defaults or model substitutions."""
import copy
import hashlib
import json
import re

from .domain import normalize, numeric

ROLES = {"checkpoint": "checkpoints", "lora": "loras", "vae": "vae"}


def sha256(value):
    return value.lower() if isinstance(value, str) and re.fullmatch(r"[a-fA-F0-9]{64}", value) else None


def build_plan(record, versions=None, choices=None):
    raw = copy.deepcopy(record["raw"])
    if versions is not None:
        raw["model_versions"] = versions
    resources = normalize(raw)["resources"]
    # A1111 hash-only "model" entries can repeat a Civitai version reference.
    # Merge only when provider file hashes establish one unambiguous identity.
    merged = []
    for resource in resources:
        reported = resource.get("hash")
        if resource.get("version_id") is None and resource["type"].lower() in {"model", "checkpoint"} and isinstance(reported, str) and re.fullmatch(r"[a-fA-F0-9]{8,64}", reported):
            matches = [other for other in resources if other.get("version_id") is not None
                       and other["type"].lower() == "checkpoint"
                       and any(isinstance(file.get("hashes"), dict) and reported.lower() in [str(h).lower() for h in file["hashes"].values()]
                               for file in other.get("files", []))]
            if len(matches) == 1:
                matches[0].setdefault("reported_hashes", []).append(reported)
                matches[0].setdefault("linked_source_evidence", []).append(resource)
                continue
        merged.append(resource)
    resources = merged
    entries = []
    for i, resource in enumerate(resources):
        role = resource["type"].lower()
        entry = {"id": str(i), "name": resource["name"], "role": role,
                 "version_id": resource["version_id"], "version_name": resource.get("version_name"),
                 "candidates": [], "file": None, "status": "blocked", "message": None}
        entry["linked_source_evidence"] = resource.get("linked_source_evidence", [])
        entries.append(entry)
        if role not in ROLES:
            entry["message"] = "This resource type is not supported for model acquisition yet."
            continue
        if not re.fullmatch(r"[1-9][0-9]{0,17}", str(resource["version_id"])):
            entry["message"] = "An exact Civitai version is required."
            continue
        for file in resource.get("files", []):
            digest = sha256((file.get("hashes") or {}).get("SHA256")) if isinstance(file.get("hashes"), dict) else None
            metadata = file.get("metadata") or {}
            if (not digest or not re.fullmatch(r"[1-9][0-9]{0,17}", str(file.get("id")))
                    or file.get("type") not in {"Model", "VAE"}
                    or not isinstance(file.get("name"), str) or not file["name"].lower().endswith(".safetensors")
                    or not isinstance(metadata, dict) or metadata.get("format", "SafeTensor") != "SafeTensor"):
                continue
            size = numeric(file.get("sizeKB"))
            entry["candidates"].append({"provider": "civitai", "model_id": resource["model_id"],
                "version_id": str(resource["version_id"]), "file_id": str(file["id"]), "sha256": digest,
                "name": file["name"], "role": role, "base_model": resource.get("base_model"),
                "size_estimate": int(size * 1024) if size is not None and size < 1024**3 else None,
                "metadata": metadata, "hashes": file["hashes"]})
        candidates = entry["candidates"]
        if resource.get("file_id") is not None:
            candidates = [f for f in candidates if f["file_id"] == str(resource["file_id"])]
        reported = resource.get("hash")
        for source_hash in ([reported] if reported is not None else []) + resource.get("reported_hashes", []):
            # Source hashes constrain selection even when they are only lookup clues.
            candidates = [f for f in candidates if isinstance(source_hash, str) and
                          source_hash.lower() in [str(h).lower() for h in f["hashes"].values()]]
        selected_id = (choices or {}).get(str(i))
        if selected_id is not None:
            candidates = [f for f in candidates if f["file_id"] == str(selected_id)]
        if len(candidates) == 1:
            entry.update(file=candidates[0], status="download_needed",
                         selection_reason="explicit_choice" if selected_id else
                         "source_file_identity" if resource.get("file_id") or sha256(reported) else
                         "source_hash_match" if resource.get("reported_hashes") else "only_compatible_file")
        elif len(candidates) > 1:
            entry.update(status="choose_file", message="Choose the file variant used by the source.")
        else:
            entry["message"] = "No supported file agrees with the source identity. Refresh metadata or check the original model version."
    identity = {"import_id": record["id"], "dependencies": entries}
    revision = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    return {**identity, "revision": revision}
