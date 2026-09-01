# CD4.5B — OpenH3-IR S02 L40S generation proof

Date: 2026-09-01

Decision: **E — L40S EXECUTION BLOCKED**

The exact CD4.5A OpenH3-IR prompt was extracted and prepared in the proven native
I2V graph. An initial single Modal L40S function call was left queued beyond its
bounded 120-second startup window. The later five-minute L40S retry recorded below
was also left queued and stopped without allocating a worker. No ComfyUI process
started, no live graph validation ran, no H3 enqueue occurred, and no output media
was produced.

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

## Generation and technical record

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

## Comparison with CD4.4 Composer

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

## Current decision

**E — L40S EXECUTION BLOCKED.** The five-minute L40S-only retry reproduced the
allocation blocker. CD4.5B cannot make the requested visual A/B/C/D comparison
until an L40S worker can be scheduled.

## Commit scope

Only `CD4_5B_REPORT.md` is intended for commit. Generated media remains ignored;
pre-existing unrelated untracked files were preserved.
