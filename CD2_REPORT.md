# CD2 — A100-80GB execution

Date: 2026-08-31
Decision: **A — CODEX DRAMA EXECUTION PASSES ON A100-80GB**

## Ponytail and scope

Ponytail full mode was used. This was one isolated CD2 attempt from:

`/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`

- Starting commit: `d456f026a4c2fc518c7b4608a34f5fa5eb4a8090`
- Branch: `codex/cd1-1-storyboard-original`
- Protected checkout was not modified:
  `/home/karim/Documents/minimax-h3-microdrama`
- No CD3, retry, second seed, second take, public bridge restart, MCP
  connector, model download, or generated-media commit was performed.

## A100 allocation probe

Temporary probe: `/tmp/modal_a100_80gb_probe.py`

- Exact request: `gpu="A100-80GB"`
- Region specified: no
- Cloud specified: no
- `min_containers` specified: no
- Volume used: no
- Web server used: no
- Command: one bounded `modal run`, wrapped with a 120-second timeout
- Worker allocated: yes
- Probe result: `GPU 0: NVIDIA A100 80GB PCIe (UUID: GPU-d91e5f84-4eae-57c2-69ac-1f930016870e)`
- Probe wall time was approximately 6.15 seconds including Modal setup and
  teardown; worker-only allocation latency was not separately emitted.
- The temporary probe app completed and had no active container afterward.

## CD2 execution

The single temporary runner was `/tmp/cd2_a100_runner.py`.

- Modal app: `minimax-h3-codex-drama-cd2-a100`
- Function: `run_cd2`
- Modal app id: `ap-eMJ5F0j8ybHLFGnjTtlyy5`
- GPU request: `gpu="A100-80GB"`
- Actual GPU: `GPU 0: NVIDIA A100 80GB PCIe (UUID: GPU-127868c8-9e12-8221-705b-76a93720d79f)`
- Modal run: <https://modal.com/apps/dadakarim081/main/ap-eMJ5F0j8ybHLFGnjTtlyy5>
- Allocation latency: 4.36 seconds
- ComfyUI startup: 26.06 seconds
- ComfyUI execution: 423.49 seconds
- Generation wall time: 426.12 seconds
- End-to-end function wall time: 452.99 seconds
- Peak VRAM: 72,476 MiB

These are A100-80GB measurements and are not an apples-to-apples comparison
with the earlier L40S attempt.

## Locked controls and staging

- Route: `--mode r2v --variant storyboard-original`
- `prompt_enhance`: `false`
- Canonical API SHA-256:
  `0ef2ffa84db75bcf84d436ac116e1ac11688eca67797e433019cc6342ee5cd25`
- Prompt SHA-256:
  `e735d7adaacd04998015ab1b17f9a5b407a19d6cfba228f9e2291d492ac8b9cc`
- Storyboard SHA-256:
  `9dc14895bae2396cac2ff54154398b9fb365c7f8d8c075a8a0903006f069ed2e`
- Standalone Audio1 SHA-256:
  `f78f0c12bca386fdc86edf88ff53429ae20796ac97a18b5aef9607ac55825260`
- Seed immediately before enqueue: `774787641417050`
- Prepared graph SHA-256:
  `252492149c6f5534331b444a9369e9dbb54b42b339b073b59456f63aeedab44b`

Codex Drama's `storyboard-original` preparer staged the existing storyboard
and standalone Audio1 and changed only the locked mutable fields plus the
output prefix. Node 11 routed `ref_images.ref_image_0` to the storyboard and
`ref_audios.ref_audio_0` to the standalone Audio1. No
`ref_video_audios.ref_video_audio_0` was added. The graph preserved node 39's
megapixels mode, megapixels value, alignment, CUDA device, fp16 precision, and
chunking; `10Eros_Max_h3_TURBO_ref2va_beta2.safetensors` remained selected and
Larry Turbo was not added.

## Validation, enqueue, monitoring, and retrieval

- Validation package: `comfyui-mcp@0.49.6`
- Validation target: the actual ComfyUI runtime inside the A100 container
- Validation result: `valid: true`, `issues: []`, summary `Workflow is valid`
- Enqueue count: exactly 1
- Queue response: `number: 0`, `node_errors: {}`
- Prompt id: `a4d4ca84-8f73-465c-933b-aae0040aaa9e`
- The exact prompt id was monitored through `execution_success`.
- Retrieval: success; the output was copied from the Modal volume to
  `/tmp/cd2_m6_2_storyboard_original_a100.mp4`.

The validation helper used the pinned package against container-local
ComfyUI. No persistent or public web-server bridge was started. The local
runner performed one direct local `/prompt` submission after validation and
the fixed-seed assertion immediately before enqueue.

## Output and minimal review

Modal output:

`/cache/cd2-output/1788178934843530969/cd2_m6_2_storyboard_original_a100_00001-audio.mp4`

Local copy:

`/tmp/cd2_m6_2_storyboard_original_a100.mp4`

- Dimensions: 1344×768
- Frames: 294
- Frame rate: 24 fps
- Duration: 12.256 seconds
- Video: H.264
- Audio: AAC-LC, stereo, 32 kHz
- File size: 5,567,011 bytes
- SHA-256:
  `5b6c1938e2c4824b1ebac8f35cae54addb7fd33108ab39520b97186af5398ec8`

Sampled opening, middle, closing, and four speaking-segment frames:

- identity remained coherent across the sampled sequence;
- chronology was coherent: bus stop, speaking close-up, then inside the bus;
- a speaking shot was present and the mouth position changed across the
  sampled dialogue segment;
- no catastrophic morphing or severe ghosting/smear was apparent in the
  sampled frames;
- the single AAC track was non-silent (`mean_volume: -17.5 dB`), with no
  second audio stream or double soundtrack detected.

## Repository and Modal state

Only `CD2_REPORT.md` was added by this milestone. No source integration fix
was necessary. Generated media remains outside the repository and was not
pushed.

The protected checkout remained at its pre-existing state (`?? m8c/`). The
CD2 checkout's pre-existing untracked `?? __pycache__/` and `??
cd2_modal_bridge.py` were left untouched. After the run, Modal container list
was empty; the probe and CD2 app both exited normally.

The final report commit SHA and push result are recorded in the final task
handoff because a commit cannot embed its own content hash. The report was
committed and pushed only to the authenticated fork:

`fork` → <https://github.com/dadakarim081-rgb/MiniMax-H3-Codex-Drama>

Target branch: `codex/cd1-1-storyboard-original`

## Decision

**A — CODEX DRAMA EXECUTION PASSES ON A100-80GB.**

The pinned Codex Drama route staged, validated, enqueued once with the locked
seed, monitored the exact prompt, retrieved the expected MP4, and exited
normally on A100-80GB. Stop after this CD2 attempt.
