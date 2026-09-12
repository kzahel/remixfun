# Visionatrix

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/Visionatrix/Visionatrix) · [Local clone](../../../references/visionatrix/) · [Raw snapshot](../evidence/visionatrix.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:58:15.967620+00:00 |
| Repository creation / age | 2024-02-29 / 925 days (about 2.53 years) |
| Oldest reachable commit | 2024-02-29T11:44:23+03:00 — can include inherited history |
| Stars / forks / subscribers | 169 / 16 / 2 |
| Open issues + PRs | 6 (GitHub combined count) |
| Archived on GitHub | True |
| Inspected branch / HEAD | main / `9f56eb5443371bed89e3f96ffc971ec46f9ac7fd` |
| HEAD commit | 2025-12-12T19:07:42+02:00 archive repo |
| Reachable commits, including merges | 720 |
| Historical distinct author names | 8 |
| Last 90 days: nonmerge commits / author names | 0 / 0 |
| Source license assessment | AGPL-3.0-or-later |
| Operating systems / hardware scope | Windows portable CUDA/CPU; Linux/macOS source paths; Docker/remote workers |
| Distribution model | Python/Nuxt web app, CLI/service, Docker images, Windows portable archive; archived repository |
| Fit for Remixfun | Closest service/worker/preset architecture reference; archived, so not recommended as maintained foundation |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Alexander Piskun | 525 | — | — |
| pre-commit-ci[bot] | 66 | — | — |
| Andrey Borysenko | 65 | — | — |
| bigcat88 | 39 | — | — |
| dependabot[bot] | 8 | — | — |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v2.7.0](https://github.com/Visionatrix/Visionatrix/releases/tag/v2.7.0) | 2025-07-26T11:59:17Z | `vix_portable_cuda.7z` |
| [v2.6.0](https://github.com/Visionatrix/Visionatrix/releases/tag/v2.6.0) | 2025-07-13T11:52:35Z | `vix_portable_cuda.7z` |
| [v2.5.1](https://github.com/Visionatrix/Visionatrix/releases/tag/v2.5.1) | 2025-06-06T08:14:04Z | `vix_portable_cuda.7z` |
| [v2.5.0](https://github.com/Visionatrix/Visionatrix/releases/tag/v2.5.0) | 2025-05-30T07:08:28Z | `vix_portable_cuda.7z` |
| [v2.4.1](https://github.com/Visionatrix/Visionatrix/releases/tag/v2.4.1) | 2025-05-18T13:07:18Z | `vix_portable_cuda.7z` |

## Assessment

Visionatrix is particularly close to the proposed service architecture: a simplified Comfy workflow UI, installable/versioned flows, model acquisition, persistent tasks, workers, and CLI/API deployment. It is also explicitly archived. The live repository/API and cloned README supersede search snippets that still describe it as an actively maintained option.[^s1]

## Architecture

Python FastAPI/Pydantic services, SQLAlchemy/database migrations, and a Nuxt/Vue/Pinia frontend sit above Comfy. Flow definitions connect UI inputs to workflow nodes and model catalog requirements. Model mapping/install services prepare resources; the task engine runs work through the Comfy integration.[^s2][^s3][^s4][^s5][^s6][^s7][^s8]

CLI modes and worker/service separation support deployment beyond one desktop process. Database and task abstractions make it a closer comparison to Dreamtime than a thin JavaScript form builder. That breadth also carries authentication, multi-user, scheduling, migration, and installation maintenance costs.[^s2][^s7][^s9]

## Workflow overlap and missing proof

Installing a flow with its required models and then running it through simple controls is highly aligned with Remixfun's video presets. Civitai LoRA integration and send-to-flow concepts connect outputs to subsequent tasks. These features demonstrate that downloadable workflows plus hidden nodes are established ideas.[^s1][^s4][^s6]

A catalog-managed flow is still different from reconstructing an arbitrary foreign image. The review did not establish an exact source-recipe replay and controlled-diff product. Its value for this survey is the flow/model/task architecture and the practical work involved in maintaining it.

## OS, distribution, and maintenance

The project documented Linux/macOS/source setup, Windows portable CUDA/CPU delivery, and Docker/remote service modes. Captured releases include a Windows portable archive. GPU/model parity across those modes was not independently tested.[^s1]

The repository was archived after an explicit capacity statement; the last inspected commit is the archive update. This is firmer evidence than merely observing zero recent commits. Archive status does not make the code unusable, but adopting it means owning compatibility and operational fixes yourself.[^s1]

Source is AGPL-3.0-or-later, with separate Comfy/node/model terms. Historical authorship and stars describe this repository's history, not a current support organization.[^s2][^s10]

## Comparison with Dreamtime and recommendation

Dreamtime already uses similar Python application components but maintains task-specific graph adapters instead of a general flow marketplace. Remixfun can borrow the architectural lesson—version a preset together with its requirements and UI schema—without inheriting Visionatrix's whole multi-user service stack.

Inspect and test model catalog mapping, installation failure recovery, output-to-next-flow transfer, and separation of data from runtime directories. Use these as design references. Do not choose an archived dependency as the quickest route to a new maintained desktop product without explicitly budgeting the ownership it transfers.

## Source map and citations

[^s1]: **Archive declaration, features, and install modes** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/README.md); [local README.md](../../../references/visionatrix/README.md).

[^s2]: **Python API/database dependencies** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/pyproject.toml); [local pyproject.toml](../../../references/visionatrix/pyproject.toml).

[^s3]: **Nuxt/Vue/Pinia frontend** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/web/package.json); [local web/package.json](../../../references/visionatrix/web/package.json).

[^s4]: **Versioned workflow installation and management** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/visionatrix/flows.py); [local visionatrix/flows.py](../../../references/visionatrix/visionatrix/flows.py).

[^s5]: **Model installation** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/visionatrix/models.py); [local visionatrix/models.py](../../../references/visionatrix/visionatrix/models.py).

[^s6]: **Graph-to-model catalog mapping** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/visionatrix/models_map.py); [local visionatrix/models_map.py](../../../references/visionatrix/visionatrix/models_map.py).

[^s7]: **Task execution** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/visionatrix/tasks_engine.py); [local visionatrix/tasks_engine.py](../../../references/visionatrix/visionatrix/tasks_engine.py).

[^s8]: **Comfy integration** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/visionatrix/comfyui_wrapper.py); [local visionatrix/comfyui_wrapper.py](../../../references/visionatrix/visionatrix/comfyui_wrapper.py).

[^s9]: **CLI/service entry points** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/visionatrix/__main__.py); [local visionatrix/__main__.py](../../../references/visionatrix/visionatrix/__main__.py).

[^s10]: **AGPL license** — [Pinned source](https://github.com/Visionatrix/Visionatrix/blob/9f56eb5443371bed89e3f96ffc971ec46f9ac7fd/LICENSE.txt); [local LICENSE.txt](../../../references/visionatrix/LICENSE.txt).
