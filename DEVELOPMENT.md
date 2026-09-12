# Development

Remixfun is in repository bootstrap. Generation, desktop packaging, and signed
publication are planned; there is no runnable application yet.

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

GitHub Actions runs these checks on Windows, macOS, and Linux. These are
repository checks, not application builds or installed-app verification.

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
