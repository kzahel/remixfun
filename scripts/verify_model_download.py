"""Opt-in real Civitai model transfer, service restart/reuse and optional GPU handoff."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time

import httpx
from platformdirs import user_data_path

DIGEST = "e6bb9ea85bbf7bf6478a7c6d18b71246f22e95d41bcdd80ed40aa212c33cfeff"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", type=Path, default=Path(user_data_path("Remixfun", appauthor=False)) / "models")
    parser.add_argument("--output", type=Path, default=Path("artifacts/model-download-live"))
    parser.add_argument("--comfy-root", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    process = None
    token = secrets.token_urlsafe(32)
    log = (args.output / "service.log").open("ab")
    report = {"source": "https://civitai.com/images/141984808", "expected_sha256": DIGEST}
    client = httpx.Client(base_url=base, timeout=40, trust_env=False)
    def request(method, path, **kwargs):
        response = client.request(method, path, **kwargs); response.raise_for_status(); return response.json()
    def start(gpu=False):
        nonlocal process
        command = [sys.executable, "-m", "remixfun.cli", "serve", "--port", str(port), "--data-dir", str(args.output / "library"),
                   "--model-dir", str(args.model_dir), "--instance", "model-download-verification"]
        if gpu: command += ["--comfy-root", str(args.comfy_root)]
        process = subprocess.Popen(command, env={**os.environ, "REMIXFUN_OWNER_TOKEN": token}, stdout=log, stderr=log,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        deadline = time.monotonic() + 150
        while time.monotonic() < deadline:
            if process.poll() is not None: raise RuntimeError("Verification service failed; inspect its log.")
            try:
                request("GET", "/api/health"); return
            except httpx.HTTPError: time.sleep(.25)
        raise RuntimeError("Service startup timed out")
    def stop():
        nonlocal process
        if process and process.poll() is None:
            request("POST", "/api/shutdown", headers={"X-Remixfun-Owner": token})
            process.wait(timeout=45)
        process = None
    try:
        start()
        source = request("POST", "/api/imports", json={"url": report["source"]})
        identifier = source["id"]
        report["import_id"] = identifier
        path = f"/api/imports/{identifier}"
        request("POST", path + "/dependencies/resolve")
        for _ in range(180):
            plan = request("GET", path + "/dependencies")
            if not plan.get("operation") or plan["operation"]["status"] not in {"queued", "running"}: break
            time.sleep(.5)
        assert len(plan["dependencies"]) == 1 and plan["dependencies"][0]["file"]["sha256"] == DIGEST
        report["file"] = plan["dependencies"][0]["file"]
        submitted = request("POST", path + "/downloads", json={"revision": plan["revision"]})
        job_id = submitted["dependencies"]["0"].get("download_id")
        if job_id:
            deadline = time.monotonic() + 1800
            paused, last = False, 0
            while time.monotonic() < deadline:
                job = request("GET", f"/api/downloads/{job_id}")
                if job["status"] in {"failed", "canceled"}: raise RuntimeError(job["message"])
                if job["status"] == "ready": break
                if not paused and job["status"] == "downloading" and job["downloaded_bytes"] >= 64 * 1024**2:
                    job = request("POST", f"/api/downloads/{job_id}/pause")
                    report["paused_bytes"] = job["downloaded_bytes"]
                    stop(); start()
                    assert request("GET", f"/api/downloads/{job_id}")["status"] == "paused"
                    request("POST", f"/api/downloads/{job_id}/resume")
                    paused = True
                    print(f"Paused and restarted at {report['paused_bytes']} bytes; resumed same file.", flush=True)
                if time.monotonic() - last >= 10:
                    print(f"{job['status']}: {job['downloaded_bytes']} / {job['total_bytes']}", flush=True); last = time.monotonic()
                time.sleep(.25)
            else: raise RuntimeError("Download wait expired")
            report["download"] = job
            assert job["status"] == "ready"
            if report.get("paused_bytes"): assert job["resumed_from"] == report["paused_bytes"]
        stop(); start()
        ready = request("GET", path + "/dependencies")
        assert ready["dependencies"][0]["status"] == "available"
        reused = request("POST", path + "/downloads", json={"revision": ready["revision"]})
        assert reused["dependencies"]["0"] == {"status": "available", "download_id": None}
        assert request("GET", path + "/manifest") == source
        report.update(reuse_after_restart=True, source_unchanged=True)
        print("Verified model persisted and was reused after service restart.", flush=True)
        if args.comfy_root:
            stop(); start(gpu=True)
            recipe = request("POST", "/api/recipes", json={"prompt": "A quiet alpine lake at sunrise, a red canoe on still water, realistic landscape photograph",
                "seed": "42", "model_sha256": DIGEST})
            job = request("POST", f"/api/imports/{recipe['id']}/reproduce")
            while job["status"] in {"queued", "running"}:
                time.sleep(1); job = request("GET", f"/api/jobs/{job['id']}")
            assert job["status"] == "completed", job["message"]
            assert job["model_binding"]["sha256"] == DIGEST
            content = client.get(job["output"]["url"]).content
            assert hashlib.sha256(content).hexdigest() == job["output"]["sha256"]
            (args.output / "generated.png").write_bytes(content)
            report["generation"] = job
            print("Downloaded checkpoint generated a new authored image through the service.", flush=True)
        (args.output / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    finally:
        try: stop()
        finally: client.close(); log.close()


if __name__ == "__main__": main()
