# Product

Status: accepted direction; application implementation pending.

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
