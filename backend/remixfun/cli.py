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
    serve.add_argument("--comfy-root", type=Path, help="Manage the pinned local SDXL runtime in this directory")
    serve.add_argument("--model-dir", type=Path, help="Persistent model cache, separate from Comfy")
    serve.add_argument("--model-path", type=Path, action="append", default=[], help="Existing read-only model library to scan")
    models = sub.add_parser("models")
    model_commands = models.add_subparsers(dest="model_command", required=True)
    for name in ("resolve", "download"):
        command = model_commands.add_parser(name)
        command.add_argument("id")
        command.add_argument("--wait", action="store_true")
        command.add_argument("--json", action="store_true")
    model_commands.add_parser("scan").add_argument("--json", action="store_true")
    downloads = sub.add_parser("downloads")
    downloads.add_argument("action", nargs="?", choices=["pause", "resume", "cancel", "retry"])
    downloads.add_argument("id", nargs="?")
    downloads.add_argument("--json", action="store_true")
    recipe = sub.add_parser("create")
    recipe.add_argument("prompt")
    recipe.add_argument("--seed", default="42")
    recipe.add_argument("--model-sha256", help="Verified SDXL checkpoint for a new authored recipe")
    recipe.add_argument("--json", action="store_true")
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
            cmd.add_argument("--accept-assumptions", action="store_true", help="Accept the disclosed imported-attempt settings")
            cmd.add_argument("--seed-offset", type=int, default=0, choices=range(32), help="Explicit imported batch-base seed hypothesis (0–31)")
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
                    from .engine import Comfy
                    engine = Comfy(args.comfy_root, args.data_dir / "logs") if args.comfy_root else None
                    def stop():
                        server.should_exit = True
                    app = create_app(args.data_dir, args.web_dir or default_web, instance=args.instance, engine=engine,
                                     model_root=args.model_dir, model_paths=args.model_path,
                                     owner_token=os.environ.get("REMIXFUN_OWNER_TOKEN"), shutdown=stop)
                    server = uvicorn.Server(uvicorn.Config(app, host=args.host, port=args.port, access_log=False))
                    server.run()
            except Timeout as exc:
                raise RuntimeError("This library is already open in another Remixfun service. Attach to that service instead.") from exc
            return 0
        if args.command == "models":
            if args.model_command == "scan":
                result = request(args.service, "POST", "/api/models/scan")
            elif args.model_command == "resolve":
                result = request(args.service, "POST", f"/api/imports/{args.id}/dependencies/resolve")
                if args.wait:
                    while result["status"] in {"queued", "running"}:
                        time.sleep(1)
                        result = request(args.service, "GET", f"/api/operations/{result['id']}")
                    result = request(args.service, "GET", f"/api/imports/{args.id}/dependencies")
            else:
                plan = request(args.service, "GET", f"/api/imports/{args.id}/dependencies")
                result = request(args.service, "POST", f"/api/imports/{args.id}/downloads", json={"revision": plan["revision"]})
                if args.wait:
                    while True:
                        result = request(args.service, "GET", f"/api/imports/{args.id}/dependencies")
                        if not any(d["status"] in {"queued", "downloading", "retry_wait", "verifying"} for d in result["dependencies"]):
                            break
                        time.sleep(1)
                    if any(d["status"] != "available" for d in result["dependencies"]):
                        print(json.dumps(result, indent=2))
                        return 1
        elif args.command == "downloads":
            if args.action and not args.id:
                raise RuntimeError("Specify a download ID.")
            result = request(args.service, "POST", f"/api/downloads/{args.id}/{args.action}") if args.action else request(args.service, "GET", "/api/downloads")
        elif args.command == "create":
            result = request(args.service, "POST", "/api/recipes", json={"prompt": args.prompt, "seed": args.seed, "model_sha256": args.model_sha256})
        elif args.command == "import":
            if args.source.startswith("https://"):
                result = request(args.service, "POST", "/api/imports", json={"url": args.source})
            else:
                with Path(args.source).open("rb") as stream:
                    result = request(args.service, "POST", "/api/imports/file", files={"file": (Path(args.source).name, stream)})
        elif args.command == "reproduce":
            source = request(args.service, "GET", f"/api/imports/{args.id}")
            body = {}
            if source["source"]["kind"] in {"civitai", "file"}:
                plan = request(args.service, "GET", f"/api/imports/{args.id}/dependencies", params={"seed_offset": args.seed_offset})["reproduction"]
                if not args.accept_assumptions:
                    print(json.dumps(plan, ensure_ascii=True, indent=2))
                    raise RuntimeError("Review these settings; use --accept-assumptions to run an attempt.")
                body = {"revision": plan["revision"], "accept_assumptions": True, "seed_offset": args.seed_offset}
            elif args.seed_offset:
                raise RuntimeError("Seed-offset hypotheses apply only to imported recipes.")
            result = request(args.service, "POST", f"/api/imports/{args.id}/reproduce", json=body)
            if args.wait:
                deadline = time.monotonic() + 660
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
        return 1 if isinstance(result, dict) and result.get("status") in {"failed", "interrupted", "unknown"} else 0
    except (RuntimeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
