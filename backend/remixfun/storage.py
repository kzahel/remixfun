"""SQLite records and atomic, content-addressed artifacts outside the app bundle."""

import hashlib
import json
import os
import sqlite3
import tempfile
from contextlib import contextmanager
from pathlib import Path

from .domain import Problem


class Store:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        (root / "media").mkdir(exist_ok=True)
        self.db = root / "library.sqlite3"
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, kind TEXT NOT NULL, body TEXT NOT NULL)")

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.db, timeout=15)
        try:
            with db:
                yield db
        finally:
            db.close()

    def put(self, record, kind="import"):
        with self.connect() as db:
            db.execute("INSERT INTO records VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET body=excluded.body",
                       (record["id"], kind, json.dumps(record, ensure_ascii=False)))
        return record

    def get(self, identifier, kind="import"):
        with self.connect() as db:
            row = db.execute("SELECT body FROM records WHERE id=? AND kind=?", (identifier, kind)).fetchone()
        if not row:
            raise Problem("That saved item was not found.", 404)
        return json.loads(row[0])

    def list(self, kind="import"):
        with self.connect() as db:
            rows = db.execute("SELECT body FROM records WHERE kind=? ORDER BY rowid DESC", (kind,)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def artifact(self, content: bytes, extension: str):
        digest = hashlib.sha256(content).hexdigest()
        name = f"{digest}.{extension}"
        target = self.root / "media" / name
        if not target.exists():
            fd, temporary = tempfile.mkstemp(dir=target.parent, suffix=".partial")
            try:
                with os.fdopen(fd, "wb") as stream:
                    stream.write(content)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, target)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        return {"name": name, "sha256": digest, "bytes": len(content), "url": f"/api/media/{name}"}
