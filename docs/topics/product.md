# Product

Status: local import/library preview implemented; generation remains planned.

## Implemented local preview

Import a public Civitai image URL or upload a PNG/JPEG/WebP (25 MB maximum).
The service saves source bytes, SHA-256, source provenance and raw metadata,
and normalizes common A1111 fields without adding generation defaults. URL
acquisition reads `__NEXT_DATA__` from the image page. It selects `image.get`
and `image.getGenerationData` by exact query key and requested input ID, then
checks the returned image ID. Carousel metadata cannot supply a missing recipe.
An absent matching image record is not-found even on HTTP 200; an unreadable
page is a separate acquisition failure. No login or browser dependency is used.

REST is optional preview-URL enrichment and never supplies recipe metadata.
The full generation record retains arbitrary metadata, resources, tools,
process and display keys, subject to credential redaction. Hidden or missing
generation settings produce a partial import with available resources and base
model evidence. Missing settings remain unknown. Preview download or decoding
failure preserves the recipe with a warning. Access denial supports retry or
original-image upload without assuming an API key is required. Embedded Comfy
graphs are retained, not flattened or executed. Current verification uses
[synthetic provider fixtures](../evidence/civitai-page-import.md).

The library survives restart and exports a JSON source/recipe manifest. Model,
version, file and reported hash evidence remain separate and unresolved; no
models are downloaded or substituted. Unknown source fields stay visible under
collapsed details. Source dimensions are distinct from generation dimensions.
Unsigned 64-bit seeds cross the API as decimal strings without rounding.
Raw evidence also has a JSON-text representation so the browser can display
large source integers without JavaScript number rounding.

An authored landscape demo illustrates the saved recipe and asynchronous result
flow. It reuses the sample SVG, explicitly labels its output as demo, and never
reports generation, similarity or pixel-equality evidence. Real imports reject
reproduction with an actionable 409 response until a tested runtime and exact
model resolution exist. Remixing and animation are not exposed as working actions.

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
