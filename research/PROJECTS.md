# Project dossiers

28 source and architecture reviews, captured 2026-09-12. Each dossier includes popularity/age, historical and recent contributors, release evidence, OS/runtime distinctions, license findings, architecture, workflow coverage, and comparison with Dreamtime.

| Project | Role in this survey |
|---|---|
| [Dreamtime — existing implementation](projects/dreamtime.md) | Primary extraction source: import, model inventory, image and video adapters |
| [CiviImport](projects/civiimport.md) | Direct Civitai URL → missing models → reconstructed Comfy graph competitor |
| [ComfyUI-Unbake](projects/unbake.md) | Closest conceptual competitor for provenance-aware replay and controlled comparisons |
| [ComfyUI LoRA Manager](projects/lora-manager.md) | Strongest model/recipe collection reference in the direct remix shortlist |
| [ComfyUI Civitai Toolkit](projects/civitai-toolkit.md) | Integrated Civitai browsing, local inventory, recipe diagnostics |
| [genrecord](projects/genrecord.md) | Reference for normalized evidence, sufficiency, provenance, and variation planning |
| [SwarmUI](projects/swarmui.md) | Strongest established Comfy-based general-purpose app benchmark |
| [Stability Matrix](projects/stability-matrix.md) | Strongest combined installer, shared-model library, and native Comfy inference competitor |
| [Invoke / InvokeAI](projects/invokeai.md) | Mature creative application; current Wan video features make it a stronger competitor than older summaries suggest |
| [SD.Next](projects/sdnext.md) | Major all-in-one alternative: metadata, Civitai downloads, image/video generation, broad hardware |
| [Wan2GP / WanGP](projects/wan2gp.md) | Strong video workflow benchmark; commercially restricted implementation is not a default embedding choice |
| [Krita AI Diffusion](projects/krita-ai-diffusion.md) | Strong visual-remix and managed Comfy reference; different primary interaction from recipe replay |
| [ComfyUI — inference engine and graph server](projects/comfyui.md) | Recommended initial execution engine; existing Dreamtime investment and broad workflow primitives |
| [ComfyUI official frontend / App Mode](projects/comfy-frontend.md) | Direct baseline for simplified workflow forms; App Mode removes the node-editor requirement |
| [stable-diffusion.cpp](projects/stable-diffusion-cpp.md) | Most relevant alternative native runtime; attractive packaging, different reproduction semantics |
| [Draw Things community core](projects/draw-things.md) | Apple performance/product benchmark and possible remote runtime; not a ready cross-platform UI base |
| [Official Civitai CLI](projects/civitai-cli.md) | Provider integration/download reference; also a cloud generation/App toolchain, not a local inference engine |
| [Desktop Release Kit — distribution baseline](projects/desktop-release-kit.md) | Adopt release contracts and validation patterns; not a Python/GPU/model installer |
| [Comfy Desktop](projects/comfy-desktop.md) | Primary benchmark for managed Comfy installation, instances, snapshots, and recovery |
| [Wan2GP Desktop Tauri launcher](projects/wan2gp-desktop.md) | Very close packaging concept, very young implementation, unresolved license |
| [Pinokio](projects/pinokio.md) | Established onboarding alternative; not a recipe-reproduction application |
| [ViewComfy](projects/viewcomfy.md) | Prepared Comfy workflow → approachable form; not a foreign recipe resolver |
| [SDFX](projects/sdfx.md) | Useful declarative workflow/UI architecture; stale default branch makes it a poor primary dependency |
| [Visionatrix](projects/visionatrix.md) | Closest service/worker/preset architecture reference; archived, so not recommended as maintained foundation |
| [AUTOMATIC1111 Stable Diffusion WebUI](projects/automatic1111.md) | Historical metadata/parameter-reuse baseline; major attention, limited recent default-branch activity |
| [Stable Diffusion WebUI Forge](projects/forge.md) | A1111-compatible interaction and memory optimization reference; inspected original fork is not all Forge descendants |
| [Fooocus](projects/fooocus.md) | Simplicity/preset UX benchmark; limited SDXL-focused LTS, not a modern general video foundation |
| [Easy Diffusion](projects/easy-diffusion.md) | Established simple installation/image workflow reference; not proven full Civitai replay-to-video product |

Start with the [landscape synthesis](LANDSCAPE.md), then use the [repository matrix](REPOSITORY-MATRIX.md) to compare metrics and distribution. Source evidence is linked within each dossier.
