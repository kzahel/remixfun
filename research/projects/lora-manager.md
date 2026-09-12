# ComfyUI LoRA Manager

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/willmiao/ComfyUI-Lora-Manager) · [Local clone](../../../references/lora-manager/) · [Raw snapshot](../evidence/lora-manager.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2025-01-27 / 592 days (about 1.62 years) |
| Oldest reachable commit | 2025-01-25T19:22:02+08:00 — can include inherited history |
| Stars / forks / subscribers | 1,454 / 147 / 11 |
| Open issues + PRs | 122 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `6d3f82976fd140499bcb000a3c078dbd31d98898` |
| HEAD commit | 2026-09-11T23:03:24+08:00 fix(scanner): serve folder tree from scan-recorded, persisted directory list (#1110) |
| Reachable commits, including merges | 3,041 |
| Historical distinct author names | 33 |
| Last 90 days: nonmerge commits / author names | 509 / 8 |
| Source license assessment | AGPL-3.0 |
| Operating systems / hardware scope | Comfy extension or standalone Python web app; model execution depends on a separate engine |
| Distribution model | Comfy custom-node installation, portable standalone option, source releases |
| Fit for Remixfun | Strongest model/recipe collection reference in the direct remix shortlist |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Will Miao | 2568 | Will Miao | 493 |
| pixelpaws | 162 | willmiao | 9 |
| willmiao | 15 | s.ivanov | 2 |
| start-life | 13 | Aaalice | 1 |
| hein | 4 | Luna_K | 1 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v1.2.2](https://github.com/willmiao/ComfyUI-Lora-Manager/releases/tag/v1.2.2) | 2026-09-06T14:29:39Z | No attached artifacts in captured expansion; check external distribution |
| [backup/ed7cf418-tip-fix](https://github.com/willmiao/ComfyUI-Lora-Manager/releases/tag/backup%2Fed7cf418-tip-fix) | 2026-09-04T04:41:44Z | No attached artifacts in captured expansion; check external distribution |
| [v1.2.1](https://github.com/willmiao/ComfyUI-Lora-Manager/releases/tag/v1.2.1) | 2026-08-16T11:48:49Z | No attached artifacts in captured expansion; check external distribution |
| [v1.2.0](https://github.com/willmiao/ComfyUI-Lora-Manager/releases/tag/v1.2.0) | 2026-07-31T13:31:13Z | No attached artifacts in captured expansion; check external distribution |
| [v1.1.9](https://github.com/willmiao/ComfyUI-Lora-Manager/releases/tag/v1.1.9) | 2026-07-21T14:22:59Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

LoRA Manager is a meaningful existing alternative for collecting Civitai recipes and managing the models needed to reuse them. It is considerably more established than Unbake or CiviImport in this snapshot: roughly 1.45k stars, over 19 months of repository history, and sustained recent development. Its strongest product center is the model and recipe library, not a proof that any imported image can be recreated.[^s1]

## Architecture

Python handles model scanning, metadata acquisition, hashing/fingerprints, recipe parsing, file persistence, download orchestration, and HTTP routes. The browser UI provides model cards, recipes, search, previews, and workflow handoff. It can attach to Comfy or run its own standalone management server without starting Comfy inference.[^s1][^s7][^s9]

The recipe stack has explicit boundaries: registrar → controller → handler set → use cases/services → caches and files. The analysis service accepts uploaded, local, remote, and widget metadata. Persistence writes image/JSON metadata and keeps fingerprint indexes synchronized. This architecture is useful for Remixfun because import, recipe organization, and inference do not need to live in the same process or share the same lifetime.[^s2][^s4][^s5]

The parser factory contains separate handlers for A1111, Comfy, Civitai, Swarm metadata, and the application's own recipe formats. A merger/enrichment stage combines evidence. The presence of many parsers improves interoperability but does not imply their outputs retain every stage of an arbitrary source graph.[^s3]

## Target workflow coverage

Recipe import, missing-LoRA discovery/download, and transfer of LoRA selections/weights to a Comfy workflow are directly relevant. Checkpoint and embedding scanners also exist; this is broader than the project name suggests. However, sending a recipe to the current workflow is a different operation from reconstructing the exact original pipeline, including hidden hires, refiner, ControlNet, VAE, RNG, and postprocessing stages.[^s1][^s3][^s6][^s9]

The product is an especially strong benchmark for the part of Remixfun that prevents repeated downloads, lets people rediscover their models, attaches example images, and organizes recipes. It is less clearly a substitute for a preserved baseline with a typed diff and a lineage tree across image and video runs.

## Storage and model management lessons

File-backed metadata and previews support browsing existing collections without requiring everything to have been generated through one application. Fingerprints support duplicate handling and recipe reconnection. Mutation paths update both persistent files and in-memory indexes; these consistency rules deserve explicit tests in any extracted Dreamtime library.[^s2][^s5]

The download subsystem is larger than a single fetch loop, with queue/coordinator/routing responsibilities visible in the source tree. Remixfun should distinguish a physical model blob, the Civitai version/file identity, and the set of projects referencing it. Otherwise library organization will either duplicate multi-gigabyte files or lose provenance when filenames change.[^s6]

## Packaging, license, and project health

The standalone option is a model/recipe browser, not a standalone generation runtime. Windows portable distribution and source installation reduce setup for collection management, while actual Comfy workflows retain their host's OS/GPU constraints. The source is AGPL-3.0; a separate model or image does not inherit permission merely because the manager can download it.[^s1][^s7][^s8]

Historical and recent activity are concentrated around Will Miao; variations of that author name appear in history. The contributor table gives evidence of activity and external contributions without pretending all historical names are a current support team. This is a more substantial maintenance signal than tiny new recipe extensions, but still not a user-count estimate.

## Comparison with Dreamtime and evaluation

Dreamtime already has a Civitai image import detail, availability checking, jobs, and image/video generators. LoRA Manager offers a deeper existing collection-management surface and a more modular recipe persistence/indexing architecture. It should be used as a UX and storage benchmark, rather than assuming that Remixfun must first reproduce its whole library interface.

Test importing the same Civitai image and a local PNG, downloading all missing dependencies, reconnecting a renamed model, and sending the recipe into a fresh Comfy instance. Record exactly which values reach the submitted graph. Then ask whether a non-Comfy user can get from that state to a controlled baseline and video without editing nodes. That distinguishes “useful component of the workflow” from “already solves the whole product.”

## Source map and citations

[^s1]: **Installation, standalone mode, and capabilities** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/blob/6d3f82976fd140499bcb000a3c078dbd31d98898/README.md); [local README.md](../../../references/lora-manager/README.md).

[^s2]: **Layered recipe architecture** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/blob/6d3f82976fd140499bcb000a3c078dbd31d98898/docs/architecture/recipe_routes.md); [local docs/architecture/recipe_routes.md](../../../references/lora-manager/docs/architecture/recipe_routes.md).

[^s3]: **Foreign recipe parsers and merging** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/tree/6d3f82976fd140499bcb000a3c078dbd31d98898/py/recipes); [local py/recipes](../../../references/lora-manager/py/recipes).

[^s4]: **Recipe input analysis** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/blob/6d3f82976fd140499bcb000a3c078dbd31d98898/py/services/recipes/analysis_service.py); [local py/services/recipes/analysis_service.py](../../../references/lora-manager/py/services/recipes/analysis_service.py).

[^s5]: **Recipe storage and fingerprint maintenance** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/blob/6d3f82976fd140499bcb000a3c078dbd31d98898/py/services/recipes/persistence_service.py); [local py/services/recipes/persistence_service.py](../../../references/lora-manager/py/services/recipes/persistence_service.py).

[^s6]: **Model download service** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/blob/6d3f82976fd140499bcb000a3c078dbd31d98898/py/services/download_manager.py); [local py/services/download_manager.py](../../../references/lora-manager/py/services/download_manager.py).

[^s7]: **Engine-independent management server** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/blob/6d3f82976fd140499bcb000a3c078dbd31d98898/standalone.py); [local standalone.py](../../../references/lora-manager/standalone.py).

[^s8]: **Source license** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/blob/6d3f82976fd140499bcb000a3c078dbd31d98898/LICENSE); [local LICENSE](../../../references/lora-manager/LICENSE).

[^s9]: **Browser recipe and model interaction** — [Pinned source](https://github.com/willmiao/ComfyUI-Lora-Manager/tree/6d3f82976fd140499bcb000a3c078dbd31d98898/static/js); [local static/js](../../../references/lora-manager/static/js).
