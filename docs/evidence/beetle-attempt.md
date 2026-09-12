# Civitai beetle attempt

Date: 2026-09-12. Real Windows/NVIDIA GPU run through the shared service.
Result: a repeatable generated beetle, **not a match to the source**.

The opt-in `scripts/verify_reproduction.py` fetched
https://civitai.com/images/141984808 with Python HTTP, reused the previously
downloaded exact checkpoint by hash, and submitted two imported attempts.
No browser fetched Civitai data; no reference application was executed.

| Setting | Submitted value |
|---|---|
| Model / version / file | SD XL / 128078 / 92696 (`sdXL_v10VAEFix.safetensors`) |
| Model SHA-256 | `e6bb9ea85bbf7bf6478a7c6d18b71246f22e95d41bcdd80ed40aa212c33cfeff` |
| Prompt and negative prompt | Preserved verbatim from imported metadata |
| Seed | 119907136, unchanged |
| Steps / CFG / dimensions | 32 / 9.5 / 1024 × 1024 |
| Sampler | Source `Euler a` → Comfy `euler_ancestral` |
| CLIP skip | Source 2 → absolute hidden layer -2, both encoders |
| Scheduler | `normal`, disclosed assumption because source omitted it |
| Batch | One image, position zero, no seed offset; disclosed assumption |
| Execution | Pinned Comfy SDXL encoding/noise; source numerical behavior unverified |

Profile: `sdxl-import-attempt-v1`. Comfy revision:
`40c4fcdf513a4523e39d54a9d391908af8df8171`; Python 3.12.11,
Torch `2.14.0+cu130`. Graph, effective settings, model binding and original
recipe were saved with each job. The source manifest was unchanged after both.

Source JPEG: 361,136 bytes, SHA-256
`f63183e136f641ed750d2872eff9b50c37367e2251ccc71f96590b7b24da678b`.
Both output PNGs: 1,599,993 bytes, SHA-256
`7a9559d31cc7d0870ff57596b0590ecb72109963b93f2a3e45064666aff8db75`.
Jobs: `567b5dad-18b9-4922-b895-d8951b9493dd` and
`ec70884b-5ec7-4a56-87b8-fdd2c3c6a46b`.

Decoded RGBA comparison without resizing found different source/output pixels.
Mean absolute RGB channel error was 78.77970631917317 on the 0–255 scale;
this is not a perceptual similarity percentage. Visual inspection found a
similar stained-glass palette and subject, with an upright beetle versus the
source's sideways beetle and different surrounding glass patterns. The two
local outputs have identical decoded pixels and identical file hashes.

The source is a web JPEG, not a verified lossless original. This test establishes
that the imported settings run and repeat locally; it does not identify whether
the source difference comes from scheduler, batch/seed position, encoding, RNG
or other runtime behavior. No seed/scheduler search or exact-match claim was made.

Ignored local artifacts: `artifacts/beetle-attempt/source.jpeg`, `attempt-1.png`,
`attempt-2.png`, `verification.json`, and the service/Comfy logs. Model weights
and local machine paths are excluded from public evidence.

CPU/API tests cover plan revision and acceptance, immutable sources, exact
checkpoint handoff, sampler/CLIP mapping, preserved known scheduler/batch values,
unsupported stages, missing/changed models, reference comparison and output
recovery. Local UI tests cover assumption disclosure and reviewed submission.
GPU execution is separate from these test doubles. Native installed desktop
acceptance and signed delivery remain unverified.

Final checks: 117 backend tests and seven local UI tests passed, frontend build
and source-service smoke passed, and repository/whitespace checks passed.
An updated unsigned folder was assembled at `dist/desktop-attempt-preview`
using the unchanged desktop shell and newly frozen service/UI. Its frozen-service
smoke passed. The already-open older desktop was not replaced or restarted;
native GPU configuration and installed-artifact acceptance are not claimed.
