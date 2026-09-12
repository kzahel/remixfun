# Signed desktop delivery

Status: contract and product configuration scaffolded. Installer builds,
signing credentials, live route registration, and publication are not wired yet.

## Shared foundation

Adopt Desktop Release Kit's [update contract](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/contract/desktop-update-v1.md)
and [channels extension](https://github.com/kzahel/desktop-release-kit/blob/c8d96dd87cb244f96b0123c113b4da17bd698c37/contract/desktop-update-channels-v1.md).
The inspected kit revision is `c8d96dd87cb244f96b0123c113b4da17bd698c37`.
Adapt its workflow, identity checks, signature validation, checksums, and release
finalizer; it is an operational reference, not an exported reusable workflow.

Remixfun owns its branding, service packaging, release identity, updater key,
channel setting, and [product registration](../../update-server/remixfun.json).
Use the existing simple-app-update-server and deployment guidance in the local
dotfiles checkout: `projects/desktop-release-platform/README.md`,
`runbooks/desktop-code-signing.md`, and the Pi update-server runbook. Do not
copy private machine inventory or signing material into this public repo.

## Stable and Nightly

| Track | ID | Tags | GitHub kind | Publication |
| --- | --- | --- | --- | --- |
| Stable (default) | `stable` | `desktop-vM.m.p` | Release | Deliberate release |
| Nightly | `nightly` | `desktop-nightly-vM.m.p` | Prerelease | Scheduled CI on changed, verified main; manual dispatch also supported |

Nightly is this product's channel name. Do not expose the canary's `latest` ID.
The shared protocol permits product-defined channel IDs; configure/discover
`nightly` explicitly. Requests without a channel retain Stable semantics.
The proposed route is `https://updates.graehlarts.com/remixfun`, not yet deployed.

Follow the kit's numeric version ordering: after Stable `M.m.p`, Nightly is
`M.(m+1).S`, with `S = workflow run number * 100 + run attempt`. Enforce native
package bounds and sequence exhaustion before building. A later Stable release
must exceed every shipped Nightly in that train. Never promote by relabeling or
overwriting a published prerelease. Record source SHA separately.

Persist track selection. Switching invalidates old candidates and checks the
chosen track. Returning to Stable never downgrades: wait for Stable to catch up.
Automatic checks do not install or relaunch; installation is an explicit action.
Validate channel discovery and candidate identity; never accept ignored-channel
responses as proof of support. Keep active jobs safe across update/relaunch.

## Signing and CI requirements

Build installers in GitHub Actions from the exact verified source SHA. PR checks
have no signing credentials or publication permission. Signed publication uses
trusted branch/tag events, serialized publication, and immutable draft assets;
only the finalizer publishes after the complete declared target matrix passes.
Never fall back to unsigned publication when a required credential is absent.

- All updater artifacts: Remixfun-specific Tauri signature; embed only its
  public key in the app. Never reuse the canary's private updater key.
- Windows: Authenticode-sign and verify the per-user NSIS installer and shipped
  native executables, including the service sidecar, using Azure Trusted Signing.
- macOS: Developer ID signing and notarization for app, sidecar, and DMG.
- Linux: signed updater payload and checksums; AppImage for self-updates.

Windows x64 is the initial installer target. Add macOS arm64/x64 and Linux
arm64/x64 to the declared release matrix as their packaging is implemented.
Do not advertise unbuilt targets or omit an enabled target from a published
release. OS package-manager distributions retain manual/package-manager updates.

The signing secret names and provisioning procedure are recorded in the
[integration plan](../tactical/signed-desktop-delivery.md). Hosted CI proves
build/signature checks; machine-control campaigns prove installed behavior.
