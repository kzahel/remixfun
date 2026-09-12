# SDFX

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/sdfxai/sdfx) · [Local clone](../../../references/sdfx/) · [Raw snapshot](../evidence/sdfx.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2024-04-09 / 886 days (about 2.43 years) |
| Oldest reachable commit | 2024-04-09T07:02:11+04:00 — can include inherited history |
| Stars / forks / subscribers | 445 / 32 / 8 |
| Open issues + PRs | 21 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `f63c7b85ab2e544b3b4636988c214d04491f7dee` |
| HEAD commit | 2025-05-01T07:12:27+04:00 add IPAdapterAvanced weight widget default |
| Reachable commits, including merges | 128 |
| Historical distinct author names | 5 |
| Last 90 days: nonmerge commits / author names | 0 / 0 |
| Source license assessment | AGPL-3.0 |
| Operating systems / hardware scope | Web/Electron builds for Windows/Linux/macOS are described; current binary delivery unestablished |
| Distribution model | Source setup scripts; Vue/Vite web build and Electron build; no release feed captured |
| Fit for Remixfun | Useful declarative workflow/UI architecture; stale default branch makes it a poor primary dependency |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| dmx | 101 | — | — |
| spartanz51 | 12 | — | — |
| kevin96666 | 3 | — | — |
| Thibaud Arnault | 1 | — | — |
| kevin codfert | 1 | — | — |

### Release evidence

No GitHub release entries were captured. This does not exclude registry packages, git installation, external installers, or a private release process.

## Assessment

SDFX is another explicit precedent for turning Comfy workflows into application-like interfaces. It is useful architecture research but a weak default foundation today: the inspected default branch has not changed since May 2025 and no GitHub release entries were captured.[^s1]

## Architecture

The code under `src` uses Vue, Pinia, Vite, and an Electron build path. Separate web/app Vite configurations allow browser and native-shell presentations. Graph/application views and stores manage enriched workflow state. Setup scripts arrange the Comfy backend and bridge integration.[^s2][^s3][^s4][^s5][^s6]

The central idea is a workflow with presentation metadata: controls map to graph widgets and are arranged into UI regions. That is directly relevant to Remixfun presets, but it creates a compatibility layer that must survive graph/node schema changes. A generic mapping engine can become a large project of its own.

## Target workflow coverage

Prepared graph → simplified app → generation is its focus. The review did not establish automatic Civitai-image recipe resolution, a content-verified dependency plan, or controlled baseline lineage. Compatibility claims about Comfy workflows should be checked against current node packs rather than accepted as universal.[^s1][^s3]

The application-creator/editor scope includes work-in-progress language in the project description. Avoid presenting an architectural concept or internal screen as a fully supported end-user feature. Likewise, native build scripts are not evidence of current downloadable signed installers.

## OS, releases, and licensing

Web and Electron builds aim at cross-platform use; actual model inference remains a Comfy responsibility. The old Node/Vue/Electron dependency era and inactive default branch imply upgrade work before using it as a current shipping base. No build or installer compatibility test was run.[^s2][^s5]

The source is AGPL-3.0. Its historical author count is small and concentrated. No evidence was obtained for active users, current downloads, or a supported release cadence.[^s7]

## Comparison with Dreamtime and evaluation

Dreamtime has current task-specific image/video code in a familiar React/Python stack. Replacing it with SDFX would trade that investment for a generic but older frontend. The useful transferable concept is a versioned preset schema containing input controls, graph bindings, model requirements, and output types.

Compare SDFX's mapping approach with ViewComfy and Comfy App Mode using one representative workflow. The outcome should inform how much generic UI metadata Remixfun needs. It should not lead to inheriting an entire dormant application simply because it once pursued a similar interface idea.

## Source map and citations

[^s1]: **Workflow app concept and maturity** — [Pinned source](https://github.com/sdfxai/sdfx/blob/f63c7b85ab2e544b3b4636988c214d04491f7dee/README.md); [local README.md](../../../references/sdfx/README.md).

[^s2]: **Vue/Pinia/Electron stack and build modes** — [Pinned source](https://github.com/sdfxai/sdfx/blob/f63c7b85ab2e544b3b4636988c214d04491f7dee/src/package.json); [local src/package.json](../../../references/sdfx/src/package.json).

[^s3]: **Graph/application views** — [Pinned source](https://github.com/sdfxai/sdfx/tree/f63c7b85ab2e544b3b4636988c214d04491f7dee/src/src/views/OpenGraph); [local src/src/views/OpenGraph](../../../references/sdfx/src/src/views/OpenGraph).

[^s4]: **Workflow and model state** — [Pinned source](https://github.com/sdfxai/sdfx/tree/f63c7b85ab2e544b3b4636988c214d04491f7dee/src/src/stores); [local src/src/stores](../../../references/sdfx/src/src/stores).

[^s5]: **Native shell** — [Pinned source](https://github.com/sdfxai/sdfx/blob/f63c7b85ab2e544b3b4636988c214d04491f7dee/src/electron/main/index.ts); [local src/electron/main/index.ts](../../../references/sdfx/src/electron/main/index.ts).

[^s6]: **Backend setup** — [Pinned source](https://github.com/sdfxai/sdfx/blob/f63c7b85ab2e544b3b4636988c214d04491f7dee/setup.py); [local setup.py](../../../references/sdfx/setup.py).

[^s7]: **AGPL source license** — [Pinned source](https://github.com/sdfxai/sdfx/blob/f63c7b85ab2e544b3b4636988c214d04491f7dee/LICENSE); [local LICENSE](../../../references/sdfx/LICENSE).
