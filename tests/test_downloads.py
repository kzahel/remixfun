"""Real local HTTP transfer tests; public-provider metadata is replayed separately."""
import asyncio
import copy
from contextlib import contextmanager
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
import time

import httpx
import pytest
from fastapi.testclient import TestClient

from remixfun.api import create_app
from remixfun.domain import Problem
from remixfun.downloads import Downloads
from remixfun.model_inventory import Inventory
from remixfun.model_resolution import build_plan
from remixfun.model_transport import ModelTransport, TransferError, STORAGE_HOSTS
from remixfun.provider import Civitai

DATA = b"owned model-transfer fixture\0" * 160000
DIGEST = hashlib.sha256(DATA).hexdigest()
FILE = {"provider": "civitai", "model_id": 101055, "version_id": "128078", "file_id": "92696",
        "sha256": DIGEST, "name": "owned.safetensors", "role": "checkpoint", "size_estimate": len(DATA), "base_model": "SDXL 1.0"}


class MemoryCredentials:
    def __init__(self): self.value = None
    def get(self): return self.value
    def set(self, value): self.value = value or None


@contextmanager
def origin(mode="range", slow=False):
    calls = []
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_): pass
        def do_GET(self):
            offset = int(self.headers.get("Range", "bytes=0-").split("=")[1].split("-")[0])
            calls.append({"offset": offset, "if_range": self.headers.get("If-Range")})
            if mode == "ignore": offset = 0
            if mode == "denied":
                self.send_response(403); self.end_headers(); return
            if offset == len(DATA):
                self.send_response(416); self.send_header("Content-Range", f"bytes */{len(DATA)}"); self.end_headers(); return
            self.send_response(206 if offset else 200)
            self.send_header("Content-Length", str(len(DATA) - offset))
            self.send_header("ETag", '"changed"' if mode == "changed" else '"owned"')
            if offset: self.send_header("Content-Range", f"bytes {offset}-{len(DATA)-1}/{len(DATA)}")
            self.end_headers()
            payload = DATA[offset:]
            if mode == "corrupt": payload = bytes([payload[0] ^ 1]) + payload[1:]
            try:
                for i in range(0, len(payload), 65536):
                    self.wfile.write(payload[i:i+65536]); self.wfile.flush()
                    if slow: time.sleep(.01)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError): pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=lambda: server.serve_forever(poll_interval=.05), daemon=True)
    thread.start()
    class LocalTransport:
        credentials = MemoryCredentials()
        @contextmanager
        def stream(self, file, offset=0, etag=None):
            headers = {"Range": f"bytes={offset}-", "If-Range": etag} if offset and etag else {}
            with httpx.stream("GET", f"http://127.0.0.1:{server.server_port}", headers=headers, trust_env=False) as response:
                from remixfun.model_transport import check_status
                check_status(response)
                yield response
    try: yield LocalTransport(), calls
    finally:
        server.shutdown(); server.server_close(); thread.join()


async def until(predicate, timeout=5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = predicate()
        if result: return result
        await asyncio.sleep(.01)
    raise AssertionError("Timed out waiting for test transition")


def record():
    queries = json.loads((Path(__file__).parent / "fixtures/civitai-141984808/queries.json").read_text())
    version = json.loads((Path(__file__).parent / "fixtures/civitai-141984808/model-version.json").read_text())
    version["files"][0]["hashes"]["SHA256"] = DIGEST
    version["files"][0]["sizeKB"] = len(DATA) / 1024
    return {"id": "source", "raw": {"meta": queries[1]["state"]["data"]["meta"],
        "generation_data": queries[1]["state"]["data"], "model_versions": [{"status": "identified", "version_id": "128078",
        "model_id": 101055, "name": "v1.0 VAE fix", "files": version["files"]}]}}


def test_file_selection_preserves_conflicts_and_ambiguous_variants():
    source = record()
    baseline = copy.deepcopy(source)
    plan = build_plan(source)
    assert len(plan["dependencies"]) == 1
    assert plan["dependencies"][0]["file"]["sha256"] == DIGEST
    assert source == baseline
    variant = copy.deepcopy(source["raw"]["model_versions"][0]["files"][0])
    variant["id"] = 7; variant["hashes"]["SHA256"] = "a" * 64
    source["raw"]["model_versions"][0]["files"].append(variant)
    assert build_plan(source)["dependencies"][0]["status"] == "choose_file"
    assert build_plan(source, choices={"0": "7"})["dependencies"][0]["file"]["file_id"] == "7"
    source["raw"]["meta"]["civitaiResources"][0]["fileId"] = 92696
    assert build_plan(source, choices={"0": "7"})["dependencies"][0]["status"] == "blocked"


def test_local_http_completion_deduplication_and_changed_file(tmp_path):
    with origin() as (transport, calls):
        async def run():
            inventory = Inventory(tmp_path)
            downloads = Downloads(inventory, transport)
            await downloads.start()
            try:
                first = downloads.enqueue(FILE, "import-one:0")
                second = downloads.enqueue(FILE, "import-two:0")
                assert first["download_id"] == second["download_id"]
                await until(lambda: downloads.get(first["download_id"])["status"] == "ready")
                assert len(calls) == 1
                assert len(downloads.get(first["download_id"])["consumers"]) == 2
                assert inventory.available(DIGEST)
                binding = inventory.bind(FILE)
                assert Path(binding["path"]).read_bytes() == DATA
                assert downloads.enqueue(FILE, "three")["status"] == "available"
                inventory.target(DIGEST).write_bytes(b"changed")
                assert inventory.available(DIGEST) is None
            finally: await downloads.close()
        asyncio.run(run())


@pytest.mark.parametrize("mode", ["range", "ignore", "changed"])
def test_resume_range_ignored_range_and_changed_validator(tmp_path, mode):
    with origin(mode) as (transport, calls):
        async def run():
            inventory = Inventory(tmp_path)
            downloads = Downloads(inventory, transport)
            await downloads.start()
            try:
                job = {"id": "owned", "file": FILE, "status": "paused", "consumers": ["source:0"],
                       "downloaded_bytes": 12345, "total_bytes": len(DATA), "etag": '"owned"'}
                inventory.partial(job).write_bytes(DATA[:12345])
                downloads.save(job)
                downloads.action("owned", "resume")
                await until(lambda: downloads.get("owned")["status"] == "ready")
                assert calls[0] == {"offset": 12345, "if_range": '"owned"'}
                assert inventory.target(DIGEST).read_bytes() == DATA
                if mode == "changed": assert calls[1]["offset"] == 0
            finally: await downloads.close()
        asyncio.run(run())


def test_pause_close_reopen_and_resume_keeps_partial(tmp_path):
    with origin(slow=True) as (transport, calls):
        async def run():
            inventory = Inventory(tmp_path)
            downloads = Downloads(inventory, transport)
            await downloads.start()
            identifier = downloads.enqueue(FILE, "source:0")["download_id"]
            job = downloads.get(identifier)
            await until(lambda: inventory.partial(job).exists() and inventory.partial(job).stat().st_size >= 1024**2)
            await downloads.control(identifier, "pause")
            offset = inventory.partial(job).stat().st_size
            assert 0 < offset < len(DATA)
            await downloads.close()
            again = Downloads(Inventory(tmp_path), transport)
            await again.start()
            try:
                assert again.get(identifier)["status"] == "paused"
                again.action(identifier, "resume")
                await until(lambda: again.get(identifier)["status"] == "ready")
                assert calls[-1]["offset"] == offset
            finally: await again.close()
        asyncio.run(run())


@pytest.mark.parametrize("mode,code", [("corrupt", "hash_mismatch"), ("denied", "access_denied")])
def test_bad_bytes_and_access_failures_never_publish(tmp_path, mode, code):
    with origin(mode) as (transport, _):
        async def run():
            inventory = Inventory(tmp_path); downloads = Downloads(inventory, transport)
            await downloads.start()
            try:
                identifier = downloads.enqueue(FILE, "source:0")["download_id"]
                await until(lambda: downloads.get(identifier)["status"] == "failed")
                assert downloads.get(identifier)["error_code"] == code
                assert not inventory.available(DIGEST)
                assert not inventory.target(DIGEST).exists()
            finally: await downloads.close()
        asyncio.run(run())


def test_complete_partial_416_is_hashed_before_ready(tmp_path):
    with origin() as (transport, _):
        async def run():
            inventory = Inventory(tmp_path); downloads = Downloads(inventory, transport)
            await downloads.start()
            try:
                job = {"id": "complete", "file": FILE, "status": "paused", "consumers": [],
                       "downloaded_bytes": len(DATA), "total_bytes": len(DATA), "etag": '"owned"'}
                inventory.partial(job).write_bytes(DATA)
                downloads.save(job); downloads.action("complete", "resume")
                await until(lambda: downloads.get("complete")["status"] == "ready")
                assert inventory.available(DIGEST)
            finally: await downloads.close()
        asyncio.run(run())


def test_inventory_reuses_renamed_external_bytes_and_locks_cache(tmp_path):
    library = tmp_path / "existing"; library.mkdir()
    path = library / "renamed.safetensors"; path.write_bytes(DATA)
    inventory = Inventory(tmp_path / "cache"); inventory.start()
    try:
        other = Inventory(tmp_path / "cache")
        with pytest.raises(Problem, match="another service"): other.start()
        assert inventory.scan([library], [FILE]) == [DIGEST]
        assert inventory.available(DIGEST)["external"]
        assert path.read_bytes() == DATA
    finally: inventory.close()


def test_api_plan_live_status_export_and_stale_revision(tmp_path):
    with origin() as (transport, _):
        with TestClient(create_app(tmp_path, download_transport=transport), base_url="http://127.0.0.1") as client:
            service = client.app.state.service
            source = service.save(record()["raw"], None, {"kind": "civitai"}, "Owned fixture")
            path = f"/api/imports/{source['id']}"
            plan = client.get(path + "/dependencies").json()
            assert client.post(path + "/downloads", json={"revision": "f" * 64}).status_code == 409
            response = client.post(path + "/downloads", json={"revision": plan["revision"]})
            assert response.status_code == 202
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                current = client.get(path + "/dependencies").json()
                if current["dependencies"][0]["status"] == "available": break
                time.sleep(.02)
            assert current["dependencies"][0]["status"] == "available"
            assert current["generation_blockers"] and current["total_download_bytes"] == 0
            assert client.get(path + "/manifest").json() == source
            assert client.post(path + "/reproduce").status_code == 409
        with TestClient(create_app(tmp_path, download_transport=transport), base_url="http://127.0.0.1") as client:
            assert client.get(path + "/dependencies").json()["dependencies"][0]["status"] == "available"


def test_model_transport_identity_redirects_and_credentials():
    calls = []
    credentials = MemoryCredentials(); credentials.set("owned-test-secret")
    storage = next(iter(STORAGE_HOSTS))
    def handler(request):
        calls.append(request)
        if request.url.path.startswith("/api/v1/"):
            return httpx.Response(200, json={"id": 128078, "modelId": 101055, "files": [{"id": 92696,
                "hashes": {"SHA256": DIGEST}, "downloadUrl": "https://civitai.com/api/download/models/128078"}]})
        if request.url.host == "civitai.com":
            return httpx.Response(307, headers={"location": f"https://{storage}/object?signature=ephemeral"})
        return httpx.Response(206, content=DATA[123:], headers={"content-range": f"bytes 123-{len(DATA)-1}/{len(DATA)}"})
    transport = ModelTransport(httpx.MockTransport(handler), credentials)
    with transport.stream(FILE, 123, '"owned"') as response: assert response.read() == DATA[123:]
    assert calls[1].url.params["fileId"] == "92696"
    assert calls[0].headers["authorization"] == "Bearer owned-test-secret"
    assert "authorization" not in calls[-1].headers
    assert calls[-1].headers["range"] == "bytes=123-"


@pytest.mark.parametrize("location", ["http://127.0.0.1/private", "https://evil.test/file", "https://civitai.com/api/v1/private"])
def test_model_transport_rejects_other_redirect_destinations(location):
    from remixfun.model_transport import checked_url
    with pytest.raises(TransferError): checked_url(location)


def test_shutdown_needs_owner_secret_and_does_not_expose_it(tmp_path):
    stopped = []
    with TestClient(create_app(tmp_path, owner_token="owned-secret", shutdown=lambda: stopped.append(True)), base_url="http://127.0.0.1") as client:
        assert "owned-secret" not in client.get("/api/health").text
        assert client.post("/api/shutdown").status_code == 403
        assert client.post("/api/shutdown", headers={"X-Remixfun-Owner": "wrong"}).status_code == 403
        assert client.post("/api/shutdown", headers={"X-Remixfun-Owner": "owned-secret"}).status_code == 200
        assert stopped == [True]
        assert client.post("/api/demo").status_code == 503


def test_active_transfer_automatically_resumes_after_owned_shutdown(tmp_path):
    with origin(slow=True) as (transport, calls):
        async def run():
            inventory = Inventory(tmp_path); downloads = Downloads(inventory, transport)
            await downloads.start()
            identifier = downloads.enqueue(FILE, "source:0")["download_id"]
            job = downloads.get(identifier)
            await until(lambda: inventory.partial(job).exists() and inventory.partial(job).stat().st_size >= 1024**2)
            await downloads.close()
            offset = inventory.partial(job).stat().st_size
            assert downloads.get(identifier)["status"] == "queued"
            again = Downloads(Inventory(tmp_path), transport)
            await again.start()
            try:
                await until(lambda: again.get(identifier)["status"] == "ready")
                assert calls[-1]["offset"] == offset
            finally: await again.close()
        asyncio.run(run())


def test_published_blob_recovery_and_corrupt_cache_retry(tmp_path):
    with origin() as (transport, calls):
        async def run():
            inventory = Inventory(tmp_path); downloads = Downloads(inventory, transport)
            target = inventory.target(DIGEST); target.parent.mkdir(parents=True); target.write_bytes(DATA)
            await downloads.start()
            try:
                identifier = downloads.enqueue(FILE, "source:0")["download_id"]
                await until(lambda: downloads.get(identifier)["status"] == "ready")
                assert not calls  # Crash between rename and the database commit.
                target.write_bytes(b"damaged managed cache")
                await until(lambda: identifier not in downloads.tasks)
                downloads.action(identifier, "retry")
                await until(lambda: downloads.get(identifier)["status"] == "ready")
                assert len(calls) == 1
                assert inventory.available(DIGEST)
                assert Path(inventory.bind(FILE)["path"]).read_bytes() == DATA
            finally: await downloads.close()
        asyncio.run(run())


def test_disk_reservation_rejects_before_network(tmp_path, monkeypatch):
    from types import SimpleNamespace
    with origin() as (transport, calls):
        async def run():
            inventory = Inventory(tmp_path); downloads = Downloads(inventory, transport)
            await downloads.start()
            try:
                monkeypatch.setattr("remixfun.downloads.shutil.disk_usage", lambda _: SimpleNamespace(free=1))
                with pytest.raises(Problem, match="free space"):
                    downloads.enqueue(FILE, "source:0")
                assert not calls and not downloads.list()
            finally: await downloads.close()
        asyncio.run(run())


def test_invalid_source_hash_and_provider_identity_cannot_be_replaced():
    source = record()
    source["raw"]["meta"]["civitaiResources"][0]["hash"] = "f" * 64
    assert build_plan(source)["dependencies"][0]["status"] == "blocked"
    def handler(_):
        return httpx.Response(200, json={"id": 128078, "modelId": 101055, "files": [
            {"id": 92696, "hashes": {"SHA256": "f" * 64}, "downloadUrl": "https://civitai.com/api/download/models/128078"}]})
    transport = ModelTransport(httpx.MockTransport(handler), MemoryCredentials())
    with pytest.raises(TransferError, match="identity changed"):
        transport.resolve(FILE)


def test_downloaded_checkpoint_is_explicit_in_authored_graph(tmp_path):
    from test_generation import FakeEngine, finished
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        inventory = client.app.state.service.inventory
        partial = inventory.root / "partials" / "owned.partial"; partial.write_bytes(DATA)
        inventory.publish(partial, FILE)
        recipe = client.post("/api/recipes", json={"prompt": "An owned fixture", "model_sha256": DIGEST}).json()
        assert recipe["raw"]["checkpoint_sha256"] == DIGEST
        job = finished(client, client.post(f"/api/imports/{recipe['id']}/reproduce").json()["id"])
        assert job["status"] == "completed"
        assert job["workflow"]["1"]["inputs"]["ckpt_name"] == DIGEST + ".safetensors"
        assert job["model_binding"]["sha256"] == DIGEST
        assert job["comparison"] == "not_tested"
        assert client.post("/api/recipes", json={"prompt": "test", "model_sha256": "f" * 64}).status_code == 409
