# Desktop Release Kit — distribution baseline

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/kzahel/desktop-release-kit) · [Local clone](../../../references/desktop-release-kit/) · [Raw snapshot](../evidence/desktop-release-kit.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2026-08-09 / 33 days (about 0.09 years) |
| Oldest reachable commit | 2026-08-09T12:09:21+02:00 — can include inherited history |
| Stars / forks / subscribers | 0 / 0 / 0 |
| Open issues + PRs | 0 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `c8d96dd87cb244f96b0123c113b4da17bd698c37` |
| HEAD commit | 2026-09-05T19:26:08+02:00 Document completed Stable Latest channel acceptance |
| Reachable commits, including merges | 10 |
| Historical distinct author names | 1 |
| Last 90 days: nonmerge commits / author names | 10 / 1 |
| Source license assessment | MIT |
| Operating systems / hardware scope | macOS Apple Silicon/Intel; Windows x64; Linux x64/ARM64 |
| Distribution model | Tauri canary with signed releases, native installers, updater artifacts, and acceptance evidence |
| Fit for Remixfun | Adopt release contracts and validation patterns; not a Python/GPU/model installer |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Kyle Graehl | 10 | Kyle Graehl | 10 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [Desktop Release Canary v0.4.0](https://github.com/kzahel/desktop-release-kit/releases/tag/desktop-v0.4.0) | 2026-09-05T17:07:43Z | `Desktop.Release.Canary-0.4.0-1.aarch64.rpm`, `Desktop.Release.Canary-0.4.0-1.x86_64.rpm`, `Desktop.Release.Canary_0.4.0_aarch64.AppImage`, `Desktop.Release.Canary_0.4.0_aarch64.dmg`, `Desktop.Release.Canary_0.4.0_amd64.AppImage`, `Desktop.Release.Canary_0.4.0_amd64.deb`, `Desktop.Release.Canary_0.4.0_arm64.deb`; +8 more in snapshot |
| [Desktop Release Canary v0.2.0](https://github.com/kzahel/desktop-release-kit/releases/tag/desktop-v0.2.0) | 2026-09-05T16:13:28Z | `Desktop.Release.Canary-0.2.0-1.aarch64.rpm`, `Desktop.Release.Canary-0.2.0-1.x86_64.rpm`, `Desktop.Release.Canary_0.2.0_aarch64.AppImage`, `Desktop.Release.Canary_0.2.0_aarch64.dmg`, `Desktop.Release.Canary_0.2.0_amd64.AppImage`, `Desktop.Release.Canary_0.2.0_amd64.deb`, `Desktop.Release.Canary_0.2.0_arm64.deb`; +8 more in snapshot |
| [Desktop Release Canary v0.5.1201](https://github.com/kzahel/desktop-release-kit/releases/tag/desktop-latest-v0.5.1201) | 2026-09-05T17:06:56Z | `Desktop.Release.Canary-0.5.1201-1.aarch64.rpm`, `Desktop.Release.Canary-0.5.1201-1.x86_64.rpm`, `Desktop.Release.Canary_0.5.1201_aarch64.AppImage`, `Desktop.Release.Canary_0.5.1201_aarch64.dmg`, `Desktop.Release.Canary_0.5.1201_amd64.AppImage`, `Desktop.Release.Canary_0.5.1201_amd64.deb`, `Desktop.Release.Canary_0.5.1201_arm64.deb`; +8 more in snapshot |
| [Desktop Release Canary v0.3.1101](https://github.com/kzahel/desktop-release-kit/releases/tag/desktop-latest-v0.3.1101) | 2026-09-05T16:34:59Z | `Desktop.Release.Canary-0.3.1101-1.aarch64.rpm`, `Desktop.Release.Canary-0.3.1101-1.x86_64.rpm`, `Desktop.Release.Canary_0.3.1101_aarch64.AppImage`, `Desktop.Release.Canary_0.3.1101_aarch64.dmg`, `Desktop.Release.Canary_0.3.1101_amd64.AppImage`, `Desktop.Release.Canary_0.3.1101_amd64.deb`, `Desktop.Release.Canary_0.3.1101_arm64.deb`; +8 more in snapshot |
| [Desktop Release Canary v0.3.901](https://github.com/kzahel/desktop-release-kit/releases/tag/desktop-latest-v0.3.901) | 2026-09-05T16:11:39Z | `Desktop.Release.Canary-0.3.901-1.aarch64.rpm`, `Desktop.Release.Canary-0.3.901-1.x86_64.rpm`, `Desktop.Release.Canary_0.3.901_aarch64.AppImage`, `Desktop.Release.Canary_0.3.901_aarch64.dmg`, `Desktop.Release.Canary_0.3.901_amd64.AppImage`, `Desktop.Release.Canary_0.3.901_amd64.deb`, `Desktop.Release.Canary_0.3.901_arm64.deb`; +8 more in snapshot |

## Assessment

This is the appropriate distribution reference because it belongs to the user's existing release infrastructure and already defines the intended multi-platform updater contract. It is a deliberately small canary, not a generic image-generation starter app. Remixfun should adopt its contracts and tested release behavior, while keeping its own product identity and lifecycle.[^s1][^s2]

The clone is taken from the existing local repository at `c8d96dd87cb2`, with a clean original working tree. Public stars and age are recorded for completeness, but they are not meaningful measures of suitability for an internal release contract.

## Architecture and artifacts

The Tauri application contains native updater/lifecycle logic, a webview, bundled resources, and a small nested native sidecar. The sidecar staging script creates target-triple-specific binaries. Matching build identities across app, frontend, and sidecar let an update test prove the whole installed product was replaced.[^s4][^s5][^s6]

The shared update server routes release metadata; immutable artifacts are hosted in GitHub Releases. The server is a separate project. Stable and Latest channels are defined explicitly, including version identities, channel transitions, publication gates, and older-client behavior.[^s1][^s2][^s3]

The release matrix covers five updater targets: Apple Silicon and Intel macOS, Windows x64, and Linux x64/ARM64. NSIS is the Windows in-app update path; AppImage is the Linux path. Additional DMG/MSI/DEB/RPM artifacts are validated as part of the normal release matrix. These are concrete artifact obligations, not evidence that a GPU engine runs on all five targets.[^s1][^s2]

## What it solves for Remixfun

It provides patterns for signing, notarization, updater signatures, release completeness, build identity, channels, relaunch, and installed-version testing. This is much more valuable than copying a blank Tauri window and adding an updater later.[^s2][^s3][^s7]

It does **not** install Python, choose Torch wheels, resolve CUDA/ROCm/MPS compatibility, manage custom nodes, validate workflow dependencies, or cache model weights. Remixfun needs a separate runtime installer and content ledger. A tiny native canary sidecar is not evidence that a large Python environment can be bundled identically.[^s6]

App updates, engine-profile updates, and model downloads should have separate version/rollback rules. Otherwise an ordinary UI update can invalidate a reproducible experiment or cause multi-gigabyte redownloads.

## Adoption boundaries

Remixfun needs its own application identifier, updater key, update-server product route, release naming/configuration, and installed old-to-new acceptance run. The canary's existing identity and signing material must not be reused. This follows the repository's explicit adoption contract and is a concrete implementation requirement for future release work.[^s1][^s2]

The recorded acceptance campaigns are useful evidence that the kit was exercised, but this survey did not repeat those runs. Distinguish source/runbook evidence from a new validation of Remixfun, which currently has no runtime or release artifacts.[^s7][^s8]

## Comparison with Dreamtime

Dreamtime provides the application and inference integration but lacks a desktop release lifecycle. The kit provides the release lifecycle but none of the generation domain. They are complementary. Initial Windows-only shipment can be sensible, provided any adaptation of the kit's five-target publication gate is explicit and tested rather than silently removing missing-target checks.

The source is MIT. Future release validation should include paths with spaces/non-ASCII text, interrupted updates, running engine jobs, library preservation, and engine rollback compatibility, extending the existing installed-update tests with Remixfun-specific behavior.[^s9]

## Source map and citations

[^s1]: **Canary purpose, architecture, and adoption rules** — [Pinned source](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/README.md); [local README.md](../../../references/desktop-release-kit/README.md).

[^s2]: **Normative updater contract** — [Pinned source](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/contract/desktop-update-v1.md); [local contract/desktop-update-v1.md](../../../references/desktop-release-kit/contract/desktop-update-v1.md).

[^s3]: **Stable/Latest channel contract** — [Pinned source](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/contract/desktop-update-channels-v1.md); [local contract/desktop-update-channels-v1.md](../../../references/desktop-release-kit/contract/desktop-update-channels-v1.md).

[^s4]: **Tauri package configuration** — [Pinned source](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/src-tauri/tauri.conf.json); [local src-tauri/tauri.conf.json](../../../references/desktop-release-kit/src-tauri/tauri.conf.json).

[^s5]: **Native lifecycle and updater integration** — [Pinned source](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/src-tauri/src/lib.rs); [local src-tauri/src/lib.rs](../../../references/desktop-release-kit/src-tauri/src/lib.rs).

[^s6]: **Target-specific sidecar staging** — [Pinned source](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/scripts/prepare-sidecar.mjs); [local scripts/prepare-sidecar.mjs](../../../references/desktop-release-kit/scripts/prepare-sidecar.mjs).

[^s7]: **Installed old-to-new acceptance procedure** — [Pinned source](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/docs/canary-testbed-runbook.md); [local docs/canary-testbed-runbook.md](../../../references/desktop-release-kit/docs/canary-testbed-runbook.md).

[^s8]: **Existing recorded cross-platform acceptance evidence** — [Pinned source](https://github.com/kzahel/desktop-release-kit/tree/c8d96dd87cb244f96b0123c113b4da17bd698c37/docs/evidence); [local docs/evidence](../../../references/desktop-release-kit/docs/evidence).

[^s9]: **MIT source license** — [Pinned source](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/LICENSE); [local LICENSE](../../../references/desktop-release-kit/LICENSE).
