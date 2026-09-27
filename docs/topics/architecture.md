# Architecture

Status: shared local service, browser/CLI clients, SQLite/artifact storage and
Windows developer shell implemented. Optional managed Comfy SDXL profiles run
through the source service on verified Windows/NVIDIA and Apple Silicon/MPS
setups. Remote listening remains planned.

## Current application boundary

`remixfun serve` hosts the built frontend and `/api` from one loopback address
(default port 8788). Vite can proxy the API for development. The CLI calls this
HTTP contract; it never creates its own service or engine for import commands.
`/api/health` returns app, version, API version, source SHA, process-instance
identity, and current engine/network capability. The frozen service embeds its
own build identity; local development defaults to `development`.

SQLite stores imports and jobs; content-addressed files are promoted atomically
after writing and flushing. A cross-process file lock prevents multiple service
hosts from recovering or mutating the same library concurrently. Active demo
jobs become interrupted after shutdown or crash recovery; they are never
silently rerun. Source manifests remain unchanged by jobs.

The Windows Tauri shell displays the same loopback UI. It attaches only when
application/version/API/source identities match, otherwise fails on the occupied
port. A newly spawned service must also match the shell's process nonce. Desktop
close keeps an independently started service alive. It refuses ordinary window
close while its owned service reports active generation or an unknown outcome.
An owner-authenticated shutdown request stops admission and saves active download
progress before exit; restart resumes queued transfers. Crash cleanup, generation cancellation, and robust active-job
update coordination still require the later runtime/lifecycle work.

With `--comfy-root`, the service verifies the pinned Comfy revision, then starts
its own runtime on an available loopback port. It verifies the selected checkpoint
before generation. Managed cache aliases are supplied through extra model paths.
The service requires CUDA on Windows/Linux and MPS on macOS; the Mac profile is
validated for newly authored SDXL Base images. The selected device type is saved
with the job runtime identity. No custom or API nodes load. Graphs are
constructed from bounded authored or supported imported-recipe fields; arbitrary imported graphs are
never executed. See the [runtime profile](../../runtime-profiles/README.md).

One real generation may be active at a time. Submission is not retried after
an uncertain response. The job retains its Comfy prompt ID once acknowledged;
uncertain outcomes block further GPU submissions until inspection and restart.
Shutdown cancels monitoring, marks the job interrupted and stops the owned
runtime. Restart never resubmits jobs. Hard-crash child-process reconciliation
is still manual. CPU tests cover these transitions; real GPU close/restart
acceptance remains pending. The initial frozen desktop does not configure this
optional source-service runtime. macOS desktop packaging is not implemented.

The preview has no remote bind option, native privileged web
commands, updater, or external engine attachment. Host and Origin checks reject
foreign browser access; images are served by opaque content hashes. Provider
requests use the validated Civitai page host and the image CDN, with a
browser-style User-Agent. Page HTML is parsed as data; scripts never execute
and rotating Next.js build IDs are not needed. REST enriches CDN URLs and bounded
exact model-version/file evidence; it never overrides generation settings.
Responses have size limits, timeouts and bounded transient retries. Redirects
stay on the request's allowed HTTPS hosts, without credentials or query strings.
Image downloads allow `image.civitai.com` and its observed public blob destination
`blobs-b2.civitai.com`; page and model requests retain their page-host restriction;
the final page must still identify the requested image. Transient
URLs and known credential fields are omitted from retained provider evidence.
Do not interpret local-only checks as the planned remote authentication scheme.

Model acquisition has a separate persistent queue, locked model inventory and
restricted download transport. Civitai keys use an approved OS credential store;
they are sent only to Civitai, never redirected storage. Background resolution
keeps file choices separate from source metadata. See the implemented
[model contract](models.md) for transfer, cache and shutdown behavior.
Imported attempts have a revisioned plan and save effective settings separately
from immutable sources. The [attempt contract](reproduction.md) owns mappings,
explicit assumptions and decoded-reference comparisons.

## Planned runtime and distribution boundaries

The React/Vite client is shared by a Tauri desktop shell and ordinary browsers.
A Python/FastAPI service owns imports, model acquisition, jobs, history, SQLite
metadata, filesystem artifacts, and engine supervision. The CLI uses that same
service contract. No generation operation requires an open webview.

Comfy is an execution adapter behind the service. Runtime profiles pin Comfy,
Python, Torch, and any reviewed custom nodes. App updates, runtime upgrades,
and model downloads have separate identities and lifecycles. Modernize the
Dreamtime integration with a tested replacement profile and preserve rollback.

Desktop-owned service processes and independently launched headless services
have explicit ownership. Closing a window must not terminate an independent
service. Updating or relaunching must account for active generation/downloads;
preserve job state and never interrupt them silently.

Bind to loopback by default. Settings can enable a network listener and select
its port/address. Remote access requires authentication for UI/API, media, and
progress streams. Comfy remains on loopback. Keep credentials out of URLs,
artifacts, and logs. Model and app-data paths are portable and configurable.

Inject provider, engine, download transport, clock, and storage boundaries for
tests. Keep original source metadata immutable and persist per-image effective
seed, batch strategy, model hashes, runtime profile, and recipe lineage.
