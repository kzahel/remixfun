"""Bounded imported SDXL attempts; never alter the source or infer exactness."""
import copy
import hashlib
import io
import json

from PIL import Image, ImageChops, ImageStat
from .domain import Problem

IMPORT_PROFILE = "sdxl-import-attempt-v1"
SAMPLERS = {"euler": "euler", "euler a": "euler_ancestral",
            "euler ancestral": "euler_ancestral", "euler_ancestral": "euler_ancestral",
            "dpm++ 2m sde": "dpmpp_2m_sde", "dpmpp_2m_sde": "dpmpp_2m_sde"}
SCHEDULERS = {"normal", "karras", "exponential", "sgm_uniform", "simple", "ddim_uniform", "beta", "linear_quadratic", "kl_optimal"}
META_FIELDS = {"prompt", "negativePrompt", "seed", "Seed", "steps", "Steps", "cfgScale", "CFG scale",
               "sampler", "Sampler", "scheduler", "Schedule type", "clipSkip", "Clip skip", "width", "height",
               "Size", "Batch pos", "batchPosition", "Batch size", "batchSize", "resources", "civitaiResources",
               "Created Date", "extra", "baseModel", "Model", "Model hash", "version", "Version"}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def attempt_plan(record, dependencies, seed_offset=0):
    if isinstance(seed_offset, bool) or not isinstance(seed_offset, int) or not 0 <= seed_offset <= 31:
        raise Problem("Seed offset must be an integer from 0 to 31.")
    recipe = copy.deepcopy(record["recipe"])
    fields = recipe["fields"]
    raw = record["raw"]
    meta = raw.get("meta") or {}
    generation = raw.get("generation_data") or {}
    blockers, assumptions, mappings = [], [], []
    files = [d.get("file") for d in dependencies]
    checkpoint = files[0] if len(files) == 1 else None
    if not checkpoint or checkpoint.get("role") != "checkpoint" or checkpoint.get("base_model") != "SDXL 1.0":
        blockers.append("This attempt requires one resolved SDXL 1.0 checkpoint and no additional model stages.")
    if checkpoint and meta.get("Model hash") and str(meta["Model hash"]).lower() not in {str(v).lower() for v in checkpoint.get("hashes", {}).values()}:
        blockers.append("The reported model hash conflicts with the selected checkpoint file.")
    known_meta = set(META_FIELDS)
    hashes = meta.get("hashes")
    if isinstance(hashes, dict) and set(hashes) == {"model"} and checkpoint and str(hashes["model"]).lower() in {str(v).lower() for v in checkpoint.get("hashes", {}).values()}:
        known_meta.add("hashes")
        mappings.append({"field": "hashes.model", "source": hashes["model"], "effective": checkpoint["sha256"]})
    style_keys = {"Style Selector Style", "Style Selector Enabled", "Style Selector Randomize"}
    if meta.get("Style Selector Style") == "base" and str(meta.get("Style Selector Randomize")).lower() == "false":
        known_meta.update(style_keys)
        assumptions.append({"field": "style_selector", "value": "use_recorded_prompts",
                            "reason": "Style Selector reports base with randomization disabled; use the recorded prompts without reapplying an extension."})
    for dependency in dependencies:
        if dependency["status"] != "available":
            blockers.append(f"{dependency['name']}: {dependency.get('message') or 'download and verify the selected model'}.")
    missing = [key for key in recipe["unknown"] if key != "scheduler"]
    if missing:
        blockers.append("Missing required source settings: " + ", ".join(missing) + ".")
    sampler = SAMPLERS.get(str(fields.get("sampler")).strip().lower())
    if not sampler:
        blockers.append("The imported attempt currently supports Euler, Euler a and DPM++ 2M SDE samplers.")
    else:
        mappings.append({"field": "sampler", "source": fields["sampler"], "effective": sampler})
        fields["sampler"] = sampler
    if fields.get("scheduler") is None:
        assumptions.append({"field": "scheduler", "value": "normal", "reason": "The source does not specify a scheduler; this attempt uses normal."})
        fields["scheduler"] = "normal"
    else:
        scheduler = fields["scheduler"].strip().lower()
        if scheduler not in SCHEDULERS:
            blockers.append(f"Source scheduler {fields['scheduler']} has no supported mapping.")
        else:
            fields["scheduler"] = scheduler
    clip = fields.get("clip_skip")
    if clip is None:
        assumptions.append({"field": "clip_skip", "value": 2, "reason": "CLIP skip is unreported; use this SDXL runtime's penultimate layer (2)."})
        fields["clip_skip"] = 2
    elif not 1 <= clip <= 12:
        blockers.append("Source CLIP skip is outside the supported range (1–12).")
    mappings.append({"field": "clip_skip", "source": clip, "effective": -fields["clip_skip"],
                     "meaning": "Absolute CLIP hidden-layer index for both SDXL text encoders; not an additional skip."})
    if fields.get("batch_position") not in {None, 0} or fields.get("batch_size") not in {None, 1}:
        blockers.append("Explicit source batching requires a supported batch replay; this attempt handles one image at position zero.")
    elif fields.get("batch_position") is None or fields.get("batch_size") is None:
        assumptions.append({"field": "batch", "value": {"size": 1, "position": 0, "seed_offset": seed_offset},
                            "reason": f"Batch details are incomplete; try one image at the recorded seed plus {seed_offset}. This tests incremented seeds, not a shared-seed noise stream."})
    if seed_offset:
        if record["recipe"]["fields"].get("batch_position") is not None:
            blockers.append("An explicit source batch position cannot be replaced by a seed-offset hypothesis.")
        elif fields.get("seed") is not None:
            effective_seed = int(fields["seed"]) + seed_offset
            if effective_seed >= 2**64:
                blockers.append("The effective seed exceeds the unsigned 64-bit range.")
            else:
                fields["seed"] = str(effective_seed)
                mappings.append({"field": "seed", "source": record["recipe"]["fields"]["seed"], "effective": fields["seed"], "offset": seed_offset})
    fields.update(batch_size=1, batch_position=0)
    recipe["batch_strategy"] = "incremented_seed_hypothesis" if seed_offset else "single_image_recorded_seed"
    recipe["unknown"] = missing
    recipe["readiness"] = "attempt"
    process = generation.get("process")
    if process is not None and process != "txt2img":
        blockers.append(f"Source process {process} requires a separate generation profile.")
    elif process is None:
        assumptions.append({"field": "process", "value": "txt2img", "reason": "Source process is unreported; attempt text-to-image."})
    extras = sorted(set(meta) - known_meta)
    if extras or meta.get("extra") or generation.get("tools") or generation.get("techniques") or generation.get("external") or raw.get("embedded_metadata", {}).get("workflow"):
        blockers.append("Additional source settings or stages need support before running: " + ", ".join(extras or ["extra metadata / tools / workflow"]) + ".")
    if any(token in (fields.get("prompt") or "").lower() + (fields.get("negative_prompt") or "").lower()
           for token in ("<lora:", "<lyco:", "embedding:")):
        blockers.append("Prompt model references require explicit dependency and conditioning support.")
    if (fields.get("steps") is not None and not 1 <= fields["steps"] <= 100
        or fields.get("cfg") is not None and not 0 <= fields["cfg"] <= 20
        or any(fields.get(k) is not None and (not 256 <= fields[k] <= 1536 or fields[k] % 64) for k in ("width", "height"))):
        blockers.append("Source dimensions, steps or guidance exceed the supported generation limits.")
    assumptions.append({"field": "execution", "value": "pinned_comfy_sdxl",
                        "reason": "Use Comfy's text encoding and seeded noise. The source generator's numerical behavior is unverified."})
    plan = {"profile": IMPORT_PROFILE, "seed_offset": seed_offset, "source_manifest_sha256": digest(record), "checkpoint": checkpoint,
            "effective_recipe": recipe, "assumptions": assumptions, "mappings": mappings, "blockers": blockers,
            "ready": not blockers, "reference_quality": record["source"].get("reference_quality")}
    plan["revision"] = digest(plan)
    return plan


def compare_reference(reference, generated, quality):
    """Compare decoded RGBA pixels, without resizing or treating JPEG as original."""
    with Image.open(io.BytesIO(reference)) as source, Image.open(io.BytesIO(generated)) as output:
        result = {"method": "decoded_rgba_no_resize", "reference_quality": quality,
                  "source_size": list(source.size), "output_size": list(output.size), "exact_reproduction": False}
        if source.size != output.size:
            return {**result, "status": "different_dimensions"}
        delta = ImageChops.difference(source.convert("RGBA"), output.convert("RGBA"))
        channels = delta.split()
        maximum = channels[0]
        for channel in channels[1:]:
            maximum = ImageChops.lighter(maximum, channel)
        different_pixels = source.width * source.height - maximum.histogram()[0]
        equal = different_pixels == 0
        stats = ImageStat.Stat(delta)
        return {**result, "status": "equal_reference_pixels" if equal else "different_pixels",
                "different_pixels": different_pixels, "total_pixels": source.width * source.height,
                "maximum_channel_error": max(high for low, high in delta.getextrema()),
                "root_mean_square_rgb_error": (sum(v * v for v in stats.rms[:3]) / 3) ** .5,
                "mean_absolute_rgb_error": sum(stats.mean[:3]) / 3}
