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
from .provider import Civitai, redact
from .storage import Store


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
    def __init__(self, root, provider=None, demo_delay=1.5):
        self.store = Store(root)
        self.provider = provider or Civitai()
        self.demo_delay = demo_delay
        self.tasks = set()

    def recover(self):
        for job in self.store.list("job"):
            if job["status"] in {"queued", "running"}:
                job.update(status="interrupted", message="The service stopped before this demo finished. You can run it again.", finished_at=now())
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
        return self.store.put(record)

    async def import_url(self, url):
        identifier, raw, content, warning = await self.provider.acquire(url)
        return self.save(raw, content, {"kind": "civitai", "image_id": identifier,
                         "url": f"https://civitai.com/images/{identifier}", "acquired_at": now(),
                         "reference_quality": "provider_image_not_verified_original"}, f"Civitai image {identifier}", warning=warning)

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

    def reproduce(self, identifier):
        record = self.store.get(identifier)
        if not record["demo"]:
            raise Problem("Real generation is not connected yet. Your source recipe is saved; exact model resolution and a tested Comfy runtime are required before reproduction.", 409)
        job = {"id": str(uuid.uuid4()), "import_id": identifier, "created_at": now(), "status": "queued",
               "engine": "demo", "comparison": "not_applicable", "message": "Preparing the demo preview",
               "recipe": record["recipe"], "output": None}
        self.store.put(job, "job")
        task = asyncio.create_task(self.run_demo(job, record))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return job

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
        for task in self.tasks:
            task.cancel()
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
