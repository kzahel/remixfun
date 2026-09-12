"""Imported attempt contracts using owned bytes, never fake GPU evidence."""
import copy
import hashlib
import io
import json
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image
import pytest

from remixfun.api import create_app
from remixfun.domain import normalize
from remixfun.provider import parse_page
from remixfun.reproduction import attempt_plan, compare_reference
from test_generation import FakeEngine, GENERATED_PNG, finished
from test_civitai_live_fixture import page, VERSION

DATA = b"owned checkpoint fixture, not weights"
SHA = hashlib.sha256(DATA).hexdigest()


def source_record(service, change=None, preview=GENERATED_PNG):
    raw, _, _ = parse_page(page(), "141984808")
    version = copy.deepcopy(VERSION)
    version["files"][0]["hashes"]["SHA256"] = SHA
    raw["model_versions"] = [{"version_id": "128078", "status": "identified", "model_id": 101055,
                              "base_model": "SDXL 1.0", "name": version["name"], "files": version["files"]}]
    if change: change(raw)
    source = service.save(raw, preview, {"kind": "civitai", "reference_quality": "owned_test_fixture"}, "Owned imported test")
    file = service.dependencies(source["id"])["dependencies"][0]["file"]
    if file:
        partial = service.inventory.root / "owned.part"
        partial.write_bytes(DATA)
        service.inventory.publish(partial, file)
    return source


def test_attempt_requires_current_plan_and_acceptance_preserves_source_and_replays(tmp_path):
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        source = source_record(client.app.state.service)
        path = f"/api/imports/{source['id']}"
        plan = client.get(path + "/dependencies").json()["reproduction"]
        assert plan["ready"] and plan["effective_recipe"]["fields"]["scheduler"] == "normal"
        assert source["recipe"]["fields"]["scheduler"] is None
        assert client.post(path + "/reproduce").status_code == 409
        assert client.post(path + "/reproduce", json={"revision": plan["revision"]}).status_code == 409
        assert client.post(path + "/reproduce", json={"revision": "f" * 64, "accept_assumptions": True}).status_code == 409
        assert client.get("/api/jobs").json() == []
        response = client.post(path + "/reproduce", json={"revision": plan["revision"], "accept_assumptions": True})
        assert response.status_code == 202, response.text
        job = finished(client, response.json()["id"])
        assert job["status"] == "completed", job["message"]
        assert job["source_recipe"] == source["recipe"]
        graph = json.loads(job["workflow_json"])
        assert graph["1"]["inputs"]["ckpt_name"] == SHA + ".safetensors"
        assert graph["5"]["inputs"]["sampler_name"] == "euler_ancestral"
        assert graph["5"]["inputs"]["seed"] == 119907136
        assert graph["5"]["inputs"]["cfg"] == 9.5 and graph["5"]["inputs"]["steps"] == 32
        assert graph["8"]["inputs"]["stop_at_clip_layer"] == -2
        assert graph["2"]["inputs"]["clip"] == graph["3"]["inputs"]["clip"] == ["8", 0]
        assert graph["3"]["inputs"]["text"] == source["recipe"]["fields"]["negative_prompt"]
        assert job["reference_comparison"]["status"] == "equal_reference_pixels"
        assert job["reference_comparison"]["exact_reproduction"] is False
        assert client.get(path + "/manifest").json() == source
        assert client.get(path + "/dependencies").json()["reproduction"]["revision"] == plan["revision"]
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        assert client.get(f"/api/jobs/{job['id']}").json()["attempt"] == plan
        assert client.get(path + "/manifest").json() == source


@pytest.mark.parametrize("settings", [
    {"sampler": "unmapped"}, {"scheduler": "unmapped"}, {"clipSkip": 13}, {"batchPosition": 2},
    {"batchSize": 4}, {"Hires upscale": 2}, {"extra": {"refiner": True}}, {"seed": None},
    {"prompt": "test <lora:missing:1>"}, {"width": 1025}, {"Model hash": "wrong"},
])
def test_unsupported_settings_are_not_silently_dropped(tmp_path, settings):
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        source = source_record(client.app.state.service, lambda raw: raw["meta"].update(settings))
        path = f"/api/imports/{source['id']}"
        plan = client.get(path + "/dependencies").json()["reproduction"]
        assert not plan["ready"]
        assert client.post(path + "/reproduce", json={"revision": plan["revision"], "accept_assumptions": True}).status_code == 409
        assert client.get("/api/jobs").json() == []


def test_known_scheduler_and_batch_are_retained_and_missing_model_invalidates_plan(tmp_path):
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        service = client.app.state.service
        source = source_record(service, lambda raw: raw["meta"].update(scheduler="Karras", batchSize=1, batchPosition=0))
        plan = service.dependencies(source["id"])["reproduction"]
        assert plan["effective_recipe"]["fields"]["scheduler"] == "karras"
        assert not any(a["field"] in {"scheduler", "batch"} for a in plan["assumptions"])
        service.inventory.target(SHA).write_bytes(b"corrupted")
        updated = service.dependencies(source["id"])["reproduction"]
        assert not updated["ready"] and updated["revision"] != plan["revision"]


def test_comparison_checks_rgb_when_alpha_is_identical_and_never_resizes():
    def png(color, size=(8, 8)):
        output = io.BytesIO(); Image.new("RGBA", size, color).save(output, "PNG"); return output.getvalue()
    result = compare_reference(png("red"), png("blue"), "provider_image_not_verified_original")
    assert result["status"] == "different_pixels" and result["mean_absolute_rgb_error"] > 0
    assert result["different_pixels"] == result["total_pixels"] == 64
    assert result["maximum_channel_error"] == 255
    equal = compare_reference(png("red"), png("red"), "test")
    assert equal["different_pixels"] == equal["maximum_channel_error"] == equal["root_mean_square_rgb_error"] == 0
    assert not result["exact_reproduction"]
    assert compare_reference(png("red"), png("red", (9, 9)), "test")["status"] == "different_dimensions"


def test_lost_reference_does_not_discard_a_successful_generation(tmp_path):
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        buffer = io.BytesIO(); Image.new("RGB", (1024, 1024), "white").save(buffer, "PNG")
        source = source_record(client.app.state.service, preview=buffer.getvalue())
        (tmp_path / "media" / source["media"]["name"]).write_bytes(b"damaged reference")
        path = f"/api/imports/{source['id']}"
        plan = client.get(path + "/dependencies").json()["reproduction"]
        response = client.post(path + "/reproduce", json={"revision": plan["revision"], "accept_assumptions": True})
        job = finished(client, response.json()["id"])
        assert job["status"] == "completed" and job["output"]
        assert job["comparison"] == "not_tested" and "comparison was unavailable" in job["message"]
        assert client.get(job["output"]["url"]).content == GENERATED_PNG


def test_output_artifact_repairs_damaged_existing_bytes(tmp_path):
    from remixfun.storage import Store
    store = Store(tmp_path)
    artifact = store.artifact(GENERATED_PNG, "png")
    path = tmp_path / "media" / artifact["name"]
    path.write_bytes(b"damaged cached output")
    assert store.artifact(GENERATED_PNG, "png") == artifact
    assert path.read_bytes() == GENERATED_PNG


def test_cli_shows_plan_then_runs_only_with_explicit_assumptions(tmp_path, monkeypatch, capsys):
    from remixfun import cli
    with TestClient(create_app(tmp_path, engine=FakeEngine()), base_url="http://127.0.0.1") as client:
        source = source_record(client.app.state.service)
        def request(base, method, path, **kwargs):
            response = client.request(method, path, **kwargs)
            assert response.is_success, response.text
            return response.json()
        monkeypatch.setattr(cli, "request", request)
        assert cli.main(["reproduce", source["id"]]) == 1
        assert "scheduler" in capsys.readouterr().out
        assert client.get("/api/jobs").json() == []
        assert cli.main(["reproduce", source["id"], "--accept-assumptions", "--wait"]) == 0
        job = json.loads(capsys.readouterr().out)
        assert job["status"] == "completed" and job["attempt"]["assumptions"]
