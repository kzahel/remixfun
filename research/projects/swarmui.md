# SwarmUI

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/mcmonkeyprojects/SwarmUI) · [Local clone](../../../references/swarmui/) · [Raw snapshot](../evidence/swarmui.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2024-06-21 / 813 days (about 2.23 years) |
| Oldest reachable commit | 2023-05-05T13:13:15-07:00 — can include inherited history |
| Stars / forks / subscribers | 4,549 / 460 / 40 |
| Open issues + PRs | 147 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | master / `194b879e4c2a239b42ed1841aad3d6967cae7797` |
| HEAD commit | 2026-09-10T22:49:55-07:00 patch var seed with video-audio |
| Reachable commits, including merges | 4,968 |
| Historical distinct author names | 77 |
| Last 90 days: nonmerge commits / author names | 277 / 6 |
| Source license assessment | MIT |
| Operating systems / hardware scope | Windows/Linux/macOS application server; actual model/GPU support comes from configured backends |
| Distribution model | Install/run scripts and web UI; beta source releases; external Comfy processes |
| Fit for Remixfun | Strongest established Comfy-based general-purpose app benchmark |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Alex "mcmonkey" Goodwin | 4724 | Alex "mcmonkey" Goodwin | 250 |
| Juan Treminio | 72 | Juan Treminio | 23 |
| maedtb | 14 | BetaDoggo | 1 |
| Blomblo | 12 | Glen Carpenter | 1 |
| Brandon Wallace | 9 | kalebbroo | 1 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [0.9.8-Beta](https://github.com/mcmonkeyprojects/SwarmUI/releases/tag/0.9.8-Beta) | 2026-03-10T21:18:02Z | `install-windows.bat` |
| [0.9.7-Beta](https://github.com/mcmonkeyprojects/SwarmUI/releases/tag/0.9.7-Beta) | 2025-08-25T14:42:03Z | No attached artifacts in captured expansion; check external distribution |
| [0.9.6-Beta](https://github.com/mcmonkeyprojects/SwarmUI/releases/tag/0.9.6-Beta) | 2025-04-15T14:31:55Z | No attached artifacts in captured expansion; check external distribution |
| [0.9.5-Beta](https://github.com/mcmonkeyprojects/SwarmUI/releases/tag/0.9.5-Beta) | 2025-03-02T15:58:12Z | `install-windows.bat` |
| [0.9.4-Beta](https://github.com/mcmonkeyprojects/SwarmUI/releases/tag/0.9.4.0-Beta) | 2024-12-06T14:00:47Z | No attached artifacts in captured expansion; check external distribution |

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

## Source map and citations

[^s1]: **Product, installation, and independent continuation** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/README.md); [local README.md](../../../references/swarmui/README.md).

[^s2]: **.NET application boundary** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/src/SwarmUI.csproj); [local src/SwarmUI.csproj](../../../references/swarmui/src/SwarmUI.csproj).

[^s3]: **Backend orchestration** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/tree/194b879e4c2a239b42ed1841aad3d6967cae7797/src/Backends); [local src/Backends](../../../references/swarmui/src/Backends).

[^s4]: **Graph generation** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/src/BuiltinExtensions/ComfyUIBackend/WorkflowGenerator.cs); [local src/BuiltinExtensions/ComfyUIBackend/WorkflowGenerator.cs](../../../references/swarmui/src/BuiltinExtensions/ComfyUIBackend/WorkflowGenerator.cs).

[^s5]: **Generation stages** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/src/BuiltinExtensions/ComfyUIBackend/WorkflowGeneratorSteps.cs); [local src/BuiltinExtensions/ComfyUIBackend/WorkflowGeneratorSteps.cs](../../../references/swarmui/src/BuiltinExtensions/ComfyUIBackend/WorkflowGeneratorSteps.cs).

[^s6]: **Foreign metadata normalization** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/src/wwwroot/js/genpage/helpers/metadatahelpers.js); [local src/wwwroot/js/genpage/helpers/metadatahelpers.js](../../../references/swarmui/src/wwwroot/js/genpage/helpers/metadatahelpers.js).

[^s7]: **Image interaction and parameter reuse** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/src/wwwroot/js/genpage/gentab/currentimagehandler.js); [local src/wwwroot/js/genpage/gentab/currentimagehandler.js](../../../references/swarmui/src/wwwroot/js/genpage/gentab/currentimagehandler.js).

[^s8]: **Persisted image metadata and optional model hashes** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/docs/Image%20Metadata%20Format.md); [local docs/Image Metadata Format.md](../../../references/swarmui/docs/Image%20Metadata%20Format.md).

[^s9]: **Utility/model download interface** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/src/wwwroot/js/genpage/utiltab.js); [local src/wwwroot/js/genpage/utiltab.js](../../../references/swarmui/src/wwwroot/js/genpage/utiltab.js).

[^s10]: **MIT source license** — [Pinned source](https://github.com/mcmonkeyprojects/SwarmUI/blob/194b879e4c2a239b42ed1841aad3d6967cae7797/LICENSE.txt); [local LICENSE.txt](../../../references/swarmui/LICENSE.txt).
