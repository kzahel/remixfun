# Easy Diffusion

[Landscape](../LANDSCAPE.md) · [Repository](https://github.com/easydiffusion/easydiffusion) · [Local clone](../../../references/easy-diffusion/) · [Raw snapshot](../evidence/easy-diffusion.json)

> Source and documentation review, captured 2026-09-12. No GPU generation, installer, or end-to-end reproduction tests were run. “Not found” means not established in this review, not proof a feature cannot exist.

## Repository, popularity, age, and maintenance

| Signal | Evidence |
|---|---|
| Snapshot | 2026-09-12T06:58:15.967620+00:00 |
| Repository creation / age | 2022-08-23 / 1,480 days (about 4.05 years) |
| Oldest reachable commit | 2022-08-24T01:58:18+05:30 — can include inherited history |
| Stars / forks / subscribers | 10,462 / 862 / 111 |
| Open issues + PRs | 95 (GitHub combined count) |
| Archived on GitHub | False |
| Inspected branch / HEAD | main / `9cd95259381921c9a8be433cf02c9f5db68ad7a7` |
| HEAD commit | 2026-09-11T13:18:38+05:30 Fix missing ensure_torchruntime.py to startup scripts (#2060) |
| Reachable commits, including merges | 3,868 |
| Historical distinct author names | 58 |
| Last 90 days: nonmerge commits / author names | 21 / 2 |
| Source license assessment | Custom MIT-style license with use-based restrictions; not plain MIT |
| Operating systems / hardware scope | Windows/Linux/macOS; runtime/backend and hardware support vary |
| Distribution model | Windows installer, Linux/Mac archives, Python/FastAPI web app; evolving v4 engine paths |
| Fit for Remixfun | Established simple installation/image workflow reference; not proven full Civitai replay-to-video product |

Stars indicate accumulated attention, not active users. Author-name counts include aliases, bots, and inherited commits; they are not verified people or the current team size. Activity covers the inspected default-branch history, not every branch, companion repository, or private development. See [methodology](../METHODOLOGY.md).

### Contributors visible in this history

| Historical author name | Nonmerge commits | Recent author name | Nonmerge commits in 90 days |
|---|---:|---|---:|
| cmdr2 | 2061 | cmdr2 | 20 |
| JeLuF | 235 | Bryce Villanueva | 1 |
| Marc-Andre Ferland | 191 | — | — |
| patriceac | 138 | — | — |
| caranicas | 132 | — | — |

### Release evidence

The following are the first five available Atom-feed entries, **not a semantic-version ranking**. Dates are feed **updated** timestamps, not independently verified publication dates. Rolling tags, prereleases, and edited older releases can appear here. Download lists exclude automatic source archives.

| Release entry | Feed updated (UTC) | Attached artifacts observed (sample) |
|---|---|---|
| [v3.0.16](https://github.com/easydiffusion/easydiffusion/releases/tag/v3.0.16) | 2026-03-31T11:00:10Z | `Easy-Diffusion-Linux.zip`, `Easy-Diffusion-Mac.zip`, `Easy-Diffusion-Windows.exe` |
| [v3.0.13](https://github.com/easydiffusion/easydiffusion/releases/tag/v3.0.13) | 2025-08-08T11:03:40Z | `Easy-Diffusion-Linux.zip`, `Easy-Diffusion-Mac.zip`, `Easy-Diffusion-Windows.exe` |
| [v3.0 - Maintenance release](https://github.com/easydiffusion/easydiffusion/releases/tag/v3.0.9c) | 2025-03-06T06:49:18Z | `Easy-Diffusion-Linux.zip`, `Easy-Diffusion-Mac.zip`, `Easy-Diffusion-Windows.exe` |
| [v3.0 - Maintenance release](https://github.com/easydiffusion/easydiffusion/releases/tag/v3.0.9) | 2024-09-09T14:33:10Z | `Easy-Diffusion-Linux.zip`, `Easy-Diffusion-Mac.zip`, `Easy-Diffusion-Windows.exe` |
| [v3.0.7: Merge pull request #1702 from easydiffusion/beta](https://github.com/easydiffusion/easydiffusion/releases/tag/v3.0.7) | 2023-12-12T12:40:46Z | No attached artifacts in captured expansion; check external distribution |

## Assessment

Easy Diffusion is a relevant baseline for approachable local installation, a simple browser UI, queued tasks, image variations, and automatic model handling. It should not be written off as an untouched 2022 prototype: the current README/source include an evolving v4 engine path and newer image model families.[^s1][^s2]

## Architecture

The Python FastAPI service exposes generation and configuration endpoints, serves static UI assets, and dispatches work through model/device/task modules. The task manager organizes render threads and temporary task/result state. Source shows sdkit/torchruntime integration and configurable backend choices; setup scripts bootstrap the environment.[^s2][^s3][^s4][^s5]

This differs from Dreamtime's persistent application job model over an external Comfy server. A temporary queue/cache is useful for interactive generation, but durable source/baseline/variant provenance would need its own persistence rather than relying on a render thread's lifetime.

## Target workflow coverage

The app offers text-to-image, image-to-image, inpainting, variations, prompt combinations, custom models, and postprocessing. These satisfy common creative tasks and can make local generation accessible. The review did not establish arbitrary Civitai-image exact dependency recovery or a unified first/last-frame/loop video workflow.[^s1][^s4]

Its “loopback” image feature should not be counted as a temporally coherent video loop; it feeds an image result into another image task. Likewise, a low historical minimum GPU requirement for basic images says little about modern video-model feasibility.

## Distribution, license, and maintenance

Captured releases include a Windows executable installer and Linux/Mac archives. The source has Windows-specific path/runtime setup and cross-platform startup scripts, illustrating practical issues that persist beneath a friendly UI.[^s1][^s5]

The license starts with MIT-like grants but adds use-based restrictions in Section II/Attachment A. GitHub marks it `NOASSERTION`. It should be recorded as a **custom restricted license**, not plain MIT merely because the opening paragraphs look familiar. Downloaded models have additional independent terms.[^s6]

Recent activity is modest but nonzero, largely concentrated around cmdr2. Roughly 10.5k stars measure accumulated attention; the current engine transition and actual release behavior are more useful than assuming old popularity proves current feature completeness.

## Comparison with Dreamtime and evaluation

Easy Diffusion is a good first-install and simple-queue benchmark. Dreamtime is closer to the desired recipe-import and advanced motion primitives, with an application API already separated from inference. Its source is therefore an onboarding reference rather than an obvious replacement engine.

Evaluate a fresh install, switching a supported model, repeated variations, interrupted tasks, and preservation of effective parameters. Test the latest source and the distributed release separately when their engine capabilities differ. Do not credit source-only v4 additions as independently verified stable installer behavior.

## Source map and citations

[^s1]: **Installers, current engine changes, and user features** — [Pinned source](https://github.com/easydiffusion/easydiffusion/blob/9cd95259381921c9a8be433cf02c9f5db68ad7a7/README.md); [local README.md](../../../references/easy-diffusion/README.md).

[^s2]: **FastAPI and backend selection** — [Pinned source](https://github.com/easydiffusion/easydiffusion/blob/9cd95259381921c9a8be433cf02c9f5db68ad7a7/ui/easydiffusion/server.py); [local ui/easydiffusion/server.py](../../../references/easy-diffusion/ui/easydiffusion/server.py).

[^s3]: **Device threads and task cache** — [Pinned source](https://github.com/easydiffusion/easydiffusion/blob/9cd95259381921c9a8be433cf02c9f5db68ad7a7/ui/easydiffusion/task_manager.py); [local ui/easydiffusion/task_manager.py](../../../references/easy-diffusion/ui/easydiffusion/task_manager.py).

[^s4]: **Application/model/task modules** — [Pinned source](https://github.com/easydiffusion/easydiffusion/tree/9cd95259381921c9a8be433cf02c9f5db68ad7a7/ui/easydiffusion); [local ui/easydiffusion](../../../references/easy-diffusion/ui/easydiffusion).

[^s5]: **Cross-platform bootstrap/runtime setup** — [Pinned source](https://github.com/easydiffusion/easydiffusion/tree/9cd95259381921c9a8be433cf02c9f5db68ad7a7/scripts); [local scripts](../../../references/easy-diffusion/scripts).

[^s6]: **Custom use-restricted software license** — [Pinned source](https://github.com/easydiffusion/easydiffusion/blob/9cd95259381921c9a8be433cf02c9f5db68ad7a7/LICENSE); [local LICENSE](../../../references/easy-diffusion/LICENSE).
