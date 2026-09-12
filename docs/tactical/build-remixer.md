# Remixfun product and implementation plan

**Status: current build plan, 2026-09-12.** The first local app slice is implemented: shared service/CLI, browser import/library, explicit demo jobs and Windows developer shell. Model downloads and real generation remain unimplemented. See [local preview evidence](../evidence/local-preview.md). Competitive trials remain outside the implementation prerequisites.

### Local preview checkpoint

The user requested a runnable basic version, screenshots, a commit, and a stop
at a reasonable signing/publishing handoff. The local preview provides the app
and service payload to package. Continue operational work using the
[signed delivery plan](signed-desktop-delivery.md), with private provisioning
and deployment performed on an infrastructure-equipped machine.

M0 is partial: the core import/result flow, persistence, CLI and desktop shell
exist. Public SDXL fixture acquisition, current Comfy profile selection and
real engine work remain open. Anonymous Civitai acquisition returned HTTP 403
from the development machine; original-image upload and recorded-response
tests work. No public reproduction fixture or image-match result was invented.
The authored demo is only a UI/service fixture. Full M1 reproduction acceptance
still gates a supported reproduction release, even if signing setup starts now.

## 1. Product contract

Build an opinionated, easy-to-use desktop remixer whose headline feature is **Civitai image reproduction and remixing**, with automatic acquisition of the relevant models and a few simple video workflows. Advanced generation controls are hidden by default.

The normal journey is:

1. Paste a Civitai image URL or drop an image.
2. See the source image and a concise recipe summary.
3. Reuse installed models and download missing supported dependencies, with clear progress and total required space.
4. Reproduce the source recipe; recover missing batch/seed position where possible.
5. Edit the prompt or a small set of meaningful remix controls and compare results.
6. Choose an image and animate it with a compatible preset.
7. Reopen the result later with its recipe, models, seed, and parent image intact.

Decisions from the user: build our app; use Dreamtime as the implementation starting point; modernize Comfy integration; desktop experience plus headless operation and optional network listening; strong automated testability; prioritize basic SDXL source reproduction fixtures. Reference applications remain source-only research unless the user later chooses otherwise.

Recommended implementation choices: React/Vite UI, Python/FastAPI application service and domain code, Comfy as the execution engine, Tauri desktop shell, Desktop Release Kit distribution contracts, SQLite metadata plus filesystem artifacts. Windows/NVIDIA first, with portable paths/process boundaries from the outset; Linux and Apple Silicon support expand through tested runtime profiles.

## 2. Small default UI

| Surface | Default controls | Advanced, collapsed by default |
|---|---|---|
| Import/reproduce | Source preview, recovered prompt, required downloads, Reproduce, comparison | Raw metadata, unresolved fields, source versions, batch recovery details |
| Remix | Prompt, a small preset-specific set of style/LoRA strengths, Generate, compare/select | Seed, steps, CFG, sampler/scheduler, clip skip, VAE, exact model versions |
| Animate | Source image, motion prompt, supported duration/quality presets, optional end image | Model-specific tuning, seed, supported extension/loop details |
| Library | Imports and results, simple search, reopen/remix/animate | Full manifest, model storage and diagnostics |
| Settings | Storage location, Civitai credential, runtime status, network access | Listen address/port, external engine, logs, maintenance/recovery |

The imported baseline keeps recorded source settings even if they differ from the app's usual defaults. Imported resources can be displayed in plain terms while technical provenance stays behind a details panel. No prompt enhancement, substituted model, hires pass, or other default may silently change the baseline.

Dependency acquisition is part of import, not a separate mandatory model-browser task. Show what will be downloaded; reuse a previous choice for the same exact resource. Missing authentication, license acceptance, unavailable files, or an unsupported recipe gets one actionable explanation. Routine supported imports should not trigger a chain of configuration questions.

V1 has no node editor, arbitrary custom-node installer, general model marketplace, training, checkpoint merging, music/storyboards, multi-user administration, or generic workflow app builder. Keep internal flexibility behind a deliberately small supported recipe/preset set.

## 3. Desktop, headless, and network modes use the same service

The Python service owns import, recipe resolution, downloads, jobs, history, and engine supervision. The web client and CLI use its API. Tauri supplies the native window, dialogs, application lifecycle, and updates. Required service/runtime logic must work without a webview or JavaScript client running.

Proposed module layout, to be created during implementation:

```text
web/                         React UI shared by desktop and browser
desktop/                     Tauri shell and Release Kit integration
backend/remixfun/domain/      Records, manifests, diffs, dependency plans
backend/remixfun/providers/   Civitai acquisition and image metadata adapters
backend/remixfun/storage/     SQLite, source/output files, model inventory
backend/remixfun/downloads/   Verified, resumable transfers
backend/remixfun/engines/     Comfy adapter and process/runtime supervisor
backend/remixfun/presets/     Curated image/video graph builders
backend/remixfun/api/         HTTP commands and progress events
backend/remixfun/cli/         Headless commands, machine-readable output
tests/fixtures/              Recorded provider metadata and recipe fixtures
tests/gpu/                   Explicit real-engine reproduction/upgrade tests
```

Target CLI contract (the implemented subset is documented in [development](../../DEVELOPMENT.md)):

```text
remixfun serve
remixfun serve --host 0.0.0.0 --port 8788 --auth-token-file <path>
remixfun import <civitai-image-url> --json
remixfun reproduce <import-id> --recover-batch --wait --json
remixfun remix <run-id> --prompt <text> --wait --json
remixfun animate <image-id> --preset <preset-id> --wait --json
```

Desktop starts a managed local service or attaches to its already-running instance. Use a single-instance/process identity and explicit ownership to avoid duplicate engines. Closing the desktop window should not accidentally kill an independently started headless service. The default desktop-owned service can exit with the app when idle; keeping jobs running is an explicit preference. Shutdown behavior must be tested with active jobs.

Networking is local-only by default. Enabling network access publishes the **Remixfun API and web UI**, while the managed Comfy server stays on loopback. Settings expose an enable toggle and port, with advanced bind-address selection. Require authentication for remote access, including progress streams and media endpoints; use deliberate browser pairing/session exchange rather than long-lived tokens in URLs. Keep credentials out of recipe exports/logs. Do not open router ports or configure internet exposure automatically. Test bind/auth/origin behavior, occupied ports, and restart with changed settings.

## 4. Reproduction and batch-position recovery

The user reports a concrete failure in prior Civitai reproduction work: a stored seed identifies the batch start, while the selected image's offset `n` is absent, so the effective seed may be `start_seed + n`. Treat this as a required fixture and recovery case, not a rare error the user must debug manually. It has not yet been reproduced against a saved example during this work.

Do not assume this describes all providers, upload formats, or generators. Preserve explicit per-image seed, batch position, size, and embedded graph data whenever present. Historical Civitai API examples contain a `Batch pos` field in some metadata; that is a reason to inspect available evidence, not proof it is available for the user's images.[^1]

There are two materially different recovery strategies:

| Strategy | Candidate identity | When appropriate |
|---|---|---|
| Incremented seed | recorded start seed + candidate offset | Source generator assigns a new integer seed to each image |
| Shared-seed noise stream | original seed + noise/batch index, possibly original batch size | Source generator draws a tensor batch or successive noise samples from one seeded generator |

Comfy's inspected noise code supports the latter pattern. The nth noise sample from one seeded stream is not generally equivalent to starting a new stream at `seed + n`. Recreating selected noise also does not guarantee identical downstream batched numerical execution. Preserve batching mode and batch size when known; validate candidate replay under the supported engine profile.[^2]

Recovery algorithm:

1. Gather all available source evidence, including original file metadata, provider responses, embedded graph, and explicit batch fields. Do not infer generation order from a gallery's display order.
2. Resolve exact supported model files and generation settings first. A seed search must not conceal a known wrong checkpoint or missing conditioning stage.
3. Try the best-supported candidate. If metadata leaves batch position unresolved, offer a simple **Find matching image** action.
4. Run a bounded candidate set, initially offsets/indices 0–7 for the supported strategy. This is a proposed product default, not a claim about Civitai batch limits. Allow expansion to 0–31 in advanced controls or on a clear request; deduplicate candidates, show estimated work, and support cancel/resume.
5. Hold all other recipe fields fixed. Do not scan arbitrary sampler/CFG/model combinations automatically.
6. Compare decoded output pixels with a suitable original reference. Stop on an exact match. Where only a resized/recompressed web reference exists, rank similarity but label it as similarity; retain the best candidates for inspection.
7. Persist the recovered effective seed or noise index, batching strategy/size, runtime identity, and evidence of the match. Keep the original reported seed separately. Future remixes use the resolved baseline directly.
8. Report no match as no match. Preserve the search history and remaining unknowns; do not label the highest similarity score exact.

For Remixfun's own new variations, default to separate per-image tasks with explicit effective seeds. Performance batching can be added only when it preserves the documented semantics. Every output should retain enough information to rerun that exact image without another offset search.

## 5. SDXL fixtures and exactness

The first reproduction milestone uses a few basic public Civitai SDXL images. Identify candidates through read-only metadata acquisition; prefer ordinary landscape/object/illustration examples with complete settings and accessible exact model files. Begin with one checkpoint and no hires, refiner, detailer, ControlNet, or LoRA; then add one LoRA and a known missing-batch-offset case. A public image must have sufficiently trustworthy original image bytes for a claim of decoded-pixel equality.

Store source URL/image ID, acquisition date, raw metadata, image hash/dimensions/encoding, model/version/file IDs, expected/observed file hashes, source-engine clues, and known/unknown settings. Respect redistribution conditions: restricted weights never go into Git; restricted reference images can be fetched into a local test cache through a manifest. API response fixtures must omit credentials and transient signed URLs.

Maintain two complementary fixture sets:

- **Public source fixtures:** prove that real imported images can be recovered, including the user's batch-offset failure. Metadata completeness may vary; record that honestly.
- **Controlled local fixtures:** generate known SDXL batches, deliberately strip per-image seed/index metadata, and verify recovery. These provide ground truth for both batching strategies and prevent a changing website from being the sole test oracle.

Separate fixed-profile repeatability, exact decoded-pixel source equality, and perceptual similarity. Exact equality on selected fixtures is a release gate for the supported reproduction profile; it is not a promise that every arbitrary Civitai image can be reconstructed. If a source used a different conditioning/RNG/pipeline implementation, record the mismatch and either add a narrow reviewed compatibility adapter or classify it as unsupported/approximate. Never relabel it exact to pass a milestone.

## 6. Modernize Comfy and Dreamtime together

Dreamtime's checked-in setup currently records Comfy commit `d9dc02a7d602a1918b9dabfc91890e6689f6f16d` from 2026-01-13. That is configuration evidence, not a verification of which engine is presently running on every machine.[^3]

Use a current stable Comfy release as the candidate at implementation time; record the exact commit and compatible Python/Torch/node dependencies. Pin the tested combination. Do not make every app launch pull the latest engine or latest custom nodes.

Migration sequence:

1. Inventory Dreamtime image/video graph requirements, actual available runtime configuration, and existing reproduction fixtures. Preserve the old configuration and useful artifacts.
2. Set up an isolated current Comfy profile for Remixfun. Keep large model storage shareable, but Python/node environments separate. Reference clones remain research checkouts.
3. Port the minimal SDXL adapter to current core nodes first. Add reviewed compatibility code only where necessary for the selected source fixtures.
4. Run graph-contract and real-engine fixtures, including effective prompt/conditioning, seed strategy, VAE, sampler/scheduler, LoRA application, and repeatability.
5. Port one image-to-video preset, then end-frame/loop/extension features supported by that preset. Fail clearly if a capability is unavailable; the old Wan 5B path must not silently skip a requested loop.
6. Apply compatible fixes and updated runtime documentation to the actual Dreamtime repository as a parallel migration deliverable. Avoid importing its music/project domain into Remixfun. Use small shared adapters only where both apps truly need the same implementation; do not prematurely create a broad shared framework.
7. Promote the new Dreamtime runtime after its retained workflows pass. Keep an explicit rollback profile and record output changes. A modern engine upgrade can legitimately change numerical results, so preserve versioned baselines rather than overwriting them.

Updating the app, updating an engine profile, and acquiring a model are separate lifecycles. Desktop Release Kit governs signed application delivery; it does not itself provide Python/Torch/model compatibility.

## 7. Downloads, persistence, and curated motion

Retain Dreamtime's provider parsing and version-aware availability concepts. Strengthen them with model/file/hash identity, expected-digest verification, compatible transfer resume, atomic promotion, and restart reconciliation. Installed exact bytes should be reusable across recipes and engine instances. User data, model cache, and runtime environments live outside the installed application bundle.

Use a small persistent model: source/import, normalized recipe with provenance, resolved baseline manifest, generation run, variant diff, model blob/reference, download job, and motion run. Store the submitted graph and exact selected input image hash. Keep unmodified source metadata even after resolving an offset or choosing a different model.

Start motion with one reliable image-to-video preset. Add an end-image field and loop/extend actions when tested on the selected model. Quality/duration choices should be curated and hardware-aware. Advanced details stay collapsed; unsupported requests must not be silently ignored. Every video links back to the selected image and its remix recipe.

## 8. Test architecture

| Layer | Tests | Required environment |
|---|---|---|
| Pure domain | Metadata normalization, unknown fields, exact identities, candidate seed/index plans, immutable baseline and diff | CPU only; no network or Comfy imports |
| Provider adapter | Recorded REST/metadata responses, incomplete/gated/deleted cases, retry/auth redaction | Fixtures and fake HTTP service |
| Download/storage | Resume and incompatible validators, corrupt hash, interrupted promotion, restart, existing library paths | Local fixture HTTP server and temp filesystem |
| API/CLI | Same command behavior, job IDs, machine-readable output, auth/network settings, errors/exit statuses | Service with injected fake engine |
| Browser UI | Paste/import → progress → reproduce → advanced controls → remix → animate; failure states | Playwright against our service/fake engine |
| Comfy adapter | Submission/progress/history/upload/output contracts, schema compatibility, unknown job reconciliation | Recorded/fake protocol tests plus current engine smoke tests |
| Real reproduction | SDXL native round trip, public Civitai source cases, both batch strategies, model/LoRA exactness | Pinned Windows/NVIDIA profile and cached permitted models |
| Real video | Correct source/end frames, supported loop/extension, frame counts, output provenance | Pinned video profile |
| Desktop/release | Startup, single instance, process ownership, close/restart, paths, installed old-to-new updates | OS-specific Tauri builds/testbeds |

Inject engine, provider, downloader, clock, and storage boundaries where they have external effects. Fake-engine success must not count as real reproduction success. Fast tests run without credentials or GPUs; a small explicit GPU suite runs for graph/runtime changes and release qualification. Record actual hardware/profile in test artifacts and skip with a visible reason where unavailable.

Add regression tests specifically for reported start seed with missing offset, missing noise-stream batch index, explicit index overriding inference, search cancellation/resume, budget exhaustion, unsigned/unknown source values, and lost connection after an engine accepted a job. Verify one-axis changes at manifest/graph level as well as through the UI.

## 9. Implementation milestones and acceptance

Signed CI, Stable/Nightly tracks, and machine-control installer acceptance are required.
See the [release contract](../topics/releases.md) and [delivery plan](signed-desktop-delivery.md).

| Milestone | Deliverable | Acceptance |
|---|---|---|
| M0 — skeleton and fixtures | Desktop shell, shared web/API/CLI skeleton, fake engine, fixture acquisition manifests, current runtime candidate | Normal import/result flow testable without GPU; desktop and headless share service behavior |
| M1 — first real reproduction | Current Comfy SDXL adapter, exact model resolution/downloads, source baseline record | At least one suitable public SDXL source matched exactly on the supported profile; controlled native fixture repeatable |
| M2 — missing-batch recovery | Bounded seed-offset/noise-index recovery and retained effective identity | Controlled cases recover the correct image; a real affected Civitai example is tested when identifiable; no false exact labels |
| M3 — opinionated remixer | Prompt/limited style controls, collapsed advanced panel, variant history/comparison | Reopen and rerun a selected variant; all undeclared baseline fields stay fixed |
| M4 — simple motion | One I2V preset, then supported end-frame/loop/extension | Correct selected image used; controls reflect actual capabilities; output lineage survives restart |
| M5 — distribution and Dreamtime promotion | Windows managed runtime + signed Release Kit pipeline; Dreamtime adapter/runtime updates | Clean install, network-auth tests, headless jobs, restart recovery, installed update preserving data; retained Dreamtime smoke tests pass |

Windows packaging/lifecycle is exercised from M0; polished signed distribution lands after the real workflow is reliable. Dreamtime compatibility work begins with M1 and is promoted once validated. Linux and Apple Silicon use the same domain/API; support is declared by tested runtime profile, with simpler image scope on Mac initially if needed.

There is no competitor-evaluation milestone. The next development work is M0/M1: establish the small app contract, select a suitable SDXL fixture, and prove the real current-Comfy reproduction path.

## Sources for technical constraints

[^1]: [Historical official Civitai API example](https://github.com/civitai/civitai/wiki/REST-API-Reference/e34d23767078ec6f536ec824a9cf95840d918dbc), inspected 2026-09-12. Some example metadata includes batch position; no universal current availability is inferred. The missing-offset case is the user's reported experience and needs a captured fixture.
[^2]: [Comfy noise preparation](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy/sample.py); [local inspected source](../../../references/comfyui/comfy/sample.py). A generator can produce multiple noise samples under one seed, including indexed samples. Downstream numerical equality still requires a tested runtime/pipeline.
[^3]: [Dreamtime's recorded Comfy setup](../../../references/dreamtime/COMFYUI.md). The [Dreamtime comparison](../../research/DREAMTIME-COMPARISON.md) contains the extraction findings, and [Release Kit dossier](../../research/projects/desktop-release-kit.md) describes the distribution boundary.
