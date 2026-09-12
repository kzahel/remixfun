# Architecture

Status: selected boundaries; application implementation pending.

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
