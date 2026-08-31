# S02 prompt A/B — CD4.4

## Conclusion

The Composer prompt is better for S02 temporal and scene compliance: it shows no bus during the 5.17-second take, while the manual prompt produces a bus with bright headlights by about 1 second. Neither take passes the strict empty-road rule: the Composer take still introduces a generic vehicle and lights around 3–4 seconds. Nora consistency is a near tie, with a slight Composer edge in the observed hand/face motion. This is one controlled take per arm, so the result is directional rather than statistical.

Ponytail full mode was used. No S01/S03 generation or master assembly was performed.

## Composer path and provenance

The original Composer is `/home/karim/Tools/minimax-h3-prompt-composer/Prompt_Composer.html`, locked at git commit `0548331876476934a081927017041bcc2bedab81` (`H3 Prompt Composer V5.43.4`). The exact headless path used was:

```text
/home/karim/Documents/minimax-h3-microdrama/tools/prompt_composer_headless.mjs
  -> previewAIImport()
  -> applyAIImport()
  -> aiImportToState()
  -> projectToAIInterchange()
  -> build()
  -> lint()
```

Within `Prompt_Composer.html`, `build()` at line 5157 routes the imported shot through `shotText()` (line 4524), `definitionFor()` (line 4707), and the retention helpers before returning the `REF` prompt. The import state path is `previewAIImport()` line 9096, `aiImportToState()` line 9112, `applyAIImport()` line 9147, and `projectToAIInterchange()` line 9157.

The target repo had no saved Nora-specific historical Composer fixture or output. To make the comparison reproducible, an equivalent one-shot `REF` import was created from the committed S02 shot contract and passed through the original Composer unchanged. Composer returned one shot with no blocking errors; its only warnings were the expected canonical-subject-name and unattached-environment-source-view warnings. The generic six-shot headless acceptance predicate was not applicable to this one-shot comparison.

## Controls

| Control | Both arms |
|---|---|
| Weight | `10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors` |
| Workflow | Native `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1/skills/minimax-h3-comfyui/assets/workflows/i2v.api.json` |
| Sampler / scheduler | `euler` / `simple` |
| Steps / denoise / seed | `8` / `1.0` / `4102` |
| Size / frames / FPS | `1344x768` / `124` / `24` |
| First frame | `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1/outputs/the-last-bus/images/keyframes/s02-last-chance.png` |
| Last frame | None present for either arm |
| LoRA / service | None; one temporary local ComfyUI process on one A100-80GB |
| Enqueues | Exactly two: one manual, one Composer |

The first-frame SHA-256 was `37bdd9a3f1f34b2859afad9b9653fa364a39d6fda47e0f526053856b9f4e9ad5`. The beta4 checkpoint was already present in the persistent volume at the pinned 20,967,637,320-byte size; no model download occurred.

## Outputs

| Arm | Output | Prompt SHA-256 |
|---|---|---|
| Manual | `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1/outputs/the-last-bus/clips/cd4-4-ab/S02-i2v-10eros-manual.mp4` | `df7fd00ecaf09e74b5b1c1fab76ac70ccbd7ce938da3e63262721dc33c9fc77c` |
| Composer | `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1/outputs/the-last-bus/clips/cd4-4-ab/S02-i2v-10eros-composer.mp4` | `79fc85065b03a5b31526dab31caae92c6e332cf491ec568b709d955df8535258` |

Both outputs decoded successfully and are 1344×768, 124 frames, 24 FPS, 5.166667 seconds, H.264/AAC. Output SHA-256 values:

```text
manual:   099833ea68ceb4a33fc5fdc4c9a44f5652f78f2be841f5a90dde9a4248a20f6e
composer: 2ff8ca56ee33499f6236ca5cedddc083e4df2363f8485372b7b4b51b5bb19484
```

## Evaluation

| Criterion | Manual | Composer |
|---|---|---|
| Bus timing | A faint road vehicle is already visible in the opening sample; a recognizable bus with bright headlights is clear by about 1 second and grows through the shot. | No bus through the end sample at about 5 seconds. A generic car/vehicle with red/white lights appears around 3–4 seconds. |
| Nora consistency | Recognizable Nora, stable yellow raincoat, hair, face, backpack, and shelter; expression changes toward worry with modest motion variation. | Recognizable Nora with stable identity, wardrobe, backpack, and shelter; hand/face motion is slightly cleaner in this take. |
| Visual quality | Clean decode and readable arrival, but the bus dominates and a bright route/destination-like panel appears. | Clean, stable blue-hour shelter and wet-road rendering; the late car/lights are the main defect. |
| Scene compliance | Fails: bus, headlights, vehicle motion, and bus-like text/panel violate S02's empty-road/no-arrival contract. | Better but still fails the strict gate: no bus appears, but a generic vehicle and headlights enter before the end. |

## Wording differences and temporal risk

- The manual prompt is a compact exact-opening-frame instruction with explicit `0–1`, `1–2.5`, and `2.5–5` timing, followed by repeated hard negatives for bus, vehicle, headlights, and reflections.
- The Composer prompt is a 2,961-character structured `REF` prompt: subject definitions, environment definition, storyboard-reference definition, retention analysis, then detailed shot/camera/action/audio text. It does not explicitly say “use the supplied image as the exact opening frame.”
- The manual prompt mentions the prohibited arrival vocabulary early and repeatedly: `do not show the bus or headlights`, then `no bus, no vehicle approaching, no headlights, no vehicle lights`, plus `arriving bus` in the reflection prohibition. It also mentions a `faint far-off engine near the final beat`.
- The Composer prompt mentions `bus arrival belongs to the next shot` only in the Picture 1 definition and mentions a `faint far-off engine near the final beat` in sound. It has no explicit `headlights` term and no explicit throughout-shot `no vehicle` prohibition.

For H3 temporal compliance, the manual prompt has stronger stated timing and negatives, but this take appears to have activated the arrival concept anyway. The Composer prompt's structured continuity and reference framing delayed the bus beyond the shot, but its weaker vehicle/headlight exclusion allowed a smaller substitute arrival cue. For this S02 repair, the Composer wording is the better base; it still needs the manual prompt's empty-road constraint if used in production.

## Exact prompts

### Current manual prompt

Source: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1/outputs/the-last-bus/prompts/minimax-h3/s02-i2v-turbo.md`

```text
Use the supplied image as the exact opening frame.

PRESERVE: one Nora only; the same late-twenties woman, same face, shoulder-length dark wavy hair, mustard-yellow raincoat, dark clothes, black ankle boots, and small black backpack; preserve the same glass-and-metal shelter, bench, wet road, cool blue-hour ambient light, warm shelter practical, and screen-right road axis from the opening frame.

MOTION PATH: 0-1 second, hold the opening composition; 1-2.5 seconds, Nora naturally checks the time on the plain wristwatch at her wrist; 2.5-5 seconds, she lowers her wrist and looks screen-right down the wet road with restrained, readable concern, then holds that gaze as the camera makes only a slight stable eye-level settle.

CAMERA AND LOOK: restrained cinematic live action, stable eye-level medium close-up with the shelter and road readable in depth, physically plausible hand and eye motion, same blue-hour/warm-practical direction, no axis flip, no new location.

AUDIO: restrained rain-wet street ambience, distant traffic, and a faint far-off engine near the final beat; no dialogue and no music.

CONSTRAINTS: no abrupt cut or morph, no duplicate Nora, no face, hair, wardrobe, backpack, shelter, bench, road, or geometry drift, no text, logos, or route numbers, no extra limbs or fingers, do not show the bus or headlights, and preserve the concerned screen-right gaze at the end.

ADDITIONAL CONSTRAINTS FOR THIS REPAIR: During the entire S02 shot there is no bus, no vehicle approaching, no headlights, no vehicle lights, no bus silhouette, no large moving vehicle, and no reflection suggesting an arriving bus anywhere in frame. The road remains visibly empty throughout; the bus arrival belongs exclusively to the next shot.
```

### Composer-generated prompt

Source: original Composer V5.43.4 via the headless path above; generated from the equivalent S02 import described in the provenance section.

```text
subject_definitions:
<Subject 1> is Nora, an adult woman in her late twenties with shoulder-length dark wavy hair, a mustard-yellow raincoat over dark clothes, black ankle boots, and a small black backpack.
<Subject 2> is the bus stop, described as one modern urban glass-and-metal bus shelter at blue hour after light rain, with one bench, wet reflective pavement, and a road directly in front.
<Picture 1> is a storyboard reference for [Shot 1], defining shot order, viewpoint, framing, blocking, action direction, and timing; annotations and rough-composite artifacts are planning only; the S02 storyboard beat is a medium close-up in the same shelter: Nora checks the time, then looks screen-right down the road with concern. Preserve the established shot order, road axis, and blue-hour/warm-practical continuity; the bus arrival belongs to the next shot.

summary:
[reference generation] Nora checks the time, then looks down the road with concern.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - Nora's complete defined identity and body proportions are preserved.
<Subject 2> (appears in [Shot 1]): fully_preserved - the environment’s defined architecture, layout, and spatial continuity are retained.
<Picture 1> (storyboard reference for [Shot 1]): fully_preserved - the assigned storyboard reference relationship is retained.

detailed_description:
The target video is presented with Live-action cinematic blue-hour realism with restrained color and consistent cool ambient light plus warm shelter practical.
[Shot 1] The shot takes place in <Subject 2>. At first appearance, <Subject 2> matches the complete defined environment identity, architecture, layout, and reference lighting. Follow the shot planning in <Picture 1>. At first appearance, <Subject 1> (Nora) matches the complete defined identity and physical appearance: An adult woman in her late twenties with shoulder-length dark wavy hair, a mustard-yellow raincoat over dark clothes, black ankle boots and a small black backpack. Nora is already inside the same glass-and-metal shelter, with the bench and wet road readable behind her, her small black backpack present, and her plain wristwatch visible at her raised wrist. The described action controls subject movement. The Camera instructions change only the camera. The camera follows its own path through the location. Camera: begin with a medium close-up at eye level, with the camera directly in front of <Subject 1>. Nora naturally checks the time on the plain wristwatch at her wrist, lowers her wrist, and looks screen-right down the wet road with restrained, readable concern, then holds that gaze. Hold the camera at the established position. Rain-wet street ambience, distant traffic, and a faint far-off engine only near the final beat can be heard.

overall_soundscape:
Restrained rain-wet street ambience, distant traffic, and a faint far-off engine near the final beat.

non_diegetic_music:
N/A
```

## Commit scope

Only this report is intended for commit. The A/B MP4s and contact sheets remain in the ignored output path; the temporary Composer fixture and A/B runner are not part of the change. No source behavior was changed.
