# CD4.5B — OpenH3-IR S02 L40S generation proof

Date: 2026-09-01

Decision: **C — COMPOSER REMAINS BETTER**

The exact CD4.5A OpenH3-IR prompt was extracted and prepared in the proven native
I2V graph. Both L40S scheduling attempts were left queued without a worker. The
explicit A100-80GB capacity fallback then completed the exact one-shot S02
generation and the direct Composer comparison recorded below; the OpenH3-IR take
introduced visible traffic earlier, so Composer remains better.

## Scope and starting point

- Repository: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`
- Branch: `codex/cd1-1-storyboard-original`
- Starting HEAD: `7a86c623e86334e64a44006ab8cd25c60dadf786`
- OpenH3-IR result artifact:
  `outputs/the-last-bus/cd4-5a/openh3-ir-result.json`
- Serialized result SHA-256:
  `d006f84cccd5a2c59b00e59f49a32bfca12d121d3f49d1969f526cb7426200a4`
- CD4.5A final written IR SHA-256:
  `de460eac726ac75b5c3a528fe77f9632fc2f3325628be56c36662a368e1e7342`
- Approved first-frame SHA-256:
  `37bdd9a3f1f34b2859afad9b9653fa364a39d6fda47e0f526053856b9f4e9ad5`

The CD4.5A JSON was read once; OpenH3-IR, Gemini, and LiteLLM were not rerun.
The prompt wording was not changed, expanded, filtered, or merged with Composer
wording.

## Exact prompt prepared

This is the complete final written IR from CD4.5A, copied verbatim into the prompt
file used by the local graph preparer. It was not sent to ComfyUI because no worker
was allocated.

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, dim, ambient light from streetlights and the interior of the bus stop. The sky is dark blue. A medium shot frames the woman (dark wavy hair, dark eyes, medium build, wearing a yellow hooded jacket, wearing a black t-shirt, wearing a black backpack) as shown in <Picture 1>. She checks the time on her wristwatch, then lowers her wrist. The camera holds a static shot as she looks screen-right down the quiet, empty, wet road with restrained concern, holding her gaze through the end of the shot.

overall_soundscape: Steady rain taps against the glass shelter while distant traffic hums. The faint sound of her wristwatch strap moving against her jacket can be heard.

non_diegetic_music: N/A
```

Prompt SHA-256 was rechecked before the Modal call and matched
`de460eac726ac75b5c3a528fe77f9632fc2f3325628be56c36662a368e1e7342`.

## Locked graph and controls

The graph was prepared locally from:

`skills/minimax-h3-comfyui/assets/workflows/i2v.api.json`

Native API workflow SHA-256:
`29a514908a7be39d48bf02492ad81b897ae0325c81234b9c1a4e2d643bf5ea48`

Prepared graph SHA-256:
`e0ae1257219978becc4dde2073df0f0291a9b91d20eed39b7d1798b0a6acc45f`

Local mechanical assertions passed before allocation:

| Control | Prepared value |
|---|---|
| Graph variant | Standard native I2V / FL2VA; Turbo false |
| Diffusion checkpoint | `10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors` |
| Qwen encoder | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` |
| Video VAE | `minimax_h3_video_vae_fp16.safetensors` |
| Audio VAE | `minimax_h3_audio_vae_fp32.safetensors` |
| Sampler / scheduler | `euler` / `simple` |
| Steps / denoise | `8` / `1.0` |
| Seed | `4102` |
| Resolution / frames / FPS | `1344x768` / `124` / `24` |
| First frame | node `114`, `s02-last-chance.png`, linked to node `104.first_frame` |
| Last frame | absent; no node `116` |
| LoRAs | none; no Larry or other LoRA field in the graph |
| Latent upscaler | absent |
| Output prefix | `cd4-5b/S02-openh3-ir` |

The requested duration is therefore the existing effective H3 duration of
`5.166666667s`.

## Persistent-volume preflight

Read-only `modal volume ls` confirmed the required files already existed in
`minimax-h3-microdrama-cache` before the attempt:

- beta4 diffusion checkpoint: `20,967,637,320` bytes
- Qwen encoder: `15,687,142,551` bytes
- video VAE: `5,207,808,496` bytes
- audio VAE: `605,254,808` bytes

No model download was requested or performed. The existing Larry Turbo LoRA was
not selected and was not part of the prepared graph.

## Modal attempt

- Modal client: `1.5.1`
- Temporary app: `ap-zg4z5H6h5UKGH22dnyAueJ`
- Function: `run` (`fu-bT70Sjrennk4WlOU9IGiZX`)
- Requested GPU: `L40S`
- Actual GPU: none
- Volume: `minimax-h3-microdrama-cache` mounted at `/cache`
- Function shape: one GPU function, no public web endpoint, no bridge, no
  `min_containers`, no fallback, and no second attempt
- Runtime image included the proven `gcc` and `python3-dev` fix
- Intended ComfyUI bind: `127.0.0.1:8188`

Modal reported at `2026-09-01 08:44:25+01:00`:

```text
Function 'run' (...) is waiting to be scheduled on a GPU_L40S worker. We are actively working on acquiring more capacity for your workload.
```

No worker output appeared during the bounded 120-second startup window used by
the earlier allocation proof. Allocation latency and ComfyUI startup latency
are therefore **not available**. The queued function was canceled, the temporary
app was stopped explicitly, and `modal container list` was empty afterward.

## L40S attempt generation and technical record

| Field | Result |
|---|---|
| L40S allocation | Blocked; no worker |
| ComfyUI startup | Not reached |
| Live `/object_info` validation | Not reached; worker required |
| H3 enqueue count | `0` |
| Generation execution time | N/A |
| Peak GPU memory | N/A |
| Output path | None |
| Output SHA-256 | None |
| FFmpeg decode | Not applicable; no output |
| Generated media | None; `outputs/the-last-bus/cd4-5b/` remained empty |

## L40S attempt comparison with CD4.4 Composer

No fair visual comparison was possible because OpenH3-IR produced no clip. The
existing Composer baseline was not regenerated:

`outputs/the-last-bus/clips/cd4-4-ab/S02-i2v-10eros-composer.mp4`

Composer output SHA-256:
`2ff8ca56ee33499f6236ca5cedddc083e4df2363f8485372b7b4b51b5bb19484`

The recorded CD4.4 result remains: no bus through the end sample, but a generic
vehicle with red/white lights appears around 3–4 seconds. Nora identity, the
mustard raincoat/backpack, watch-to-lowered-wrist action, screen-right concern,
environment continuity, and motion/quality remain unchallenged for this milestone.

The OpenH3-IR phrase `distant traffic hums` was not visually testable because the
generation never started.

## Initial attempt decision

**E — L40S EXECUTION BLOCKED.** The exact OpenH3-IR input and locked graph were
prepared successfully, but L40S capacity prevented a worker from starting within
the bounded window. No A100 fallback, alternative seed, Composer regeneration,
S01/S03 work, assembly, or source change was made in that initial attempt.

## Retry record — five-minute L40S scheduling window

This is the requested CD4.5B retry only. It reused the existing unmodified
CD4.5A result, exact prompt, approved S02 first frame, prepared native graph, and
temporary runner. OpenH3-IR, Gemini, LiteLLM, and Composer were not rerun.

- Retry starting HEAD: `8234a21ae1cadd09cfc629c73c9245da4bce5b58`
- Result artifact SHA-256: `d006f84cccd5a2c59b00e59f49a32bfca12d121d3f49d1969f526cb7426200a4`
- Final IR prompt SHA-256: `de460eac726ac75b5c3a528fe77f9632fc2f3325628be56c36662a368e1e7342`
- First-frame SHA-256: `37bdd9a3f1f34b2859afad9b9653fa364a39d6fda47e0f526053856b9f4e9ad5`
- Prepared graph SHA-256: `e0ae1257219978becc4dde2073df0f0291a9b91d20eed39b7d1798b0a6acc45f`
- Retry start: `2026-09-01T07:51:20Z`
- Scheduling cutoff: `2026-09-01T07:56:20Z` (five minutes)
- Modal client: `1.5.1`
- Temporary app: `ap-ozs4y3jghSufbXPlyRNgz9`
- Function: `run` (`fu-exUfXrY7EtYpd9yM40Q425`)
- Requested GPU: `L40S`
- Actual GPU: none
- Persistent volume: `minimax-h3-microdrama-cache`

Modal reported the function waiting for a `GPU_L40S` worker at
`2026-09-01 08:52:05+01:00` and again at `08:52:43+01:00`. No worker allocation
appeared by the five-minute cutoff. The local Modal run was interrupted after the
window, the temporary app was stopped at `2026-09-01 08:56:39+01:00`, and a final
`modal container list --json` returned `[]`.

Because no L40S worker was allocated, the retry did not reach ComfyUI startup,
live `/object_info` validation, H3 enqueue, generation, FFmpeg decode, or visual
comparison. The retry enqueue count was `0`; no output path, output hash, runtime
metrics, or new media exists. There was no A100 fallback, prompt/model/workflow
change, second enqueue, or production-source change.

## L40S retry decision

**E — L40S EXECUTION BLOCKED.** The five-minute L40S-only retry reproduced the
allocation blocker. CD4.5B cannot make the requested visual A/B/C/D comparison
until an L40S worker can be scheduled.

## A100-80GB capacity fallback

This fallback continued the same CD4.5B experiment after the two documented L40S
capacity blockers. It changed capacity only. The CD4.5A result, complete final
prompt, S02 first frame, prepared native graph, seed, sampler, model files, and
all generation controls were unchanged. OpenH3-IR, Gemini, LiteLLM, Composer,
and the Composer baseline were not rerun.

- Fallback starting HEAD: `e9483b83683624e2c00f3038cb77725f5c46ea6a`
- Requested fallback GPU: `A100-80GB`
- Actual GPU: `NVIDIA A100-SXM4-80GB, 81920 MiB`
- Exact prompt used: the complete prompt in **Exact prompt prepared** above,
  byte-for-byte; prompt SHA-256 `de460eac726ac75b5c3a528fe77f9632fc2f3325628be56c36662a368e1e7342`
- Prompt file: `/tmp/cd45b_openh3_s02_prompt.txt` (872 bytes)
- Prepared graph SHA-256: `e0ae1257219978becc4dde2073df0f0291a9b91d20eed39b7d1798b0a6acc45f`
- Local Modal call start: `2026-09-01T08:00:29Z`
- Worker/container start: `2026-09-01 09:00:43+01:00` (approximately 14 seconds after call start)
- ComfyUI startup: `29.422s` from runner metadata; server-ready log at
  `2026-09-01 09:01:12+01:00`
- Generation execution: `217.619s` from enqueue to completed history;
  ComfyUI reported `Prompt executed in 211.52 seconds`
- Worker wall time: `247.060s`
- Local Modal call wall time: `261.134s`
- Peak VRAM: runner reported `allocated_bytes: 0` and `reserved_bytes: 0`;
  no usable peak sample was available
- Temporary Modal app: `ap-79DFklK4vkG4Yh57oPCAWe`
- Local ComfyUI: `127.0.0.1:8188`; no public endpoint, bridge, or persistent service

### Cache, validation, and enqueue

All required model files were present in `minimax-h3-microdrama-cache`; every
entry reported `downloaded: false`:

| File | Bytes |
|---|---:|
| `diffusion_models/10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors` | `20,967,637,320` |
| `text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | `15,687,142,551` |
| `vae/minimax_h3_video_vae_fp16.safetensors` | `5,207,808,496` |
| `vae/minimax_h3_audio_vae_fp32.safetensors` | `605,254,808` |

Live `/object_info` validation passed with `1,144` node definitions and no
errors. The selected graph values were:

| Control | Effective value |
|---|---|
| Checkpoint | `10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors` |
| Qwen / video VAE / audio VAE | exact cached files listed above |
| Sampler / scheduler / steps | `euler` / `simple` / `8` |
| Denoise / seed | `1.0` / `4102` |
| Resolution / frames / FPS | `1344x768` / `124` / `24` |
| First frame | `s02-last-chance.png`; SHA-256 matches approved frame |
| Larry or other LoRA | absent / false |
| Latent upscaler | absent / false |
| Last frame | absent |

The history status was `success`, the enqueue count was exactly `1`, and the
prompt ID was `9555ffb5-1fb4-4442-991d-0a14d30bc181`.

### Output and decode record

- Remote output: `/cache/cd4-5b-output/openh3-s02-1788249644089374593/cd4-5b/S02-openh3-ir_00001_.mp4`
- Local output: `outputs/the-last-bus/clips/cd4-5b/S02-i2v-openh3-ir.mp4`
- Output size: `1,269,268` bytes
- Output SHA-256: `b328eceb91d4a351ef211e433053be558767962085950da41faec8d622122ca7`
- Video: H.264 High, `1344x768`, `yuv420p`, `124` frames at `24 fps`, `5.166667s`
- Audio: AAC LC, `32 kHz`, stereo, `5.167000s`
- Container: MP4; `2` streams; `1,965,191` bit/s
- Full decode: `ffmpeg -hide_banner -v error -i ... -f null -` exited `0` with no stderr

### Direct visual comparison with CD4.4 Composer

The existing Composer baseline was used without regeneration:
`outputs/the-last-bus/clips/cd4-4-ab/S02-i2v-10eros-composer.mp4`.
Its SHA-256 remains
`2ff8ca56ee33499f6236ca5cedddc083e4df2363f8485372b7b4b51b5bb19484`.

| Criterion | CD4.4 Composer | CD4.5B OpenH3-IR on A100-80GB |
|---|---|---|
| Empty road | Violated by a generic vehicle/vehicle lights around `3–4s` | Violated earlier: a small edge cue around `0.75s`, clear generic car and paired red taillights by about `1.0s` |
| Bus | No bus | No bus |
| Headlights / vehicle lights | Generic vehicle with red/white lights late in the shot; no bus headlights | Red rear/taillights appear early; no clear headlight approach |
| Arrival / next-shot information | None | No bus arrival or next-shot information; a generic road vehicle is visible |
| Nora identity and continuity | Stable; mustard raincoat/backpack preserved | Stable; mustard raincoat/backpack preserved |
| Watch → lower wrist → screen-right concern | Readable and holds | Readable; screen-right concern holds through the end |
| Hand/face stability | Usable with normal generative softness | Usable with comparable generative softness; no identity break |
| Environment continuity | Shelter, rain, wet road preserved | Shelter, rain, wet road preserved; traffic is the violation |
| Motion / overall quality | Comparable cinematic quality | Comparable cinematic quality, but earlier traffic makes it less compliant |

The OpenH3-IR phrase `distant traffic hums` was not audio-only in this
realization: visible generic traffic and red taillights appear at approximately
the one-second mark. The clip did not visibly introduce a bus, bus headlights,
engine, arrival event, or future-shot cue.

## Final CD4.5B decision

**C — COMPOSER REMAINS BETTER.** Both takes are visually usable for Nora’s
identity, clothing continuity, watch action, screen-right gaze, and rainy shelter
environment. OpenH3-IR produces the unwanted generic vehicle/taillights roughly
two seconds earlier than Composer, so it is the more serious empty-road violation.
The A100-80GB fallback changed capacity only; it did not change the experimental
comparison.

## Commit scope

Only `CD4_5B_REPORT.md` is intended for commit. Generated media remains ignored;
pre-existing unrelated untracked files were preserved.
