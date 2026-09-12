# Development

Remixfun has a local import/library application, shared service and CLI, and a
Windows Tauri developer shell. An optional managed Comfy profile generates new
SDXL images on the GPU through the source service. Imported-source reproduction,
signed installers and publication remain planned. Civitai model acquisition
with verified downloads and resume is implemented; see [models](docs/topics/models.md).
See the [local preview evidence](docs/evidence/local-preview.md) and
[GPU evidence](docs/evidence/local-sdxl-generation.md).

## Run the local app

Install Python 3.12+, uv, and Node 24. From the repository root:

```sh
uv sync --locked
npm ci --prefix web
npm --prefix web run build
uv run remixfun serve
```

Open `http://127.0.0.1:8788`. Try **Open demo**, a public Civitai image URL,
or an original PNG with A1111 metadata. Civitai import reads generation metadata
from the image page's embedded data, without login or a browser dependency.
REST enriches preview URLs; background model resolution retrieves exact version
and file candidates, never generation settings. Hidden metadata produces a partial import;
denied requests support retry or original-image upload. See the
[provider evidence](docs/evidence/civitai-page-import.md) for verification limits.
Demo output reuses an
authored illustration and is never classified as reproduced or generated.

The default data directory comes from `platformdirs` (`Remixfun`, no app author).
Override it with `--data-dir "path with spaces"` or `REMIXFUN_DATA_DIR`.
Only one service can open a library. The service binds to loopback; remote
listening is not exposed in this preview. Optional Civitai credentials use the OS store.

For actual GPU generation, follow the [SDXL runtime setup](runtime-profiles/README.md)
and run the source service with `--comfy-root`. The browser then offers new
SDXL recipes and **Generate image**. The source import path does not substitute
SDXL Base for an unresolved imported model. The frozen desktop supports model
acquisition but does not configure the optional GPU runtime.

For frontend hot reload, keep the service running and run `npm --prefix web run
dev` in another terminal. Vite proxies `/api` to the same service.

```sh
uv run remixfun demo --json
uv run remixfun list --json
uv run remixfun import https://civitai.com/images/12345 --json
uv run remixfun import original.png --json
uv run remixfun models resolve <import-id> --wait --json
uv run remixfun models download <import-id> --wait --json
uv run remixfun downloads --json
uv run remixfun reproduce <demo-import-id> --wait --json
```

The import view offers **Download missing models**. Model folders and optional
Civitai credentials are in Settings. Files are verified against provider SHA-256
before availability; downloads can pause/resume across restart. See
[live acquisition](docs/evidence/model-downloads.md). Model availability does not
imply that an imported recipe has a supported reproduction profile.

For the unsigned Windows desktop folder, install Rust with MSVC build tools
and WebView2, then run `uv run python scripts/build_local.py`. Open
`dist/desktop-preview/Remixfun.exe`; keep the entire folder together. This build
needs no signing credentials. It attaches to a compatible independent service
or starts its bundled service, and only stops the service it owns.

For development, after building the frontend and sidecar once, use
`cargo run --manifest-path desktop/Cargo.toml`. See the
[delivery handoff](docs/tactical/signed-desktop-delivery.md) before packaging
installers or publishing. macOS/Linux desktop packaging is not implemented.

## Documentation ownership

- `README.md`: short product and contributor entry point.
- `docs/topics/`: durable product behavior and technical contracts.
- `docs/tactical/`: bounded implementation plans and remaining acceptance work.
- `research/`: dated source research, not current product requirements.
- `topics.md`: registry of commit-series Topic strings.

Use descriptive tactical step names rather than private phase codes. When
retiring a completed tactical, migrate durable decisions into its topic first.
Update contracts for intentional behavior changes, including failure behavior;
tests and commit history are evidence, not substitutes for those contracts.

## Required reading

| Work | Read |
| --- | --- |
| Product UI, import, reproduction, models, video | [Product](docs/topics/product.md) and [build plan](docs/tactical/build-remixer.md) |
| API, CLI, runtime, storage, process ownership, networking | [Architecture](docs/topics/architecture.md) |
| CI, packaging, signing, updater, channels | [Releases](docs/topics/releases.md) and [release integration plan](docs/tactical/signed-desktop-delivery.md) |
| Tests or claims about a supported OS | [Testing](docs/topics/testing.md) |

## Checks

Python 3.12 or newer is sufficient for repository checks; no dependencies or
reference checkouts are needed:

```sh
python -X utf8 scripts/check_repo.py
git diff --check
```

Application checks:

```sh
uv run pytest -q
npm --prefix web run build
uv run python scripts/smoke_service.py
cd web
npx playwright install chromium
npm test
```

The browser suite starts its own service on port 8791 with an ignored test
library. The process smoke uses an isolated temporary library and an available
port. After packaging, also run `uv run python scripts/smoke_service.py
--executable dist/desktop-preview/remixfun-service.exe` and
`cargo test --locked --manifest-path desktop/Cargo.toml`.

GitHub Actions is configured for repository and service/frontend checks on
Windows, macOS, and Linux, browser tests on Linux, and an unsigned Windows
developer folder. Hosted results are pending until pushed and run. These
checks do not establish installed-app, signing, update, or GPU acceptance.

For local research maintenance with the sibling reference clones available:

```sh
python -X utf8 scripts/build_research.py
python -X utf8 scripts/validate_research.py
```

The renderer regenerates dossiers from `scripts/dossiers_*.py`. Main synthesis
documents are edited directly. Consult research/METHODOLOGY.md before refreshing
the frozen evidence. External reference links are optional in ordinary CI.

Introduce component checks with the implementation. Use focused tests for real
contracts and failures, and report which OS, runtime, artifact, and fixture were
actually exercised. A fake engine cannot establish image reproduction.

## Commits

- Aim for a subject of 65 characters or fewer; wrap bodies at 72 columns.
- For nontrivial work, summarize the motivating request, implementation choices,
  validation, and deliberate deferrals. Small self-evident changes need no body.
- Use the same `Topic: <string>` trailer across a related series. Search
  `topics.md` first and register new strings there. Standalone commits need none.
- Do not add assistant co-author trailers or generated-with banners.
- Verify maintainer name/email before pushing. Work on the current branch unless
  the task requires otherwise; preserve unrelated concurrent changes.
- Run appropriate checks before committing and state material test limitations.

These conventions follow Yep Anywhere's documentation and commit practices,
using `docs/topics/` as this repository's durable topic location.
