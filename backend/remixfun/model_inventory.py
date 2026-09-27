"""A locked model cache, persistent transfer records, and verified loader paths."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import time
import tempfile
from contextlib import contextmanager

from filelock import FileLock, Timeout

from .domain import Problem
from .model_resolution import ROLES


def fingerprint(path):
    stat = path.stat()
    return [stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns]


class Inventory:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = FileLock(self.root / "cache.lock")
        self.hardlinks = True
        self.db = self.root / "inventory.sqlite3"
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS schema_info (version INTEGER NOT NULL);
                INSERT INTO schema_info SELECT 1 WHERE NOT EXISTS (SELECT 1 FROM schema_info);
                CREATE TABLE IF NOT EXISTS blobs (sha256 TEXT PRIMARY KEY, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS downloads (id TEXT PRIMARY KEY, sha256 TEXT UNIQUE NOT NULL, body TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS plans (id TEXT PRIMARY KEY, body TEXT NOT NULL);
            """)
        (self.root / "partials").mkdir(exist_ok=True)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.db, timeout=15)
        db.execute("PRAGMA synchronous=FULL")
        try:
            with db:
                yield db
        finally:
            db.close()

    def start(self):
        try:
            self.lock.acquire(timeout=0)
        except Timeout as exc:
            raise Problem("This model cache is open in another service. Attach to it or choose another model directory.", 409) from exc
        fd, probe = tempfile.mkstemp(dir=self.root / "partials", suffix=".probe")
        os.close(fd)
        link = probe + ".link"
        try:
            os.link(probe, link)
        except OSError:
            self.hardlinks = False
        finally:
            Path(link).unlink(missing_ok=True)
            Path(probe).unlink(missing_ok=True)

    def close(self):
        self.lock.release()

    def put(self, table, key, body):
        assert table in {"blobs", "downloads", "plans"}
        column = "sha256" if table == "blobs" else "id"
        with self.connect() as db:
            if table == "downloads":
                db.execute("INSERT INTO downloads VALUES (?, ?, ?) ON CONFLICT(id) DO UPDATE SET body=excluded.body",
                           (key, body["file"]["sha256"], json.dumps(body)))
            else:
                db.execute(f"INSERT INTO {table} VALUES (?, ?) ON CONFLICT({column}) DO UPDATE SET body=excluded.body",
                           (key, json.dumps(body)))
        return body

    def get(self, table, key):
        assert table in {"blobs", "downloads", "plans"}
        column = "sha256" if table == "blobs" else "id"
        with self.connect() as db:
            row = db.execute(f"SELECT body FROM {table} WHERE {column}=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def list(self, table):
        assert table in {"blobs", "downloads", "plans"}
        with self.connect() as db:
            rows = db.execute(f"SELECT body FROM {table} ORDER BY rowid DESC").fetchall()
        return [json.loads(row[0]) for row in rows]

    def partial(self, job):
        return self.root / "partials" / (job["id"] + ".partial")

    def target(self, digest):
        return self.root / "blobs" / digest / "model.safetensors"

    def available(self, digest):
        blob = self.get("blobs", digest)
        if blob:
            try:
                if fingerprint(Path(blob["path"])) == blob["fingerprint"]:
                    return blob
            except OSError:
                pass
        return None

    def verify(self, path, expected):
        before = fingerprint(path)
        with path.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != expected or before != fingerprint(path):
            raise Problem("Model SHA-256 verification failed. The file is not available for generation.", 409)
        return before

    def publish(self, partial, file):
        digest = file["sha256"]
        self.verify(partial, digest)
        target = self.target(digest)
        target.parent.mkdir(parents=True, exist_ok=True)
        if partial != target:
            # All staging and managed targets are under the same cache root/volume.
            os.replace(partial, target)
        body = {"sha256": digest, "path": str(target), "fingerprint": fingerprint(target),
                "size": target.stat().st_size, "verified_at": time.time(), "file": file}
        self.put("blobs", digest, body)
        self.bind(file)
        return self.get("blobs", digest)

    def bind(self, file):
        blob = self.available(file["sha256"])
        if not blob:
            raise Problem("The selected model is missing or changed. Verify or download it again.", 409)
        target = self.root / "comfy" / ROLES[file["role"]] / (file["sha256"] + ".safetensors")
        target.parent.mkdir(parents=True, exist_ok=True)
        source = Path(blob["path"])
        if target.exists():
            if not os.path.samefile(target, source):
                try:
                    self.verify(target, file["sha256"])
                except Problem:
                    # This hash-named alias is owned by the cache; external originals
                    # are never modified when repairing a damaged loader alias.
                    target.unlink()
        if not target.exists():
            try:
                os.link(source, target)
            except OSError:
                if shutil.disk_usage(target.parent).free < blob["size"] + 256 * 1024**2:
                    raise Problem("Insufficient space to publish a model copy on this filesystem.", 409)
                temporary = target.with_suffix(".copying")
                shutil.copyfile(source, temporary)
                self.verify(temporary, file["sha256"])
                os.replace(temporary, target)
            else:
                # Creating a hardlink changes the source inode's ctime on POSIX.
                # Recheck its bytes before saving the new fingerprint so the
                # freshly verified blob remains available across restarts.
                try:
                    current = self.verify(source, file["sha256"])
                except Problem:
                    target.unlink()
                    raise
                if current != blob["fingerprint"]:
                    blob["fingerprint"] = current
                    self.put("blobs", file["sha256"], blob)
        return {"sha256": file["sha256"], "filename": target.name, "path": str(target), "file": file}

    def scan(self, paths, expected_files):
        """Index only explicitly configured folders; originals are never mutated."""
        found = []
        for root in paths:
            root = Path(root).resolve()
            if not root.is_dir():
                continue
            for path in root.rglob("*.safetensors"):
                if path.is_symlink() or not path.resolve().is_relative_to(root):
                    continue
                try:
                    before = fingerprint(path)
                    # Provider sizes are estimates; hash all discovered files, never
                    # reject matching bytes just because a size estimate was rounded.
                    with path.open("rb") as stream:
                        digest = hashlib.file_digest(stream, "sha256").hexdigest()
                    matches = [f for f in expected_files if f["sha256"] == digest]
                    if not matches or before != fingerprint(path):
                        continue
                    body = {"sha256": digest, "path": str(path.resolve()), "fingerprint": before,
                            "size": before[0], "verified_at": time.time(), "file": matches[0], "external": True}
                    if not self.available(digest):
                        self.put("blobs", digest, body)
                    found.append(digest)
                except OSError:
                    continue
        return found
