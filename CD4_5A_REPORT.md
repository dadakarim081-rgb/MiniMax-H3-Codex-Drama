# CD4.5A — OpenH3-IR Vertex compatibility proof

Decision: **A — OPENH3-IR COMPILES SUCCESSFULLY THROUGH VERTEX**

The pinned OpenH3-IR `0.4.1` checkout passed its vision doctor through a temporary
localhost LiteLLM adapter backed by Vertex AI Gemini, then produced a valid S02 IR.
No production source was changed. The full serialized result, including the complete
plan, IR, sections, findings, provenance, bindings, and hashes, is retained at:

`outputs/the-last-bus/cd4-5a/openh3-ir-result.json`

The doctor transcript is retained at:

`outputs/the-last-bus/cd4-5a/doctor.txt`

Both are ignored by the project `outputs/` rule.

## Scope and starting point

- Branch: `codex/cd1-1-storyboard-original`
- Starting HEAD: `f6ae6a1e75e7a9d6b745a345fb56ab33434e7c48`
- External checkout: `/home/karim/Tools/open-h3-ir`
- External pinned commit: `fd031e136ae3d89147324c0d1b2aa65e838c21f5`
- External version: `0.4.1`
- GPU allocations: `0`
- ComfyUI starts: `0`
- H3 enqueues: `0`

The external checkout was not updated, modified, vendored, or copied into this
repository.

## Authentication, project, region, and model

Application Default Credentials were available through the existing gcloud
authentication. The access token, ADC contents, credential paths, and secrets were
not printed or recorded. The configured values were:

- Vertex project: `gen-lang-client-0827827186`
- Vertex location: `global`
- Process-scoped ADC quota project: `gen-lang-client-0827827186`
- Google AI Studio/Gemini API keys: explicitly unset for every proxy, doctor, and
  compile process; none were used

The live Model Garden query returned the selected model among the current Gemini
catalog results:

```text
gcloud --project=gen-lang-client-0827827186 \
  --billing-project=gen-lang-client-0827827186 \
  ai model-garden models list --model-filter=gemini --limit=100
```

Selected exact Vertex model identifier:

`gemini-2.5-flash-lite`

Before LiteLLM was configured, a direct ADC-authenticated multimodal
`generateContent` request to the global Vertex endpoint returned HTTP 200 and `OK`
for the S02 PNG. The command used a process-only billing/quota override; gcloud
configuration was not changed.

Reference documentation checked: [LiteLLM Vertex AI provider
documentation](https://docs.litellm.ai/docs/providers/vertex), [Google Gemini model
catalog](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models), and
the [gcloud Model Garden list command](https://docs.cloud.google.com/sdk/gcloud/reference/ai/model-garden/models/list).

## Temporary adapter

The adapter was run as a foreground process, bound only to
`http://127.0.0.1:4000`, then stopped after the compile. No Docker service or
persistent service was created.

Runtime:

- `uv 0.12.4`
- LiteLLM environment: CPython `3.14.4`
- OpenH3-IR environment: CPython `3.12.3`
- `litellm==1.99.0`
- `google-auth==2.57.0` (the minimal optional Vertex ADC dependency LiteLLM needed)

Temporary config (`/tmp/cd45a-litellm.yaml`):

```yaml
model_list:
  - model_name: gemini-s02
    litellm_params:
      model: vertex_ai/gemini-2.5-flash-lite
      vertex_project: gen-lang-client-0827827186
      vertex_location: global

litellm_settings:
  drop_params: true
```

Process flags: `--host 127.0.0.1 --port 4000 --num_workers 1`.

Adapter gates:

| Check | Result |
|---|---|
| `GET /v1/models` | HTTP 200, valid JSON, model `gemini-s02` |
| text `POST /v1/chat/completions` | HTTP 200, `object=chat.completion`, reply `OK` |
| image+text `POST /v1/chat/completions` | HTTP 200, valid OpenAI-compatible response, reply `OK` |

## OpenH3-IR doctor

The pinned process used:

```text
H3IR_LLM_URL=http://127.0.0.1:4000/v1
H3IR_LLM_MODEL=gemini-s02
H3IR_LLM_KEY=local-cd45a
```

Doctor result:

- profile: `h3ir/2026-08-a`
- endpoint health: `True`, `/v1/models` HTTP 200
- recognized model: `gemini-s02`
- `chat_ok`: `True`
- `vision_ok`: `True`, `vision_reply: 473`
- ComfyUI probe: unreachable (`127.0.0.1:8188` connection refused); no ComfyUI
  process was started

## Exact S02 compile

Input intent, passed unchanged:

```text
Nora checks the time on her wristwatch, lowers her wrist, then looks screen-right down the quiet empty wet road with restrained concern and holds her gaze through the end of the shot.
```

Request:

- image: `outputs/the-last-bus/images/keyframes/s02-last-chance.png`
- image SHA-256: `37bdd9a3f1f34b2859afad9b9653fa364a39d6fda47e0f526053856b9f4e9ad5`
- role: first-frame anchor (`frame_anchor_first`)
- creativity: `restrained`
- requested duration: `5.17s`
- aspect: `16:9`
- compiler seed: `4102`
- analyzer cache: disabled for this proof (`use_cache=False`)

Result:

- presentation: `Animating your image`; `5.17 seconds`; `widescreen`; two
  planned shots
- inferred mode: `i2va`
- mode decision: `explicit-role`, confidence `1.0`
- task type: `keyframe completion`
- asset binding: slot `0`, `<Picture 1>`, SHA above, role
  `frame_anchor_first`, wiring `ref_image_1`, source pixels `1672x941`, sizing
  `match`
- effective target: `124` frames at `24` fps, `5.166666667s`, canvas `1344x768`
- source: `written`
- validator: `ok=True`, `0` errors, `1` warning
- warning: `H3-token-band` — 205 prompt tokens is below the published 350–1400
  distribution band; the validator labels this distribution drift, not a cost
  problem
- informational finding: `P5b-camera-no-amplitude`
- repair: `added the mandated i2va instruction line, which was absent; it is the
  first line of the prompt and carries the frame alignment`
- fix rounds: `0`
- IR prompt SHA-256: `de460eac726ac75b5c3a528fe77f9632fc2f3325628be56c36662a368e1e7342`
- serialized result JSON SHA-256:
  `d006f84cccd5a2c59b00e59f49a32bfca12d121d3f49d1969f526cb7426200a4`

The generated complete IR below is copied verbatim from the ignored result
artifact; it was not edited:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Live-action, cinematic, dim, ambient light from streetlights and the interior of the bus stop. The sky is dark blue. A medium shot frames the woman (dark wavy hair, dark eyes, medium build, wearing a yellow hooded jacket, wearing a black t-shirt, wearing a black backpack) as shown in <Picture 1>. She checks the time on her wristwatch, then lowers her wrist. The camera holds a static shot as she looks screen-right down the quiet, empty, wet road with restrained concern, holding her gaze through the end of the shot.

overall_soundscape: Steady rain taps against the glass shelter while distant traffic hums. The faint sound of her wristwatch strap moving against her jacket can be heard.

non_diegetic_music: N/A
```

The serialized deterministic plan is also retained verbatim in the result JSON.
It contains two internal planned ranges (`0.00–2.60s` and `2.60–5.1667s`) while
the written complete IR has one `[Shot 1]` description. This did not produce a
validator error, but is recorded for follow-up if a later milestone requires plan
and written-section shot counts to match exactly.

## Structural comparison with CD4.4 Composer

The CD4.4 Composer baseline is the original Composer V5.43.4 prompt recorded in
`CD4_4_REPORT.md`, SHA-256
`79fc85065b03a5b31526dab31caae92c6e332cf491ec568b709d955df8535258`.

| Structural property | CD4.4 Composer | OpenH3-IR complete output |
|---|---|---|
| Section shape | `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music` | anchor instruction, `integrated_multimodal_description`, `overall_soundscape`, `non_diegetic_music` |
| Approximate prompt size | 2,962 characters | 872 characters / 205 tokens |
| Reference treatment | `<Picture 1>` as storyboard reference plus retention analysis | `<Picture 1>` explicitly fully referenced at `0.00` as the first-frame anchor |
| Subject/environment detail | Separate `<Subject 1>` and `<Subject 2>` definitions | Image-grounded woman and shelter details embedded in the integrated description |
| Future-shot language | `bus arrival belongs to the next shot` | none |
| Engine language | `faint far-off engine near the final beat` | none |

OpenH3-IR wording audit:

| Requested audit item | Complete IR | Serialized plan / analysis | Conclusion |
|---|---|---|---|
| bus | `bus stop` | `bus stop shelter` | Yes, as the grounded environment label; no bus object or arrival is described |
| vehicle | no literal term | no literal `vehicle`; the plan says `car headlights` | No final-IR vehicle wording; a car concept exists only in the raw plan |
| headlights | none | `car headlights` in the first deterministic shot body | Not emitted by the complete written IR |
| engine | none | none | Not introduced |
| arrival | none | none | Not introduced |
| next-shot information | none | none | Not introduced |
| approaching traffic | none; only `distant traffic hums` | none | Not introduced |

Therefore, OpenH3-IR itself introduced the word **bus** only through the image-
grounded `bus stop` environment, and introduced **headlights** only in the raw
deterministic plan's `car headlights` description. The final written IR did not
introduce a bus, vehicle, headlights, engine, arrival, next-shot information, or
approaching traffic. No negative list was added to the request or generated IR.

## Commit scope

Only `CD4_5A_REPORT.md` is intended for commit. The generated IR and doctor
transcript remain ignored output artifacts. Pre-existing unrelated untracked files
were preserved.
