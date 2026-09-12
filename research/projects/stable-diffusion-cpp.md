# stable-diffusion.cpp

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/leejet/stable-diffusion.cpp) · [Local clone](../../../references/stable-diffusion-cpp/) · [Raw snapshot](../evidence/stable-diffusion-cpp.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2023-08-13 / 1,125 days (about 3.08 years) |
| Oldest reachable commit | 2023-08-13T15:38:16+08:00 — can include inherited history |
| Stars / forks / subscribers | 6,964 / 782 / 78 |
| Open issues + PRs | 271 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | master / `7f410a3793c5bba8eb198e962ce7a3d6095f9d89` |
| HEAD commit | 2026-09-12T01:41:28+08:00 feat: add linear and attention scale overrides (#1964) |
| Reachable commits, including merges | 859 |
| Historical distinct author names | 106 |
| Last 90 days: nonmerge commits / author names | 164 / 31 |
| Source license assessment | MIT |
| Operating systems / hardware scope | Windows/Linux/macOS plus additional targets; CPU/CUDA/Vulkan/Metal/OpenCL/SYCL |
| Distribution model | Native CLI/library/server; rolling platform/backend-specific archives and web UI |
| Fit for Remixfun | Most relevant alternative native runtime; attractive packaging, different reproduction semantics |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| leejet | 408 | leejet | 73 |
| Wagner Bruna | 94 | stduhpf | 19 |
| stduhpf | 93 | fszontagh | 17 |
| fszontagh | 25 | Wagner Bruna | 11 |
| vmobilis | 17 | vmobilis | 10 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [master-859-7f410a3](https://github.com/leejet/stable-diffusion.cpp/releases/tag/master-859-7f410a3) | 2026-09-11T20:38:49Z | `cudart-sd-bin-win-cu12-x64.zip`, `sd-master-7f410a3-bin-Darwin-macOS-26.6.2-arm64.zip`, `sd-master-7f410a3-bin-Linux-Ubuntu-24.04-x86_64-rocm-7.14.0.zip`, `sd-master-7f410a3-bin-Linux-Ubuntu-24.04-x86_64-vulkan.zip`, `sd-master-7f410a3-bin-Linux-Ubuntu-24.04-x86_64.zip`, `sd-master-7f410a3-bin-win-cpu-x64.zip`, `sd-master-7f410a3-bin-win-cuda12-x64.zip`; +2 more in snapshot |
| [master-858-5ebce93](https://github.com/leejet/stable-diffusion.cpp/releases/tag/master-858-5ebce93) | 2026-09-11T19:46:52Z | `cudart-sd-bin-win-cu12-x64.zip`, `sd-master-5ebce93-bin-Darwin-macOS-26.6.2-arm64.zip`, `sd-master-5ebce93-bin-Linux-Ubuntu-24.04-x86_64-rocm-7.14.0.zip`, `sd-master-5ebce93-bin-Linux-Ubuntu-24.04-x86_64-vulkan.zip`, `sd-master-5ebce93-bin-Linux-Ubuntu-24.04-x86_64.zip`, `sd-master-5ebce93-bin-win-cpu-x64.zip`, `sd-master-5ebce93-bin-win-cuda12-x64.zip`; +2 more in snapshot |
| [master-857-7f986a9](https://github.com/leejet/stable-diffusion.cpp/releases/tag/master-857-7f986a9) | 2026-09-11T19:34:29Z | `cudart-sd-bin-win-cu12-x64.zip`, `sd-master-7f986a9-bin-Darwin-macOS-26.6.2-arm64.zip`, `sd-master-7f986a9-bin-Linux-Ubuntu-24.04-x86_64-rocm-7.14.0.zip`, `sd-master-7f986a9-bin-Linux-Ubuntu-24.04-x86_64-vulkan.zip`, `sd-master-7f986a9-bin-Linux-Ubuntu-24.04-x86_64.zip`, `sd-master-7f986a9-bin-win-cpu-x64.zip`, `sd-master-7f986a9-bin-win-cuda12-x64.zip`; +2 more in snapshot |
| [master-856-e06b205](https://github.com/leejet/stable-diffusion.cpp/releases/tag/master-856-e06b205) | 2026-09-11T18:36:44Z | `cudart-sd-bin-win-cu12-x64.zip`, `sd-master-e06b205-bin-Darwin-macOS-26.6.2-arm64.zip`, `sd-master-e06b205-bin-Linux-Ubuntu-24.04-x86_64-rocm-7.14.0.zip`, `sd-master-e06b205-bin-Linux-Ubuntu-24.04-x86_64-vulkan.zip`, `sd-master-e06b205-bin-Linux-Ubuntu-24.04-x86_64.zip`, `sd-master-e06b205-bin-win-cpu-x64.zip`, `sd-master-e06b205-bin-win-cuda12-x64.zip`; +2 more in snapshot |
| [master-855-3191b23](https://github.com/leejet/stable-diffusion.cpp/releases/tag/master-855-3191b23) | 2026-09-11T18:07:06Z | `cudart-sd-bin-win-cu12-x64.zip`, `sd-master-3191b23-bin-Darwin-macOS-26.6.2-arm64.zip`, `sd-master-3191b23-bin-Linux-Ubuntu-24.04-x86_64-rocm-7.14.0.zip`, `sd-master-3191b23-bin-Linux-Ubuntu-24.04-x86_64-vulkan.zip`, `sd-master-3191b23-bin-Linux-Ubuntu-24.04-x86_64.zip`, `sd-master-3191b23-bin-win-cpu-x64.zip`, `sd-master-3191b23-bin-win-cuda12-x64.zip`; +2 more in snapshot |

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

## Source map and citations

[^s1]: **Model/backend/platform scope** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/blob/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/README.md); [local README.md](../../../references/stable-diffusion-cpp/README.md).

[^s2]: **Native build boundary** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/blob/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/CMakeLists.txt); [local CMakeLists.txt](../../../references/stable-diffusion-cpp/CMakeLists.txt).

[^s3]: **Core inference implementation** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/blob/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/src/stable-diffusion.cpp); [local src/stable-diffusion.cpp](../../../references/stable-diffusion-cpp/src/stable-diffusion.cpp).

[^s4]: **Command-line application and metadata handling** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/tree/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/examples/cli); [local examples/cli](../../../references/stable-diffusion-cpp/examples/cli).

[^s5]: **HTTP server and web UI** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/blob/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/examples/server/README.md); [local examples/server/README.md](../../../references/stable-diffusion-cpp/examples/server/README.md).

[^s6]: **Server runtime** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/blob/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/examples/server/runtime.cpp); [local examples/server/runtime.cpp](../../../references/stable-diffusion-cpp/examples/server/runtime.cpp).

[^s7]: **Asynchronous jobs** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/blob/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/examples/server/async_jobs.cpp); [local examples/server/async_jobs.cpp](../../../references/stable-diffusion-cpp/examples/server/async_jobs.cpp).

[^s8]: **Wan model-specific usage** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/blob/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/docs/wan.md); [local docs/wan.md](../../../references/stable-diffusion-cpp/docs/wan.md).

[^s9]: **MIT source license** — [Pinned source](https://github.com/leejet/stable-diffusion.cpp/blob/7f410a3793c5bba8eb198e962ce7a3d6095f9d89/LICENSE); [local LICENSE](../../../references/stable-diffusion-cpp/LICENSE).
