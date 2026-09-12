# Stability Matrix

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/LykosAI/StabilityMatrix) · [Local clone](../../../references/stability-matrix/) · [Raw snapshot](../evidence/stability-matrix.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2023-06-13 / 1,187 days (about 3.25 years) |
| Oldest reachable commit | 2023-05-23T19:00:11-04:00 — can include inherited history |
| Stars / forks / subscribers | 8,763 / 598 / 96 |
| Open issues + PRs | 164 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002` |
| HEAD commit | 2026-09-10T19:40:50-07:00 Merge pull request #1737 from NeuralFault/patch-2 |
| Reachable commits, including merges | 7,410 |
| Historical distinct author names | 35 |
| Last 90 days: nonmerge commits / author names | 153 / 8 |
| Source license assessment | AGPL-3.0 source; official binaries have a separately linked EULA |
| Operating systems / hardware scope | Windows x64, Linux x64, macOS Apple Silicon; packages and GPU support vary |
| Distribution model | Native Avalonia desktop; Windows/Linux archives and macOS DMG; managed AI packages |
| Fit for Remixfun | Strongest combined installer, shared-model library, and native Comfy inference competitor |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Ionite | 3013 | jt | 58 |
| JT | 1172 | NeuralFault | 56 |
| jt | 467 | JT | 32 |
| NeuralFault | 204 | ungrav | 3 |
| ionite34 | 134 | 0xDELUXA | 1 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v2.16.3](https://github.com/LykosAI/StabilityMatrix/releases/tag/v2.16.3) | 2026-08-29T03:47:54Z | `StabilityMatrix-linux-x64.zip`, `StabilityMatrix-macos-arm64.dmg`, `StabilityMatrix-win-x64.zip` |
| [v2.16.2](https://github.com/LykosAI/StabilityMatrix/releases/tag/v2.16.2) | 2026-08-02T22:46:54Z | `StabilityMatrix-linux-x64.zip`, `StabilityMatrix-macos-arm64.dmg`, `StabilityMatrix-win-x64.zip` |
| [v2.16.1](https://github.com/LykosAI/StabilityMatrix/releases/tag/v2.16.1) | 2026-06-16T02:20:49Z | `StabilityMatrix-linux-x64.zip`, `StabilityMatrix-macos-arm64.dmg`, `StabilityMatrix-win-x64.zip` |
| [v2.16.0](https://github.com/LykosAI/StabilityMatrix/releases/tag/v2.16.0) | 2026-06-09T02:15:23Z | `StabilityMatrix-linux-x64.zip`, `StabilityMatrix-macos-arm64.dmg`, `StabilityMatrix-win-x64.zip` |
| [v2.15.8](https://github.com/LykosAI/StabilityMatrix/releases/tag/v2.15.8) | 2026-05-17T01:09:11Z | `StabilityMatrix-linux-x64.zip`, `StabilityMatrix-macos-arm64.dmg`, `StabilityMatrix-win-x64.zip` |

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

## Source map and citations

[^s1]: **Package manager, platforms, distribution, and binary license distinction** — [Pinned source](https://github.com/LykosAI/StabilityMatrix/blob/af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002/README.md); [local README.md](../../../references/stability-matrix/README.md).

[^s2]: **Shared services, packages, models, and downloads** — [Pinned source](https://github.com/LykosAI/StabilityMatrix/tree/af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002/StabilityMatrix.Core); [local StabilityMatrix.Core](../../../references/stability-matrix/StabilityMatrix.Core).

[^s3]: **Image metadata ingestion** — [Pinned source](https://github.com/LykosAI/StabilityMatrix/blob/af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002/StabilityMatrix.Avalonia/ViewModels/Base/InferenceTabViewModelBase.cs); [local StabilityMatrix.Avalonia/ViewModels/Base/InferenceTabViewModelBase.cs](../../../references/stability-matrix/StabilityMatrix.Avalonia/ViewModels/Base/InferenceTabViewModelBase.cs).

[^s4]: **Generic/Civitai parameter representation** — [Pinned source](https://github.com/LykosAI/StabilityMatrix/blob/af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002/StabilityMatrix.Core/Models/GenerationParameters.cs); [local StabilityMatrix.Core/Models/GenerationParameters.cs](../../../references/stability-matrix/StabilityMatrix.Core/Models/GenerationParameters.cs).

[^s5]: **Installed model matching and state restoration** — [Pinned source](https://github.com/LykosAI/StabilityMatrix/blob/af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002/StabilityMatrix.Avalonia/ViewModels/Inference/ModelCardViewModel.cs); [local StabilityMatrix.Avalonia/ViewModels/Inference/ModelCardViewModel.cs](../../../references/stability-matrix/StabilityMatrix.Avalonia/ViewModels/Inference/ModelCardViewModel.cs).

[^s6]: **Native inference, supported modes, and project state** — [Pinned source](https://github.com/LykosAI/StabilityMatrix/blob/af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002/docs/inference/overview.md); [local docs/inference/overview.md](../../../references/stability-matrix/docs/inference/overview.md).

[^s7]: **Comfy graph and API boundary** — [Pinned source](https://github.com/LykosAI/StabilityMatrix/blob/af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002/docs/advanced/comfyui-integration.md); [local docs/advanced/comfyui-integration.md](../../../references/stability-matrix/docs/advanced/comfyui-integration.md).

[^s8]: **AGPL source license** — [Pinned source](https://github.com/LykosAI/StabilityMatrix/blob/af93d6ef57c01cd890d7e0ad0a9ea8c9fcda3002/LICENSE); [local LICENSE](../../../references/stability-matrix/LICENSE).
