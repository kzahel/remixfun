# Repository comparison matrix

Snapshot: 2026-09-12. Figures come from the linked evidence files; definitions and limits are in [METHODOLOGY.md](METHODOLOGY.md). Dates and activity refer to the inspected branch, not necessarily the latest shipped product. Full contributor names, release samples, architecture, and citations are in each dossier.

| Project | Created | Stars | Forks | Author names: history / 90d | Nonmerge commits: 90d | HEAD date | Archived |
|---|---|---:|---:|---:|---:|---|---|
| [Dreamtime — existing implementation](projects/dreamtime.md) | unknown | — | — | 1 / 0 | 0 | 2026-03-30 | unknown |
| [CiviImport](projects/civiimport.md) | 2026-09-06 | 1 | 0 | 1 / 1 | 6 | 2026-09-06 | False |
| [ComfyUI-Unbake](projects/unbake.md) | 2026-08-25 | 0 | 0 | 2 / 2 | 39 | 2026-09-09 | False |
| [ComfyUI LoRA Manager](projects/lora-manager.md) | 2025-01-27 | 1454 | 147 | 33 / 8 | 509 | 2026-09-11 | False |
| [ComfyUI Civitai Toolkit](projects/civitai-toolkit.md) | 2025-08-29 | 142 | 7 | 2 / 0 | 0 | 2026-02-19 | False |
| [genrecord](projects/genrecord.md) | 2026-08-19 | 0 | 0 | 1 / 1 | 2 | 2026-08-20 | False |
| [SwarmUI](projects/swarmui.md) | 2024-06-21 | 4549 | 460 | 77 / 6 | 277 | 2026-09-10 | False |
| [Stability Matrix](projects/stability-matrix.md) | 2023-06-13 | 8763 | 598 | 35 / 8 | 153 | 2026-09-10 | False |
| [Invoke / InvokeAI](projects/invokeai.md) | 2022-08-17 | 28193 | 2970 | 422 / 28 | 174 | 2026-09-06 | False |
| [SD.Next](projects/sdnext.md) | 2022-12-24 | 7338 | 583 | 525 / 13 | 651 | 2026-08-26 | False |
| [Wan2GP / WanGP](projects/wan2gp.md) | 2025-02-27 | 9293 | 1468 | 36 / 4 | 174 | 2026-09-07 | False |
| [Krita AI Diffusion](projects/krita-ai-diffusion.md) | 2023-09-01 | 10571 | 625 | 51 / 6 | 40 | 2026-08-23 | False |
| [ComfyUI — inference engine and graph server](projects/comfyui.md) | 2023-01-17 | 132635 | 15654 | 368 / 56 | 491 | 2026-09-11 | False |
| [ComfyUI official frontend / App Mode](projects/comfy-frontend.md) | 2024-06-13 | 2006 | 696 | 250 / 61 | 1588 | 2026-09-12 | False |
| [stable-diffusion.cpp](projects/stable-diffusion-cpp.md) | 2023-08-13 | 6964 | 782 | 106 / 31 | 164 | 2026-09-12 | False |
| [Draw Things community core](projects/draw-things.md) | 2023-11-19 | 556 | 67 | 9 / 6 | 173 | 2026-09-11 | False |
| [Official Civitai CLI](projects/civitai-cli.md) | 2026-06-18 | 10 | 1 | 3 / 3 | 437 | 2026-09-12 | False |
| [Desktop Release Kit — distribution baseline](projects/desktop-release-kit.md) | 2026-08-09 | 0 | 0 | 1 / 1 | 10 | 2026-09-05 | False |
| [Comfy Desktop](projects/comfy-desktop.md) | 2026-02-13 | 446 | 59 | 17 / 14 | 184 | 2026-09-12 | False |
| [Wan2GP Desktop Tauri launcher](projects/wan2gp-desktop.md) | 2026-09-03 | 12 | 0 | 2 / 2 | 218 | 2026-09-11 | False |
| [Pinokio](projects/pinokio.md) | 2023-07-09 | 8018 | 807 | 1 / 1 | 157 | 2026-09-02 | False |
| [ViewComfy](projects/viewcomfy.md) | 2024-09-27 | 668 | 85 | 3 / 0 | 0 | 2026-03-19 | False |
| [SDFX](projects/sdfx.md) | 2024-04-09 | 445 | 32 | 5 / 0 | 0 | 2025-05-01 | False |
| [Visionatrix](projects/visionatrix.md) | 2024-02-29 | 169 | 16 | 8 / 0 | 0 | 2025-12-12 | True |
| [AUTOMATIC1111 Stable Diffusion WebUI](projects/automatic1111.md) | 2022-08-22 | 164897 | 30549 | 641 / 0 | 0 | 2024-07-27 | False |
| [Stable Diffusion WebUI Forge](projects/forge.md) | 2024-01-14 | 13003 | 1727 | 639 / 0 | 0 | 2025-06-26 | False |
| [Fooocus](projects/fooocus.md) | 2023-08-09 | 53008 | 8603 | 61 / 0 | 0 | 2025-09-02 | False |
| [Easy Diffusion](projects/easy-diffusion.md) | 2022-08-23 | 10462 | 862 | 58 / 2 | 21 | 2026-09-11 | False |

## License, platform, and distribution

These are software-source assessments. Models, bundled components, paid services, and branded binaries can have additional terms. “Cross-platform” never implies every model and GPU combination works.

| Project | Source license | OS / hardware | Distribution | Role |
|---|---|---|---|---|
| [Dreamtime — existing implementation](projects/dreamtime.md) | No tracked root license found; user-owned local baseline, third-party obligations remain | Existing development/deployment assumes Linux; browser client is portable; GPU support depends on Comfy | Source checkout, Python service + Vite web frontend; no desktop release found | Primary extraction source: import, model inventory, image and video adapters |
| [CiviImport](projects/civiimport.md) | MIT | ComfyUI extension; OS and GPU support inherit the host and graph nodes | Git/custom-node installation; no release feed or desktop installer captured | Direct Civitai URL → missing models → reconstructed Comfy graph competitor |
| [ComfyUI-Unbake](projects/unbake.md) | GPL-3.0 family; README adds “Not for sale” language requiring clarification | Browser extension + Python Comfy routes; host-dependent Windows/Linux/macOS | Custom-node source installation; no GitHub releases captured | Closest conceptual competitor for provenance-aware replay and controlled comparisons |
| [ComfyUI LoRA Manager](projects/lora-manager.md) | AGPL-3.0 | Comfy extension or standalone Python web app; model execution depends on a separate engine | Comfy custom-node installation, portable standalone option, source releases | Strongest model/recipe collection reference in the direct remix shortlist |
| [ComfyUI Civitai Toolkit](projects/civitai-toolkit.md) | MIT | Runs inside Comfy; host-dependent OS/GPU support | Custom-node source installation and tagged source releases | Integrated Civitai browsing, local inventory, recipe diagnostics |
| [genrecord](projects/genrecord.md) | AGPL-3.0 with a documented commercial licensing option | Portable JavaScript library; no GPU, network, UI, or server required | Library source/package; no GitHub releases captured | Reference for normalized evidence, sufficiency, provenance, and variation planning |
| [SwarmUI](projects/swarmui.md) | MIT | Windows/Linux/macOS application server; actual model/GPU support comes from configured backends | Install/run scripts and web UI; beta source releases; external Comfy processes | Strongest established Comfy-based general-purpose app benchmark |
| [Stability Matrix](projects/stability-matrix.md) | AGPL-3.0 source; official binaries have a separately linked EULA | Windows x64, Linux x64, macOS Apple Silicon; packages and GPU support vary | Native Avalonia desktop; Windows/Linux archives and macOS DMG; managed AI packages | Strongest combined installer, shared-model library, and native Comfy inference competitor |
| [Invoke / InvokeAI](projects/invokeai.md) | Apache-2.0; component and model terms remain separate | Windows, Linux, macOS; supported accelerators and model families vary | Python application with browser UI; source/package releases and separate launcher distribution | Mature creative application; current Wan video features make it a stronger competitor than older summaries suggest |
| [SD.Next](projects/sdnext.md) | Apache-2.0 at inspected root; inherited/third-party files need their own review | Windows/Linux/macOS; CUDA, ROCm/ZLUDA, Intel, DirectML/OpenVINO, MPS paths vary by feature | Web server + Python installer; dated releases; Windows launcher referenced separately | Major all-in-one alternative: metadata, Civitai downloads, image/video generation, broad hardware |
| [Wan2GP / WanGP](projects/wan2gp.md) | Custom WanGP Community License 2.0; restricted commercial embedding/hosting | Windows/Linux primary; early Apple Silicon MPS support exists with documented limitations | Python/Gradio application, setup scripts, headless CLI/API; companion Tauri launcher | Strong video workflow benchmark; commercially restricted implementation is not a default embedding choice |
| [Krita AI Diffusion](projects/krita-ai-diffusion.md) | GPL-3.0 | Krita on Windows/Linux/macOS; managed local or remote Comfy; model-dependent GPU support | Krita plugin ZIP; local server installer or optional cloud connection | Strong visual-remix and managed Comfy reference; different primary interaction from recipe replay |
| [ComfyUI — inference engine and graph server](projects/comfyui.md) | GPL-3.0 | Windows/Linux/macOS Apple Silicon; CPU and multiple GPU backends; node/model support varies | Python server, Windows portable archives, separate Desktop/frontend/cloud products | Recommended initial execution engine; existing Dreamtime investment and broad workflow primitives |
| [ComfyUI official frontend / App Mode](projects/comfy-frontend.md) | GPL-3.0-only in package manifest | Browser frontend; runs with Comfy on supported host OSes; desktop/cloud builds differ | Versioned frontend packages/releases consumed by Comfy; no independent GPU runtime | Direct baseline for simplified workflow forms; App Mode removes the node-editor requirement |
| [stable-diffusion.cpp](projects/stable-diffusion-cpp.md) | MIT | Windows/Linux/macOS plus additional targets; CPU/CUDA/Vulkan/Metal/OpenCL/SYCL | Native CLI/library/server; rolling platform/backend-specific archives and web UI | Most relevant alternative native runtime; attractive packaging, different reproduction semantics |
| [Draw Things community core](projects/draw-things.md) | GPL-3.0 public core; full consumer app is not all in this repository | Apple-native consumer app; public macOS CLI/server and CUDA Linux server path; no Windows app established | Consumer Apple app separately; macOS CLI/gRPC binaries and Linux server/container path | Apple performance/product benchmark and possible remote runtime; not a ready cross-platform UI base |
| [Official Civitai CLI](projects/civitai-cli.md) | Apache-2.0 | Static binaries for Windows/Linux/macOS, x64 and ARM64 | Go binary; archives, npm/Homebrew/Nix/source install routes | Provider integration/download reference; also a cloud generation/App toolchain, not a local inference engine |
| [Desktop Release Kit — distribution baseline](projects/desktop-release-kit.md) | MIT | macOS Apple Silicon/Intel; Windows x64; Linux x64/ARM64 | Tauri canary with signed releases, native installers, updater artifacts, and acceptance evidence | Adopt release contracts and validation patterns; not a Python/GPU/model installer |
| [Comfy Desktop](projects/comfy-desktop.md) | Dual AGPL-3.0-or-later OR commercial license | Windows, macOS Apple Silicon, and documented Linux AppImage/.deb support | Electron desktop manager; external installer delivery; source release feed can lack binary attachments | Primary benchmark for managed Comfy installation, instances, snapshots, and recovery |
| [Wan2GP Desktop Tauri launcher](projects/wan2gp-desktop.md) | No tracked LICENSE file found; reuse permission unresolved | Windows release artifacts verified in snapshot; macOS/Linux delivery not established | Tauri 2 launcher; Windows NSIS/MSI and updater metadata; manages external WanGP runtime | Very close packaging concept, very young implementation, unresolved license |
| [Pinokio](projects/pinokio.md) | MIT application source; installed scripts/apps have separate terms | Windows/Linux/macOS; shipped x64/ARM64 coverage varies by artifact and installed app | Electron desktop launcher with installer/archive releases and a separate pinokiod backend dependency | Established onboarding alternative; not a recipe-reproduction application |
| [ViewComfy](projects/viewcomfy.md) | AGPL-3.0 | Node/browser app on Windows/Linux/macOS; Comfy can be local or remote | Next.js web app, source releases, separately offered hosted service | Prepared Comfy workflow → approachable form; not a foreign recipe resolver |
| [SDFX](projects/sdfx.md) | AGPL-3.0 | Web/Electron builds for Windows/Linux/macOS are described; current binary delivery unestablished | Source setup scripts; Vue/Vite web build and Electron build; no release feed captured | Useful declarative workflow/UI architecture; stale default branch makes it a poor primary dependency |
| [Visionatrix](projects/visionatrix.md) | AGPL-3.0-or-later | Windows portable CUDA/CPU; Linux/macOS source paths; Docker/remote workers | Python/Nuxt web app, CLI/service, Docker images, Windows portable archive; archived repository | Closest service/worker/preset architecture reference; archived, so not recommended as maintained foundation |
| [AUTOMATIC1111 Stable Diffusion WebUI](projects/automatic1111.md) | AGPL-3.0 | Windows/Linux; Apple Silicon instructions exist; hardware/extensions vary | Python/Gradio web app, launch scripts, Windows portable-style assets; extensions | Historical metadata/parameter-reuse baseline; major attention, limited recent default-branch activity |
| [Stable Diffusion WebUI Forge](projects/forge.md) | AGPL-3.0 at root; substantial inherited code | Windows/Linux primarily; inherited/general platform paths do not establish full Mac parity | Python/Gradio web app, Windows one-click archives, source/rolling releases | A1111-compatible interaction and memory optimization reference; inspected original fork is not all Forge descendants |
| [Fooocus](projects/fooocus.md) | GPL-3.0 | Windows/Linux; Mac MPS guidance is explicitly less tested; model/hardware scope constrained | Gradio app with Windows archive and automatic preset-model downloads; source scripts | Simplicity/preset UX benchmark; limited SDXL-focused LTS, not a modern general video foundation |
| [Easy Diffusion](projects/easy-diffusion.md) | Custom MIT-style license with use-based restrictions; not plain MIT | Windows/Linux/macOS; runtime/backend and hardware support vary | Windows installer, Linux/Mac archives, Python/FastAPI web app; evolving v4 engine paths | Established simple installation/image workflow reference; not proven full Civitai replay-to-video product |
