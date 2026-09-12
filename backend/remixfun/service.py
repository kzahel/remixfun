"""Application commands shared by HTTP, desktop and CLI clients."""

import asyncio
import io
import json
import uuid
import warnings
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from .domain import Problem, normalize, parse_parameters
from .engine import CHECKPOINT, CHECKPOINT_SHA256, PROFILE, MODEL_PROFILE, reproduction_blockers, workflow
from .provider import Civitai, redact
from .storage import Store
from .model_inventory import Inventory
from .model_resolution import build_plan
from .downloads import Downloads
from .provider import USER_AGENT
import httpx


def now():
    return datetime.now(timezone.utc).isoformat()


def inspect_image(content):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(content)) as img:
                if img.format not in {"PNG", "JPEG", "WEBP"}:
                    raise Problem("Use a PNG, JPEG, or WebP image.")
                info = {k: v for k, v in img.info.items() if isinstance(v, str)}
                details = {"width": img.width, "height": img.height, "encoding": img.format.lower()}
                img.verify()
                return details, info
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise Problem("This image is damaged, unsupported, or too large to decode safely.") from exc


class Service:
    def __init__(self, root, provider=None, demo_delay=1.5, engine=None, model_root=None, model_paths=(), download_transport=None):
        self.store = Store(root)
        self.provider = provider or Civitai(resolve_versions=False)
        self.auto_resolve = provider is None
        self.demo_delay = demo_delay
        self.tasks = set()
        self.engine = engine
        try:
            settings = self.store.get("model-settings", "config")
        except Problem:
            settings = {}
        self.inventory = Inventory(model_root or settings.get("model_root") or root / "models")
        self.downloads = Downloads(self.inventory, download_transport)
        self.model_paths = list(model_paths) or settings.get("model_paths", [])
        if engine and hasattr(engine, "root"):
            self.model_paths.append(engine.root / "models")
            engine.inventory = self.inventory
        self.operations = set()

    def model_settings(self):
        return {"model_root": str(self.inventory.root), "model_paths": [str(p) for p in self.model_paths],
                "civitai_key_configured": bool(self.downloads.transport.credentials.get())}

    def configure_models(self, model_root, model_paths):
        paths = [Path(p).expanduser() for p in [model_root, *model_paths]]
        if any(not p.is_absolute() for p in paths):
            raise Problem("Model folders must be absolute paths on the service's computer.")
        self.store.put({"id": "model-settings", "model_root": str(paths[0]),
                        "model_paths": [str(p) for p in paths[1:]]}, "config")
        self.model_paths = paths[1:]
        return {**self.model_settings(), "restart_required": paths[0].resolve() != self.inventory.root,
                "configured_model_root": str(paths[0])}

    async def start(self):
        await self.downloads.start()
        for operation in self.store.list("operation"):
            if operation["status"] in {"queued", "running"}:
                operation.update(status="interrupted", message="Service restarted; refresh to check models again.")
                self.store.put(operation, "operation")

    def dependencies(self, identifier):
        record = self.store.get(identifier)
        saved = self.inventory.get("plans", identifier) or {}
        plan = build_plan(record, saved.get("versions"), saved.get("choices"))
        jobs = {job["file"]["sha256"]: job for job in self.downloads.list()}
        required = {}
        for entry in plan["dependencies"]:
            file = entry["file"]
            if not file:
                continue
            blob = self.inventory.available(file["sha256"])
            job = jobs.get(file["sha256"])
            entry["download"] = job
            if blob:
                entry.update(status="available", message="SHA-256 verified", verified_sha256=blob["sha256"])
            else:
                required[file["sha256"]] = file.get("size_estimate")
                if job:
                    entry.update(status=job["status"] if job["status"] != "ready" else "download_needed", message=job["message"])
        blockers = []
        for dependency in plan["dependencies"]:
            if dependency["status"] != "available":
                file = dependency["file"]
                if file and file["role"] == "checkpoint" and file["sha256"] != CHECKPOINT_SHA256:
                    blockers.append(f"{dependency['name']} requires checkpoint bytes different from the configured SDXL Base model. Download and verify the selected file.")
                else:
                    blockers.append(f"{dependency['name']}: {dependency.get('message') or 'model acquisition is required'}.")
        if record["recipe"]["unknown"]:
            blockers.append("Missing source settings: " + ", ".join(record["recipe"]["unknown"]) + ".")
        blockers.append("Imported-source sampling and conditioning still need a supported generation profile. No model was substituted.")
        plan.update(total_download_bytes=sum(v for v in required.values() if v is not None),
                    unknown_sizes=sum(v is None for v in required.values()),
                    generation_blockers=blockers, operation=saved.get("operation"))
        if saved.get("operation"):
            plan["operation"] = self.store.get(saved["operation"], "operation")
        return plan

    def operation(self, kind, work):
        operation = {"id": str(uuid.uuid4()), "kind": kind, "status": "queued", "created_at": now()}
        self.store.put(operation, "operation")
        async def run():
            operation.update(status="running")
            self.store.put(operation, "operation")
            try:
                operation["result"] = await work()
                operation.update(status="completed")
            except Exception:
                operation.update(status="failed", message="Model lookup or verification failed. Check provider access and configured folders, then retry.")
            self.store.put(operation, "operation")
        task = asyncio.create_task(run())
        self.operations.add(task)
        task.add_done_callback(self.operations.discard)
        return operation

    def resolve_models(self, identifier):
        record = self.store.get(identifier)
        saved = self.inventory.get("plans", identifier) or {}
        if saved.get("operation"):
            previous = self.store.get(saved["operation"], "operation")
            if previous["status"] in {"queued", "running"}:
                return previous
        async def resolve():
            provider = self.provider if isinstance(self.provider, Civitai) else Civitai()
            key = self.downloads.transport.credentials.get()
            headers = {"User-Agent": USER_AGENT, **({"Authorization": f"Bearer {key}"} if key else {})}
            async with httpx.AsyncClient(transport=provider.transport, timeout=provider.timeout,
                                        headers=headers) as client:
                versions = await provider.model_versions(client, "civitai.com", record["raw"])
            current = self.inventory.get("plans", identifier) or {}
            current["versions"] = versions
            self.inventory.put("plans", identifier, current)
            # Revalidate discovered local files off the service event loop.
            plan = self.dependencies(identifier)
            if self.model_paths:
                await asyncio.to_thread(self.inventory.scan, self.model_paths,
                                        [d["file"] for d in plan["dependencies"] if d["file"]])
            return {"identified_versions": sum(v["status"] == "identified" for v in versions)}
        operation = self.operation("model_resolution", resolve)
        saved["operation"] = operation["id"]
        self.inventory.put("plans", identifier, saved)
        return operation

    def download_models(self, identifier, revision, choices=None):
        plan = self.dependencies(identifier)
        if plan["revision"] != revision:
            raise Problem("Model details changed. Review the refreshed download plan and try again.", 409)
        if choices:
            known = {d["id"] for d in plan["dependencies"]}
            if not set(choices) <= known:
                raise Problem("Unknown model dependency choice.")
            saved = self.inventory.get("plans", identifier) or {}
            selected = {**saved.get("choices", {}), **choices}
            proposed = build_plan(self.store.get(identifier), saved.get("versions"), selected)
            if any(d["id"] in choices and d["file"] is None for d in proposed["dependencies"]):
                raise Problem("That file choice conflicts with the source identity or current model metadata.", 409)
            saved["choices"] = selected
            self.inventory.put("plans", identifier, saved)
            plan = self.dependencies(identifier)
        results = {}
        for dependency in plan["dependencies"]:
            if dependency["file"]:
                try:
                    results[dependency["id"]] = self.downloads.enqueue(dependency["file"], f"{identifier}:{dependency['id']}")
                except Problem as exc:
                    results[dependency["id"]] = {"status": "blocked", "message": exc.message}
            else:
                results[dependency["id"]] = {"status": dependency["status"], "message": dependency["message"]}
        return {"dependencies": results, "plan": self.dependencies(identifier)}

    def scan_models(self):
        files = [d["file"] for r in self.store.list() for d in self.dependencies(r["id"])["dependencies"] if d["file"]]
        async def scan():
            return await asyncio.to_thread(self.inventory.scan, self.model_paths, files)
        return self.operation("model_scan", scan)

    def recover(self):
        for job in self.store.list("job"):
            if job["status"] in {"queued", "running", "unknown"}:
                job.update(status="interrupted", message="The service stopped before this job finished. It was not automatically resubmitted.", finished_at=now())
                self.store.put(job, "job")

    def save(self, raw, content, source, title, demo=False, warning=None, extension=None):
        recipe = normalize(raw)
        media, image = None, None
        if content:
            if extension == "svg":
                image = {"width": 960, "height": 1120, "encoding": "svg"}
            else:
                image, _ = inspect_image(content)
                extension = image["encoding"]
            media = self.store.artifact(content, extension)
        record = {"id": str(uuid.uuid4()), "created_at": now(), "title": title,
                  "source": source, "raw": raw, "raw_json": json.dumps(raw, ensure_ascii=False, indent=2),
                  "recipe": recipe, "image": image,
                  "media": media, "demo": demo, "warning": warning,
                  "comparison": "not_tested"}
        if source["kind"] in {"civitai", "file"}:
            record["reproduction"] = {"status": "blocked", "blockers": reproduction_blockers(record)}
        return self.store.put(record)

    async def import_url(self, url):
        identifier, raw, content, warning = await self.provider.acquire(url)
        if content:
            try:
                inspect_image(content)
            except Problem:
                content = None
                warning = " ".join(filter(None, [warning, "Recipe saved; the source preview was not a valid supported image."]))
        record = self.save(raw, content, {"kind": "civitai", "image_id": identifier,
                         "url": f"https://civitai.com/images/{identifier}", "acquired_at": now(),
                         "reference_quality": "provider_image_not_verified_original"}, f"Civitai image {identifier}", warning=warning)
        if self.auto_resolve and "model_versions" not in raw:
            self.resolve_models(record["id"])
        return record

    def import_file(self, content, filename):
        details, metadata = inspect_image(content)
        parameters = metadata.get("parameters")
        raw = {"meta": parse_parameters(parameters) if parameters else {},
               "embedded_metadata": redact(metadata), "image": details}
        return self.save(raw, content, {"kind": "file", "acquired_at": now(),
                         "reference_quality": "uploaded_bytes"}, Path(filename.replace("\\", "/")).name[:180],
                         warning=None if parameters else "No supported A1111 recipe found. Embedded metadata is preserved in source details.")

    def demo(self):
        for record in self.store.list():
            if record["demo"]:
                return record
        raw = {"fixture": "hand-drawn-landscape-v1", "meta": {
            "prompt": "A quiet alpine lake at first light, layered mountain silhouettes, a tiny canoe on still water, soft peach sky, tranquil composition",
            "negativePrompt": "text, watermark, blurry", "seed": "18446744073709551614", "steps": 28,
            "cfgScale": 6.5, "sampler": "DPM++ 2M", "scheduler": "karras", "Size": "960x1120",
            "resources": [{"name": "Demo checkpoint (illustrative)", "type": "checkpoint"}]}}
        return self.save(raw, (Path(__file__).parent / "assets/demo.svg").read_bytes(),
                         {"kind": "demo", "reference_quality": "authored_svg_not_generated"},
                         "Stillwater at dawn", demo=True, extension="svg")

    def create_recipe(self, settings):
        if self.engine is None:
            raise Problem("Start the service with a configured Comfy runtime to create a generation recipe.", 409)
        settings = dict(settings)
        selected = settings.pop("model_sha256", None)
        raw = {"generation_profile": PROFILE, "checkpoint_sha256": CHECKPOINT_SHA256,
               "meta": {**settings, "resources": [{"name": CHECKPOINT, "type": "checkpoint", "hash": CHECKPOINT_SHA256}]}}
        if selected:
            blob = self.inventory.available(selected)
            if not blob or blob["file"].get("role") != "checkpoint" or blob["file"].get("base_model") != "SDXL 1.0":
                raise Problem("Select a verified SDXL 1.0 checkpoint from the model cache.", 409)
            binding = self.inventory.bind(blob["file"])
            raw.update(generation_profile=MODEL_PROFILE, checkpoint_sha256=selected, model_binding=binding)
            raw["meta"]["resources"] = [{"name": blob["file"]["name"], "type": "checkpoint", "hash": selected}]
        return self.save(raw, None, {"kind": "authored", "acquired_at": now(), "reference_quality": "no_source_image"},
                         "SDXL · " + settings["prompt"][:65])

    def reproduce(self, identifier):
        record = self.store.get(identifier)
        if record["source"]["kind"] in {"civitai", "file"}:
            raise Problem(" ".join(self.dependencies(identifier)["generation_blockers"]), 409)
        if not record["demo"]:
            if self.engine is None:
                raise Problem("Real generation is not connected yet. " + " ".join(self.dependencies(identifier)["generation_blockers"]), 409)
            graph = workflow(record)
            if any(job["status"] in {"queued", "running", "unknown"} and job.get("engine") == "comfy" for job in self.store.list("job")):
                raise Problem("A generation is already active or awaiting inspection. Finish or resolve it before starting another.", 409)
            job = {"id": str(uuid.uuid4()), "import_id": identifier, "created_at": now(), "status": "queued",
                   "engine": "comfy", "comparison": "not_tested", "message": "Preparing the SDXL model",
                   "recipe": record["recipe"], "workflow": graph, "workflow_json": json.dumps(graph, indent=2),
                   "runtime": self.engine.identity, "output": None, "prompt_id": None}
            job["model_binding"] = record["raw"].get("model_binding") or {"sha256": CHECKPOINT_SHA256, "filename": CHECKPOINT}
            job["generation_profile"] = record["raw"]["generation_profile"]
            self.store.put(job, "job")
            task = asyncio.create_task(self.run_generation(job))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.discard)
            return job
        job = {"id": str(uuid.uuid4()), "import_id": identifier, "created_at": now(), "status": "queued",
               "engine": "demo", "comparison": "not_applicable", "message": "Preparing the demo preview",
               "recipe": record["recipe"], "output": None}
        self.store.put(job, "job")
        task = asyncio.create_task(self.run_demo(job, record))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return job

    async def run_generation(self, job):
        def accepted(prompt_id):
            job.update(prompt_id=prompt_id, status="running", message="Generating on your GPU")
            self.store.put(job, "job")
        try:
            content = await self.engine.generate(job["workflow"], accepted)
            details, _ = inspect_image(content)
            if any(details[key] != job["recipe"]["fields"][key] for key in ("width", "height")):
                raise Problem("The generated image dimensions differ from the submitted recipe. No result was accepted.", 502)
            job.update(status="completed", finished_at=now(), image=details,
                       output=self.store.artifact(content, details["encoding"]),
                       message="Generated with SDXL. Recipe, model SHA-256 and workflow are saved; source matching has not been evaluated.")
        except asyncio.CancelledError:
            job.update(status="interrupted", finished_at=now(), message="Generation interrupted by service shutdown. It was not resubmitted.")
        except Problem as exc:
            job.update(status="unknown" if exc.status == 504 else "failed", finished_at=now(), message=exc.message)
        except Exception:
            job.update(status="unknown", finished_at=now(),
                       message="Generation status could not be confirmed. Inspect the runtime log and restart the service before retrying; no job was resubmitted.")
        self.store.put(job, "job")

    async def run_demo(self, job, record):
        try:
            job.update(status="running", message="Testing the result flow; no image model is running")
            self.store.put(job, "job")
            await asyncio.sleep(self.demo_delay)
            job.update(status="completed", finished_at=now(), output=record["media"],
                       message="Demo complete. The sample illustration is reused; this is not a generated reproduction.")
        except asyncio.CancelledError:
            job.update(status="interrupted", message="Demo interrupted by service shutdown.", finished_at=now())
        except Exception:
            job.update(status="failed", message="The demo could not finish. Try again.", finished_at=now())
        self.store.put(job, "job")

    async def close(self):
        self.downloads.closing = True
        for stop in self.downloads.stops.values():
            stop.set()
        if self.operations:
            await asyncio.gather(*list(self.operations))
        await self.downloads.close()
        for task in self.tasks:
            task.cancel()
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        if self.engine:
            await self.engine.close()
