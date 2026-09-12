from research_tools import dossier


def write():
    dossier('automatic1111', 'AUTOMATIC1111 Stable Diffusion WebUI', 'AGPL-3.0',
        'Windows/Linux; Apple Silicon instructions exist; hardware/extensions vary',
        'Python/Gradio web app, launch scripts, Windows portable-style assets; extensions',
        'Historical metadata/parameter-reuse baseline; major attention, limited recent default-branch activity',
        [('README.md', 'PNG Info reuse, XY plots, installation, and features'), ('modules/infotext_utils.py', 'Metadata parsing and parameter transfer'),
         ('modules/processing.py', 'Generation pipeline and saved parameters'), ('modules/sd_models.py', 'Checkpoint inventory and loading'),
         ('scripts/xyz_grid.py', 'Controlled parameter grid'), ('modules/api/api.py', 'Automation API'), ('LICENSE.txt', 'AGPL license')],
        r'''
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
''')

    dossier('forge', 'Stable Diffusion WebUI Forge', 'AGPL-3.0 at root; substantial inherited code',
        'Windows/Linux primarily; inherited/general platform paths do not establish full Mac parity',
        'Python/Gradio web app, Windows one-click archives, source/rolling releases',
        'A1111-compatible interaction and memory optimization reference; inspected original fork is not all Forge descendants',
        [('README.md', 'Lineage, install routes, and stated compatibility'), ('backend/memory_management.py', 'Memory/offload policy'),
         ('backend/loader.py', 'Model loading'), ('backend/diffusion_engine', 'Model-family execution'),
         ('modules/infotext_utils.py', 'Inherited parameter import'), ('LICENSE.txt', 'AGPL license')],
        r'''
## Assessment

Forge is relevant because many users want A1111-style parameter reuse with improved model loading and memory behavior. It offers familiar image-generation controls rather than requiring a graph editor. The inspected repository is the original `lllyasviel` Forge, not an aggregate of every later Forge-branded fork.[^s1]

## Architecture and inheritance

Forge retains much of the WebUI/Gradio application and adds a backend layer for loading, model-family execution, memory management, patching, attention, and quantized operations. This is an alternative inference implementation with inherited UI conventions, not a Comfy frontend.[^s2][^s3][^s4]

The inheritance is visible in contributor counts: prominent A1111 authors account for substantial historical commits. A count of hundreds of author names does not mean Forge has that many original contributors or active maintainers. Its original-fork default branch shows no recent 90-day commits in the snapshot.

## Import/reproduce/remix coverage

Metadata import and parameter transfer inherit the useful WebUI workflow. Users can restore source settings and edit them in familiar controls. Whether a recipe reproduces depends on the original engine/version, model files, backend precision, extensions, and hidden generation stages.[^s1][^s5]

The reviewed base paths do not establish automatic Civitai-image dependency recovery with a verified baseline and persistent experiment lineage. A compatible prompt box and model selector are necessary but insufficient for that promise. Likewise, generic image operations should not be counted as a complete first/last-frame video journey.

## Distribution and source terms

Windows archives reduce setup burden, while source launch paths support other environments with hardware-specific constraints. The release feed includes rolling/previous-version entries; its first item is not necessarily a stable latest release. Current support should be assessed against the exact repository and artifact, not a community tutorial for a different fork.[^s1]

AGPL-3.0 governs the root source. Inherited and external components retain their own notices and model licenses. Nothing about a memory-optimization backend grants permission for unrelated downloaded content.[^s6]

## Comparison with Dreamtime and evaluation

Dreamtime is already closer to Remixfun's independent web API and Comfy video graph model. Forge is useful as a source-format and execution-semantics benchmark, especially for Civitai images generated with Forge. Migrating to it would replace the graph engine and its existing video adapters.

Test a Forge-native metadata image, exact local checkpoint/LoRA identities, and a controlled parameter change. Compare original Forge output with the Comfy reconstruction, explicitly recording precision and sampler/RNG differences. Treat newer descendants as a future focused follow-up, not as features silently credited to this clone.
''')

    dossier('fooocus', 'Fooocus', 'GPL-3.0',
        'Windows/Linux; Mac MPS guidance is explicitly less tested; model/hardware scope constrained',
        'Gradio app with Windows archive and automatic preset-model downloads; source scripts',
        'Simplicity/preset UX benchmark; limited SDXL-focused LTS, not a modern general video foundation',
        [('readme.md', 'Product goals, explicit LTS status, presets, and OS caveats'), ('modules/default_pipeline.py', 'Generation pipeline'),
         ('modules/async_worker.py', 'Task execution and UI coordination'), ('modules/meta_parser.py', 'Metadata formats and reconstruction'),
         ('modules/config.py', 'Presets/model configuration'), ('LICENSE', 'GPL source license')],
        r'''
## Assessment

Fooocus is an important precedent for making local generation approachable through strong defaults and automatic model downloads. It is not a strong initial engine choice for the requested modern image/video application: the README explicitly declares limited SDXL-focused long-term support with bug fixes and no current plan to add newer architectures.[^s1]

## Architecture

Python/Gradio UI state feeds an asynchronous worker and a model pipeline. Presets/configuration determine models, styles, and generation behavior. Metadata parsing can recover settings, while the app also performs prompt processing and generation improvements intended to produce good results with fewer exposed controls.[^s2][^s3][^s4][^s5]

This is useful UX research: model presets and automatic setup can substantially reduce user effort. It also shows a conflict with strict source replay. Helpful prompt expansion or automatically selected defaults change the effective recipe unless recorded and explicitly enabled.

## Workflow coverage

Fooocus handles image generation, variations, inpainting/outpainting, references, and metadata-oriented reuse. It can download preset models, but that is not proof that it resolves every exact dependency of an arbitrary Civitai image. Its own conventions and enhancements make cross-engine fidelity a separate question.[^s1][^s4][^s5]

The reviewed application does not provide the requested modern first/last-frame video flow. A simplified image UI and a very large historical star count should not be used to infer a broader model roadmap that the project explicitly disclaims.

## Platforms, maintenance, and license

Windows has a downloadable archive; Linux uses source/scripts; Mac guidance is explicitly described as less intensively tested. Historical performance numbers in the README are not reproduced as current benchmark results. Modern hardware and models need fresh measurement.[^s1]

The repository has over 53k stars but no recent default-branch commits in this snapshot. Its explicit LTS statement is stronger evidence of scope than the activity count alone. The actual source license is **GPL-3.0**, not AGPL; the root text and GitHub classification agree.[^s6]

## Comparison with Dreamtime and evaluation

Dreamtime already covers more of the desired image/video breadth and offers explicit model-specific graph templates. Fooocus is useful for preset onboarding, progressive disclosure, and low-friction image editing, but replacing Dreamtime with it would narrow the product.

Evaluate whether a first-time user can download only the necessary preset models, understand generation defaults, and recover the effective expanded prompt/settings. Remixfun should borrow simplicity while preserving a strict mode where imported baseline settings are not silently enhanced.
''')

    dossier('easy-diffusion', 'Easy Diffusion', 'Custom MIT-style license with use-based restrictions; not plain MIT',
        'Windows/Linux/macOS; runtime/backend and hardware support vary',
        'Windows installer, Linux/Mac archives, Python/FastAPI web app; evolving v4 engine paths',
        'Established simple installation/image workflow reference; not proven full Civitai replay-to-video product',
        [('README.md', 'Installers, current engine changes, and user features'), ('ui/easydiffusion/server.py', 'FastAPI and backend selection'),
         ('ui/easydiffusion/task_manager.py', 'Device threads and task cache'), ('ui/easydiffusion', 'Application/model/task modules'),
         ('scripts', 'Cross-platform bootstrap/runtime setup'), ('LICENSE', 'Custom use-restricted software license')],
        r'''
## Assessment

Easy Diffusion is a relevant baseline for approachable local installation, a simple browser UI, queued tasks, image variations, and automatic model handling. It should not be written off as an untouched 2022 prototype: the current README/source include an evolving v4 engine path and newer image model families.[^s1][^s2]

## Architecture

The Python FastAPI service exposes generation and configuration endpoints, serves static UI assets, and dispatches work through model/device/task modules. The task manager organizes render threads and temporary task/result state. Source shows sdkit/torchruntime integration and configurable backend choices; setup scripts bootstrap the environment.[^s2][^s3][^s4][^s5]

This differs from Dreamtime's persistent application job model over an external Comfy server. A temporary queue/cache is useful for interactive generation, but durable source/baseline/variant provenance would need its own persistence rather than relying on a render thread's lifetime.

## Target workflow coverage

The app offers text-to-image, image-to-image, inpainting, variations, prompt combinations, custom models, and postprocessing. These satisfy common creative tasks and can make local generation accessible. The review did not establish arbitrary Civitai-image exact dependency recovery or a unified first/last-frame/loop video workflow.[^s1][^s4]

Its “loopback” image feature should not be counted as a temporally coherent video loop; it feeds an image result into another image task. Likewise, a low historical minimum GPU requirement for basic images says little about modern video-model feasibility.

## Distribution, license, and maintenance

Captured releases include a Windows executable installer and Linux/Mac archives. The source has Windows-specific path/runtime setup and cross-platform startup scripts, illustrating practical issues that persist beneath a friendly UI.[^s1][^s5]

The license starts with MIT-like grants but adds use-based restrictions in Section II/Attachment A. GitHub marks it `NOASSERTION`. It should be recorded as a **custom restricted license**, not plain MIT merely because the opening paragraphs look familiar. Downloaded models have additional independent terms.[^s6]

Recent activity is modest but nonzero, largely concentrated around cmdr2. Roughly 10.5k stars measure accumulated attention; the current engine transition and actual release behavior are more useful than assuming old popularity proves current feature completeness.

## Comparison with Dreamtime and evaluation

Easy Diffusion is a good first-install and simple-queue benchmark. Dreamtime is closer to the desired recipe-import and advanced motion primitives, with an application API already separated from inference. Its source is therefore an onboarding reference rather than an obvious replacement engine.

Evaluate a fresh install, switching a supported model, repeated variations, interrupted tasks, and preservation of effective parameters. Test the latest source and the distributed release separately when their engine capabilities differ. Do not credit source-only v4 additions as independently verified stable installer behavior.
''')
