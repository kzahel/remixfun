# Official Civitai CLI

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/civitai/cli) · [Local clone](../../../references/civitai-cli/) · [Raw snapshot](../evidence/civitai-cli.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2026-06-18 / 85 days (about 0.23 years) |
| Oldest reachable commit | 2026-06-18T09:21:54-05:00 — can include inherited history |
| Stars / forks / subscribers | 10 / 1 / 0 |
| Open issues + PRs | 22 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `f98eb736adc33aa4974b9b56d355e1bf94d9166c` |
| HEAD commit | 2026-09-12T01:00:16-05:00 docs(handoff): rank 21 done (cli#569 merged, re-verified); rank 20 claimed (#571) |
| Reachable commits, including merges | 439 |
| Historical distinct author names | 3 |
| Last 90 days: nonmerge commits / author names | 437 / 3 |
| Source license assessment | Apache-2.0 |
| Operating systems / hardware scope | Static binaries for Windows/Linux/macOS, x64 and ARM64 |
| Distribution model | Go binary; archives, npm/Homebrew/Nix/source install routes |
| Fit for Remixfun | Provider integration/download reference; also a cloud generation/App toolchain, not a local inference engine |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Zachary Lowden | 431 | Zachary Lowden | 431 |
| ZacxDev | 4 | ZacxDev | 4 |
| xsvm | 2 | xsvm | 2 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v0.1.104](https://github.com/civitai/cli/releases/tag/v0.1.104) | 2026-09-09T02:56:05Z | `checksums.txt`, `civitai.rb`, `civitai_0.1.104_darwin_amd64`, `civitai_0.1.104_darwin_amd64.tar.gz`, `civitai_0.1.104_darwin_arm64`, `civitai_0.1.104_darwin_arm64.tar.gz`, `civitai_0.1.104_linux_amd64`; +7 more in snapshot |
| [v0.1.103](https://github.com/civitai/cli/releases/tag/v0.1.103) | 2026-09-09T00:56:40Z | `checksums.txt`, `civitai.rb`, `civitai_0.1.103_darwin_amd64`, `civitai_0.1.103_darwin_amd64.tar.gz`, `civitai_0.1.103_darwin_arm64`, `civitai_0.1.103_darwin_arm64.tar.gz`, `civitai_0.1.103_linux_amd64`; +7 more in snapshot |
| [v0.1.102](https://github.com/civitai/cli/releases/tag/v0.1.102) | 2026-08-27T18:03:55Z | `checksums.txt`, `civitai.rb`, `civitai_0.1.102_darwin_amd64`, `civitai_0.1.102_darwin_amd64.tar.gz`, `civitai_0.1.102_darwin_arm64`, `civitai_0.1.102_darwin_arm64.tar.gz`, `civitai_0.1.102_linux_amd64`; +7 more in snapshot |
| [v0.1.101](https://github.com/civitai/cli/releases/tag/v0.1.101) | 2026-08-26T03:56:29Z | `checksums.txt`, `civitai.rb`, `civitai_0.1.101_darwin_amd64`, `civitai_0.1.101_darwin_amd64.tar.gz`, `civitai_0.1.101_darwin_arm64`, `civitai_0.1.101_darwin_arm64.tar.gz`, `civitai_0.1.101_linux_amd64`; +7 more in snapshot |
| [v0.1.100](https://github.com/civitai/cli/releases/tag/v0.1.100) | 2026-08-25T19:08:17Z | `checksums.txt`, `civitai.rb`, `civitai_0.1.100_darwin_amd64`, `civitai_0.1.100_darwin_amd64.tar.gz`, `civitai_0.1.100_darwin_arm64`, `civitai_0.1.100_darwin_arm64.tar.gz`, `civitai_0.1.100_linux_amd64`; +7 more in snapshot |

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

## Source map and citations

[^s1]: **CLI capabilities, auth boundaries, and distribution** — [Pinned source](https://github.com/civitai/cli/blob/f98eb736adc33aa4974b9b56d355e1bf94d9166c/README.md); [local README.md](../../../references/civitai-cli/README.md).

[^s2]: **Go module/dependencies** — [Pinned source](https://github.com/civitai/cli/blob/f98eb736adc33aa4974b9b56d355e1bf94d9166c/go.mod); [local go.mod](../../../references/civitai-cli/go.mod).

[^s3]: **Image API client** — [Pinned source](https://github.com/civitai/cli/blob/f98eb736adc33aa4974b9b56d355e1bf94d9166c/pkg/civitai/images.go); [local pkg/civitai/images.go](../../../references/civitai-cli/pkg/civitai/images.go).

[^s4]: **Version identity API** — [Pinned source](https://github.com/civitai/cli/blob/f98eb736adc33aa4974b9b56d355e1bf94d9166c/pkg/civitai/model_versions.go); [local pkg/civitai/model_versions.go](../../../references/civitai-cli/pkg/civitai/model_versions.go).

[^s5]: **Hash lookups** — [Pinned source](https://github.com/civitai/cli/blob/f98eb736adc33aa4974b9b56d355e1bf94d9166c/pkg/civitai/hashes.go); [local pkg/civitai/hashes.go](../../../references/civitai-cli/pkg/civitai/hashes.go).

[^s6]: **Download client and integrity behavior** — [Pinned source](https://github.com/civitai/cli/blob/f98eb736adc33aa4974b9b56d355e1bf94d9166c/pkg/civitai/download.go); [local pkg/civitai/download.go](../../../references/civitai-cli/pkg/civitai/download.go).

[^s7]: **Retry semantics** — [Pinned source](https://github.com/civitai/cli/blob/f98eb736adc33aa4974b9b56d355e1bf94d9166c/pkg/civitai/retry.go); [local pkg/civitai/retry.go](../../../references/civitai-cli/pkg/civitai/retry.go).

[^s8]: **Apache source license** — [Pinned source](https://github.com/civitai/cli/blob/f98eb736adc33aa4974b9b56d355e1bf94d9166c/LICENSE); [local LICENSE](../../../references/civitai-cli/LICENSE).
