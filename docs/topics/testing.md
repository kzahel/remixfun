# Testing and evidence

Status: service/domain tests, browser flow tests and process smoke checks exist.
Local Windows evidence is in [local preview](../evidence/local-preview.md).
Hosted CI, installed-artifact acceptance and exact imported-source GPU reproduction
remain unverified. [Local SDXL generation](../evidence/local-sdxl-generation.md)
records a real GPU output created through the app, separate from mock tests.
The [beetle attempt](../evidence/beetle-attempt.md) records two identical local
imported-recipe outputs that differ from the public source.

The [Civitai provider evidence](../evidence/civitai-page-import.md) separates
historical user-supplied findings, a live HTTP import, and offline parser,
transport and persistence tests. The selected live metadata excerpts are
explicitly distinguished from synthetic HTML and owned preview-image fixtures.

[Model acquisition evidence](../evidence/model-downloads.md) records the exact
checkpoint transfer, restart/resume, reuse and authored GPU generation. CPU tests
exercise local HTTP range responses, corruption, identity conflicts, credentials,
disk reservations and cache recovery; UI tests cover restored transfer progress.

Use pure CPU tests for metadata normalization, exact dependency resolution,
recipe diffs, seed/batch search, and lineage. Replay provider responses and use a
local HTTP fixture server for download resume, corruption, restart, and auth
errors. Exercise API and CLI against the same injected fake engine; test the
normal UI flow with Playwright, including collapsed advanced controls.

Real GPU tests separately establish selected public SDXL image reproduction,
controlled missing-batch recovery, Comfy upgrade compatibility, and video output.
Record exact model hashes, workflow, runtime, source bytes, and comparison method.
Never report fake-engine success as GPU correctness or similarity as equality.
Use automated decoded-pixel equality and image-difference metrics to assess and
rank reproduction trials. Avoid token-consuming manual composition inspection.
Record dimensions, preprocessing (none by default), differing-pixel count and
RGB error metrics. An error score is not a perceptual similarity percentage.
The [castle trial](../evidence/castle-attempt.md) tests eight incremented-seed
candidates against a PNG reference, with a separate exact local repeat check.

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
