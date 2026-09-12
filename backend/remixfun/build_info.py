"""Frozen binaries report their own baked source identity, not a caller's claim."""
import json
import os
import sys
from pathlib import Path


def source_sha():
    if getattr(sys, "frozen", False):
        return json.loads((Path(sys._MEIPASS) / "build-info.json").read_text())["source_sha"]
    return os.environ.get("REMIXFUN_SOURCE_SHA", "development")
