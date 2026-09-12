# Tests

`test_reproduction.py` covers imported attempt plans, exact checkpoint and graph
binding, source preservation, settings/assumption boundaries, comparison and
damaged artifact recovery. `scripts/verify_reproduction.py` separately runs the
live beetle recipe twice on GPU; see [evidence](../docs/evidence/beetle-attempt.md).
`test_castle.py` replays image 141866240 metadata, checks unique hash-based model
reference linking, DPM++ 2M SDE/Karras mapping, bounded explicit seed offsets,
conflict rejection and credential stripping on Civitai's B2 redirect.

`test_app.py` covers source normalization, file imports,
exact seed transport, immutable manifests, persistence and job recovery.
`test_civitai.py` uses owned synthetic Next.js pages and mock HTTP responses for
exact image/query selection, arbitrary metadata, hidden/deleted cases, optional
REST enrichment, safe CDN redirects, retry limits and corrupt previews. It
makes no live requests; fixture settings are invented, not those of the example
image ID. See [provider evidence](../docs/evidence/civitai-page-import.md).
`test_civitai_live_fixture.py` replays selected live metadata from image
141984808, with owned preview bytes, and checks model-version evidence,
blob redirects, dependency coalescing and actionable reproduction blocking.
`scripts/verify_civitai_import.py` is an opt-in live HTTP test against a running
desktop/shared service; it saves the actual source JPEG and manifest locally.
`test_generation.py` checks graph, exact model hash, generation settings,
submission/poll/download contracts, source immutability, saved outputs and
interrupted/uncertain jobs using an injected engine. These are CPU tests.
`scripts/verify_gpu.mjs` explicitly drives a configured local GPU service through
the browser and saves actual output evidence; it is separate from ordinary CI.
`scripts/smoke_service.py` exercises a real service process and CLI with restart
and library-lock checks; it also runs against the frozen service executable.
`web/tests/` exercises the browser flow against the actual service and demo.

`test_downloads.py` covers exact plans, cache identity, local HTTP resume and
failure responses, durable controls, shared consumers, shutdown and authored
checkpoint handoff. The UI also uses mocked transfer states to test reload.
`scripts/verify_model_download.py` is an opt-in live HTTP acquisition test: it
downloads the 6.94 GB source checkpoint, proves pause/restart/resume and reuse,
and optionally generates a new authored image with `--comfy-root`. See
[download evidence](../docs/evidence/model-downloads.md); it is not a reproduction test.

Owned fixtures include an authored SVG demo and small generated PNG metadata
fixtures. Neither is evidence of real diffusion generation or Civitai reproduction.
See [testing](../docs/topics/testing.md) for CPU, GPU, and installed-artifact
acceptance. No model weights or personal machine configuration belong in Git.
