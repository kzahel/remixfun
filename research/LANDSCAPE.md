# Remixfun landscape survey

**Research snapshot: 12 September 2026.** This survey covers 28 cloned repositories, including Dreamtime and Desktop Release Kit, with a separate architectural dossier for each. It is a source/documentation investigation, not a hands-on GPU benchmark. Facts below refer to inspected revisions; recommendations are the researcher's assessment.

**Decision update:** The user has chosen to build Remixfun. The [current product/build plan](../PLAN.md) supersedes this survey's recommendations to run competitor trials before implementation. References remain source-only research.

## 1. Decision-level findings

**The broad idea is established; the specific product can still be worthwhile.** Friendly local generation apps, model downloaders, Comfy workflow forms, PNG metadata reuse, and parameter grids already exist. Several newer extensions directly implement Civitai image import and replay. The unresolved opportunity is to make the entire chain dependable and understandable: **source image → recovered evidence → qualified baseline → controlled variants → selected image → motion**.

Three groups deserve immediate evaluation:

| Evaluation group | Projects | Why they matter |
|---|---|---|
| Closest to the core import/replay idea | Unbake, CiviImport, LoRA Manager, Civitai Toolkit | Challenge novelty directly; recover recipes, resolve resources, or compare variations |
| Established complete applications | SwarmUI, Stability Matrix, SD.Next, Invoke | Could already satisfy much of the practical task with fewer new components |
| Existing simplified Comfy presentation and setup | Official frontend/App Mode, Comfy Desktop, ViewComfy, Krita AI Diffusion | Remove much of the node-editor and installer friction that a wrapper might otherwise claim to solve |

These roles are supported by code paths and installation/product documentation in the linked dossiers.[^1][^2][^3]

**Retain Comfy as the proposed initial engine.** Dreamtime already contains useful image/video graph adapters, including chaining and loop work. Replacing the engine now would discard that investment before proving it is the bottleneck. stable-diffusion.cpp is the strongest later native-runtime candidate; Draw Things is a valuable Apple benchmark; WanGP is a strong motion benchmark with material commercial-embedding restrictions.[^4]

**Treat desktop packaging and model execution as separate portability problems.** Tauri/Release Kit can deliver Windows, Linux, and Mac application artifacts. A tested engine profile must separately establish which Python/Torch/node/model combinations work on each GPU. Comfy runs on Apple Silicon; that does not establish parity for every video workflow.[^5]

**Do not use “deterministic” as an unconditional source-reproduction promise.** A fixed seed and model name are not sufficient. The source can omit important stages, and numerical results can differ across runtime releases, platforms, devices, and execution settings. PyTorch explicitly limits reproducibility guarantees across such changes.[^6]

A [2026-09-28 source follow-up](../docs/evidence/determinism-source-review.md)
recloned the closest replay tools on Mac and traced a concrete Euler ancestral
CPU-noise mismatch candidate. It did not execute competitors or establish a
pixel-identical Civitai replay.

## 2. Define the actual user job

The user's request is more precise than “make something inspired by this image.” It is:

1. Import a Civitai URL, a downloaded image, or a complete graph/recipe.
2. Extract recorded settings and retain the original evidence.
3. Identify exact resources and explain missing or ambiguous dependencies.
4. Download and verify available files, reusing an existing local library.
5. Attempt the original recipe and qualify the resulting baseline.
6. Change selected parameters without silently changing everything else.
7. Compare results and preserve which variant was selected.
8. Animate that exact image using a suitable model/preset, including first/last-frame, extension, or loop operations where supported.
9. Reopen or share the recipe later without losing source identity or relying on a browser session.

A competitor should be scored against that whole journey. A model browser only covers part of step 3/4. PNG Info covers part of step 2/5. A generic workflow form covers execution controls. A polished image editor may be excellent for visual changes but weak at source-recipe reconstruction.

The initial product should accept incomplete evidence gracefully. It can still offer a useful remix, but should explain whether it is replaying recorded conditions, filling in missing settings, substituting a resource, or using the image only as visual input.

## 3. Direct recipe/replay competition

### Unbake: closest conceptual overlap

Unbake explicitly models records, replay manifests, and sweeps. It checks the installed Comfy environment, classifies missing resources, builds graphs, and enforces declared comparison axes. It persists per-cell execution state and uses graph fingerprints to avoid accidental duplicate work. Those are concrete ideas central to the proposed Remixfun workflow.[^1]

The limitation is maturity and scope. The repository is weeks old, has minimal public attention, and exposes different capabilities for recipe-derived records versus captured graphs. Model collection/browsing is intentionally outside its scope, and the complete motion journey was not established. It is the first direct concept to test, but not evidence that the whole consumer product is already solved.

### CiviImport: focused reconstruction with useful integrity checks

CiviImport performs Civitai image URL acquisition, resource matching, missing-file downloads, and graph construction. Its downloader checks an expected digest before promoting the file, which is stronger than Dreamtime's inspected post-download hash recording. Its builder also invents plausible defaults and can synthesize a hires chain; therefore a valid generated graph is not necessarily the original recipe.[^1]

The useful lesson is to expose assumptions. A baseline that silently adds a refine pass can look attractive while defeating the user's desire to understand and reproduce someone else's settings.

### LoRA Manager and Civitai Toolkit: collection and discovery

LoRA Manager is substantially more established than the two new replay extensions and has a deeper model/recipe collection architecture. It handles multiple metadata sources, library scanning, fingerprints, missing resources, and Comfy handoff. Its standalone mode manages collections without running inference. Toolkit brings Civitai browsing, local inventory, and recipe diagnostics into Comfy.[^1]

Neither should be assumed to recover every hidden stage just because the UI calls a collection of settings a recipe. For evaluation, inspect the actual submitted graph and resolved file identities. These projects are particularly strong references for keeping a useful local model library after the first import.

### genrecord: a domain-model reference

genrecord separates evidence, sufficiency, resolution, provenance, and potential reuse. It is a library without network, GPU, queue, or UI. The conceptual separation is valuable; it is not a ready-made application. Its AGPL/commercial licensing and tiny history also deserve explicit consideration before code reuse.[^1]

## 4. Established apps could already satisfy much of the task

### SwarmUI

Swarm is the most relevant broad Comfy-based application benchmark. It already offers task controls, generated graphs, parameter reuse, model tools, image/video workflows, and multiple backend orchestration. Its MIT source and active development are useful signals. Its .NET application architecture differs from Dreamtime's Python/React stack.[^2]

The key question is not whether Swarm can generate a video—it can—but how much manual work remains between an arbitrary Civitai image and a controlled baseline plus motion result. That must be observed through the user journey.

### Stability Matrix

Matrix combines a native Avalonia application, managed AI packages/environments, shared model storage, Civitai browsing/downloads, and its own native Comfy inference UI. Current inference docs include Wan and SVD video modes. It is a direct competitor to “desktop generation with easy downloads,” not merely an installer.[^2]

Its own embedded project state is richer than its generic foreign-metadata route. In the inspected Civitai resource parser, LoRA version IDs are retained through a structure that does not carry their per-resource weights; other prompt syntax paths may still supply weights. Installed-model matching is separate from downloading missing models. Those are specific integration points to test, not proof that the whole app loses every LoRA weight.

### SD.Next

SD.Next provides a broad image/video product with active development, foreign metadata, Civitai file management, queued/resumable downloads with expected hashes, model loading/quantization, and diverse hardware support. It deserves primary evaluation. It is an alternative engine/application, so migrating to it would require translating Dreamtime's Comfy-specific work.[^2]

### Invoke

Invoke is an established image/canvas application with a persistent queue, model registry, metadata recall, and its own invocation graph. **Current source includes Wan video, two-image interpolation, and video extension workflows.** Older “image-only” comparisons are no longer accurate. Its Apache-licensed source and similar Python/web application patterns make it a useful architecture reference, although it does not execute Comfy workflows as its primary engine.[^2]

### A1111, Forge, Fooocus, and Easy Diffusion

A1111 is the historical baseline for PNG Info, parameter reuse, and XY/Z experiments. Forge inherits that interaction style with different loading/memory behavior. Their huge inherited ecosystems are relevant to foreign recipe semantics, but the inspected original default branches have limited recent activity. That observation does not summarize every descendant fork.[^7]

Fooocus demonstrates strong preset UX and automatic model acquisition, but explicitly limits its roadmap to SDXL-oriented LTS. Easy Diffusion is still evolving, including newer engine paths, and remains a useful installation/queue benchmark. Easy Diffusion's root license is custom and use-restricted; Fooocus's is GPL-3.0, not AGPL.[^7]

## 5. Simplified workflow UI is now common infrastructure

The official Comfy frontend's App Mode lets an author select workflow inputs/outputs, preview them, and choose an app-style default view. Local workflow saving and cloud share links are distinct. This directly covers the basic premise of making a prepared Comfy graph usable without opening the node editor.[^3]

ViewComfy and SDFX pursue related workflow-to-form ideas. ViewComfy is a Next/React app with local and hosted surfaces; its public default branch's inactivity does not prove private service inactivity. SDFX has web/Electron builds and enriched graph/UI mappings, but its old default branch and absent captured releases make it a weak foundation for a new maintained product.[^8]

Visionatrix is the closest full service architecture reference: Python API/database, Nuxt UI, installable/versioned flows, model catalog mapping, workers, and CLI/service modes. It is now explicitly archived. Its history illustrates how much work sits beyond a nice workflow form: compatibility, installs, migrations, data locations, and operational recovery.[^8]

Krita AI Diffusion shows another successful approach: attach Comfy to a specific creative task in a mature host. Its canvas, layers, masks, references, history, and managed server are a strong visual-remix alternative. It does not establish the particular foreign-recipe replay journey, but it may be better than parameter editing for users whose intent is to change visible content.[^3]

## 6. Workflow coverage matrix

**Evidence labels:** `C` = relevant code path inspected; `D` = documented capability; `P` = partial, separate step, or needs integration; `?` = not established in this review; `—` = outside the component's role. No entry means hands-on tested or pixel-identical reproduction. “Video” includes a model-dependent workflow, not every requested motion feature.

| Project | Foreign image/recipe import | Missing-resource acquisition | Explicit replay/controlled experiment model | Image → video | Desktop / CLI-web optionality |
|---|---|---|---|---|---|
| Dreamtime | C | C, verification/resume gaps | P: restores generator state | C | Web/API; desktop absent |
| Unbake | C/D | C/D, scoped resolvers | C/D: manifest and sweeps | ? | Comfy extension |
| CiviImport | C | C: expected digest checks | P: constructed graph and assumptions | ? | Comfy extension |
| LoRA Manager | C | C/D | P: recipes and handoff | ? | Standalone manager or extension |
| Civitai Toolkit | C/D | C/D | P: recipe diagnostics | ? | Comfy extension |
| SwarmUI | C, format-dependent | C, separate utility | P: metadata reuse and controls | C | Web/server; install scripts |
| Stability Matrix | C, own state richer | C/D, separate browser | P: saved tab/projects | D/C | Native UI; managed apps have web UIs |
| SD.Next | C | C | P: parameter restoration/variation | C/D | Web/API; installer paths |
| Invoke | C: strongest for own metadata | C: model installer | P: own metadata/workflows | C | Web/API; separate launcher |
| Comfy + App Mode | C: complete graphs | P: separate installation layers | P: graph run/edit | C | Desktop or independent server |
| WanGP | P: own settings/inputs | C/D: supported model workflows | P: saved settings/queues | C/D | CLI + web; Tauri companion |
| A1111 / Forge | C: infotext/PNG | P: manual/extensions | C: parameters/grids; no full provenance | P: external extensions | Web/API/scripts |
| Krita AI Diffusion | P: visual image input | C: managed resources | P: canvas/history | ? for requested motion journey | Krita plugin, remote/local backend |
| ViewComfy / SDFX | P: authored workflows | P | P: exposed controls | P: prepared graph | Web; SDFX Electron path |
| Visionatrix | P: catalog/custom flows | C/D | P: tasks and flow versions | D | Web/CLI/workers; archived |
| stable-diffusion.cpp | P: parameter inputs | P: external model acquisition | P: runtime/CLI repeatability | C/D | Native CLI/server/web UI |
| genrecord | C: parsing library | —: no network/download | C: assessment/planning only | — | Library |
| Pinokio / WanGP launcher | — | P: application/runtime installation | — | —: delegated to launched app | Desktop launchers |

Detailed claims and their scope are traceable through the individual dossiers. This matrix deliberately avoids a numeric “best app” score: comparable user-task measurements do not yet exist.[^1][^2][^3][^4][^7][^8][^9]

## 7. Popularity, age, and contributor interpretation

The largest accumulated attention is around A1111 (~165k stars), Comfy (~133k), Fooocus (~53k), and Invoke (~28k). Among other relevant apps, the snapshot includes Forge (~13k), Krita AI Diffusion (~10.6k), Easy Diffusion (~10.5k), WanGP (~9.3k), Matrix (~8.8k), Pinokio (~8k), SD.Next (~7.3k), stable-diffusion.cpp (~7k), and Swarm (~4.5k). LoRA Manager (~1.45k) is meaningfully larger than the new replay extensions.[^10]

These are **repository stars, not users, installs, market share, satisfaction, or commercial adoption**. The detailed matrix contains exact figures and captured timestamps. GitHub release downloads, Discord membership, package downloads, and paid customers were not collected; they should not be invented from popularity badges.

Age requires care. Swarm and Forge inherit earlier code; Comfy Desktop's repository age is not the full product age; Draw Things' public core age is not the consumer app's age. Dreamtime's public metadata was unavailable, so its local history is reported without fabricated public metrics.

Contributor counts are distinct names visible in Git history, with top historical and recent names in every dossier. Aliases, bots, and inherited commits inflate apparent team size. The 90-day window helps distinguish historical popularity from recent work, but only covers the inspected default-branch history. Visionatrix's explicit archive status and Fooocus's explicit LTS statement are firmer scope signals than an inactivity heuristic.

## 8. Licensing findings that affect architecture

| Project/group | Source finding | Consequence for evaluating reuse |
|---|---|---|
| Swarm, CiviImport, Civitai Toolkit, stable-diffusion.cpp, Pinokio, Release Kit | MIT roots | Useful permissive references; still inspect dependencies/models |
| Invoke, SD.Next, Civitai CLI | Apache-2.0 roots | Attractive source terms; inherited/bundled components still matter |
| Comfy engine/frontend, Krita, Draw Things core, Fooocus | GPL-3.0 family | Preserve exact package/file license distinctions; frontend declares GPL-3.0-only |
| Matrix, LoRA Manager, ViewComfy, SDFX, Visionatrix, A1111/Forge | AGPL family | Source obligations and distribution boundaries need explicit treatment |
| Comfy Desktop | AGPL-or-commercial dual license | Not MIT and not proprietary-only unavailable source |
| WanGP | Custom Community License 2.0 | Commercial embedding/paid access can require a separate agreement, including wrapper/API forms |
| Easy Diffusion | MIT-like text plus use restrictions | Not plain MIT |
| Unbake | GPL text plus README no-sale phrase | Ambiguity recorded; clarify before code reuse |
| WanGP Tauri launcher | No tracked license found | Public clone does not establish reuse permission |
| Dreamtime | No tracked license found in local baseline | User-owned extraction context; choose Remixfun license deliberately |

The matrix is based on the license files, not merely GitHub's automated labels. Matrix also distinguishes AGPL source from its official binary EULA; Draw Things' full consumer UI is not in its public core repository. Model licenses are separate from application licenses, and rights recorded in metadata are evidence rather than automatic permission.[^11]

This survey does not choose a business model or source license for Remixfun. In particular, subprocess separation is not treated as a universal way around an engine's terms; WanGP explicitly includes integrations in its custom license.

## 9. What Dreamtime already gives this project

Dreamtime already has a React/Vite UI, FastAPI services, persistent imports/jobs/models, Civitai acquisition, multiple metadata parsers, version-aware resource states, Download Missing, Remix parameter restoration, image templates, and substantial video composition. The frontend is not Next.js despite older descriptions.[^12]

The concrete gaps are not mysterious:

- Hash recording after download is not expected-hash verification; interrupted transfers currently restart.
- A Civitai version match does not uniquely identify every file variant or execution environment.
- Route-parameter restoration does not preserve immutable source/baseline/variant lineage.
- Flattening foreign metadata can discard stages or hide unknowns.
- Linux absolute path defaults and shell/service assumptions need replacement.
- Video capabilities differ by template: the inspected Wan 5B loop path explicitly skips the closing segment.
- Comfy cancellation semantics matter when sharing an engine with another frontend.
- App updates, runtime upgrades, and model acquisition need separate lifecycle rules.

The extraction proposal in [DREAMTIME-COMPARISON.md](DREAMTIME-COMPARISON.md) retains the useful parts and narrows the original music-video application domain.

## 10. Recommendation and decision gates

Build the product case around **understanding and controlling a remix**, with import and motion integrated around that core. Begin with a narrow supported recipe set and explicit unknown/substitution states. Export the source evidence, resolved requirements, submitted graph, and variant diff so a user can inspect or leave the app later.

Before implementing a complete new UI, run the fixture plan against Unbake, CiviImport, Swarm, Matrix, SD.Next, Invoke, and Comfy App Mode. If one already meets the task with little friction, a focused extension or complementary library could be the better result. If the gap is persistent source/variant lineage and a smooth motion handoff, proceed with the Dreamtime extraction.[^13]

Use one application service for web, CLI, and optional desktop. Keep Comfy behind a capability-aware adapter; use Release Kit's distribution contract; implement runtime profiles and model storage separately. Prove one Windows/NVIDIA image baseline and one video preset before promising broad model/OS parity. Linux can share much of the runtime work; Apple Silicon should have its own measured supported profile.[^14]

## Sources and supporting dossiers

[^1]: Direct tools: [Unbake](projects/unbake.md), [CiviImport](projects/civiimport.md), [LoRA Manager](projects/lora-manager.md), [Civitai Toolkit](projects/civitai-toolkit.md), [genrecord](projects/genrecord.md). Each contains pinned source citations.
[^2]: Established apps: [SwarmUI](projects/swarmui.md), [Stability Matrix](projects/stability-matrix.md), [SD.Next](projects/sdnext.md), [Invoke](projects/invokeai.md).
[^3]: [Official Comfy frontend/App Mode](projects/comfy-frontend.md), [Comfy Desktop](projects/comfy-desktop.md), [Krita AI Diffusion](projects/krita-ai-diffusion.md).
[^4]: Runtime alternatives: [ComfyUI](projects/comfyui.md), [stable-diffusion.cpp](projects/stable-diffusion-cpp.md), [Draw Things](projects/draw-things.md), [WanGP](projects/wan2gp.md).
[^5]: [Official Comfy requirements](https://docs.comfy.org/installation/system_requirements), accessed 2026-09-12; [Desktop Release Kit](projects/desktop-release-kit.md).
[^6]: [PyTorch reproducibility guidance](https://docs.pytorch.org/docs/2.14/notes/randomness.html), accessed 2026-09-12. Exact equality across releases/platforms and CPU/GPU is not generally guaranteed.
[^7]: Historical/simple apps: [A1111](projects/automatic1111.md), [Forge](projects/forge.md), [Fooocus](projects/fooocus.md), [Easy Diffusion](projects/easy-diffusion.md).
[^8]: Workflow frontends: [ViewComfy](projects/viewcomfy.md), [SDFX](projects/sdfx.md), [Visionatrix](projects/visionatrix.md).
[^9]: Packaging/integration: [Pinokio](projects/pinokio.md), [WanGP Tauri launcher](projects/wan2gp-desktop.md), [official Civitai CLI](projects/civitai-cli.md).
[^10]: [Exact repository matrix](REPOSITORY-MATRIX.md), [individual machine-readable snapshots](evidence/), and [collection methodology](METHODOLOGY.md).
[^11]: License file links and distribution qualifications are in each project's dossier and the [license/platform matrix](REPOSITORY-MATRIX.md#license-platform-and-distribution).
[^12]: [Dreamtime dossier and pinned local source map](projects/dreamtime.md).
[^13]: [Evaluation plan](EVALUATION-PLAN.md); proposed measurements, not completed benchmark results.
[^14]: [Proposed architecture](ARCHITECTURE.md); recommendation, not implemented product code.
