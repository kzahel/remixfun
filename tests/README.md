# Tests

`test_app.py` covers source normalization, file imports,
exact seed transport, immutable manifests, persistence and job recovery.
`test_civitai.py` uses owned synthetic Next.js pages and mock HTTP responses for
exact image/query selection, arbitrary metadata, hidden/deleted cases, optional
REST enrichment, safe CDN redirects, retry limits and corrupt previews. It
makes no live requests; fixture settings are invented, not those of the example
image ID. See [provider evidence](../docs/evidence/civitai-page-import.md).
`test_generation.py` checks graph, exact model hash, generation settings,
submission/poll/download contracts, source immutability, saved outputs and
interrupted/uncertain jobs using an injected engine. These are CPU tests.
`scripts/verify_gpu.mjs` explicitly drives a configured local GPU service through
the browser and saves actual output evidence; it is separate from ordinary CI.
`scripts/smoke_service.py` exercises a real service process and CLI with restart
and library-lock checks; it also runs against the frozen service executable.
`web/tests/` exercises the browser flow against the actual service and demo.

Owned fixtures include an authored SVG demo and small generated PNG metadata
fixtures. Neither is evidence of real diffusion generation or Civitai reproduction.
See [testing](../docs/topics/testing.md) for CPU, GPU, and installed-artifact
acceptance. No model weights or personal machine configuration belong in Git.
