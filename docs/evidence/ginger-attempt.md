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

The next investigation is the source's unreported batch position, scheduler,
CLIP layer and generation backend. Test a bounded seed-offset hypothesis only
as an explicitly labeled hypothesis; a different seed or closer-looking image
must not be treated as exact without decoded-pixel equality to a trustworthy
reference.

Ignored raw evidence is under `artifacts/ginger-attempt/`: source and output
PNGs, full verification report, library and service log. No weights, raw logs or
machine-local paths are committed.
