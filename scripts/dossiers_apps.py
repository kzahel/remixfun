from research_tools import dossier


def write():
    dossier('swarmui', 'SwarmUI', 'MIT',
        'Windows/Linux/macOS application server; actual model/GPU support comes from configured backends',
        'Install/run scripts and web UI; beta source releases; external Comfy processes',
        'Strongest established Comfy-based general-purpose app benchmark',
        [('README.md', 'Product, installation, and independent continuation'), ('src/SwarmUI.csproj', '.NET application boundary'),
         ('src/Backends', 'Backend orchestration'), ('src/BuiltinExtensions/ComfyUIBackend/WorkflowGenerator.cs', 'Graph generation'),
         ('src/BuiltinExtensions/ComfyUIBackend/WorkflowGeneratorSteps.cs', 'Generation stages'),
         ('src/wwwroot/js/genpage/helpers/metadatahelpers.js', 'Foreign metadata normalization'),
         ('src/wwwroot/js/genpage/gentab/currentimagehandler.js', 'Image interaction and parameter reuse'),
         ('docs/Image Metadata Format.md', 'Persisted image metadata and optional model hashes'),
         ('src/wwwroot/js/genpage/utiltab.js', 'Utility/model download interface'), ('LICENSE.txt', 'MIT source license')],
        r'''
## Assessment

SwarmUI is a serious existing answer to “a friendly app on top of Comfy with image and video generation.” Its backend abstraction, generated workflows, model tools, saved outputs, and broad controls make it the first established product to evaluate before assuming Remixfun needs a complete new generation interface.[^s1][^s3][^s4]

Its independent repository was created in June 2024 and inherits the StableSwarmUI lineage. The creation date and large historical commit count therefore measure different things. Activity is substantial but heavily concentrated around Alex “mcmonkey” Goodwin; historical contributors should not be mistaken for a comparably large active maintenance team.

## Architecture

Swarm is a .NET 8 ASP.NET application with a browser UI built from its web assets/pages. C# services handle user/session state, parameter definitions, media/model metadata, and backend scheduling. Comfy is one backend implementation and can be managed locally or contacted over its API. There is also a graph-editor path for advanced workflow use.[^s2][^s3][^s4]

The important boundary is application parameters → backend-specific graph generation → execution. `WorkflowGenerator` and the stage/model-support code encode substantial model-family knowledge. This is analogous to Dreamtime's Python image/video adapters, but generalized across a larger parameter/backend surface.[^s4][^s5]

Multiple backends and workers make it more suitable than a single embedded inference loop for remote GPUs and parallel generation. That flexibility creates orchestration complexity Remixfun need not copy for its initial single-user, one-GPU experience.[^s3]

## Import/reproduce/remix coverage

Swarm imports and reuses image parameters, and its metadata helpers normalize A1111 and Fooocus representations into its own schema. Its own outputs can include rich parameters and optional model identity information. The generic metadata import path does not automatically turn an arbitrary Comfy graph JSON into a complete flat Swarm recipe; arbitrary workflows use a different route.[^s6][^s7][^s8]

Parameter reuse is a credible way to reproduce Swarm's own outputs when dependencies and settings are preserved. It is weaker evidence for a Civitai image from an unknown engine. A source may omit conditioning, refiner settings, VAE, prompt weighting semantics, or additional processing. The metadata format's model hash option also needs care: the documented tensor-oriented hash is not automatically interchangeable with a provider's whole-file SHA-256.[^s8]

The model downloader provides a way to acquire resources, but a separate download utility is not proof that dropping any Civitai image resolves every exact dependency automatically. The imported recipe, selected model file, and final generated workflow should be inspected together in evaluation.[^s6][^s9]

## Video and workflow continuity

Swarm's graph-generation stages cover video workflows as part of the same application. It competes directly with a unified image/video front end; it is not just a still-image UI. Whether a given model supports first/last-frame constraints, extension, or loops must be checked against its graph adapter and current installed nodes, rather than inferred from a general video tab.[^s4][^s5]

Remixfun's potential distinction is narrower: preserving the source image, exact baseline, declared changes, selected winner, and resulting motion clip as a comprehensible chain. Swarm's broad capability list by itself does not demonstrate that specific evidence-driven journey.

## OS, distribution, and licensing

Swarm uses install/run scripts and a local web server, with Windows/Linux/macOS instructions. It is not a Tauri binary with a uniform signed updater. A browser can run on a machine different from the GPU server. Backend compatibility and custom-node requirements still determine which models actually execute.[^s1][^s3]

The MIT license makes its own implementation a comparatively straightforward source reference, while Comfy, extensions, downloaded models, and bundled components retain their terms. Its beta release naming should be preserved in reporting; frequent commits do not imply every combination has a stable support contract.[^s10]

## Comparison with Dreamtime and evaluation

Dreamtime is closer to a focused product flow and already has first/last-frame loop construction. Swarm offers stronger generalized backend orchestration and a larger established generation surface. Replacing Dreamtime wholesale would exchange Python/React familiarity for a C# application and its broader domain. Studying its adapter boundaries is more immediately useful.

Run the full target task in Swarm: import a known Civitai recipe, resolve missing models, reproduce a baseline, compare one changed LoRA weight, and animate the selected result. Record every manual model search, graph edit, setting lost during import, and extra navigation step. If that journey is already easy, Remixfun should concentrate on baseline fidelity and traceable experiments rather than competing on raw model support.
''')

    dossier('stability-matrix', 'Stability Matrix', 'AGPL-3.0 source; official binaries have a separately linked EULA',
        'Windows x64, Linux x64, macOS Apple Silicon; packages and GPU support vary',
        'Native Avalonia desktop; Windows/Linux archives and macOS DMG; managed AI packages',
        'Strongest combined installer, shared-model library, and native Comfy inference competitor',
        [('README.md', 'Package manager, platforms, distribution, and binary license distinction'),
         ('StabilityMatrix.Core', 'Shared services, packages, models, and downloads'),
         ('StabilityMatrix.Avalonia/ViewModels/Base/InferenceTabViewModelBase.cs', 'Image metadata ingestion'),
         ('StabilityMatrix.Core/Models/GenerationParameters.cs', 'Generic/Civitai parameter representation'),
         ('StabilityMatrix.Avalonia/ViewModels/Inference/ModelCardViewModel.cs', 'Installed model matching and state restoration'),
         ('docs/inference/overview.md', 'Native inference, supported modes, and project state'),
         ('docs/advanced/comfyui-integration.md', 'Comfy graph and API boundary'), ('LICENSE', 'AGPL source license')],
        r'''
## Assessment

Stability Matrix already combines many features proposed for Remixfun: a desktop application, environment/package management, a shared model library, Civitai browsing/downloads, and a native generation interface over Comfy. It should not be dismissed as merely a launcher. Its roughly 8.8k stars and continuing development are substantial attention/maintenance signals for this category.[^s1][^s6]

## Architecture

The application uses C#/.NET with Avalonia for native UI, with reusable services and models in `StabilityMatrix.Core`. It manages Python/Git and multiple AI packages, establishes shared model locations, and talks to a launched Comfy server through HTTP/WebSockets. The native inference UI constructs Comfy graphs from tab state, uploads inputs, consumes progress/previews, and retrieves outputs.[^s2][^s7]

This is a close architectural analogy to the proposed Tauri product, but the UI portability story is different: Avalonia views do not become a standalone browser frontend simply by removing the native shell. The managed web applications can still be used separately. Remixfun's browser and CLI requirements favor keeping the domain service/API separate from desktop view models.

## What image import actually restores

`InferenceTabViewModelBase` has paths for embedded Stability Matrix projects and more generic generation metadata, including Civitai-style data. Its own `.smproj`/embedded project state is richer than an imported foreign parameter string. The project file records state, not the actual model weights or an immutable runtime environment.[^s3][^s6]

In the inspected Civitai parsing path, resources carry version IDs, while the LoRA representation used there is a list of IDs rather than the complete per-resource weight record. LoRA weights may also be represented through prompt syntax elsewhere; the observation is about this parser path, not a claim that the whole application cannot use weighted LoRAs.[^s4]

`ModelCardViewModel.LoadStateFromParameters` attempts installed-model matching by available hashes, versions, and names. It can return when it cannot identify a local model. This route does not itself establish an automatic “recover every missing recipe dependency, download it, then replay” transaction. The separate model browser/download capability should not be credited as such without testing the connecting UI path.[^s5]

## Image and video generation

Current inference documentation lists text-to-image, image-to-image, upscale, Wan text-to-video/image-to-video, and Stable Video Diffusion. A description of Matrix as image-only would be out of date. Saved native tab state and metadata reinjection make within-app iteration convenient.[^s6]

The unresolved part for Remixfun is the exact imported-source journey: does a Civitai image retain every relevant weight and stage, can the baseline be distinguished from an approximation, and does moving a chosen image into video preserve a clear lineage? A general gallery, seed reuse, or tab save is not automatically that experiment model.

## Packaging and license distinctions

The captured stable release includes Windows x64 and Linux x64 archives and an Apple Silicon macOS DMG. The project also documents AppImage/AUR routes. That distribution is materially more polished than running separate setup scripts. Managed packages still have their own hardware and extension constraints; installing Matrix successfully does not prove a selected video model fits a GPU.[^s1]

The README explicitly separates AGPL source from the EULA governing official binaries. The survey records that distinction but does not infer the entire binary EULA from the source license. Any reuse or redistribution decision must inspect the actual distribution being used.[^s1][^s8]

Recent contributors are concentrated around the core maintainers, with visible external contributions. Historical names include aliases. A first-party native inference product and active package management are stronger evidence than stars alone, but no active-user or commercial adoption count was available.

## Comparison with Dreamtime and evaluation

Matrix is ahead on managed installation, package switching, and shared model operations. Dreamtime is closer to the user's focused import detail and existing motion-loop adapters, and its React web UI already fits an optional desktop shell. Rebuilding Matrix's entire package manager would unnecessarily expand Remixfun's scope.

Use Matrix as the onboarding benchmark: a fresh library, one missing checkpoint plus two LoRAs, imported Civitai metadata, baseline generation, saved project reload, and Wan image-to-video. Inspect restored weights and file identities rather than accepting a populated model selector as success. Measure where the user must independently understand Comfy or file layouts.
''')

    dossier('invokeai', 'Invoke / InvokeAI', 'Apache-2.0; component and model terms remain separate',
        'Windows, Linux, macOS; supported accelerators and model families vary',
        'Python application with browser UI; source/package releases and separate launcher distribution',
        'Mature creative application; current Wan video features make it a stronger competitor than older summaries suggest',
        [('README.md', 'Product and installation entry point'), ('pyproject.toml', 'Backend libraries, platform-specific dependencies, and packaging'),
         ('invokeai/frontend/web/package.json', 'React/TypeScript web stack'), ('invokeai/app/api_app.py', 'FastAPI application'),
         ('invokeai/app/services/session_queue', 'Persistent generation queue'), ('invokeai/app/services/model_install', 'Model import/install services'),
         ('invokeai/frontend/web/src/features/metadata/parsing.tsx', 'Metadata handlers and recall'),
         ('invokeai/frontend/web/src/features/gallery/hooks/useRecallAllImageMetadata.ts', 'Gallery recall interaction'),
         ('invokeai/app/services/workflow_records/default_workflows', 'Shipped image/video/interpolation/extension workflows'),
         ('invokeai/app/invocations/wan_video_denoise.py', 'Wan video invocation'), ('LICENSE', 'Apache source license')],
        r'''
## Assessment

Invoke is an established creative application with image generation, editing/canvas workflows, model management, a gallery, and an explicit invocation graph. **The inspected source also contains Wan video, interpolation, and extension workflows.** Treating it as a still-image-only alternative would understate the competition.[^s1][^s9][^s10]

It has a long history, roughly 28k stars, hundreds of historical author names, and ongoing multi-author activity. Those are strong project-health signals, while still not a measured user base. Historical Lincoln Stein-era contributions and current maintainers appear together in the table; their counts should not be read as today's staffing.

## Architecture

The backend is Python with FastAPI, Pydantic, SQLAlchemy/SQLite-backed services, a persistent session queue, model install/load/cache services, and typed invocation nodes. Diffusers/PyTorch and related libraries implement inference. The React/TypeScript frontend uses its own application state, graph construction, canvas/gallery interactions, and API bindings.[^s2][^s3][^s4][^s5][^s6]

Invoke does **not** run Comfy graphs as its core engine. Its invocation graph, model keys, metadata, and queue are its own ecosystem. A new Remixfun UI over Invoke would exchange Comfy custom-node compatibility for Invoke's model and invocation APIs; Dreamtime's existing JSON graphs would not transfer directly.

The separation between model installation, cached loading, invocation execution, and persisted output metadata is valuable. It makes explicit several responsibilities that Dreamtime currently distributes across model jobs, import records, and Comfy's own filesystem state.

## Import, replay, and controlled changes

Gallery metadata recall is a concrete user flow. Handlers restore settings from saved metadata, and richer workflow metadata can reopen a graph. Models are resolved through the application's installed model registry. That is a strong foundation for reproducing Invoke's own outputs and for iterative editing.[^s7][^s8]

The model installer accepts remote/local model sources, including Civitai-oriented URLs. However, the reviewed paths did not establish a single foreign Civitai-image import operation that recovers every original dependency and reconstructs an arbitrary non-Invoke pipeline. A model-source URL and image-generation provenance are different objects.[^s6][^s7]

Invoke is particularly strong for visual remixing through editing, masks, references, and canvas operations. The user here wants an additional form of remix: controlled recipe changes against a recovered baseline. Both can coexist, but evaluating only an inpainting demonstration would miss the core requirement.

## Video scope at this snapshot

The default workflow catalog includes Wan 2.2 text-to-video, image-to-video, two-image interpolation, and video extension, including variants with concept LoRAs and a 5B path. The backend contains video denoising, frame extraction, concatenation, and video output invocations. This is concrete source evidence, not a roadmap inference.[^s9][^s10]

A workflow existing in the catalog does not prove a novice can complete the entire image-remix-to-video journey without changing interfaces or learning nodes. First/last-frame interpolation also does not establish seamless loop quality. Those are usability and output tests still to perform.

## OS, distribution, and license

The Python package explicitly supports Windows/Linux/macOS, and its dependency declarations include platform-specific Torch choices. The source release feed is not the sole distribution channel; launcher delivery is separate. Empty binary attachments on an Invoke source release must not be reported as “no desktop installation.”[^s1][^s2]

Apache-2.0 source is a favorable reuse characteristic compared with copyleft or restricted commercial embedding licenses, but it does not remove third-party library or model terms. The architecture is still a large creative application to inherit.[^s11]

## Comparison with Dreamtime and evaluation

Dreamtime and Invoke share useful application patterns: Python APIs, jobs, persistent models/assets, and a web UI. Their execution engines differ. Dreamtime already has Comfy-specific motion and metadata adapters; adopting Invoke would mean replacing rather than merely packaging that layer.

Evaluate Invoke as a user-facing competitor and as a reference for persistent jobs, model registry design, and metadata recall. Test a foreign recipe, an Invoke-native image, an exact version mismatch, a controlled LoRA change, and a Wan interpolation/extension workflow. The distinction between excellent native round-trip and uncertain foreign reconstruction should remain visible in the results.
''')

    dossier('sdnext', 'SD.Next', 'Apache-2.0 at inspected root; inherited/third-party files need their own review',
        'Windows/Linux/macOS; CUDA, ROCm/ZLUDA, Intel, DirectML/OpenVINO, MPS paths vary by feature',
        'Web server + Python installer; dated releases; Windows launcher referenced separately',
        'Major all-in-one alternative: metadata, Civitai downloads, image/video generation, broad hardware',
        [('README.md', 'Supported workflows/platforms and installation'), ('installer.py', 'Runtime setup'),
         ('modules/processing_diffusers.py', 'Diffusers execution integration'), ('modules/infotext_utils.py', 'Parameter transfer and metadata handling'),
         ('modules/image/metadata.py', 'Image metadata reader'), ('modules/civitai/metadata_civitai.py', 'Local identity and provider metadata'),
         ('modules/civitai/download_civitai.py', 'Download queue, resume, and expected hashes'),
         ('modules/video_models', 'Video loading, execution, caching, and UI'), ('modules/api/api.py', 'Automation API'), ('LICENSE.txt', 'Root source license')],
        r'''
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
''')

    dossier('wan2gp', 'Wan2GP / WanGP', 'Custom WanGP Community License 2.0; restricted commercial embedding/hosting',
        'Windows/Linux primary; early Apple Silicon MPS support exists with documented limitations',
        'Python/Gradio application, setup scripts, headless CLI/API; companion Tauri launcher',
        'Strong video workflow benchmark; commercially restricted implementation is not a default embedding choice',
        [('README.md', 'Current features and install routes'), ('wgp.py', 'Application orchestration and model/runtime dispatch'),
         ('models', 'Model-family implementations and settings'), ('shared/api.py', 'Programmatic generation interface'),
         ('docs/CLI.md', 'Headless saved queues, dry runs, and automation'), ('shared/utils/download.py', 'Model download utility'),
         ('shared/mps/device_patch.py', 'Early Apple Silicon compatibility layer'), ('docs/CHANGELOG.md', 'Version history and MPS limitations'),
         ('LICENSE.txt', 'Binding custom license terms')],
        r'''
## Assessment

WanGP is one of the strongest references for making complex video generation available through ordinary controls, saved settings, queues, and model automation. It does not depend on Comfy. It substantially weakens any claim that the motion half of Remixfun is new by itself.[^s1][^s2][^s5]

The important commercial finding is its **current custom license**. This snapshot should not be described as a clean permissive open-source engine available for unrestricted white-label embedding. Its commercial restrictions cover wrappers/APIs and paid access as well as direct sale of the software.[^s9]

## Architecture

`wgp.py` is a large Python application combining Gradio UI state, generation orchestration, model selection, queues, and media workflow decisions. Model families live under `models`; shared modules handle memory/offloading integration, acceleration, media processing, downloads, and API/CLI access.[^s2][^s3][^s4][^s6]

The architecture gains flexibility through model-specific adapters and configuration, but the central application's size signals coupling between UI controls, runtime tuning, and orchestration. Wrapping it in Tauri solves windowing and installation, not that internal coupling. It also does not make Dreamtime's Comfy graphs directly reusable.

## Video workflow and headless operation

WanGP supports model-specific image/video inputs, continuation/sliding-window behavior, multi-stage execution, LoRAs, and memory profiles. Some current families expose first/last-frame or reference-driven controls. Capabilities vary by model; a shared control surface is not proof every model supports every operation.[^s1][^s2][^s3]

The CLI can process an exported queue ZIP with attached media or a settings JSON with external paths. It supports a dry-run path, output-directory override, and documented exit statuses. This is directly relevant to the requirement that desktop be optional: the executable work description has value independent of the UI session.[^s5]

The package is not primarily a foreign Civitai-image recipe reconstruction product. Downloading a selected model or restoring its own settings is different from recovering an unknown source image's exact original pipeline. The image-remix entry step remains a separate product question.

## Mac, Windows, and Linux

Windows/Linux have detailed installation paths and acceleration choices. Unlike older descriptions, the inspected source **does contain MPS support**: startup applies an Apple Silicon compatibility patch before importing the memory-management layer. It redirects CUDA-oriented operations where possible and disables unsupported compile behavior.[^s2][^s7]

The changelog labels this early Apple support and states performance/optimization and model coverage are limited. Thus the correct classification is early/partial Mac support, not “Mac impossible” and not full cross-platform parity. The shell install route alone would be insufficient evidence; the actual code and explicit limitations are what support this conclusion.[^s7][^s8]

## License and distribution

The binding license permits several free/internal uses and contains conditions for outputs and redistribution, while restricting commercialization of the implementation. Section 1.9 includes paid, metered, sponsored, ad-supported, hosted, SaaS, white-label, OEM, and material paid-product use; later terms govern grants and exceptions. Calling it through a local service or IPC bridge is explicitly within the defined integration surface.[^s9]

For Remixfun, a paid wrapper must not assume process separation bypasses these terms. A separate commercial agreement or a different engine would be needed for restricted uses under the stated license. This is a source-license finding, not an assessment of every third-party component's terms or a decision about Remixfun's business model.

No GitHub release entries were captured for the main repository. Updates are still distributed through source/scripts and versioned change documentation, with a separate Tauri launcher. Absence of releases is not absence of an installable product.[^s1][^s8]

## Comparison with Dreamtime and evaluation

Dreamtime already has a Comfy-based video pipeline with explicit loop/chaining logic and a separate application API. WanGP offers a much larger video-focused feature/optimization surface and portable saved queue concepts. Replacing the engine would sacrifice the existing graph work and introduce license/dependency decisions.

Use it as a functional benchmark: start image, end image, extension, repeatable saved queue, model switch, low-memory profile, and result metadata. Evaluate visual continuity and restart behavior on the same hardware. Study workflow design and capability gating; keep Comfy as the default proposed engine until an actual benchmark or licensing decision warrants changing it.
''')

    dossier('krita-ai-diffusion', 'Krita AI Diffusion', 'GPL-3.0',
        'Krita on Windows/Linux/macOS; managed local or remote Comfy; model-dependent GPU support',
        'Krita plugin ZIP; local server installer or optional cloud connection',
        'Strong visual-remix and managed Comfy reference; different primary interaction from recipe replay',
        [('README.md', 'User goals, features, and installation'), ('ai_diffusion/backend/comfy_client.py', 'Comfy connection'),
         ('ai_diffusion/backend/workflow.py', 'Generation planning'), ('ai_diffusion/backend/server.py', 'Managed runtime setup'),
         ('ai_diffusion/backend/resources.py', 'Required model/node resources'), ('ai_diffusion/model/jobs.py', 'Job state'),
         ('ai_diffusion/persistence.py', 'Document-associated persistence'), ('ai_diffusion/backend/requirements', 'OS/GPU dependency profiles'),
         ('LICENSE', 'GPL source license')],
        r'''
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
''')
