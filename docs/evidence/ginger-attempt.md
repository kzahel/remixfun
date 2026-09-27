# Civitai ginger image attempt on Apple Silicon

Date: 2026-09-27. A real Apple M4 Pro/MPS run through the shared service and
managed ComfyUI. The source was [Civitai image 1760948](https://civitai.com/images/1760948).
This is the simplest currently identified public reproduction target that reuses
the SDXL Base checkpoint already installed on this Mac. No model download was
needed for this trial.

The live page import supplied one checkpoint resource, SD XL version `126601`,
and no LoRA resources. Civitai's version response identified file `91488`,
`sdXL_v10.safetensors`, with SHA-256
`31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b`.
The service verified that hash against the local checkpoint before submission.
The source recipe recorded a prompt, negative prompt, seed `1763772207`, 20
steps, CFG 7, Euler sampling and 1024 × 1024 dimensions. Scheduler, CLIP skip
and batch position were absent. The attempt disclosed its `normal` scheduler,
SDXL penultimate CLIP layer, one image at offset zero, and Comfy execution
assumptions.

Two imported attempts completed using ComfyUI v0.35.0 at revision
`40c4fcdf513a4523e39d54a9d391908af8df8171`, Python 3.12.12,
PyTorch 2.12.1 and MPS. Both output PNGs have SHA-256
`2733652ad4c9eec37bde6cf8073bc9a56a5c894e38b05e8df4c91db09f45cdfa`.
The repeat comparison found zero different decoded RGBA pixels across
1,048,576 pixels. The imported source bytes were unchanged after the jobs.

The saved Civitai preview was a 1024 × 1024 PNG with SHA-256
`d82bfa82a4797efb7c954246836474a4309a9671a9b56706472192ae50dab009`.
Compared without resizing, the attempt differed at 1,048,573 of 1,048,576
pixels. Mean absolute RGB channel error was 55.1124 on a 0–255 scale and RGB
RMSE was 79.7162. These are pixel errors, not perceptual similarity scores.
The provider image is not verified as the lossless original, and this trial
does not establish exact source reproduction.

## Bounded follow-up experiments

The saved PNG has a `parameters` text chunk ending in `Version: v1.5.1`.
Civitai's page data also says `onSite: false` and `process: txt2img`. This is
strong evidence of an uploaded AUTOMATIC1111 image, though the original
generator and its machine settings were not independently verified.
[AUTOMATIC1111 v1.5.1's processing code](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.5.1/modules/processing.py)
increments seeds across a batch but writes each image's effective seed into
its own infotext (lines 624 and 716). Its
[default RNG source](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.5.1/modules/shared.py)
is `GPU` (line 431). [ComfyUI's maintainer explains](https://github.com/Comfy-Org/ComfyUI/discussions/118)
that Comfy's CPU noise and A1111's GPU noise need not produce the same image
from the same integer seed. Neither source proves which RNG setting generated
this particular image.

The existing `verify_reproduction.py` runner tested incremented-seed offsets
0–7 through the shared service, then repeated offset zero. All used the exact
checkpoint and otherwise fixed effective recipe. All differed from the saved
source, and the repeat was pixel-identical to the first offset-zero run.

| Offset | Differing pixels / 1,048,576 | Mean absolute RGB error |
| ---: | ---: | ---: |
| 0 | 1,048,573 | 55.1124 |
| 1 | 1,048,576 | 70.7890 |
| 2 | 1,048,576 | 76.4715 |
| 3 | 1,048,575 | 64.9375 |
| 4 | 1,048,574 | 65.4147 |
| 5 | 1,048,575 | 65.7289 |
| 6 | 1,048,573 | 63.6965 |
| 7 | 1,048,576 | 66.9973 |

Two isolated Comfy graph variants held the recorded seed at offset zero. A
Karras scheduler changed the mean RGB error to 54.4660 and differed at
1,048,573 pixels. Using CLIP layer -1 instead of -2 changed the error to
55.7743 and differed at 1,048,574 pixels. A slightly lower error does not
identify the source setting; neither variant matched. These variants were
experimental graphs, not newly supported imported-attempt options.

Dreamtime checkout `1129dfc` was inspected as source only. It increments
seeds for multiple requested images, as recorded in the
[Dreamtime batch research](dreamtime-batch-research.md), and maps A1111/Civitai
Euler to Comfy Euler with `normal` as the missing-scheduler default. It has no
checked-in exact Civitai pixel-match fixture. Its seed convention alone does
not override this image's per-image A1111-style seed metadata.

This target is useful for checking import, exact model reuse and local
repeatability, but it is a poor exact-match oracle for the current Comfy/MPS
profile. The next source-matching target should ideally include its original
workflow and RNG provenance. A different seed or lower pixel error must not
be labeled exact without decoded-pixel equality to a trustworthy reference.

Ignored raw evidence is under `artifacts/ginger-attempt/`,
`artifacts/ginger-offsets/` and `artifacts/ginger-variants/`: source and output
PNGs, full verification reports, comparison metrics, library and service logs.
No weights, raw logs or machine-local paths are committed.
