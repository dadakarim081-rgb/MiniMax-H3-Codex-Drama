# CD3.1 Modal stock H3 readiness preflight

Date: 2026-08-31

## Result

Decision: **B — ready after one missing model was added**.

The independent one-shot preflight allocated an A100-80GB, started the pinned
ComfyUI runtime on localhost, and validated the native stock T2V, I2V
first+last-frame, and R2V API workflows. FL2VA was the only required model
missing at the start. It was downloaded once into the existing cache, then
size- and SHA256-verified. No workflow was queued or executed.

The runner's post-staging result was mechanically labelled `A` because all
post-staging checks passed; the milestone rubric is `B` because one model had
to be added during this preflight.

## Ponytail and isolation

- Ponytail full mode: confirmed.
- Target repository: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`.
- Branch before the report: `codex/cd1-1-storyboard-original`.
- HEAD before the report: `2402a6f35ca1d3effca5a904b72e45b89f596754`.
- Temporary runner: `/tmp/cd3_1_modal_preflight.py`.
- One bounded command: `timeout 150m modal run /tmp/cd3_1_modal_preflight.py`.
- No retry was issued.
- No video was generated; no MiniMax H3 generation was run.
- No `/prompt` request was made; the pinned validator was imported directly as
  a library and an MCP server/transport was not started.

## Modal probe

| Item | Value |
|---|---|
| Modal app | `minimax-h3-codex-drama-cd3-1-preflight` |
| Modal function | `readiness_preflight` |
| App ID | `ap-ESduzkbOZf6XDCSziSux7K` |
| Requested GPU | `A100-80GB` |
| Actual GPU | `GPU 0: NVIDIA A100-SXM4-80GB` |
| Worker allocated | Yes |
| Existing volume | `minimax-h3-microdrama-cache` |
| Volume mount | `/cache` |
| Region specified | No |
| Cloud specified | No |
| `min_containers` specified | No |
| `max_containers` specified | No |
| Scaledown/concurrency settings | None |
| Volume used | Yes; existing volume only |
| Web server/public endpoint | No; ComfyUI listened on `127.0.0.1:8188` inside the worker |
| Secrets | None |
| Prompt endpoint calls | 0 |
| Generation enqueue count | 0 |

The worker container was observable from `2026-08-31 17:11:20+01:00`.
The local command wall time was `780.709 s`; function time was `764.321 s`.
The exact Modal scheduler queue wait was not separately exposed. `nvidia-smi -L`
completed normally in `0.035 s` and reported:

```text
GPU 0: NVIDIA A100-SXM4-80GB (UUID: GPU-8018c372-6480-9802-9c73-6834b385e33a)
```

## Native manifest and route contracts

The native manifest was inspected before runtime validation. The standard
graphs were prepared with the existing `prepare_workflow.py` helper and
`--no-turbo`:

| Route | Native model/node contract |
|---|---|
| T2V | FL2VA UNET, Qwen3-VL text encoder, video VAE, audio VAE, `MiniMaxH3ImageToVideo` |
| I2V | Same FL2VA/Qwen/video-VAE/audio-VAE stack, `MiniMaxH3ImageToVideo`, first frame plus optional last frame |
| R2V | REF2VA UNET, Qwen3-VL text encoder, video VAE, audio VAE, `MiniMaxH3ReferenceToVideo` |

The runtime exposed both `first_frame` and `last_frame` on
`MiniMaxH3ImageToVideo`. The two-reference R2V graph also exposed both
reference image inputs. Turbo support was not executed, but the runtime
registered `MiniMaxH3TurboSampler` and `MiniMaxH3TurboLoRA`, and the Larry
Turbo LoRA was present in the cache.

Prepared graph hashes:

| Graph | Temporary path | SHA256 |
|---|---|---|
| T2V | `/tmp/cd3_1_t2v.json` | `5632152f014d60e0b7d659f9f7b0239a080fcc174a68720ca5a43e360e6538d8` |
| I2V first+last | `/tmp/cd3_1_i2v_first_last.json` | `6ca2d61c82a661cfcf49ce4fe09ba0e9feafa20f1513b2f08c660687ed384b31` |
| R2V | `/tmp/cd3_1_r2v.json` | `f43973511c79dbecb80bc96ad3a76be13d114a47caa557b3bb365a001bdc0986` |

Minimal dummy inputs were used only for graph input discovery:
`/tmp/cd3_1_first.png`, `/tmp/cd3_1_last.png`,
`/tmp/cd3_1_ref0.png`, and `/tmp/cd3_1_ref1.png`.

## Persistent model cache

The cache was inspected before any download. Exact required paths and sizes
reported by the worker are:

| Model | Exact cache path | Before | Final size |
|---|---|---:|---:|
| FL2VA | `/cache/comfy-models/diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors` | Missing | `20,970,379,616` bytes |
| REF2VA | `/cache/comfy-models/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors` | Present | `20,970,379,616` bytes |
| Qwen3-VL text encoder | `/cache/comfy-models/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | Present | `15,687,142,551` bytes |
| Video VAE | `/cache/comfy-models/vae/minimax_h3_video_vae_fp16.safetensors` | Present | `5,207,808,496` bytes |
| Audio VAE | `/cache/comfy-models/vae/minimax_h3_audio_vae_fp32.safetensors` | Present | `605,254,808` bytes |
| Larry Turbo LoRA | `/cache/comfy-models/loras/minimax_h3_turbo_v4_step600_ema.safetensors` | Present | `779,849,816` bytes |

Only the missing FL2VA file was downloaded. The immutable authoritative source
used was `Comfy-Org/MiniMax-H3`, revision
`3f57e8291d2ef846f9a074b1b76d2767db434abe`, with expected size
`20,970,379,616` bytes and expected SHA256
`e889202c41dafb67b10d67b97f0d8541508036a6090af23425a5c2615d03c47a`.
The downloaded file matched that SHA256 exactly. The transfer took
`717.237 s` and was committed to the existing Modal volume.

Source lock: [Comfy-Org MiniMax-H3 FL2VA at the immutable revision](https://huggingface.co/Comfy-Org/MiniMax-H3/blob/3f57e8291d2ef846f9a074b1b76d2767db434abe/diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors)

## ComfyUI runtime

- ComfyUI commit: `7cee3ceb1a35503172e0dfb8dbdbdedee2aba8aa` (`0.33.2`).
- VideoHelperSuite commit: `4ee72c065db22c9d96c2427954dc69e7b908444b`.
- KJNodes commit: `3f20054214fec9f9234fd3841ae6f1e4287948f6`.
- Larry Turbo commit: `4274783a23afcfdbea3b4876cb79effd6c510785`.
- Latent upscaler commit: `6a4b191e8af583b7c097f564690325f91d18c2e2`.
- PyTorch: `2.13.0+cu130`.
- ComfyUI reached `http://127.0.0.1:8188` in `26.039 s`.
- Runtime saw `81,153 MB` total VRAM and an A100-SXM4-80GB device.
- Required H3 nodes were all present, including `MiniMaxH3ImageToVideo`,
  `MiniMaxH3ReferenceToVideo`, and the standard sampler/decoder/output nodes.
- No custom-node import failure appeared in the captured startup log.
- ComfyUI was terminated after inspection and validation.

## Route validation

Pinned package: `comfyui-mcp@0.49.6`, using its direct
`validateWorkflow(workflow, { health: false })` implementation against the
actual local ComfyUI `/object_info` endpoint. No validation call executes a
workflow.

| Route | Validator result | Issues |
|---|---|---:|
| T2V | `Workflow is valid` | 0 |
| I2V first+last | `Workflow is valid` | 0 |
| R2V | `Workflow is valid` | 0 |

ComfyUI `/queue` was checked before and after validation:

```text
before: running=0, pending=0
after:  running=0, pending=0
```

## CD2 comparison (read-only)

The temporary CD2 bridge definition was compared with the known-good native
runner in `/home/karim/Documents/minimax-h3-microdrama/modal/app.py`.

| Setting | CD2 bridge | Known-good runner |
|---|---|---|
| GPU | `L40S` | `L40S` |
| Volume | `/cache` | `/cache` |
| `region=` | Not present | Not present |
| `cloud=` | Not present | Not present |
| `min_containers=` | `1` | Not present |
| `max_containers=` | `1` | Not present |
| Unusual concurrency | `@modal.concurrent(max_inputs=100)` | None |
| Web lifecycle | `@modal.web_server(8188, startup_timeout=120, label=...)` | None; local process is started and terminated inside the function |
| ComfyUI listen address | `0.0.0.0` | `127.0.0.1` |

Conclusion: CD2 did not introduce a region or cloud placement restriction.
It did introduce keep-warm/single-container constraints, a 100-input
concurrency setting, and a persistent Modal web-server lifecycle. Those are
the material scheduling/lifecycle differences from the known-good runner.

## Safety and repository state

- CD2 bridge restarted: **No**.
- CD2 generation enqueue count: **0**.
- CD3.1 H3 generation count: **0**.
- `/prompt` calls: **0**.
- Public bridge/deployment created: **No**.
- The temporary preflight app stopped at completion; final active Modal
  container count: `0`.
- Protected repository was read-only inspected only. Its prior untracked
  `m8c/` directory remained untouched.
- No source files or workflow assets were modified. This report is the only
  intended tracked change for CD3.1.
- Existing unrelated untracked files in the target worktree were left
  untouched and unstaged.

