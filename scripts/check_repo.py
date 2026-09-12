"""Portable, dependency-free checks; never execute reference applications."""

import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def main():
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, capture_output=True, check=True,
    )
    paths = sorted(set(result.stdout.decode("utf-8").split("\0")) - {""})
    errors = []
    external_links = 0
    for name in paths:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"Missing file: {name}")
            continue
        if path.suffix not in {".md", ".py", ".json", ".yml"}:
            continue
        content = path.read_text(encoding="utf-8")
        if "\ufffd" in content:
            errors.append(f"Invalid text encoding: {name}")
        if path.suffix == ".py":
            ast.parse(content, filename=name)
        if path.suffix == ".json":
            json.loads(content)
        if path.suffix != ".md":
            continue
        for raw in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", content):
            target = raw.strip("<>").split("#", 1)[0]
            if not target or target.startswith(("https://", "http://", "mailto:")):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            if not resolved.is_relative_to(ROOT):
                if resolved.is_relative_to(ROOT.parent / "references"):
                    external_links += 1
                    continue
                errors.append(f"Unexpected external local link: {name}: {target}")
            elif not resolved.exists():
                errors.append(f"Missing link: {name}: {target}")
        definitions = set(re.findall(r"^\[\^([^\]]+)\]:", content, re.M))
        uses = set(re.findall(r"\[\^([^\]]+)\](?!:)", content))
        if uses - definitions:
            errors.append(f"Undefined footnotes: {name}: {uses - definitions}")

    config = json.loads((ROOT / "update-server/remixfun.json").read_text())
    expected = {
        "stable": {"displayName": "Stable", "tagPrefix": "desktop-v", "releaseKind": "release"},
        "nightly": {"displayName": "Nightly", "tagPrefix": "desktop-nightly-v", "releaseKind": "prerelease"},
    }
    if config["channels"] != expected:
        errors.append("Release channels differ from the Stable/Nightly contract")
    if (config["id"], config["githubRepo"], config["pathPrefix"], config["tagPrefix"]) != (
        "remixfun", "kzahel/remixfun", "/remixfun", "desktop-v"
    ):
        errors.append("Update product identity differs from Remixfun")
    print(f"Checked {len(paths)} repository files; {external_links} optional reference links.")
    for error in errors:
        print(error, file=sys.stderr)
    print("Repository checks failed." if errors else "Repository checks passed.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
