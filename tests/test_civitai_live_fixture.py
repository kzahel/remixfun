"""Offline replay of selected live metadata; preview bytes are an owned fixture."""
import copy
import json
from pathlib import Path

from fastapi.testclient import TestClient
import httpx
import pytest

from remixfun.api import create_app
from remixfun.domain import normalize
from remixfun.provider import Civitai, parse_page

FIXTURES = Path(__file__).parent / "fixtures"
QUERIES = json.loads((FIXTURES / "civitai-141984808/queries.json").read_text())
VERSION = json.loads((FIXTURES / "civitai-141984808/model-version.json").read_text())
URL = "https://civitai.com/images/141984808"
BLOB = "https://blobs-b2.civitai.com/file/blobs-managed-public/owned.jpg"
PNG = (FIXTURES / "metadata.png").read_bytes()


def page():
    payload = {"props": {"pageProps": {"trpcState": {"json": {"queries": QUERIES}}}}}
    return '<img src="https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/example">' + '<script id="__NEXT_DATA__">' + json.dumps(payload) + '</script>'


def test_live_recipe_blob_redirect_version_identity_and_restart(tmp_path):
    calls = []
    def handler(request):
        calls.append(str(request.url))
        if request.url.path == "/images/141984808":
            return httpx.Response(200, text=page())
        if request.url.path == "/api/v1/model-versions/128078":
            return httpx.Response(200, json={**VERSION, "images": [{"meta": {"prompt": "Wrong gallery recipe"}}]})
        if request.url.host == "image.civitai.com":
            return httpx.Response(301, headers={"location": BLOB})
        assert str(request.url) == BLOB
        return httpx.Response(200, content=PNG, headers={"content-type": "image/png"})
    provider = Civitai(httpx.MockTransport(handler), use_rest=False)
    with TestClient(create_app(tmp_path, provider=provider), base_url="http://127.0.0.1") as client:
        response = client.post("/api/imports", json={"url": URL})
        assert response.status_code == 201
        record = response.json()
        fields = record["recipe"]["fields"]
        assert "a beetle with a shell like stained glass" in fields["prompt"]
        assert fields["seed"] == "119907136" and fields["steps"] == 32
        assert fields["cfg"] == 9.5 and fields["sampler"] == "Euler a"
        assert fields["clip_skip"] == 2 and fields["scheduler"] is None
        assert record["recipe"]["unknown"] == ["scheduler"]
        assert record["recipe"]["batch_strategy"] == "unknown"
        assert record["warning"] is None
        resources = record["recipe"]["resources"]
        assert len(resources) == 1
        model = resources[0]
        assert model["name"] == "SD XL" and model["version_name"] == "v1.0 VAE fix"
        assert model["model_id"] == 101055 and model["version_id"] == 128078
        assert model["files"][0]["id"] == 92696
        assert model["files"][0]["hashes"]["SHA256"] == "E6BB9EA85BBF7BF6478A7C6D18B71246F22E95D41BCDD80ED40AA212C33CFEFF"
        assert model["file_id"] is None and model["hash"] is None and model["status"] == "unresolved"
        assert len(model["evidence_sources"]) == 2
        assert record["raw"]["meta"] == QUERIES[1]["state"]["data"]["meta"]
        assert client.get(record["media"]["url"]).content == PNG
        assert record["raw"]["acquisition"]["download_url"] == BLOB
        assert record["reproduction"]["status"] == "blocked"
        blocked = client.post(f"/api/imports/{record['id']}/reproduce")
        assert blocked.status_code == 409
        assert "different from the configured" in blocked.json()["detail"]
        plan = client.get(f"/api/imports/{record['id']}/dependencies").json()
        assert any(a["field"] == "scheduler" for a in plan["reproduction"]["assumptions"])
        assert client.get("/api/jobs").json() == []
    assert len(calls) == 4  # Duplicate source references require only one version lookup.
    with TestClient(create_app(tmp_path), base_url="http://127.0.0.1") as client:
        assert client.get(f"/api/imports/{record['id']}/manifest").json() == record


@pytest.mark.parametrize("version", [{"id": 7}, {**VERSION, "files": None}, None])
def test_failed_or_mismatched_version_lookup_preserves_recipe(tmp_path, version):
    def handler(request):
        if request.url.path.startswith("/images/"):
            return httpx.Response(200, text=page())
        if request.url.path.startswith("/api/v1/model-versions/"):
            return httpx.Response(200, json=version)
        return httpx.Response(403)
    provider = Civitai(httpx.MockTransport(handler), use_rest=False, retries=0)
    with TestClient(create_app(tmp_path, provider=provider), base_url="http://127.0.0.1") as client:
        record = client.post("/api/imports", json={"url": URL}).json()
        assert record["recipe"]["fields"]["seed"] == "119907136"
        assert record["recipe"]["resources"][0]["files"] == []
        assert record["raw"]["model_versions"][0]["status"] == "unavailable"
        assert "model-version details" in record["warning"]


def test_conflicting_source_identities_and_zero_strength_are_not_merged():
    raw, _, _ = parse_page(page(), "141984808")
    raw["meta"]["civitaiResources"][0]["weight"] = 0
    raw["generation_data"]["resources"][0]["strength"] = 1
    assert len(normalize(raw)["resources"]) == 2
    assert normalize(raw)["resources"][0]["weight"] == 0
    raw["generation_data"]["resources"][0]["strength"] = 0
    assert len(normalize(raw)["resources"]) == 1
    raw["meta"]["civitaiResources"].append(copy.deepcopy(raw["meta"]["civitaiResources"][0]))
    assert len(normalize(raw)["resources"]) == 2
