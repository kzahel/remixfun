# CiviImport

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/Kiriouchine/CiviImport) · [Local clone](../../../references/civiimport/) · [Raw snapshot](../evidence/civiimport.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:50:24.985385+00:00 |
| Repository creation / age | 2026-09-06 / 5 days (about 0.01 years) |
| Oldest reachable commit | 2026-09-06T20:41:05+02:00 — can include inherited history |
| Stars / forks / subscribers | 1 / 0 / 0 |
| Open issues + PRs | 0 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `b2c854bb76f8b84f728a74c277e3f562625aebe2` |
| HEAD commit | 2026-09-06T21:21:01+02:00 Added image |
| Reachable commits, including merges | 6 |
| Historical distinct author names | 1 |
| Last 90 days: nonmerge commits / author names | 6 / 1 |
| Source license assessment | MIT |
| Operating systems / hardware scope | ComfyUI extension; OS and GPU support inherit the host and graph nodes |
| Distribution model | Git/custom-node installation; no release feed or desktop installer captured |
| Fit for Remixfun | Direct Civitai URL → missing models → reconstructed Comfy graph competitor |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| Sev (Vsevolod) Kiriouchine | 6 | Sev (Vsevolod) Kiriouchine | 6 |

### Release evidence

No GitHub release entries were captured. This does not exclude registry packages, git installation, external installers, or a private release process.

## Assessment

This is one of the closest implementations of the exact entry workflow: paste a Civitai image URL, recover its recipe, resolve local resources, download missing files, and construct an editable Comfy graph. It challenges the novelty of that mechanism directly. It does not establish broad adoption: the snapshot is less than a week after repository creation, with one star, six commits, and one author name.[^s1]

## Architecture

The extension divides the workflow into reasonably small Python modules: Civitai acquisition, local model inventory, hashing, downloads, graph generation, and HTTP routes. A JavaScript panel runs inside the existing Comfy frontend. Comfy remains the inference server and graph editor; CiviImport does not introduce an independent database-backed desktop application.[^s2][^s3][^s4][^s5][^s6][^s7][^s8]

The service follows image URL → Civitai response → normalized recipe/resources → installed-file resolution → optional downloads → graph. Public endpoints and tRPC fallback are used to recover fields not consistently supplied in one response. The local resolver integrates with Comfy model paths rather than assuming every resource lives in one hardcoded directory.[^s2][^s3]

## What it covers in the target workflow

| Stage | Evidence and limitation |
|---|---|
| Import Civitai image | Directly implemented; metadata availability still constrains recovery |
| Resolve checkpoint/LoRAs/other resources | Version/hash-aware lookup and local scanning |
| Download exact resource | Expected SHA-256, or weaker AutoV2 prefix, checked before final rename |
| Reconstruct baseline | Explicit graph builder; also makes assumptions where the source is incomplete |
| Controlled remix/compare | Graph is editable, but no durable experiment lineage/sweep product established |
| Animate selected result | Comfy can do it through other workflows; no integrated video journey established |

The downloader uses temporary partial files and verifies the expected digest before promoting the download. Full SHA-256 is preferred; an AutoV2 prefix is a partial identity check, not equivalent assurance. The hash cache avoids re-reading large files unnecessarily, with size/mtime used to recognize cache validity.[^s4][^s5]

## Reproduction caveat: reconstruction includes invention

The graph builder synthesizes a conventional checkpoint/CLIP/LoRA/sampler/VAE image pipeline. Its base-resolution heuristics and second sampling pass are especially important: the code can add a hires chain when metadata does not fully specify one. Fallback refine values include a low denoise and derived step/CFG settings. Those are practical approximation choices, but must not be reported as recovered source facts.[^s6]

A model-family hint is not a complete execution adapter. For example, recognizing “Flux” in a resolution heuristic does not prove the conventional checkpoint graph correctly handles every Flux packaging format or encoder arrangement. Test complete graph behavior, not a string in a supported-model list.[^s6]

This distinction is central for Remixfun. An importer can be good at making a plausible new image while still being unable to reproduce the source. Preserve every assumption and make synthetic refinements explicit; the baseline should not silently include embellishments.

## Packaging, license, and operational exposure

The application is installed into a Comfy custom-node environment, so its apparent setup simplicity presupposes a working host. The exported graph uses ordinary Comfy nodes where possible, reducing ongoing dependence on the importing extension. There are no standalone desktop assets in the captured release feed. Source is MIT; model licenses and Comfy's license are separate.[^s1][^s6][^s9]

The concentrated authorship and extremely young history increase uncertainty about API breakage, model-family coverage, and future maintenance. That is a reason to evaluate carefully, not evidence that its implementation is ineffective.

## Comparison with Dreamtime and useful lessons

Dreamtime already has the stronger persistent application shell: imports, jobs, workspace inventory, separate generators, and video adapters. CiviImport is more focused on turning the imported recipe into an inspectable graph and has a stronger expected-hash download check in the inspected path. Its small modules are useful references for strengthening Dreamtime's resolver/download boundary.[^s3][^s5][^s6]

Evaluation should use an SDXL image with known checkpoint version, two LoRAs, an embedding, and published hashes; then repeat with a missing VAE, stripped metadata, and ambiguous hires data. Record what was recovered versus invented. Test extra model paths and same-name/different-hash files. Do not conclude it satisfies Remixfun's complete workflow merely because the generated graph queues successfully.

## Source map and citations

[^s1]: **User workflow and installation** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/README.md); [local README.md](../../../references/civiimport/README.md).

[^s2]: **Metadata acquisition and resource resolution** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/civitai_api.py); [local civitai_api.py](../../../references/civiimport/civitai_api.py).

[^s3]: **Installed model lookup** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/local_models.py); [local local_models.py](../../../references/civiimport/local_models.py).

[^s4]: **File identity and hash cache** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/hashing.py); [local hashing.py](../../../references/civiimport/hashing.py).

[^s5]: **Atomic downloads and expected-digest verification** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/downloader.py); [local downloader.py](../../../references/civiimport/downloader.py).

[^s6]: **Graph assembly and inferred generation stages** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/graph_builder.py); [local graph_builder.py](../../../references/civiimport/graph_builder.py).

[^s7]: **Comfy HTTP integration** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/routes.py); [local routes.py](../../../references/civiimport/routes.py).

[^s8]: **Browser panel** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/web/js/civiimport.js); [local web/js/civiimport.js](../../../references/civiimport/web/js/civiimport.js).

[^s9]: **MIT source license** — [Pinned source](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/LICENSE); [local LICENSE](../../../references/civiimport/LICENSE).
