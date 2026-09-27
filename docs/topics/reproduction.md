# Imported SDXL attempts

Status: an initial imported text-to-image attempt profile is implemented.
Image 141984808 was run twice on the local Windows GPU, and image 1760948 was
run twice on Apple Silicon/MPS. Each pair repeated locally but differed from
its public source. See the [beetle evidence](../evidence/beetle-attempt.md)
and [Mac ginger evidence](../evidence/ginger-attempt.md). Exact source reproduction,
batch recovery, remix and animation acceptance remain open.

## Attempt contract

An import is immutable. `GET /api/imports/{id}/dependencies` includes a
`reproduction` plan with its revision, source manifest digest, selected model,
effective recipe, mappings, assumptions and blockers. Model availability and
runtime connectivity determine whether the UI enables **Try reproduction**.

Supported inputs have one resolved, verified SDXL 1.0 SafeTensor checkpoint,
Euler, Euler ancestral or DPM++ 2M SDE sampling, supported named Comfy schedulers, CLIP skip
1–12, and a single text-to-image stage. Seed, prompts, steps, CFG and dimensions
are preserved. Existing size/step/CFG limits still apply. Additional model
dependencies, tools, techniques, unknown extra settings, prompt model references,
explicit multi-image batching and arbitrary graphs are blocked before submission.
The attempt never falls back to the preset Base checkpoint.

Missing scheduler does not prevent an attempt: the UI discloses **normal**.
Missing batch details mean one image at the recorded seed, position zero and
no seed offset. Missing CLIP skip uses the runtime's SDXL penultimate layer.
The API/CLI can explicitly test a bounded seed-offset hypothesis (0–31) when
source batch position is absent. It preserves the recorded seed and saves the
effective seed, offset and incremented-seed strategy with a distinct plan revision.
It rejects overflow and replacement of an explicit source batch position.
This is not shared-seed noise-stream recovery, nor an automatic UI search.
Missing process is disclosed as text-to-image. Required missing prompt, negative
prompt, seed, sampler, size, CFG or steps still prevent a run. Comfy execution
is explicitly an assumption about source text encoding/noise behavior, not a
claim of numerical compatibility with Civitai's generator.

The UI shows these assumptions beside the attempt action. POST
`/api/imports/{id}/reproduce` requires the current plan `revision` and
`accept_assumptions: true` for imported recipes. Stale plans and unaccepted
assumptions return 409 without creating a job. Demo/authored submissions retain
their existing API. The CLI displays the plan without running unless
`reproduce --accept-assumptions` is supplied.
For an offset, GET dependencies with `?seed_offset=N`, then include the same
`seed_offset` in the reproduce request. CLI uses `--seed-offset N`.

## Engine mapping and saved evidence

`sdxl-import-attempt-v1` maps `Euler a` to `euler_ancestral`. Recorded clip skip
N sets the absolute hidden layer to -N through `CLIPSetLastLayer`, for both
positive and negative conditioning. In the pinned Comfy source, setting -2
selects the same layer as SDXL's native penultimate default; it is not an
additional two-layer skip. Reviewed source: `nodes.py`, `comfy/sdxl_clip.py`,
`comfy/sd1_clip.py`, `comfy/sd.py` at revision
`40c4fcdf513a4523e39d54a9d391908af8df8171`.
DPM++ 2M SDE maps to `dpmpp_2m_sde`, the pinned Comfy midpoint solver with CPU
Brownian noise. It does not select the separately named GPU-noise variant.
An explicit Karras scheduler is retained. Source `hashes.model` is accepted
only when it agrees with the selected file. Style Selector `base` with
randomization disabled is handled as a disclosed assumption to use the recorded
prompts without reapplying the extension; other styles remain blocked.

The service binds and verifies the selected model before generation. It saves
the original recipe, effective recipe, plan, mappings, assumptions, exact model
binding, graph, source reference, runtime identity and output with the job.
Single-job admission and uncertain-outcome handling are unchanged. Source
acquisition-time assessments remain historical; the dependency plan is current.

After generation, the service checks reference SHA-256 and compares decoded RGBA
pixels without resizing. It records different dimensions, different pixels or
equal saved-reference pixels, plus mean absolute RGB error where sizes agree.
It also records differing-pixel count, total pixels, maximum channel error and
RGB RMSE. Assessment uses automated pixel metrics rather than manual inspection.
This metric is not a perceptual similarity percentage. A provider JPEG is not
treated as a verified lossless original; even equal reference pixels do not set
`exact_reproduction` true. Missing/damaged reference bytes leave the successful
output saved with comparison unavailable. Damaged existing output artifacts are
replaced atomically with their verified content.

## Use and remaining work

Start the shared service with the documented pinned `--comfy-root`. Browser,
CLI and desktop attached to that service use the same attempt contract. The
default desktop-owned service still starts without a configured GPU runtime.
An attempt is not enabled merely by downloading its checkpoint.

```sh
uv run remixfun --service http://127.0.0.1:8793 models resolve <import-id> --wait
uv run remixfun --service http://127.0.0.1:8793 reproduce <import-id> --accept-assumptions --wait
uv run python scripts/verify_reproduction.py --comfy-root runtimes/comfyui-v0.35.0
```

The verification script uses a separate library/cache lock, reuses existing
checkpoint bytes, imports through HTTP and starts/stops only its owned runtime.
It runs the recipe twice and records source comparison and local repeatability.
Its optional `--seed-offsets N` tests offsets 0 through N-1 (maximum eight), then
repeats zero; `--source-url`, `--expected-sha256` and `--download` select an explicit
new source/model acquisition test. It does not scan schedulers. Next work is establishing
source execution behavior and testing bounded batch/seed recovery under the
[build plan](../tactical/build-remixer.md), without treating a nearest result as exact.
