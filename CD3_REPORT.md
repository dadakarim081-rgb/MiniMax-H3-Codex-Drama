# CD3 — native Codex Drama visual-development proof

Date: 2026-08-31

Decision: **A — NATIVE CODEX DRAMA ASSET PIPELINE PASSES**

## Scope and controls

- Ponytail full mode: confirmed.
- Starting commit: `168b56a7efe4cc0eefb3334908d5002461c77eae`
- Branch: `codex/cd1-1-storyboard-original`
- Producer mode: `fast` (the task supplied a complete brief and requested
  immediate execution).
- Resolved profile: `base-video` 1.0.0. This was selected because the brief is
  a quiet observational three-shot story; the available TikTok profile is
  vertical, hook-first, caption-heavy, and explicitly excludes slow
  observational film.
- Project directory:
  `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1/outputs/the-last-bus`
- Protected repository was not touched:
  `/home/karim/Documents/minimax-h3-microdrama`

This milestone used only the Producer's project/state machinery and the
native Codex built-in `image_gen` / GPT-Image path. No external image service,
CLI image fallback, ComfyUI, Modal, MCP connector, MiniMax H3 call, T2V/I2V/R2V
workflow, or video generation was used.

## Planning

The project records the minimal Producer plan:

- `planning/production-brief.md`
- `planning/story.md`
- `planning/entities.md`
- `planning/asset-ledger.yaml`
- `planning/continuity.yaml`
- `planning/shot-list.yaml`
- `planning/budget.yaml`

The story remains one recurring character, one bus-stop environment, and three
shots: waiting, concern/time-check, and arrival/relief. All three first-frame
keyframes were justified because each shot has a distinct composition and
continuity-sensitive opening state. No end frames or overhead companion view
were needed; the simple shelter/road layout is already spatially legible.

## Imagegen calls

There were 8 imagegen tool invocations:

- 7 completed image outputs;
- 1 aborted zero-byte S03 attempt, not accepted or staged;
- 6 final accepted assets.

The only correction was one targeted edit to the first scene output: it had
placed Nora twice to illustrate two legal positions. The edit removed the
duplicate and preserved the shelter, bench, road, lighting, and camera
geometry. No Producer source code, generator, abstraction, or test was added.

Prompt records are in `prompts/gpt-image/01-...` through `06-...`. Later
assets were generated with the approved character master, scene master, and
storyboard as bounded references rather than independently redesigned.

## Final asset paths and hashes

| Asset | Project path | Dimensions | SHA-256 |
|---|---|---:|---|
| Nora character master | `images/entity-sheets/nora-character-master.png` | 1536×1024 | `08237ad1603fffac8e3131d93e672aec78149e82ca1db77b8dd6ba4072ecfedc` |
| Bus-stop scene master | `images/scenes/bus-stop-scene-master.png` | 1672×941 | `8dd5507fb524209885bbca21f63e5f679dc3ae5faef26fa34c75a86f8b5cf310` |
| Three-shot storyboard | `images/storyboards/the-last-bus-storyboard.png` | 1536×1024 | `1f9af3a5d0f1ee4965045d2dd6ad34afaa1b813e93c7eae949377470bfd0c7e9` |
| S01 waiting keyframe | `images/keyframes/s01-waiting.png` | 1672×941 | `c073179d111f29634fe397892cb414be906122c1bee9267a3b2321020038ee19` |
| S02 last-chance keyframe | `images/keyframes/s02-last-chance.png` | 1672×941 | `37bdd9a3f1f34b2859afad9b9653fa364a39d6fda47e0f526053856b9f4e9ad5` |
| S03 arrival-relief keyframe | `images/keyframes/s03-arrival-relief.png` | 1672×941 | `583a0e5375dea44b630befc8ee73bbd75ec2376e8851e31bdc54a9fe724918b1` |

The keyframes are single full-frame landscape images at the intended 16:9
composition (the native raster is 1672×941, a rounding-level aspect
approximation). None is a collage, panel sheet, labeled frame, or end frame.

## Visual consistency assessment

### Character identity and wardrobe

The character master contains four full-body diagnostic views and three close
views covering neutral, concern/time-check, and relief. Nora remains one adult
woman with the same dark shoulder-length wavy hair, face, late-twenties age,
body proportions, mustard-yellow raincoat, dark clothes, black ankle boots,
and small black backpack. The storyboard and all three keyframes visibly
inherit that identity and wardrobe. No duplicate body parts, extra limbs, or
second Nora appears in the accepted assets.

### Environment and props

The accepted scene master establishes one glass-and-metal shelter, one bench,
one road directly in front, wet reflective pavement, neutral buildings, cool
blue ambient dusk, and warm shelter practical light. The storyboard and
keyframes preserve the broad shelter/bench/road relationship and screen-right
road direction. S03 adds only one generic unbranded bus and its headlights;
there are no readable route numbers, advertising, or brand names. Minor
background and perspective variation is normal stochastic imagegen drift, not
a continuity-breaking layout change.

### Storyboard quality

The storyboard is a readable three-panel sequence: wide waiting, medium-close
time-check/concern, and medium-wide arrival/relief. It has clear actions,
useful compositions, a coherent emotional progression, one Nora per panel,
and no baked text contamination. It is sufficient as a practical handoff to a
later three-shot H3 plan.

### Keyframe usability

- S01 is a literal wide opening frame with Nora waiting under the shelter;
  there is no premature bus or headlight cue.
- S02 is a literal medium-close opening frame with a readable plain watch
  check, restrained concern, and the road still present in depth.
- S03 is a literal medium-wide opening frame with one bus, visible headlights,
  Nora's relief, and the beginning of the curbward step.

All three are production-usable first-frame candidates. They preserve the
scene axis, lighting direction, wardrobe, and action intent well enough for a
later micro-drama generation pass. Pixel-perfect identity was not required;
the observed consistency is realistically sufficient.

## Producer workflow evaluation

The native workflow was practical. The dependency order—character master,
scene master, storyboard, then keyframes—made the source of truth explicit and
prevented independent redesign of later assets. The character sheet was a
useful diagnostic anchor, and the scene master was genuinely useful for
shelter geometry, road axis, lighting, and legal positions.

Codex needed one targeted intervention after inspection: remove the duplicate
Nora from the first scene draft. No parallel orchestration or source change was
needed. The structured planning documents and visual-lock record were useful
for this continuity-sensitive proof; no excessive approval gate, framework, or
extra environment was created. The only missing capability relevant to this
milestone is a deterministic exact-aspect output control in the built-in
imagegen path; the native 1672×941 frames are effectively 16:9 and usable.

Another image backend is not needed based on this run. It would be justified
only if later work shows repeatable identity or environment drift that the
existing master-reference workflow cannot correct.

## Generation and repository state

- H3 generation count: **0**.
- Shot-generation stage: not entered.
- Modal/ComfyUI: not started.
- CD1, CD1.1, and CD2 execution work: unchanged.
- Generated images and project state remain under the ignored normal project
  directory; generated images were not added to Git.
- Tracked source changes: none.
- Tracked CD3 artifact: this report only.
- The target checkout retains untracked `__pycache__/`,
  `cd2_modal_bridge.py`, and the Producer script cache; none was staged.
- The protected checkout retains only its pre-existing untracked `m8c/`
  directory; it was not modified.

The final report commit SHA and push result are recorded in the task handoff
because a commit cannot embed its own content hash. The requested push target
is the authenticated fork:

`https://github.com/dadakarim081-rgb/MiniMax-H3-Codex-Drama`

Branch: `codex/cd1-1-storyboard-original`

Stop after CD3. Do not start H3 generation or CD4.

## Decision

**A — NATIVE CODEX DRAMA ASSET PIPELINE PASSES.**
