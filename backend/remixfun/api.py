import re
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
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


class RecipeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1, max_length=10000)
    negativePrompt: str = Field(default="", max_length=10000)
    seed: str = Field(default="42", pattern=r"^[0-9]{1,20}$")
    steps: int = Field(default=25, ge=1, le=100, strict=True)
    cfgScale: float = Field(default=7.0, ge=0, le=20)
    width: int = Field(default=1024, ge=256, le=1536, strict=True)
    height: int = Field(default=1024, ge=256, le=1536, strict=True)

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


def create_app(root: Path, web: Path | None = None, provider=None, demo_delay=1.5, instance="headless", engine=None):
    service = Service(root, provider, demo_delay, engine)

    @asynccontextmanager
    async def lifespan(app):
        service.recover()
        try:
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
    async def reproduce(identifier: str):
        return service.reproduce(identifier)

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
