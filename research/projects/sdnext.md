# SD.Next

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/vladmandic/sdnext) · [Local clone](../../../references/sdnext/) · [Raw snapshot](../evidence/sdnext.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:58:15.967620+00:00 |
| Repository creation / age | 2022-12-24 / 1,357 days (about 3.72 years) |
| Oldest reachable commit | 2022-08-22T17:05:27+03:00 — can include inherited history |
| Stars / forks / subscribers | 7,338 / 583 / 65 |
| Open issues + PRs | 60 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | master / `684940e015911efab2911667231946d91fef9f50` |
| HEAD commit | 2026-08-26T11:17:43+02:00 Merge pull request #5062 from vladmandic/dev |
| Reachable commits, including merges | 14,447 |
| Historical distinct author names | 525 |
| Last 90 days: nonmerge commits / author names | 651 / 13 |
| Source license assessment | Apache-2.0 at inspected root; inherited/third-party files need their own review |
| Operating systems / hardware scope | Windows/Linux/macOS; CUDA, ROCm/ZLUDA, Intel, DirectML/OpenVINO, MPS paths vary by feature |
| Distribution model | Web server + Python installer; dated releases; Windows launcher referenced separately |
| Fit for Remixfun | Major all-in-one alternative: metadata, Civitai downloads, image/video generation, broad hardware |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Vladimir Mandic | 5093 | Vladimir Mandic | 271 |
| Disty0 | 1404 | CalamitousFelicitousness | 209 |
| AUTOMATIC | 1032 | Disty0 | 91 |
| CalamitousFelicitousness | 598 | Dity0 | 22 |
| vladmandic | 570 | Claude | 13 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [2026-07-14: Merge pull request #4994 from vladmandic/dev](https://github.com/vladmandic/sdnext/releases/tag/2026-07-14) | 2026-07-14T08:24:45Z | No attached artifacts in captured expansion; check external distribution |
| [2026-07-07: Merge pull request #4983 from vladmandic/dev](https://github.com/vladmandic/sdnext/releases/tag/2026-07-07) | 2026-07-07T07:19:56Z | No attached artifacts in captured expansion; check external distribution |
| [2026-06-16: Merge pull request #4937 from vladmandic/dev](https://github.com/vladmandic/sdnext/releases/tag/2026-06-16) | 2026-06-16T10:17:57Z | No attached artifacts in captured expansion; check external distribution |
| [2026-05-14: fix hidream-o1 loader](https://github.com/vladmandic/sdnext/releases/tag/2026-05-14) | 2026-05-14T19:09:50Z | No attached artifacts in captured expansion; check external distribution |
| [2026-04-29: Merge pull request #4814 from vladmandic/dev](https://github.com/vladmandic/sdnext/releases/tag/2026-04-29) | 2026-04-29T05:13:43Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

SD.Next belongs in the primary comparison, not a footnote. It combines image/video generation, Civitai discovery/downloads, foreign metadata handling, model quantization/offload, and a broad hardware matrix. It is also actively developed in this snapshot. A survey limited to A1111, Forge, and Comfy wrappers would miss an important existing alternative.[^s1]

Its history begins as a WebUI lineage, so historical contributor totals include inherited work. Recent authorship is a more useful signal of current maintenance: several named contributors account for substantial work in the captured 90-day window, though aliases and automated authors remain possible.

## Architecture

SD.Next is a Python server and Gradio-oriented web interface, with installation/environment detection in `installer.py`, common parameter and model state, a Diffusers execution layer, API routes, and dedicated image/video subsystems. It is an alternative runtime/application, not an ordinary Comfy frontend.[^s2][^s3][^s8][^s9]

The video subsystem separates model definitions, loading, execution, cache, save/codec handling, and UI. Civitai integration is similarly divided into API/client, model metadata, browsing, file management, and download code. This modularization is more useful to Remixfun than copying the entire application state model.[^s6][^s7][^s8]

## Import and model resolution

Image metadata readers and infotext transfer provide a route for restoring source settings. The Civitai metadata service looks up local files by hash, stores provider metadata, identifies available versions, and can backfill preview generation parameters. That is a stronger connection between local inventory and source examples than a simple directory picker.[^s4][^s5][^s6]

The download manager tracks queued/downloading/verifying/completed/failed/cancelled states, carries expected hashes and version IDs, and has explicit partial-file/resume machinery. This is a concrete reference for improving Dreamtime's restart-from-zero downloader and post-hoc hash recording.[^s7]

The remaining question is the connection between these capabilities: does a foreign image import reliably create one exact dependency plan and restore every LoRA weight, VAE, hires/refiner stage, and sampler condition? The inspected metadata and download subsystems do not alone prove that end-to-end guarantee. Test it rather than inferring it from the breadth of the browser.

## Remix and motion

The application offers image-to-image, controlled image processing, reference models, LoRAs, video generation, and interpolation-related tools. It may already satisfy much of a user's practical “reuse this, tweak it, animate it” need. Its broad UI and runtime-specific sampler/conditioning semantics remain relevant when the source image came from another engine.[^s1][^s3][^s8]

Remixfun cannot distinguish itself simply by supporting more current model families or automating downloads. A clearer opportunity is an understandable source/baseline/variant record with explicit approximation states and a curated motion handoff.

## Platforms, releases, and licensing

The README lists extensive GPU/platform combinations and Docker recipes. These are supported paths, not a guarantee every video model/quantization kernel works across every accelerator. Windows installer/launcher distribution is referenced separately from the inspected main repository; the captured release-feed entries are dated source releases.[^s1][^s2]

The root license is Apache-2.0. Because the project has inherited code and bundled third-party components, that label should not substitute for a file-level redistribution inventory if implementation is copied.[^s10]

## Comparison with Dreamtime and evaluation

Dreamtime has the more direct architectural fit for Remixfun's React/FastAPI/Comfy plan. SD.Next has a broader working generation product, richer Civitai file management, and hardware setup expertise. Adopting it as the engine would require translating Dreamtime graph presets and accepting a different inference stack.

Evaluate SD.Next alongside Swarm and Matrix with an identical imported recipe. Check the exact graph/pipeline settings after import, interrupted download recovery, and one-axis replay. Then try video from the selected image. If it handles these smoothly, Remixfun's justification needs to be the workflow and evidence model, not a claim that no usable all-in-one application exists.

## Source map and citations

[^s1]: **Supported workflows/platforms and installation** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/README.md); [local README.md](../../../references/sdnext/README.md).

[^s2]: **Runtime setup** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/installer.py); [local installer.py](../../../references/sdnext/installer.py).

[^s3]: **Diffusers execution integration** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/modules/processing_diffusers.py); [local modules/processing_diffusers.py](../../../references/sdnext/modules/processing_diffusers.py).

[^s4]: **Parameter transfer and metadata handling** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/modules/infotext_utils.py); [local modules/infotext_utils.py](../../../references/sdnext/modules/infotext_utils.py).

[^s5]: **Image metadata reader** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/modules/image/metadata.py); [local modules/image/metadata.py](../../../references/sdnext/modules/image/metadata.py).

[^s6]: **Local identity and provider metadata** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/modules/civitai/metadata_civitai.py); [local modules/civitai/metadata_civitai.py](../../../references/sdnext/modules/civitai/metadata_civitai.py).

[^s7]: **Download queue, resume, and expected hashes** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/modules/civitai/download_civitai.py); [local modules/civitai/download_civitai.py](../../../references/sdnext/modules/civitai/download_civitai.py).

[^s8]: **Video loading, execution, caching, and UI** — [Pinned source](https://github.com/vladmandic/sdnext/tree/684940e015911efab2911667231946d91fef9f50/modules/video_models); [local modules/video_models](../../../references/sdnext/modules/video_models).

[^s9]: **Automation API** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/modules/api/api.py); [local modules/api/api.py](../../../references/sdnext/modules/api/api.py).

[^s10]: **Root source license** — [Pinned source](https://github.com/vladmandic/sdnext/blob/684940e015911efab2911667231946d91fef9f50/LICENSE.txt); [local LICENSE.txt](../../../references/sdnext/LICENSE.txt).
