# CD5.1 — Minimal Producer → Composer → 10Eros production path

Date: 2026-09-01  
Status: **PASS — S01 integration proof complete**  
Ponytail: full mode  
Repository: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`  
Branch: `codex/cd1-1-storyboard-original`  
Starting SHA: `45f14f41472d88d195cc13362ade27e86e043f1b`

## Scope

This proof used The Last Bus S01 only. S02 was not modified, regenerated, or
rerouted. No storyboard, first/last-frame bridge, OpenH3-IR, Gemini, Composer
baseline, assembly, or post-production operation was run.

The committed source change is one small Producer-owned adapter:

`skills/minimax-h3-drama-producer/scripts/production_path.py`

It reads the existing Producer state and S01 shot contract, resolves the
existing route and reference artifacts, creates the Composer interchange JSON,
invokes the pre-existing external Composer harness, captures its prompt
unchanged, and calls the existing `prepare_workflow.py` boundary. It does not
add a router class, service, workflow DSL, dependency, or state mutation.

## Producer source and route

- Shot contract: `outputs/the-last-bus/planning/shot-list.yaml`, `S01` / `Waiting`.
- Producer state: `outputs/the-last-bus/project.yaml`.
- Producer-selected route from the S01 job: `frame-to-video`.
- Prepared H3 mode: native `i2v`.
- Storyboard use: **false**. S01's existing reference roles are only
  `nora-character-master` and `bus-stop-scene-master`.
- Approved first frame: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1/outputs/the-last-bus/images/keyframes/s01-waiting.png`.
- First-frame SHA-256:
  `c073179d111f29634fe397892cb414be906122c1bee9267a3b2321020038ee19`.
- Selected reference hashes:
  - Nora character master:
    `08237ad1603fffac8e3131d93e672aec78149e82ca1db77b8dd6ba4072ecfedc`
  - Bus-stop scene master:
    `8dd5507fb524209885bbca21f63e5f679dc3ae5faef26fa34c75a86f8b5cf310`

The existing accepted S01 comparison clip was reused unchanged:

`outputs/the-last-bus/clips/cd4-1/S01-i2v-turbo.mp4`  
SHA-256: `9471f3da372163b3e2ffe863f28bc3090386f1955be3c67c41412e0c02be2077`

## External Prompt Composer

- Checkout: `/home/karim/Tools/minimax-h3-prompt-composer`
- Composer file: `/home/karim/Tools/minimax-h3-prompt-composer/Prompt_Composer.html`
- Commit: `0548331876476934a081927017041bcc2bedab81`
- Version: `H3 Prompt Composer V5.43.4`
- Existing headless harness:
  `/home/karim/Documents/minimax-h3-microdrama/tools/prompt_composer_headless.mjs`
- Runtime: Node `v24.15.0`, harness DOM runtime `happy-dom`.
- Invocation path: `previewAIImport()` → `applyAIImport()` →
  `aiImportToState()` → `projectToAIInterchange()` → `build()` → `lint()`.
- Composer input: `outputs/the-last-bus/cd5-1/composer-input.json`
- Composer input SHA-256:
  `f8aa4f218580e25d631877ac331a55b088e189082fc4f4cbe2e618cd6cb30ed8`
- Raw Composer result: `outputs/the-last-bus/cd5-1/composer-result.json`
- Captured prompt: `outputs/the-last-bus/cd5-1/composer-prompt.txt`
- Prompt SHA-256:
  `bc960e5ef316fa8e6c7d5d2bc389cc1e390735bda0ef64d3f75ad493fb569b17`
- Composer mode: `REF` / `Ref2VA` authoring mode. This did not change the
  Producer-selected H3 route, which remained native I2V.

The harness's generic six-shot acceptance predicate is not applicable to this
one-shot fixture and returned false because the input has one shot. The
one-shot acceptance used here passed: one generation, one shot, generated
prompt, and zero blocking Prompt Check errors. The only warnings were the
known literal-subject-name warnings and the expected lack of standalone source
views in the semantic interchange.

### Exact Composer prompt

```text
subject_definitions:
<Subject 1> is Nora, an adult woman in her late twenties with shoulder-length dark wavy hair, a mustard-yellow raincoat over dark clothes, black ankle boots, and a small black backpack.
<Subject 2> is the bus stop, described as one modern glass-and-metal bus shelter at blue hour after light rain, with one bench, wet reflective pavement, and a road directly in front.

summary:
[reference generation] establish Nora and the single bus-stop environment.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - Nora's complete defined identity and body proportions are preserved.
<Subject 2> (appears in [Shot 1]): fully_preserved - the environment’s defined architecture, layout, and spatial continuity are retained.

detailed_description:
The target video is in a live-action and cinematic style.
[Shot 1] The shot takes place in <Subject 2>. At first appearance, <Subject 2> matches the complete defined environment identity, architecture, layout, and reference lighting. At first appearance, <Subject 1> (Nora) matches the complete defined identity and physical appearance: An adult woman in her late twenties with shoulder-length dark wavy hair, a mustard-yellow raincoat over dark clothes, black ankle boots and a small black backpack. Nora waits alone inside or immediately beside the shelter. The described action controls subject movement. The Camera instructions change only the camera. The camera follows its own path through the location. Camera: begin with a wide shot at eye level, with the camera directly in front of <Subject 1>. Nora waits alone inside or immediately beside the shelter. The camera smoothly moves along a straight path from that position to directly in front of <Subject 1> while pushing in. The framing changes from a wide shot to a medium shot. Keep the move rigidly stable and shake-free. A natural-perspective lens preserves familiar proportions without pronounced wide-angle distortion or telephoto compression. End on a medium shot at eye level with the camera directly in front of <Subject 1>. Rain-wet ambience and distant traffic; no dialogue can be heard.

overall_soundscape:
rain-wet ambience and distant traffic; no dialogue.

non_diegetic_music:
N/A
```

## Existing H3 preparer and locked graph

- Preparer: `skills/minimax-h3-comfyui/scripts/prepare_workflow.py`.
- Workflow basis: `skills/minimax-h3-comfyui/assets/workflows/i2v.api.json`.
- Effective variant: `standard` / `--no-turbo`, because CD5 requires native
  beta4 without Larry Turbo stacking.
- Prepared graph:
  `outputs/the-last-bus/cd5-1/s01-prepared-i2v.json`
- Prepared graph SHA-256:
  `f0d66f901145efbefaaf2850d495d276d9242732bb04397e0f8d17eea67c5138`

| Control | Value |
|---|---|
| Diffusion checkpoint | `10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors` |
| Qwen encoder | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` |
| Video VAE | `minimax_h3_video_vae_fp16.safetensors` |
| Audio VAE | `minimax_h3_audio_vae_fp32.safetensors` |
| Sampler / scheduler | `euler` / `simple` |
| Steps / denoise | `8` / `1.0` |
| Seed | `4101` (existing Producer S01 seed) |
| Size | `1344×768` |
| Requested duration | `5.0s` |
| Effective H3 length | `124` frames at `24` fps (`5.166667s` video) |
| First-frame binding | node `104.first_frame = ["114", 0]`; node `114.image = s01-waiting.png` live |
| Last frame | None |
| Larry / other LoRA | None |
| Latent upscaler | None |

## CPU dry-run

Command shape:

```text
python3 skills/minimax-h3-drama-producer/scripts/production_path.py \
  --project-root outputs/the-last-bus \
  --composer-harness /home/karim/Documents/minimax-h3-microdrama/tools/prompt_composer_headless.mjs \
  --output-dir outputs/the-last-bus/cd5-1
```

Result: **passed before any GPU allocation**.

The inspectable dry-run manifest is
`outputs/the-last-bus/cd5-1/dry-run.json`. It records the Producer contract,
route, selected references, Composer input/result/prompt, hashes, and prepared
graph. Mechanical assertions passed for I2V routing, S01 first frame, external
Composer invocation, beta4, native Euler/simple/8, seed 4101, normal H3 VAEs,
no last frame, no storyboard, no latent upscaler, no Larry/LoRA, and no Turbo
sampler node.

The existing preparer tests also passed: `16 passed`.

## GPU/runtime execution

The two earlier bounded CD4.5B L40S capacity failures were not retried. A new
L40S investigation would have violated the practical-capacity condition, so the
already-proven explicit fallback was used directly.

- Requested GPU: `A100-80GB`
- Actual GPU: `NVIDIA A100-SXM4-80GB, 81920 MiB`
- Modal app: `minimax-h3-codex-drama-cd5-1-s01-a100-80gb`
- Temporary function: one GPU function, one worker, no `min_containers`.
- ComfyUI: local `127.0.0.1:8188`; no public endpoint and no bridge.
- Runtime image fix: existing `gcc` + `python3-dev` shape.
- ComfyUI commit: `7cee3ceb1a35503172e0dfb8dbdbdedee2aba8aa`
- VideoHelperSuite commit: `4ee72c065db22c9d96c2427954dc69e7b908444b`
- KJNodes commit: `3f20054214fec9f9234fd3841ae6f1e4287948f6`
- Modal client: `1.5.1`
- Model downloads: **0**. All four required files were present in
  `minimax-h3-microdrama-cache` at the pinned sizes before ComfyUI started.

| Timing / resource | Result |
|---|---:|
| Modal call wall time (allocation + worker) | `257.834s` |
| Worker function wall time | `246.210s` |
| ComfyUI startup | `27.451s` |
| Generation execution after enqueue | `218.744s` |
| Peak sampled GPU memory | `41,967 MiB / 81,920 MiB` |
| Live `/object_info` node types | `1,144` |

Live graph validation passed with zero errors. The live graph selected beta4,
the Qwen encoder, both normal H3 VAEs, native Euler/simple/8, denoise 1.0,
seed 4101, 1344×768, 124 frames, and `s01-waiting.png`. Larry, other LoRAs,
Turbo sampler, last-frame, and upscaler nodes were absent.

H3 enqueue count: **1**. No retry, alternate seed, S02, S03, or assembly was
performed. ComfyUI was terminated after completion and the temporary Modal app
stopped.

## Output and technical validation

- Remote output:
  `/cache/cd5-1-output/s01-1788253662732677510/cd5-1/s01_i2v_composer_00001_.mp4`
- Local output:
  `outputs/the-last-bus/clips/cd5-1/S01-i2v-composer.mp4`
- Local output SHA-256:
  `4dfe119086a69bcf723784d40dc68379071c2822f0d0ac439c8f4ebaceed9ad9`
- Output size: `1,678,445` bytes.
- Dimensions: `1344×768`.
- Video: H.264 High, progressive, `24/1` fps, `124` frames.
- Audio: AAC-LC, stereo, `32000` Hz.
- Duration: video `5.166667s`; container/audio `5.167000s`.
- Full FFmpeg decode: **passed**, no stderr.
- FFprobe: **passed**, two streams (H.264 video + AAC audio).

## Visual acceptance against existing S01

Inspection frames and matched contact sheets are under the ignored directory
`outputs/the-last-bus/cd5-1/inspection/`.

| Gate | Composer-path S01 result |
|---|---|
| One Nora / identity | Pass. One recognizable Nora remains consistent. |
| Wardrobe / backpack | Pass. Mustard raincoat and black backpack remain present. |
| Shelter / bench / road | Pass. The glass shelter, bench, wet road, blue-hour light, and warm practical remain coherent. |
| Waiting / roadward behavior | Pass. Nora waits facing the road with hands in pockets; no unrelated beat appears. |
| Camera intent | Pass with a stronger but smooth push-in from wide toward medium framing; this is the meaningful difference from the mostly static accepted baseline. |
| Hand / face stability | Pass. No obvious extra-limb, face, or hand instability in the inspected samples. |
| Bus / arrival cue | Pass for S01. No identifiable bus or approaching vehicle enters the shot. |
| Road lights | Pass with note below. Distant lamp points and wet-road reflections remain consistent with the accepted baseline and do not form an identifiable arrival event. |

A conservative automated video review classified some distant light points as
possible vehicle lights at approximately `0.0–0.6s`. Direct matched frame-sample
and side-by-side inspection found no discernible vehicle body, bus, or
approaching arrival cue; the same fixed road-light chain and reflections are
visible in the accepted CD4.1 baseline. This advisory does not fail an existing S01 hard gate:
`one-Nora`, `wardrobe-intact`, and `shelter-bench-road-readable` all pass.

Overall visual acceptance: **S01 remains production-usable relative to the
existing accepted S01 take**. The integration proof passes; this was not a
quality shootout or a request for aesthetic optimization.

## Invocation boundaries

- OpenH3-IR: **not invoked**; remains parked per CD5.
- LiteLLM / Gemini: **not invoked**.
- Storyboard skill: **not invoked** for S01.
- Composer checkout: **not modified**.
- ComfyUI: temporary local process only; **1** start, then terminated.
- GPU allocations: **1** A100-80GB allocation.
- H3 generations: **1** enqueue.
- Model downloads: **0**.
- Generated media and dry-run artifacts remain ignored and are not committed.

## Commit scope

Tracked files intended for this milestone:

- `skills/minimax-h3-drama-producer/scripts/production_path.py`
- `CD5_1_REPORT.md`

The temporary Modal runner and all generated media remain under ignored output
paths. No Producer project-state file, prompt source, workflow asset, external
checkout, or S02 artifact was changed.
