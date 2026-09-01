# CD4.5 — OpenH3-IR S02 comparison

## Result

Ponytail full mode was used. The experiment stopped before GPU allocation because the only
configured candidate LLM endpoint did not provide a usable OpenAI-compatible chat API. No OpenH3-IR
brief was compiled and no H3 generation was submitted. Decision: **D — OPENH3-IR CANNOT BE FAIRLY TESTED**.

## Provenance and scope

| Field | Recorded value |
|---|---|
| Starting branch | `codex/cd1-1-storyboard-original` |
| Starting commit | `6d77c3d85dfaabce3edb75546b974e7790392c89` |
| Upstream | [ruashots/open-h3-ir](https://github.com/ruashots/open-h3-ir) |
| OpenH3-IR commit | `fd031e136ae3d89147324c0d1b2aa65e838c21f5` |
| External checkout | `/home/karim/Tools/open-h3-ir` |
| OpenH3-IR version | `0.4.1` (`pyproject.toml`) |
| Execution method | Upstream CLI; `h3ir doctor` completed as far as endpoint compatibility allowed; compile was not reached |
| Inspected upstream files | `README.md`, `docs/calling-the-api.md`, `h3ir/cli.py`, `h3ir/config.py`, `h3ir/backend.py`, `h3ir/analyse.py`, `h3ir/compile.py`, `h3ir/plan.py`, `h3ir/render.py`, `pyproject.toml`, `requirements.txt` |

The upstream checkout remained clean and was not modified or vendored. Its temporary Python
environment was `/tmp/open-h3-ir-cd45-venv`.

## Endpoint qualification

| Field | Result |
|---|---|
| Endpoint type | Existing Codex-configured OpenCode API base, `https://api.opencode.ai/v1` |
| Credential | Existing bearer credential sent; value not recorded |
| Model identifier | `gpt-5.6-luna`, from `/home/karim/.codex/config.toml`; not confirmed as served by the endpoint |
| Model discovery | `GET /v1/models` returned HTTP 200 with plain-text `Not Found`, not a JSON model list |
| Doctor health | `True`, via `/v1/models` only because the endpoint used HTTP 200 for the error body |
| Doctor/image capability | `vision_ok` not reached. With the configured model, `h3ir doctor` failed while parsing `/v1/chat/completions`: HTTP 200 plain-text `Not Found`, not a JSON chat response |
| Local fallback check | No Ollama/vLLM/llama.cpp/LM Studio/ComfyUI listener was present on the checked local ports; no compatible local process was running |

OpenH3-IR's static qualification passed: `h3ir controls` reported `23 controls, 0 failing`, and
the upstream test suite reported `990 passed, 1 skipped, 1 warning`. The runtime blocker is the
LLM endpoint, not the upstream checkout.

## Intended S02 input

Exact intent:

> Nora checks the time on her wristwatch, lowers her wrist, then looks screen-right down the quiet empty wet road with restrained concern and holds her gaze through the end of the shot.

| Field | Recorded value |
|---|---|
| Input image | `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1/outputs/the-last-bus/images/keyframes/s02-last-chance.png` |
| Input image SHA-256 | `37bdd9a3f1f34b2859afad9b9653fa364a39d6fda47e0f526053856b9f4e9ad5` |
| Creativity | `restrained` |
| Intended compile wiring | One first-frame anchor via upstream CLI `--image ... --anchor` |
| Intended H3 mode | `i2va` (not inferred because compilation did not start) |
| Requested duration | `5.17s` |
| Effective duration/frame count | `5.166667s`, `124` frames at 24 FPS; verified by `h3ir budget --seconds 5.17 --aspect 16:9` |
| Compiled IR | Not produced; no path or hash |
| Validation/repairs | Target IR not reached; no deterministic repairs or target warnings |

The planned compile would have used the existing approved opening frame, the intent above only, and
no S03/future-arrival information beyond what the compiler itself might derive. No alternative prompt
generator was substituted.

## Pre-generation textual comparison

The manual and Composer entries below are the existing CD4.4 baseline. Prompt hashes: manual
`df7fd00ecaf09e74b5b1c1fab76ac70ccbd7ce938da3e63262721dc33c9fc77c`; Composer
`79fc85065b03a5b31526dab31caae92c6e332cf491ec568b709d955df8535258`.

| Semantic activation | Existing manual prompt | Existing original Composer prompt | OpenH3-IR |
|---|---|---|---|
| Bus | Yes, prohibited repeatedly; also says bus arrival belongs exclusively to next shot | Yes, through bus stop and “bus arrival belongs to the next shot” | Not produced |
| Vehicle | Yes, prohibited (`no vehicle approaching`, `no vehicle lights`) | No explicit vehicle term | Not produced |
| Headlights | Yes, prohibited repeatedly | No explicit headlights term | Not produced |
| Engine | Yes, faint far-off engine near final beat | Yes, faint far-off engine near final beat | Not produced |
| Arrival | Yes, as a prohibited arriving-bus/reflection concept | Yes, bus arrival assigned to next shot | Not produced |
| Next-shot information | Yes, explicit next-shot ownership | Yes, explicit next-shot ownership | Not produced |

This comparison is descriptive only; no prompt was rewritten.

## Generation and visual comparison

| Field | Result |
|---|---|
| Requested GPU | `L40S` |
| Actual GPU | None; no allocation attempt |
| ComfyUI startup | Not attempted |
| Graph validation | Not attempted |
| Generation time | N/A |
| OpenH3-IR output path/hash | None |
| Visual comparison | Not performed. CD4.4 remains the only visual baseline: manual bus/headlights around ~1s; Composer no bus but generic vehicle/lights around ~3–4s |
| Total new H3 generations | `0` |
| Model/checkpoint downloads | `0` |
| Production source changes | None |

No S02 OpenH3-IR take, S03 take, master assembly, or A/B regeneration was performed.

## Decision

**D — OPENH3-IR CANNOT BE FAIRLY TESTED.** The concrete blocker is that no already-available
OpenAI-compatible LLM endpoint with verified text and image capability was available to OpenH3-IR.
The requested L40S generation was therefore not attempted.

Only this report is intended for commit. Pre-existing unrelated untracked files in the worktree were
left untouched; OpenH3-IR was not integrated, vendored, or modified.
