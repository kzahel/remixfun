# Civitai page metadata import

The acquisition-time generation limits below are historical. The subsequent
[beetle attempt](beetle-attempt.md) runs this imported recipe with disclosed
assumptions and its exact acquired checkpoint; it does not match the source.

## Live import and desktop rebuild, 2026-09-12

The shared Python importer successfully acquired
[image 141984808](https://civitai.com/images/141984808) using direct HTTP requests,
including through the rebuilt desktop's frozen service. No browser tools,
page scripts or reference applications were used for acquisition.

Importer provenance: commit `cf839c9` rebuilt the approach described in the
user's findings about `/tmp/civitai-pw/civitai-metadata.mjs`. That scratch file
remains absent at the checked Windows drive-root and user-temp paths. This is
a reimplementation of its reported approach, not a verified line-by-line port.
The live response confirms that the matching `image.get` and
`image.getGenerationData` page queries supply the recipe. REST image metadata
was null, while its preview URL was usable.

The initial live import recovered metadata but lost the preview: its CDN URL
redirected to `blobs-b2.civitai.com`, outside the old allowlist. Image downloads
now allow that specific HTTPS host, retaining size, timeout, redirect-count and
credential/query restrictions. Page and model requests keep their own host
boundary. The source JPEG then downloaded successfully.

The source repeats one checkpoint in two metadata locations. Complementary
references now form one dependency with both provenance locations; conflicts
remain separate. Optional bounded model-version lookups retain file candidates,
sizes and provider hashes. They do not select the source file, download weights,
or mark local bytes verified. The desktop shows the version and concrete
reproduction blockers; detailed file evidence stays collapsed.

| Source setting | Recovered value |
| --- | --- |
| Subject | Beetle with a stained-glass shell |
| Model | SD XL, model 101055, version 128078, v1.0 VAE fix |
| Seed | 119907136 |
| Steps / CFG | 32 / 9.5 |
| Sampler / clip skip | Euler a / 2 |
| Generation dimensions | 1024 × 1024 |
| Scheduler / batch strategy | Unknown / unknown |
| Provider generation process | On-site txt2img |

The [version endpoint](https://civitai.com/api/v1/model-versions/128078) lists
file 92696, `sdXL_v10VAEFix.safetensors`, approximately 6.94 GB, SHA-256
`e6bb9ea85bbf7bf6478a7c6d18b71246f22e95d41bcdd80ed40aa212c33cfeff`.
This differs from the configured SDXL Base checkpoint hash
`31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b`.

The source JPEG is 1024 × 1024, 361,136 bytes, SHA-256
`f63183e136f641ed750d2872eff9b50c37367e2251ccc71f96590b7b24da678b`.
It was decoded and visually inspected. The CDN's original flag does not prove
that a JPEG is a lossless generator original.

Verification:

- Live source import saved the recipe, one dependency and JPEG without warnings.
- Rebuilt the unsigned developer folder, closed the idle old desktop normally,
  and reopened the new desktop. Its own frozen service imported the live image,
  served matching JPEG bytes, and exported the unchanged manifest. Import ID:
  `b69d5770-a126-4ce6-bb54-ab884ee8a652`.
- The reproduction request returned actionable HTTP 409: missing scheduler,
  differing checkpoint and unsupported source profile. No model ran.
- 79 CPU/backend tests pass, including
  [selected live metadata replay](../../tests/fixtures/civitai-141984808/README.md).
  Replay uses synthetic HTML around captured queries and an owned PNG preview;
  those preview bytes are not the public image. Failed/mismatched version
  lookups, duplicate dependencies and conflicting strengths are covered.
- Frontend build, source and frozen-service process/CLI/restart smokes, Rust
  test, repository and whitespace checks pass.

Repeat against a running desktop: `uv run python scripts/verify_civitai_import.py`.
This imports into its library and saves the source JPEG, manifest and report
under ignored `artifacts/civitai-141984808/desktop/`. The full page stays in local
artifacts; Git contains selected public metadata, omitting unrelated user,
social and gallery information.

Import is verified; GPU reproduction is not implemented or validated. The
desktop starts without a configured GPU runtime. The independently running
authored SDXL service uses different checkpoint bytes and an Euler/normal
profile. A source attempt still needs exact-model acquisition/verification,
source-compatible Euler ancestral and clip-skip conditioning, and explicit
treatment of missing scheduler/batch evidence. No weights were downloaded,
candidate generated, or similarity/pixel-equality claim made. This is service
and developer-folder evidence; native visual acceptance, browser automation,
signed installer and publication were not performed.

## Historical implementation evidence, before the live check

The following records the earlier revision and its verification limits. The
successful live check and rebuild above supersede its unverified-live status.

Date: 2026-09-12. Implementation: shared Python provider in
`backend/remixfun/provider.py`; browser, desktop and CLI use the same service.

### Input evidence

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

### Implemented behavior

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

### Verification

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
