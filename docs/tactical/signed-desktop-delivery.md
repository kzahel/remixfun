# Deliver signed desktop builds

Status: unsigned local Windows app/service build exists; signed delivery remains
planned. The CI configuration builds a developer folder without publishing a
release. Local checks are recorded in [preview evidence](../evidence/local-preview.md).

## Handoff to the infrastructure-equipped machine

Application development and unsigned build preparation can run on the current
machine. Do private provisioning, secret uploads, update-server registration and
inventory-backed machine-control campaigns on a machine where the private
dotfiles checkout, publisher credentials and infrastructure access work.
Do not copy that private configuration into Remixfun or assume it is available
on the development machine.

The reviewable starting point is:

- `uv.lock`, `web/package-lock.json`, and `desktop/Cargo.lock` lock the payload.
- `uv run python scripts/build_local.py` builds the Windows developer folder.
  Its `Remixfun.exe`, `remixfun-service.exe`, and `_internal/` must travel together.
- The service owns and serves the bundled web frontend and keeps user data
  outside the app directory. The shell attaches to a compatible service or owns
  its newly launched service. Both report a source identity; CI supplies the
  exact SHA through `REMIXFUN_SOURCE_SHA` at build time.
- `desktop/tauri.conf.json` includes NSIS current-user intent and sidecar/resource
  paths, but bundling is disabled. There is no updater key/plugin configured.
- Ordinary CI contains no signing secrets or release-publication step.
- `update-server/remixfun.json` describes the intended Stable/Nightly product;
  its live route is still unregistered/unverified.

Next work on that machine, in order:

1. Run the locked build and smoke checks on the committed source, then adapt the
   pinned Release Kit contracts. Resolve one numeric version plus source SHA and
   stamp Python, Cargo, Tauri and web identities consistently; `0.1.0` remains the
   local scaffold version. Reject dirty release source and mismatched payloads.
2. Provision dedicated updater/native signing material using the private runbook
   below. Only the public updater key belongs in this repository. Authenticate
   the repository secret upload through the existing publisher mechanism.
3. Enable and verify a per-user Windows NSIS installer. Sign the shell, sidecar,
   shipped native binaries and installer, and validate the bundled Python/web
   resource layout. Add the updater plugin, persisted channel selection and
   active-job update coordination before claiming update support.
4. Adapt the Release Kit version/channel checks and draft/finalize CI pipeline.
   Keep unsigned developer artifacts out of signed publication and update feeds.
5. Register and verify the product on the existing update server using dotfiles.
6. Use machine-control for clean installed launch and old-to-new signed update
   campaigns. Local source/developer-folder screenshots are not installed evidence.

This handoff is ready for packaging work, not a generation-capable product release.
Real Comfy integration, exact model acquisition and SDXL reproduction evidence
remain tracked in the application build plan.

### 1 — Package the shared application service

Build the web frontend and Python service from a locked dependency set, then
bundle them through Tauri. Define the service executable, resources, version and
source-SHA handshake, startup/shutdown ownership, and application-data location.
Use per-user Windows NSIS first; add macOS DMG/App and Linux AppImage.
Keep Comfy profiles and model caches separate from the replaceable app bundle.

### 2 — Provision Remixfun signing

Follow the private dotfiles signing runbook. Generate and retain a dedicated
Remixfun updater key outside Git; install its public half into Tauri config.
Provision the repository's secret store from authorized publisher material:

- `TAURI_SIGNING_PRIVATE_KEY`, `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`
- `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`
- `MACOS_CERTIFICATE_P12_BASE64`, `MACOS_CERTIFICATE_PASSWORD`,
  `MACOS_KEYCHAIN_PASSWORD`
- `ASC_API_KEY_P8_BASE64`, `ASC_API_KEY_ID`, `ASC_API_ISSUER_ID`

Existing GitHub secrets cannot be read back for copying. Keep source material
and passphrases in the existing private provisioning system. Never print them.

### 3 — Build and finalize in CI

Adapt the pinned Desktop Release Kit workflow and validators to Remixfun's
actual sidecar and enabled target matrix. Add a nightly schedule that skips
unchanged source, explicit nightly dispatch, and deliberate Stable tags.
Resolve one numeric identity and exact source SHA before all builds. Verify
updater signatures, native signatures/notarization, checksums and manifest
completeness before the only publication step. Keep failed releases as drafts.
Ordinary PR checks must not publish or access signing secrets.

### 4 — Register Stable and Nightly updates

Validate `update-server/remixfun.json` against the shared server. Use the existing
deployment, symlinking the product-owned JSON into its `products.d` directory
according to the dotfiles runbook. Verify `/remixfun/channels`, explicit stable
and nightly selection, unknown-channel rejection, and channel-less Stable.
Do not claim the proposed URL works until the deployed route is checked.

### 5 — Verify installed artifacts with machine-control

Run the [acceptance campaign](../topics/testing.md) on each supported OS using
exact CI artifacts, including an older-to-newer signed update and both tracks.
Record platform-specific evidence and remaining gaps. The current developer folder
has no signed installer artifact; these checks remain pending until packaging exists.
