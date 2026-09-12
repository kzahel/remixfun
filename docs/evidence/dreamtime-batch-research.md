# Dreamtime batch fixture search

Inspected 2026-09-12, source only. Local checkout revision
`1129dfcca23afb59c59de48d97d92abbd31cd439`, main/origin-main, non-shallow,
62 commits reachable from the locally available refs. This is not a claim
about other machines, unpushed branches or private runtime data.

No checked-in SDXL/Civitai image reproduction fixture or pixel-equality assertion
was found in that tree or its reachable image-file history. The only raster
fixtures found were the Flux Kontext character-transfer source and reference
images, documented in [its test README](../../../references/dreamtime/api/tests/flux_kontext/README.md).
They test an edit workflow, not reconstruction of a Civitai source from a seed.
`test_sdxl.py` accepts a prompt/seed and downloads an output; it has no source
image equality assertion. The `test_finds_exact_match` hit in alignment tests
matches words in a transcript, not image pixels. Image 117446208 appears as an
accepted-URL example in the Civitai router, not as a reproduction oracle.

Dreamtime does implement incremented seeds for multiple requested images:
[generator.py](../../../references/dreamtime/api/routers/generator.py) lines
403–410 loop over `request.count` and use `request.seed + i` when count exceeds
one. The edit endpoint has the same pattern around line 1075. This supports the
user's recollection of a batch-base seed convention in Dreamtime's own generation,
but does not establish which convention generated a particular external image.

Searches covered fixture/test/image paths, exact/reproduction/batch/offset terms,
all reachable image-file history, and commit diffs introducing `seed_offset`,
`Batch pos` or `reproduce`. Reference applications and tests were not executed.
The remembered exact-match example may be outside this checkout; it was not
invented or substituted with an unrelated test.
