# genrecord

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/syugoji/genrecord) · [Local clone](../../../references/genrecord/) · [Raw snapshot](../evidence/genrecord.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2026-08-19 / 23 days (about 0.06 years) |
| Oldest reachable commit | 2026-08-20T01:42:22+09:00 — can include inherited history |
| Stars / forks / subscribers | 0 / 0 / 0 |
| Open issues + PRs | 0 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c` |
| HEAD commit | 2026-08-20T01:57:03+09:00 drop private flag for publication |
| Reachable commits, including merges | 2 |
| Historical distinct author names | 1 |
| Last 90 days: nonmerge commits / author names | 2 / 1 |
| Source license assessment | AGPL-3.0 with a documented commercial licensing option |
| Operating systems / hardware scope | Portable JavaScript library; no GPU, network, UI, or server required |
| Distribution model | Library source/package; no GitHub releases captured |
| Fit for Remixfun | Reference for normalized evidence, sufficiency, provenance, and variation planning |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| syugoji | 2 | syugoji | 2 |

### Release evidence

No GitHub release entries were captured. This does not exclude registry packages, git installation, external installers, or a private release process.

## Assessment

genrecord is a conceptual/data-model reference, not an alternative desktop application. It separates provenance, reproducibility, permissible-use evidence, and possible variations. That is useful because knowing which model probably created an image is different from possessing the files and execution conditions needed to recreate it.[^s1][^s2][^s6][^s8]

The snapshot is a very young, two-commit project with no stars. Claims about its performance on the author's own image folder should be treated as self-reported evaluation of that corpus, not coverage of arbitrary Civitai images or current Comfy node packs.

## Architecture and boundaries

It is dependency-free JavaScript with no network access. Callers provide records, model inventories, and licensing catalogs. Modules handle parameter/image parsing, graph traversal, name/evidence matching, record sufficiency, resolution, provenance, and variation planning. There is no download manager, queue, GPU runtime, persistent application database, or UI hidden behind the library API.[^s1][^s2][^s3][^s5][^s7]

This is a useful shape for a Remixfun domain layer: the reasoning about an imported record should be testable without starting Comfy or downloading models. It also exposes a tradeoff. A JavaScript core fits the React/Tauri client, while Dreamtime's existing parsing and job logic is Python. Avoid implementing the same canonical decisions independently in both languages; choose one authority and expose it through the application API.

## Evidence fidelity

The strongest input is a structured ledger or richer LoRA Manager recipe that includes hashes, source IDs, version IDs, and model-family information. Extraction from image metadata is weaker. The README explicitly distinguishes these paths: a graph can provide a model filename without a verified content hash or a trustworthy license lookup key.[^s1][^s3][^s4]

Graph traversal follows relationships to generation nodes instead of simply taking the first sampler anywhere in a file. Ambiguous paths are left unresolved with machine-readable reasons. This is preferable to plausible but incorrect flattening. It also means refusal is expected for some multi-stage or unusual graphs and should be surfaced as useful information.[^s4][^s6]

The licensing assessor consumes a catalog supplied by the caller. It does not independently establish model ownership, legal permission, or the accuracy of a website's labels. Remixfun can record the evidence and unknowns without pretending a library calculation grants rights.[^s8]

## Target workflow and Dreamtime comparison

genrecord can normalize and assess an imported recipe and suggest viable variation axes; it cannot fetch Civitai metadata, install a missing checkpoint, run the baseline, or animate the result. Those steps remain the surrounding application's responsibility. Dreamtime already supplies many of them, making the ideas complementary.[^s5][^s7]

The most useful lessons are field-level evidence, explicit unknown states, graph-aware extraction, and a difference between “not recorded,” “not identifiable,” and “not installed.” In Dreamtime, resource availability already has useful version-aware states; a richer record can extend that vocabulary to the entire recipe and runtime.

## Distribution and reuse

The root license is AGPL-3.0 and a commercial option is documented. This is not a drop-in permissive parsing library. The architecture can be studied independently; copying its implementation entails the actual license terms. No adoption or long-term support inference should be made from a readable API and extensive README alone.[^s9][^s10]

Evaluate on a deliberately mixed corpus: A1111 text metadata, ordinary Comfy graphs, multiple samplers, missing LoRA hashes, and metadata-stripped images. Compare extracted fields and refusal reasons with Dreamtime. Success should be measured as correct facts plus honest unknowns, not the maximum number of filled fields.

## Source map and citations

[^s1]: **Scope and input limitations** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/README.md); [local README.md](../../../references/genrecord/README.md).

[^s2]: **Canonical record representation** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/src/generationRecord.mjs); [local src/generationRecord.mjs](../../../references/genrecord/src/generationRecord.mjs).

[^s3]: **Image ingestion** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/src/fromImage.mjs); [local src/fromImage.mjs](../../../references/genrecord/src/fromImage.mjs).

[^s4]: **Graph-aware extraction** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/src/workflowGraph.mjs); [local src/workflowGraph.mjs](../../../references/genrecord/src/workflowGraph.mjs).

[^s5]: **Resource resolution** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/src/resolve.mjs); [local src/resolve.mjs](../../../references/genrecord/src/resolve.mjs).

[^s6]: **Completeness assessment** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/src/recordSufficiency.mjs); [local src/recordSufficiency.mjs](../../../references/genrecord/src/recordSufficiency.mjs).

[^s7]: **Variation planning** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/src/variation.mjs); [local src/variation.mjs](../../../references/genrecord/src/variation.mjs).

[^s8]: **Caller-supplied licensing evidence** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/src/license.mjs); [local src/license.mjs](../../../references/genrecord/src/license.mjs).

[^s9]: **AGPL source license** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/LICENSE); [local LICENSE](../../../references/genrecord/LICENSE).

[^s10]: **Commercial option** — [Pinned source](https://github.com/syugoji/genrecord/blob/b885d461deb77e07f7fd109cd4cc3ca5e21ebf5c/COMMERCIAL.md); [local COMMERCIAL.md](../../../references/genrecord/COMMERCIAL.md).
