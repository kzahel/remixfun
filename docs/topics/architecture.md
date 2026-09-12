# Architecture

Status: shared local service, browser/CLI clients, SQLite/artifact storage and
Windows developer shell implemented. Comfy and remote listening remain planned.

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
close while its owned service reports an active demo, and stops an idle owned
service on exit. Crash cleanup, generation cancellation, and robust active-job
update coordination still require the later runtime/lifecycle work.

The preview has no remote bind option, credential store, native privileged web
commands, updater, or external engine attachment. Host and Origin checks reject
foreign browser access; images are served by opaque content hashes. Provider
requests use fixed API/CDN hosts, with no redirects to arbitrary hosts. Transient
URLs and known credential fields are omitted from retained provider evidence.
Do not interpret local-only checks as the planned remote authentication scheme.

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
