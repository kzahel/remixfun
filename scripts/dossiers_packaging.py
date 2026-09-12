from research_tools import dossier


def write():
    dossier('desktop-release-kit', 'Desktop Release Kit — distribution baseline', 'MIT',
        'macOS Apple Silicon/Intel; Windows x64; Linux x64/ARM64',
        'Tauri canary with signed releases, native installers, updater artifacts, and acceptance evidence',
        'Adopt release contracts and validation patterns; not a Python/GPU/model installer',
        [('README.md', 'Canary purpose, architecture, and adoption rules'), ('contract/desktop-update-v1.md', 'Normative updater contract'),
         ('contract/desktop-update-channels-v1.md', 'Stable/Latest channel contract'), ('src-tauri/tauri.conf.json', 'Tauri package configuration'),
         ('src-tauri/src/lib.rs', 'Native lifecycle and updater integration'), ('scripts/prepare-sidecar.mjs', 'Target-specific sidecar staging'),
         ('docs/canary-testbed-runbook.md', 'Installed old-to-new acceptance procedure'),
         ('docs/evidence', 'Existing recorded cross-platform acceptance evidence'), ('LICENSE', 'MIT source license')],
        r'''
## Assessment

This is the appropriate distribution reference because it belongs to the user's existing release infrastructure and already defines the intended multi-platform updater contract. It is a deliberately small canary, not a generic image-generation starter app. Remixfun should adopt its contracts and tested release behavior, while keeping its own product identity and lifecycle.[^s1][^s2]

The clone is taken from the existing local repository at `c8d96dd87cb2`, with a clean original working tree. Public stars and age are recorded for completeness, but they are not meaningful measures of suitability for an internal release contract.

## Architecture and artifacts

The Tauri application contains native updater/lifecycle logic, a webview, bundled resources, and a small nested native sidecar. The sidecar staging script creates target-triple-specific binaries. Matching build identities across app, frontend, and sidecar let an update test prove the whole installed product was replaced.[^s4][^s5][^s6]

The shared update server routes release metadata; immutable artifacts are hosted in GitHub Releases. The server is a separate project. Stable and Latest channels are defined explicitly, including version identities, channel transitions, publication gates, and older-client behavior.[^s1][^s2][^s3]

The release matrix covers five updater targets: Apple Silicon and Intel macOS, Windows x64, and Linux x64/ARM64. NSIS is the Windows in-app update path; AppImage is the Linux path. Additional DMG/MSI/DEB/RPM artifacts are validated as part of the normal release matrix. These are concrete artifact obligations, not evidence that a GPU engine runs on all five targets.[^s1][^s2]

## What it solves for Remixfun

It provides patterns for signing, notarization, updater signatures, release completeness, build identity, channels, relaunch, and installed-version testing. This is much more valuable than copying a blank Tauri window and adding an updater later.[^s2][^s3][^s7]

It does **not** install Python, choose Torch wheels, resolve CUDA/ROCm/MPS compatibility, manage custom nodes, validate workflow dependencies, or cache model weights. Remixfun needs a separate runtime installer and content ledger. A tiny native canary sidecar is not evidence that a large Python environment can be bundled identically.[^s6]

App updates, engine-profile updates, and model downloads should have separate version/rollback rules. Otherwise an ordinary UI update can invalidate a reproducible experiment or cause multi-gigabyte redownloads.

## Adoption boundaries

Remixfun needs its own application identifier, updater key, update-server product route, release naming/configuration, and installed old-to-new acceptance run. The canary's existing identity and signing material must not be reused. This follows the repository's explicit adoption contract and is a concrete implementation requirement for future release work.[^s1][^s2]

The recorded acceptance campaigns are useful evidence that the kit was exercised, but this survey did not repeat those runs. Distinguish source/runbook evidence from a new validation of Remixfun, which currently has no runtime or release artifacts.[^s7][^s8]

## Comparison with Dreamtime

Dreamtime provides the application and inference integration but lacks a desktop release lifecycle. The kit provides the release lifecycle but none of the generation domain. They are complementary. Initial Windows-only shipment can be sensible, provided any adaptation of the kit's five-target publication gate is explicit and tested rather than silently removing missing-target checks.

The source is MIT. Future release validation should include paths with spaces/non-ASCII text, interrupted updates, running engine jobs, library preservation, and engine rollback compatibility, extending the existing installed-update tests with Remixfun-specific behavior.[^s9]
''')

    dossier('comfy-desktop', 'Comfy Desktop', 'Dual AGPL-3.0-or-later OR commercial license',
        'Windows, macOS Apple Silicon, and documented Linux AppImage/.deb support',
        'Electron desktop manager; external installer delivery; source release feed can lack binary attachments',
        'Primary benchmark for managed Comfy installation, instances, snapshots, and recovery',
        [('README.md', 'Desktop setup, instances, supported packaging'), ('package.json', 'Electron/Vue/TypeScript build'),
         ('src/main', 'Runtime management, installation, and native operations'), ('src/preload', 'Native/renderer bridge'),
         ('src/renderer', 'Vue desktop UI'), ('src/types/ipc.ts', 'Typed process boundary'), ('LICENSE', 'Explicit dual license'),
         ('https://docs.comfy.org/installation/system_requirements', 'Current official Linux/Mac/Windows distribution guidance')],
        r'''
## Assessment

Comfy Desktop already tackles the environment-management work often underestimated in a new wrapper: installing and managing Comfy instances, Python/Git-related resources, runtime environments, model locations, updates, and recovery. It is a stronger baseline than “Comfy is hard to install” suggests.[^s1][^s3]

This repository's February 2026 creation date is not the birth date of every version of the Comfy desktop product. Repository succession and packaging changes matter when comparing age/popularity to older apps.

## Architecture

The inspected application uses Electron with Vue/TypeScript and Pinia-oriented renderer state. Main-process code owns installation, files, processes, and runtime lifecycle; preload/typed IPC exposes those operations to the renderer. Electron-vite and associated test tooling support the desktop build.[^s2][^s3][^s4][^s5][^s6]

The installer/instance model separates application UI from Comfy environments and data. Bootstrap/runtime resources, instance migration, snapshots, and rollback are first-class concerns in the source. That is the sort of subsystem Remixfun would need in addition to Tauri's window and updater.[^s1][^s3]

Using Tauri instead of Electron changes the shell/toolchain, not the underlying need to manage executable environments. The larger installed footprint will often be Python/Torch, nodes, and weights rather than the webview framework itself.

## Workflow overlap

Desktop makes the existing Comfy frontend available in an ordinary app and manages its execution environment. Combined with App Mode, it can already provide a simple workflow UI. It does not by itself establish a foreign-image recipe recovery and controlled experiment product; that remains the relevant distinction for Remixfun.[^s1][^s5]

A separate Remixfun application gains a focused library and source/baseline/variant workflow. A Comfy extension gains an existing installer, runtime, and graph editor. The cost difference between those approaches should be evaluated before committing to a large custom runtime manager.

## OS and release interpretation

Current dedicated documentation and repository material include Windows, Apple Silicon macOS, and Linux AppImage/.deb. Some older badges/engine README snippets mention only Windows/macOS. The report uses the dedicated current guidance rather than repeating the older limited list.[^s1][^s8]

The captured release feed includes a release candidate and may show no attached installer files because delivery occurs externally. Feed order does not establish the latest stable consumer installer. OS support also does not imply all custom nodes and models work on each platform.

## License, maintenance, and comparison

The actual license explicitly offers **AGPL-3.0-or-later or a separate commercial license**. GitHub's `NOASSERTION` classification is less informative than that text. It is neither simply MIT nor unavailable proprietary-only source.[^s7]

Dreamtime has no equivalent runtime manager but already has the focused generation UI and Comfy adapter. Study Desktop's installation/recovery behavior and typed process boundary; do not copy a large Electron application merely to package a React app in Tauri.

Evaluation should include first install, importing an existing Comfy directory, shared model paths, failed node installation, restoring an instance snapshot, and engine updates while jobs exist. Compare those experiences with the proposed minimal Remixfun runtime manager. No installers were run in this survey.
''')

    dossier('wan2gp-desktop', 'Wan2GP Desktop Tauri launcher', 'No tracked LICENSE file found; reuse permission unresolved',
        'Windows release artifacts verified in snapshot; macOS/Linux delivery not established',
        'Tauri 2 launcher; Windows NSIS/MSI and updater metadata; manages external WanGP runtime',
        'Very close packaging concept, very young implementation, unresolved license',
        [('README.md', 'Launcher purpose and install experience'), ('src-tauri/tauri.conf.json', 'Tauri targets, CSP, and updater endpoint'),
         ('src-tauri/src', 'Rust process/install commands'), ('src/app.js', 'Launcher UI'), ('src', 'Frontend runtime/service controls'),
         ('package.json', 'Frontend/build dependency scope')],
        r'''
## Assessment

This is a directly relevant example of wrapping a complex local video-generation application with Tauri. It demonstrates that the packaging idea already exists. It is also extremely young: created less than ten days before the snapshot, with low double-digit stars and a history dominated by two likely related author names.[^s1]

## Architecture

The shell uses Tauri 2 and Rust native commands, with a lightweight HTML/JavaScript frontend. The configuration points at static frontend assets rather than a large framework build. Rust modules handle installation/runtime operations and subprocess behavior; browser-facing service controls manage the launched WanGP web application.[^s2][^s3][^s4][^s5][^s6]

The launcher handles substantially more than opening a URL: prerequisites, Python/environment setup, GPU-related runtime choices, process start/stop, and updates. The native code includes Windows-specific subprocess handling. This makes it useful for studying the work a Windows-first Remixfun shell will need, while also showing why a Tauri target list alone does not establish Linux/Mac readiness.[^s1][^s3]

## What it changes about the user's workflow

It can reduce the friction of installing and launching WanGP. The generation semantics, metadata, model capabilities, and headless behavior still come from WanGP. The launcher does not establish a new foreign-image replay model, dependency provenance layer, or controlled-remix experiment system.

For Remixfun, that division should remain explicit: desktop onboarding can improve access to an engine, while the application's data model supplies the distinct creative workflow. A branded window around an existing Gradio app is not itself the full product opportunity.

## Distribution and licensing

The captured release assets establish Windows installer/updater delivery. Tauri's configuration uses broad bundle targets and includes cross-platform icon files, but those are not proof of Mac/Linux releases or usable GPU environments. The report therefore classifies those platforms as unestablished for this launcher.[^s2]

No tracked `LICENSE`/license file was found at collection. Public source visibility and Tauri's own license do not determine permission to copy this application. WanGP's custom license is an additional, separate consideration even if launcher-source permission is later clarified. These two licensing questions must not be collapsed.

## Comparison with Dreamtime and release kit

Dreamtime supplies the generator application; this launcher supplies a packaging pattern for another engine. Desktop Release Kit is the stronger fit for the user's established signing/updater infrastructure. The useful lessons here are setup progress, environment diagnostics, process supervision, and recovery—not copying its updater identity or replacing the kit.

Evaluate on a clean Windows account, with install paths containing spaces, missing prerequisites, interrupted downloads, application restart, and an already-running engine. Then compare how it distinguishes a UI update from a runtime update. Such a short source history and successful release attachments are insufficient evidence of long-term recovery reliability.
''')

    dossier('pinokio', 'Pinokio', 'MIT application source; installed scripts/apps have separate terms',
        'Windows/Linux/macOS; shipped x64/ARM64 coverage varies by artifact and installed app',
        'Electron desktop launcher with installer/archive releases and a separate pinokiod backend dependency',
        'Established onboarding alternative; not a recipe-reproduction application',
        [('README.md', 'Launcher/script model and catalog policy'), ('package.json', 'Electron packaging and backend dependency'),
         ('main.js', 'Desktop main process'), ('preload.js', 'Renderer bridge'), ('updater.js', 'Application update lifecycle'),
         ('LICENSE', 'MIT source license')],
        r'''
## Assessment

Pinokio addresses “make this local AI application install and run without manual terminal work.” That overlaps strongly with Remixfun onboarding and competes with the claim that desktop packaging alone is a differentiator. It does not itself implement image recipe recovery or video generation.[^s1]

## Architecture

The inspected repository is an Electron desktop shell with window/navigation/native integration and updater code. A substantial backend is supplied through the separate `pinokiod` package; that companion source was not cloned or deeply audited in this survey. The package manifest explicitly shows this boundary.[^s2][^s3][^s4][^s5]

Application scripts describe install/run/update actions, environments, and local services. The launcher provides a friendly interface around those operations and can expose the resulting web applications. Per-app directories/environments organize dependencies, but that is not the same as a security sandbox: the README explicitly says scripts can execute commands.[^s1]

The practical architectural lesson is to keep the generation app's web service usable independently of the launcher. The difficult part is dependency lifecycle, shell differences, process state, and recovery; a window alone does not solve those.

## Target workflow coverage

Pinokio can deliver other applications that implement image/video workflows. It does not make those applications share a model identity ledger, imported source record, experiment history, or a single coherent source-to-motion journey. End-to-end task coverage must be attributed to the installed app, not to the launcher catalog.

The catalog's verification/review claims are project policy, not an independent guarantee that every script is safe or every engine combination works. This survey did not install or execute catalog scripts.[^s1]

## Distribution, maintenance, and license

The repository has substantial historical attention, continued recent commits, and multi-platform release assets. The current package is versioned separately from the software it launches, illustrating why app updates and engine/runtime updates are different concerns.[^s2][^s5]

The source license is MIT. Each installed script, engine, and model retains its own terms. A permissive launcher license cannot make a commercially restricted engine permissive.[^s6]

## Comparison with Dreamtime and evaluation

Dreamtime has the application domain that Pinokio lacks; Pinokio has a broader installation/catalog product that Dreamtime lacks. Remixfun could eventually be installable through such a launcher while still offering its own Tauri package and CLI/web modes. That is a distribution option, not a required architecture dependency.

Use it as an onboarding benchmark: install a relevant image/video app, restart it, update it, locate its model directory, and recover from a failed environment setup. Compare the clarity and amount of technical knowledge needed. Keep those results separate from whether the installed application can actually recover and remix a Civitai recipe.
''')
