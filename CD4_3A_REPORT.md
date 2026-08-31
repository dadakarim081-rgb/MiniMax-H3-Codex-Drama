# CD4.3A — CPU-only 10Eros beta4 checkpoint staging

Date: 2026-08-31

## Decision

**A — 10EROS CHECKPOINT STAGED AND VERIFIED**

## Run record

- Ponytail: full mode.
- Repository: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`.
- Branch: `codex/cd1-1-storyboard-original`.
- Starting commit: `6819a6a` (`docs: record CD4.2 repair gate`).
- Modal app: `minimax-h3-codex-drama-cd4-3a-stage-cpu` (`ap-55nEaMUzM3NXzyGvyEXUuR`).
- Modal function: `stage_checkpoint`.
- GPU requested: **no**; the function had no GPU allocation configured.

## Checkpoint

- Exact target path: `/cache/comfy-models/diffusion_models/10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors`.
- Source repository: `TenStrip/10Eros-Max`.
- Immutable source revision: `3c071106f5b62c02b3cb0b7d831083cdb582b289`.
- Resulting size: `20,967,637,320` bytes.
- Verified SHA-256: `54d56b15c65923b54c9ca16b494dae641bfe9455cfcb1c19c49b1008e270bbc1`.

## Inspection and transfer

The in-function pre-download inspection found no canonical target file and no target-specific `.partial`, `.incomplete`, or downloader artifact. The previously aborted bytes were **not reusable**; the inspection was empty and no unrelated cached model was touched.

- Downloader: `huggingface_hub.hf_hub_download`.
- `huggingface_hub`: `1.29.0`.
- `hf-xet`: installed (`1.6.0`) and enabled; the run reported Xet active and `HF_HUB_DISABLE_XET` unset.
- Model download operations attempted: **1**.
- Transfer duration: `169.959723454` seconds.
- Average effective rate: `0.1148956563` GiB/s.

The model was staged under a target-specific temporary directory and promoted to the canonical filename only after exact size and SHA-256 verification. No BF16 model or other model was downloaded.

## Persistence and scope checks

- Modal Volume: `minimax-h3-microdrama-cache`, mounted at `/cache`.
- Volume commit: **successful**.
- Persistence check: `Volume.reload()` exposed the canonical file at the exact path with the exact expected size; a final volume listing showed the canonical file and no partial artifact.
- Total GPU allocations: **0**.
- ComfyUI starts: **0**.
- H3 enqueues: **0**.
- No web endpoint, persistent service, `min_containers`, bridge, workflow, prompt, S01, S03, plugin, or generated media operation was used.

## Source changes

No production source, plugin, prompt, workflow, or binary artifact was changed. The temporary CPU-only runner was removed after completion. The only tracked file from this task is this report; the checkpoint remains in the persistent Modal volume and is not committed to Git.
