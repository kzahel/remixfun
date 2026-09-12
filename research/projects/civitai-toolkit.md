# ComfyUI Civitai Toolkit

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit) · [Local clone](../../../references/civitai-toolkit/) · [Raw snapshot](../evidence/civitai-toolkit.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2025-08-29 / 378 days (about 1.03 years) |
| Oldest reachable commit | 2025-08-29T23:35:50+08:00 — can include inherited history |
| Stars / forks / subscribers | 142 / 7 / 3 |
| Open issues + PRs | 4 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `c1589348ff3ecbb07f326a833936e692fec4fa2d` |
| HEAD commit | 2026-02-19T19:43:30+08:00 feat: 改进 Windows 路径比较逻辑，以正确处理不同驱动器和大小写不敏感的路径。 |
| Reachable commits, including merges | 82 |
| Historical distinct author names | 2 |
| Last 90 days: nonmerge commits / author names | 0 / 0 |
| Source license assessment | MIT |
| Operating systems / hardware scope | Runs inside Comfy; host-dependent OS/GPU support |
| Distribution model | Custom-node source installation and tagged source releases |
| Fit for Remixfun | Integrated Civitai browsing, local inventory, recipe diagnostics |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| BAIKEMARK | 58 | — | — |
| Mark | 1 | — | — |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v4.1.0](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/releases/tag/v4.1.0) | 2025-10-10T12:54:27Z | No attached artifacts in captured expansion; check external distribution |
| [v4.0.2](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/releases/tag/v4.0.2) | 2025-10-07T04:01:43Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

Civitai Toolkit puts discovery, local model management, and recipe analysis inside Comfy. It is more integrated into browsing than CiviImport and more oriented toward recipe exploration than a general workflow-form builder. The repository has modest attention and no default-branch commits in the captured 90-day window; its most recent inspected commit fixes Windows path handling.[^s1]

## Architecture and data flow

The Python side exposes Civitai and local-file operations through `api.py`, with parsing and shared utilities in `utils.py`. Custom nodes perform recipe lookup/analysis and return display data. JavaScript implements a Civitai browser, local manager, gallery, notifications, and global settings. It is not a separate Tauri/Electron product or an independent inference engine.[^s2][^s3][^s4][^s5][^s6][^s7][^s8]

The useful sequence is model discovery → preview/example image → recipe fields and dependencies → local availability/download actions → Comfy workflow inputs. Supported inventory categories include checkpoints, LoRAs, VAEs, embeddings, diffusion models, text encoders, and hypernetworks. Category breadth should not be confused with complete graph reconstruction for every corresponding model architecture.[^s1][^s3]

## Does it satisfy import/reproduce/remix?

It implements important prerequisites: source browsing, metadata-linked model files, parameter/LoRA recipe extraction, and diagnostics for unavailable dependencies. It also exposes aggregate recipe analysis, such as common settings and model combinations. That supports discovery and remix inspiration.[^s4][^s8]

The survey did not establish a durable baseline/replay manifest or an invariant that only declared remix parameters change. A recipe gallery restoring prompt and LoRAs is not evidence that source-specific upscaling, sampler semantics, conditioning, or omitted stages were recovered. Treat “full recipe” wording in the README as a product claim whose boundary needs a fixture test.[^s1][^s3][^s4]

No integrated image-to-video handoff with first/last-frame and loop lineage was established. Comfy can supply those workflows, but the toolkit's role is discovery and metadata rather than the complete guided motion experience.

## Packaging, operation, and licensing

The tagged v4.1.0 release is a source release in the captured feed; installing the node package still assumes a compatible Comfy environment. Background hashing and metadata scanning address slow startup for large libraries. API-key configuration and an optional network mirror are present; a product embedding these ideas would need explicit provider configuration and provenance about where each response came from.[^s1][^s2][^s3]

The source license is MIT. Comfy, bundled dependencies, downloaded models, and remote provider conditions remain separate. The small contributor base and limited recent activity suggest maintaining a narrow internal adapter may be easier than depending on every part of this extension.[^s9]

## Comparison with Dreamtime

Dreamtime starts from a user-imported image and follows it into application jobs and generators. Toolkit starts nearer the model browser and community examples. Its recipe diagnostics and local/remote browsing integration can improve Dreamtime's Model Hub; it is not an architectural replacement for Dreamtime's API/worker/video services.

Evaluate one known Civitai image with all metadata and one with a missing checkpoint or VAE. Capture the emitted recipe and final graph, not just the displayed text. Check model aliases, extra paths, download status after restart, and whether ambiguous graph metadata remains visibly incomplete. This will reveal whether the implementation is useful as a focused parser/browser reference or as an actual reproduction path.

## Source map and citations

[^s1]: **Features and installation** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/README.md); [local README.md](../../../references/civitai-toolkit/README.md).

[^s2]: **HTTP routes and Civitai integration** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/api.py); [local api.py](../../../references/civitai-toolkit/api.py).

[^s3]: **Metadata and model utilities** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/utils.py); [local utils.py](../../../references/civitai-toolkit/utils.py).

[^s4]: **Recipe and analysis nodes** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/nodes.py); [local nodes.py](../../../references/civitai-toolkit/nodes.py).

[^s5]: **Display-oriented nodes** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/nodes_display.py); [local nodes_display.py](../../../references/civitai-toolkit/nodes_display.py).

[^s6]: **Online model browser** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/js/civitai_browser.js); [local js/civitai_browser.js](../../../references/civitai-toolkit/js/civitai_browser.js).

[^s7]: **Local model manager** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/js/local_manager.js); [local js/local_manager.js](../../../references/civitai-toolkit/js/local_manager.js).

[^s8]: **Recipe gallery UI** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/js/gallery.js); [local js/gallery.js](../../../references/civitai-toolkit/js/gallery.js).

[^s9]: **MIT license** — [Pinned source](https://github.com/BAIKEMARK/ComfyUI-Civitai-Toolkit/blob/c1589348ff3ecbb07f326a833936e692fec4fa2d/LICENSE); [local LICENSE](../../../references/civitai-toolkit/LICENSE).
