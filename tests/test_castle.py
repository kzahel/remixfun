"""Live castle metadata replay and bounded seed hypothesis contracts."""
import copy
import json
from pathlib import Path

from fastapi.testclient import TestClient
import httpx
import pytest

from remixfun.api import create_app
from remixfun.domain import normalize, parse_parameters, Problem
from remixfun.model_resolution import build_plan
from remixfun.model_transport import ModelTransport
from remixfun.reproduction import attempt_plan
from test_generation import FakeEngine, finished
from test_reproduction import source_record

RAW = json.loads((Path(__file__).parent / "fixtures/civitai-141866240/recipe.json").read_text())
SHA = "3304b2b91749c1ea2ccba3687e5329133b675e70b41f8aede3a9ca52f6b8b6df"


def test_embedded_png_parameters_agree_with_page_settings():
    text = (Path(__file__).parent / "fixtures/civitai-141866240/parameters.txt").read_text()
    embedded = normalize({"meta": parse_parameters(text)})["fields"]
    page_fields = normalize(RAW)["fields"]
    for key in ("prompt", "negative_prompt", "seed", "steps", "cfg", "sampler", "scheduler", "width", "height"):
        assert embedded[key] == page_fields[key]
    assert embedded["batch_position"] is None and embedded["batch_size"] is None


def record(raw=None):
    raw = copy.deepcopy(raw or RAW)
    return {"id": "castle", "raw": raw, "recipe": normalize(raw), "source": {"kind": "civitai"}}


def test_exact_hash_links_duplicate_source_references_without_changing_source():
    source = record(); before = copy.deepcopy(source)
    dependencies = build_plan(source)["dependencies"]
    assert len(source["recipe"]["resources"]) == 2 and len(dependencies) == 1
    dependency = dependencies[0]
    assert dependency["file"]["sha256"] == SHA
    assert dependency["selection_reason"] == "source_hash_match"
    assert dependency["linked_source_evidence"][0]["hash"] == "3304b2b917"
    dependency["status"] = "available"
    plan = attempt_plan(source, dependencies)
    assert plan["ready"], plan["blockers"]
    assert plan["effective_recipe"]["fields"]["sampler"] == "dpmpp_2m_sde"
    assert plan["effective_recipe"]["fields"]["scheduler"] == "karras"
    assert not any(a["field"] == "scheduler" for a in plan["assumptions"])
    assert source == before


@pytest.mark.parametrize("change", ["hash", "ambiguous", "style", "random", "hashes"])
def test_conflicting_or_unmapped_evidence_stays_blocked(change):
    source = record()
    if change == "hash": source["raw"]["meta"]["resources"][0]["hash"] = "aaaaaaaaaa"
    if change == "ambiguous":
        other = copy.deepcopy(source["raw"]["generation_data"]["resources"][0])
        other.update(versionId=1317650, modelVersionId=1317650)
        source["raw"]["generation_data"]["resources"].append(other)
        version = copy.deepcopy(source["raw"]["model_versions"][0]); version["version_id"] = "1317650"
        source["raw"]["model_versions"].append(version)
    if change == "style": source["raw"]["meta"]["Style Selector Style"] = "unresolved-style"
    if change == "random": source["raw"]["meta"]["Style Selector Randomize"] = "True"
    if change == "hashes": source["raw"]["meta"]["hashes"]["model"] = "aaaaaaaaaa"
    source["recipe"] = normalize(source["raw"])
    dependencies = build_plan(source)["dependencies"]
    for dependency in dependencies:
        if dependency["file"]: dependency["status"] = "available"
    assert not attempt_plan(source, dependencies)["ready"]


def test_seed_offset_requires_its_own_reviewed_plan_and_preserves_base_seed(tmp_path):
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        source = source_record(client.app.state.service)
        path = f"/api/imports/{source['id']}"
        zero = client.get(path + "/dependencies").json()["reproduction"]
        plan = client.get(path + "/dependencies", params={"seed_offset": 3}).json()["reproduction"]
        assert plan["revision"] != zero["revision"]
        assert plan["effective_recipe"]["fields"]["seed"] == "119907139"
        assert client.post(path + "/reproduce", json={"revision": zero["revision"], "accept_assumptions": True, "seed_offset": 3}).status_code == 409
        job = finished(client, client.post(path + "/reproduce", json={"revision": plan["revision"], "accept_assumptions": True, "seed_offset": 3}).json()["id"])
        assert job["workflow"]["5"]["inputs"]["seed"] == 119907139
        assert job["source_recipe"]["fields"]["seed"] == "119907136"
        assert client.get(path + "/manifest").json() == source
        assert client.get(path + "/dependencies", params={"seed_offset": 32}).status_code == 422
        assert client.post(path + "/reproduce", json={"seed_offset": True}).status_code == 422


def test_explicit_batch_position_and_seed_overflow_block_offset_hypotheses():
    source = record(); deps = build_plan(source)["dependencies"]; deps[0]["status"] = "available"
    source["recipe"]["fields"]["batch_position"] = 0
    assert not attempt_plan(source, deps, 1)["ready"]
    source["recipe"]["fields"].update(batch_position=None, seed=str(2**64 - 1))
    assert not attempt_plan(source, deps, 1)["ready"]
    with pytest.raises(Problem): attempt_plan(source, deps, -1)


def test_b2_redirect_keeps_credentials_off_storage():
    seen = []
    file = build_plan(record())["dependencies"][0]["file"]
    class Credentials:
        def get(self): return "owned-test-secret"
    def handler(request):
        seen.append(request)
        if request.url.path.startswith("/api/v1/"):
            return httpx.Response(200, json={"id": 1317649, "modelId": 1171106, "files": [{"id": 1221707,
                "hashes": {"SHA256": SHA}, "downloadUrl": "https://civitai.com/api/download/models/1317649"}]})
        if request.url.host == "civitai.com":
            return httpx.Response(307, headers={"location": "https://b2.civitai.com/file/civitai-modelfiles/owned?signature=ephemeral"})
        return httpx.Response(200, content=b"owned transport fixture")
    with ModelTransport(httpx.MockTransport(handler), Credentials()).stream(file) as response:
        assert response.read() == b"owned transport fixture"
    assert seen[0].headers["authorization"] == "Bearer owned-test-secret"
    assert "authorization" not in seen[-1].headers
