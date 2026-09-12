# Remixfun agent instructions

Read [DEVELOPMENT.md](DEVELOPMENT.md) before planning or changing this repo.
Read the relevant [topics](docs/topics/README.md) and search existing
[tactical plans](docs/tactical/README.md) before defining new work.

Build the focused Civitai import → reproduce → remix → animate experience.
Keep advanced controls hidden by default. Preserve imported recipes and exact
model identities; never silently substitute a model or claim an approximate
result is an exact reproduction.

Desktop, browser, and CLI share one service. Keep Comfy behind that service.
Use Desktop Release Kit for release contracts and machine-control for installed
artifact verification. Read the release and testing topics before changing
packaging, signing, update channels, or installer acceptance.

Update owning topic contracts when observable behavior changes. Keep planned
behavior distinct from implemented and verified behavior. Follow the commit
conventions in DEVELOPMENT.md, including Topic trailers for related series.

Preserve unrelated edits. Do not execute reference applications as part of
source research. Never commit credentials, private signing keys, model weights,
personal machine inventory, or generated runtime environments.
