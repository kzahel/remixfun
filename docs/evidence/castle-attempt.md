# Civitai 141866240: quantitative seed-offset trial

Date: 2026-09-12. Real Windows/NVIDIA GPU through the shared service.
Outcome: **none of offsets 0–7 matched the source pixels**. Repeating offset
zero produced identical decoded pixels and the same output file SHA-256.
These conclusions use automated comparisons, not composition inspection.

## Source and exact model

Python HTTP imported https://civitai.com/images/141866240. The downloaded source
is a 1152 × 896 PNG (1,315,436 bytes) with embedded A1111-style `parameters`.
Those parameters agree with the page's prompt, negative prompt, seed, steps,
CFG, sampler, scheduler and dimensions. Neither source supplies batch position
or size. Source SHA-256:
`cb6a7607fbb2d4bcc51fc30e1d490734106896362edf985eb546dfe234b63602`.

The page identifies an externally generated image and records version
`f2.0.1v1.10.1-previous-669-gdfdcbab6`. Source generator behavior beyond the
recorded settings was not assumed proven. The PNG is lossless and retains
generation metadata; independent original-file provenance is still unverified.

Checkpoint: RealBlueJuggernautMix v1.0, model 1171106, version 1317649,
file 1221707, `realbluejuggernautmi_v10.safetensors`, 6,938,042,930 bytes.
Downloaded and verified SHA-256:
`3304b2b91749c1ea2ccba3687e5329133b675e70b41f8aede3a9ca52f6b8b6df`.
The source's short hash `3304b2b917` agrees with the provider file's AutoV2 hash.
This links its A1111 hash-only model reference and Civitai version reference
into one constrained dependency without changing either source entry.

The file used Civitai's HTTPS redirect to `b2.civitai.com`. After verifying this
host, the downloader allowlist was extended; provider credentials remain absent
from storage requests and signed query strings are not retained. The initial
host rejection and explicit retry did not accept any unverified model bytes.

## Fixed settings and candidate identity

- Source seed: 1902445674; tested effective seeds 1902445674–1902445681.
- Prompt/negative prompt: verbatim source text, identical across attempts.
- 30 steps, CFG 7, 1152 × 896; recorded Karras scheduler retained.
- DPM++ 2M SDE mapped to Comfy `dpmpp_2m_sde` (CPU Brownian noise, midpoint solver).
- Missing CLIP skip: explicit SDXL penultimate-layer assumption, layer -2.
- Missing batching: single-image incremented-seed hypothesis, offsets 0–7.
- Style Selector base/nonrandom: disclosed use of recorded prompts without
  reapplying the extension. This is not an assertion of extension equivalence.
- Profile `sdxl-import-attempt-v1`; Comfy revision
  `40c4fcdf513a4523e39d54a9d391908af8df8171`, Torch `2.14.0+cu130`, Python 3.12.11.

Source manifest remained unchanged after all nine jobs. Every job saves its
original recipe, effective seed/settings, assumptions, exact binding and graph.
The ninth job repeats offset zero as a local repeatability check. No scheduler
scan, shared-seed noise-stream reconstruction or automatic claim of exactness
was performed.

## Automated pixel comparison

Decode source/output to RGBA at native dimensions. No resize, alignment,
rotation, cropping or tolerance. Exact equality requires zero differing pixels.
RGB MAE/RMSE use channel values on the 0–255 scale; neither is a perceptual
similarity percentage. Total pixels: 1,032,192.

| Offset | Effective seed | Differing pixels | RGB MAE | RGB RMSE |
|---|---|---:|---:|---:|
| 0 | 1902445674 | 1,032,109 | 54.0413 | 70.6917 |
| 1 | 1902445675 | 1,032,165 | 48.4131 | 66.6584 |
| 2 | 1902445676 | 1,031,846 | 41.8676 | 59.3831 |
| 3 | 1902445677 | 1,032,064 | 51.4581 | 71.2367 |
| 4 | 1902445678 | 1,032,155 | 60.1522 | 77.9927 |
| 5 | 1902445679 | 1,032,126 | 50.3215 | 67.7420 |
| 6 | 1902445680 | 1,032,149 | 53.1926 | 70.9658 |
| 7 | 1902445681 | 1,031,834 | 46.9011 | 63.8724 |

Offset two has the lowest MAE/RMSE in this set, and still fails equality by over
a million pixels. The offset-zero repeat has zero differing pixels, zero MAE,
zero RMSE and zero maximum channel error. Both file hashes are
`4d326666ca7aaf339c0a9b1c30a2797a16f92cee8594f53aaae26312280648e6`.

This rules out a match among these eight candidates on this execution profile.
It does not rule out another batch convention, another offset, or source/runtime
encoding and RNG differences. The [Dreamtime research](dreamtime-batch-research.md)
establishes its own base-seed-plus-index behavior, not this source's convention.

## Re-run and artifacts

```sh
uv run python scripts/verify_reproduction.py --comfy-root runtimes/comfyui-v0.35.0 --source-url https://civitai.com/images/141866240 --expected-sha256 3304b2b91749c1ea2ccba3687e5329133b675e70b41f8aede3a9ca52f6b8b6df --download --seed-offsets 8 --output artifacts/castle-attempt
```

Ignored `artifacts/castle-attempt/` contains source PNG, nine output PNGs,
`verification.json`, `pixel-comparison.json`, source parameters, comparison HTML,
and service logs. The quantitative JSON was computed from the saved image bytes;
the extended counts/RMSE were added after the original jobs completed. Future
jobs record those extended metrics directly. No weights or machine paths enter Git.

127 backend tests passed, including metadata agreement, hash linking and
ambiguity, seed-offset revision checks, immutable source seeds, overflow,
explicit batch protection, B2 credential stripping and numeric pixel metrics.
