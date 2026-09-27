"""CPU contracts for real-job plumbing; GPU evidence is recorded separately."""
import asyncio
import copy
import hashlib
import io
import json
from pathlib import Path
import time
from types import SimpleNamespace

from fastapi.testclient import TestClient
import httpx
import pytest
from PIL import Image

from remixfun.api import create_app
from remixfun.domain import Problem
from remixfun.engine import CHECKPOINT, CHECKPOINT_SHA256, Comfy, verified_gpu_device, workflow
from remixfun.service import Service

PNG = (Path(__file__).parent / "fixtures/metadata.png").read_bytes()
buffer = io.BytesIO()
Image.new("RGB", (1024, 1024), "#78908a").save(buffer, format="PNG")
GENERATED_PNG = buffer.getvalue()


class FakeEngine:
    identity = {"profile": "test-double-not-GPU-evidence"}

    def __init__(self, error=None, wait=False):
        self.error, self.wait, self.closed, self.calls = error, wait, False, 0

    async def start(self):
        pass

    async def close(self):
        self.closed = True

    async def generate(self, graph, accepted):
        self.calls += 1
        accepted("owned-prompt-id")
        if self.wait:
            await asyncio.sleep(60)
        if self.error:
            raise self.error
        return GENERATED_PNG


def finished(client, identifier):
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        job = client.get(f"/api/jobs/{identifier}").json()
        if job["status"] not in {"queued", "running"}:
            return job
        time.sleep(0.01)
    raise AssertionError("Job did not finish")


@pytest.mark.parametrize("platform,device", [("darwin", "mps"), ("win32", "cuda"), ("linux", "cuda")])
def test_gpu_profile_requires_the_primary_platform_device(platform, device):
    primary = {"type": device, "name": "owned GPU"}
    assert verified_gpu_device({"devices": [primary]}, platform) == primary
    with pytest.raises(Problem, match=device.upper()):
        verified_gpu_device({"devices": [{"type": "cpu"}, primary]}, platform)


def test_generation_persists_workflow_seed_output_and_immutable_source(tmp_path):
    engine = FakeEngine()
    with TestClient(create_app(tmp_path, engine=engine), base_url="http://127.0.0.1") as client:
        record = client.post("/api/recipes", json={"prompt": "Owned test lake", "seed": "18446744073709551614"}).json()
        before = copy.deepcopy(record)
        response = client.post(f"/api/imports/{record['id']}/reproduce")
        assert response.status_code == 202
        job = finished(client, response.json()["id"])
        assert job["status"] == "completed"
        assert job["prompt_id"] == "owned-prompt-id"
        assert job["comparison"] == "not_tested"
        assert job["runtime"] == engine.identity
        assert json.loads(job["workflow_json"])["5"]["inputs"]["seed"] == 18446744073709551614
        assert job["workflow"]["1"]["inputs"]["ckpt_name"] == CHECKPOINT
        assert client.get(job["output"]["url"]).content == GENERATED_PNG
        assert client.get(f"/api/imports/{record['id']}").json() == before
    assert engine.closed
    assert Service(tmp_path).store.get(job["id"], "job")["status"] == "completed"


@pytest.mark.parametrize("body", [{"width": 1025}, {"seed": str(2**64)}, {"seed": True}, {"steps": 0}, {"cfgScale": 100}, {"arbitrary_graph": {}}])
def test_invalid_generation_settings_do_not_create_a_recipe(tmp_path, body):
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        assert client.post("/api/recipes", json={"prompt": "test", **body}).status_code == 422
        assert client.get("/api/imports").json() == []


def test_imported_recipes_never_use_the_test_checkpoint_as_a_substitute(tmp_path):
    engine = FakeEngine()
    with TestClient(create_app(tmp_path, engine=engine), base_url="http://127.0.0.1") as client:
        record = client.post("/api/imports/file", files={"file": ("source.png", PNG)}).json()
        response = client.post(f"/api/imports/{record['id']}/reproduce")
        assert response.status_code == 409
        assert "No model was substituted" in response.json()["detail"]
        assert engine.calls == 0 and client.get("/api/jobs").json() == []


def test_uncertain_submission_is_saved_and_blocks_duplicate_work(tmp_path):
    engine = FakeEngine(error=httpx.ReadTimeout("response lost"))
    with TestClient(create_app(tmp_path, engine=engine), base_url="http://127.0.0.1") as client:
        record = client.post("/api/recipes", json={"prompt": "test"}).json()
        path = f"/api/imports/{record['id']}/reproduce"
        identifier = client.post(path).json()["id"]
        assert finished(client, identifier)["status"] == "unknown"
        assert client.post(path).status_code == 409
        assert engine.calls == 1
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        assert client.get(f"/api/jobs/{identifier}").json()["status"] == "interrupted"


def test_shutdown_marks_real_job_interrupted_and_closes_owned_engine(tmp_path):
    engine = FakeEngine(wait=True)
    with TestClient(create_app(tmp_path, engine=engine), base_url="http://127.0.0.1") as client:
        record = client.post("/api/recipes", json={"prompt": "test"}).json()
        path = f"/api/imports/{record['id']}/reproduce"
        job = client.post(path).json()
        assert client.post(path).status_code == 409
    assert engine.closed
    assert Service(tmp_path).store.get(job["id"], "job")["status"] == "interrupted"


def test_wrong_output_dimensions_are_not_accepted(tmp_path):
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        record = client.post("/api/recipes", json={"prompt": "test", "width": 512}).json()
        job = finished(client, client.post(f"/api/imports/{record['id']}/reproduce").json()["id"])
        assert job["status"] == "failed" and job["output"] is None
        assert "dimensions differ" in job["message"]


def test_checkpoint_hash_is_verified_and_modified_files_rechecked(tmp_path, monkeypatch):
    checkpoint = tmp_path / "models" / "checkpoints" / CHECKPOINT
    checkpoint.parent.mkdir(parents=True)
    checkpoint.write_bytes(b"owned fixture, not model weights")
    expected = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    monkeypatch.setattr("remixfun.engine.CHECKPOINT_SHA256", expected)
    engine = Comfy(tmp_path, tmp_path / "logs")
    engine.verify_checkpoint()
    checkpoint.write_bytes(b"modified")
    with pytest.raises(Problem, match="SHA-256"):
        engine.verify_checkpoint()


def test_workflow_rejects_missing_settings_and_changed_model(tmp_path):
    service = Service(tmp_path, engine=FakeEngine())
    record = service.create_recipe({"prompt": "test"})
    with pytest.raises(Problem, match="incomplete"):
        workflow(record)
    record["raw"]["checkpoint_sha256"] = "different"
    with pytest.raises(Problem, match="No model was substituted"):
        workflow(record)


def test_comfy_protocol_submits_once_polls_own_job_and_downloads_output(tmp_path, monkeypatch):
    calls = []
    def handler(request):
        calls.append((request.method, request.url.path))
        if request.url.path == "/prompt":
            return httpx.Response(200, json={"prompt_id": "our-job"})
        if request.url.path == "/history/our-job":
            return httpx.Response(200, json={"our-job": {"status": {"completed": True},
                "outputs": {"7": {"images": [{"filename": "test.png", "subfolder": "remixfun", "type": "output"}]}}}})
        assert request.url.path == "/view" and request.url.params["filename"] == "test.png"
        return httpx.Response(200, content=PNG)
    original = httpx.AsyncClient
    monkeypatch.setattr("remixfun.engine.httpx.AsyncClient", lambda **kwargs: original(**kwargs, transport=httpx.MockTransport(handler)))
    engine = Comfy(tmp_path, tmp_path / "logs")
    engine.process = SimpleNamespace(poll=lambda: None)
    engine.url = "http://127.0.0.1:8188"
    engine.verify_checkpoint = lambda: None
    accepted = []
    assert asyncio.run(engine.generate({}, accepted.append)) == PNG
    assert accepted == ["our-job"]
    assert calls == [("POST", "/prompt"), ("GET", "/history/our-job"), ("GET", "/view")]
