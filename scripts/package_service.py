"""Build the locked Python service and frontend into a Tauri sidecar."""
import os
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not (ROOT / "web/dist/index.html").is_file():
        raise SystemExit("Build the frontend first: npm --prefix web run build")
    host = next(line.split(": ", 1)[1] for line in subprocess.check_output(["rustc", "-vV"], text=True).splitlines() if line.startswith("host:"))
    build_info = ROOT / "build/build-info.json"
    build_info.parent.mkdir(exist_ok=True)
    build_info.write_text(json.dumps({"source_sha": os.environ.get("REMIXFUN_SOURCE_SHA", "development")}), encoding="utf-8")
    subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir", "--name", "remixfun-service",
                    "--specpath", str(ROOT / "build"),
                    "--add-data", f"{build_info}{os.pathsep}.",
                    "--collect-all", "remixfun", "--collect-all", "uvicorn", "--add-data", f"{ROOT / 'web/dist'}{os.pathsep}web",
                    str(ROOT / "scripts/service_entry.py")], cwd=ROOT, check=True)
    extension = ".exe" if sys.platform == "win32" else ""
    folder = ROOT / "desktop/binaries"
    folder.mkdir(exist_ok=True)
    shutil.copy2(ROOT / f"dist/remixfun-service/remixfun-service{extension}", folder / f"remixfun-service-{host}{extension}")
    print("Service built. Its _internal directory must accompany the executable.")


if __name__ == "__main__":
    main()
