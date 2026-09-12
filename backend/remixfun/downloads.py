"""Durable, independent download workers. Never submit generation jobs."""
import asyncio
import copy
import os
import re
import shutil
import threading
import time
import uuid

import httpx

from .domain import Problem
from .model_transport import ModelTransport, TransferError

ACTIVE = {"queued", "downloading", "verifying", "retry_wait"}
MAX_FILE = 100 * 1024**3
SPACE_FLOOR = 256 * 1024**2


class Downloads:
    def __init__(self, inventory, transport=None):
        self.inventory = inventory
        self.transport = transport or ModelTransport()
        self.tasks = {}
        self.stops = {}
        self.slots = asyncio.Semaphore(2)
        self.hash_slot = threading.Lock()
        self.closing = False
        self.started = False
        self.mutex = threading.RLock()

    async def start(self):
        self.inventory.start()
        self.started = True
        for job in self.list():
            if job["status"] in ACTIVE:
                job.update(status="queued", message="Recovering saved download")
                self.save(job)
                self.launch(job["id"])

    def list(self):
        return self.inventory.list("downloads")

    def get(self, identifier):
        job = self.inventory.get("downloads", identifier)
        if not job:
            raise Problem("Download not found.", 404)
        return job

    def save(self, job):
        with self.mutex:
            current = self.inventory.get("downloads", job["id"])
            if current:
                job["consumers"] = list(dict.fromkeys([*current["consumers"], *job["consumers"]]))
            job["updated_at"] = time.time()
            return self.inventory.put("downloads", job["id"], job)

    def enqueue(self, file, consumer):
        if self.closing:
            raise Problem("The service is shutting down. Reopen it to start a download.", 409)
        if self.inventory.available(file["sha256"]):
            return {"status": "available", "download_id": None}
        for job in self.list():
            if job["file"]["sha256"] == file["sha256"]:
                if consumer not in job["consumers"]:
                    job["consumers"].append(consumer)
                    self.save(job)
                if job["status"] == "ready":
                    resumed = self.action(job["id"], "retry")
                    return {"status": resumed["status"], "download_id": job["id"]}
                return {"status": job["status"], "download_id": job["id"]}
        job = {"id": str(uuid.uuid4()), "file": copy.deepcopy(file), "status": "queued", "consumers": [consumer],
               "downloaded_bytes": 0, "total_bytes": None, "etag": None, "attempts": 0,
               "error_code": None, "message": "Queued", "created_at": time.time(), "bytes_per_second": 0}
        try:
            self.reserve(file.get("size_estimate") or MAX_FILE)
        except TransferError as exc:
            raise Problem(exc.message, 409) from exc
        self.save(job)
        self.launch(job["id"])
        return {"status": "queued", "download_id": job["id"]}

    def reserve(self, remaining, excluding=None):
        jobs = self.list()
        reserved = sum(max(0, (j["total_bytes"] or j["file"].get("size_estimate") or MAX_FILE) - j["downloaded_bytes"])
                       for j in jobs if j["status"] in ACTIVE and j["id"] != excluding)
        if not self.inventory.hardlinks:
            reserved += sum(j["total_bytes"] or j["file"].get("size_estimate") or MAX_FILE for j in jobs if j["status"] in ACTIVE)
            if excluding is None:
                reserved += remaining
        if remaining + reserved + SPACE_FLOOR > shutil.disk_usage(self.inventory.root).free:
            raise TransferError("disk_full", "There is not enough free space in the model folder. Free space and retry.")

    def launch(self, identifier):
        if identifier in self.tasks or self.closing:
            return
        self.stops[identifier] = threading.Event()
        task = asyncio.create_task(self.run(identifier))
        self.tasks[identifier] = task
        def completed(done):
            if self.tasks.get(identifier) is done:
                self.tasks.pop(identifier, None)
        task.add_done_callback(completed)

    async def run(self, identifier):
        async with self.slots:
            if not self.stops[identifier].is_set():
                await asyncio.to_thread(self.worker, identifier, self.stops[identifier])

    async def control(self, identifier, action):
        if action in {"pause", "cancel"}:
            job = self.get(identifier)
            if job["status"] in {"ready", "canceled"}:
                return job
            stop = self.stops.get(identifier)
            if stop:
                stop.set()
            task = self.tasks.get(identifier)
            if task:
                await task
            job = self.get(identifier)
            if job["status"] == "ready":
                return job
            job.update(status="paused" if action == "pause" else "canceled", message="Paused" if action == "pause" else "Canceled")
            if action == "cancel":
                self.inventory.partial(job).unlink(missing_ok=True)
                job.update(downloaded_bytes=0, etag=None)
            return self.save(job)
        return self.action(identifier, action)

    def action(self, identifier, action):
        if action not in {"resume", "retry"}:
            raise Problem("Unknown download action.")
        if self.closing:
            raise Problem("The service is shutting down.", 409)
        job = self.get(identifier)
        if job["status"] in ACTIVE or (job["status"] == "ready" and self.inventory.available(job["file"]["sha256"])):
            return job
        if identifier in self.tasks and not self.tasks[identifier].done():
            raise Problem("The previous download worker is still stopping. Retry shortly.", 409)
        self.tasks.pop(identifier, None)
        job.update(status="queued", error_code=None, message="Queued", attempts=0)
        self.save(job)
        self.launch(identifier)
        return job

    def worker(self, identifier, stop):
        job = self.get(identifier)
        for attempt in range(3):
            if stop.is_set():
                return
            job.update(attempts=attempt + 1, error_code=None)
            try:
                self.transfer(job, stop)
                return
            except TransferError as exc:
                code, message, retry, delay = exc.code, exc.message, exc.retry, exc.delay
                if exc.restart:
                    self.inventory.partial(job).unlink(missing_ok=True)
                    job.update(downloaded_bytes=0, etag=None, total_bytes=None)
            except httpx.HTTPError:
                code, message, retry, delay = "network_error", "The model download lost its connection. Retry will preserve a resumable partial.", True, 0
            except OSError:
                code, message, retry, delay = "storage_error", "The model folder could not be written. Check storage access and free space, then retry.", False, 0
            except Problem as exc:
                code, message, retry, delay = "hash_mismatch", exc.message, False, 0
                self.inventory.partial(job).unlink(missing_ok=True)
                job.update(downloaded_bytes=0, etag=None)
            except Exception:
                code, message, retry, delay = "download_error", "The download could not finish. Its file identity is preserved; retry or refresh the plan.", False, 0
            if stop.is_set():
                return
            job.update(error_code=code, message=message, status="retry_wait" if retry and attempt < 2 else "failed")
            self.save(job)
            if not retry or attempt == 2 or stop.wait(max(delay, 2**attempt)):
                return

    def transfer(self, job, stop):
        file = job["file"]
        target = self.inventory.target(file["sha256"])
        # Recover a crash after atomic promotion but before recording success.
        if target.exists():
            try:
                with self.hash_slot:
                    self.inventory.publish(target, file)
                job.update(status="ready", message="Model verified and available", downloaded_bytes=target.stat().st_size, total_bytes=target.stat().st_size)
                self.save(job)
                return
            except Problem:
                # Keep corrupt managed bytes for inspection while allowing a clean
                # retry; never remove or overwrite an external model library file.
                os.replace(target, target.with_suffix(".invalid"))
        partial = self.inventory.partial(job)
        offset = partial.stat().st_size if partial.exists() else 0
        etag = job.get("etag")
        if not etag or etag.startswith("W/"):
            offset = 0
        job.update(status="downloading", message="Downloading model", downloaded_bytes=offset)
        self.save(job)
        self.reserve(max(0, (job["total_bytes"] or file.get("size_estimate") or MAX_FILE) - offset), job["id"])
        with self.transport.stream(file, offset, etag) as response:
            if response.headers.get("content-encoding", "identity") != "identity":
                raise TransferError("encoding_error", "The download returned encoded bytes that cannot be safely resumed.")
            actual_etag = response.headers.get("etag")
            total = None
            if response.status_code == 416:
                match = re.fullmatch(r"bytes \*/([0-9]+)", response.headers.get("content-range", ""))
                if not match or not offset or offset != int(match[1]):
                    raise TransferError("range_changed", "The stored partial no longer agrees with the provider. Restarting.", retry=True, restart=True)
                total = offset
            elif response.status_code == 206:
                match = re.fullmatch(r"bytes ([0-9]+)-([0-9]+)/([0-9]+)", response.headers.get("content-range", ""))
                if (not match or int(match[1]) != offset or int(match[2]) + 1 != int(match[3])
                        or (offset and actual_etag != etag)):
                    raise TransferError("range_changed", "The provider returned an incompatible download range. Restarting.", retry=True, restart=True)
                total = int(match[3])
            elif response.status_code == 200:
                offset = 0  # A server ignoring Range must never be appended.
                length = response.headers.get("content-length")
                total = int(length) if length and length.isdigit() else None
            else:
                raise TransferError("response_error", "Unexpected model transfer response.")
            if total is not None and (total <= 0 or total > MAX_FILE):
                raise TransferError("size_limit", "The model file exceeds the supported transfer size.")
            self.reserve(max(0, (total or file.get("size_estimate") or MAX_FILE) - offset), job["id"])
            job.update(total_bytes=total, etag=actual_etag if actual_etag and not actual_etag.startswith("W/") else None,
                       downloaded_bytes=offset, resumed_from=offset, response_status=response.status_code)
            self.save(job)
            if response.status_code != 416:
                started, last, initial = time.monotonic(), time.monotonic(), offset
                with partial.open("ab" if offset else "wb") as stream:
                    try:
                        for chunk in response.iter_bytes(1024 * 1024):
                            if stop.is_set():
                                return
                            if job["downloaded_bytes"] + len(chunk) > (total or MAX_FILE):
                                raise TransferError("size_limit", "The downloaded file exceeds its declared size.", restart=True)
                            stream.write(chunk)
                            job["downloaded_bytes"] += len(chunk)
                            if time.monotonic() - last >= 0.5:
                                stream.flush()
                                os.fsync(stream.fileno())
                                job["bytes_per_second"] = (job["downloaded_bytes"] - initial) / max(.1, time.monotonic() - started)
                                self.save(job)
                                last = time.monotonic()
                    finally:
                        stream.flush()
                        os.fsync(stream.fileno())
                        self.save(job)
            if total is not None and partial.stat().st_size != total:
                raise TransferError("incomplete", "The model response ended early. Retrying.", retry=True)
        if stop.is_set():
            return
        job.update(status="verifying", message="Verifying model SHA-256", bytes_per_second=0)
        self.save(job)
        with self.hash_slot:
            if stop.is_set():
                return
            self.inventory.publish(partial, file)
        job.update(status="ready", message="Model verified and available", total_bytes=self.inventory.available(file["sha256"])["size"])
        self.save(job)

    async def close(self):
        if not self.started:
            return
        self.closing = True
        for stop in self.stops.values():
            stop.set()
        if self.tasks:
            await asyncio.gather(*list(self.tasks.values()))
        for job in self.list():
            if job["status"] in ACTIVE:
                job.update(status="queued", message="Saved for resume when the service starts")
                self.save(job)
        self.inventory.close()
        self.started = False
