from research_tools import dossier


def write():
    dossier('viewcomfy', 'ViewComfy', 'AGPL-3.0',
        'Node/browser app on Windows/Linux/macOS; Comfy can be local or remote',
        'Next.js web app, source releases, separately offered hosted service',
        'Prepared Comfy workflow → approachable form; not a foreign recipe resolver',
        [('README.md', 'Local versus hosted scope'), ('package.json', 'Next/React/TypeScript stack'),
         ('app/services/comfyui-service.ts', 'Comfy service adapter'), ('app/api', 'Server API/media routes'),
         ('app/editor', 'Workflow form editor'), ('app', 'Playground/application structure'), ('LICENSE', 'AGPL source license')],
        r'''
## Assessment

ViewComfy is a direct precedent for making a Comfy workflow usable through a conventional web form. It is relevant to preset presentation and sharing, but it begins with an authored workflow rather than a foreign image whose recipe needs to be recovered.[^s1][^s5]

## Architecture

The application uses Next.js, React, TypeScript, form/schema tooling, and browser state. Server routes bridge requests and media to Comfy or the separately offered service. The editor maps exposed controls to a workflow, and the playground lets users run it and view outputs.[^s2][^s3][^s4][^s5][^s6]

This places presentation/configuration above the graph engine, much like the proposed Remixfun preset layer. It introduces a Node application runtime, whereas Dreamtime already has a Python application service and a static Vite frontend. Adopting it wholesale would add or replace an application layer rather than merely skinning Dreamtime.

## Workflow coverage

It is suitable for a prepared image/video workflow with a few inputs and useful outputs. Form generation does not reconstruct the source graph from incomplete Civitai metadata, prove exact model identity, or preserve a controlled baseline with declared changes. Those remain surrounding product functions.[^s1][^s3][^s5]

The hosted offering advertises additional capabilities; they should not automatically be credited to the self-hosted source. Inspect the actual local paths for authentication, history, storage, sharing, and billing rather than treating one marketing feature list as the open-source product contract.[^s1][^s4]

## Distribution, maintenance, and license

The repository ships source releases rather than native desktop installers in the captured feed. A browser frontend can run on all three target operating systems, while the separate Comfy runtime and model nodes determine GPU compatibility. AGPL-3.0 governs the source.[^s2][^s7]

No default-branch commits appear in the captured 90-day window. That is an observation about this open repository, not proof the company, hosted service, or private development has stopped. Historical activity is concentrated among a few authors.

## Comparison with Dreamtime and evaluation

Dreamtime's hand-built generator pages are less generic but already support the user's domain. ViewComfy is useful for understanding declarative workflow-to-control mapping, input validation, and media output rendering. Remixfun can adopt the pattern without becoming a general app-builder product.

Test one Dreamtime image graph and one first/last-frame video graph through ViewComfy. Count configuration effort and note what happens when node IDs, models, or required inputs change. Compare with Comfy's official App Mode before investing in a competing generic workflow form system.
''')

    dossier('sdfx', 'SDFX', 'AGPL-3.0',
        'Web/Electron builds for Windows/Linux/macOS are described; current binary delivery unestablished',
        'Source setup scripts; Vue/Vite web build and Electron build; no release feed captured',
        'Useful declarative workflow/UI architecture; stale default branch makes it a poor primary dependency',
        [('README.md', 'Workflow app concept and maturity'), ('src/package.json', 'Vue/Pinia/Electron stack and build modes'),
         ('src/src/views/OpenGraph', 'Graph/application views'), ('src/src/stores', 'Workflow and model state'),
         ('src/electron/main/index.ts', 'Native shell'), ('setup.py', 'Backend setup'), ('LICENSE', 'AGPL source license')],
        r'''
## Assessment

SDFX is another explicit precedent for turning Comfy workflows into application-like interfaces. It is useful architecture research but a weak default foundation today: the inspected default branch has not changed since May 2025 and no GitHub release entries were captured.[^s1]

## Architecture

The code under `src` uses Vue, Pinia, Vite, and an Electron build path. Separate web/app Vite configurations allow browser and native-shell presentations. Graph/application views and stores manage enriched workflow state. Setup scripts arrange the Comfy backend and bridge integration.[^s2][^s3][^s4][^s5][^s6]

The central idea is a workflow with presentation metadata: controls map to graph widgets and are arranged into UI regions. That is directly relevant to Remixfun presets, but it creates a compatibility layer that must survive graph/node schema changes. A generic mapping engine can become a large project of its own.

## Target workflow coverage

Prepared graph → simplified app → generation is its focus. The review did not establish automatic Civitai-image recipe resolution, a content-verified dependency plan, or controlled baseline lineage. Compatibility claims about Comfy workflows should be checked against current node packs rather than accepted as universal.[^s1][^s3]

The application-creator/editor scope includes work-in-progress language in the project description. Avoid presenting an architectural concept or internal screen as a fully supported end-user feature. Likewise, native build scripts are not evidence of current downloadable signed installers.

## OS, releases, and licensing

Web and Electron builds aim at cross-platform use; actual model inference remains a Comfy responsibility. The old Node/Vue/Electron dependency era and inactive default branch imply upgrade work before using it as a current shipping base. No build or installer compatibility test was run.[^s2][^s5]

The source is AGPL-3.0. Its historical author count is small and concentrated. No evidence was obtained for active users, current downloads, or a supported release cadence.[^s7]

## Comparison with Dreamtime and evaluation

Dreamtime has current task-specific image/video code in a familiar React/Python stack. Replacing it with SDFX would trade that investment for a generic but older frontend. The useful transferable concept is a versioned preset schema containing input controls, graph bindings, model requirements, and output types.

Compare SDFX's mapping approach with ViewComfy and Comfy App Mode using one representative workflow. The outcome should inform how much generic UI metadata Remixfun needs. It should not lead to inheriting an entire dormant application simply because it once pursued a similar interface idea.
''')

    dossier('visionatrix', 'Visionatrix', 'AGPL-3.0-or-later',
        'Windows portable CUDA/CPU; Linux/macOS source paths; Docker/remote workers',
        'Python/Nuxt web app, CLI/service, Docker images, Windows portable archive; archived repository',
        'Closest service/worker/preset architecture reference; archived, so not recommended as maintained foundation',
        [('README.md', 'Archive declaration, features, and install modes'), ('pyproject.toml', 'Python API/database dependencies'),
         ('web/package.json', 'Nuxt/Vue/Pinia frontend'), ('visionatrix/flows.py', 'Versioned workflow installation and management'),
         ('visionatrix/models.py', 'Model installation'), ('visionatrix/models_map.py', 'Graph-to-model catalog mapping'),
         ('visionatrix/tasks_engine.py', 'Task execution'), ('visionatrix/comfyui_wrapper.py', 'Comfy integration'),
         ('visionatrix/__main__.py', 'CLI/service entry points'), ('LICENSE.txt', 'AGPL license')],
        r'''
## Assessment

Visionatrix is particularly close to the proposed service architecture: a simplified Comfy workflow UI, installable/versioned flows, model acquisition, persistent tasks, workers, and CLI/API deployment. It is also explicitly archived. The live repository/API and cloned README supersede search snippets that still describe it as an actively maintained option.[^s1]

## Architecture

Python FastAPI/Pydantic services, SQLAlchemy/database migrations, and a Nuxt/Vue/Pinia frontend sit above Comfy. Flow definitions connect UI inputs to workflow nodes and model catalog requirements. Model mapping/install services prepare resources; the task engine runs work through the Comfy integration.[^s2][^s3][^s4][^s5][^s6][^s7][^s8]

CLI modes and worker/service separation support deployment beyond one desktop process. Database and task abstractions make it a closer comparison to Dreamtime than a thin JavaScript form builder. That breadth also carries authentication, multi-user, scheduling, migration, and installation maintenance costs.[^s2][^s7][^s9]

## Workflow overlap and missing proof

Installing a flow with its required models and then running it through simple controls is highly aligned with Remixfun's video presets. Civitai LoRA integration and send-to-flow concepts connect outputs to subsequent tasks. These features demonstrate that downloadable workflows plus hidden nodes are established ideas.[^s1][^s4][^s6]

A catalog-managed flow is still different from reconstructing an arbitrary foreign image. The review did not establish an exact source-recipe replay and controlled-diff product. Its value for this survey is the flow/model/task architecture and the practical work involved in maintaining it.

## OS, distribution, and maintenance

The project documented Linux/macOS/source setup, Windows portable CUDA/CPU delivery, and Docker/remote service modes. Captured releases include a Windows portable archive. GPU/model parity across those modes was not independently tested.[^s1]

The repository was archived after an explicit capacity statement; the last inspected commit is the archive update. This is firmer evidence than merely observing zero recent commits. Archive status does not make the code unusable, but adopting it means owning compatibility and operational fixes yourself.[^s1]

Source is AGPL-3.0-or-later, with separate Comfy/node/model terms. Historical authorship and stars describe this repository's history, not a current support organization.[^s2][^s10]

## Comparison with Dreamtime and recommendation

Dreamtime already uses similar Python application components but maintains task-specific graph adapters instead of a general flow marketplace. Remixfun can borrow the architectural lesson—version a preset together with its requirements and UI schema—without inheriting Visionatrix's whole multi-user service stack.

Inspect and test model catalog mapping, installation failure recovery, output-to-next-flow transfer, and separation of data from runtime directories. Use these as design references. Do not choose an archived dependency as the quickest route to a new maintained desktop product without explicitly budgeting the ownership it transfers.
''')
