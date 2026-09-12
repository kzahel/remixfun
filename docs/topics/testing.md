# Testing and evidence

Status: service/domain tests, browser flow tests and process smoke checks exist.
Local Windows evidence is in [local preview](../evidence/local-preview.md).
Hosted CI, installed-artifact acceptance and GPU reproduction remain unverified.

The [Civitai provider evidence](../evidence/civitai-page-import.md) separates
user-supplied live findings from our offline parser, transport and persistence
tests. Synthetic HTML must not be described as a captured public image fixture.

Use pure CPU tests for metadata normalization, exact dependency resolution,
recipe diffs, seed/batch search, and lineage. Replay provider responses and use a
local HTTP fixture server for download resume, corruption, restart, and auth
errors. Exercise API and CLI against the same injected fake engine; test the
normal UI flow with Playwright, including collapsed advanced controls.

Real GPU tests separately establish selected public SDXL image reproduction,
controlled missing-batch recovery, Comfy upgrade compatibility, and video output.
Record exact model hashes, workflow, runtime, source bytes, and comparison method.
Never report fake-engine success as GPU correctness or similarity as equality.

## Installed desktop acceptance

Use [machine-control](https://github.com/kzahel/machine-control) for Windows,
macOS, and Linux installer verification. Discover configured targets via
`bin/machine-control targets` and `bin/machine-control inventory status`.
Read the selected platform guide, acquire an exact-target claim, use native
desktop controls, and release the claim when finished. Machine selectors and
credentials come from the private dotfiles inventory, not this repository.

Each Remixfun campaign owns its fixtures and assertions. Capture:

1. Exact CI run, source SHA, artifact digest, signature, OS and architecture.
2. Fresh install, first launch, service ownership, storage paths with spaces,
   network default/settings, and clean shutdown.
3. Install an exact older signed release; update to a newer signed release
   through the app; verify relaunch and matching app/service build identities.
4. Stable → Nightly, Nightly → newer Nightly, return to Stable without downgrade,
   and later Stable catch-up, preserving selection, installation ID and library.
5. Active-job handling, failed update recovery, and invalid-signature rejection
   using owned fixtures. Verify model cache and imported recipes survive.

Store public, redacted results in `docs/evidence/`; keep raw machine logs and
screenshots with personal data outside Git. A VM without a supported GPU can
prove installer/lifecycle behavior; it cannot prove image/video generation.
