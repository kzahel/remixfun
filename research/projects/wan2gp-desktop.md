# Wan2GP Desktop Tauri launcher

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/GKartist75/Wan2GP-Desktop-Tauri) · [Local clone](../../../references/wan2gp-desktop/) · [Raw snapshot](../evidence/wan2gp-desktop.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2026-09-03 / 9 days (about 0.02 years) |
| Oldest reachable commit | 2026-08-31T10:35:29+02:00 — can include inherited history |
| Stars / forks / subscribers | 12 / 0 / 0 |
| Open issues + PRs | 2 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | master / `e453fafaf9dac560c4eca9b2372b152c1345579f` |
| HEAD commit | 2026-09-11T21:42:11+02:00 Merge branch 'dev' into master — v0.6.2 release |
| Reachable commits, including merges | 243 |
| Historical distinct author names | 2 |
| Last 90 days: nonmerge commits / author names | 218 / 2 |
| Source license assessment | No tracked LICENSE file found; reuse permission unresolved |
| Operating systems / hardware scope | Windows release artifacts verified in snapshot; macOS/Linux delivery not established |
| Distribution model | Tauri 2 launcher; Windows NSIS/MSI and updater metadata; manages external WanGP runtime |
| Fit for Remixfun | Very close packaging concept, very young implementation, unresolved license |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| GKartist75 | 214 | GKartist75 | 214 |
| Gerard | 4 | Gerard | 4 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v0.6.2](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/releases/tag/v0.6.2) | 2026-09-11T19:42:26Z | `Wan2GP.Desktop.Launcher.Tauri_0.6.2_x64-setup.exe`, `Wan2GP.Desktop.Launcher.Tauri_0.6.2_x64-setup.exe.sig`, `Wan2GP.Desktop.Launcher.Tauri_0.6.2_x64_en-US.msi`, `latest.json` |
| [v0.6.1](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/releases/tag/v0.6.1) | 2026-09-11T14:20:12Z | `Wan2GP.Desktop.Launcher.Tauri_0.6.1_x64-setup.exe`, `Wan2GP.Desktop.Launcher.Tauri_0.6.1_x64-setup.exe.sig`, `Wan2GP.Desktop.Launcher.Tauri_0.6.1_x64_en-US.msi`, `latest.json` |
| [v0.6.0](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/releases/tag/v0.6.0) | 2026-09-11T13:20:36Z | `Wan2GP.Desktop.Launcher.Tauri_0.6.0_x64-setup.exe`, `Wan2GP.Desktop.Launcher.Tauri_0.6.0_x64-setup.exe.sig`, `Wan2GP.Desktop.Launcher.Tauri_0.6.0_x64_en-US.msi`, `latest.json` |
| [backup/dev-2026-09-11: fix(embed): include w2gp.js native bridges omitted from feature commit](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/releases/tag/backup%2Fdev-2026-09-11) | 2026-09-11T06:38:52Z | No attached artifacts in captured expansion; check external distribution |
| [archive/dev-clean-2026-09-11](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/releases/tag/archive%2Fdev-clean-2026-09-11) | 2026-09-11T06:41:20Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

This is a directly relevant example of wrapping a complex local video-generation application with Tauri. It demonstrates that the packaging idea already exists. It is also extremely young: created less than ten days before the snapshot, with low double-digit stars and a history dominated by two likely related author names.[^s1]

## Architecture

The shell uses Tauri 2 and Rust native commands, with a lightweight HTML/JavaScript frontend. The configuration points at static frontend assets rather than a large framework build. Rust modules handle installation/runtime operations and subprocess behavior; browser-facing service controls manage the launched WanGP web application.[^s2][^s3][^s4][^s5][^s6]

The launcher handles substantially more than opening a URL: prerequisites, Python/environment setup, GPU-related runtime choices, process start/stop, and updates. The native code includes Windows-specific subprocess handling. This makes it useful for studying the work a Windows-first Remixfun shell will need, while also showing why a Tauri target list alone does not establish Linux/Mac readiness.[^s1][^s3]

## What it changes about the user's workflow

It can reduce the friction of installing and launching WanGP. The generation semantics, metadata, model capabilities, and headless behavior still come from WanGP. The launcher does not establish a new foreign-image replay model, dependency provenance layer, or controlled-remix experiment system.

For Remixfun, that division should remain explicit: desktop onboarding can improve access to an engine, while the application's data model supplies the distinct creative workflow. A branded window around an existing Gradio app is not itself the full product opportunity.

## Distribution and licensing

The captured release assets establish Windows installer/updater delivery. Tauri's configuration uses broad bundle targets and includes cross-platform icon files, but those are not proof of Mac/Linux releases or usable GPU environments. The report therefore classifies those platforms as unestablished for this launcher.[^s2]

No tracked `LICENSE`/license file was found at collection. Public source visibility and Tauri's own license do not determine permission to copy this application. WanGP's custom license is an additional, separate consideration even if launcher-source permission is later clarified. These two licensing questions must not be collapsed.

## Comparison with Dreamtime and release kit

Dreamtime supplies the generator application; this launcher supplies a packaging pattern for another engine. Desktop Release Kit is the stronger fit for the user's established signing/updater infrastructure. The useful lessons here are setup progress, environment diagnostics, process supervision, and recovery—not copying its updater identity or replacing the kit.

Evaluate on a clean Windows account, with install paths containing spaces, missing prerequisites, interrupted downloads, application restart, and an already-running engine. Then compare how it distinguishes a UI update from a runtime update. Such a short source history and successful release attachments are insufficient evidence of long-term recovery reliability.

## Source map and citations

[^s1]: **Launcher purpose and install experience** — [Pinned source](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/blob/e453fafaf9dac560c4eca9b2372b152c1345579f/README.md); [local README.md](../../../references/wan2gp-desktop/README.md).

[^s2]: **Tauri targets, CSP, and updater endpoint** — [Pinned source](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/blob/e453fafaf9dac560c4eca9b2372b152c1345579f/src-tauri/tauri.conf.json); [local src-tauri/tauri.conf.json](../../../references/wan2gp-desktop/src-tauri/tauri.conf.json).

[^s3]: **Rust process/install commands** — [Pinned source](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/tree/e453fafaf9dac560c4eca9b2372b152c1345579f/src-tauri/src); [local src-tauri/src](../../../references/wan2gp-desktop/src-tauri/src).

[^s4]: **Launcher UI** — [Pinned source](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/blob/e453fafaf9dac560c4eca9b2372b152c1345579f/src/app.js); [local src/app.js](../../../references/wan2gp-desktop/src/app.js).

[^s5]: **Frontend runtime/service controls** — [Pinned source](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/tree/e453fafaf9dac560c4eca9b2372b152c1345579f/src); [local src](../../../references/wan2gp-desktop/src).

[^s6]: **Frontend/build dependency scope** — [Pinned source](https://github.com/GKartist75/Wan2GP-Desktop-Tauri/blob/e453fafaf9dac560c4eca9b2372b152c1345579f/package.json); [local package.json](../../../references/wan2gp-desktop/package.json).
