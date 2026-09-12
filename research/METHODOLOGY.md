# Research methodology and limitations

## Snapshot and scope

Research date: **2026-09-12**. Each repository snapshot records its own exact UTC collection timestamp. The corpus contains **28 repositories**: 26 public comparison/reference projects and two user-owned local baselines, Dreamtime and Desktop Release Kit. Desktop Release Kit also has public repository metadata; Dreamtime's public endpoint was unavailable.

The central question was whether existing software satisfies **import a foreign image/recipe → recover exact dependencies → reproduce a qualified baseline → make controlled changes → animate the chosen image**, with a Windows-first desktop experience and optional CLI/web operation.

Selection covers direct Civitai recipe tools, complete image/video applications, Comfy frontends, runtime/install managers, alternative inference engines, and the user's existing code. See [catalog.json](catalog.json), [PROJECTS.md](PROJECTS.md), and the [repository matrix](REPOSITORY-MATRIX.md).

This is a detailed purposive survey, not an exhaustive census. It does not audit every Comfy custom node, every Forge/Fooocus descendant, every Diffusers pipeline, every commercial/cloud image service, or all companion repositories. Pinokio's `pinokiod`, Invoke's launcher, SD.Next's separate launcher, cloud backends, and Draw Things' private app are described as boundaries rather than silently treated as fully inspected code. No market-share dataset or active-user survey was available.

## Sources and evidence hierarchy

1. **Inspected source at a recorded commit:** manifests, API/client code, metadata parsers, download completion paths, workflow builders, job/persistence logic, and license files.
2. **Official repository documentation and release assets:** intended installation, features, platform support, explicit LTS/archive statements, and distribution channels.
3. **Public GitHub repository API:** dated popularity and metadata snapshot.
4. **Official external documentation:** Comfy platform/App Mode guidance, PyTorch reproducibility, Tauri distribution, and Civitai documentation migration/client context.
5. **Analysis/recommendation:** conclusions drawn from comparing the above; not represented as measured product behavior.

Every dossier contains a source map with commit-pinned public links and local checkout links. Dreamtime uses local evidence because its public URL could not be verified. The machine-readable [source-map.json](source-map.json) lists the inspected files/directories used for citations.

“Code inspected” establishes that an implementation path exists and what it appears to do. It does not prove installer success, backend compatibility, performance, or output fidelity. “Documented” means the project claims a capability. “Not established” means this review did not find sufficient evidence; it is not a categorical statement that a feature is impossible or absent from every extension.

## Acquisition and checkout policy

References live at `D:/code/references/<slug>`. Public repositories were cloned using a single default branch with Git blob filtering; history is not shallow. Local baselines were cloned with `--no-hardlinks` from the existing original directories. The inspected HEAD, branch, history count, oldest reachable commit, and working-tree status are saved.

LFS payloads and submodules were not fetched. Working-tree source necessary for review was obtained, but full historical blobs need not be locally materialized. Source cloning does not install Python packages, Node dependencies, GPU kernels, models, or application runtimes. No reference startup/install scripts were executed, and no cloud generation or paid operations were invoked.

The original Dreamtime and Desktop Release Kit working trees were clean at capture and left unchanged. No branches/worktrees, commits, pushes, external publications, or release operations were performed for this research. `D:/code/remixfun` was initialized as a new local Git repository containing research artifacts.

## Popularity and age definitions

The collector records GitHub stars, forks, subscribers, open issues, creation time, last push metadata, default branch, archived state, and the API's license classification. These are public repository signals, not product users or revenue.

- **Stars:** accumulated attention/bookmarks; not active adoption.
- **Forks:** repository copies; not necessarily maintained descendants or users.
- **Subscribers:** GitHub watchers receiving notifications; not downloads.
- **Open issues count:** GitHub's repository count includes pull requests; not a direct quality score.
- **Repository age:** days from GitHub creation to collection, with an approximate year conversion. It is not necessarily the age of the product, inherited code, or public launch.
- **Oldest reachable commit:** the first entry from reverse Git history traversal, useful for lineage. Commit dates can be rewritten or imported and are not independent proof of project inception.
- **HEAD date:** last commit on the inspected branch. It is not necessarily the latest release date, latest push to any branch, or latest private development.

Counts were collected with unauthenticated public APIs. Dreamtime's public repository API and release feed returned 404; these errors are retained in its evidence JSON. Missing metrics are reported as unavailable, not zero. Other collection errors, if any, remain in their snapshot's `errors` list.

## Contributors and maintenance

Historical and recent contributor signals use `git shortlog -sn --no-merges HEAD`, with a 90-day `--since` filter for recent history. Counts refer to **distinct author names**, subject to Git's normal author/mailmap handling. They are not deduplicated people, GitHub-account counts, employment counts, or a list of current maintainers.

Aliases, bots, automated authors, and inherited history can distort totals. For example, A1111/Forge/SD.Next share lineage; Swarm inherits earlier work; several projects have multiple spellings of apparent core-maintainer names. Each dossier shows the top five historical and recent author names; raw snapshots retain up to twelve per group. Commit shares are not treated as a complete measure of design/review/community work.

The recent activity window covers history reachable from the inspected default branch. It can include merged work and exclude unmerged branches, separate repositories, private work, or other release pipelines. Zero recent commits therefore does not automatically mean abandoned. Explicit statements such as Visionatrix's archive declaration and Fooocus's limited LTS scope are reported separately.

## Releases and operating systems

The collector reads up to five entries from each public GitHub `releases.atom` feed and expands attached asset lists from the release page. Raw evidence includes release titles, links, **updated timestamps**, notes, and download paths.

Feed order is not semantic-version order. Prereleases, rolling tags, and edited older entries can appear before a stable release. The report labels timestamps as feed updates rather than inventing publication dates. Attached-asset samples omit automatic source archives; full captured lists are in JSON.

An empty attached-asset list does not prove there are no installers. Comfy Desktop uses external delivery; Invoke has a separate launcher; registry packages, containers, and script installers are other channels. Conversely, a Tauri/Electron build target or icon file does not prove a shipped and tested installer exists.

The report separates:

1. OS support for the UI/server;
2. actually documented/captured distribution artifacts;
3. inference backend/device support;
4. model/custom-node compatibility;
5. measured performance and reliability, which this survey did not test.

## Licensing method

Root license text and relevant README/package distinctions take precedence over GitHub's automated SPDX label. Nonstandard/custom licenses, absent grants, binary EULAs, and public/private code boundaries are explicitly recorded. A repository being public or depending on MIT-licensed Tauri does not make its own source MIT.

The report distinguishes application source, branded/distributed binaries, bundled dependencies, engines/custom nodes, model weights, and imported/generated content. It does not select a Remixfun license or conclude that a component can be redistributed in every commercial design. The user asked for license research, so material uncertainties are included rather than deferred or hidden.

## External source checks

| Official source | Use | Observation |
|---|---|---|
| [Comfy system requirements](https://docs.comfy.org/installation/system_requirements) | OS/hardware/Desktop guidance | Current Windows/Linux/Apple Silicon support; separate runtime constraints |
| [Comfy App Mode](https://docs.comfy.org/interface/app-mode) | Simplified workflow competitor | Prepared workflow inputs/outputs; cloud share links distinguished |
| [PyTorch reproducibility](https://docs.pytorch.org/docs/2.14/notes/randomness.html) | Determinism limits | Runtime/platform equality is not universally guaranteed |
| [Tauri distribution](https://v2.tauri.app/distribute/) | Shell packaging context | Native platform bundles are distinct from inference-runtime setup |
| [Civitai REST wiki](https://github.com/civitai/civitai/wiki/REST-API-Reference) | API source location | Wiki now redirects readers to developer.civitai.com; destination failed in browser retrieval, so current client source was used for implementation analysis |

External pages were accessed on 2026-09-12. Unlike Git commit links, live documentation may later change. The survey avoids relying on stale search snippets where current source contradicts them, notably Visionatrix's archived status and newly present video/MPS/App Mode features.

## Reproducing and refreshing the research

From the Remixfun project directory:

```powershell
# Re-render reports from frozen evidence and authored analysis; no network.
python -X utf8 scripts/build_research.py

# Validate completeness, local links, citations, and inspected checkout identities.
python -X utf8 scripts/validate_research.py

# Deliberate collection example; overwrites that project's evidence JSON.
python -X utf8 scripts/collect_landscape.py comfyui
```

Preserve/archive the dated evidence before recollecting. The collector **does not update an existing checkout**. If reviewing a newer version, explicitly fetch/select that revision, record the new baseline, and then recollect. Otherwise new GitHub popularity can be paired with an old local HEAD; the timestamps and identities will show this, but it should be intentional.

`scripts/dossiers_*.py` contain the authored per-project analysis. `build_research.py` renders them with frozen metrics, release tables, and source maps; it overwrites `research/projects/*.md`. Main synthesis documents are edited directly. No generation-app dependencies are required to rebuild the research.

## Validation and remaining uncertainty

The validation script checks catalog/dossier/evidence completeness, exact clone HEADs, working-tree cleanliness, source-path existence, local Markdown links, footnote references, and basic text hygiene. Results are saved in [evidence/validation.json](evidence/validation.json).

It does not run reference unit tests, UI tests, installers, model downloads, or GPU generation. The [evaluation plan](EVALUATION-PLAN.md) specifies those next measurements. Until they are performed, claims about end-to-end usability, source-match rates, speed, memory, and platform reliability remain unmeasured.
