import asyncio
import io
import json
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient as FastAPITestClient
from functools import partial
from PIL import Image, PngImagePlugin

from remixfun.api import create_app
from remixfun.cli import main
from remixfun.domain import Problem, image_id, normalize
from remixfun.provider import Civitai, redact
from remixfun.service import Service

TestClient = partial(FastAPITestClient, base_url="http://127.0.0.1")


def png(parameters=None, graph=None):
    buffer = io.BytesIO()
    info = PngImagePlugin.PngInfo()
    if parameters:
        info.add_text("parameters", parameters)
    if graph:
        info.add_text("prompt", graph)
    Image.new("RGB", (32, 24), "#78908a").save(buffer, format="PNG", pnginfo=info)
    return buffer.getvalue()


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(tmp_path / "library with spaces", demo_delay=0.01)) as value:
        yield value


@pytest.mark.parametrize("url", ["https://evil.test/civitai.com/images/123", "http://civitai.com/images/123", "https://civitai.com.evil.test/images/123", "https://me@civitai.com/images/123", "https://civitai.com:444/images/123", "https://civitai.com/models/123", "https://civitai.com/images/-1", "file:///images/123"])
def test_url_boundary(url):
    with pytest.raises(Problem):
        image_id(url)


def test_recipe_never_guesses_or_loses_large_seed():
    raw = {"width": 200, "height": 300, "meta": {"seed": 18446744073709551614, "steps": "-1", "prompt": {"subject": "tree"}, "Batch pos": 3,
           "civitaiResources": [{"modelId": 12, "modelVersionId": 34, "fileId": 56, "hash": "abcd", "type": "checkpoint"}], "unrecognized": "evidence"}}
    recipe = normalize(raw)
    assert recipe["fields"]["seed"] == "18446744073709551614"
    assert recipe["fields"]["width"] is None # web dimensions are not generation dimensions
    assert recipe["fields"]["steps"] is None
    assert recipe["fields"]["prompt"] is None # structured prompts need a reviewed adapter
    assert recipe["fields"]["batch_position"] == 3
    assert recipe["batch_strategy"] == "unknown"
    assert recipe["resources"][0]["version_id"] == 34
    assert raw["meta"]["unrecognized"] == "evidence"


@pytest.mark.parametrize("seed", [-1, True, 1.5, "1.0", "NaN", 2**64])
def test_invalid_seeds_remain_unknown(seed):
    assert normalize({"meta": {"seed": seed}})["fields"]["seed"] is None


def test_import_upload_preserves_evidence_and_survives_restart(tmp_path):
    raw_text = "A lake\nNegative prompt: fog\nSteps: 25, Sampler: DPM++ 2M, CFG scale: 6.5, Seed: 18446744073709551614, Size: 1024x1024, Custom: retained"
    content = png(raw_text)
    root = tmp_path / "library with spaces"
    with TestClient(create_app(root)) as client:
        response = client.post("/api/imports/file", files={"file": ("lake.png", content, "image/png")})
        assert response.status_code == 201
        record = response.json()
        assert record["raw"]["embedded_metadata"]["parameters"] == raw_text
        assert record["recipe"]["fields"]["scheduler"] is None
        assert record["recipe"]["fields"]["width"] == 1024
        assert record["image"]["width"] == 32
        assert client.get(record["media"]["url"]).content == content
        assert client.post(f"/api/imports/{record['id']}/reproduce").status_code == 409
    with TestClient(create_app(root)) as client:
        assert client.get(f"/api/imports/{record['id']}/manifest").json() == record
        assert len(client.get("/api/imports").json()) == 1


def test_graph_preserved_without_flattening(client):
    graph = '{"1": {"class_type": "UnknownNode"}}'
    record = client.post("/api/imports/file", files={"file": ("graph.png", png(graph=graph))}).json()
    assert record["raw"]["embedded_metadata"]["prompt"] == graph
    assert record["recipe"]["fields"]["prompt"] is None
    assert record["warning"]


def test_invalid_upload_and_oversize(client):
    assert client.post("/api/imports/file", files={"file": ("bad.png", b"not an image")}).status_code == 422
    from remixfun.provider import MAX_IMAGE
    assert client.post("/api/imports/file", files={"file": ("big.png", b"x" * (MAX_IMAGE + 1))}).status_code == 422
    assert client.get("/api/imports").json() == []


def test_local_origin_and_media_boundaries(client):
    assert client.post("/api/demo", headers={"Origin": "https://evil.test"}).status_code == 403
    assert client.get("/api/health", headers={"Host": "evil.test"}).status_code == 403
    assert client.get("/api/health", headers={"Host": "testserver"}).status_code == 403
    assert client.get("/api/media/library.sqlite3").status_code == 404
    assert client.get("/api/media/" + "a" * 64 + ".png").status_code == 404
    assert client.post("/api/demo", headers={"Origin": "http://localhost:5173"}).status_code == 201


def test_demo_result_has_no_exactness_claim(client):
    record = client.post("/api/demo").json()
    assert client.post("/api/demo").json()["id"] == record["id"]
    response = client.post(f"/api/imports/{record['id']}/reproduce")
    assert response.status_code == 202
    identifier = response.json()["id"]
    import time
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        job = client.get(f"/api/jobs/{identifier}").json()
        if job["status"] == "completed":
            break
        time.sleep(0.01)
    assert job["status"] == "completed"
    assert job["comparison"] == "not_applicable"
    assert job["engine"] == "demo"
    assert job["recipe"] == record["recipe"]
    assert job["output"] == record["media"]


def test_interrupted_job_recovered(tmp_path):
    service = Service(tmp_path)
    service.store.put({"id": "unfinished", "status": "running"}, "job")
    with TestClient(create_app(tmp_path)) as client:
        assert client.get("/api/jobs/unfinished").json()["status"] == "interrupted"


def test_shutdown_marks_demo_interrupted(tmp_path):
    with TestClient(create_app(tmp_path, demo_delay=60)) as client:
        record = client.post("/api/demo").json()
        job = client.post(f"/api/imports/{record['id']}/reproduce").json()
    assert Service(tmp_path).store.get(job["id"], "job")["status"] == "interrupted"


def test_provider_preserves_requested_identity_and_requests_metadata(tmp_path):
    def handler(request):
        assert request.url.params["imageId"] == "123"
        assert request.url.params["withMeta"] == "true"
        return httpx.Response(200, json={"items": [{"id": 123, "meta": {"seed": 18446744073709551614, "prompt": "a lake", "unknown": "keep"}}]})
    provider = Civitai(httpx.MockTransport(handler))
    with TestClient(create_app(tmp_path, provider=provider)) as client:
        response = client.post("/api/imports", json={"url": "https://civitai.com/images/123?foo=bar"})
        assert response.status_code == 201
        record = response.json()
        assert record["source"]["url"] == "https://civitai.com/images/123"
        assert record["raw"]["meta"]["unknown"] == "keep"
        assert '18446744073709551614' in record["raw_json"]
        assert record["recipe"]["fields"]["seed"] == '18446744073709551614'
        assert record["media"] is None


@pytest.mark.parametrize("status,body,expected", [(403, {}, 502), (429, {}, 503), (200, {"items": [{"id": 999}]}, 404), (500, {}, 502)])
def test_provider_failures_are_actionable(tmp_path, status, body, expected):
    provider = Civitai(httpx.MockTransport(lambda req: httpx.Response(status, json=body)))
    with TestClient(create_app(tmp_path, provider=provider)) as client:
        response = client.post("/api/imports", json={"url": "https://civitai.com/images/123"})
        assert response.status_code == expected
        assert isinstance(response.json()["detail"], str)
        assert client.get("/api/imports").json() == []


def test_provider_does_not_fetch_arbitrary_preview_host():
    calls = []
    def handler(request):
        calls.append(str(request.url))
        return httpx.Response(200, json={"items": [{"id": 123, "url": "http://127.0.0.1/private"}]})
    result = asyncio.run(Civitai(httpx.MockTransport(handler)).acquire("https://civitai.com/images/123"))
    assert len(calls) == 1
    assert result[2] is None


@pytest.mark.parametrize("body", [None, [], {"items": None}])
def test_malformed_provider_response_is_actionable(tmp_path, body):
    provider = Civitai(httpx.MockTransport(lambda req: httpx.Response(200, content=json.dumps(body), headers={"Content-Type": "application/json"})))
    with TestClient(create_app(tmp_path, provider=provider)) as client:
        response = client.post("/api/imports", json={"url": "https://civitai.com/images/123"})
        assert response.status_code == 502
        assert client.get("/api/imports").json() == []


def test_redaction():
    assert redact({"token": "secret", "nested": ["https://example.com/file?token=secret"], "prompt": "A lake"}) == {
        "nested": ["[transient URL omitted]"], "prompt": "A lake"}


def test_cli_uses_same_http_contract(monkeypatch, capsys):
    calls = []
    def fake_request(base, method, path, **kwargs):
        calls.append((method, path, kwargs))
        return {"id": "saved"}
    monkeypatch.setattr("remixfun.cli.request", fake_request)
    assert main(["import", "https://civitai.com/images/123", "--json"]) == 0
    assert calls == [("POST", "/api/imports", {"json": {"url": "https://civitai.com/images/123"}})]
    assert json.loads(capsys.readouterr().out)["id"] == "saved"


def test_cli_disallows_remote_listening():
    with pytest.raises(SystemExit) as exc:
        main(["serve", "--host", "0.0.0.0"])
    assert exc.value.code == 2
