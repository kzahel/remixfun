"""Opt-in real SDXL CLI run against a managed local Comfy runtime."""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

import httpx
from PIL import Image

from remixfun.engine import CHECKPOINT_SHA256, COMFY_REVISION


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comfy-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("artifacts/gpu-cli"))
    parser.add_argument("--expected-device", choices=("cuda", "mps"),
                        default="mps" if sys.platform == "darwin" else "cuda")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    command = [sys.executable, "-m", "remixfun.cli"]
    log = (args.output / "service.log").open("ab")
    process = None

    def request(client, path):
        response = client.get(path)
        response.raise_for_status()
        return response.json()

    def start(gpu):
        nonlocal process
        invocation = [*command, "serve", "--port", str(port), "--data-dir", str(args.output / "library")]
        if gpu:
            invocation += ["--comfy-root", str(args.comfy_root.resolve())]
        process = subprocess.Popen(invocation, stdout=log, stderr=log,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        with httpx.Client(base_url=base, timeout=5, trust_env=False) as client:
            deadline = time.monotonic() + (150 if gpu else 30)
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError(f"Service exited during startup; inspect {args.output / 'service.log'}")
                try:
                    return request(client, "/api/health")
                except httpx.HTTPError:
                    time.sleep(.25)
        raise RuntimeError(f"Service startup timed out; inspect {args.output / 'service.log'}")

    def stop():
        nonlocal process
        if process is not None:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)
            process = None

    def cli(*parts, timeout=30):
        result = subprocess.run([*command, "--service", base, *parts], capture_output=True,
                                text=True, timeout=timeout, check=True)
        return json.loads(result.stdout)

    try:
        health = start(gpu=True)
        assert health["engine"] == "comfy"
        recipe = cli("create", "A quiet alpine lake at sunrise with a small red canoe, realistic landscape photograph",
                     "--seed", "42", "--json")
        assert recipe["raw"]["checkpoint_sha256"] == CHECKPOINT_SHA256
        started = time.monotonic()
        job = cli("reproduce", recipe["id"], "--wait", "--json", timeout=720)
        elapsed = round(time.monotonic() - started, 2)
        assert job["status"] == "completed", job["message"]
        assert job["runtime"]["device_type"] == args.expected_device
        assert job["runtime"]["comfy_revision"] == COMFY_REVISION
        assert job["model_binding"]["sha256"] == CHECKPOINT_SHA256
        with httpx.Client(base_url=base, timeout=30, trust_env=False) as client:
            response = client.get(job["output"]["url"])
            response.raise_for_status()
            png = response.content
        with Image.open(io.BytesIO(png)) as image:
            image.load()
            assert image.format == "PNG" and image.size == (1024, 1024)
        digest = hashlib.sha256(png).hexdigest()
        (args.output / "generated.png").write_bytes(png)
        (args.output / "job.json").write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")
        stop()
        restart = start(gpu=False)
        with httpx.Client(base_url=base, timeout=30, trust_env=False) as client:
            saved = request(client, f"/api/jobs/{job['id']}")
            response = client.get(saved["output"]["url"])
            response.raise_for_status()
            assert hashlib.sha256(response.content).hexdigest() == digest
        assert restart["engine"] == "demo_only" and saved["status"] == "completed"
        report = {"job_id": job["id"], "device_type": job["runtime"]["device_type"],
                  "torch_version": job["runtime"]["torch_version"], "comfy_revision": COMFY_REVISION,
                  "checkpoint_sha256": CHECKPOINT_SHA256, "output_sha256": digest,
                  "dimensions": [1024, 1024], "generation_seconds": elapsed,
                  "reopened_after_restart": True}
        (args.output / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
    finally:
        stop()
        log.close()


if __name__ == "__main__":
    main()
