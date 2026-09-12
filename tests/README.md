# Tests

`test_app.py` covers source normalization, provider failures, file imports,
exact seed transport, immutable manifests, persistence and job recovery.
`scripts/smoke_service.py` exercises a real service process and CLI with restart
and library-lock checks; it also runs against the frozen service executable.
`web/tests/` exercises the browser flow against the actual service and demo.

Owned fixtures include an authored SVG demo and small generated PNG metadata
fixtures. Neither is evidence of real diffusion generation or Civitai reproduction.
See [testing](../docs/topics/testing.md) for CPU, GPU, and installed-artifact
acceptance. No model weights or personal machine configuration belong in Git.
