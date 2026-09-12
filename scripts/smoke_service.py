"""Exercise the real service executable, CLI, restart and library lock."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--executable", type=Path)
    args = parser.parse_args()
    command = [str(args.executable.resolve())] if args.executable else [sys.executable, "-m", "remixfun.cli"]
    with tempfile.TemporaryDirectory(prefix="remixfun smoke with spaces ") as folder:
        root = Path(folder)
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        base = f"http://127.0.0.1:{port}"

        def call(path, method="GET"):
            req = urllib.request.Request(base + path, method=method)
            with urllib.request.urlopen(req, timeout=3) as response:
                return json.load(response)

        def start():
            process = subprocess.Popen([*command, "serve", "--port", str(port), "--data-dir", str(root / "library")],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                       creationflags=0x08000000 if os.name == "nt" else 0)
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise AssertionError("Service exited before becoming ready")
                try:
                    health = call("/api/health")
                    assert health["app"] == "remixfun" and health["version"] == "0.1.0"
                    return process
                except (urllib.error.URLError, TimeoutError):
                    time.sleep(0.1)
            process.terminate()
            process.wait(timeout=10)
            raise AssertionError("Service did not become ready")

        process = start()
        try:
            with urllib.request.urlopen(base, timeout=3) as response:
                assert b'<div id="root"></div>' in response.read()
            source = call("/api/demo", "POST")
            assert source["recipe"]["fields"]["seed"] == "18446744073709551614"
            result = subprocess.run([*command, "--service", base, "reproduce", source["id"], "--wait", "--json"],
                                    capture_output=True, text=True, timeout=30, check=True)
            job = json.loads(result.stdout)
            assert job["status"] == "completed" and job["comparison"] == "not_applicable"
            duplicate = subprocess.run([*command, "serve", "--port", "0", "--data-dir", str(root / "library")],
                                       capture_output=True, text=True, timeout=15)
            assert duplicate.returncode != 0 and "already open" in duplicate.stderr
        finally:
            process.terminate()
            process.wait(timeout=15)
        process = start()
        try:
            assert call(f"/api/imports/{source['id']}") == source
            assert call(f"/api/jobs/{job['id']}")["status"] == "completed"
        finally:
            process.terminate()
            process.wait(timeout=15)
    print("Service smoke passed: frontend, API/CLI, exact seed, result, library lock, restart.")


if __name__ == "__main__":
    main()
