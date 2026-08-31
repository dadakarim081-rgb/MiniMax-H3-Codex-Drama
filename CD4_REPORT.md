# CD4 — Native Codex Drama end-to-end proof

Date: 2026-08-31  
Decision: **D — concrete functional blocker**

## Scope and baseline

- Ponytail: full mode confirmed.
- Project resumed: `outputs/the-last-bus` in the existing Producer project.
- Branch: `codex/cd1-1-storyboard-original`.
- Starting commit: `2bcfefc`.
- Locked visual assets were reused; no approved Nora, scene master, storyboard, or keyframe was regenerated.
- Producer route selected from the shot contract: `frame-to-video` using native I2V because each shot has a literal opening keyframe. No `storyboard-original` route was forced.
- Prompt files: `outputs/the-last-bus/prompts/minimax-h3/s01-i2v-turbo.md`, `s02-i2v-turbo.md`, `s03-i2v-turbo.md`.
- Prepared workflows: `outputs/the-last-bus/workflows/S01-i2v-turbo.json`, `S02-i2v-turbo.json`, `S03-i2v-turbo.json`.
- Local workflow self-check passed for all three graphs: I2V Turbo node family, first-frame binding, 1344×768 dimensions, and fixed seeds 4101/4102/4103.

## Modal execution

Temporary runner: `/tmp/cd4_modal_runner.py`  
Modal app: `minimax-h3-codex-drama-cd4-production-a100` (`ap-fGmlz28di1OOSNs9XDDZoB`)  
Modal function: `run_cd4`  
GPU request: `A100-80GB` (the allowed fallback after the prior L40S allocation blocker)  
GPU allocated: yes — `GPU 0: NVIDIA A100-SXM4-80GB`  
Volume: `minimax-h3-microdrama-cache` mounted at `/cache`  
Model downloads: 0; all required cached model files were present.

The function started a local ComfyUI `0.33.2` process on `127.0.0.1:8188`, validated the native/Turbo node set, observed an empty queue (`running=0`, `pending=0`), and used no public endpoint, bridge, web server, concurrency setting, region, cloud, or persistent service. The validator was the installed `comfyui-mcp@0.49.6` library invoked locally; no MCP server or connector was used.

Allocation timing was not exposed as a separate Modal queue event. Observable timing was:

- remote function wall time: `49.837 s`
- ComfyUI startup: `16.019 s`
- worker start timestamp: `2026-08-31T16:57:48.582234+00:00`
- Modal app lifecycle `created_at` to worker start was approximately `239.6 s`, including image construction and startup overhead, not pure GPU queue time.

## Generation result

Exactly one CD4 `/prompt` call was made, for S01 only. S02 and S03 were not enqueued. No take was accepted and no second take was attempted.

- S01 route/variant: `frame-to-video` / `i2v-turbo`
- S01 seed: `4101`
- S01 prompt ID: `b3070564-bbf0-4ecb-8446-2dc33d91298a`
- S01 workflow validation: passed before enqueue
- S01 output: none
- S02/S03 prompt calls: 0
- CD4 generation enqueue count: 1

The exact ComfyUI failure was:

```text
RuntimeError: Failed to find C compiler. Please specify via CC environment variable or set triton.knobs.build.impl.
```

It occurred while the Qwen/MiniMax text encoder reached Triton’s CUDA `bmm_outer_product` helper compilation. This is a temporary runtime-image dependency failure, not Modal GPU-capacity waiting: the A100 worker was allocated, ComfyUI became ready, native nodes were present, and the prompt entered execution before failing.

## Required gates

- `final/master.mp4`: not produced; assembly not run because no usable shots existed.
- Media-info, contact sheet, timeline, technical QC, and visual-QC recording: not produced because generation stopped before media output.
- CD2 generation enqueue count remains `0`.
- CD2 bridge restarted: **no**.
- ComfyUI started: only inside the temporary CD4 worker; it was terminated on exit.
- CD4 Modal app stopped: **yes**.
- Active Modal containers after cleanup: **0**.
- Repositories modified: **no tracked source changes**. Only the ignored Producer state/prompt/workflow artifacts and this report were written; generated media was not added to Git.

The project state records `shot-generation: failed` with the same blocker. Stop after this probe; the next corrective action would be to add a compiler to the temporary image and rerun CD4, which was intentionally not attempted under the no-retry rule.
