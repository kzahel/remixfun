# Wan2GP / WanGP

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/deepbeepmeep/Wan2GP) · [Local clone](../../../references/wan2gp/) · [Raw snapshot](../evidence/wan2gp.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2025-02-27 / 561 days (about 1.54 years) |
| Oldest reachable commit | 2025-02-25T22:07:47+08:00 — can include inherited history |
| Stars / forks / subscribers | 9,293 / 1,468 / 102 |
| Open issues + PRs | 1,181 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `362c3467a70e1136ceb52eec95907205a8f88543` |
| HEAD commit | 2026-09-07T07:40:01+02:00 fixed viggle max duration |
| Reachable commits, including merges | 1,738 |
| Historical distinct author names | 36 |
| Last 90 days: nonmerge commits / author names | 174 / 4 |
| Source license assessment | Custom WanGP Community License 2.0; restricted commercial embedding/hosting |
| Operating systems / hardware scope | Windows/Linux primary; early Apple Silicon MPS support exists with documented limitations |
| Distribution model | Python/Gradio application, setup scripts, headless CLI/API; companion Tauri launcher |
| Fit for Remixfun | Strong video workflow benchmark; commercially restricted implementation is not a default embedding choice |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| DeepBeepMeep | 837 | deepbeepmeep | 96 |
| deepbeepmeep | 331 | DeepBeepMeep | 74 |
| Chris Malone | 267 | Chris Malone | 3 |
| DELUXA | 28 | GOvEy1nw | 1 |
| Gunther Schulz | 12 | — | — |

### Release evidence

No GitHub release entries were captured. This does not exclude registry packages, git installation, external installers, or a private release process.

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

## Source map and citations

[^s1]: **Current features and install routes** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/blob/362c3467a70e1136ceb52eec95907205a8f88543/README.md); [local README.md](../../../references/wan2gp/README.md).

[^s2]: **Application orchestration and model/runtime dispatch** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/blob/362c3467a70e1136ceb52eec95907205a8f88543/wgp.py); [local wgp.py](../../../references/wan2gp/wgp.py).

[^s3]: **Model-family implementations and settings** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/tree/362c3467a70e1136ceb52eec95907205a8f88543/models); [local models](../../../references/wan2gp/models).

[^s4]: **Programmatic generation interface** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/blob/362c3467a70e1136ceb52eec95907205a8f88543/shared/api.py); [local shared/api.py](../../../references/wan2gp/shared/api.py).

[^s5]: **Headless saved queues, dry runs, and automation** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/blob/362c3467a70e1136ceb52eec95907205a8f88543/docs/CLI.md); [local docs/CLI.md](../../../references/wan2gp/docs/CLI.md).

[^s6]: **Model download utility** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/blob/362c3467a70e1136ceb52eec95907205a8f88543/shared/utils/download.py); [local shared/utils/download.py](../../../references/wan2gp/shared/utils/download.py).

[^s7]: **Early Apple Silicon compatibility layer** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/blob/362c3467a70e1136ceb52eec95907205a8f88543/shared/mps/device_patch.py); [local shared/mps/device_patch.py](../../../references/wan2gp/shared/mps/device_patch.py).

[^s8]: **Version history and MPS limitations** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/blob/362c3467a70e1136ceb52eec95907205a8f88543/docs/CHANGELOG.md); [local docs/CHANGELOG.md](../../../references/wan2gp/docs/CHANGELOG.md).

[^s9]: **Binding custom license terms** — [Pinned source](https://github.com/deepbeepmeep/Wan2GP/blob/362c3467a70e1136ceb52eec95907205a8f88543/LICENSE.txt); [local LICENSE.txt](../../../references/wan2gp/LICENSE.txt).
