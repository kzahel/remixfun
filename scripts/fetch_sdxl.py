"""Fetch the public SDXL base checkpoint for the explicit local GPU test profile."""
import argparse
import hashlib
from pathlib import Path

import httpx

REVISION = "462165984030d82259a11f4367a4eed129e94a7b"
SHA256 = "31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b"
NAME = "sd_xl_base_1.0.safetensors"
SIZE = 6938078334


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("comfy_root", type=Path)
    args = parser.parse_args()
    target = args.comfy_root.resolve() / "models" / "checkpoints" / NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        with target.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() == SHA256:
                print("Verified existing SDXL base checkpoint.")
                return
        raise SystemExit("Existing checkpoint differs; preserve it and choose another runtime directory.")
    temporary = target.with_suffix(".download")
    digest, total, reported = hashlib.sha256(), 0, 0
    url = f"https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/{REVISION}/{NAME}"
    with httpx.stream("GET", url, follow_redirects=True, timeout=120) as response:
        response.raise_for_status()
        with temporary.open("wb") as stream:
            for chunk in response.iter_bytes(1024 * 1024):
                total += len(chunk)
                if total > SIZE:
                    raise RuntimeError("Checkpoint exceeds the expected size")
                digest.update(chunk)
                stream.write(chunk)
                if total - reported >= 512 * 1024 * 1024:
                    print(f"Downloaded {total / 1024**3:.1f} / {SIZE / 1024**3:.1f} GiB", flush=True)
                    reported = total
    if total != SIZE or digest.hexdigest() != SHA256:
        raise SystemExit("Checkpoint verification failed; partial file was not promoted.")
    temporary.replace(target)
    print(f"Verified SDXL base checkpoint: {SHA256}")


if __name__ == "__main__":
    main()
