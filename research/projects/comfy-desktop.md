# Comfy Desktop

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/Comfy-Org/Comfy-Desktop) · [Local clone](../../../references/comfy-desktop/) · [Raw snapshot](../evidence/comfy-desktop.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2026-02-13 / 210 days (about 0.57 years) |
| Oldest reachable commit | 2026-02-13T00:09:30-08:00 — can include inherited history |
| Stars / forks / subscribers | 446 / 59 / 3 |
| Open issues + PRs | 192 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `8f2f26c021971c61608a6207e013474011594dbb` |
| HEAD commit | 2026-09-12T01:43:23Z feat(telemetry): capture typed asset scanner errors (#1490) |
| Reachable commits, including merges | 858 |
| Historical distinct author names | 17 |
| Last 90 days: nonmerge commits / author names | 184 / 14 |
| Source license assessment | Dual AGPL-3.0-or-later OR commercial license |
| Operating systems / hardware scope | Windows, macOS Apple Silicon, and documented Linux AppImage/.deb support |
| Distribution model | Electron desktop manager; external installer delivery; source release feed can lack binary attachments |
| Fit for Remixfun | Primary benchmark for managed Comfy installation, instances, snapshots, and recovery |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Jedrzej Kosinski | 520 | Jedrzej Kosinski | 57 |
| Deep Mehta | 115 | cloud-code-bot[bot] | 40 |
| Maanil Verma | 65 | Benjamin Lu | 30 |
| Benjamin Lu | 56 | Maanil Verma | 21 |
| cloud-code-bot[bot] | 56 | Deep Mehta | 19 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v1.1.0-rc.1: chore: bump version to 1.1.0-rc.1 (#1516)](https://github.com/Comfy-Org/Comfy-Desktop/releases/tag/v1.1.0-rc.1) | 2026-09-09T23:37:31Z | No attached artifacts in captured expansion; check external distribution |
| [v1.0.47: chore: bump version to 1.0.47 (#1500)](https://github.com/Comfy-Org/Comfy-Desktop/releases/tag/v1.0.47) | 2026-09-08T20:50:08Z | No attached artifacts in captured expansion; check external distribution |
| [v1.0.47-rc.4](https://github.com/Comfy-Org/Comfy-Desktop/releases/tag/v1.0.47-rc.4) | 2026-09-04T03:05:03Z | No attached artifacts in captured expansion; check external distribution |
| [v1.0.47-rc.3: fix(release): raise upload limit and bump to 1.0.47-rc.3 (#1483)](https://github.com/Comfy-Org/Comfy-Desktop/releases/tag/v1.0.47-rc.3) | 2026-09-04T02:39:21Z | No attached artifacts in captured expansion; check external distribution |
| [v1.0.47-rc.2: chore: bump version to 1.0.47-rc.2 (#1482)](https://github.com/Comfy-Org/Comfy-Desktop/releases/tag/v1.0.47-rc.2) | 2026-09-04T02:26:34Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

Comfy Desktop already tackles the environment-management work often underestimated in a new wrapper: installing and managing Comfy instances, Python/Git-related resources, runtime environments, model locations, updates, and recovery. It is a stronger baseline than “Comfy is hard to install” suggests.[^s1][^s3]

This repository's February 2026 creation date is not the birth date of every version of the Comfy desktop product. Repository succession and packaging changes matter when comparing age/popularity to older apps.

## Architecture

The inspected application uses Electron with Vue/TypeScript and Pinia-oriented renderer state. Main-process code owns installation, files, processes, and runtime lifecycle; preload/typed IPC exposes those operations to the renderer. Electron-vite and associated test tooling support the desktop build.[^s2][^s3][^s4][^s5][^s6]

The installer/instance model separates application UI from Comfy environments and data. Bootstrap/runtime resources, instance migration, snapshots, and rollback are first-class concerns in the source. That is the sort of subsystem Remixfun would need in addition to Tauri's window and updater.[^s1][^s3]

Using Tauri instead of Electron changes the shell/toolchain, not the underlying need to manage executable environments. The larger installed footprint will often be Python/Torch, nodes, and weights rather than the webview framework itself.

## Workflow overlap

Desktop makes the existing Comfy frontend available in an ordinary app and manages its execution environment. Combined with App Mode, it can already provide a simple workflow UI. It does not by itself establish a foreign-image recipe recovery and controlled experiment product; that remains the relevant distinction for Remixfun.[^s1][^s5]

A separate Remixfun application gains a focused library and source/baseline/variant workflow. A Comfy extension gains an existing installer, runtime, and graph editor. The cost difference between those approaches should be evaluated before committing to a large custom runtime manager.

## OS and release interpretation

Current dedicated documentation and repository material include Windows, Apple Silicon macOS, and Linux AppImage/.deb. Some older badges/engine README snippets mention only Windows/macOS. The report uses the dedicated current guidance rather than repeating the older limited list.[^s1][^s8]

The captured release feed includes a release candidate and may show no attached installer files because delivery occurs externally. Feed order does not establish the latest stable consumer installer. OS support also does not imply all custom nodes and models work on each platform.

## License, maintenance, and comparison

The actual license explicitly offers **AGPL-3.0-or-later or a separate commercial license**. GitHub's `NOASSERTION` classification is less informative than that text. It is neither simply MIT nor unavailable proprietary-only source.[^s7]

Dreamtime has no equivalent runtime manager but already has the focused generation UI and Comfy adapter. Study Desktop's installation/recovery behavior and typed process boundary; do not copy a large Electron application merely to package a React app in Tauri.

Evaluation should include first install, importing an existing Comfy directory, shared model paths, failed node installation, restoring an instance snapshot, and engine updates while jobs exist. Compare those experiences with the proposed minimal Remixfun runtime manager. No installers were run in this survey.

## Source map and citations

[^s1]: **Desktop setup, instances, supported packaging** — [Pinned source](https://github.com/Comfy-Org/Comfy-Desktop/blob/8f2f26c021971c61608a6207e013474011594dbb/README.md); [local README.md](../../../references/comfy-desktop/README.md).

[^s2]: **Electron/Vue/TypeScript build** — [Pinned source](https://github.com/Comfy-Org/Comfy-Desktop/blob/8f2f26c021971c61608a6207e013474011594dbb/package.json); [local package.json](../../../references/comfy-desktop/package.json).

[^s3]: **Runtime management, installation, and native operations** — [Pinned source](https://github.com/Comfy-Org/Comfy-Desktop/tree/8f2f26c021971c61608a6207e013474011594dbb/src/main); [local src/main](../../../references/comfy-desktop/src/main).

[^s4]: **Native/renderer bridge** — [Pinned source](https://github.com/Comfy-Org/Comfy-Desktop/tree/8f2f26c021971c61608a6207e013474011594dbb/src/preload); [local src/preload](../../../references/comfy-desktop/src/preload).

[^s5]: **Vue desktop UI** — [Pinned source](https://github.com/Comfy-Org/Comfy-Desktop/tree/8f2f26c021971c61608a6207e013474011594dbb/src/renderer); [local src/renderer](../../../references/comfy-desktop/src/renderer).

[^s6]: **Typed process boundary** — [Pinned source](https://github.com/Comfy-Org/Comfy-Desktop/blob/8f2f26c021971c61608a6207e013474011594dbb/src/types/ipc.ts); [local src/types/ipc.ts](../../../references/comfy-desktop/src/types/ipc.ts).

[^s7]: **Explicit dual license** — [Pinned source](https://github.com/Comfy-Org/Comfy-Desktop/blob/8f2f26c021971c61608a6207e013474011594dbb/LICENSE); [local LICENSE](../../../references/comfy-desktop/LICENSE).

[^s8]: [Current official Linux/Mac/Windows distribution guidance](https://docs.comfy.org/installation/system_requirements), accessed 2026-09-12.
