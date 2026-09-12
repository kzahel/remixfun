"""Civitai file transport; signed locations are ephemeral and host-scoped."""
from contextlib import contextmanager
import re
from urllib.parse import urljoin, urlsplit

import httpx

from .domain import Problem
from .provider import USER_AGENT, MAX_JSON

STORAGE_HOSTS = {
    "civitai-delivery-worker-prod.5ac0637cfd0766c97916cefa3764fbdf.r2.cloudflarestorage.com",
}


class TransferError(Exception):
    def __init__(self, code, message, *, retry=False, restart=False, delay=0):
        self.code, self.message = code, message
        self.retry, self.restart, self.delay = retry, restart, delay
        super().__init__(message)


class Credentials:
    """Keys never pass through import records, download jobs, or log messages."""
    def backend(self):
        import keyring
        backend = keyring.get_keyring()
        allowed = {"keyring.backends.Windows", "keyring.backends.macOS", "keyring.backends.SecretService", "keyring.backends.kwallet"}
        candidates = getattr(backend, "backends", [backend])
        for candidate in candidates:
            if type(candidate).__module__ in allowed:
                return candidate
        raise RuntimeError("No operating-system credential backend")

    def get(self):
        try:
            return self.backend().get_password("Remixfun", "civitai")
        except Exception:
            return None

    def set(self, value):
        try:
            backend = self.backend()
            if value:
                backend.set_password("Remixfun", "civitai", value)
            elif self.get():
                backend.delete_password("Remixfun", "civitai")
        except Exception as exc:
            raise Problem("The operating-system credential store is unavailable. No key was saved.", 409) from exc


def checked_url(url):
    try:
        parsed = urlsplit(url)
        if (parsed.scheme != "https" or parsed.hostname not in {"civitai.com", *STORAGE_HOSTS}
                or parsed.port not in {None, 443} or parsed.username or parsed.password or parsed.fragment):
            raise ValueError()
        if parsed.hostname == "civitai.com" and not re.fullmatch(r"/api/download/models/[1-9][0-9]*", parsed.path):
            raise ValueError()
        return parsed.hostname
    except ValueError as exc:
        raise TransferError("redirect_denied", "The provider returned an unsupported model storage address.") from exc


def check_status(response):
    code = response.status_code
    if code in {200, 206, 416}:
        return
    if code == 401:
        raise TransferError("authentication_required", "Civitai requires authentication. Add your Civitai key in Settings and retry.")
    if code == 403:
        raise TransferError("access_denied", "Civitai denied access to this file. Check provider access requirements, then retry.")
    if code == 404:
        raise TransferError("file_unavailable", "This exact model file is no longer available from Civitai.")
    if code in {429, 500, 502, 503, 504}:
        delay = response.headers.get("retry-after", "0")
        raise TransferError("provider_busy", "The provider is busy. The download will retry.", retry=True,
                            delay=min(int(delay), 60) if delay.isdigit() else 0)
    raise TransferError("provider_error", f"The model provider returned HTTP {code}.")


class ModelTransport:
    def __init__(self, transport=None, credentials=None):
        self.transport = transport
        self.credentials = credentials or Credentials()

    def client(self):
        return httpx.Client(transport=self.transport, timeout=httpx.Timeout(20, read=10), follow_redirects=False,
                            headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})

    def headers(self, host):
        key = self.credentials.get() if host == "civitai.com" else None
        return {"Authorization": f"Bearer {key}"} if key else {}

    def resolve(self, file):
        with self.client() as client:
            url = f"https://civitai.com/api/v1/model-versions/{file['version_id']}"
            with client.stream("GET", url, headers=self.headers("civitai.com")) as response:
                check_status(response)
                if response.status_code != 200:
                    raise TransferError("metadata_error", "Model version metadata was not returned.")
                body = bytearray()
                for chunk in response.iter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_JSON:
                        raise TransferError("metadata_error", "Model version metadata exceeds the size limit.")
            import json
            try:
                version = json.loads(body)
                candidates = [f for f in version["files"] if str(f.get("id")) == file["file_id"]]
                if (str(version["id"]) != file["version_id"] or len(candidates) != 1
                        or (file.get("model_id") is not None and str(version.get("modelId")) != str(file["model_id"]))
                        or candidates[0]["hashes"]["SHA256"].lower() != file["sha256"]):
                    raise ValueError()
                location = candidates[0]["downloadUrl"]
                # Force the exact file even if the provider URL names only a version.
                parsed = urlsplit(location)
                if parsed.hostname != "civitai.com" or parsed.path != f"/api/download/models/{file['version_id']}":
                    raise ValueError()
                return f"https://civitai.com{parsed.path}?fileId={file['file_id']}"
            except (ValueError, KeyError, TypeError, AttributeError) as exc:
                raise TransferError("identity_changed", "Provider file identity changed or is ambiguous. Refresh the dependency plan; no model was substituted.") from exc

    @contextmanager
    def stream(self, file, offset=0, etag=None):
        url = self.resolve(file)
        with self.client() as client:
            refreshed = False
            for _ in range(5):
                host = checked_url(url)
                headers = self.headers(host)
                if offset and etag:
                    headers.update({"Range": f"bytes={offset}-", "If-Range": etag})
                with client.stream("GET", url, headers=headers) as response:
                    if response.is_redirect:
                        url = urljoin(str(response.url), response.headers.get("location", ""))
                        continue
                    if response.status_code in {401, 403} and host in STORAGE_HOSTS and not refreshed:
                        # Expired signed locations are refreshed once for the same
                        # selected identity, never logged or retained in job state.
                        url = self.resolve(file)
                        refreshed = True
                        continue
                    check_status(response)
                    yield response
                    return
            raise TransferError("redirect_denied", "The model download exceeded its redirect limit.")
