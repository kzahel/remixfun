# Local application preview — 2026-09-12

This is Windows developer-build evidence, not installed-artifact or GPU
acceptance. The application version is `0.1.0`; the local artifact identity is
`development`. Signed builds must use the exact committed source SHA instead.

Local Windows x64 developer binaries (unsigned, with their accompanying
`_internal/` directory), built with Python 3.12.11, Node 24.18.0 and Rust 1.96.0:

| File | SHA-256 |
| --- | --- |
| `Remixfun.exe` | `8db433721cfe65636a15b323578070d6bd335a9fde57d5b96d2413b6103b6dcd` |
| `remixfun-service.exe` | `674a57dc5b5d4e59cf3e53ab3e78f04e4a496f3622c642c101ab832c991de734` |

## Implemented and exercised

- React/Vite frontend built with Node 24; FastAPI service with Python 3.12.
- 34 backend tests passed: conservative normalization, 64-bit seed identity,
  provider failures and malformed envelopes, source-file metadata, byte/hash
  preservation, unchanged manifests, artifact boundaries, startup recovery,
  local Origin/Host checks and CLI command routing.
- Five Playwright tests passed in Chromium on Windows: demo recipe/result,
  advanced fields, persisted library, invalid URL, original PNG upload,
  unavailable real generation, mobile overflow and keyboard dialog dismissal.
- Source-process and frozen-executable smoke checks passed: bundled frontend,
  API/CLI, demo job completion, library locking, paths with spaces and restart.
- Rust attachment identity test passed. The release-profile Tauri executable
  and onedir Python service build into an unsigned Windows developer folder.
- The native executable was launched and exposed a Remixfun window; attachment
  to an independently running compatible service was observed through its
  unchanged health identity. A separate launch without that service started the
  bundled executable and reported a desktop-owned instance. Native UI interaction
  is not verified below.
- Browser inspection of workspace, recipe and result showed no console errors.
  Screenshots of the [workspace](local-preview/workspace.png) and
  [recipe](local-preview/recipe.png) are retained here; the demo result screenshot
  is a local artifact under `artifacts/screenshots/`.

## Fixtures and limits

The bundled `hand-drawn-landscape-v1` SVG is authored artwork, paired with a
synthetic recipe. Demo jobs reuse it; no model executes. The PNG fixture is a
small solid-color authored image containing A1111 text metadata and a large
unsigned seed. Provider tests replay owned synthetic responses, not captured
public SDXL reproduction cases. No model weights or personal inventory are
included in Git.

Anonymous Civitai metadata acquisition returned HTTP 403 from this machine.
The provider reports denial and supports an original-file alternative; live
successful provider acquisition and CDN download are not established by the
synthetic tests. The browser extension's file-chooser automation lacked file
URL permission; the separate repository Playwright upload test passed.

The Windows Computer Use helper could not connect. Ordinary native close,
active-job close refusal, focus/single-instance interaction, and installed
lifecycle acceptance remain to be verified with machine-control. Source and
frozen-service process tests are not substitutes for those native checks.

No current Comfy profile, checkpoint acquisition, real SDXL output, pixel
comparison, batch recovery, remix, or video workflow was exercised. No signed
installer, hosted CI run, published release, updater or deployed update-server
route has been verified. macOS/Linux are CI targets for portable service tests;
no local execution evidence is claimed for those platforms.

## Reproduce the checks and continue

See [DEVELOPMENT.md](../../DEVELOPMENT.md) for locked startup, build and test
commands. The [signed-delivery handoff](../tactical/signed-desktop-delivery.md)
identifies the concrete payload and work requiring the infrastructure-equipped
machine. The [application plan](../tactical/build-remixer.md) keeps real
reproduction acceptance separate from this developer-preview milestone.
