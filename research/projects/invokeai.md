# Invoke / InvokeAI

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/invoke-ai/InvokeAI) · [Local clone](../../../references/invokeai/) · [Raw snapshot](../evidence/invokeai.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2022-08-17 / 1,487 days (about 4.07 years) |
| Oldest reachable commit | 2021-12-21T01:59:06+01:00 — can include inherited history |
| Stars / forks / subscribers | 28,193 / 2,970 / 211 |
| Open issues + PRs | 378 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `ef832d1aa57641dd7d0c262f4d40fe8b7b420489` |
| HEAD commit | 2026-09-06T18:55:54Z Feat(text tool): Add import custom fonts (#9091) |
| Reachable commits, including merges | 19,171 |
| Historical distinct author names | 422 |
| Last 90 days: nonmerge commits / author names | 174 / 28 |
| Source license assessment | Apache-2.0; component and model terms remain separate |
| Operating systems / hardware scope | Windows, Linux, macOS; supported accelerators and model families vary |
| Distribution model | Python application with browser UI; source/package releases and separate launcher distribution |
| Fit for Remixfun | Mature creative application; current Wan video features make it a stronger competitor than older summaries suggest |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| psychedelicious | 7363 | Lincoln Stein | 58 |
| Lincoln Stein | 1908 | Alexander Eichhorn | 46 |
| Ryan Dick | 963 | Jonathan | 19 |
| blessedcoolant | 906 | Valeri Che | 14 |
| Mary Hipp | 777 | Nianze Wu | 5 |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [Version 6.14.1](https://github.com/invoke-ai/InvokeAI/releases/tag/v6.14.1) | 2026-09-06T17:16:29Z | No attached artifacts in captured expansion; check external distribution |
| [InvokeAI 6.14.0](https://github.com/invoke-ai/InvokeAI/releases/tag/v6.14.0) | 2026-08-25T23:12:16Z | No attached artifacts in captured expansion; check external distribution |
| [InvokeAI 6.14.0 (release candidate 2)](https://github.com/invoke-ai/InvokeAI/releases/tag/v6.14.0-rc2) | 2026-08-16T22:50:49Z | No attached artifacts in captured expansion; check external distribution |
| [v6.13.8](https://github.com/invoke-ai/InvokeAI/releases/tag/v6.13.8) | 2026-08-13T21:49:56Z | No attached artifacts in captured expansion; check external distribution |
| [InvokeAI 6.14.0 (release candidate 1)](https://github.com/invoke-ai/InvokeAI/releases/tag/v6.14.0-rc1) | 2026-07-31T17:38:20Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

Invoke is an established creative application with image generation, editing/canvas workflows, model management, a gallery, and an explicit invocation graph. **The inspected source also contains Wan video, interpolation, and extension workflows.** Treating it as a still-image-only alternative would understate the competition.[^s1][^s9][^s10]

It has a long history, roughly 28k stars, hundreds of historical author names, and ongoing multi-author activity. Those are strong project-health signals, while still not a measured user base. Historical Lincoln Stein-era contributions and current maintainers appear together in the table; their counts should not be read as today's staffing.

## Architecture

The backend is Python with FastAPI, Pydantic, SQLAlchemy/SQLite-backed services, a persistent session queue, model install/load/cache services, and typed invocation nodes. Diffusers/PyTorch and related libraries implement inference. The React/TypeScript frontend uses its own application state, graph construction, canvas/gallery interactions, and API bindings.[^s2][^s3][^s4][^s5][^s6]

Invoke does **not** run Comfy graphs as its core engine. Its invocation graph, model keys, metadata, and queue are its own ecosystem. A new Remixfun UI over Invoke would exchange Comfy custom-node compatibility for Invoke's model and invocation APIs; Dreamtime's existing JSON graphs would not transfer directly.

The separation between model installation, cached loading, invocation execution, and persisted output metadata is valuable. It makes explicit several responsibilities that Dreamtime currently distributes across model jobs, import records, and Comfy's own filesystem state.

## Import, replay, and controlled changes

Gallery metadata recall is a concrete user flow. Handlers restore settings from saved metadata, and richer workflow metadata can reopen a graph. Models are resolved through the application's installed model registry. That is a strong foundation for reproducing Invoke's own outputs and for iterative editing.[^s7][^s8]

The model installer accepts remote/local model sources, including Civitai-oriented URLs. However, the reviewed paths did not establish a single foreign Civitai-image import operation that recovers every original dependency and reconstructs an arbitrary non-Invoke pipeline. A model-source URL and image-generation provenance are different objects.[^s6][^s7]

Invoke is particularly strong for visual remixing through editing, masks, references, and canvas operations. The user here wants an additional form of remix: controlled recipe changes against a recovered baseline. Both can coexist, but evaluating only an inpainting demonstration would miss the core requirement.

## Video scope at this snapshot

The default workflow catalog includes Wan 2.2 text-to-video, image-to-video, two-image interpolation, and video extension, including variants with concept LoRAs and a 5B path. The backend contains video denoising, frame extraction, concatenation, and video output invocations. This is concrete source evidence, not a roadmap inference.[^s9][^s10]

A workflow existing in the catalog does not prove a novice can complete the entire image-remix-to-video journey without changing interfaces or learning nodes. First/last-frame interpolation also does not establish seamless loop quality. Those are usability and output tests still to perform.

## OS, distribution, and license

The Python package explicitly supports Windows/Linux/macOS, and its dependency declarations include platform-specific Torch choices. The source release feed is not the sole distribution channel; launcher delivery is separate. Empty binary attachments on an Invoke source release must not be reported as “no desktop installation.”[^s1][^s2]

Apache-2.0 source is a favorable reuse characteristic compared with copyleft or restricted commercial embedding licenses, but it does not remove third-party library or model terms. The architecture is still a large creative application to inherit.[^s11]

## Comparison with Dreamtime and evaluation

Dreamtime and Invoke share useful application patterns: Python APIs, jobs, persistent models/assets, and a web UI. Their execution engines differ. Dreamtime already has Comfy-specific motion and metadata adapters; adopting Invoke would mean replacing rather than merely packaging that layer.

Evaluate Invoke as a user-facing competitor and as a reference for persistent jobs, model registry design, and metadata recall. Test a foreign recipe, an Invoke-native image, an exact version mismatch, a controlled LoRA change, and a Wan interpolation/extension workflow. The distinction between excellent native round-trip and uncertain foreign reconstruction should remain visible in the results.

## Source map and citations

[^s1]: **Product and installation entry point** — [Pinned source](https://github.com/invoke-ai/InvokeAI/blob/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/README.md); [local README.md](../../../references/invokeai/README.md).

[^s2]: **Backend libraries, platform-specific dependencies, and packaging** — [Pinned source](https://github.com/invoke-ai/InvokeAI/blob/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/pyproject.toml); [local pyproject.toml](../../../references/invokeai/pyproject.toml).

[^s3]: **React/TypeScript web stack** — [Pinned source](https://github.com/invoke-ai/InvokeAI/blob/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/invokeai/frontend/web/package.json); [local invokeai/frontend/web/package.json](../../../references/invokeai/invokeai/frontend/web/package.json).

[^s4]: **FastAPI application** — [Pinned source](https://github.com/invoke-ai/InvokeAI/blob/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/invokeai/app/api_app.py); [local invokeai/app/api_app.py](../../../references/invokeai/invokeai/app/api_app.py).

[^s5]: **Persistent generation queue** — [Pinned source](https://github.com/invoke-ai/InvokeAI/tree/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/invokeai/app/services/session_queue); [local invokeai/app/services/session_queue](../../../references/invokeai/invokeai/app/services/session_queue).

[^s6]: **Model import/install services** — [Pinned source](https://github.com/invoke-ai/InvokeAI/tree/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/invokeai/app/services/model_install); [local invokeai/app/services/model_install](../../../references/invokeai/invokeai/app/services/model_install).

[^s7]: **Metadata handlers and recall** — [Pinned source](https://github.com/invoke-ai/InvokeAI/blob/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/invokeai/frontend/web/src/features/metadata/parsing.tsx); [local invokeai/frontend/web/src/features/metadata/parsing.tsx](../../../references/invokeai/invokeai/frontend/web/src/features/metadata/parsing.tsx).

[^s8]: **Gallery recall interaction** — [Pinned source](https://github.com/invoke-ai/InvokeAI/blob/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/invokeai/frontend/web/src/features/gallery/hooks/useRecallAllImageMetadata.ts); [local invokeai/frontend/web/src/features/gallery/hooks/useRecallAllImageMetadata.ts](../../../references/invokeai/invokeai/frontend/web/src/features/gallery/hooks/useRecallAllImageMetadata.ts).

[^s9]: **Shipped image/video/interpolation/extension workflows** — [Pinned source](https://github.com/invoke-ai/InvokeAI/tree/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/invokeai/app/services/workflow_records/default_workflows); [local invokeai/app/services/workflow_records/default_workflows](../../../references/invokeai/invokeai/app/services/workflow_records/default_workflows).

[^s10]: **Wan video invocation** — [Pinned source](https://github.com/invoke-ai/InvokeAI/blob/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/invokeai/app/invocations/wan_video_denoise.py); [local invokeai/app/invocations/wan_video_denoise.py](../../../references/invokeai/invokeai/app/invocations/wan_video_denoise.py).

[^s11]: **Apache source license** — [Pinned source](https://github.com/invoke-ai/InvokeAI/blob/ef832d1aa57641dd7d0c262f4d40fe8b7b420489/LICENSE); [local LICENSE](../../../references/invokeai/LICENSE).
