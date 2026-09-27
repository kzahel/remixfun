# Local SDXL GPU profiles

Windows/NVIDIA source-service profile, verified 2026-09-12. An Apple Silicon/MPS
profile is verified separately in [Mac evidence](../docs/evidence/mac-sdxl-generation.md).
These runtimes are separate from the application environment and from reference
checkouts. They support newly authored SDXL Base 1.0 recipes or an explicitly
selected verified SDXL 1.0 checkpoint, Euler/normal, batch size one, checkpoint
VAE, and no LoRAs or additional conditioning stages. Imported Civitai
recipes are not silently assigned this model or profile.
The separate [imported attempt profile](../docs/topics/reproduction.md) uses an
exact acquired SDXL checkpoint, Euler/Euler ancestral, explicit CLIP layer and
disclosed scheduler/batch assumptions. The [beetle run](../docs/evidence/beetle-attempt.md)
verified generation and local repeatability on Windows, with a source non-match.

## Windows/NVIDIA setup

Install Python 3.12, uv, Git, and a compatible NVIDIA driver. From the repo root:

```sh
git clone --depth 1 --branch v0.35.0 https://github.com/Comfy-Org/ComfyUI.git runtimes/comfyui-v0.35.0
uv venv runtimes/comfyui-v0.35.0/.venv --python 3.12
uv pip install --python runtimes/comfyui-v0.35.0/.venv/Scripts/python.exe torch==2.14.0+cu130 torchvision==0.29.0+cu130 torchaudio==2.11.0+cu130 --index-url https://download.pytorch.org/whl/cu130
uv pip install --python runtimes/comfyui-v0.35.0/.venv/Scripts/python.exe -r runtime-profiles/sdxl-windows.txt
uv pip check --python runtimes/comfyui-v0.35.0/.venv/Scripts/python.exe
uv run python scripts/fetch_sdxl.py runtimes/comfyui-v0.35.0
npm --prefix web run build
uv run remixfun serve --port 8793 --data-dir artifacts/gpu-library --comfy-root runtimes/comfyui-v0.35.0
```

These dependency lists record versions in tested environments, not a
cross-platform lockfile or a signed distribution contract. No environment or
weights enter Git. The model fetch is roughly 6.9 GB and checks size and SHA-256
before promoting a partial download. That bootstrap script does not resume;
the shared service's [model downloader](../docs/topics/models.md) does.

## Apple Silicon/MPS setup

Install Python 3.12, uv, Git and Node 24. The pinned Mac dependencies are in
`sdxl-macos.txt`; they were tested with Comfy revision
`40c4fcdf513a4523e39d54a9d391908af8df8171` and PyTorch 2.12.1 on an M4 Pro.
From the repo root:

```sh
git clone --depth 1 --branch v0.35.0 https://github.com/Comfy-Org/ComfyUI.git runtimes/comfyui-v0.35.0
uv venv runtimes/comfyui-v0.35.0/.venv --python 3.12
uv pip install --python runtimes/comfyui-v0.35.0/.venv/bin/python -r runtime-profiles/sdxl-macos.txt
uv pip check --python runtimes/comfyui-v0.35.0/.venv/bin/python
runtimes/comfyui-v0.35.0/.venv/bin/python -c 'import torch; assert torch.backends.mps.is_available()'
uv run python scripts/fetch_sdxl.py runtimes/comfyui-v0.35.0
npm ci --prefix web
npm --prefix web run build
uv run remixfun serve --port 8793 --data-dir artifacts/mac-gpu-library --comfy-root runtimes/comfyui-v0.35.0
```

In another terminal, use the CLI to create a recipe and generate its image:

```sh
uv run remixfun --service http://127.0.0.1:8793 create "A quiet alpine lake at sunrise" --seed 42 --json
uv run remixfun --service http://127.0.0.1:8793 reproduce <recipe-id> --wait --json
```

The opt-in CLI check exercises generation, downloads the result, and verifies
persistence across service restart:

```sh
uv run python scripts/verify_gpu_cli.py --comfy-root runtimes/comfyui-v0.35.0 --expected-device mps --output artifacts/mac-gpu-cli
```

Stop any other service using the same Comfy root before running it.
This profile establishes new-image generation on Apple Silicon. Imported-source
pixel matching, Mac desktop packaging and installed-app acceptance remain separate.

## Shared behavior and limits

Open `http://127.0.0.1:8793`, enter a prompt under **Create an image on your GPU**,
create the recipe, then choose **Generate image**. Generation settings start
collapsed. The CLI uses the same service:

```sh
uv run remixfun --service http://127.0.0.1:8793 create "A quiet alpine lake at sunrise" --seed 42 --json
uv run remixfun --service http://127.0.0.1:8793 reproduce <recipe-id> --wait --json
node scripts/verify_gpu.mjs
```

For a downloaded checkpoint, select it in the advanced new-recipe controls or
pass `create --model-sha256 <full-sha256>`. The authored recipe saves its explicit
binding. Acquisition alone does not enable imported-source reproduction.

The service checks Comfy commit `40c4fcdf513a4523e39d54a9d391908af8df8171`
before startup and the selected model SHA-256 before generation. It owns the
Comfy child process, selects an available loopback port, and requires CUDA on
Windows/Linux or MPS on macOS. Custom nodes, API nodes, browser launch and
Comfy compiler are disabled. The frozen desktop preview does not
configure this runtime yet; use the source service/browser for this profile.

The engine log is under the selected library's `logs/comfy.log`. Submitted
workflows, runtime identity and outputs belong to saved jobs. Unknown outcomes
block further GPU submissions until inspection and service restart; restarting
marks unfinished jobs interrupted without resubmitting them. Normal service
shutdown stops its owned runtime. After a hard service crash, child-process
reconciliation is still manual. Check for a remaining child before starting
another runtime. The adapter does not attach to a shared external engine.

Sources: [Comfy v0.35.0](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.35.0),
[SDXL Base model card and license](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0).
The checkpoint is pinned to Hugging Face revision
`462165984030d82259a11f4367a4eed129e94a7b`, file
`sd_xl_base_1.0.safetensors`, SHA-256
`31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b`.
