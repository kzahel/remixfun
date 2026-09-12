"""The CLI is an HTTP client; serve is the single application host."""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import httpx
from platformdirs import user_data_path

from . import __version__


def request(base, method, path, **kwargs):
    try:
        with httpx.Client(base_url=base, timeout=35) as client:
            response = client.request(method, path, **kwargs)
        body = response.json()
        if response.is_error:
            raise RuntimeError(body.get("detail", "Service request failed"))
        return body
    except (httpx.HTTPError, ValueError) as exc:
        raise RuntimeError("Cannot reach Remixfun. Start it with 'remixfun serve'.") from exc


def main(argv=None):
    parser = argparse.ArgumentParser(prog="remixfun")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--service", default="http://127.0.0.1:8788")
    sub = parser.add_subparsers(dest="command", required=True)
    serve = sub.add_parser("serve")
    serve.add_argument("--host", choices=["127.0.0.1", "::1"], default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8788)
    serve.add_argument("--data-dir", type=Path, default=Path(os.environ.get("REMIXFUN_DATA_DIR", user_data_path("Remixfun", appauthor=False))))
    serve.add_argument("--web-dir", type=Path)
    serve.add_argument("--instance", default="headless")
    for name in ("health", "list", "demo", "jobs"):
        sub.add_parser(name).add_argument("--json", action="store_true")
    imp = sub.add_parser("import")
    imp.add_argument("source")
    imp.add_argument("--json", action="store_true")
    for name in ("show", "reproduce"):
        cmd = sub.add_parser(name)
        cmd.add_argument("id")
        cmd.add_argument("--json", action="store_true")
        if name == "reproduce":
            cmd.add_argument("--wait", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "serve":
            import uvicorn
            from filelock import FileLock, Timeout
            from .api import create_app
            default_web = Path(__file__).resolve().parents[2] / "web" / "dist"
            if getattr(sys, "frozen", False):
                default_web = Path(sys._MEIPASS) / "web"
            args.data_dir.mkdir(parents=True, exist_ok=True)
            try:
                with FileLock(args.data_dir / "service.lock", timeout=0):
                    app = create_app(args.data_dir, args.web_dir or default_web, instance=args.instance)
                    uvicorn.run(app, host=args.host, port=args.port, access_log=False)
            except Timeout as exc:
                raise RuntimeError("This library is already open in another Remixfun service. Attach to that service instead.") from exc
            return 0
        if args.command == "import":
            if args.source.startswith("https://"):
                result = request(args.service, "POST", "/api/imports", json={"url": args.source})
            else:
                with Path(args.source).open("rb") as stream:
                    result = request(args.service, "POST", "/api/imports/file", files={"file": (Path(args.source).name, stream)})
        elif args.command == "reproduce":
            result = request(args.service, "POST", f"/api/imports/{args.id}/reproduce")
            if args.wait:
                deadline = time.monotonic() + 120
                while result["status"] in {"queued", "running"}:
                    if time.monotonic() > deadline:
                        raise RuntimeError(f"Wait timed out; job {result['id']} remains saved.")
                    time.sleep(0.25)
                    result = request(args.service, "GET", f"/api/jobs/{result['id']}")
        else:
            method, path = {"health": ("GET", "/api/health"), "list": ("GET", "/api/imports"),
                            "demo": ("POST", "/api/demo"), "jobs": ("GET", "/api/jobs"),
                            "show": ("GET", f"/api/imports/{getattr(args, 'id', '')}")}[args.command]
            result = request(args.service, method, path)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 1 if isinstance(result, dict) and result.get("status") in {"failed", "interrupted"} else 0
    except (RuntimeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
