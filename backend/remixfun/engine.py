"""Managed, loopback-only Comfy runtime and a deliberately narrow SDXL graph."""
import asyncio
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import time

import httpx

from .domain import Problem
from .reproduction import IMPORT_PROFILE, SCHEDULERS, SAMPLERS

COMFY_REVISION = "40c4fcdf513a4523e39d54a9d391908af8df8171"
CHECKPOINT = "sd_xl_base_1.0.safetensors"
CHECKPOINT_SHA256 = "31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b"
PROFILE = "sdxl-base-txt2img-v1"
MODEL_PROFILE = "sdxl-checkpoint-txt2img-v1"


def reproduction_blockers(record):
    """Explain the current imported-source boundary without filling missing fields."""
    recipe = record["recipe"]
    blockers = []
    if recipe["unknown"]:
        blockers.append("Missing source settings: " + ", ".join(recipe["unknown"]) + ". Obtain the original generation settings; missing values will not be guessed.")
    for resource in recipe["resources"]:
        label = resource["name"]
        if resource.get("version_id") is not None:
            label += f" (version {resource['version_id']})"
        files = resource.get("files", [])
        candidates = [f for f in files if f.get("type") == "Model"]
        hashes = [f["hashes"]["SHA256"].lower() for f in candidates
                  if isinstance(f.get("hashes"), dict)
                  and isinstance(f["hashes"].get("SHA256"), str)
                  and re.fullmatch(r"[a-fA-F0-9]{64}", f["hashes"]["SHA256"])]
        if hashes and len(hashes) == len(candidates) and all(h != CHECKPOINT_SHA256 for h in hashes) and resource["type"].lower() == "checkpoint":
            blockers.append(f"{label} requires checkpoint bytes different from the configured SDXL Base model. Acquire and verify the exact source model before trying reproduction.")
        else:
            blockers.append(f"{label}: exact source file and local availability have not been verified.")
    fields = recipe["fields"]
    if fields.get("sampler") is not None and fields["sampler"] != "euler":
        blockers.append(f"Source sampler {fields['sampler']} needs a supported mapping; the current profile supports Euler / normal only.")
    if fields.get("clip_skip") is not None:
        blockers.append(f"Source clip skip {fields['clip_skip']} needs a tested source-compatible conditioning profile.")
    blockers.append("Imported-source generation profiles are not connected yet. No model was substituted.")
    return blockers


def workflow(record):
    raw = record["raw"]
    binding = raw.get("model_binding")
    imported = raw.get("generation_profile") == IMPORT_PROFILE and record.get("source", {}).get("kind") in {"civitai", "file"}
    selected = ((raw.get("generation_profile") == MODEL_PROFILE and record.get("source", {}).get("kind") == "authored" or imported)
                and isinstance(binding, dict) and binding.get("sha256") == raw.get("checkpoint_sha256")
                and re.fullmatch(r"[a-f0-9]{64}", str(binding.get("sha256")))
                and binding.get("filename") == binding["sha256"] + ".safetensors"
                and binding.get("file", {}).get("base_model") == "SDXL 1.0"
                and binding.get("file", {}).get("role") == "checkpoint")
    if not selected and (raw.get("generation_profile") != PROFILE or raw.get("checkpoint_sha256") != CHECKPOINT_SHA256):
        raise Problem(" ".join(reproduction_blockers(record)), 409)
    fields = record["recipe"]["fields"]
    required = ("prompt", "negative_prompt", "seed", "steps", "cfg", "width", "height", "sampler", "scheduler")
    if any(fields.get(key) is None for key in required):
        raise Problem("Generation settings are incomplete. Missing values will not be guessed.", 409)
    if imported and (fields["sampler"] not in set(SAMPLERS.values()) or fields["scheduler"] not in SCHEDULERS
                     or fields.get("clip_skip") not in range(1, 13) or fields.get("batch_size") != 1 or fields.get("batch_position") != 0):
        raise Problem("The effective imported recipe exceeds this attempt profile.", 409)
    if not imported and (fields["sampler"] != "euler" or fields["scheduler"] != "normal"):
        raise Problem("This runtime profile supports Euler with the normal scheduler only.", 409)
    if not (1 <= fields["steps"] <= 100 and 0 <= fields["cfg"] <= 20
            and 0 <= int(fields["seed"]) < 2**64
            and all(256 <= fields[key] <= 1536 and fields[key] % 64 == 0 for key in ("width", "height"))):
        raise Problem("Generation settings exceed the supported profile limits.", 409)
    graph = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": binding["filename"] if selected else CHECKPOINT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": fields["prompt"], "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": fields["negative_prompt"], "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": fields["width"], "height": fields["height"], "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {"seed": int(fields["seed"]), "steps": fields["steps"],
            "cfg": fields["cfg"], "sampler_name": fields["sampler"], "scheduler": fields["scheduler"],
            "denoise": 1.0, "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "remixfun/generated"}},
    }
    if imported:
        graph["8"] = {"class_type": "CLIPSetLastLayer", "inputs": {"clip": ["1", 1], "stop_at_clip_layer": -fields["clip_skip"]}}
        graph["2"]["inputs"]["clip"] = ["8", 0]
        graph["3"]["inputs"]["clip"] = ["8", 0]
    return graph


class Comfy:
    def __init__(self, root: Path, log_dir: Path):
        self.root = root.resolve()
        self.log_dir = log_dir
        self.process = None
        self.log = None
        self.url = None
        self.identity = None
        self.verified_stat = None
        self.inventory = None

    def verify_checkpoint(self):
        path = self.root / "models" / "checkpoints" / CHECKPOINT
        try:
            stat = path.stat()
            identity = (stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns)
            if identity != self.verified_stat:
                with path.open("rb") as stream:
                    digest = hashlib.file_digest(stream, "sha256").hexdigest()
                if digest != CHECKPOINT_SHA256:
                    raise Problem("The SDXL checkpoint does not match the required SHA-256. Generation was stopped.", 409)
                self.verified_stat = identity
        except OSError as exc:
            raise Problem("The SDXL base checkpoint is missing or unreadable. Complete the local runtime setup.", 409) from exc

    async def start(self):
        revision = await asyncio.to_thread(subprocess.check_output, ["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True)
        if revision.strip() != COMFY_REVISION:
            raise Problem("The Comfy checkout differs from the tested runtime revision.", 409)
        python = self.root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        self.url = f"http://127.0.0.1:{port}"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log = (self.log_dir / "comfy.log").open("ab")
        try:
            model_args = []
            if self.inventory:
                from .model_resolution import ROLES
                config = self.log_dir / "model-paths.yaml"
                config.write_text(json.dumps({"remixfun": {"base_path": str(self.inventory.root / "comfy"),
                    **{folder: folder for folder in ROLES.values()}}}), encoding="utf-8")
                model_args = ["--extra-model-paths-config", str(config.resolve())]
            self.process = subprocess.Popen([str(python), "main.py", "--listen", "127.0.0.1", "--port", str(port),
                "--disable-auto-launch", "--disable-all-custom-nodes", "--disable-api-nodes", "--disable-comfy-compiler", *model_args],
                cwd=self.root, stdout=self.log, stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            async with httpx.AsyncClient(base_url=self.url, timeout=5, trust_env=False) as client:
                deadline = time.monotonic() + 120
                while time.monotonic() < deadline:
                    if self.process.poll() is not None:
                        raise Problem("The generation runtime exited during startup. See the local Comfy log.", 503)
                    try:
                        response = await client.get("/system_stats")
                        response.raise_for_status()
                        stats = response.json()
                        if not any(device.get("type") == "cuda" for device in stats.get("devices", [])):
                            raise Problem("The SDXL GPU profile requires an available CUDA device.", 503)
                        system = stats["system"]
                        self.identity = {"comfy_revision": COMFY_REVISION, "default_checkpoint_sha256": CHECKPOINT_SHA256,
                            "supported_profiles": [PROFILE, MODEL_PROFILE, IMPORT_PROFILE], "torch_version": system.get("pytorch_version"),
                            "python_version": system.get("python_version")}
                        return
                    except httpx.HTTPError:
                        await asyncio.sleep(0.5)
            raise Problem("The generation runtime did not become ready. See the local Comfy log.", 503)
        except BaseException:
            await self.close()
            raise

    async def generate(self, graph, accepted, *, timeout=600):
        if self.process is None or self.process.poll() is not None:
            raise Problem("The generation runtime is not running. Restart the service.", 503)
        name = graph.get("1", {}).get("inputs", {}).get("ckpt_name", CHECKPOINT)
        if name == CHECKPOINT:
            await asyncio.to_thread(self.verify_checkpoint)
        else:
            if not self.inventory or not re.fullmatch(r"[a-f0-9]{64}\.safetensors", name):
                raise Problem("The workflow has no verified model binding.", 409)
            blob = self.inventory.available(name[:-12])
            if not blob:
                raise Problem("The selected model is missing or changed. Verify it again before generation.", 409)
            binding = await asyncio.to_thread(self.inventory.bind, blob["file"])
            await asyncio.to_thread(self.inventory.verify, Path(binding["path"]), binding["sha256"])
            collision = self.root / "models" / "checkpoints" / name
            if collision.exists() and not os.path.samefile(collision, binding["path"]):
                raise Problem("Comfy has an ambiguous model filename. Resolve the collision before generation.", 409)
        async with httpx.AsyncClient(base_url=self.url, timeout=30, trust_env=False) as client:
            # Submission is deliberately never retried: a lost response could already
            # have created a GPU job. Preserve uncertainty instead of duplicating it.
            response = await client.post("/prompt", json={"prompt": graph})
            response.raise_for_status()
            prompt_id = response.json()["prompt_id"]
            accepted(prompt_id)
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                if self.process.poll() is not None:
                    raise Problem("The generation runtime stopped before saving an output.", 503)
                response = await client.get(f"/history/{prompt_id}")
                response.raise_for_status()
                record = response.json().get(prompt_id)
                if record:
                    if record.get("status", {}).get("status_str") == "error":
                        raise Problem("Comfy could not generate this image. See the local Comfy log.", 502)
                    images = record.get("outputs", {}).get("7", {}).get("images", [])
                    if record.get("status", {}).get("completed") and not images:
                        raise Problem("The generation finished without an image.", 502)
                    if images:
                        if len(images) != 1 or images[0].get("type") != "output":
                            raise Problem("The generation returned an unexpected output set.", 502)
                        output = images[0]
                        async with client.stream("GET", "/view", params={key: output[key] for key in ("filename", "subfolder", "type")}) as download:
                            download.raise_for_status()
                            content = bytearray()
                            async for chunk in download.aiter_bytes():
                                content.extend(chunk)
                                if len(content) > 25 * 1024 * 1024:
                                    raise Problem("The generated image exceeds the output size limit.", 502)
                        return bytes(content)
                await asyncio.sleep(0.5)
            raise Problem("Generation monitoring timed out. The runtime may still be working; inspect it before retrying.", 504)

    async def close(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                await asyncio.to_thread(self.process.wait, timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                await asyncio.to_thread(self.process.wait, timeout=10)
        if self.log:
            self.log.close()
