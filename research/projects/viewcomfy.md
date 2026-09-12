# ViewComfy

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/ViewComfy/ViewComfy) · [Local clone](../../../references/viewcomfy/) · [Raw snapshot](../evidence/viewcomfy.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2024-09-27 / 714 days (about 1.95 years) |
| Oldest reachable commit | 2024-09-12T16:55:53-03:00 — can include inherited history |
| Stars / forks / subscribers | 668 / 85 / 8 |
| Open issues + PRs | 12 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `fc0ba28a745231e98fd21688cdbb392800a8eb7b` |
| HEAD commit | 2026-03-19T12:12:27-03:00 Merge pull request #231 from ViewComfy/sso |
| Reachable commits, including merges | 608 |
| Historical distinct author names | 3 |
| Last 90 days: nonmerge commits / author names | 0 / 0 |
| Source license assessment | AGPL-3.0 |
| Operating systems / hardware scope | Node/browser app on Windows/Linux/macOS; Comfy can be local or remote |
| Distribution model | Next.js web app, source releases, separately offered hosted service |
| Fit for Remixfun | Prepared Comfy workflow → approachable form; not a foreign recipe resolver |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Jean Delannoy | 295 | — | — |
| GBieler | 146 | — | — |
| Veka | 5 | — | — |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v.0.3.23](https://github.com/ViewComfy/ViewComfy/releases/tag/v.0.3.23) | 2026-01-08T15:02:37Z | No attached artifacts in captured expansion; check external distribution |
| [v.0.3.22](https://github.com/ViewComfy/ViewComfy/releases/tag/v.0.3.22) | 2025-09-02T17:24:23Z | No attached artifacts in captured expansion; check external distribution |
| [v.0.3.21](https://github.com/ViewComfy/ViewComfy/releases/tag/v.0.3.21) | 2025-08-29T12:38:43Z | No attached artifacts in captured expansion; check external distribution |
| [v.0.3.20](https://github.com/ViewComfy/ViewComfy/releases/tag/v.0.3.20) | 2025-08-28T22:22:14Z | No attached artifacts in captured expansion; check external distribution |
| [v.0.3.19](https://github.com/ViewComfy/ViewComfy/releases/tag/v.0.3.19) | 2025-07-31T18:35:38Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

ViewComfy is a direct precedent for making a Comfy workflow usable through a conventional web form. It is relevant to preset presentation and sharing, but it begins with an authored workflow rather than a foreign image whose recipe needs to be recovered.[^s1][^s5]

## Architecture

The application uses Next.js, React, TypeScript, form/schema tooling, and browser state. Server routes bridge requests and media to Comfy or the separately offered service. The editor maps exposed controls to a workflow, and the playground lets users run it and view outputs.[^s2][^s3][^s4][^s5][^s6]

This places presentation/configuration above the graph engine, much like the proposed Remixfun preset layer. It introduces a Node application runtime, whereas Dreamtime already has a Python application service and a static Vite frontend. Adopting it wholesale would add or replace an application layer rather than merely skinning Dreamtime.

## Workflow coverage

It is suitable for a prepared image/video workflow with a few inputs and useful outputs. Form generation does not reconstruct the source graph from incomplete Civitai metadata, prove exact model identity, or preserve a controlled baseline with declared changes. Those remain surrounding product functions.[^s1][^s3][^s5]

The hosted offering advertises additional capabilities; they should not automatically be credited to the self-hosted source. Inspect the actual local paths for authentication, history, storage, sharing, and billing rather than treating one marketing feature list as the open-source product contract.[^s1][^s4]

## Distribution, maintenance, and license

The repository ships source releases rather than native desktop installers in the captured feed. A browser frontend can run on all three target operating systems, while the separate Comfy runtime and model nodes determine GPU compatibility. AGPL-3.0 governs the source.[^s2][^s7]

No default-branch commits appear in the captured 90-day window. That is an observation about this open repository, not proof the company, hosted service, or private development has stopped. Historical activity is concentrated among a few authors.

## Comparison with Dreamtime and evaluation

Dreamtime's hand-built generator pages are less generic but already support the user's domain. ViewComfy is useful for understanding declarative workflow-to-control mapping, input validation, and media output rendering. Remixfun can adopt the pattern without becoming a general app-builder product.

Test one Dreamtime image graph and one first/last-frame video graph through ViewComfy. Count configuration effort and note what happens when node IDs, models, or required inputs change. Compare with Comfy's official App Mode before investing in a competing generic workflow form system.

## Source map and citations

[^s1]: **Local versus hosted scope** — [Pinned source](https://github.com/ViewComfy/ViewComfy/blob/fc0ba28a745231e98fd21688cdbb392800a8eb7b/README.md); [local README.md](../../../references/viewcomfy/README.md).

[^s2]: **Next/React/TypeScript stack** — [Pinned source](https://github.com/ViewComfy/ViewComfy/blob/fc0ba28a745231e98fd21688cdbb392800a8eb7b/package.json); [local package.json](../../../references/viewcomfy/package.json).

[^s3]: **Comfy service adapter** — [Pinned source](https://github.com/ViewComfy/ViewComfy/blob/fc0ba28a745231e98fd21688cdbb392800a8eb7b/app/services/comfyui-service.ts); [local app/services/comfyui-service.ts](../../../references/viewcomfy/app/services/comfyui-service.ts).

[^s4]: **Server API/media routes** — [Pinned source](https://github.com/ViewComfy/ViewComfy/tree/fc0ba28a745231e98fd21688cdbb392800a8eb7b/app/api); [local app/api](../../../references/viewcomfy/app/api).

[^s5]: **Workflow form editor** — [Pinned source](https://github.com/ViewComfy/ViewComfy/tree/fc0ba28a745231e98fd21688cdbb392800a8eb7b/app/editor); [local app/editor](../../../references/viewcomfy/app/editor).

[^s6]: **Playground/application structure** — [Pinned source](https://github.com/ViewComfy/ViewComfy/tree/fc0ba28a745231e98fd21688cdbb392800a8eb7b/app); [local app](../../../references/viewcomfy/app).

[^s7]: **AGPL source license** — [Pinned source](https://github.com/ViewComfy/ViewComfy/blob/fc0ba28a745231e98fd21688cdbb392800a8eb7b/LICENSE); [local LICENSE](../../../references/viewcomfy/LICENSE).
