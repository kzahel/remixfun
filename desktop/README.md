# Desktop shell

Tauri Windows developer shell and bundled Python service. Build the unsigned
folder using `uv run python scripts/build_local.py` from the repository root.
Open `dist/desktop-preview/Remixfun.exe`, keeping its sibling service executable
and `_internal` resources together. Data lives outside the replaceable app folder.

The shell attaches to an identity-compatible service or starts its own, refuses
ordinary close during an owned demo job, and leaves independent services running.
There are no privileged web commands or updater capabilities.

Signed installers, updates and publication remain in the
[delivery handoff](../docs/tactical/signed-desktop-delivery.md). This developer
folder is not installed-artifact evidence.
