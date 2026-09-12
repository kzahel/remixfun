# Civitai page metadata import

Date: 2026-09-12. Implementation: shared Python provider in
`backend/remixfun/provider.py`; browser, desktop and CLI use the same service.

## Input evidence

The user supplied findings from independent live probes and requested their
integration into the existing provider. The supplied scratch Node script was
absent at the checked Windows paths, so this implementation was rebuilt from
those findings. No live Civitai request was made for this revision.

The supplied findings identify `__NEXT_DATA__` as the metadata source:
`props.pageProps.trpcState.json.queries`, keyed by `image.get` and
`image.getGenerationData`, with matching `queryKey[1].input.id`. They report
anonymous access with a browser-like User-Agent, null REST metadata, HTTP 200
for missing images, and hidden metadata as a normal partial outcome. They also
report generator-dependent fields and multiple resource stacks. These are
user-supplied observations, not independently reproduced results here.

## Implemented behavior

- Parse the page without executing scripts or depending on a rotating build ID.
- Select exact query keys and image IDs; never take carousel metadata.
- Preserve raw metadata and generation records, including resources, tools,
  process and display keys, with existing credential redaction.
- Normalize explicit resource identity and strength evidence without resolving
  models or guessing generation settings. Keep zero strengths and large seeds.
- Save partial imports for hidden/missing settings or unavailable previews.
- Use optional REST only for a matching image's CDN URL. If unavailable, build
  a preview URL from the selected image UUID and a unique observed CDN prefix.
- Bound response sizes, retries, redirects and host selection. Treat denied,
  unreadable and missing-image responses distinctly.

## Verification

Windows, Python, offline: `uv run pytest -q` passes 60 tests. Provider tests use
`httpx.MockTransport`, synthetic page caches and an owned PNG. The example ID
141984808 identifies the requested query only; fixture prompts, model identities
and preview bytes are invented and do not represent that public image.

Coverage includes decoy carousel queries, mismatched IDs, duplicate queries,
HTTP-200 deleted pages, hidden metadata, arbitrary generator keys, six-resource
stacks, null/failed/unrelated REST results, CDN redirects, bounded retries and
HTML size, 64-bit seed persistence, and recipe retention after preview corruption.

The source service/CLI process smoke also passes, including frontend serving,
API/CLI agreement, library locking and restart. Repository and whitespace checks
pass. No frontend or native-shell behavior changed in this revision.

The earlier [local preview evidence](local-preview.md) describes the previous
build and screenshots. Its frozen desktop payload predates this provider
revision and must be rebuilt to include it. No new live Civitai success, public
SDXL reproduction, GPU result, installer, signing or publication is claimed.
