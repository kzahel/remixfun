# Stable Diffusion WebUI Forge

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/lllyasviel/stable-diffusion-webui-forge) · [Local clone](../../../references/forge/) · [Raw snapshot](../evidence/forge.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2024-01-14 / 971 days (about 2.66 years) |
| Oldest reachable commit | 2022-08-22T17:05:27+03:00 — can include inherited history |
| Stars / forks / subscribers | 13,003 / 1,727 / 126 |
| Open issues + PRs | 1,159 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `dfdcbab685e57677014f05a3309b48cc87383167` |
| HEAD commit | 2025-06-26T18:53:55+01:00 Fix SD upscale Batch count (#2950) |
| Reachable commits, including merges | 8,627 |
| Historical distinct author names | 639 |
| Last 90 days: nonmerge commits / author names | 0 / 0 |
| Source license assessment | AGPL-3.0 at root; substantial inherited code |
| Operating systems / hardware scope | Windows/Linux primarily; inherited/general platform paths do not establish full Mac parity |
| Distribution model | Python/Gradio web app, Windows one-click archives, source/rolling releases |
| Fit for Remixfun | A1111-compatible interaction and memory optimization reference; inspected original fork is not all Forge descendants |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| AUTOMATIC | 1228 | — | — |
| lllyasviel | 891 | — | — |
| AUTOMATIC1111 | 524 | — | — |
| layerdiffusion | 427 | — | — |
| w-e-w | 229 | — | — |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [previous_versions](https://github.com/lllyasviel/stable-diffusion-webui-forge/releases/tag/previous) | 2024-07-22T06:24:48Z | `webui_forge_cu121_torch21_f0017.7z` |
| [v1.7.0d](https://github.com/lllyasviel/stable-diffusion-webui-forge/releases/tag/v1.7.0d) | 2024-02-05T02:41:20Z | No attached artifacts in captured expansion; check external distribution |
| [latest](https://github.com/lllyasviel/stable-diffusion-webui-forge/releases/tag/latest) | 2024-08-11T21:54:41Z | `webui_forge_cu121_torch21.7z`, `webui_forge_cu121_torch231.7z`, `webui_forge_cu124_torch24.7z` |

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

## Source map and citations

[^s1]: **Lineage, install routes, and stated compatibility** — [Pinned source](https://github.com/lllyasviel/stable-diffusion-webui-forge/blob/dfdcbab685e57677014f05a3309b48cc87383167/README.md); [local README.md](../../../references/forge/README.md).

[^s2]: **Memory/offload policy** — [Pinned source](https://github.com/lllyasviel/stable-diffusion-webui-forge/blob/dfdcbab685e57677014f05a3309b48cc87383167/backend/memory_management.py); [local backend/memory_management.py](../../../references/forge/backend/memory_management.py).

[^s3]: **Model loading** — [Pinned source](https://github.com/lllyasviel/stable-diffusion-webui-forge/blob/dfdcbab685e57677014f05a3309b48cc87383167/backend/loader.py); [local backend/loader.py](../../../references/forge/backend/loader.py).

[^s4]: **Model-family execution** — [Pinned source](https://github.com/lllyasviel/stable-diffusion-webui-forge/tree/dfdcbab685e57677014f05a3309b48cc87383167/backend/diffusion_engine); [local backend/diffusion_engine](../../../references/forge/backend/diffusion_engine).

[^s5]: **Inherited parameter import** — [Pinned source](https://github.com/lllyasviel/stable-diffusion-webui-forge/blob/dfdcbab685e57677014f05a3309b48cc87383167/modules/infotext_utils.py); [local modules/infotext_utils.py](../../../references/forge/modules/infotext_utils.py).

[^s6]: **AGPL license** — [Pinned source](https://github.com/lllyasviel/stable-diffusion-webui-forge/blob/dfdcbab685e57677014f05a3309b48cc87383167/LICENSE.txt); [local LICENSE.txt](../../../references/forge/LICENSE.txt).
