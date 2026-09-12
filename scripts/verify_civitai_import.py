"""Opt-in live import through the desktop/shared service; no browser dependency."""
import argparse
import hashlib
import io
import json
from pathlib import Path

import httpx
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service", default="http://127.0.0.1:8788")
    parser.add_argument("--output", type=Path, default=Path("artifacts/civitai-141984808/desktop"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with httpx.Client(base_url=args.service, timeout=120, trust_env=False) as client:
        health = client.get("/api/health")
        health.raise_for_status()
        response = client.post("/api/imports", json={"url": "https://civitai.com/images/141984808"})
        response.raise_for_status()
        record = response.json()
        assert record["source"]["image_id"] == "141984808"
        assert record["recipe"]["fields"]["seed"] == "119907136"
        assert len(record["recipe"]["resources"]) == 1
        assert record["recipe"]["resources"][0]["version_id"] == 128078
        assert record["media"], record["warning"]
        media = client.get(record["media"]["url"])
        media.raise_for_status()
        assert hashlib.sha256(media.content).hexdigest() == record["media"]["sha256"]
        with Image.open(io.BytesIO(media.content)) as source:
            assert source.size == (1024, 1024)
            source.verify()
        manifest = client.get(f"/api/imports/{record['id']}/manifest")
        manifest.raise_for_status()
        assert manifest.json() == record
        blocked = client.post(f"/api/imports/{record['id']}/reproduce")
        assert blocked.status_code == 409, blocked.text
        assert "scheduler" in blocked.json()["detail"]
        (args.output / "source.jpeg").write_bytes(media.content)
        (args.output / "manifest.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        report = {"health": health.json(), "import_id": record["id"], "media": record["media"],
                  "reproduction_status": blocked.status_code, "reproduction": blocked.json()}
        (args.output / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
