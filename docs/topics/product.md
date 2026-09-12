# Product

Status: local import/library, new SDXL generation and initial imported SDXL
attempts implemented. Exact source reproduction, remixing and animation remain planned.

## Implemented local preview

Import a public Civitai image URL or upload a PNG/JPEG/WebP (25 MB maximum).
The service saves source bytes, SHA-256, source provenance and raw metadata,
and normalizes common A1111 fields without adding generation defaults. URL
acquisition reads `__NEXT_DATA__` from the image page. It selects `image.get`
and `image.getGenerationData` by exact query key and requested input ID, then
checks the returned image ID. Carousel metadata cannot supply a missing recipe.
An absent matching image record is not-found even on HTTP 200; an unreadable
page is a separate acquisition failure. No login or browser dependency is used.

REST optionally enriches preview URLs; background operations resolve explicitly referenced model versions;
it never supplies generation settings. Up to 16 distinct version IDs are queried
for file candidates, sizes and provider hashes. Version responses must match the
requested ID. Failed enrichment preserves the recipe with a warning. Model
gallery metadata is never used. Candidate files remain distinct from a verified
source file and local availability. Complementary references to the same version
are combined in the dependency display; conflicting identities or strengths
remain separate and all original evidence is retained.
The full generation record retains arbitrary metadata, resources, tools,
process and display keys, subject to credential redaction. Hidden or missing
generation settings produce a partial import with available resources and base
model evidence. Missing settings remain unknown. Preview download or decoding
failure preserves the recipe with a warning. Access denial supports retry or
original-image upload without assuming an API key is required. Embedded Comfy
graphs are retained, not flattened or executed. Verification includes
[live image 141984808 and offline replay](../evidence/civitai-page-import.md).

The library survives restart and exports a JSON source/recipe manifest. Model,
version, file and reported hash evidence remain separate. The import view can
download selected files and verify their hashes without substituting models
or rewriting source evidence. See [model acquisition](models.md).
Unknown source fields stay visible under
collapsed details. Source dimensions are distinct from generation dimensions.
Unsigned 64-bit seeds cross the API as decimal strings without rounding.
Raw evidence also has a JSON-text representation so the browser can display
large source integers without JavaScript number rounding.

An authored landscape demo illustrates the saved recipe and asynchronous result
flow. It reuses the sample SVG, explicitly labels its output as demo, and never
reports generation, similarity or pixel-equality evidence. Supported imports can
**Try reproduction** after model verification and disclosure of attempt assumptions;
unsupported dependencies/settings return 409 before generation. See the
[attempt contract](reproduction.md). Remixing and animation are not exposed as working actions.
Imports retain an acquisition-time assessment; the dependency API and desktop
show the current reproduction assessment, including model availability:
missing settings, unverified model files, differing checkpoint hashes where
established, and unsupported sampler/conditioning behavior. The source image
141984808 ran through the imported attempt profile with its exact VAE-fix checkpoint.
The result differed from the source and repeated identically locally. Missing
scheduler and batch evidence remain unknown in the source, with explicit
effective assumptions attached to each attempt.

An explicitly configured managed Comfy runtime enables **Create an image on your
GPU**. New recipes default to the verified SDXL Base 1.0 checkpoint, Euler/normal,
checkpoint VAE and one image per job. Defaults apply to these new recipes only;
they never fill missing imported settings. The default UI exposes the prompt;
the seed and preset settings stay collapsed. The API also accepts bounded steps,
guidance and dimensions. Runtime setup remains a documented developer operation.
Advanced settings can explicitly select another verified SDXL 1.0 checkpoint
for a new authored recipe. This does not substitute a model in an imported source.

Real jobs retain the submitted graph, decimal-text graph representation, model
SHA-256, runtime identity and output bytes. The result view and download work
even when the recipe has no source preview. These are newly generated images,
not evidence of matching a Civitai source. See [GPU evidence](../evidence/local-sdxl-generation.md).

## Intended complete experience

Remixfun makes Civitai image reproduction and remixing straightforward. The
normal path is import → reproduce → remix → animate, with advanced controls
collapsed by default and a small set of supported presets.

Import a Civitai URL or image with metadata, preserve its source evidence,
resolve exact model versions and hashes, reuse local files, and download missing
dependencies with progress. Report unavailable resources and missing metadata.
Do not silently replace a checkpoint, LoRA, VAE, or generation setting.

Preserve the imported baseline separately from variants. Recover missing batch
position through bounded candidate searches, distinguishing incremented seeds
from samples drawn from one seeded random stream. Save the evidence and effective
recipe. Pixel equality and visual similarity are separate outcomes.

Remixing changes explicit parameters while retaining parentage and provenance.
Animation begins with a selected image and a curated compatible preset. Offer
end-frame, loop, and extension controls only where the selected workflow supports
them. There is no general node editor or arbitrary custom-node installer in V1.

Windows/NVIDIA is the first generation target. macOS and Linux are intended
desktop platforms; generation support depends on separately validated runtime
profiles. Packaging support alone does not prove a GPU workflow works.

See the [build plan](../tactical/build-remixer.md) for detailed fixtures and scope.
