# Apple Silicon SDXL generation through the CLI

Date: 2026-09-27. Source service on an Apple M4 Pro Mac with 48 GiB unified
memory, macOS 26.6.2. This verifies new authored SDXL Base image generation
through Remixfun's CLI and managed Comfy process. It does not verify a Mac
desktop package, Civitai model acquisition, or imported-source reproduction.
An imported-source MPS attempt was subsequently run; see the
[ginger evidence](ginger-attempt.md).

## Runtime and model

- ComfyUI v0.35.0, commit `40c4fcdf513a4523e39d54a9d391908af8df8171`.
- Python 3.12.12, PyTorch 2.12.1, MPS primary device. The isolated dependency
  versions are recorded in [sdxl-macos.txt](../../runtime-profiles/sdxl-macos.txt);
  `uv pip check` passed.
- SDXL Base 1.0 checkpoint, 6,938,078,334 bytes, SHA-256
  `31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b`.
  The bootstrap download verified size and hash before promotion, and the
  service checked the hash before generation.
- Authored prompt: “A quiet alpine lake at sunrise with a small red canoe,
  realistic landscape photograph”; seed 42, 25 steps, CFG 7, Euler/normal,
  1024 × 1024, batch one, checkpoint VAE, empty negative prompt.

## Observed CLI runs

The first run used `remixfun serve --comfy-root`, `remixfun create`, and
`remixfun reproduce <id> --wait`. The second used the opt-in
`scripts/verify_gpu_cli.py`, which exercised those CLI commands, downloaded the
result, stopped the GPU service, restarted the source service without Comfy,
and reopened the saved job and output bytes.

| Observation | First job | Second job |
| --- | --- | --- |
| Job ID | `5f2f182f-79f7-4e22-ad70-44a4ad4d7d30` | `7acaa5b8-0b17-47e5-b9d1-356247cda580` |
| Comfy execution | 84.75 s | 91.85 s |
| Result | Completed 1024 × 1024 PNG | Completed 1024 × 1024 PNG; reopened after restart |
| Output SHA-256 | `3e4a468a7806ceda2ceea57ce13520daf699e73ca81a5e41564bc284052f91c2` | Same |

Both outputs are 1,616,650 bytes and decode as PNG. They have identical file
hashes across separate managed Comfy processes. The second CLI submission and
wait took 95.31 s. The output depicts the requested lake and red canoe. This
establishes local repeatability for this authored recipe, not equality to a
public source image or to a CUDA run.

Ignored local artifacts are under `artifacts/mac-sdxl/` and
`artifacts/mac-gpu-cli/`; neither model weights nor raw logs enter Git.

## Checks and limits

- 131 backend tests pass on this Mac with Python 3.12, including hardlinked
  model availability, content-change invalidation, and platform device checks.
- The frontend build and source-service process smoke pass. The smoke covers
  HTTP frontend serving, API/CLI, library locking and restart without a GPU.
- The Mac model cache's previous ctime failure was fixed by rechecking the hash
  and refreshing its fingerprint after hardlink creation. A real Civitai model
  download on Mac was not part of this GPU test.
- The second Comfy shutdown logged a Python `resource_tracker` warning about
  one leaked semaphore. The service and its managed Comfy child exited; this
  warning has not been investigated further.
- Mac desktop packaging, browser UI GPU acceptance, imported SDXL attempts,
  cross-backend pixel equality, remixing and animation remain unverified.
