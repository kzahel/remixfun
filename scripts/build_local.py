"""Portable unsigned Windows build for developer verification; never publishes."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    if sys.platform != "win32":
        raise SystemExit("The packaged desktop preview is currently Windows-only. Use 'uv run remixfun serve' on other platforms.")
    env = os.environ.copy()
    # Explicit release identity wiring remains part of the signed-delivery handoff.
    env.setdefault("REMIXFUN_SOURCE_SHA", "development")
    npm = shutil.which("npm")
    subprocess.run([npm, "--prefix", "web", "run", "build"], cwd=ROOT, env=env, check=True)
    subprocess.run([sys.executable, "scripts/package_service.py"], cwd=ROOT, env=env, check=True)
    subprocess.run(["cargo", "build", "--release", "--locked", "--manifest-path", "desktop/Cargo.toml"], cwd=ROOT, env=env, check=True)
    output = ROOT / "dist/desktop-preview"
    output.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "dist/remixfun-service", output, dirs_exist_ok=True)
    shutil.copy2(ROOT / "desktop/target/release/remixfun-desktop.exe", output / "Remixfun.exe")
    print(f"Unsigned local preview: {output / 'Remixfun.exe'}")
    print("Keep the entire folder together. No installer, signing, updater, or publication was performed.")


if __name__ == "__main__":
    main()
