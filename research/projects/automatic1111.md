# AUTOMATIC1111 Stable Diffusion WebUI

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/AUTOMATIC1111/stable-diffusion-webui) · [Local clone](../../../references/automatic1111/) · [Raw snapshot](../evidence/automatic1111.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2022-08-22 / 1,481 days (about 4.05 years) |
| Oldest reachable commit | 2022-08-22T17:05:27+03:00 — can include inherited history |
| Stars / forks / subscribers | 164,897 / 30,549 / 1,262 |
| Open issues + PRs | 2,506 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | master / `82a973c04367123ae98bd9abdf80d9eda9b910e2` |
| HEAD commit | 2024-07-27T15:49:39+03:00 changelog |
| Reachable commits, including merges | 7,689 |
| Historical distinct author names | 641 |
| Last 90 days: nonmerge commits / author names | 0 / 0 |
| Source license assessment | AGPL-3.0 |
| Operating systems / hardware scope | Windows/Linux; Apple Silicon instructions exist; hardware/extensions vary |
| Distribution model | Python/Gradio web app, launch scripts, Windows portable-style assets; extensions |
| Fit for Remixfun | Historical metadata/parameter-reuse baseline; major attention, limited recent default-branch activity |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| AUTOMATIC | 1228 | — | — |
| AUTOMATIC1111 | 666 | — | — |
| w-e-w | 311 | — | — |
| DepFA | 164 | — | — |
| Aarni Koskela | 155 | — | — |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [1.10.1](https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.10.1) | 2025-02-09T08:00:10Z | No attached artifacts in captured expansion; check external distribution |
| [1.10.0](https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.10.0) | 2025-01-30T13:38:59Z | `sd.webui-1.10.1-blackwell.7z` |
| [1.10.0-RC](https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.10.0-RC) | 2024-07-06T08:28:39Z | No attached artifacts in captured expansion; check external distribution |
| [1.9.4](https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.9.4) | 2024-05-28T18:35:52Z | No attached artifacts in captured expansion; check external distribution |
| [1.9.3](https://github.com/AUTOMATIC1111/stable-diffusion-webui/releases/tag/v1.9.3) | 2024-04-22T15:03:02Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

A1111 is the essential historical baseline for the requested workflow. It already supports reading PNG generation parameters, sending them to generation controls, seed reuse, variations, and parameter grids. Many Civitai images use its metadata conventions. Thus “import settings and tweak them” is a longstanding workflow, even if dependency recovery remains manual.[^s1][^s2][^s5]

## Architecture

The application combines a Python generation pipeline with a Gradio web UI, filesystem model inventory, extensions/scripts, and an API. Processing code assembles conditioning and sampling, then saves output parameters. UI transfer helpers map metadata values back into controls.[^s2][^s3][^s4][^s6]

This is a monolithic inference application rather than a frontend over Comfy. Its prompt-weighting, sampler, RNG, hires, refiner, and extension semantics are part of the recipe. Copying displayed parameters into another engine is not necessarily an equivalent replay.

## Exact workflow coverage

For an A1111-native output with retained metadata and matching local environment, PNG Info and parameter reuse provide a strong starting point. XY/Z grids already implement controlled comparisons. That means Remixfun's experiments should improve provenance and usability, not imply parameter sweeps are novel.[^s1][^s2][^s5]

The default image import does not establish a complete transaction that resolves and verifies every missing checkpoint, LoRA, VAE, embedding, and extension from a Civitai source. Extensions can add pieces, but extension capability should be credited individually rather than assumed in the base product.

Video generation generally requires other extensions/workflows rather than being the central first/last-frame/loop product in the inspected base repository. Image loopback is repeated image-to-image processing, not necessarily temporal video generation.[^s1][^s3]

## Popularity, releases, and license

This repository has the largest accumulated star count in the survey. Its inspected default branch has no commits in the latest 90-day window and an older HEAD. Release-feed updated dates can be newer than that HEAD, so the report does not treat the commit date as the last activity anywhere in the project.

The large historical contributor count includes name aliases and many years of community work. It measures ecosystem history, not a current team of hundreds. Source is AGPL-3.0, with separate model and extension terms.[^s7]

## Comparison with Dreamtime and evaluation

Dreamtime should preserve A1111 metadata as a first-class foreign format, including unrecognized fields, rather than discard everything outside its generator controls. A genuine A1111 baseline is also useful for measuring how much cross-engine reconstruction differs.

Use an A1111-native fixture with known hires/refiner/LoRA settings. Reproduce it in the original environment, then import it into Dreamtime and other competitors. Record which changes come from missing metadata versus differing engine semantics. This is a more informative fidelity benchmark than comparing unrelated prompt examples.

## Source map and citations

[^s1]: **PNG Info reuse, XY plots, installation, and features** — [Pinned source](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/82a973c04367123ae98bd9abdf80d9eda9b910e2/README.md); [local README.md](../../../references/automatic1111/README.md).

[^s2]: **Metadata parsing and parameter transfer** — [Pinned source](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/82a973c04367123ae98bd9abdf80d9eda9b910e2/modules/infotext_utils.py); [local modules/infotext_utils.py](../../../references/automatic1111/modules/infotext_utils.py).

[^s3]: **Generation pipeline and saved parameters** — [Pinned source](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/82a973c04367123ae98bd9abdf80d9eda9b910e2/modules/processing.py); [local modules/processing.py](../../../references/automatic1111/modules/processing.py).

[^s4]: **Checkpoint inventory and loading** — [Pinned source](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/82a973c04367123ae98bd9abdf80d9eda9b910e2/modules/sd_models.py); [local modules/sd_models.py](../../../references/automatic1111/modules/sd_models.py).

[^s5]: **Controlled parameter grid** — [Pinned source](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/82a973c04367123ae98bd9abdf80d9eda9b910e2/scripts/xyz_grid.py); [local scripts/xyz_grid.py](../../../references/automatic1111/scripts/xyz_grid.py).

[^s6]: **Automation API** — [Pinned source](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/82a973c04367123ae98bd9abdf80d9eda9b910e2/modules/api/api.py); [local modules/api/api.py](../../../references/automatic1111/modules/api/api.py).

[^s7]: **AGPL license** — [Pinned source](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/82a973c04367123ae98bd9abdf80d9eda9b910e2/LICENSE.txt); [local LICENSE.txt](../../../references/automatic1111/LICENSE.txt).
