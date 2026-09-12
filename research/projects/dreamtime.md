# Dreamtime — existing implementation

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/kzahel/dreamtime) · [Local clone](../../../references/dreamtime/) · [Raw snapshot](../evidence/dreamtime.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | Public API unavailable; see local history below |
| Oldest reachable commit | 2026-01-14T17:01:54+01:00 — can include inherited history |
| Stars / forks / subscribers | unavailable / unavailable / unavailable |
| Open issues + PRs | unavailable (GitHub combined count) |
| Archived on GitHub | unavailable |
| Inspected branch / HEAD | main / `1129dfcca23afb59c59de48d97d92abbd31cd439` |
| HEAD commit | 2026-03-30T18:15:51+02:00 Fix storyboard image generation using wrong aspect ratio for HiDream and other square-default models |
| Reachable commits, including merges | 62 |
| Historical distinct author names | 1 |
| Last 90 days: nonmerge commits / author names | 0 / 0 |
| Source license assessment | No tracked root license found; user-owned local baseline, third-party obligations remain |
| Operating systems / hardware scope | Existing development/deployment assumes Linux; browser client is portable; GPU support depends on Comfy |
| Distribution model | Source checkout, Python service + Vite web frontend; no desktop release found |
| Fit for Remixfun | Primary extraction source: import, model inventory, image and video adapters |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Kyle Graehl | 62 | — | — |

### Release evidence

No GitHub release entries were captured. This does not exclude registry packages, git installation, external installers, or a private release process.

Collection limitations: repository API: HTTP Error 404: Not Found; release feed: HTTP Error 404: Not Found.

## Assessment

Dreamtime already implements much of the proposed product's middle: importing an image, identifying resources, downloading models, restoring generation parameters, and generating standalone images and video. Remixfun is therefore a focused extraction and hardening exercise, not a new diffusion implementation. The largest missing layer is a durable, inspectable record connecting an imported recipe, a validated baseline, its controlled variants, and the video produced from a chosen variant.[^s2][^s5][^s8]

The local baseline is commit `1129dfcca23a`, with a clean original working tree at collection. The public repository API returned 404. That means popularity, public creation date, and public releases are **unavailable**, not zero. Git history shows one author name and 62 commits; this is a personal implementation baseline, not evidence of a public user community.

## Architecture and execution path

| Boundary | Current implementation | Extraction implication |
|---|---|---|
| Browser application | Vite, React 19, TypeScript; React Query server state and Zustand client state | Retain the web build and make native integration optional |
| Application service | FastAPI/Pydantic, SQLAlchemy/SQLite, application jobs and workers | Keep one API for desktop, CLI, and browser clients |
| Imported artifacts | Import records, downloaded source images, normalized metadata and resources | Add immutable raw evidence and field-level provenance |
| Model inventory | ModelAsset and workspace associations; Civitai identities; local paths | Separate physical blobs from project/workspace references |
| Inference | HTTP/WebSocket Comfy client and Python graph adapters | Preserve process separation and expose backend capabilities |
| Media | Comfy templates, chaining logic, FFmpeg processing | Extract model-specific presets rather than copying the music-video domain |

The actual frontend manifest contradicts older descriptions of a Next.js app: it is Vite/React. The job service mediates between UI actions and Comfy execution; the app is not itself a PyTorch model runtime.[^s1][^s7][^s11][^s12]

## Import → reproduce → remix

The resource resolver distinguishes an installed exact Civitai version, another installed version of the same model, a downloadable resource with a version ID, and an unresolved resource. This is more useful than a filename-only “installed” badge. It is still version-level availability, not proof that the exact original file variant, precision, VAE, and execution environment are present.[^s2]

Civitai import uses public image/model endpoints and fallback tRPC calls to recover generation data. Local parsing covers A1111 parameters, Comfy metadata, NovelAI comments, and legacy Invoke-style metadata. These are separate evidence sources with different completeness, not interchangeable representations of a complete graph. A Comfy graph reduced to a flat parameter set can lose multi-stage behavior.[^s3][^s4]

`ImportDetail.tsx` has concrete Download Missing and Remix actions. Remix restores prompt, negative prompt, dimensions, seed, steps, CFG, sampler/scheduler, clip skip, checkpoint, LoRAs, and embeddings into the generator route. Query-string restoration is useful interaction glue, but it is not an immutable run manifest or a recorded diff. The original evidence, inferred defaults, and user edits need to remain distinguishable after navigation.[^s5]

The downloader computes SHA-256 after transfer and stores it. In the inspected completion path it does **not compare that digest against an expected upstream digest**. Retries remove an existing partial rather than resume it. These are concrete gaps relative to CiviImport and SD.Next download implementations: recording an observed hash is different from verifying expected bytes.[^s6]

## Image → video

The video adapter is substantial: model-specific workflow mutation, frame counts, motion prompts, chaining, trimming overlapping frames, latent-versus-decoded joins, interpolation, and a return-to-start loop segment. The templates include Wan 2.2, LTX-2/LTX-2.3 and multiple image families. Existing graph knowledge is valuable and should be preserved as versioned presets.[^s8][^s9]

Capabilities are not uniform. The Wan 5B loop branch explicitly returns without constructing the closing segment because that path lacks `end_image`; LTX chaining has different machinery. “Loop” must be a capability of a tested preset, not a global checkbox that appears to work on every model. A closing segment is also not evidence of a visually seamless loop until its boundary is assessed.[^s8]

## Portability, maintenance, and licensing

Configuration defaults include Linux absolute paths for Comfy and SQLite. Frontend scripts use shell tools; deployment and service supervision assume the original machine. A desktop shell will not remove those dependencies. Replace path construction with application-data/cache directories, make engine discovery explicit, and supervise the process tree portably.[^s1][^s10]

Cancellation in the Comfy client uses the engine's interrupt mechanism, which matters if another frontend shares that engine. Remixfun should own an engine instance by default or clearly model shared-instance cancellation semantics.[^s7]

No tracked license file was found in this local snapshot. User ownership authorizes this investigation and potential extraction, but does not determine the license of every third-party graph, dependency, or node. A Remixfun source license has deliberately not been chosen.

## Recommended extraction and evaluation

Retain the import adapters, availability vocabulary, image/video workflow knowledge, API types, and useful generator interactions. Refactor workspace-bound storage, download verification, job identity, and runtime paths. Keep music, lyric alignment, storyboard orchestration, character/account workflows, and Claude integration outside the initial standalone product unless a retained feature actually needs them.

Before porting broadly, replay a supported exact-version recipe with two LoRAs; record the full submitted graph and output; restart the app; repeat without redownloading; change only one LoRA weight; then animate the selected variant. Compare this with Unbake, CiviImport, Swarm, and SD.Next using the same inputs. The detailed [Dreamtime comparison](../DREAMTIME-COMPARISON.md) lists the extraction boundaries and acceptance checks.

## Source map and citations

[^s1]: **Actual frontend stack** — Local-only baseline; public URL not verified; [local web/package.json](../../../references/dreamtime/web/package.json).

[^s2]: **Resource availability resolution** — Local-only baseline; public URL not verified; [local api/services/imports.py](../../../references/dreamtime/api/services/imports.py).

[^s3]: **Civitai metadata and identity lookup** — Local-only baseline; public URL not verified; [local api/services/civitai.py](../../../references/dreamtime/api/services/civitai.py).

[^s4]: **Foreign image metadata parsers** — Local-only baseline; public URL not verified; [local api/services/png_metadata.py](../../../references/dreamtime/api/services/png_metadata.py).

[^s5]: **Download Missing and Remix user flow** — Local-only baseline; public URL not verified; [local web/src/pages/ImportDetail.tsx](../../../references/dreamtime/web/src/pages/ImportDetail.tsx).

[^s6]: **Model transfer and hash recording** — Local-only baseline; public URL not verified; [local api/services/model_download.py](../../../references/dreamtime/api/services/model_download.py).

[^s7]: **External Comfy execution boundary** — Local-only baseline; public URL not verified; [local api/services/comfy/client.py](../../../references/dreamtime/api/services/comfy/client.py).

[^s8]: **Video chaining, interpolation, and loop construction** — Local-only baseline; public URL not verified; [local api/services/comfy/video.py](../../../references/dreamtime/api/services/comfy/video.py).

[^s9]: **Versioned image and video graph templates** — Local-only baseline; public URL not verified; [local api/workflows](../../../references/dreamtime/api/workflows).

[^s10]: **Runtime configuration and path assumptions** — Local-only baseline; public URL not verified; [local api/config.py](../../../references/dreamtime/api/config.py).

[^s11]: **Application job dispatch** — Local-only baseline; public URL not verified; [local api/services/worker.py](../../../references/dreamtime/api/services/worker.py).

[^s12]: **Persistent application entities** — Local-only baseline; public URL not verified; [local api/models](../../../references/dreamtime/api/models).
