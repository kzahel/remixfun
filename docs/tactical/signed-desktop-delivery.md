# Deliver signed desktop builds

Status: planned; repository CI and product registration file are scaffolded.

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
Record platform-specific evidence and remaining gaps. The first scaffold has
no installer artifact; these checks remain pending until packaging exists.
