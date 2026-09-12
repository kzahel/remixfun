"""Opt-in imported attempts through the shared HTTP service and a real Comfy GPU."""
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

from remixfun.reproduction import compare_reference

SHA = "e6bb9ea85bbf7bf6478a7c6d18b71246f22e95d41bcdd80ed40aa212c33cfeff"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comfy-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("artifacts/beetle-attempt"))
    parser.add_argument("--source-url", default="https://civitai.com/images/141984808")
    parser.add_argument("--expected-sha256", default=SHA)
    parser.add_argument("--download", action="store_true", help="Download the explicitly pinned model if missing")
    parser.add_argument("--seed-offsets", type=int, choices=range(1, 9), default=1, help="Test offsets 0 through N-1, then repeat zero")
    parser.add_argument("--model-path", type=Path, default=Path(user_data_path("Remixfun", appauthor=False)) / "models" / "blobs" / SHA)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if not args.model_path.is_dir():
        raise RuntimeError("Download the exact checkpoint first or supply its existing model folder.")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]
    token = secrets.token_urlsafe(32)
    with (args.output / "service.log").open("ab") as log, httpx.Client(base_url=f"http://127.0.0.1:{port}", timeout=45, trust_env=False) as client:
        process = subprocess.Popen([sys.executable, "-m", "remixfun.cli", "serve", "--port", str(port),
            "--data-dir", str(args.output / "library"), "--model-dir", str(args.output / "models"),
            "--model-path", str(args.model_path), "--comfy-root", str(args.comfy_root), "--instance", "beetle-verification"],
            env={**os.environ, "REMIXFUN_OWNER_TOKEN": token}, stdout=log, stderr=log,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        def request(method, path, **kwargs):
            response = client.request(method, path, **kwargs)
            if response.is_error: raise RuntimeError(f"{path}: {response.status_code} {response.text[:1500]}")
            return response.json()
        try:
            deadline = time.monotonic() + 180
            while time.monotonic() < deadline:
                if process.poll() is not None: raise RuntimeError("Service failed; inspect service.log")
                try:
                    request("GET", "/api/health"); break
                except httpx.HTTPError: time.sleep(.25)
            else: raise RuntimeError("Service startup timed out")
            source = request("POST", "/api/imports", json={"url": args.source_url})
            path = f"/api/imports/{source['id']}"
            print("Imported live recipe; resolving and verifying checkpoint bytes.", flush=True)
            deadline = time.monotonic() + 240
            while time.monotonic() < deadline:
                plan = request("GET", path + "/dependencies")
                if (plan.get("operation") or {}).get("status") not in {"queued", "running"}: break
                time.sleep(1)
            attempt = plan["reproduction"]
            assert attempt["checkpoint"]["sha256"] == args.expected_sha256
            if args.download and any(d["status"] != "available" for d in plan["dependencies"]):
                submitted = request("POST", path + "/downloads", json={"revision": plan["revision"]})
                for download in submitted["dependencies"].values():
                    if download.get("download_id") and download["status"] in {"failed", "canceled"}:
                        request("POST", f"/api/downloads/{download['download_id']}/retry")
                deadline = time.monotonic() + 1800
                last = 0
                while time.monotonic() < deadline:
                    plan = request("GET", path + "/dependencies")
                    if all(d["status"] == "available" for d in plan["dependencies"]): break
                    if not any(d["status"] in {"queued", "downloading", "retry_wait", "verifying"} for d in plan["dependencies"]):
                        raise RuntimeError(str(plan["generation_blockers"]))
                    if time.monotonic() - last > 10:
                        print([(d["status"], (d.get("download") or {}).get("downloaded_bytes")) for d in plan["dependencies"]], flush=True)
                        last = time.monotonic()
                    time.sleep(1)
                else: raise RuntimeError("Model download timed out")
            assert not plan["generation_blockers"], plan["generation_blockers"]
            attempt = plan["reproduction"]
            assert client.post(path + "/reproduce").status_code == 409
            reference = client.get(source["media"]["url"]).content
            (args.output / f"source.{source['image']['encoding']}").write_bytes(reference)
            jobs, outputs = [], []
            offsets = list(range(args.seed_offsets)) + [0]
            for index, offset in enumerate(offsets):
                selected_plan = request("GET", path + "/dependencies", params={"seed_offset": offset})["reproduction"]
                job = request("POST", path + "/reproduce", json={"revision": selected_plan["revision"], "accept_assumptions": True, "seed_offset": offset})
                deadline = time.monotonic() + 660
                while job["status"] in {"queued", "running"} and time.monotonic() < deadline:
                    time.sleep(1); job = request("GET", f"/api/jobs/{job['id']}")
                assert job["status"] == "completed", job["message"]
                output = client.get(job["output"]["url"]).content
                assert hashlib.sha256(output).hexdigest() == job["output"]["sha256"]
                (args.output / f"attempt-{index + 1}.png").write_bytes(output)
                jobs.append(job); outputs.append(output)
                print(f"Attempt {index + 1}, seed offset {offset}: {job['comparison']}; output {job['output']['sha256']}", flush=True)
            assert request("GET", path + "/manifest") == source
            repeat = compare_reference(outputs[0], outputs[-1], "controlled_same_recipe_repeat")
            assert repeat["status"] == "equal_reference_pixels", repeat
            report = {"source": source, "plan": attempt, "offsets": offsets, "jobs": jobs, "source_unchanged": True, "repeat_comparison": repeat}
            (args.output / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
            print("Source preserved; repeated attempt produced identical decoded pixels.", flush=True)
        finally:
            if process.poll() is None:
                response = client.post("/api/shutdown", headers={"X-Remixfun-Owner": token})
                response.raise_for_status()
                process.wait(timeout=45)


if __name__ == "__main__":
    main()
