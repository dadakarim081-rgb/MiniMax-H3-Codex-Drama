# CD5 — Production H3 Architecture and Routing Policy

Status: frozen for MiniMax-H3-Codex-Drama

This document is the production source of truth for ownership, shot control,
H3 routing, escalation, prompt writing, and GPU selection. It reconciles the
CD4 experiments without changing the Producer or adding a routing service.

## Ownership

The Codex Drama Producer remains the main director and orchestrator. It owns:

- story and script ingestion;
- character masters and scene masters;
- continuity, shot decomposition, and shot contracts;
- deciding which references a shot needs;
- deciding whether a storyboard is necessary;
- choosing the H3 route and generation backend;
- retry and escalation policy;
- take selection, assembly, and technical and visual QC.

Prompt Composer, OpenH3-IR, ComfyUI, and the storyboard skill do not own these
decisions.

## Storyboard policy

Storyboards are optional. The Producer decides per shot whether one is useful.

Default to no storyboard for:

- one simple visual beat;
- a simple reaction or performance;
- a shot whose approved opening frame is sufficient;
- a shot whose approved opening and ending frames are sufficient.

Use a storyboard when multiple ordered visual beats require spatial blocking or
choreography, or when a complicated reference-driven sequence cannot be
adequately controlled with I2V or first+last-frame control. The Producer may
escalate to a storyboard only after a concrete simpler-route failure. Do not
force every shot through a six-panel storyboard.

The external `h3-storyboard` skill creates the storyboard after the Producer
chooses this route. It does not choose routes, models, Producer state, or final
H3 prompt policy.

## Route hierarchy

The Producer selects the least constrained route that can satisfy the shot:

| Route | Select when | Native H3 control |
|---|---|---|
| T2V | No image, video, or audio reference must control the result | Text-only FL2VA generation |
| I2V | An approved image must be the exact opening frame | FL2VA/I2V with one first frame |
| first+last | Both opening and ending compositions materially matter | FL2VA/I2V with exact first and last frames |
| R2V | Identity, style, location, motion, camera, performance, or other reference relationships matter more than literal endpoints | Native REF2VA/reference conditioning |
| storyboard-original | A complex storyboard/reference-driven shot has multiple ordered visual beats | Ref2VA/R2V only; pinned `storyboard-original` route |
| Editor | An existing clip needs a localized change while other content remains stable | Reference-conditioned regeneration through the editor/R2V path |

`storyboard-original` is not a general-purpose I2V or first+last route. Keep it
Ref2VA/R2V only. An existing clip edit is not pixel-stable source editing; it is
localized reference-conditioned regeneration with explicit preservation rules.

## Escalation

Use this sequence when the current route cannot satisfy a concrete shot gate:

```text
T2V
  ↓ exact opening control required
I2V
  ↓ ending composition cannot be controlled
first+last
  ↓ ordered choreography/reference structure remains inadequate
storyboard / Ref2VA
```

Escalate the conditioning or control mechanism. Do not respond to structural
failures by endlessly adding negative prompt terms, changing seeds, increasing
prompt length, or switching prompt systems.

## Prompt path

The preferred current H3 prompt-writing path is the original external Prompt
Composer checkout:

`/home/karim/Tools/minimax-h3-prompt-composer`

Keep it external and use the existing headless execution path with the original
Composer logic unchanged. CD4.4 used the pinned checkout at commit
`0548331876476934a081927017041bcc2bedab81` (`H3 Prompt Composer V5.43.4`). The
Producer supplies an approved shot contract and reference-role set; Composer
writes the H3 prompt. Composer does not decide the route, storyboard usage,
model, GPU, retry policy, or take selection.

CD4.4 and CD4.5B provide the current choice: the manual prompt produced unwanted
bus/headlights at about one second, OpenH3-IR produced generic traffic/taillights
at about one second, and Composer delayed comparable unwanted traffic until
about three to four seconds. Composer is therefore preferred for production
prompt writing.

## OpenH3-IR status

OpenH3-IR is researched and parked, not production.

The pinned external checkout is `/home/karim/Tools/open-h3-ir`, version `0.4.1`,
at commit `fd031e136ae3d89147324c0d1b2aa65e838c21f5`. Keep it external and
unmodified.

Proven in CD4.5A:

- pinned external OpenH3-IR `0.4.1` works;
- Vertex Gemini through a temporary LiteLLM adapter works;
- a valid I2VA Context-IR can be produced.

CD4.5B then compiled the exact S02 prompt through A100-80GB. Its generic
vehicle/red-taillight cue appeared about two seconds earlier than Composer's,
so Composer remains better for this production constraint.

Do not integrate OpenH3-IR, vendor or copy its source, add LiteLLM as a
production dependency, or delete the CD4.5A/CD4.5B reports. Keep the findings
for a separately authorized future reevaluation.

## H3 backend defaults

The preferred FL2VA production checkpoint is:

`10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors`

Use the appropriate native H3 mode for the selected route. Do not substitute an
FL2VA checkpoint for a REF2VA route or vice versa. For the preferred beta4
checkpoint, the tested production defaults are:

- sampler: `euler`;
- scheduler: `simple`;
- steps: `8`;
- no Larry Turbo LoRA;
- no other LoRA by default.

Do not delete official H3 checkpoints; they remain fallback and reference assets.
The standalone ComfyUI skill may still expose Turbo as an explicit capability,
but the Producer's CD5 production path must select native beta4 without Larry
Turbo stacking.

## GPU policy

GPU selection is explicit:

1. preferred: `L40S`;
2. capacity fallback: `A100-80GB`.

The Producer must not silently change GPU type. `A100-40GB` is not part of the
production policy and may only be evaluated in a separate cost/VRAM experiment.
CD4.5B established A100-80GB as the proven fallback after two L40S scheduling
failures.

## Latent upscale/refinement

The original two-stage H3 latent upscale/refinement technique is promising but
not production-default across routes. Conceptually it remains:

```text
Producer route
     ↓
10Eros H3 generation
     ↓
optional latent upscale/refinement
     ↓
decode
```

Do not integrate or generalize it in CD5. It needs its own controlled proof.

## Frozen architecture

```text
Story / Script
      ↓
Codex Drama Producer
      ↓
character + scene masters
      ↓
shot contracts / continuity
      ↓
Producer decides required control
      │
      ├─ no controlling image → T2V
      ├─ exact opening → I2V
      ├─ exact opening + ending → first+last
      ├─ identity/reference → R2V
      ├─ complex ordered beats → storyboard-original
      └─ existing clip modification → editor
      ↓
external Prompt Composer
      ↓
10Eros H3 / ComfyUI
      ↓
Producer QC
      ↓
accept OR escalate conditioning
      ↓
assembly / audio / captions / final QC
```

For the storyboard branch:

```text
Producer determines storyboard is needed
      ↓
external h3-storyboard skill
      ↓
approved storyboard
      ↓
external Prompt Composer
      ↓
10Eros Ref2VA storyboard-original
```

## Boundaries and implementation

CD5 does not add a router class, service, workflow DSL, dependency injection,
or new production dependency. The existing Producer remains the orchestrator;
its per-shot route metadata and existing sibling skills remain the execution
boundary. This policy document makes the decisions explicit without changing
runtime routing behavior.

## What remains unproven

- Reliable L40S capacity and scheduling latency; it remains preferred but failed
  two bounded CD4.5B allocation attempts.
- Latent upscale/refinement as a controlled, repeatable production stage across
  routes.
- OpenH3-IR performance outside the tested S02 comparison; it remains parked.
- Broad visual generalization of Composer-versus-OpenH3-IR results beyond S02.
- A cost/VRAM decision for A100-40GB.
- Whether complex storyboard-original shots need further route-specific QC after
  their existing structural proof.

See [CD4.4](CD4_4_REPORT.md), [CD4.5A](CD4_5A_REPORT.md), and
[CD4.5B](CD4_5B_REPORT.md) for the evidence this policy freezes.
