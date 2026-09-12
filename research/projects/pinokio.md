# Pinokio

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/pinokiocomputer/pinokio) · [Local clone](../../../references/pinokio/) · [Raw snapshot](../evidence/pinokio.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:58:15.967620+00:00 |
| Repository creation / age | 2023-07-09 / 1,160 days (about 3.18 years) |
| Oldest reachable commit | 2023-07-09T06:08:01-04:00 — can include inherited history |
| Stars / forks / subscribers | 8,018 / 807 / 105 |
| Open issues + PRs | 468 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `0765ab1c24eee9bf7acf1618b94e1cfdc52886fc` |
| HEAD commit | 2026-09-02T18:52:13-04:00 8.2.0 |
| Reachable commits, including merges | 677 |
| Historical distinct author names | 1 |
| Last 90 days: nonmerge commits / author names | 157 / 1 |
| Source license assessment | MIT application source; installed scripts/apps have separate terms |
| Operating systems / hardware scope | Windows/Linux/macOS; shipped x64/ARM64 coverage varies by artifact and installed app |
| Distribution model | Electron desktop launcher with installer/archive releases and a separate pinokiod backend dependency |
| Fit for Remixfun | Established onboarding alternative; not a recipe-reproduction application |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| cocktailpeanut | 677 | cocktailpeanut | 157 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v8.2.0](https://github.com/pinokiocomputer/pinokio/releases/tag/v8.2.0) | 2026-09-03T14:48:45Z | `Pinokio-8.2.0-arm64-mac.zip`, `Pinokio-8.2.0-arm64-mac.zip.blockmap`, `Pinokio-8.2.0-arm64.AppImage`, `Pinokio-8.2.0-arm64.dmg`, `Pinokio-8.2.0-arm64.dmg.blockmap`, `Pinokio-8.2.0-mac.zip`, `Pinokio-8.2.0-mac.zip.blockmap`; +13 more in snapshot |
| [v8.0.40](https://github.com/pinokiocomputer/pinokio/releases/tag/v8.0.40) | 2026-07-22T06:09:22Z | `Pinokio-8.0.40-arm64-mac.zip`, `Pinokio-8.0.40-arm64-mac.zip.blockmap`, `Pinokio-8.0.40-arm64.AppImage`, `Pinokio-8.0.40-arm64.dmg`, `Pinokio-8.0.40-arm64.dmg.blockmap`, `Pinokio-8.0.40-mac.zip`, `Pinokio-8.0.40-mac.zip.blockmap`; +13 more in snapshot |
| [v8.0.35](https://github.com/pinokiocomputer/pinokio/releases/tag/v8.0.35) | 2026-07-18T15:36:54Z | `Pinokio-8.0.35-arm64-mac.zip`, `Pinokio-8.0.35-arm64-mac.zip.blockmap`, `Pinokio-8.0.35-arm64.AppImage`, `Pinokio-8.0.35-arm64.dmg`, `Pinokio-8.0.35-arm64.dmg.blockmap`, `Pinokio-8.0.35-mac.zip`, `Pinokio-8.0.35-mac.zip.blockmap`; +13 more in snapshot |
| [v8.0.31](https://github.com/pinokiocomputer/pinokio/releases/tag/v8.0.31) | 2026-07-15T22:04:53Z | `Pinokio-8.0.31-arm64-mac.zip`, `Pinokio-8.0.31-arm64-mac.zip.blockmap`, `Pinokio-8.0.31-arm64.AppImage`, `Pinokio-8.0.31-arm64.dmg`, `Pinokio-8.0.31-arm64.dmg.blockmap`, `Pinokio-8.0.31-mac.zip`, `Pinokio-8.0.31-mac.zip.blockmap`; +13 more in snapshot |
| [v8.0.30](https://github.com/pinokiocomputer/pinokio/releases/tag/v8.0.30) | 2026-07-15T15:12:32Z | `Pinokio-8.0.30-arm64-mac.zip`, `Pinokio-8.0.30-arm64-mac.zip.blockmap`, `Pinokio-8.0.30-arm64.AppImage`, `Pinokio-8.0.30-arm64.dmg`, `Pinokio-8.0.30-arm64.dmg.blockmap`, `Pinokio-8.0.30-mac.zip`, `Pinokio-8.0.30-mac.zip.blockmap`; +13 more in snapshot |

## Assessment

Pinokio addresses “make this local AI application install and run without manual terminal work.” That overlaps strongly with Remixfun onboarding and competes with the claim that desktop packaging alone is a differentiator. It does not itself implement image recipe recovery or video generation.[^s1]

## Architecture

The inspected repository is an Electron desktop shell with window/navigation/native integration and updater code. A substantial backend is supplied through the separate `pinokiod` package; that companion source was not cloned or deeply audited in this survey. The package manifest explicitly shows this boundary.[^s2][^s3][^s4][^s5]

Application scripts describe install/run/update actions, environments, and local services. The launcher provides a friendly interface around those operations and can expose the resulting web applications. Per-app directories/environments organize dependencies, but that is not the same as a security sandbox: the README explicitly says scripts can execute commands.[^s1]

The practical architectural lesson is to keep the generation app's web service usable independently of the launcher. The difficult part is dependency lifecycle, shell differences, process state, and recovery; a window alone does not solve those.

## Target workflow coverage

Pinokio can deliver other applications that implement image/video workflows. It does not make those applications share a model identity ledger, imported source record, experiment history, or a single coherent source-to-motion journey. End-to-end task coverage must be attributed to the installed app, not to the launcher catalog.

The catalog's verification/review claims are project policy, not an independent guarantee that every script is safe or every engine combination works. This survey did not install or execute catalog scripts.[^s1]

## Distribution, maintenance, and license

The repository has substantial historical attention, continued recent commits, and multi-platform release assets. The current package is versioned separately from the software it launches, illustrating why app updates and engine/runtime updates are different concerns.[^s2][^s5]

The source license is MIT. Each installed script, engine, and model retains its own terms. A permissive launcher license cannot make a commercially restricted engine permissive.[^s6]

## Comparison with Dreamtime and evaluation

Dreamtime has the application domain that Pinokio lacks; Pinokio has a broader installation/catalog product that Dreamtime lacks. Remixfun could eventually be installable through such a launcher while still offering its own Tauri package and CLI/web modes. That is a distribution option, not a required architecture dependency.

Use it as an onboarding benchmark: install a relevant image/video app, restart it, update it, locate its model directory, and recover from a failed environment setup. Compare the clarity and amount of technical knowledge needed. Keep those results separate from whether the installed application can actually recover and remix a Civitai recipe.

## Source map and citations

[^s1]: **Launcher/script model and catalog policy** — [Pinned source](https://github.com/pinokiocomputer/pinokio/blob/0765ab1c24eee9bf7acf1618b94e1cfdc52886fc/README.md); [local README.md](../../../references/pinokio/README.md).

[^s2]: **Electron packaging and backend dependency** — [Pinned source](https://github.com/pinokiocomputer/pinokio/blob/0765ab1c24eee9bf7acf1618b94e1cfdc52886fc/package.json); [local package.json](../../../references/pinokio/package.json).

[^s3]: **Desktop main process** — [Pinned source](https://github.com/pinokiocomputer/pinokio/blob/0765ab1c24eee9bf7acf1618b94e1cfdc52886fc/main.js); [local main.js](../../../references/pinokio/main.js).

[^s4]: **Renderer bridge** — [Pinned source](https://github.com/pinokiocomputer/pinokio/blob/0765ab1c24eee9bf7acf1618b94e1cfdc52886fc/preload.js); [local preload.js](../../../references/pinokio/preload.js).

[^s5]: **Application update lifecycle** — [Pinned source](https://github.com/pinokiocomputer/pinokio/blob/0765ab1c24eee9bf7acf1618b94e1cfdc52886fc/updater.js); [local updater.js](../../../references/pinokio/updater.js).

[^s6]: **MIT source license** — [Pinned source](https://github.com/pinokiocomputer/pinokio/blob/0765ab1c24eee9bf7acf1618b94e1cfdc52886fc/LICENSE); [local LICENSE](../../../references/pinokio/LICENSE).
