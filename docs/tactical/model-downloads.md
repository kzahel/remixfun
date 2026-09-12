# Model acquisition from an imported recipe

Status: initial acquisition slice implemented and live verified, 2026-09-12.
The design below records the proposal; the [owning contract](../topics/models.md)
and [evidence](../evidence/model-downloads.md) define what now exists. Per-import
detachment, cache migration/cleanup, additional storage hosts and imported
generation profiles remain follow-on work. Scope: the model-acquisition portion of the
[remixer plan](build-remixer.md), following the existing
[product](../topics/product.md) and [service](../topics/architecture.md) boundaries.

## Recommendation

Follow Dreamtime's import → resource availability → Download Missing → durable
job → available model flow. Adapt it into Remixfun's existing Python service,
with file-level identities, verified completion and resumable transfers.
Keep the current importer; its model-version evidence becomes resolver input.
There is no need to bring over Dreamtime's workspace/user ORM or its entire
worker. Downloads must work without Comfy running and without an open window.

At proposal time Remixfun had a one-off, hash-checked SDXL Base bootstrap fetch in
[`scripts/fetch_sdxl.py`](../../scripts/fetch_sdxl.py), plus Civitai version/file
metadata enrichment. It has no application download queue, inventory lookup,
resume protocol or download action. Downloading a different checkpoint also
requires replacing the engine's fixed checkpoint binding before it can run.

## What Dreamtime actually implements

Source-only review of clean local commit
`1129dfcca23afb59c59de48d97d92abbd31cd439`. The reference application and its
tests were not executed. These findings concern that inspected snapshot.

| Area | Observed Dreamtime behavior | Adaptation |
| --- | --- | --- |
| Import UI | Per-resource controls and Download Missing; polls progress every two seconds and refreshes the import after completion | Keep the interaction, restore active jobs from the service after reload |
| Availability | Dynamically joins workspace models by exact version ID and READY state; distinguishes another version, downloadable and unidentified resources | Keep dynamic availability; also verify selected file, actual bytes and file existence |
| Batch enqueue | Resolves version metadata, reuses a global asset by version ID, links it to a workspace and creates download jobs | Use import dependency references, file-level deduplication and explicit per-resource results |
| File selection | Download worker finds the requested version, then primary file or first file | Preserve explicit file/hash evidence; surface ambiguous variants rather than picking primary |
| Storage | Model-type folders directly under the configured Comfy installation | Put managed weights outside the runtime; expose them through Comfy extra paths |
| Transfer | Streams with optional Bearer authentication; commits percentage progress after roughly 5 MB increments | Keep streaming and throttled progress; track bytes, verification and durable resume state |
| Integrity | Computes SHA-256 and stores it, then marks READY; this completion path does not compare an expected digest | Compare expected SHA-256 before publishing the file |
| Recovery | Deletes partial files and requeues interrupted/orphaned downloads | Keep recovery intent; retain validated partials and resume them |
| Worker | Awaits the pending download loop within the main worker iteration | Use an independent bounded download task group so transfers do not delay generation monitoring |

Sources: [import UI](../../../references/dreamtime/web/src/pages/ImportDetail.tsx),
[availability](../../../references/dreamtime/api/services/imports.py),
[batch route](../../../references/dreamtime/api/routers/civitai.py),
[download service](../../../references/dreamtime/api/services/model_download.py),
[model schema](../../../references/dreamtime/api/models/model_asset.py),
[worker](../../../references/dreamtime/api/services/worker.py), and
[status endpoint](../../../references/dreamtime/api/routers/models.py).

Two details matter when porting: Dreamtime makes version ID unique, which cannot
represent multiple downloadable files from one version. Its batch response has
separate model/job ID lists and can skip unresolved resources, while the import
UI correlates some results by array position. Remixfun should return a result
keyed by dependency ID, including reused, queued and blocked outcomes.

## User flow

1. Import saves the original image and recipe immediately. A separate resolver
   checks dependencies in the background; downloading does not hold up import.
2. Show each dependency as **Checking**, **Available**, **Download needed**,
   **Choose file**, or an actionable failure. Show known total download size and
   additional disk space. Metadata sizes are estimates until transport checks.
3. Offer **Download missing models · 6.94 GB**. This starts the displayed plan;
   it does not change models or begin generation. Repeated clicks reuse jobs.
   An optional remembered preference can later download unambiguous dependencies
   automatically; first delivery uses the explicit action without extra dialogs.
4. Show per-file and aggregate progress, including **Verifying**, plus pause,
   resume and retry. An unknown length shows bytes transferred, not a made-up
   percentage. Switching imports or reopening the app preserves progress.
5. Refresh availability after verification. Keep generation readiness separate:
   **Models available; generation settings still need attention** is valid.
   Downloads remain available when another source field blocks generation.

The main view stays small. Source hashes, format/precision variants, provider
file IDs, resolver evidence and transfer diagnostics remain under details.
Known access requirements get one direct action, such as setting a Civitai key
or visiting the provider's access page. A generic 403 remains access denied;
we must not assume every denial means a missing API key.

## Resolution and identity

Preserve provider model ID, version ID, file ID, reported source hashes,
expected file SHA-256 and observed local SHA-256 as distinct values.

Resolution order:

1. An explicit source file ID/full hash must agree with version metadata. A
   conflict blocks resolution. Short hashes and names are lookup clues only.
2. If the source identifies a version only, filter candidates by explicit role,
   supported file format and runtime compatibility. One compatible candidate
   can be selected automatically, with `selection_reason=only_compatible_file`.
   Several variants require a saved choice; the primary flag alone is not proof
   of the source's precision or file. Never fall back to another version/latest.
3. Look for verified matching bytes in the managed inventory and configured
   local libraries before scheduling a transfer. Reuse by SHA-256 even if the
   filename differs. A familiar filename or READY database flag is insufficient.
4. Resolve an ephemeral download location for that exact file at transfer time.
   Recheck version/file/hash identity on refresh; a changed upstream identity
   invalidates the plan instead of changing its target silently.

Keep two independent facts: **downloaded bytes match the selected provider
file** and **evidence identifies that file as the source dependency**. A
verified download is not proof of source-image reproduction. Preserve selection
reason and unresolved source ambiguity in the baseline/run manifest.

V1 handles SafeTensor checkpoints, with schema roles ready for LoRA and VAE.
Add their acquisition next without implying their generation graphs are ready.
Files without a full expected SHA-256 remain unresolved for verified automatic
acquisition; offer linking an existing file with explicitly weaker evidence in
a later extension. Arbitrary archives, pickle checkpoints and custom-node
installation are outside this first path.

## Service and persistent records

Use the existing SQLite database with small versioned migrations and explicit
tables/indexes. Keep immutable import JSON intact. Add a live dependency-plan
endpoint instead of rewriting stored source recipes or treating their current
`reproduction.blockers` snapshot as permanently authoritative.

| Record | Essential contents |
| --- | --- |
| Dependency plan | Import ID, plan revision, dependency IDs/roles, source evidence, selected file identity, selection reason, per-item blockers |
| Provider file | Provider/model/version/file IDs, role, format/precision, expected SHA-256, size estimate, metadata capture time |
| Local blob/location | Observed SHA-256, actual size, managed or external path, verification time and file fingerprint; provider aliases may share bytes |
| Download job | File identity, expected hash, state, partial ID, persisted byte offset, strong validator, length, retries, error code and timestamps |
| Dependency binding | Import/dependency ID → selected file/blob; immutable resolved snapshots are attached to later generation runs |

Use uniqueness on provider/file identity and on the active transfer target.
Expected hash changes form a conflict/new revision, never an in-place mutation
of an active target. Transactional enqueue joins an existing transfer when
multiple imports require the same bytes. One writer owns a partial. Canceling
one import's request releases that reference; other consumers keep their job.
Only an explicit global cancel stops a transfer still required elsewhere.

Suggested modules: `model_resolution.py`, `model_inventory.py`, and
`downloads.py`, called by `Service`. Split further only when implementation size
justifies it. HTTP and CLI are clients of these commands; Comfy never downloads.

Proposed API:

| Command | Purpose |
| --- | --- |
| `GET /api/imports/{id}/dependencies` | Current plan, live availability, aggregate size and generation blockers |
| `POST /api/imports/{id}/dependencies/resolve` | Queue refresh; return an operation ID immediately |
| `POST /api/imports/{id}/downloads` | Submit plan revision and any explicit file choices; return keyed reused/queued/blocked results |
| `GET /api/downloads` and `GET /api/downloads/{id}` | Durable state, bytes, verification progress and sanitized failure |
| `POST /api/downloads/{id}/pause`, `/resume`, `/cancel`, `/retry` | Idempotent lifecycle commands; resume/retry preserves file identity |
| `POST /api/models/scan` | Queue verification of configured existing model paths |

The submission response is fast; it never waits for gigabytes. Poll active jobs
at roughly one-second intervals initially; SSE is unnecessary for the first
delivery. API bodies carry plan/dependency IDs, not arbitrary download URLs or
destination paths. CLI equivalents: `models resolve <import>`,
`models download <import> --wait`, `downloads`, and `downloads pause/resume <id>`.

## Transfer and recovery rules

States: `queued → downloading → verifying → ready`, with `paused`,
`retry_wait`, `blocked`, `failed` and `canceled` branches. Start with two network
transfers and one hash-verification task at a time. Disk writes and hashing must
not block the API/generation event loop. Persist throttled progress plus a final
checkpoint when pausing or shutting down.

- Stream to a generated `.partial` file outside every Comfy-visible directory.
  Reserve remaining disk space across queued jobs on the actual model volume,
  accounting for copy fallback and a configurable free-space floor.
- Request identity encoding. Resume using Range and If-Range against a saved
  strong validator, only with the same selected file/hash. Require a coherent
  206 Content-Range starting at the local file length. A 200 response is a fresh
  transfer, never appended. A 416 requires reconciling total length and hashing
  a potentially complete partial; it is not automatic success. Weak/absent or
  changed validators restart the transfer safely rather than trusting a prefix.
- Reconcile the partial's actual length with recorded state after a crash.
  Flush/fsync at durable checkpoints; a missing tail may be downloaded again.
  Recompute the full file hash after resume instead of persisting hash internals.
- Distinguish estimated `sizeKB`, transfer length and actual byte count. Enforce
  available exact lengths and finite disk/transfer limits, then compare full
  SHA-256. An incomplete response or hash mismatch never becomes available.
- Flush and atomically publish verified bytes on the same volume, then commit
  the ready binding. Reconcile crashes between rename and DB commit: validate
  an already-published blob and finish the transaction without redownloading.
  A ready row with missing/changed bytes loses verified availability.
- Retry bounded transient network errors, 429 and selected 5xx with backoff and
  Retry-After. Keep actionable auth/access/storage failures blocked until their
  cause changes. Retry a corrupt file from scratch only within a bounded policy.
  Pause retains partials; cancel discards only the job-owned unshared partial.

Unlike image-preview acquisition, model download links can contain legitimate
signed query parameters. Implement a separate transfer transport: HTTPS,
provider-controlled endpoint and reviewed storage redirect destinations, bounded
redirects, no local/private destinations, and host-scoped credentials. Refresh
expired locations through the provider without changing file identity. Signed
URLs stay in memory and out of manifests/logs. Provider keys belong in the local
OS credential store; requests to storage hosts never receive the Civitai Bearer
key. Live redirect/auth behavior must be captured during implementation, not
assumed from the existing image-CDN allowlist.

On service restart, recover unfinished downloads independently of generation
jobs: previously active/queued transfers resume after reconciliation; explicitly
paused/canceled transfers remain stopped. On normal desktop close, an owned
service checkpoints downloads and shuts down gracefully; they resume next
launch. An independent service continues. This requires replacing the shell's
hard-kill path for this case with an acknowledged service shutdown and bounded
fallback. Active-generation handling keeps its separate policy. App updates
must use the same checkpoint boundary before replacing the owned service.

## Model cache and Comfy integration

Default model root is inside the app data directory, configurable onto another
drive. One service owns a writable model root; use a cache-root lock as well as
the existing library lock. Simultaneous independent writers sharing one cache
are deferred. User-selected external libraries are indexed read-only.

Store one managed copy under `blobs/<sha256>/model.safetensors`. Publish generated
hash-named hardlinks under typed `comfy/checkpoints`, `comfy/loras`, and
`comfy/vae` directories on the same volume. If hardlinks are unavailable, use a
verified copy with its additional disk requirement included in the plan. Track
every managed alias; never overwrite/delete files from an external library.
Existing libraries can instead be bound through explicit extra paths after
hash verification. Revalidate file fingerprints before use and rehash changes.

Generate Comfy extra-path configuration from these trusted local bindings. Its
[extra-path loader](../../../references/comfyui/utils/extra_config.py) supports
typed directories; validate the integration against our pinned runtime.
Bindings must identify the exact loader filename/path and avoid basename
collisions. A resolver must reject any ambiguous Comfy lookup.

Refactor `engine.py`: runtime startup verifies the runtime, not the existence
of one hard-coded checkpoint. Before a job, verify its selected model binding
and profile compatibility, construct the graph with that filename, and save
all model hashes in the job. The authored SDXL preset keeps its existing pin.
No download automatically makes an unsupported generation profile runnable.

## First delivery and acceptance

1. **Plan and inventory:** exact-file resolver, dynamic dependency endpoint,
   SQLite migrations, existing-file hashing and immutable bindings. Replay the
   captured beetle metadata and synthetic multi-file/conflicting-hash cases.
2. **Durable transfer:** checkpoint downloads, progress, pause/resume, credential
   boundary, space reservation, digest verification, atomic publish and crash
   reconciliation. Use an owned HTTP fixture server for interruption, Range
   variants, expired redirects, corruption and concurrent duplicate requests.
3. **Desktop and CLI:** Download Missing, recover progress after reopen,
   actionable partial-plan results, model-location settings and graceful owned
   service shutdown. Verify background transfer leaves generation monitoring
   responsive and an independent service alive.
4. **Live checkpoint acceptance:** resolve version 128078/file 92696, retrieve
   the permitted file, verify its expected SHA-256, restart and reuse it without
   another download. Check pause/resume on an interrupted transfer. Preserve
   the original source recipe and configured SDXL Base model.
5. **Engine handoff:** select the verified binding through a supported graph;
   first prove a controlled generation with it. Source-specific Euler ancestral,
   clip-skip and missing-scheduler handling are explicit follow-on reproduction
   work. Extend acquisition to LoRA/VAE with tests for their roles and strengths.

For image 141984808 the current metadata gives one checkpoint candidate:
`sdXL_v10VAEFix.safetensors`, model 101055, version 128078, file 92696,
approximately 6.94 GB (6.46 GiB), SHA-256
`e6bb9ea85bbf7bf6478a7c6d18b71246f22e95d41bcdd80ed40aa212c33cfeff`.
See the [captured version](../../tests/fixtures/civitai-141984808/model-version.json)
and [live import evidence](../evidence/civitai-page-import.md). Download access
has not yet been tested. Successful acquisition should change its model status
to available; missing scheduler/batch evidence and source matching remain
separately unresolved.

Defer a general model browser, torrent/multipart acceleration, automatic model
updates, distributed workers, automatic cache eviction and video-specific
dependency discovery. Deliver the import-driven checkpoint path first, with
the identity and recovery rules needed to extend it without a storage rewrite.
