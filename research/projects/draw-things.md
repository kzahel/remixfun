# Draw Things community core

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/drawthingsai/draw-things-community) · [Local clone](../../../references/draw-things/) · [Raw snapshot](../evidence/draw-things.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2023-11-19 / 1,027 days (about 2.81 years) |
| Oldest reachable commit | 2024-03-19T14:20:58-04:00 — can include inherited history |
| Stars / forks / subscribers | 556 / 67 / 12 |
| Open issues + PRs | 98 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `08e798b5ad59c3db78b2be53f0ed60b071653302` |
| HEAD commit | 2026-09-11T16:36:52-04:00 Add missing files. |
| Reachable commits, including merges | 2,039 |
| Historical distinct author names | 9 |
| Last 90 days: nonmerge commits / author names | 173 / 6 |
| Source license assessment | GPL-3.0 public core; full consumer app is not all in this repository |
| Operating systems / hardware scope | Apple-native consumer app; public macOS CLI/server and CUDA Linux server path; no Windows app established |
| Distribution model | Consumer Apple app separately; macOS CLI/gRPC binaries and Linux server/container path |
| Fit for Remixfun | Apple performance/product benchmark and possible remote runtime; not a ready cross-platform UI base |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Liu Liu | 1742 | Liu Liu | 141 |
| weiyanlin117 | 117 | weiyanlin117 | 12 |
| Weiyan Lin | 86 | weiyan | 9 |
| Weiyan | 40 | gongster | 7 |
| gongster | 37 | Weiyan Lin | 2 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v26.0910.1](https://github.com/drawthingsai/draw-things-community/releases/tag/v26.0910.1) | 2026-09-11T21:18:19Z | `draw-things-cli`, `gRPCServerCLI-macOS` |
| [v1.20260716.0](https://github.com/drawthingsai/draw-things-community/releases/tag/v1.20260716.0) | 2026-07-20T02:47:06Z | `draw-things-cli`, `gRPCServerCLI-macOS` |
| [v1.20260430.0](https://github.com/drawthingsai/draw-things-community/releases/tag/v1.20260430.0) | 2026-05-01T18:12:44Z | `draw-things-cli`, `gRPCServerCLI-macOS` |
| [v1.20260418.1](https://github.com/drawthingsai/draw-things-community/releases/tag/v1.20260418.1) | 2026-04-20T17:35:13Z | `draw-things-cli`, `gRPCServerCLI-macOS` |
| [v1.20260410.1](https://github.com/drawthingsai/draw-things-community/releases/tag/v1.20260410.1) | 2026-04-11T18:41:23Z | `draw-things-cli`, `gRPCServerCLI-macOS` |

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

## Source map and citations

[^s1]: **Public/private boundary, CLI, and server distribution** — [Pinned source](https://github.com/drawthingsai/draw-things-community/blob/08e798b5ad59c3db78b2be53f0ed60b071653302/README.md); [local README.md](../../../references/draw-things/README.md).

[^s2]: **Swift packages and products** — [Pinned source](https://github.com/drawthingsai/draw-things-community/blob/08e798b5ad59c3db78b2be53f0ed60b071653302/Package.swift); [local Package.swift](../../../references/draw-things/Package.swift).

[^s3]: **Public model, sampler, and supporting libraries** — [Pinned source](https://github.com/drawthingsai/draw-things-community/tree/08e798b5ad59c3db78b2be53f0ed60b071653302/Libraries); [local Libraries](../../../references/draw-things/Libraries).

[^s4]: **Public command-line/server targets** — [Pinned source](https://github.com/drawthingsai/draw-things-community/tree/08e798b5ad59c3db78b2be53f0ed60b071653302/Apps); [local Apps](../../../references/draw-things/Apps).

[^s5]: **Public source license** — [Pinned source](https://github.com/drawthingsai/draw-things-community/blob/08e798b5ad59c3db78b2be53f0ed60b071653302/LICENSE.md); [local LICENSE.md](../../../references/draw-things/LICENSE.md).

[^s6]: **Contribution agreement** — [Pinned source](https://github.com/drawthingsai/draw-things-community/tree/08e798b5ad59c3db78b2be53f0ed60b071653302/CLA); [local CLA](../../../references/draw-things/CLA).
