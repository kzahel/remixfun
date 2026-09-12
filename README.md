# Remixfun

A simple, opinionated image remixer: **import → reproduce → remix → animate**.

Paste a Civitai image URL, recover its recipe, download the relevant models,
reproduce a baseline, and make it your own. Turn a selected image into video
with a few curated workflows. Advanced controls stay hidden until needed.

Planned as a Tauri desktop app with a shared web frontend and headless service.
Windows/NVIDIA first; macOS and Linux remain intended targets. Signed installers
will be built in CI, with separate **Stable** and **Nightly** update tracks,
using [Desktop Release Kit](https://github.com/kzahel/desktop-release-kit).

**Status:** repository scaffolding and research. No runnable app or installers yet.

## Development

Start with [DEVELOPMENT.md](DEVELOPMENT.md); agents read [AGENTS.md](AGENTS.md).
Python 3.12+ is sufficient for the current repository checks:

```sh
python -X utf8 scripts/check_repo.py
```

- [Product and architecture contracts](docs/topics/README.md)
- [Application build plan](docs/tactical/build-remixer.md)
- [Signed CI and installer plan](docs/tactical/signed-desktop-delivery.md)
- [Landscape research](research/LANDSCAPE.md) and [28 project dossiers](research/PROJECTS.md)

The layout reserves `web/` for React/Vite, `backend/` for the shared Python
service, and `desktop/` for Tauri. `tests/` owns fixtures and acceptance tests.
The Comfy integration starts from Dreamtime and will use a current, tested
runtime. Reproduction claims require real fixtures, not just matching seeds.

Source licensing is not yet selected. Third-party components retain their own
licenses; reference clones and model weights are not included in this repository.
