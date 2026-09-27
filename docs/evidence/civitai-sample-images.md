# Civitai Sample Images

This file tracks Civitai images worth reusing in reproduction sessions. Source
recipes are preserved; approximate attempts must not be labeled exact unless
decoded pixels compare equal to the saved reference.

## Current samples

| Image ID | URL | Saved artifacts | Reproduction status |
| --- | --- | --- | --- |
| 141984808 | https://civitai.com/images/141984808 | `artifacts/civitai-141984808/`, `artifacts/beetle-attempt/` | Attempted with exact SDXL VAE-fix checkpoint. Local repeats were deterministic, but saved Civitai reference did not pixel-match. |
| 141866240 | https://civitai.com/images/141866240 | `artifacts/civitai-141866240/`, `artifacts/castle-attempt/` | Attempted with exact RealBlueJuggernautMix checkpoint. Seed offsets 0-7 did not pixel-match. |
| 1760948 | https://civitai.com/images/1760948 | `artifacts/ginger-attempt/`, `artifacts/ginger-offsets/`, `artifacts/ginger-variants/` | Simplest current Mac target: one already-installed SDXL Base checkpoint, no LoRAs, Euler, 1024 × 1024. Offsets 0–7 and two setting variants did not match the source; offset zero repeated exactly. A1111-style source metadata makes Comfy/MPS RNG compatibility doubtful. See [ginger attempt](ginger-attempt.md). |
| 117446208 | https://civitai.com/images/117446208 | `artifacts/civitai-samples/117446208/` | Metadata-rich, but blocked before generation: Illustrious/Pony/NoobAI LoRA stack, hash-only resources without exact versions, ADetailer/TI/hash extras, and non-SDXL-1.0 checkpoint profile. |
| 142257543 | https://civitai.com/images/142257543 | `artifacts/civitai-samples/142257543/` | Metadata-rich, but blocked before generation: SDXL checkpoint plus three LoRAs, inline `DPM++ 2M Karras` sampler/scheduler spelling, workflow/ecosystem extras, and prompt model references. |

## 117446208 import notes

Imported on 2026-09-12 using Remixfun's Python HTTP/Civitai page-data importer,
not browser automation. The saved source preview decoded as PNG, 832x1216.

Core recipe fields were present: seed `4228116334`, 35 steps, CFG 5.0,
sampler `DPM++ 2M`, scheduler `Karras`, CLIP skip 2, width 832, height 1216.

Resources include checkpoint `Hassaku XL (Illustrious)` version `1240288`
(`v1.3 - Style A`) and multiple LoRAs. Several metadata resources are only
hash/name references without exact Civitai version IDs. The current Remixfun
attempt profile requires one resolved SDXL 1.0 checkpoint and no additional
model stages, so no pixel reproduction run was submitted.

## 142257543 import notes

Imported on 2026-09-12 using Remixfun's Python HTTP/Civitai page-data importer,
not browser automation. The saved source preview decoded as JPEG, 1216x832.

Core recipe fields were mostly present: seed `188326995`, 40 steps, CFG 6.0,
sampler `DPM++ 2M Karras`, CLIP skip 2, width 1216, height 832. Scheduler was
not a separate field in the imported metadata; it appears embedded in the
sampler string.

Resolved resources include SD XL `v1.0 VAE fix` (`128078`) plus LoRAs
`xl_more_art-full-v1` (`152309`), `Fresh Ideas@Moebius comic book_SDXL`
(`574045`), and `Scary / Dark / Ominous / Horrifying styled Anime for
IllustriousXL` (`1442687`). A local blob check found the SDXL checkpoint hash,
but not the three LoRA hashes. The current Remixfun attempt profile blocks
LoRA conditioning and extra workflow metadata, so no pixel reproduction run was
submitted.
