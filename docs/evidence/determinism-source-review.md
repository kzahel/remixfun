# Civitai reproduction: source review of RNG and import competitors

Date: 2026-09-28. Source/documentation review plus a model-free Torch probe:
no reference project was installed, imported into Comfy, or run. The existing [Mac CPU-RNG sweep](civitai-cpu-sweep.md)
is the measured Remixfun result; claims made in competitor comments and READMEs
are not independently verified pixel matches.
The [subsequent experiment](euler-ancestral-cpu-stream.md) used the original
images' A1111 v1.5.1 version marker and tested per-step CPU noise in Comfy.

## Local source set and prior research

The earlier [competitor survey](../../research/LANDSCAPE.md) already covered
Unbake and CiviImport, with pinned dossiers. Its clone paths referred to a
Windows `D:/code/references` research checkout. This Mac now has source-only
clones in repository-local, Git-ignored `references/`. They were cloned with
one default branch and blob filtering, without LFS content or submodules.

| Local directory | Upstream and inspected HEAD | Role |
| --- | --- | --- |
| `references/unbake` | [ComfyUI-Unbake](https://github.com/syugoji/ComfyUI-Unbake/tree/0776f99532d2edbb3e1f1400f614816932ee8bf7), `0776f99532d2` | Explicit Civitai image replay claim; provenance, graph, sweep, comparison |
| `references/civiimport` | [CiviImport](https://github.com/Kiriouchine/CiviImport/tree/b2c854bb76f8b84f728a74c277e3f562625aebe2), `b2c854bb76f8` | Imports Civitai URL and builds a Comfy graph |
| `references/comfyui-cli-fork` | [pip-and-uv-installable-ComfyUI](https://github.com/hiddenswitch/pip-and-uv-installable-ComfyUI/tree/1dba1b6b9905443565a37cdf36182cc221921f60), `1dba1b6b9905` | CLI documents “reproduce something I saw on Civitai”; translates foreign metadata to a generic graph |
| `references/civitai-media-metadata` | [Civitai media-metadata](https://github.com/civitai/media-metadata/tree/b6b5d53d8874fe03ea3d0944acc63fe165ad853c), `b6b5d53d8874` | First-party metadata parser and real-image parsing fixtures; no image generator |
| `references/comfyui-noise` | [ComfyUI_Noise](https://github.com/BlenderNeko/ComfyUI_Noise/tree/0c9ec19b16dc72334cb8ce82c3774aed183048e4), `0c9ec19b16dc` | CPU/GPU initial-noise control; no Civitai importer |

The five clone working trees were clean at inspection. The first two were
already in the September 12 survey; the other three add a CLI example, a
first-party parser, and a focused noise reference. These sources are for
reading only. In particular, a downloaded custom node is not a verified or
safe runtime component for Remixfun simply because it is in `references/`.

## What the reproduction claims amount to

Unbake's [README](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/README.md)
claims it can rebuild and run a workflow from a Civitai image. It explicitly
distinguishes a buildability verdict from a trial that actually runs, and says
the latter is not yet on screen. Its
[builder](https://github.com/syugoji/ComfyUI-Unbake/blob/0776f99532d2edbb3e1f1400f614816932ee8bf7/web/core/recipeWorkflowBuilder.js)
inspects an A1111 `RNG` field and conditionally inserts `smZ Settings` for GPU
or NV noise. CPU uses ordinary Comfy behavior. Comments there report some
large improvements in *structural correlation* when GPU noise is selected for
particular examples. They also report cases harmed by adding smZ to an
ancestral sampler, because that changes the per-step noise implementation.
Those are author-reported experiments in source comments; the cloned tree does
not contain the referenced output/metric corpus. They do not establish exact
pixel reproduction of a Civitai image.

CiviImport's [README](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/README.md)
explicitly calls cross-backend reproduction approximate and notes that
ancestral samplers inject noise repeatedly. Its
[graph builder](https://github.com/Kiriouchine/CiviImport/blob/b2c854bb76f8b84f728a74c277e3f562625aebe2/graph_builder.py)
maps metadata to a core `KSampler`; it has no RNG-source switch. Its hires
path can infer a second pass, including a fixed seed and fallback denoise.
A plausible graph is therefore not proof of the original execution path.

The [CLI fork's own guidance](https://github.com/hiddenswitch/pip-and-uv-installable-ComfyUI/blob/1dba1b6b9905443565a37cdf36182cc221921f60/llms.txt)
says an A1111/Forge PNG is translated into a *generic* Comfy graph. Its
[translator](https://github.com/hiddenswitch/pip-and-uv-installable-ComfyUI/blob/1dba1b6b9905443565a37cdf36182cc221921f60/comfy/component_model/foreign_workflow.py)
uses `EmptyLatentImage` and `KSampler` and does not reproduce a foreign RNG
implementation. This is a useful command interface, not pixel-equivalence
evidence. Civitai's [metadata package](https://github.com/civitai/media-metadata/blob/b6b5d53d8874fe03ea3d0944acc63fe165ad853c/README.md)
preserves raw metadata and distinguishes generator formats; its real-image
fixtures verify parsing and round trips, not regeneration. `ComfyUI_Noise`
[generates selected CPU or GPU initial noise](https://github.com/BlenderNeko/ComfyUI_Noise/blob/0c9ec19b16dc72334cb8ce82c3774aed183048e4/nodes.py),
but that alone does not replace noise injected on every ancestral step.

## Specific lead for the Mac failures

All four simple SDXL Base sources in the [Mac sweep](civitai-cpu-sweep.md)
report `RNG: CPU` and `Euler a`. The exact checkpoint was present; four
single-image Comfy/MPS generations were locally repeatable but none matched
the source pixels. This says CPU *initial* noise did not suffice.

The pinned [Comfy `prepare_noise`](../../runtimes/comfyui-v0.35.0/comfy/sample.py)
draws the initial latent noise on CPU. Its
[Euler ancestral sampler](../../runtimes/comfyui-v0.35.0/comfy/k_diffusion/sampling.py)
then uses `default_noise_sampler(x, seed)` for additional draws. That function
creates a generator and `torch.randn` tensor on `x.device`; on this Mac that
is MPS. In contrast, current A1111
[RNG code](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/rng.py)
selects CPU for `RNG: CPU`, maintains a generator per image, and exposes
`ImageRNG.next()`. Its
[sampler adapter](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/sd_samplers_common.py)
replaces k-diffusion's `torch.randn_like` with that `next()` path. Thus the
same seed and a CPU first tensor do **not** imply the same sequence of
ancestral draws. This is a strong source-level explanation for the four Mac
failures, not yet a demonstrated sole cause: the posted images' exact A1111
version, scheduler, batch context, prompt encoding, and precision remain
unknown. A1111's current source is also not a pinned historical source for
those uploads.

This also explains why changing the initial seed by offsets and toggling
SDXL CLIP -2 did not isolate the fault. The seed-offset search tests a
different first tensor; the CLIP check leaves the per-step RNG path intact.
Comfy's own [cross-UI discussion](https://github.com/Comfy-Org/ComfyUI/discussions/118)
records the original CPU/GPU noise incompatibility and reports limited cases
of matching after alignment, with caveats for batch size and prompt weights.
Those reports do not prove this SDXL/MPS case matches.

## Smallest discriminating follow-up

1. Capture, without a model download, the first latent tensor and first two
   ancestral noise tensors for a single seed/shape in the pinned Comfy runtime
   and in an isolated implementation of the A1111 `ImageRNG` logic. Record
   tensor digests, dtype, device, torch version, batch size, and the first
   differing draw. Do not run a cloned reference application.
2. If the initial tensors agree and the later tensors differ, trial a
   source-compatible *per-step CPU noise* sampler in an isolated graph using
   one of the four existing checkpoint-only fixtures. Keep graph, seed,
   scheduler, prompt text, and model bytes fixed. Compare decoded pixels and
   structural metrics against both the source and the current Comfy control.
3. If the first latent differs, inspect batch/subseed/seed-resize semantics
   before full generation. If all noise agrees but output differs, compare
   sigma schedule and text-conditioning tensors before investigating MPS
floating-point execution. One exact, controlled same-backend PNG with an
embedded graph would establish an oracle before a cross-backend claim.

Success means recorded tensor agreement at each tested boundary and ultimately
decoded-pixel equality to a lossless source. Better visual similarity or a
matching layout is useful progress, but it is not an exact reproduction.

### Model-free boundary probe

A separate Torch-only probe on this Mac used the first sweep fixture's seed
`4117696321`, a float32 latent shape of `[1, 4, 128, 128]`, and the same
generator/draw sequence as the source paths above. It did not import or run a
reference application. In Torch 2.12.1 with MPS available, independently
seeded CPU generators gave identical first tensors (SHA-256 prefix
`d86cdc50893750e9`). The next A1111-style CPU draw had digest
`ecf04bc1869749a4`; a fresh Comfy-style MPS sampler draw had digest
`55af56ecb472bdce` and mean absolute tensor difference `1.133166`.
This verifies the candidate RNG divergence in isolation. It does not measure
the uploaded image's original tensors or establish that RNG is the only
reason its pixels differ.
