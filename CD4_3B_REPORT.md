# CD4.3B — 10Eros beta4 S02 controlled generation proof

Date: 2026-08-31

## Decision

**C — 10EROS SHOWS NO MEANINGFUL IMPROVEMENT**

The premature arrival remains substantially similar and occurs earlier in the 10Eros proof, so the failure still points to conditioning/shot semantics rather than the official-plus-Larry stack.

## Run record

- Ponytail: full mode.
- Repository: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`.
- Branch: `codex/cd1-1-storyboard-original`.
- Starting commit: `98e3d7c` (`docs: record CD4.3A checkpoint staging`).
- Modal app: `minimax-h3-codex-drama-cd4-3b-10eros-a100` (`ap-cbrLjOdTlsJ4uPkfTiQHrc`).
- Modal function: `run_cd4_3b`.
- Requested GPU: `A100-80GB`.
- Actual GPU: `NVIDIA A100-SXM4-80GB`, `81920` MiB.
- Execution shape: one temporary A100 function, local ComfyUI on `127.0.0.1:8188`, no public endpoint, bridge, persistent service, or `min_containers`.

## Checkpoint and locked inputs

- Staged checkpoint: `/cache/comfy-models/diffusion_models/10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors`.
- Cheap GPU-worker check: passed; file existed at exactly `20,967,637,320` bytes. The full SHA-256 was not recomputed, as authorized by CD4.3A persistence proof.
- Model downloads during CD4.3B: **0**.
- Native graph basis: `skills/minimax-h3-comfyui/assets/workflows/i2v.api.json`, the plugin's standard non-Turbo I2V API graph, loaded and patched in memory only.
- Current CD4.2 S02 prompt was reused unchanged, including the repair block; prompt SHA-256: `df7fd00ecaf09e74b5b1c1fab76ac70ccbd7ce938da3e63262721dc33c9fc77c`.
- First frame: node `104.first_frame = ["114", 0]`; node `114.image = "s02-last-chance.png"`.
- Resolution/duration: `1344×768`, length `124`.
- Seed: `4102`.
- Text encoder: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`.
- Video VAE: `minimax_h3_video_vae_fp16.safetensors`.
- Audio VAE: `minimax_h3_audio_vae_fp32.safetensors`.

## Exact model-stack change from CD4.2

- Node `6`: `minimax_h3_fl2va_pruned_int8_convrot.safetensors` → `10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors`.
- CD4.2 node `134` (`MiniMaxH3TurboLoRA`, Larry `minimax_h3_turbo_v4_step600_ema.safetensors`) was absent; no `lora_name`, Turbo LoRA, or `MiniMaxH3TurboSampler` occurred in the executed graph.
- Native node `17`: `KSamplerSelect`, `sampler_name = euler`.
- Node `9`: `scheduler = simple`, `steps = 8`, `denoise = 1.0`.
- Node `9` and node `16` used the native diffusion output from node `6`; no second sampling stage or latent-upscaler node was present.
- All creative conditioning remained fixed: prompt, first frame, seed, dimensions, duration, Qwen encoder, video VAE, and audio VAE.

## Runtime validation and generation

- ComfyUI startup: `34.458325385` seconds.
- ComfyUI starts: **1**.
- Live `/object_info` graph validation: **passed with zero errors**.
- Validated graph settings: beta4 checkpoint selected; Larry Turbo absent; Euler/simple/8; seed 4102; first frame correctly bound; no latent upscaler.
- Prompt ID: `0c27554b-a67a-4534-9343-26e1798cfaa2`.
- H3 enqueues: **1**.
- Generation execution time: `231.978044455` seconds.
- Total new H3 generations: **1**.
- ComfyUI was terminated after the completed history entry and the Modal app exited.

## Output and technical QC

- Remote output: `/cache/cd4-3b-output/s02-10eros-t1/cd4-3b/s02_i2v_10eros_beta4_00001_.mp4`.
- Local output: `outputs/the-last-bus/clips/cd4-3b/S02-i2v-10eros-beta4.mp4`.
- Dimensions: `1344×768`.
- Frame rate: `24/1` fps.
- Duration: `5.167000` seconds.
- Video: H.264.
- Audio: AAC, stereo, `32000` Hz.
- Output size: `1,402,491` bytes.
- Output SHA-256: `a5fd3056a779e149130d06c693cd50fce148d7e821ef1cea93e6b1432dba9fb1`.
- Full FFmpeg decode: **passed** with no stderr.
- Contact sheet and inspection frames are retained under the ignored project output tree; no media is committed.

## Direct comparison with CD4.2 seed 4102

Baseline: `outputs/the-last-bus/clips/cd4-2/S02-i2v-turbo-t1.mp4`, SHA-256 `20bcd45d3e96155cd61061aa26af74887000aabfe8abaacb548b4b2a77d4bb96`.

- At approximately `1s`, the beta4 result already shows a bus centered on the road with bright headlights; the matching baseline frame has an empty road.
- At approximately `4s`, the beta4 result shows a large bus entering from the right; the baseline shows its known left-edge bus and vehicle/headlight failure later in the shot.
- Beta4 preserves the bus-stop setting, mustard raincoat, backpack, and recognizable Nora identity reasonably well, with no dominant anatomy failure. It does not obey the fixed no-bus/no-headlights repair block, and its arrival timing is worse than the baseline.
- Overall visual quality is usable-looking in isolation but not usable for this shot because the primary temporal constraint fails immediately.

## Source changes

No production source, prompt, workflow, plugin, S01, S03, or project-state file was changed. The temporary runner was removed after execution. The only tracked file from CD4.3B is this report; generated media and contact sheets remain ignored and the checkpoint remains in the persistent Modal volume.
