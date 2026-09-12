from research_tools import dossier


def write():
    dossier('comfyui', 'ComfyUI — inference engine and graph server', 'GPL-3.0',
        'Windows/Linux/macOS Apple Silicon; CPU and multiple GPU backends; node/model support varies',
        'Python server, Windows portable archives, separate Desktop/frontend/cloud products',
        'Recommended initial execution engine; existing Dreamtime investment and broad workflow primitives',
        [('README.md', 'Current engine/platform/install scope'), ('main.py', 'Server startup'), ('server.py', 'HTTP/WebSocket API'),
         ('execution.py', 'Graph validation/execution/cache'), ('comfy/model_management.py', 'Device/memory management'),
         ('folder_paths.py', 'Model/file categories'), ('extra_model_paths.yaml.example', 'Shared model path configuration'),
         ('requirements.txt', 'Runtime and frontend package dependencies'), ('LICENSE', 'GPL source license'),
         ('https://docs.comfy.org/installation/system_requirements', 'Official current OS and hardware guidance')],
        r'''
## Assessment

Comfy is a strong initial engine for Remixfun because Dreamtime already builds its graphs and because graph composition expresses the user's important motion operations. A UI can provide presets while preserving an inspectable graph as the execution artifact. Comfy is also a direct competitor through its evolving frontend and desktop product; being built on the engine is not differentiation.[^s1]

## Architecture

The Python process starts the HTTP/WebSocket server, registers nodes and model paths, validates prompts, schedules graph execution, caches reusable results, and emits progress/output events. Model loading and device/memory decisions live beneath the graph layer. The browser frontend is distributed separately from much of the engine code.[^s2][^s3][^s4][^s5][^s8]

This is a natural boundary for a separate Remixfun domain service. The application owns imported records, model identities, experiment lineage, and user jobs; Comfy owns execution of a validated graph. A saved visual workflow and the executable API prompt are related but not identical representations, so both should be retained where available.

## Reproducibility and dependency handling

Comfy images can preserve workflow/prompt metadata, allowing a graph to be recovered without reverse-engineering pixels. That is substantially stronger than prompt text alone. It still does not guarantee the same file bytes under each model name, the same node implementation, or identical numerical behavior on another runtime.[^s1][^s3][^s4]

Model folders and extra-path configuration make it possible to share an existing library rather than duplicate checkpoints for every app. Remixfun should map verified content identities to these paths; a filename in a graph is not itself a content-addressed dependency lock.[^s6][^s7]

Custom nodes make Comfy powerful but expand the compatibility surface. A workflow that runs on one developer machine may need specific node versions, encoders, codecs, and accelerator kernels. A curated preset catalog with runtime profiles is a more manageable first product than promising every downloaded graph will run.

## Platforms and packaging

**Yes, Comfy runs on Mac**, particularly Apple Silicon through PyTorch MPS/Metal. Windows and Linux support multiple accelerator paths, and CPU execution exists. That does not imply large video workflows run acceptably on every Mac or that CUDA-only custom nodes are portable.[^s1][^s5][^s10]

The engine's Python install, Windows portable package, official Desktop application, and cloud service are different distribution surfaces. The separate Desktop dossier records its currently documented Linux/macOS/Windows packaging. Older badges or engine README snippets can lag those product changes; current dedicated documentation and source were checked.[^s1][^s10]

## Popularity, maintenance, and license

Comfy has about 133k stars and substantial recent multi-author activity in the snapshot. That establishes ecosystem attention and active maintenance, not the number of people who would install Remixfun. Its default-branch history began in 2023, while current frontend and desktop repositories have their own ages.

The source is GPL-3.0. Using an external engine does not automatically settle distribution obligations, especially if it or custom nodes are bundled. App source, engine source, individual extensions, and model weights need separate license records.[^s9]

## Comparison with Dreamtime and evaluation

Dreamtime already uses the correct high-level separation: an application API calls a separate Comfy server. The improvement is to make that boundary explicit and portable, with engine discovery, a capability report, a pinned profile, stable job correlation, and output provenance. Avoid scattering raw node IDs through unrelated UI code.

Benchmark a curated image preset and a curated first/last-frame video preset against the original Dreamtime setup. Record Comfy commit, frontend/node-pack versions, Python/Torch/device details, full model hashes, graph, input hashes, and outputs. Keep supporting an existing external Comfy installation as an advanced route; managed installation can become the default once those profiles are tested.
''')

    dossier('comfy-frontend', 'ComfyUI official frontend / App Mode', 'GPL-3.0-only in package manifest',
        'Browser frontend; runs with Comfy on supported host OSes; desktop/cloud builds differ',
        'Versioned frontend packages/releases consumed by Comfy; no independent GPU runtime',
        'Direct baseline for simplified workflow forms; App Mode removes the node-editor requirement',
        [('package.json', 'Frontend build/distribution stack and license'), ('src/stores/appModeStore.ts', 'App input/output state and graph references'),
         ('src/composables/useAppMode.ts', 'Mode lifecycle'), ('src/components/builder', 'Workflow-to-app builder UI'),
         ('src/platform/workflow/management', 'Workflow persistence and management'), ('src/scripts', 'Graph/API integration'),
         ('LICENSE', 'GPL source text'), ('https://docs.comfy.org/interface/app-mode', 'Official App Mode guide and cloud-only sharing distinction')],
        r'''
## Assessment

The official frontend materially changes the novelty argument. **App Mode already turns a Comfy workflow into a simpler input/output interface**, with selected controls, outputs, preview, and a default app view. Remixfun cannot claim novelty merely for replacing a node graph with a form.[^s2][^s4][^s8]

This repository should be evaluated separately from the Python engine and Electron desktop manager. Their versions, licenses, contributors, and release surfaces differ, even though users experience them together.

## Architecture

The source is a Vue/TypeScript frontend using Pinia and Vite, with graph editing/integration, workflow management, UI state, and separate distribution modes. The package has desktop and cloud build variants. Its job is to present/control graphs and communicate with the backend, not perform inference itself.[^s1][^s5][^s6]

App Mode stores selected inputs and outputs as references into workflow graph entities. It must resolve node/widget identifiers, handle subgraphs, prune invalid references, and keep the app presentation synchronized as the graph changes. This exposes a subtle maintenance cost of generic workflow forms: UI metadata is coupled to evolving graph structure.[^s2][^s3][^s4]

Dreamtime takes a different approach: purpose-built React pages call known model adapters. That is less generic, but it gives the product a stronger task model and fewer arbitrary-widget compatibility obligations.

## What App Mode does and does not establish

The official guide describes a builder sequence for inputs, outputs, preview, and default view, followed by ordinary run/cancel and output interactions. It is intended to make a prepared workflow usable without editing nodes. The same guide distinguishes cloud-only share links from local workflow saving.[^s8]

App Mode starts with a workflow. It does not by itself prove that a Civitai image without its graph can be reconstructed, every missing model identified by exact hash/version, or a source baseline compared through controlled experiments. Those are separate functions that a plugin or Remixfun could add.

For video presets, however, it already provides much of the desired presentation mechanism. A well-authored first/last-frame graph could be packaged as an app-shaped workflow. The build-versus-integrate question should include whether that existing mode plus a focused import/lineage extension is sufficient.

## Distribution, license, and maintenance

The package manifest records GPL-3.0-only. Frontend releases are normally consumed alongside Comfy rather than downloaded as a standalone native generator. Cloud build capabilities should not automatically be attributed to the local build.[^s1][^s7]

Active frontend development brings improvements but also potential extension/API churn. A Remixfun interface using Comfy's server API can reduce its exposure to internal frontend changes; a panel extension gains host integration while accepting that coupling. This is an architecture tradeoff, not a universal preference for one route.

## Comparison with Dreamtime and evaluation

Dreamtime's standalone image/video screens provide application-specific interactions outside Comfy's editor. Compare those screens against App Mode using the exact same underlying graph before building more UI. If App Mode already presents the important controls well, the strongest custom work is source recovery, dependency explanation, experiments, and lineage.

Test node renames, workflow updates, missing models, file inputs, video outputs, and switching between app and graph views. Keep sharing tests separate for local files and cloud URLs. The evaluation should determine whether an independent product materially shortens the target task rather than simply reskinning a workflow form.
''')

    dossier('stable-diffusion-cpp', 'stable-diffusion.cpp', 'MIT',
        'Windows/Linux/macOS plus additional targets; CPU/CUDA/Vulkan/Metal/OpenCL/SYCL',
        'Native CLI/library/server; rolling platform/backend-specific archives and web UI',
        'Most relevant alternative native runtime; attractive packaging, different reproduction semantics',
        [('README.md', 'Model/backend/platform scope'), ('CMakeLists.txt', 'Native build boundary'),
         ('src/stable-diffusion.cpp', 'Core inference implementation'), ('examples/cli', 'Command-line application and metadata handling'),
         ('examples/server/README.md', 'HTTP server and web UI'), ('examples/server/runtime.cpp', 'Server runtime'),
         ('examples/server/async_jobs.cpp', 'Asynchronous jobs'), ('docs/wan.md', 'Wan model-specific usage'),
         ('LICENSE', 'MIT source license')],
        r'''
## Assessment

This is the clearest alternative if Remixfun later prioritizes a native runtime and simpler binary distribution over Comfy graph compatibility. It implements diffusion in C/C++ using ggml and supports both image and video families. It is not merely an old Stable Diffusion CLI.[^s1][^s3][^s8]

## Architecture

The repository provides a native inference library plus CLI and server applications. CMake selects build/backend options. The server has routing, runtime ownership, asynchronous jobs, and a web interface; the CLI handles model/parameter options and output metadata. No Python environment is required for the central native runtime.[^s2][^s3][^s4][^s5][^s6][^s7]

That reduces one major desktop-support burden, but it replaces Comfy's node ecosystem with this project's model implementations and API. Dreamtime graph JSON and custom-node chains cannot simply be executed by the native library. Video chaining, conditioning, and interpolation would need new adapters or separate processing.

## Reproduction and model handling

The project supports multiple weight formats, LoRAs, quantization, and selected conditioning/postprocessing features. Its CLI can emit WebUI-style generation metadata. The README documents RNG modes intended to align noise generation with familiar WebUI/Comfy conventions.[^s1][^s4]

Noise alignment is not a guarantee of whole-image equality. Prompt parsing, sampler implementation, precision, quantization, model conversion, and VAE behavior can still differ. An imported Civitai image made with PyTorch/Comfy needs a new compatibility assessment when replayed through this engine, even if the seed and model name match.

No complete Civitai-image import and dependency-recovery product was established in this repository. It supplies execution primitives; Remixfun would still own provider metadata, model identity/download policy, baseline/variant records, and motion lineage.

## OS, releases, and license

The project documents Windows/Linux/macOS and several accelerator backends. The captured release assets include native archives for multiple OS/backend combinations; tags are rolling `master-...` builds rather than a single stable semantic version. Do not interpret one binary working as every backend being equivalent.[^s1][^s2]

The MIT source license is attractive for reuse, with separately licensed model weights and bundled components. The README warns that API/CLI options can change during active development; an adapter should pin a version rather than track arbitrary latest binaries.[^s1][^s9]

## Comparison with Dreamtime and recommendation

Comfy preserves the most existing Dreamtime work and supports its graph-centric video operations. stable-diffusion.cpp could provide a second lightweight engine, particularly for a curated cross-platform image path, once Remixfun has a stable engine interface. It should not be selected merely because the executable is smaller if that forces a substantial loss of recipe fidelity and video capability.

Evaluate a small, fixed set of supported recipes across Comfy and this runtime. Compare exact bytes, decoded pixels, and visual differences separately, and record all runtime/quantization changes. Measure install size, startup, memory, and generation speed on actual target hardware; none of those performance measurements were performed in this survey.
''')

    dossier('draw-things', 'Draw Things community core', 'GPL-3.0 public core; full consumer app is not all in this repository',
        'Apple-native consumer app; public macOS CLI/server and CUDA Linux server path; no Windows app established',
        'Consumer Apple app separately; macOS CLI/gRPC binaries and Linux server/container path',
        'Apple performance/product benchmark and possible remote runtime; not a ready cross-platform UI base',
        [('README.md', 'Public/private boundary, CLI, and server distribution'), ('Package.swift', 'Swift packages and products'),
         ('Libraries', 'Public model, sampler, and supporting libraries'), ('Apps', 'Public command-line/server targets'),
         ('LICENSE.md', 'Public source license'), ('CLA', 'Contribution agreement')],
        r'''
## Assessment

Draw Things demonstrates that a local Apple-focused generation product can offer a polished experience without Comfy. It is relevant to the user's Mac question, but the public community repository is **not the entire consumer application's source**. Treating it as a complete desktop app ready to port would misrepresent the repository.[^s1]

## Architecture

The public Swift code includes model implementations, samplers, data models, training-related functionality, and CLI/server products. Swift Package Manager/Bazel-related build files organize a substantial native inference stack. The README says the consumer app lives in a private monorepository with code synchronized into this community repository.[^s1][^s2][^s3][^s4]

There are two useful execution surfaces: local command-line generation/training on Mac and a gRPC server that can be used for offloaded inference. The server has a documented CUDA Linux path. This is more portable at the backend level than a description of “Mac-only code” suggests, but it does not establish a Windows-native consumer interface.[^s1][^s2]

## Relationship to import and remix

Model import, generation settings, and efficient native execution make Draw Things a practical user alternative for some image tasks. The reviewed public repository did not establish a complete arbitrary Civitai-image dependency-recovery and exact replay journey. Public core capabilities also cannot prove the current behavior of every private app screen.[^s1][^s3]

An Apple-native implementation has its own sampler, precision, model conversion, and execution semantics. Even where equivalent concepts exist, a Dreamtime/Comfy recipe needs translation and a new fidelity assessment. Output that looks close should not be classified as the original deterministic baseline solely because the seed matches.

The most useful comparison is product behavior on Mac: install experience, model storage, responsiveness, and the distinction between local and remote generation. This survey did not benchmark Apple hardware or independently test consumer-app workflows.

## Distribution, license, and contributors

The public release feed includes CLI/gRPC binaries; the consumer app is distributed separately through Apple's ecosystem. Linux serving is documented through a CUDA container route. The source repository's age and stars describe the public core, not the age, installs, or revenue of the consumer app.[^s1]

The public code is GPL-3.0 and contributions use a CLA. That does not make the private UI available under the same practical source-access conditions. Historical authorship is concentrated around Liu Liu and several name variants of other core contributors; author-name totals do not establish staffing.[^s5][^s6]

## Comparison with Dreamtime and evaluation

Dreamtime's React/Python/Comfy implementation is already aligned with Windows/Linux and a browser frontend. A Swift engine adoption would be a substantial new adapter and toolchain, without obtaining the private polished interface. Keep Draw Things as an Apple UX/runtime benchmark rather than the initial Remixfun foundation.

For a later Mac feasibility study, test a known supported image recipe locally and through the gRPC path; record model conversion, sampler differences, memory, speed, and recovered metadata. Compare it with Comfy MPS and stable-diffusion.cpp Metal on the same machine before deciding whether a second engine earns its maintenance cost.
''')

    dossier('civitai-cli', 'Official Civitai CLI', 'Apache-2.0',
        'Static binaries for Windows/Linux/macOS, x64 and ARM64',
        'Go binary; archives, npm/Homebrew/Nix/source install routes',
        'Provider integration/download reference; also a cloud generation/App toolchain, not a local inference engine',
        [('README.md', 'CLI capabilities, auth boundaries, and distribution'), ('go.mod', 'Go module/dependencies'),
         ('pkg/civitai/images.go', 'Image API client'), ('pkg/civitai/model_versions.go', 'Version identity API'),
         ('pkg/civitai/hashes.go', 'Hash lookups'), ('pkg/civitai/download.go', 'Download client and integrity behavior'),
         ('pkg/civitai/retry.go', 'Retry semantics'), ('LICENSE', 'Apache source license')],
        r'''
## Assessment

The official CLI is a useful primary-source reference for current provider behavior, file identity, downloads, authentication, and machine-readable output. It can complement Remixfun's local pipeline. It is not itself a local GPU generation engine or a replacement for the application's recipe/experiment UI.[^s1]

The current CLI also includes Civitai cloud generation and an App authoring/submission toolchain. Describing it as read/download-only would be incomplete. Those features have separate credentials, availability, and cost semantics and were not invoked during this research.[^s1]

## Architecture

Go code produces a static command-line executable with reusable provider client modules. Image queries, model versions, hash lookup, downloads, retries, and other resource types are separated in `pkg/civitai`. A frontend or Python service could call a supported CLI operation or independently implement an adapter from documented API behavior.[^s2][^s3][^s4][^s5][^s6][^s7]

For Remixfun, the clean division is provider evidence → dependency plan → local execution. The CLI can help with the first two, but it should not own the canonical recipe or silently decide which engine/model substitution becomes a baseline.

## Workflow coverage and limitations

Model version/hash queries and downloading are directly relevant to missing-dependency resolution. Download and retry behavior offer a better reference than scraping arbitrary website pages. The CLI documents structured JSON output and dry-run/planning-oriented usage for automation.[^s1][^s4][^s5][^s6][^s7]

Obtaining metadata does not guarantee that metadata is complete. Civitai images can have missing fields, detached resources, or recipes originating in another engine. The CLI's own cloud generation path also documents model/ecosystem and substitution concerns; it should not be confused with guaranteed local reproduction of the source image.[^s1]

The App toolchain is platform-specific and described as beta/invite-gated for some operations in the inspected README. A Remixfun local application should not depend on access to that program for its basic import and generation functions.

## Release, license, and maturity

The repository is young but very active, with source history concentrated around the primary maintainer and a few other author names. Low stars do not mean it is irrelevant: official provider code can be valuable with little consumer GitHub attention. Conversely, official ownership is not proof of API stability or broad adoption.

Captured release assets include Windows/Linux/macOS binaries for x64/ARM64 plus archives/checksums and package-manager support. This is a much simpler packaging surface than a Python/PyTorch engine. Apache-2.0 source does not determine the provider's service terms or the licenses of downloaded models.[^s1][^s8]

## Comparison with Dreamtime and evaluation

Dreamtime has its own `civitai.py` with REST and tRPC fallback. Compare its supported endpoints and failure handling with this official client before deepening reliance on undocumented website calls. A thin provider interface would let Remixfun change acquisition strategy without rewriting recipe and experiment logic.

Test public reads, unavailable images, version lookup, hash lookup, interrupted downloads, and structured errors with non-sensitive fixtures. No authentication, downloads of model weights, cloud generation, App submission, or paid operations were performed in this survey. Keep provenance evidence even when provider calls stop working later.
''')
