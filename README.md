# Remixfun

A simple, opinionated image remixer: **import → reproduce → remix → animate**.

Paste a Civitai image URL, recover its recipe, download the relevant models,
reproduce a baseline, and make it your own. Turn a selected image into video
with a few curated workflows. Advanced controls stay hidden until needed.

Planned as a Tauri desktop app with a shared web frontend and headless service.
Windows/NVIDIA first; macOS and Linux remain intended targets. Signed installers
will be built in CI, with separate **Stable** and **Nightly** update tracks,
using [Desktop Release Kit](https://github.com/kzahel/desktop-release-kit).

**Status:** runnable local import/library preview, shared service/CLI, and a
Windows desktop developer build. An optional source-service Comfy profile now
generates new SDXL images on GPU. Imported-source reproduction and signed
installers remain planned. The illustrated demo remains separate from GPU output.

## Development

Start with [DEVELOPMENT.md](DEVELOPMENT.md); agents read [AGENTS.md](AGENTS.md).
To run locally (Python 3.12+, uv, Node 24):

```sh
uv sync --locked
npm ci --prefix web
npm --prefix web run build
uv run remixfun serve
```

Open `http://127.0.0.1:8788`. Import an original PNG, paste a Civitai image URL,
or choose **Open demo**. See [development](DEVELOPMENT.md) for CLI commands,
checks, data locations, and the unsigned Windows desktop build.
For real generation, follow the [SDXL runtime setup](runtime-profiles/README.md).

- [Product and architecture contracts](docs/topics/README.md)
- [Application build plan](docs/tactical/build-remixer.md)
- [Signed CI and installer plan](docs/tactical/signed-desktop-delivery.md)
- [Landscape research](research/LANDSCAPE.md) and [28 project dossiers](research/PROJECTS.md)

`web/` contains React/Vite, `backend/` the shared Python service, and `desktop/`
the Tauri shell. `tests/` owns service tests and `web/tests/` browser tests.
Provider design follows the Dreamtime source assessment, with conservative
normalization and separate source evidence. The narrow Comfy adapter has
[local GPU evidence](docs/evidence/local-sdxl-generation.md). Imported-source
reproduction claims still require exact models and suitable public fixtures.

Source licensing is not yet selected. Third-party components retain their own
licenses; reference clones and model weights are not included in this repository.
