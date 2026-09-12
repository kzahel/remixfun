"""Owned synthetic pages derived from supplied findings; no live network tests."""
import asyncio
import copy
import json
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from remixfun.api import create_app
from remixfun.domain import Problem, normalize
from remixfun.provider import Civitai, parse_page

IMAGE = 141984808
UUID = "11111111-2222-3333-4444-555555555555"
URL = f"https://civitai.com/images/{IMAGE}"
CDN = f"https://image.civitai.com/test-bucket/{UUID}/original=true/{UUID}.jpeg"
META = {"prompt": "A lake, with <clouds> & trees", "seed": 18446744073709551614,
        "Model hash": "reported-hash", "Created Date": "2026-09-12",
        "arbitrary": {"nested": [1, 2]}, "civitaiResources": [{"modelVersionId": 27, "type": "checkpoint"}]}
RESOURCES = [{"modelId": 100 + i, "versionId": 200 + i, "modelName": f"Resource {i}",
              "modelType": "LORA", "strength": i / 10, "baseModel": "SDXL 1.0"} for i in range(6)]


def query(method, data, identifier=IMAGE):
    return {"queryKey": [["image", method], {"input": {"id": identifier}, "type": "query"}],
            "state": {"status": "success", "data": data}}


def queries(meta=META):
    return [
        query("getGenerationData", {"meta": {"prompt": "WRONG CAROUSEL IMAGE", "cfgScale": 88}}, 7),
        query("get", {"id": 7, "url": "decoy"}, 7),
        query("get", {"id": IMAGE, "url": UUID, "baseModel": "SDXL 1.0"}),
        query("getGenerationData", {"meta": copy.deepcopy(meta), "resources": copy.deepcopy(RESOURCES),
                                    "tools": ["comfy"], "process": "txt2img", "displayKeys": ["prompt", "seed"]}),
    ]


def page(entries=None, prefix=True):
    data = {"props": {"pageProps": {"trpcState": {"json": {"queries": entries if entries is not None else queries()}}}}}
    reference = '<img src="https://image.civitai.com/test-bucket/another-image/width=450/example.jpeg">' if prefix else ""
    return f'<html><body>{reference}<script type="application/json" id="__NEXT_DATA__">{json.dumps(data)}</script></body></html>'


def acquire(handler, **options):
    async def no_sleep(_):
        pass
    return asyncio.run(Civitai(httpx.MockTransport(handler), resolve_versions=False, sleep=no_sleep, **options).acquire(URL))


def test_selects_exact_query_and_preserves_generator_specific_evidence():
    raw, url, warnings = parse_page(page(), str(IMAGE))
    assert raw["meta"] == META
    assert raw["generation_data"]["tools"] == ["comfy"]
    assert raw["generation_data"]["process"] == "txt2img"
    assert raw["generation_data"]["displayKeys"] == ["prompt", "seed"]
    assert raw["generation_data"]["resources"] == RESOURCES
    assert raw["acquisition"]["image_id"] == str(IMAGE)
    assert url == CDN and not warnings
    recipe = normalize(raw)
    assert recipe["fields"]["seed"] == "18446744073709551614"
    assert recipe["fields"]["cfg"] is None
    assert recipe["fields"]["sampler"] is None
    assert len(recipe["resources"]) == 7
    assert recipe["resources"][1]["weight"] == 0
    assert recipe["resources"][1]["version_id"] == 200
    assert recipe["resources"][1]["evidence"] == "generation_data.resources"


def test_hidden_metadata_preserves_resources_without_inventing_settings():
    entries = queries(None)
    entries[2]["state"]["data"]["hideMeta"] = True
    raw, _, warnings = parse_page(page(entries), str(IMAGE))
    assert raw["meta"] is None and raw["hideMeta"] is True
    assert raw["baseModel"] == "SDXL 1.0"
    assert len(normalize(raw)["resources"]) == 6
    assert normalize(raw)["fields"]["prompt"] is None
    assert "hidden" in warnings[0]


def test_missing_generation_query_is_partial_not_carousel_metadata():
    raw, _, warnings = parse_page(page(queries()[:-1]), str(IMAGE))
    assert raw["meta"] is None
    assert raw["generation_data"] is None
    assert warnings


@pytest.mark.parametrize("entries", [[], [query("get", {"id": 7}, 7)],
    [{"queryKey": [["hiddenPreferences", "getHidden"]], "state": {"data": {}}}],
    [query("getGenerationData", {"meta": META})]])
def test_http_200_missing_image_is_not_found(entries):
    with pytest.raises(Problem) as exc:
        parse_page(page(entries), str(IMAGE))
    assert exc.value.status == 404


@pytest.mark.parametrize("identifier", [7, None, True, float(IMAGE)])
def test_query_input_id_must_match(identifier):
    entries = queries()
    entries[2]["queryKey"][1]["input"]["id"] = identifier
    with pytest.raises(Problem) as exc:
        parse_page(page(entries), str(IMAGE))
    assert exc.value.status == 404


def test_image_payload_id_and_duplicate_queries_fail_closed():
    entries = queries()
    entries[2]["state"]["data"]["id"] = 7
    with pytest.raises(Problem, match="different image"):
        parse_page(page(entries), str(IMAGE))
    entries = queries()
    entries.append(copy.deepcopy(entries[-1]))
    with pytest.raises(Problem, match="ambiguous"):
        parse_page(page(entries), str(IMAGE))


@pytest.mark.parametrize("content", ['<html>Forbidden</html>', '<script id="__NEXT_DATA__">not json</script>',
    '<script id="__NEXT_DATA__">{}</script>', '<script id="__NEXT_DATA__">null</script>'])
def test_unrecognized_or_blocked_page_is_not_reported_deleted(content):
    with pytest.raises(Problem) as exc:
        parse_page(content, str(IMAGE))
    assert exc.value.status == 502


def test_page_first_rest_only_enriches_url_and_cdn_redirect_works(tmp_path):
    calls = []
    image = (Path(__file__).parent / "fixtures/metadata.png").read_bytes()
    canonical = "https://image.civitai.com/test-bucket/canonical/image.png"
    redirected = "https://image.civitai.com/test-bucket/canonical/final.png"
    def handler(request):
        calls.append(str(request.url))
        assert request.headers["user-agent"].startswith("Mozilla/5.0")
        assert "authorization" not in request.headers and "cookie" not in request.headers
        if request.url.path == f"/images/{IMAGE}":
            return httpx.Response(200, text=page())
        if request.url.path == "/api/v1/images":
            assert request.url.params["imageId"] == str(IMAGE)
            return httpx.Response(200, json={"items": [{"id": IMAGE, "url": canonical, "meta": None}]})
        if str(request.url) == canonical:
            return httpx.Response(301, headers={"location": redirected})
        assert str(request.url) == redirected
        return httpx.Response(200, content=image, headers={"content-type": "image/png"})
    provider = Civitai(httpx.MockTransport(handler), resolve_versions=False, retries=0)
    with TestClient(create_app(tmp_path, provider=provider), base_url="http://127.0.0.1") as client:
        response = client.post("/api/imports", json={"url": URL})
        assert response.status_code == 201
        record = response.json()
        assert record["raw"]["meta"] == META
        assert '18446744073709551614' in record["raw_json"]
        assert record["recipe"]["fields"]["seed"] == '18446744073709551614'
        assert record["raw"]["acquisition"]["preview_source"] == "rest_image_url"
        assert record["raw"]["acquisition"]["download_url"] == redirected
        assert client.get(record["media"]["url"]).content == image
    assert calls[0] == URL and len(calls) == 4


@pytest.mark.parametrize("status,body", [(403, {}), (200, {"items": None}), (200, {"items": [{"id": 7, "url": "https://image.civitai.com/wrong"}]}),
    (200, {"items": [{"id": IMAGE, "meta": {"prompt": "DO NOT USE REST"}}]})])
def test_optional_rest_failure_never_discards_page_metadata(status, body):
    def handler(request):
        if request.url.path.startswith("/images/"):
            return httpx.Response(200, text=page(prefix=False))
        return httpx.Response(status, json=body)
    result = acquire(handler, retries=0)
    assert result[1]["meta"] == META and result[2] is None
    assert "preview" in result[3]


def test_no_rest_and_missing_prefix_do_not_guess_a_cdn_account():
    calls = []
    def handler(request):
        calls.append(str(request.url))
        return httpx.Response(200, text=page(prefix=False))
    result = acquire(handler, use_rest=False)
    assert calls == [URL] and result[2] is None


def test_corrupt_preview_does_not_lose_imported_recipe(tmp_path):
    def handler(request):
        if request.url.host == "civitai.com":
            return httpx.Response(200, text=page())
        return httpx.Response(200, content=b"invalid image", headers={"content-type": "image/jpeg"})
    provider = Civitai(httpx.MockTransport(handler), resolve_versions=False, use_rest=False)
    with TestClient(create_app(tmp_path, provider=provider), base_url="http://127.0.0.1") as client:
        response = client.post("/api/imports", json={"url": URL})
        assert response.status_code == 201
        record = response.json()
        assert record["raw"]["meta"] == META
        assert record["media"] is None
        assert "not a valid" in record["warning"]


@pytest.mark.parametrize("location", ["http://127.0.0.1/private", "https://example.com/private", "https://image.civitai.com:444/private", "https://image.civitai.com/private?token=secret"])
def test_cdn_redirect_cannot_escape_allowlist(location):
    calls = []
    def handler(request):
        calls.append(str(request.url))
        if request.url.host == "civitai.com":
            return httpx.Response(200, text=page())
        return httpx.Response(301, headers={"location": location})
    result = acquire(handler, use_rest=False)
    assert result[1]["meta"] == META and result[2] is None
    assert calls == [URL, CDN]


@pytest.mark.parametrize("status,expected,count", [(401, 502, 1), (403, 502, 1), (404, 404, 1), (429, 503, 3), (503, 502, 3)])
def test_page_errors_and_bounded_transient_retries(status, expected, count):
    calls = []
    def handler(request):
        calls.append(str(request.url))
        return httpx.Response(status)
    with pytest.raises(Problem) as exc:
        acquire(handler)
    assert exc.value.status == expected and len(calls) == count
    if status == 403:
        assert "original image file" in exc.value.message
        assert "API key" not in exc.value.message


def test_retry_recovers_without_requerying_after_success():
    calls = []
    def handler(request):
        calls.append(str(request.url))
        return httpx.Response(503) if len(calls) < 2 else httpx.Response(200, text=page(prefix=False))
    assert acquire(handler, use_rest=False)[1]["meta"] == META
    assert len(calls) == 2


def test_html_response_size_is_bounded(monkeypatch):
    monkeypatch.setattr("remixfun.provider.MAX_HTML", 20)
    with pytest.raises(Problem, match="size limit"):
        acquire(lambda req: httpx.Response(200, text=page()))


def test_redirect_to_another_image_cannot_import_its_recipe():
    def handler(request):
        if str(request.url) == URL:
            return httpx.Response(302, headers={"location": "https://civitai.com/images/7"})
        return httpx.Response(200, text=page())
    with pytest.raises(Problem, match="different image"):
        acquire(handler)
