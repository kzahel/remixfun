# Euler ancestral CPU-stream experiment on Mac

Date: 2026-09-28. This follows the [source review](determinism-source-review.md)
and [original four-image sweep](civitai-cpu-sweep.md). It is an isolated
Comfy/MPS experiment, not an implemented Remixfun reproduction mode. No
reference application was run and no model was downloaded.

## Historical source and experiment boundary

All four saved source PNGs contain A1111-style `parameters` and report `RNG:
CPU`, `Sampler: Euler a`, `Model hash: 31e35c80fc`, and `Version: v1.5.1`
(one spells the version `1.5.1`). I cloned the upstream
[A1111 v1.5.1 tag](https://github.com/AUTOMATIC1111/stable-diffusion-webui/tree/v1.5.1)
at `68f336bd994bed5442ad95bad6b6ad5564a5409a` into the ignored, sparse
`references/a1111-v1.5.1/` directory for source reading only.

At that tag, [initial noise](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.5.1/modules/devices.py)
seeds Torch and draws on CPU when `RNG: CPU`. The
[Euler ancestral sampler adapter](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.5.1/modules/sd_samplers_kdiffusion.py)
replaces k-diffusion's `torch.randn_like` with CPU draws from the continuing
RNG stream for the single-image, no-ENSD case. By contrast, the pinned
[Comfy sampler](../../runtimes/comfyui-v0.35.0/comfy/k_diffusion/sampling.py)
draws its additional Euler ancestral noise on the sampled tensor's device,
which is MPS here. A Torch-only check with fixture 1785120's seed found that
the initial CPU tensor hashes agree (`d86cdc50893750e9`), and a minimal
v1.5.1-style global CPU draw agrees with the experiment's local CPU-stream
draw (`ecf04bc1869749a4`). This checks the *current Torch* stream logic;
it does not prove the posted image's original Torch version or batch state.

The [v1.5.1 infotext writer](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.5.1/modules/processing.py)
omits the negative-prompt line when it is empty and writes `Schedule type`
when its nondefault scheduler is selected. For these particular v1.5.1
records, missing negative-prompt text is evidence of an empty prompt, and
missing schedule override supports the automatic Euler a schedule. The
reference bytes still come from Civitai; their original upload lineage is
not independently established.

## Controlled generations

I used the exact saved Comfy graph for image 1785120, the verified SDXL Base
checkpoint, the pinned Comfy revision `40c4fcdf513a4523e39d54a9d391908af8df8171`,
Torch 2.12.1, and Apple M4 Pro/MPS. An ignored launcher patched only
`default_noise_sampler` in memory for the CPU-stream variant. It consumed
the first `[1,4,128,128]` CPU noise tensor, then produced subsequent float32
draws from that same CPU generator and transferred them to MPS. The control
run reproduced the previously saved output **byte for byte** (SHA-256
`a1817a29ba3a580039adb14f904451bc271fdfedd20a4c5e08548ad511d7ec5b`).
That validates the comparison harness before interpreting the variant.

The same CPU-stream patch was then tested on two more saved SDXL Base graphs.
Every number below compares decoded RGB to the saved 1024 × 1024 Civitai PNG,
without resize or alignment. Lower MAE is closer; neither MAE nor correlation
is a proof of pixel equality.

| Source image | Earlier MPS ancestral MAE | CPU-stream MAE | Luminance correlation, earlier → CPU | Pixels within 5 in every RGB channel, earlier → CPU |
| --- | ---: | ---: | ---: | ---: |
| [1785120](https://civitai.com/images/1785120) | 43.2431 | **3.0322** | 0.3939 → **0.9895** | 2.31% → **82.66%** |
| [2027882](https://civitai.com/images/2027882) | 39.8354 | **10.3866** | 0.4830 → **0.9335** | 1.46% → **28.84%** |
| [2124513](https://civitai.com/images/2124513) | 38.7538 | **8.4644** | 0.4704 → **0.9743** | 1.30% → **35.71%** |

All three CPU variants still have differing pixels, so **none is an exact
reproduction**. The repeated, large improvement supports per-step RNG as a
major cause of the previous failure. It does not establish which remaining
component accounts for each difference.

## Narrow follow-up controls

- On 2027882, changing `CLIPSetLastLayer` from `-2` to `-1` while retaining
  CPU-stream noise raised source MAE from **10.3866** to **20.6589**. This
  rules out that specific change as a fix for this fixture; it does not fully
  establish A1111/Comfy conditioning equivalence.
- The v1.5.1 A1111 default VAE dtype is fp16, with an
  [automatic fp32 retry](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.5.1/modules/processing.py)
  on VAE NaNs. Comfy/MPS defaulted to bf16 in our control. For 1785120,
  forcing Comfy fp16 VAE produced an all-black image. Forcing fp32 VAE with
  CPU-stream noise produced MAE **2.9718**, a slight improvement over bf16
  **3.0322**, but still no pixel match.
- For the fp32 VAE output, a spatial shift of one pixel in either horizontal
  direction increased MAE from **2.9718** to more than **5.09**. Simple
  per-channel affine brightness correction also failed to reduce MAE.
  A trivial crop displacement or global color scaling does not explain the
  remaining error.

Ignored raw graphs, logs, images, and JSON metrics are in
`artifacts/civitai-rng-followup/`. The Comfy checkout and reference clones
were left clean. This experiment did not change Remixfun's product graph or
its exact-reproduction claims.

## Next discriminating avenues

1. Capture Comfy and v1.5.1-derived sigma arrays, conditioning tensors, and
   sampled latents at the first, middle, and final steps for one fully
   specified fixture (1785120). This locates the remaining divergence before
   VAE and PNG processing. Preserve the source's batch, subseed, ENSD and
   version evidence; do not silently assume missing values.
2. Separate MPS numerical effects from mapping differences with a controlled,
   same-runtime PNG containing an embedded graph and original lossless pixels.
   Confirm an exact same-runtime replay first. A platform/backend comparison
   can then measure the expected numerical gap without Civitai metadata
   ambiguity.
3. Validate a source-compatible ancestral CPU-stream implementation behind an
   explicit experimental profile, with tensor-level tests and the three saved
   fixtures. Keep provenance and the selected noise mode in every attempt.
   Do not enable it merely because a recipe reports `RNG: CPU`: the
   generator/version and sampler path must support the mapping.
4. Check original-image provenance and any Civitai transcode or postprocess.
   PNG encoding alone says the saved reference is lossless *now*, not that it
   preserves the original generator pixels. A genuine uploaded original is
   needed for a final exact-equality claim.
5. After the single-image pipeline is aligned, revisit recorded seed versus
   batch position and A1111's v1.5.1 per-image noise handling. A batch-offset
   sweep before that alignment can misdiagnose an RNG mismatch as a seed issue.
