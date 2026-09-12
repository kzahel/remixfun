# ComfyUI — inference engine and graph server

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/Comfy-Org/ComfyUI) · [Local clone](../../../references/comfyui/) · [Raw snapshot](../evidence/comfyui.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2023-01-17 / 1,334 days (about 3.65 years) |
| Oldest reachable commit | 2023-01-03T01:53:32-05:00 — can include inherited history |
| Stars / forks / subscribers | 132,635 / 15,654 / 808 |
| Open issues + PRs | 4,866 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | master / `7193f5627f036701e5efc23beaea20fa37ceaadd` |
| HEAD commit | 2026-09-11T19:32:18-07:00 Bump comfyui-frontend-package to 1.52.7 (#16275) |
| Reachable commits, including merges | 5,930 |
| Historical distinct author names | 368 |
| Last 90 days: nonmerge commits / author names | 491 / 56 |
| Source license assessment | GPL-3.0 |
| Operating systems / hardware scope | Windows/Linux/macOS Apple Silicon; CPU and multiple GPU backends; node/model support varies |
| Distribution model | Python server, Windows portable archives, separate Desktop/frontend/cloud products |
| Fit for Remixfun | Recommended initial execution engine; existing Dreamtime investment and broad workflow primitives |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| comfyanonymous | 3127 | comfyanonymous | 140 |
| Alexander Piskun | 401 | Alexander Piskun | 99 |
| pythongosssss | 213 | Daxiong (Lin) | 46 |
| rattus | 154 | Jukka Seppänen | 34 |
| Chenlei Hu | 118 | rattus | 27 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v0.35.1](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.35.1) | 2026-09-10T21:14:03Z | No attached artifacts in captured expansion; check external distribution |
| [v0.35.0](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.35.0) | 2026-09-09T19:55:08Z | `ComfyUI_windows_portable_amd.7z`, `ComfyUI_windows_portable_intel.7z`, `ComfyUI_windows_portable_nvidia.7z`, `ComfyUI_windows_portable_nvidia_cu126.7z` |
| [v0.34.6](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.34.6) | 2026-09-07T19:24:58Z | No attached artifacts in captured expansion; check external distribution |
| [v0.34.5](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.34.5) | 2026-09-05T02:40:10Z | No attached artifacts in captured expansion; check external distribution |
| [v0.34.4](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.34.4) | 2026-09-04T21:07:26Z | No attached artifacts in captured expansion; check external distribution |

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

## Source map and citations

[^s1]: **Current engine/platform/install scope** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/README.md); [local README.md](../../../references/comfyui/README.md).

[^s2]: **Server startup** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/main.py); [local main.py](../../../references/comfyui/main.py).

[^s3]: **HTTP/WebSocket API** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/server.py); [local server.py](../../../references/comfyui/server.py).

[^s4]: **Graph validation/execution/cache** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/execution.py); [local execution.py](../../../references/comfyui/execution.py).

[^s5]: **Device/memory management** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/comfy/model_management.py); [local comfy/model_management.py](../../../references/comfyui/comfy/model_management.py).

[^s6]: **Model/file categories** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/folder_paths.py); [local folder_paths.py](../../../references/comfyui/folder_paths.py).

[^s7]: **Shared model path configuration** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/extra_model_paths.yaml.example); [local extra_model_paths.yaml.example](../../../references/comfyui/extra_model_paths.yaml.example).

[^s8]: **Runtime and frontend package dependencies** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/requirements.txt); [local requirements.txt](../../../references/comfyui/requirements.txt).

[^s9]: **GPL source license** — [Pinned source](https://github.com/Comfy-Org/ComfyUI/blob/7193f5627f036701e5efc23beaea20fa37ceaadd/LICENSE); [local LICENSE](../../../references/comfyui/LICENSE).

[^s10]: [Official current OS and hardware guidance](https://docs.comfy.org/installation/system_requirements), accessed 2026-09-12.
