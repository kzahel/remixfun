# Local SDXL GPU profile

Windows/NVIDIA source-service profile, verified 2026-09-12. This runtime is
separate from the application environment and from reference checkouts. It
supports newly authored SDXL Base 1.0 recipes, Euler/normal, batch size one,
checkpoint VAE, and no LoRAs or additional conditioning stages. Imported Civitai
recipes are not silently assigned this model or profile.

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

The dependency list records the versions in the tested environment, not a
cross-platform lockfile or a signed distribution contract. No environment or
weights enter Git. The model fetch is roughly 6.9 GB and checks size and SHA-256
before promoting a partial download. It does not implement transfer resume yet.

Open `http://127.0.0.1:8793`, enter a prompt under **Create an image on your GPU**,
create the recipe, then choose **Generate image**. Generation settings start
collapsed. The CLI uses the same service:

```sh
uv run remixfun --service http://127.0.0.1:8793 create "A quiet alpine lake at sunrise" --seed 42 --json
uv run remixfun --service http://127.0.0.1:8793 reproduce <recipe-id> --wait --json
node scripts/verify_gpu.mjs
```

The service checks Comfy commit `40c4fcdf513a4523e39d54a9d391908af8df8171`
and model SHA-256 before startup, owns the Comfy child process, selects an
available loopback port and requires CUDA. Custom nodes, API nodes, browser
launch and Comfy compiler are disabled. The frozen desktop preview does not
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
