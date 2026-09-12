# Krita AI Diffusion

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/Acly/krita-ai-diffusion) · [Local clone](../../../references/krita-ai-diffusion/) · [Raw snapshot](../evidence/krita-ai-diffusion.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:58:15.967620+00:00 |
| Repository creation / age | 2023-09-01 / 1,106 days (about 3.03 years) |
| Oldest reachable commit | 2023-06-07T19:36:54+02:00 — can include inherited history |
| Stars / forks / subscribers | 10,571 / 625 / 82 |
| Open issues + PRs | 100 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `dda58d1c63e361207ccec085efbc34dbd32f1654` |
| HEAD commit | 2026-08-23T13:02:28+02:00 CI: set Qt to use offscreen platform to avoid libEGL load issue |
| Reachable commits, including merges | 1,778 |
| Historical distinct author names | 51 |
| Last 90 days: nonmerge commits / author names | 40 / 6 |
| Source license assessment | GPL-3.0 |
| Operating systems / hardware scope | Krita on Windows/Linux/macOS; managed local or remote Comfy; model-dependent GPU support |
| Distribution model | Krita plugin ZIP; local server installer or optional cloud connection |
| Fit for Remixfun | Strong visual-remix and managed Comfy reference; different primary interaction from recipe replay |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Acly | 1618 | Acly | 28 |
| Danamir | 18 | Sen-sou | 8 |
| Drakosha405 | 13 | Fumiaki MATSUSHIMA | 1 |
| FeepingCreature | 11 | amiiari | 1 |
| Sen-sou | 11 | fukc-gihtub | 1 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [Version 1.53.0](https://github.com/Acly/krita-ai-diffusion/releases/tag/v1.53.0) | 2026-08-22T19:38:06Z | `krita_ai_diffusion-1.53.0.zip` |
| [Version 1.52.1](https://github.com/Acly/krita-ai-diffusion/releases/tag/v1.52.1) | 2026-06-30T12:39:14Z | `krita_ai_diffusion-1.52.1.zip` |
| [Version 1.52.0](https://github.com/Acly/krita-ai-diffusion/releases/tag/v1.52.0) | 2026-06-28T12:46:37Z | `krita_ai_diffusion-1.52.0.zip` |
| [Version 1.51.1](https://github.com/Acly/krita-ai-diffusion/releases/tag/v1.51.1) | 2026-06-05T20:49:34Z | `krita_ai_diffusion-1.51.1.zip` |
| [Version 1.51.0](https://github.com/Acly/krita-ai-diffusion/releases/tag/v1.51.0) | 2026-05-31T13:34:45Z | `krita_ai_diffusion-1.51.0.zip` |

## Assessment

Krita AI Diffusion is a successful example of hiding much of Comfy behind a task-specific interface. It integrates generation into an existing painting application: selections, layers, live painting, references, inpainting, upscaling, and history. It competes for the broader idea of remixing images, although its core is visual editing rather than recovering someone else's generation recipe.[^s1]

Its roughly 10.6k stars, multi-year history, regular plugin releases, and continuing contributions make it a stronger adoption signal than most tiny workflow wrappers. The plugin's stars are not the user count of Krita or its optional cloud service.

## Architecture

Python code runs inside Krita's extension environment and its Qt UI. Document/layer abstractions translate painting context into generation plans; the backend layer builds Comfy workflows, manages connections, and receives job output. Results can be integrated back into the document rather than merely appended to a standalone gallery.[^s2][^s3][^s6][^s7]

The local server installer and resource catalog manage required Comfy components. OS/GPU-specific dependency profiles are explicit files, including Windows/Linux accelerator choices and macOS MPS/CPU paths. This is a concrete reference for the runtime profile work that Desktop Release Kit does not supply.[^s4][^s5][^s8]

The application can connect to an existing or remote Comfy server, and also offers a cloud path. Backend abstraction is therefore meaningful rather than an unused interface invented for future portability.[^s1][^s2]

## Workflow coverage and differences

Importing an image as canvas content, making controlled local edits, and retaining generation history are well aligned with creative remixing. Region prompts and references give the user strong visual control. They do not establish what model versions, sampler pipeline, and hidden stages created the imported source.[^s1][^s3]

The survey did not establish a Civitai-URL → exact missing dependency plan → recovered baseline flow. It also did not establish the requested first/last-frame/loop video journey as the plugin's main user path. A link labeled “Video” in a README can be a product demonstration, not evidence of video-generation support; the feature list and actual workflow code must be read carefully.[^s1][^s3]

Thus this is a serious adjacent alternative, not a direct replacement for the complete recipe-and-motion product. It may be the better tool for users who primarily want to change objects or composition in an existing image, and Remixfun should avoid forcing such tasks into parameter sweeps when canvas editing is more natural.

## Distribution, license, and maintenance

Releases ship plugin ZIPs that require Krita; they are not standalone image-generator installers. The plugin can install a local inference environment, while the host application's installation/update process remains separate. This separation is analogous to a desktop shell managing an optional engine, but not equivalent to an optional web frontend.[^s1][^s4]

The GPL-3.0 source license and third-party model/node terms must be considered separately. Maintainer concentration remains visible despite external contributors; current activity is stronger than a stale README alone.[^s9]

## Comparison with Dreamtime and evaluation

Dreamtime's React/FastAPI application is more suitable for a standalone import/recipe library and headless API. Krita provides a much deeper visual editing host and a useful reference for managed-server requirements, resource installation, job state, and returning generated artifacts to their source context.

Evaluate it for two questions: how much of a user's intended remix is better expressed with masks/layers, and how clearly does it explain/install missing Comfy requirements? Use the same source image as the recipe tools, but score visual editing separately from deterministic reconstruction. Treat its runtime installer and capability profiles as lessons for Remixfun's onboarding.

## Source map and citations

[^s1]: **User goals, features, and installation** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/blob/dda58d1c63e361207ccec085efbc34dbd32f1654/README.md); [local README.md](../../../references/krita-ai-diffusion/README.md).

[^s2]: **Comfy connection** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/blob/dda58d1c63e361207ccec085efbc34dbd32f1654/ai_diffusion/backend/comfy_client.py); [local ai_diffusion/backend/comfy_client.py](../../../references/krita-ai-diffusion/ai_diffusion/backend/comfy_client.py).

[^s3]: **Generation planning** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/blob/dda58d1c63e361207ccec085efbc34dbd32f1654/ai_diffusion/backend/workflow.py); [local ai_diffusion/backend/workflow.py](../../../references/krita-ai-diffusion/ai_diffusion/backend/workflow.py).

[^s4]: **Managed runtime setup** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/blob/dda58d1c63e361207ccec085efbc34dbd32f1654/ai_diffusion/backend/server.py); [local ai_diffusion/backend/server.py](../../../references/krita-ai-diffusion/ai_diffusion/backend/server.py).

[^s5]: **Required model/node resources** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/blob/dda58d1c63e361207ccec085efbc34dbd32f1654/ai_diffusion/backend/resources.py); [local ai_diffusion/backend/resources.py](../../../references/krita-ai-diffusion/ai_diffusion/backend/resources.py).

[^s6]: **Job state** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/blob/dda58d1c63e361207ccec085efbc34dbd32f1654/ai_diffusion/model/jobs.py); [local ai_diffusion/model/jobs.py](../../../references/krita-ai-diffusion/ai_diffusion/model/jobs.py).

[^s7]: **Document-associated persistence** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/blob/dda58d1c63e361207ccec085efbc34dbd32f1654/ai_diffusion/persistence.py); [local ai_diffusion/persistence.py](../../../references/krita-ai-diffusion/ai_diffusion/persistence.py).

[^s8]: **OS/GPU dependency profiles** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/tree/dda58d1c63e361207ccec085efbc34dbd32f1654/ai_diffusion/backend/requirements); [local ai_diffusion/backend/requirements](../../../references/krita-ai-diffusion/ai_diffusion/backend/requirements).

[^s9]: **GPL source license** — [Pinned source](https://github.com/Acly/krita-ai-diffusion/blob/dda58d1c63e361207ccec085efbc34dbd32f1654/LICENSE); [local LICENSE](../../../references/krita-ai-diffusion/LICENSE).
