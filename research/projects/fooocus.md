# Fooocus

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/lllyasviel/Fooocus) · [Local clone](../../../references/fooocus/) · [Raw snapshot](../evidence/fooocus.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2023-08-09 / 1,129 days (about 3.09 years) |
| Oldest reachable commit | 2023-08-09T11:44:17-07:00 — can include inherited history |
| Stars / forks / subscribers | 53,008 / 8,603 / 484 |
| Open issues + PRs | 313 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `ae05379cc97bc4361ec8b4ec90193dab21be763f` |
| HEAD commit | 2025-09-02T22:28:40+02:00 ci: bump actions/checkout from 4 to 5 (#4085) |
| Reachable commits, including merges | 1,144 |
| Historical distinct author names | 61 |
| Last 90 days: nonmerge commits / author names | 0 / 0 |
| Source license assessment | GPL-3.0 |
| Operating systems / hardware scope | Windows/Linux; Mac MPS guidance is explicitly less tested; model/hardware scope constrained |
| Distribution model | Gradio app with Windows archive and automatic preset-model downloads; source scripts |
| Fit for Remixfun | Simplicity/preset UX benchmark; limited SDXL-focused LTS, not a modern general video foundation |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| lllyasviel | 505 | — | — |
| lvmin | 327 | — | — |
| Manuel Schmid | 157 | — | — |
| MoonRide303 | 24 | — | — |
| rsl8 | 4 | — | — |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v2.5.5](https://github.com/lllyasviel/Fooocus/releases/tag/v2.5.5) | 2024-08-12T06:12:31Z | No attached artifacts in captured expansion; check external distribution |
| [v2.5.4](https://github.com/lllyasviel/Fooocus/releases/tag/v2.5.4) | 2024-08-11T20:49:46Z | No attached artifacts in captured expansion; check external distribution |
| [v2.5.3](https://github.com/lllyasviel/Fooocus/releases/tag/v2.5.3) | 2024-08-03T13:24:08Z | No attached artifacts in captured expansion; check external distribution |
| [v2.5.2](https://github.com/lllyasviel/Fooocus/releases/tag/v2.5.2) | 2024-07-27T21:30:40Z | No attached artifacts in captured expansion; check external distribution |
| [v2.5.1](https://github.com/lllyasviel/Fooocus/releases/tag/v2.5.1) | 2024-07-25T14:05:39Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

Fooocus is an important precedent for making local generation approachable through strong defaults and automatic model downloads. It is not a strong initial engine choice for the requested modern image/video application: the README explicitly declares limited SDXL-focused long-term support with bug fixes and no current plan to add newer architectures.[^s1]

## Architecture

Python/Gradio UI state feeds an asynchronous worker and a model pipeline. Presets/configuration determine models, styles, and generation behavior. Metadata parsing can recover settings, while the app also performs prompt processing and generation improvements intended to produce good results with fewer exposed controls.[^s2][^s3][^s4][^s5]

This is useful UX research: model presets and automatic setup can substantially reduce user effort. It also shows a conflict with strict source replay. Helpful prompt expansion or automatically selected defaults change the effective recipe unless recorded and explicitly enabled.

## Workflow coverage

Fooocus handles image generation, variations, inpainting/outpainting, references, and metadata-oriented reuse. It can download preset models, but that is not proof that it resolves every exact dependency of an arbitrary Civitai image. Its own conventions and enhancements make cross-engine fidelity a separate question.[^s1][^s4][^s5]

The reviewed application does not provide the requested modern first/last-frame video flow. A simplified image UI and a very large historical star count should not be used to infer a broader model roadmap that the project explicitly disclaims.

## Platforms, maintenance, and license

Windows has a downloadable archive; Linux uses source/scripts; Mac guidance is explicitly described as less intensively tested. Historical performance numbers in the README are not reproduced as current benchmark results. Modern hardware and models need fresh measurement.[^s1]

The repository has over 53k stars but no recent default-branch commits in this snapshot. Its explicit LTS statement is stronger evidence of scope than the activity count alone. The actual source license is **GPL-3.0**, not AGPL; the root text and GitHub classification agree.[^s6]

## Comparison with Dreamtime and evaluation

Dreamtime already covers more of the desired image/video breadth and offers explicit model-specific graph templates. Fooocus is useful for preset onboarding, progressive disclosure, and low-friction image editing, but replacing Dreamtime with it would narrow the product.

Evaluate whether a first-time user can download only the necessary preset models, understand generation defaults, and recover the effective expanded prompt/settings. Remixfun should borrow simplicity while preserving a strict mode where imported baseline settings are not silently enhanced.

## Source map and citations

[^s1]: **Product goals, explicit LTS status, presets, and OS caveats** — [Pinned source](https://github.com/lllyasviel/Fooocus/blob/ae05379cc97bc4361ec8b4ec90193dab21be763f/readme.md); [local readme.md](../../../references/fooocus/readme.md).

[^s2]: **Generation pipeline** — [Pinned source](https://github.com/lllyasviel/Fooocus/blob/ae05379cc97bc4361ec8b4ec90193dab21be763f/modules/default_pipeline.py); [local modules/default_pipeline.py](../../../references/fooocus/modules/default_pipeline.py).

[^s3]: **Task execution and UI coordination** — [Pinned source](https://github.com/lllyasviel/Fooocus/blob/ae05379cc97bc4361ec8b4ec90193dab21be763f/modules/async_worker.py); [local modules/async_worker.py](../../../references/fooocus/modules/async_worker.py).

[^s4]: **Metadata formats and reconstruction** — [Pinned source](https://github.com/lllyasviel/Fooocus/blob/ae05379cc97bc4361ec8b4ec90193dab21be763f/modules/meta_parser.py); [local modules/meta_parser.py](../../../references/fooocus/modules/meta_parser.py).

[^s5]: **Presets/model configuration** — [Pinned source](https://github.com/lllyasviel/Fooocus/blob/ae05379cc97bc4361ec8b4ec90193dab21be763f/modules/config.py); [local modules/config.py](../../../references/fooocus/modules/config.py).

[^s6]: **GPL source license** — [Pinned source](https://github.com/lllyasviel/Fooocus/blob/ae05379cc97bc4361ec8b4ec90193dab21be763f/LICENSE); [local LICENSE](../../../references/fooocus/LICENSE).
