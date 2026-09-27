# Model acquisition and inventory

Status: import-driven Civitai SafeTensor acquisition implemented, 2026-09-12.
Live checkpoint download, resume/restart/reuse and a new authored GPU image are
verified on Windows. See [evidence](../evidence/model-downloads.md).

## Resolution and user flow

The shared service saves the source first and resolves model metadata in a
background operation. A dependency plan is separate from immutable import JSON.
`GET /api/imports/{id}/dependencies` reports current file selection, availability,
progress and generation blockers. Refresh never changes an active transfer's
target or rewrites source settings.

Model, version, file, expected SHA-256 and actual local SHA-256 remain distinct.
Source file IDs and hashes constrain selection. One compatible SafeTensor file
with a full expected hash is selected automatically with recorded selection
reason. Multiple variants require a file choice. Conflicts, missing identities
and unsupported formats remain blocked. There is no latest-version or primary
file substitution. Checkpoint, LoRA and VAE acquisition roles exist; only SDXL
1.0 checkpoints currently have an authored generation handoff. Live LoRA/VAE
generation is unverified.

A hash-only A1111 `model`/checkpoint reference can be linked to a versioned
checkpoint when its reported hash matches that version's file hashes and only
one referenced version matches. Both source entries remain preserved; the plan
records linked evidence and constrains selection with every reported hash.
Names alone never merge dependencies; conflicts and ambiguity remain blocked.

**Download missing models** displays known sizes and per-file progress. Pause,
resume, retry and discard-partial controls operate on durable shared transfers.
The UI identifies transfers requested by several imports: controls affect all
consumers. Per-import detachment is not exposed. Completed downloads update
availability; missing source settings and unsupported profiles remain visible.

## Storage and verification

The cache defaults to `models` under app data. Settings, `--model-dir`, and
repeatable `--model-path` configure managed and existing folders. Cache-directory
changes take effect on restart; files/partials are not moved. Existing libraries
are scanned read-only and reused by hash regardless of filename. Fingerprint
changes invalidate availability and require rehashing.

One service owns a writable cache through a cache-root lock. Cache SQLite has
schema identity and separate blob, plan and download tables. Transfers are unique
by expected SHA-256 and retain provider-file identity, consumers, byte count,
ETag, attempts and sanitized errors. Generation jobs retain a separate lifecycle.

Partials remain outside Comfy paths. Full SHA-256 verification precedes atomic
same-volume promotion to `blobs/<sha256>/model.safetensors`. Typed hash-named
Comfy aliases use hardlinks or verified copies. Copy fallback and other queued
transfers count toward free-space reservations, with a 256 MiB floor. Unknown
sizes reserve a conservative maximum; a transfer cannot exceed 100 GiB. Managed
damaged aliases can be repaired; external originals are never deleted.
After creating a hardlink, the service rechecks the source hash and refreshes
its file fingerprint because link creation can change inode metadata on POSIX.
Later content changes still invalidate availability.

Two transfer workers and one verifier run off the API event loop. Progress is
periodically flushed/fsynced and persisted, including at stream exit. Resume
uses identity encoding, Range/If-Range and a strong ETag. A 206 must match the
requested offset/total/validator; a 200 restarts from zero. A 416 requires length
reconciliation and full hashing. Missing or changed validators cannot authorize
appending bytes. Hash failures never publish a file.

Transient network/provider errors retry with bounded backoff and numeric
Retry-After. Identity, access, storage and hash failures require explicit retry
or correction. Startup recovers active jobs and files, including a crash between
rename and DB commit. Explicitly paused/canceled jobs stay stopped; formerly
active transfers resume. Ready records with missing/changed files lose availability.

## Provider and credentials

Model transfers have a separate transport from previews because legitimate
signed storage URLs have query parameters. Version/exact-file requests use
Civitai HTTPS; storage redirects allow the specifically observed Civitai R2
account and `b2.civitai.com`, observed for model version 1317649. Infrastructure
changes require a reviewed allowlist update. Enqueue
accepts plan/file choices, not arbitrary URLs or destination paths. Signed
locations are ephemeral, never saved or logged, and can be refreshed once while
preserving selected identity.

Optional Civitai keys use supported OS credential backends, with no plaintext
fallback. Keys are sent only to Civitai, never storage hosts or returned by
Settings. Generic 403 means access denied, not necessarily a missing key.
Anonymous live downloading is verified; gated-file authentication is unverified.

## Desktop, CLI and engine

Desktop progress restores from service state after reload. A private random
owner token authorizes shutdown. The service rejects shutdown during active or
uncertain generation, closes write admission, then checkpoints downloads.
Desktop waits up to 30 seconds before fallback termination. Independent services
are unaffected by window close. Signed updater integration remains planned.

CLI commands: `models resolve <import> --wait`, `models download <import> --wait`,
`models scan`, `downloads`, and `downloads pause/resume/retry/cancel <job>`.
All use the shared HTTP service.

Comfy startup validates the runtime without requiring the preset checkpoint.
Generated extra-path configuration exposes cache aliases. Each generation
verifies its model binding and rejects ambiguous loader names. The authored
SDXL preset retains its Base checkpoint pin; `model_sha256` explicitly selects
another verified SDXL 1.0 checkpoint for a new recipe. Graph, generation profile,
model binding and output are saved. The separate [imported attempt profile](reproduction.md)
can execute supported normalized settings with recorded assumptions; the downloader
never fills source gaps or executes imported graphs.

The [implementation plan](../tactical/model-downloads.md) retains broader intent.
Cache migration, per-import detachment, automatic downloads, arbitrary formats
and exact source-compatible reproduction profiles remain follow-on work.
