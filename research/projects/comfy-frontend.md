# ComfyUI official frontend / App Mode

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/Comfy-Org/ComfyUI_frontend) · [Local clone](../../../references/comfy-frontend/) · [Raw snapshot](../evidence/comfy-frontend.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:59:46.075400+00:00 |
| Repository creation / age | 2024-06-13 / 821 days (about 2.25 years) |
| Oldest reachable commit | 2013-09-26T19:40:42+02:00 — can include inherited history |
| Stars / forks / subscribers | 2,006 / 696 / 22 |
| Open issues + PRs | 2,742 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `014bafe62e402acaf6a5729d6c8924ad07e44a5a` |
| HEAD commit | 2026-09-12T06:25:04Z test(widgets): an emptied promoted text widget stays empty across a round-trip (#17524) |
| Reachable commits, including merges | 9,847 |
| Historical distinct author names | 250 |
| Last 90 days: nonmerge commits / author names | 1,588 / 61 |
| Source license assessment | GPL-3.0-only in package manifest |
| Operating systems / hardware scope | Browser frontend; runs with Comfy on supported host OSes; desktop/cloud builds differ |
| Distribution model | Versioned frontend packages/releases consumed by Comfy; no independent GPU runtime |
| Fit for Remixfun | Direct baseline for simplified workflow forms; App Mode removes the node-editor requirement |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Chenlei Hu | 1987 | Christian Byrne | 440 |
| Christian Byrne | 1644 | Alexander Brown | 162 |
| filtered | 693 | Dante | 133 |
| Comfy Org PR Bot | 614 | Comfy Org PR Bot | 80 |
| Alexander Brown | 542 | claude[bot] | 79 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v1.55.5](https://github.com/Comfy-Org/ComfyUI_frontend/releases/tag/v1.55.5) | 2026-09-12T01:42:52Z | `dist-desktop.zip`, `dist.zip` |
| [cloud/v1.54.9: [backport cloud/1.54] assetDeletionEnabled only changes message (#17377)](https://github.com/Comfy-Org/ComfyUI_frontend/releases/tag/cloud%2Fv1.54.9) | 2026-09-10T21:55:20Z | No attached artifacts in captured expansion; check external distribution |
| [cloud/v1.54.8](https://github.com/Comfy-Org/ComfyUI_frontend/releases/tag/cloud%2Fv1.54.8) | 2026-09-10T05:50:31Z | No attached artifacts in captured expansion; check external distribution |
| [v1.55.2](https://github.com/Comfy-Org/ComfyUI_frontend/releases/tag/v1.55.2) | 2026-09-09T03:43:43Z | `dist-desktop.zip`, `dist.zip` |
| [cloud/v1.54.7](https://github.com/Comfy-Org/ComfyUI_frontend/releases/tag/cloud%2Fv1.54.7) | 2026-09-08T21:27:09Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

The official frontend materially changes the novelty argument. **App Mode already turns a Comfy workflow into a simpler input/output interface**, with selected controls, outputs, preview, and a default app view. Remixfun cannot claim novelty merely for replacing a node graph with a form.[^s2][^s4][^s8]

This repository should be evaluated separately from the Python engine and Electron desktop manager. Their versions, licenses, contributors, and release surfaces differ, even though users experience them together.

## Architecture

The source is a Vue/TypeScript frontend using Pinia and Vite, with graph editing/integration, workflow management, UI state, and separate distribution modes. The package has desktop and cloud build variants. Its job is to present/control graphs and communicate with the backend, not perform inference itself.[^s1][^s5][^s6]

App Mode stores selected inputs and outputs as references into workflow graph entities. It must resolve node/widget identifiers, handle subgraphs, prune invalid references, and keep the app presentation synchronized as the graph changes. This exposes a subtle maintenance cost of generic workflow forms: UI metadata is coupled to evolving graph structure.[^s2][^s3][^s4]

Dreamtime takes a different approach: purpose-built React pages call known model adapters. That is less generic, but it gives the product a stronger task model and fewer arbitrary-widget compatibility obligations.

## What App Mode does and does not establish

The official guide describes a builder sequence for inputs, outputs, preview, and default view, followed by ordinary run/cancel and output interactions. It is intended to make a prepared workflow usable without editing nodes. The same guide distinguishes cloud-only share links from local workflow saving.[^s8]

App Mode starts with a workflow. It does not by itself prove that a Civitai image without its graph can be reconstructed, every missing model identified by exact hash/version, or a source baseline compared through controlled experiments. Those are separate functions that a plugin or Remixfun could add.

For video presets, however, it already provides much of the desired presentation mechanism. A well-authored first/last-frame graph could be packaged as an app-shaped workflow. The build-versus-integrate question should include whether that existing mode plus a focused import/lineage extension is sufficient.

## Distribution, license, and maintenance

The package manifest records GPL-3.0-only. Frontend releases are normally consumed alongside Comfy rather than downloaded as a standalone native generator. Cloud build capabilities should not automatically be attributed to the local build.[^s1][^s7]

Active frontend development brings improvements but also potential extension/API churn. A Remixfun interface using Comfy's server API can reduce its exposure to internal frontend changes; a panel extension gains host integration while accepting that coupling. This is an architecture tradeoff, not a universal preference for one route.

## Comparison with Dreamtime and evaluation

Dreamtime's standalone image/video screens provide application-specific interactions outside Comfy's editor. Compare those screens against App Mode using the exact same underlying graph before building more UI. If App Mode already presents the important controls well, the strongest custom work is source recovery, dependency explanation, experiments, and lineage.

Test node renames, workflow updates, missing models, file inputs, video outputs, and switching between app and graph views. Keep sharing tests separate for local files and cloud URLs. The evaluation should determine whether an independent product materially shortens the target task rather than simply reskinning a workflow form.

## Source map and citations

[^s1]: **Frontend build/distribution stack and license** — [Pinned source](https://github.com/Comfy-Org/ComfyUI_frontend/blob/014bafe62e402acaf6a5729d6c8924ad07e44a5a/package.json); [local package.json](../../../references/comfy-frontend/package.json).

[^s2]: **App input/output state and graph references** — [Pinned source](https://github.com/Comfy-Org/ComfyUI_frontend/blob/014bafe62e402acaf6a5729d6c8924ad07e44a5a/src/stores/appModeStore.ts); [local src/stores/appModeStore.ts](../../../references/comfy-frontend/src/stores/appModeStore.ts).

[^s3]: **Mode lifecycle** — [Pinned source](https://github.com/Comfy-Org/ComfyUI_frontend/blob/014bafe62e402acaf6a5729d6c8924ad07e44a5a/src/composables/useAppMode.ts); [local src/composables/useAppMode.ts](../../../references/comfy-frontend/src/composables/useAppMode.ts).

[^s4]: **Workflow-to-app builder UI** — [Pinned source](https://github.com/Comfy-Org/ComfyUI_frontend/tree/014bafe62e402acaf6a5729d6c8924ad07e44a5a/src/components/builder); [local src/components/builder](../../../references/comfy-frontend/src/components/builder).

[^s5]: **Workflow persistence and management** — [Pinned source](https://github.com/Comfy-Org/ComfyUI_frontend/tree/014bafe62e402acaf6a5729d6c8924ad07e44a5a/src/platform/workflow/management); [local src/platform/workflow/management](../../../references/comfy-frontend/src/platform/workflow/management).

[^s6]: **Graph/API integration** — [Pinned source](https://github.com/Comfy-Org/ComfyUI_frontend/tree/014bafe62e402acaf6a5729d6c8924ad07e44a5a/src/scripts); [local src/scripts](../../../references/comfy-frontend/src/scripts).

[^s7]: **GPL source text** — [Pinned source](https://github.com/Comfy-Org/ComfyUI_frontend/blob/014bafe62e402acaf6a5729d6c8924ad07e44a5a/LICENSE); [local LICENSE](../../../references/comfy-frontend/LICENSE).

[^s8]: [Official App Mode guide and cloud-only sharing distinction](https://docs.comfy.org/interface/app-mode), accessed 2026-09-12.
