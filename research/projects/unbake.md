# ComfyUI-Unbake

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/syugoji/ComfyUI-Unbake) · [Local clone](../../../references/unbake/) · [Raw snapshot](../evidence/unbake.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2026-08-25 / 17 days (about 0.05 years) |
| Oldest reachable commit | 2026-08-25T16:56:17+09:00 — can include inherited history |
| Stars / forks / subscribers | 0 / 0 / 0 |
| Open issues + PRs | 0 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `0776f99532d2edbb3e1f1400f614816932ee8bf7` |
| HEAD commit | 2026-09-09T04:52:00+09:00 Use the LoRA strength the image was actually made with, and say when it cannot be checked |
| Reachable commits, including merges | 39 |
| Historical distinct author names | 2 |
| Last 90 days: nonmerge commits / author names | 39 / 2 |
| Source license assessment | GPL-3.0 family; README adds “Not for sale” language requiring clarification |
| Operating systems / hardware scope | Browser extension + Python Comfy routes; host-dependent Windows/Linux/macOS |
| Distribution model | Custom-node source installation; no GitHub releases captured |
| Fit for Remixfun | Closest conceptual competitor for provenance-aware replay and controlled comparisons |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| syugoji | 35 | syugoji | 35 |
| しゅごーじ | 4 | しゅごーじ | 4 |

### Release evidence

No GitHub release entries were captured. This does not exclude registry packages, git installation, external installers, or a private release process.

## Assessment

Unbake is the strongest challenge to the **conceptual** novelty of Remixfun. It explicitly joins imported image metadata, a replay feasibility assessment, graph construction, parameter sweeps, and side-by-side outputs. This is much closer than a generic prompt editor or model browser. Its weakness as a proven alternative is maturity: the repository is under three weeks old in this snapshot, with no stars and no release feed, and reported author names may be aliases of the same person.[^s1]

## Architecture and data model

The frontend core separates three objects: a generation record describing available evidence; a replay manifest describing a proposed executable reconstruction and its missing requirements; and a sweep describing controlled variations. Python integrates with the host server, while JavaScript host adapters submit and observe Comfy jobs. Panels render the import detail, missing-model decisions, and comparison UI.[^s2][^s4][^s5][^s6][^s8]

That separation is more suitable for Remixfun than restoring a handful of route parameters. The source image can remain immutable while resolution status changes as models are installed. Likewise, a replay plan can be replaced without rewriting the historical evidence about the imported source.

## Import and replay

Documented inputs include Civitai images, local metadata-bearing PNGs, existing Comfy outputs, and LoRA Manager recipes. The resolver checks the actual host's `/object_info`, node aliases, and installed resources. Missing requirements have distinct acquisition paths: known downloads, manual actions, or no identified source. Verdicts communicate different levels of feasibility rather than treating any valid graph as exact reproduction.[^s1][^s2][^s4]

This remains a planner and execution tool, not an oracle for the original hidden pipeline. The project's own examples show a runnable substitution producing a different image. For Remixfun, “graph valid,” “exact dependencies present,” “repeatable in this runtime,” and “visually matches source” should be separate observations. An appealing probability badge cannot replace that evidence.

## Controlled remix and persistence

The implemented sweep design has several ideas worth adopting: explicitly selected axes; one baseline; validation before queue submission; graph fingerprints; per-cell persistence; and distinct states for uncertain jobs. `assertOnlySweepInputsChanged` guards against changes outside declared axes. The UI covers checkpoints, generation parameters, LoRA strength, and prompt edits, with a 500-cell cap described in the source documentation.[^s1][^s2][^s3]

Graph fingerprints are useful execution identities but not complete cross-machine identities if they omit resolved file contents and runtime versions. Remixfun should combine graph identity with its model ledger and engine environment. Likewise, a source PNG's metadata may vary between writes even if decoded pixels match.

Captured arbitrary Comfy graphs and recipe-derived records do not have identical sweep support. The README says only recipe-derived records can be swept through this mechanism. It also distinguishes trial/batch core functionality from what is exposed on screen. Those limits prevent crediting every internal module as a finished user feature.[^s1]

## What it does not replace

Model browsing and a general collection manager are explicitly outside the project's scope. No coherent first/last-frame, extension, and loop video product was established. The user still needs Comfy and a compatible environment. Thus it may satisfy the central reproduce-and-compare task for selected recipes while leaving installation, collection management, and motion handoff to other tools.[^s1][^s4]

## License, contributors, and maintenance

The root license is GPL-3.0 text; the README labels GPL-3.0-or-later but also says “Not for sale.” That phrase is in tension with ordinary GPL distribution permissions. Record the ambiguity instead of categorizing this as a clean no-sale license or assuming a permissive grant. A reuse decision should resolve the author's intended terms and any embedded components first.[^s1][^s7]

The short history is dominated by `syugoji` and a Japanese author-name variant. These are two Git author names, not evidence of two independent maintainers. No hands-on reproducibility rate has been measured in this survey; README demonstrations and author's corpus statistics are not independent benchmarks.

## Comparison with Dreamtime and next evaluation

Dreamtime has a larger application domain, persisted assets, a model hub, and existing video graph work. Unbake has a more explicit source-evidence → replay-plan → experiment model and stronger control over comparisons. Remixfun should combine Dreamtime's task-oriented UI and video adapters with an independently designed evidence/manifest boundary.

Evaluate Unbake before building a competing import UI. Test a fully known recipe, a same-name wrong-version LoRA, an incomplete recipe, and a multi-sampler Comfy image. Verify restart/resume behavior and whether a one-axis change actually leaves the submitted baseline graph otherwise unchanged. If it already meets the reproduction half comfortably, the remaining product case must be desktop onboarding, durable library/lineage, and image-to-motion continuity.

## Source map and citations

[^s1]: **Capabilities, limitations, and maturity disclosures** — [Pinned source](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/README.md); [local README.md](../../../references/unbake/README.md).

[^s2]: **Record, resolution, replay, and sweep core** — [Pinned source](https://github.com/syugoji/ComfyUI-Unbake/tree/0776f99532d2edbb3e1f1400f614816932ee8bf7/web/core); [local web/core](../../../references/unbake/web/core).

[^s3]: **Exposed sweep UI** — [Pinned source](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/web/panel/sweepView.js); [local web/panel/sweepView.js](../../../references/unbake/web/panel/sweepView.js).

[^s4]: **Comfy host adapter** — [Pinned source](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/web/host/comfyHost.js); [local web/host/comfyHost.js](../../../references/unbake/web/host/comfyHost.js).

[^s5]: **Python extension and routes** — [Pinned source](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/__init__.py); [local __init__.py](../../../references/unbake/__init__.py).

[^s6]: **Normalized generation record** — [Pinned source](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/web/core/generationRecord.js); [local web/core/generationRecord.js](../../../references/unbake/web/core/generationRecord.js).

[^s7]: **GPL text** — [Pinned source](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/LICENSE); [local LICENSE](../../../references/unbake/LICENSE).

[^s8]: **Import detail and replay interaction** — [Pinned source](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/web/panel/detailView.js); [local web/panel/detailView.js](../../../references/unbake/web/panel/detailView.js).
