from research_tools import dossier


def write():
    dossier('dreamtime', 'Dreamtime — existing implementation',
        'No tracked root license found; user-owned local baseline, third-party obligations remain',
        'Existing development/deployment assumes Linux; browser client is portable; GPU support depends on Comfy',
        'Source checkout, Python service + Vite web frontend; no desktop release found',
        'Primary extraction source: import, model inventory, image and video adapters',
        [('web/package.json', 'Actual frontend stack'), ('api/services/imports.py', 'Resource availability resolution'),
         ('api/services/civitai.py', 'Civitai metadata and identity lookup'), ('api/services/png_metadata.py', 'Foreign image metadata parsers'),
         ('web/src/pages/ImportDetail.tsx', 'Download Missing and Remix user flow'), ('api/services/model_download.py', 'Model transfer and hash recording'),
         ('api/services/comfy/client.py', 'External Comfy execution boundary'), ('api/services/comfy/video.py', 'Video chaining, interpolation, and loop construction'),
         ('api/workflows', 'Versioned image and video graph templates'), ('api/config.py', 'Runtime configuration and path assumptions'),
         ('api/services/worker.py', 'Application job dispatch'), ('api/models', 'Persistent application entities')],
        r'''
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
''')

    dossier('civiimport', 'CiviImport', 'MIT',
        'ComfyUI extension; OS and GPU support inherit the host and graph nodes',
        'Git/custom-node installation; no release feed or desktop installer captured',
        'Direct Civitai URL → missing models → reconstructed Comfy graph competitor',
        [('README.md', 'User workflow and installation'), ('civitai_api.py', 'Metadata acquisition and resource resolution'),
         ('local_models.py', 'Installed model lookup'), ('hashing.py', 'File identity and hash cache'),
         ('downloader.py', 'Atomic downloads and expected-digest verification'), ('graph_builder.py', 'Graph assembly and inferred generation stages'),
         ('routes.py', 'Comfy HTTP integration'), ('web/js/civiimport.js', 'Browser panel'), ('LICENSE', 'MIT source license')],
        r'''
## Assessment

This is one of the closest implementations of the exact entry workflow: paste a Civitai image URL, recover its recipe, resolve local resources, download missing files, and construct an editable Comfy graph. It challenges the novelty of that mechanism directly. It does not establish broad adoption: the snapshot is less than a week after repository creation, with one star, six commits, and one author name.[^s1]

## Architecture

The extension divides the workflow into reasonably small Python modules: Civitai acquisition, local model inventory, hashing, downloads, graph generation, and HTTP routes. A JavaScript panel runs inside the existing Comfy frontend. Comfy remains the inference server and graph editor; CiviImport does not introduce an independent database-backed desktop application.[^s2][^s3][^s4][^s5][^s6][^s7][^s8]

The service follows image URL → Civitai response → normalized recipe/resources → installed-file resolution → optional downloads → graph. Public endpoints and tRPC fallback are used to recover fields not consistently supplied in one response. The local resolver integrates with Comfy model paths rather than assuming every resource lives in one hardcoded directory.[^s2][^s3]

## What it covers in the target workflow

| Stage | Evidence and limitation |
|---|---|
| Import Civitai image | Directly implemented; metadata availability still constrains recovery |
| Resolve checkpoint/LoRAs/other resources | Version/hash-aware lookup and local scanning |
| Download exact resource | Expected SHA-256, or weaker AutoV2 prefix, checked before final rename |
| Reconstruct baseline | Explicit graph builder; also makes assumptions where the source is incomplete |
| Controlled remix/compare | Graph is editable, but no durable experiment lineage/sweep product established |
| Animate selected result | Comfy can do it through other workflows; no integrated video journey established |

The downloader uses temporary partial files and verifies the expected digest before promoting the download. Full SHA-256 is preferred; an AutoV2 prefix is a partial identity check, not equivalent assurance. The hash cache avoids re-reading large files unnecessarily, with size/mtime used to recognize cache validity.[^s4][^s5]

## Reproduction caveat: reconstruction includes invention

The graph builder synthesizes a conventional checkpoint/CLIP/LoRA/sampler/VAE image pipeline. Its base-resolution heuristics and second sampling pass are especially important: the code can add a hires chain when metadata does not fully specify one. Fallback refine values include a low denoise and derived step/CFG settings. Those are practical approximation choices, but must not be reported as recovered source facts.[^s6]

A model-family hint is not a complete execution adapter. For example, recognizing “Flux” in a resolution heuristic does not prove the conventional checkpoint graph correctly handles every Flux packaging format or encoder arrangement. Test complete graph behavior, not a string in a supported-model list.[^s6]

This distinction is central for Remixfun. An importer can be good at making a plausible new image while still being unable to reproduce the source. Preserve every assumption and make synthetic refinements explicit; the baseline should not silently include embellishments.

## Packaging, license, and operational exposure

The application is installed into a Comfy custom-node environment, so its apparent setup simplicity presupposes a working host. The exported graph uses ordinary Comfy nodes where possible, reducing ongoing dependence on the importing extension. There are no standalone desktop assets in the captured release feed. Source is MIT; model licenses and Comfy's license are separate.[^s1][^s6][^s9]

The concentrated authorship and extremely young history increase uncertainty about API breakage, model-family coverage, and future maintenance. That is a reason to evaluate carefully, not evidence that its implementation is ineffective.

## Comparison with Dreamtime and useful lessons

Dreamtime already has the stronger persistent application shell: imports, jobs, workspace inventory, separate generators, and video adapters. CiviImport is more focused on turning the imported recipe into an inspectable graph and has a stronger expected-hash download check in the inspected path. Its small modules are useful references for strengthening Dreamtime's resolver/download boundary.[^s3][^s5][^s6]

Evaluation should use an SDXL image with known checkpoint version, two LoRAs, an embedding, and published hashes; then repeat with a missing VAE, stripped metadata, and ambiguous hires data. Record what was recovered versus invented. Test extra model paths and same-name/different-hash files. Do not conclude it satisfies Remixfun's complete workflow merely because the generated graph queues successfully.
''')

    dossier('unbake', 'ComfyUI-Unbake', 'GPL-3.0 family; README adds “Not for sale” language requiring clarification',
        'Browser extension + Python Comfy routes; host-dependent Windows/Linux/macOS',
        'Custom-node source installation; no GitHub releases captured',
        'Closest conceptual competitor for provenance-aware replay and controlled comparisons',
        [('README.md', 'Capabilities, limitations, and maturity disclosures'), ('web/core', 'Record, resolution, replay, and sweep core'),
         ('web/panel/sweepView.js', 'Exposed sweep UI'), ('web/host/comfyHost.js', 'Comfy host adapter'),
         ('__init__.py', 'Python extension and routes'), ('web/core/generationRecord.js', 'Normalized generation record'),
         ('LICENSE', 'GPL text'), ('web/panel/detailView.js', 'Import detail and replay interaction')],
        r'''
## Assessment

Unbake is the strongest challenge to the **conceptual** novelty of Remixfun. It explicitly joins imported image metadata, a replay feasibility assessment, graph construction, parameter sweeps, and side-by-side outputs. This is much closer than a generic prompt editor or model browser. Its weakness as a proven alternative is maturity: the repository is under three weeks old in this snapshot, with no stars and no release feed, and reported author names may be aliases of the same person.[^s1]

## Architecture and data model

The frontend core separates three objects: a generation record describing available evidence; a replay manifest describing a proposed executable reconstruction and its missing requirements; and a sweep describing controlled variations. Python integrates with the host server, while JavaScript host adapters submit and observe Comfy jobs. Panels render the import detail, missing-model decisions, and comparison UI.[^s2][^s4][^s5][^s6][^s8]

That separation is more suitable for Remixfun than restoring a handful of route parameters. The source image can remain immutable while resolution status changes as models are installed. Likewise, a replay plan can be replaced without rewriting the historical evidence about the imported source.

## Import and replay

Documented inputs include Civitai images, local metadata-bearing PNGs, existing Comfy outputs, and LoRA Manager recipes. The resolver checks the actual host's `/object_info`, node aliases, and installed resources. Missing requirements have distinct acquisition paths: known downloads, manual actions, or no identified source. Verdicts communicate different levels of feasibility rather than treating any valid graph as exact reproduction.[^s1][^s2][^s4]

This remains a planner and execution tool, not an oracle for the original hidden pipeline. The project's own examples show a runnable substitution producing a different image. For Remixfun, “graph valid,” “exact dependencies present,” “repeatable in this runtime,” and “visually matches source” should be separate observations. An appealing probability badge cannot replace that evidence.

## Controlled remix and persistence

The implemented sweep design has several ideas worth adopting: explicitly selected axes; one baseline; validation before queue submission; graph fingerprints; per-cell persistence; and distinct states for uncertain jobs. `assertOnlySweepInputsChanged` guards against changes outside declared axes. The UI covers checkpoints, generation parameters, LoRA strength, and prompt edits, with a 500-cell cap described in the source documentation.[^s1][^s2][^s3]

Graph fingerprints are useful execution identities but not complete cross-machine identities if they omit resolved file contents and runtime versions. Remixfun should combine graph identity with its model ledger and engine environment. Likewise, a source PNG's metadata may vary between writes even if decoded pixels match.

Captured arbitrary Comfy graphs and recipe-derived records do not have identical sweep support. The README says only recipe-derived records can be swept through this mechanism. It also distinguishes trial/batch core functionality from what is exposed on screen. Those limits prevent crediting every internal module as a finished user feature.[^s1]

## What it does not replace

Model browsing and a general collection manager are explicitly outside the project's scope. No coherent first/last-frame, extension, and loop video product was established. The user still needs Comfy and a compatible environment. Thus it may satisfy the central reproduce-and-compare task for selected recipes while leaving installation, collection management, and motion handoff to other tools.[^s1][^s4]

## License, contributors, and maintenance

The root license is GPL-3.0 text; the README labels GPL-3.0-or-later but also says “Not for sale.” That phrase is in tension with ordinary GPL distribution permissions. Record the ambiguity instead of categorizing this as a clean no-sale license or assuming a permissive grant. A reuse decision should resolve the author's intended terms and any embedded components first.[^s1][^s7]

The short history is dominated by `syugoji` and a Japanese author-name variant. These are two Git author names, not evidence of two independent maintainers. No hands-on reproducibility rate has been measured in this survey; README demonstrations and author's corpus statistics are not independent benchmarks.

## Comparison with Dreamtime and next evaluation

Dreamtime has a larger application domain, persisted assets, a model hub, and existing video graph work. Unbake has a more explicit source-evidence → replay-plan → experiment model and stronger control over comparisons. Remixfun should combine Dreamtime's task-oriented UI and video adapters with an independently designed evidence/manifest boundary.

Evaluate Unbake before building a competing import UI. Test a fully known recipe, a same-name wrong-version LoRA, an incomplete recipe, and a multi-sampler Comfy image. Verify restart/resume behavior and whether a one-axis change actually leaves the submitted baseline graph otherwise unchanged. If it already meets the reproduction half comfortably, the remaining product case must be desktop onboarding, durable library/lineage, and image-to-motion continuity.
''')

    dossier('lora-manager', 'ComfyUI LoRA Manager', 'AGPL-3.0',
        'Comfy extension or standalone Python web app; model execution depends on a separate engine',
        'Comfy custom-node installation, portable standalone option, source releases',
        'Strongest model/recipe collection reference in the direct remix shortlist',
        [('README.md', 'Installation, standalone mode, and capabilities'), ('docs/architecture/recipe_routes.md', 'Layered recipe architecture'),
         ('py/recipes', 'Foreign recipe parsers and merging'), ('py/services/recipes/analysis_service.py', 'Recipe input analysis'),
         ('py/services/recipes/persistence_service.py', 'Recipe storage and fingerprint maintenance'),
         ('py/services/download_manager.py', 'Model download service'), ('standalone.py', 'Engine-independent management server'),
         ('LICENSE', 'Source license'), ('static/js', 'Browser recipe and model interaction')],
        r'''
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
''')

    dossier('civitai-toolkit', 'ComfyUI Civitai Toolkit', 'MIT',
        'Runs inside Comfy; host-dependent OS/GPU support',
        'Custom-node source installation and tagged source releases',
        'Integrated Civitai browsing, local inventory, recipe diagnostics',
        [('README.md', 'Features and installation'), ('api.py', 'HTTP routes and Civitai integration'), ('utils.py', 'Metadata and model utilities'),
         ('nodes.py', 'Recipe and analysis nodes'), ('nodes_display.py', 'Display-oriented nodes'), ('js/civitai_browser.js', 'Online model browser'),
         ('js/local_manager.js', 'Local model manager'), ('js/gallery.js', 'Recipe gallery UI'), ('LICENSE', 'MIT license')],
        r'''
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
''')

    dossier('genrecord', 'genrecord', 'AGPL-3.0 with a documented commercial licensing option',
        'Portable JavaScript library; no GPU, network, UI, or server required',
        'Library source/package; no GitHub releases captured',
        'Reference for normalized evidence, sufficiency, provenance, and variation planning',
        [('README.md', 'Scope and input limitations'), ('src/generationRecord.mjs', 'Canonical record representation'),
         ('src/fromImage.mjs', 'Image ingestion'), ('src/workflowGraph.mjs', 'Graph-aware extraction'),
         ('src/resolve.mjs', 'Resource resolution'), ('src/recordSufficiency.mjs', 'Completeness assessment'),
         ('src/variation.mjs', 'Variation planning'), ('src/license.mjs', 'Caller-supplied licensing evidence'),
         ('LICENSE', 'AGPL source license'), ('COMMERCIAL.md', 'Commercial option')],
        r'''
## Assessment

genrecord is a conceptual/data-model reference, not an alternative desktop application. It separates provenance, reproducibility, permissible-use evidence, and possible variations. That is useful because knowing which model probably created an image is different from possessing the files and execution conditions needed to recreate it.[^s1][^s2][^s6][^s8]

The snapshot is a very young, two-commit project with no stars. Claims about its performance on the author's own image folder should be treated as self-reported evaluation of that corpus, not coverage of arbitrary Civitai images or current Comfy node packs.

## Architecture and boundaries

It is dependency-free JavaScript with no network access. Callers provide records, model inventories, and licensing catalogs. Modules handle parameter/image parsing, graph traversal, name/evidence matching, record sufficiency, resolution, provenance, and variation planning. There is no download manager, queue, GPU runtime, persistent application database, or UI hidden behind the library API.[^s1][^s2][^s3][^s5][^s7]

This is a useful shape for a Remixfun domain layer: the reasoning about an imported record should be testable without starting Comfy or downloading models. It also exposes a tradeoff. A JavaScript core fits the React/Tauri client, while Dreamtime's existing parsing and job logic is Python. Avoid implementing the same canonical decisions independently in both languages; choose one authority and expose it through the application API.

## Evidence fidelity

The strongest input is a structured ledger or richer LoRA Manager recipe that includes hashes, source IDs, version IDs, and model-family information. Extraction from image metadata is weaker. The README explicitly distinguishes these paths: a graph can provide a model filename without a verified content hash or a trustworthy license lookup key.[^s1][^s3][^s4]

Graph traversal follows relationships to generation nodes instead of simply taking the first sampler anywhere in a file. Ambiguous paths are left unresolved with machine-readable reasons. This is preferable to plausible but incorrect flattening. It also means refusal is expected for some multi-stage or unusual graphs and should be surfaced as useful information.[^s4][^s6]

The licensing assessor consumes a catalog supplied by the caller. It does not independently establish model ownership, legal permission, or the accuracy of a website's labels. Remixfun can record the evidence and unknowns without pretending a library calculation grants rights.[^s8]

## Target workflow and Dreamtime comparison

genrecord can normalize and assess an imported recipe and suggest viable variation axes; it cannot fetch Civitai metadata, install a missing checkpoint, run the baseline, or animate the result. Those steps remain the surrounding application's responsibility. Dreamtime already supplies many of them, making the ideas complementary.[^s5][^s7]

The most useful lessons are field-level evidence, explicit unknown states, graph-aware extraction, and a difference between “not recorded,” “not identifiable,” and “not installed.” In Dreamtime, resource availability already has useful version-aware states; a richer record can extend that vocabulary to the entire recipe and runtime.

## Distribution and reuse

The root license is AGPL-3.0 and a commercial option is documented. This is not a drop-in permissive parsing library. The architecture can be studied independently; copying its implementation entails the actual license terms. No adoption or long-term support inference should be made from a readable API and extensive README alone.[^s9][^s10]

Evaluate on a deliberately mixed corpus: A1111 text metadata, ordinary Comfy graphs, multiple samplers, missing LoRA hashes, and metadata-stripped images. Compare extracted fields and refusal reasons with Dreamtime. Success should be measured as correct facts plus honest unknowns, not the maximum number of filled fields.
''')
