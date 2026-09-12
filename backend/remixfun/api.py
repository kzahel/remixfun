import re
import secrets
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Header, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, field_validator

from . import __version__
from .build_info import source_sha
from .domain import Problem
from .provider import MAX_IMAGE
from .service import Service


class ImportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    url: str = Field(min_length=1, max_length=2048)


class DownloadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    revision: str = Field(pattern=r"^[a-f0-9]{64}$")
    choices: dict[str, str] = Field(default_factory=dict, max_length=64)


class ReproduceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    revision: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    accept_assumptions: bool = Field(default=False, strict=True)
    seed_offset: int = Field(default=0, ge=0, le=31, strict=True)


class ModelSettings(BaseModel):
    model_root: str = Field(min_length=1, max_length=4096)
    model_paths: list[str] = Field(default_factory=list, max_length=16)


class CredentialRequest(BaseModel):
    key: str = Field(max_length=4096)


class RecipeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1, max_length=10000)
    negativePrompt: str = Field(default="", max_length=10000)
    seed: str = Field(default="42", pattern=r"^[0-9]{1,20}$")
    steps: int = Field(default=25, ge=1, le=100, strict=True)
    cfgScale: float = Field(default=7.0, ge=0, le=20)
    width: int = Field(default=1024, ge=256, le=1536, strict=True)
    height: int = Field(default=1024, ge=256, le=1536, strict=True)
    model_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")

    @field_validator("width", "height")
    @classmethod
    def multiples(cls, value):
        if value % 64:
            raise ValueError("Dimensions must be multiples of 64")
        return value

    @field_validator("seed")
    @classmethod
    def seed_range(cls, value):
        if int(value) >= 2**64:
            raise ValueError("Seed must fit an unsigned 64-bit integer")
        return str(int(value))


def create_app(root: Path, web: Path | None = None, provider=None, demo_delay=1.5, instance="headless", engine=None,
               model_root=None, model_paths=(), download_transport=None, owner_token=None, shutdown=None):
    service = Service(root, provider, demo_delay, engine, model_root, model_paths, download_transport)

    @asynccontextmanager
    async def lifespan(app):
        service.recover()
        try:
            await service.start()
            if engine:
                await engine.start()
            yield
        finally:
            await service.close()

    app = FastAPI(title="Remixfun", version=__version__, lifespan=lifespan, docs_url=None, redoc_url=None)
    app.state.service = service

    @app.exception_handler(Problem)
    async def problem(request, exc):
        return JSONResponse({"detail": exc.message}, status_code=exc.status)

    @app.middleware("http")
    async def local_only(request, call_next):
        if request.url.hostname not in {"127.0.0.1", "localhost", "::1"}:
            return JSONResponse({"detail": "This service accepts local requests only."}, status_code=403)
        origin = request.headers.get("origin")
        allowed = {f"http://{request.headers.get('host')}", "http://127.0.0.1:5173", "http://localhost:5173"}
        if origin and origin not in allowed:
            return JSONResponse({"detail": "This browser origin is not allowed."}, status_code=403)
        if getattr(app.state, "stopping", False) and request.method not in {"GET", "HEAD"}:
            return JSONResponse({"detail": "The service is shutting down."}, status_code=503)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'"
        return response

    @app.get("/api/health")
    def health():
        return {"app": "remixfun", "version": __version__, "api_version": 1,
                "source_sha": source_sha(),
                "instance": instance, "engine": "comfy" if engine else "demo_only", "network": "loopback_only"}

    @app.post("/api/shutdown")
    async def shutdown_owned(x_remixfun_owner: str = Header(default="")):
        if not owner_token or not secrets.compare_digest(x_remixfun_owner, owner_token) or shutdown is None:
            raise Problem("Only the owning desktop can shut down this service.", 403)
        if any(j["status"] in {"queued", "running", "unknown"} for j in service.store.list("job")):
            raise Problem("Generation is active or awaiting inspection. Finish it before closing.", 409)
        app.state.stopping = True
        shutdown()
        return {"status": "stopping"}

    @app.get("/api/imports/{identifier}/dependencies")
    def dependencies(identifier: str, seed_offset: int = Query(default=0, ge=0, le=31)):
        return service.dependencies(identifier, seed_offset)

    @app.post("/api/imports/{identifier}/dependencies/resolve", status_code=202)
    async def resolve_models(identifier: str):
        return service.resolve_models(identifier)

    @app.post("/api/imports/{identifier}/downloads", status_code=202)
    async def download_models(identifier: str, body: DownloadRequest):
        return service.download_models(identifier, body.revision, body.choices)

    @app.get("/api/downloads")
    def downloads():
        return service.downloads.list()

    @app.get("/api/downloads/{identifier}")
    def download(identifier: str):
        return service.downloads.get(identifier)

    @app.post("/api/downloads/{identifier}/{action}")
    async def control_download(identifier: str, action: str):
        return await service.downloads.control(identifier, action)

    @app.get("/api/operations/{identifier}")
    def operation(identifier: str):
        return service.store.get(identifier, "operation")

    @app.get("/api/models/settings")
    def model_settings():
        return service.model_settings()

    @app.get("/api/models")
    def models():
        return [{"sha256": b["sha256"], "name": b["file"]["name"], "role": b["file"]["role"],
                 "base_model": b["file"].get("base_model"), "size": b["size"]}
                for b in service.inventory.list("blobs") if service.inventory.available(b["sha256"])]

    @app.put("/api/models/settings")
    def configure_models(body: ModelSettings):
        return service.configure_models(body.model_root, body.model_paths)

    @app.put("/api/models/credential")
    def credential(body: CredentialRequest):
        service.downloads.transport.credentials.set(body.key)
        return {"configured": bool(body.key)}

    @app.post("/api/models/scan", status_code=202)
    async def scan_models():
        return service.scan_models()

    @app.post("/api/recipes", status_code=201)
    def create_recipe(body: RecipeRequest):
        return service.create_recipe({**body.model_dump(), "sampler": "euler", "scheduler": "normal"})

    @app.get("/api/imports")
    def imports():
        return service.store.list()

    @app.post("/api/imports", status_code=201)
    async def import_url(body: ImportRequest):
        return await service.import_url(body.url)

    @app.post("/api/imports/file", status_code=201)
    async def import_file(file: UploadFile = File()):
        try:
            content = await file.read(MAX_IMAGE + 1)
            if len(content) > MAX_IMAGE:
                raise Problem("Source image exceeds the 25 MB import limit.")
            return service.import_file(content, file.filename or "Imported image")
        finally:
            await file.close()

    @app.post("/api/demo", status_code=201)
    def demo():
        return service.demo()

    @app.get("/api/imports/{identifier}")
    def get_import(identifier: str):
        return service.store.get(identifier)

    @app.get("/api/imports/{identifier}/manifest")
    def export(identifier: str):
        return JSONResponse(service.store.get(identifier), headers={"Content-Disposition": 'attachment; filename="remixfun-recipe.json"'})

    @app.post("/api/imports/{identifier}/reproduce", status_code=202)
    async def reproduce(identifier: str, body: ReproduceRequest | None = None):
        return service.reproduce(identifier, **(body.model_dump() if body else {}))

    @app.get("/api/jobs")
    def jobs():
        return service.store.list("job")

    @app.get("/api/jobs/{identifier}")
    def job(identifier: str):
        return service.store.get(identifier, "job")

    @app.get("/api/media/{name}")
    def media(name: str):
        if not re.fullmatch(r"[a-f0-9]{64}\.(png|jpeg|webp|svg)", name):
            raise Problem("Image not found.", 404)
        path = root / "media" / name
        if not path.is_file():
            raise Problem("Image not found.", 404)
        return FileResponse(path)

    if web and (web / "index.html").is_file():
        app.mount("/", StaticFiles(directory=web, html=True), name="web")
    return app
