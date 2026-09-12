# Model acquisition verification

Date: 2026-09-12. Windows local source service and unsigned developer folder.
This verifies acquisition and a new authored GPU image, not source reproduction
or signed installer acceptance. Dreamtime was inspected as source only.

## Live HTTP acquisition

`uv run python scripts/verify_model_download.py --comfy-root runtimes/comfyui-v0.35.0`
used Python HTTP requests to import image 141984808, resolve its exact checkpoint,
download it, pause, stop/restart the owned service, resume, and verify full bytes.
No browser fetched provider data.

| Field | Observed value |
|---|---|
| Source | https://civitai.com/images/141984808 |
| Model / version / file | 101055 / 128078 / 92696 |
| Filename | `sdXL_v10VAEFix.safetensors` |
| Expected and observed SHA-256 | `e6bb9ea85bbf7bf6478a7c6d18b71246f22e95d41bcdd80ed40aa212c33cfeff` |
| Completed bytes | 6,938,078,334 |
| Saved and resumed offset | 76,546,048 |
| Resume response | HTTP 206 |
| Final state | ready; reused after another restart without transfer |
| Source manifest | unchanged |

Anonymous acquisition followed Civitai's observed signed R2 redirect. Signed
URLs were not persisted. The source environment selected Windows WinVault for
credential storage; real gated-file authentication remains untested.

## Engine handoff

The test created a separate authored recipe: an alpine lake and red canoe,
seed 42, 25 steps, CFG 7, Euler/normal, 1024 × 1024, batch one. Comfy loaded the
SHA-named alias of the downloaded VAE-fix checkpoint and produced a PNG.

- Comfy revision: `40c4fcdf513a4523e39d54a9d391908af8df8171`.
- Torch: `2.14.0+cu130`; Python: 3.12.11.
- Output SHA-256: `61845c82dfd0aca35ab1d3565c6e33bd4e71eadd4a1ace98544a53ffaea99042`.
- Output: 1,513,519 bytes; decoded and visually inspected.
- Local ignored evidence: `artifacts/model-download-live/verification.json`
  and `generated.png`. Model weights remain outside Git.

The saved graph and model binding identify the VAE-fix checkpoint. The initial
live report still labels the runtime's default profile; subsequent code separates
supported runtime profiles from the selected job generation profile. CPU tests
cover the explicit model binding and graph. No decoded-pixel comparison with the
beetle was attempted. Its Euler a/clip-skip behavior is unsupported by the current
authored profile, and scheduler/batch evidence is missing.

## Automated and packaged checks

- 100 backend tests passed, including local HTTP range/ETag/416 behavior,
  corruption, restart recovery, deduplication, cache locks, existing-file reuse,
  identity conflicts, reserved space, credential stripping and shutdown ownership.
- Six local Playwright tests passed, including restored download progress.
- Frontend build, Rust ownership test and source-service smoke passed.
- Rebuilt unsigned developer folder; frozen-service process/CLI smoke passed.
- Launched the rebuilt desktop. Its bundled service restored the existing beetle
  import and reported the exact checkpoint available, zero download bytes, and
  the remaining source-generation blockers. Repository and whitespace checks passed.

The final desktop close/reopen automation was rejected by automatic approval
review with only "blocked by policy" as its reason; the app was left open.
Desktop lifecycle acceptance is therefore still pending despite the service
restart/resume tests above.

Live copy fallback, authenticated provider downloads, other operating systems,
hard-crash process reconciliation and installed-artifact acceptance are not
established by these checks. Shared transfer controls affect all consumers;
per-import cancellation/detachment is not yet exposed.
