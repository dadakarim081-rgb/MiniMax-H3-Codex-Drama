# CD1 — Codex Drama + original MiniMax H3 workflow

Date: 2026-08-31  
Decision: **C — ORCHESTRATION GOOD, WORKFLOW ADAPTER NEEDS MORE WORK**

CD1 stops here. No CD2, no generation, and no changes to the working
MiniMax project.

## Scope and safety

Ponytail full mode was confirmed. The investigation used the exact original UI
JSON; it did not reconstruct the graph and did not substitute Codex Drama's
stock R2V graph.

There was no `enqueue_workflow` call, no `/prompt` request, no sampling, no
MP4, no model download, and no modification of the remote ComfyUI install.
The Modal work was limited to starting the already-pinned runtime long enough
to read `/object_info` and check registrations/model discovery. The runtime
reported `generation_executed: false`, `prompt_queued: false`, and
`topology_unchanged: true`.

## Working pipeline protection

Protected repository: `/home/karim/Documents/minimax-h3-microdrama`

- HEAD before CD1: `edf02fd2cfb72872e33a4e4d83756d05ebc7935b`
- HEAD after CD1: same
- Tracked diff before and after: empty
- Original workflow SHA before and after:
  `f073053eabf87c43f867d7a8879d21a3286d80490a8d2c9f84b7f2ceb2e8ee23`
- `m8c/` was not edited, deleted, reset, or committed. Its existing files
  remained untracked throughout:

  ```text
  ?? m8c/M8C1_REPORT.md
  ?? m8c/M8C2_REPORT.md
  ?? m8c/M8C_REPORT.md
  ```

The recorded hashes of those three existing reports also remained unchanged:

```text
7e2a8d5c0409b8d5a9ac829ee5f1a27c25b52b131ecda078104cb2105959795d  m8c/M8C1_REPORT.md
b5da628f6bfd46978d97eda0cc8fa2f94195405c8c4d009afc38fd07fe5d3915  m8c/M8C2_REPORT.md
7843200c7b64d9340fcd22f1e21a260cf0bd6e92743e32eca41a7623934fee8e  m8c/M8C_REPORT.md
```

## Codex Drama checkout

- Isolated checkout: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`
- Upstream: `https://github.com/chiphoton/MiniMax-H3-Codex-Drama`
- Pinned commit: `db7afb07df6740ed37c79820d1e6ab96e5b73724`
- Commit subject: `v0.5.0: add official H3 style skills`
- Plugin version: `0.5.0`
- Bundled MCP: `comfyui-mcp@0.49.3`
- Repository state: detached HEAD, no fork, no push

Only this report is intentionally left untracked in the isolated checkout.
Temporary conversion/runtime probe files were removed.

## Stock skill limitation

The stock `skills/minimax-h3-comfyui/SKILL.md` explicitly selects only the
bundled T2V, I2V, and R2V standard/Turbo variants. It says to reject arbitrary
attached workflow JSON and that custom-workflow adaptation is deferred.

That restriction exists in both layers:

1. The skill is policy-limited to six manifest entries.
2. `scripts/prepare_workflow.py` loads only those manifest-selected API
   templates and patches declared paths for prompt, media, size, length, seed,
   models, sampling, and output. It has no arbitrary UI-graph adapter.

The root `.mcp.json` pins the companion server as:

```json
{"mcpServers":{"comfyui":{"command":"npx","args":["-y","comfyui-mcp@0.49.3","--comfyui-url","http://localhost:8188"]}}}
```

The underlying MCP is broader than the skill. The stock skill limitation is
therefore a skill/preparer policy boundary, not a general MCP capability
boundary.

## `comfyui-mcp@0.49.3` capability findings

Evidence was read from the pinned compiled implementation in
`/tmp/cd1-comfyui-mcp/package/dist/`.

| Capability | Finding |
|---|---|
| Arbitrary workflow support | Yes at tool level. `strip_workflow` accepts an absolute `path`, library `filename`, or inline `graph`; `query_workflow` accepts the same. |
| `get_workflow` | Reads saved ComfyUI user-library workflows; converts UI to API when requested. |
| `strip_workflow` | Reads ad-hoc server-side paths, resolves UI buses/reroutes/bypassed nodes, converts with live `/object_info`, and returns warnings plus a flat graph. This path was exercised for the original workflow. |
| `query_workflow` | Read-only targeted type/title/field/dependency queries over API or UI input. |
| `get_node_info` | Uses `/object_info`, with individual-node backfill when a node is absent from the bulk response. |
| `modify_workflow` | Mutates an API graph through `set_input`, `add_node`, `remove_node`, `connect`, and `insert_between`. It does not understand the original UI canvas itself and does not schema-validate operations. |
| `validate_workflow` | Checks node types, required top-level inputs, link references/output indices, classic combo values, self-links, and output presence. It is not a complete V3 dynamic-input/type validator. |
| Custom nodes | Supported when their live definitions are in `/object_info`; missing types are warned and skipped. The converter does not require a bundled template. |
| UI → API | Yes, using live definitions, with link resolution and known virtual-node/bypass handling. |
| `COMFY_DYNAMICCOMBO_V3` | Supported for selected-option nested widget values. |
| Dotted DynamicCombo fields | Supported for the tested `mode.megapixels` shape when the parent is present. |
| Dotted Autogrow fields | Not safely supported by this conversion path. The final dotted-key cleanup drops a child when its dynamic parent is absent from the flat API input map. This affects both H3 references and another required Autogrow input in this graph. |
| Linked inputs/types | Normal linked inputs and output indices survive. The converter uses object-info input/output definitions, but `validate_workflow` does not provide full static type compatibility checking. |
| Seed behavior | `workflow-executor.js` deep-copies a graph and replaces numeric `seed` and `noise_seed` values with `Math.floor(Math.random() * 2**32)` unless `disable_random_seed` is true. Future fixed-seed execution must pass `disable_random_seed: true`. |

This confirms the requested premise precisely: **the stock
`minimax-h3-comfyui` skill only chooses bundled workflows, while the underlying
MCP can operate arbitrary expert workflows in principle.** “In principle” is
important here: the generic converter is not yet faithful enough for this
particular V3/Autogrow graph.

## Original workflow experiment

Input:
`/home/karim/Documents/minimax-h3-microdrama/workflow/minimax_h3_r2v_story_board.json`

- SHA-256: `f073053eabf87c43f867d7a8879d21a3286d80490a8d2c9f84b7f2ceb2e8ee23`
- UI nodes: 36
- UI links: 45
- Subgraphs: 0
- `strip_workflow` API nodes: 33
- Skipped nodes: 3 — two UI-only `MarkdownNote` nodes and the intentionally
  bypassed node 1
- Required executable node classes otherwise survived; no required executable
  class silently disappeared

The real pinned runtime `/object_info` snapshot contained all 25 executable
classes requested from the original graph. The conversion was run twice, once
through the MCP `strip_workflow` handler and once directly through the same
pinned converter for targeted inspection. Both produced the same graph.

### Conversion warnings

The four warnings were:

1. Node 39 `model_name` was replaced with the first advertised option,
   `(place models in: /opt/ComfyUI/models/latent_upscale_models)`.
2. Node 39 `device` received the stale positional value `fp16` and was
   substituted with `cuda`.
3. Node 39 `precision` received the stale positional value `true` and was
   substituted with `fp32`.
4. Node 9's storyboard filename was absent from the connected server's
   `LoadImage` option list, so it was retained with a missing-asset warning.

There was no warning for the lost H3 reference child or lost
`ComfyMathExpression.values.a`; both were silent.

### Validation

Two validation checks were performed:

- The actual Modal runtime check loaded `/object_info`, confirmed node
  registration and model discovery, and returned no queued prompt or
  generation.
- The pinned MCP `validateWorkflow` was run on the converted API graph using
  that exact runtime `/object_info` payload. A local GET-only HTTP shim served
  the captured payload so the validator could run without touching the remote
  runtime. Its only request was `GET /object_info`; it made no `/prompt`
  request.

The converted graph result was:

```text
valid: false
summary: Workflow has 2 error(s) and 0 warning(s)
```

The errors were:

- node 9 `LoadImage.image`: the original storyboard asset is not installed in
  that runtime (`example.png` was the only advertised option)
- node 19 `ComfyMathExpression`: missing required top-level `values`, because
  its linked Autogrow child `values.a` was dropped

The validator did not detect the optional H3 storyboard reference loss or the
mis-mapped upscaler fields. This is a validator blind spot, not evidence of
semantic success.

## Critical topology and semantics

| Area | Original graph | Converted observation |
|---|---|---|
| Storyboard reference | node 9 `LoadImage` output 0 → node 11 `ref_images.ref_image_0` (`IMAGE`) | node 9 survived, but the dotted H3 child was absent from node 11; silent semantic loss |
| Standalone Audio1 | No source node exists; node 11 `ref_audios.ref_audio_0` is unconnected | Remained absent/unconnected. A future `LoadAudio` plus API `add_node`/`connect` can express it, but it was not part of this original graph validation |
| Paired video audio | node 11 `ref_video_audios.ref_video_audio_0` is unconnected | Remained unconnected; no automatic conversion into paired audio occurred |
| H3 prompt | node 2 `PrimitiveStringMultiline` → node 11 `prompt` | Link survived as `11.prompt: ["2", 0]` |
| Duration/sigma input | node 17 value 12 → node 19 `values.a` → node 19 output 1 → node 11 `length`; node 33 manual sigmas → first sampler; node 24 scheduler → node 13 `SplitSigmas` → refinement sampler | The ordinary duration source and expression survived, but required Autogrow `values.a` was dropped. Sigma links and literal sampler/scheduler values otherwise survived |
| AV split | refinement node 21 output 1 → node 35 `LTXVSeparateAVLatent.av_latent` | Link survived |
| Video-only upscale | node 35 `video_latent` → node 39 `latent`; node 39 output 0 → node 10 `video_latent` | Topology survived; node 39 widget semantics did not |
| Audio bypass | node 35 `audio_latent` output 1 → node 10 `audio_latent` | Link survived directly, without H3 paired-audio routing |
| AV recombine | node 10 `LTXVConcatAVLatent` output 0 → node 16 `latent_image` | Link survived |
| First sampler | node 16 receives noise 31, guider 32, sampler 18, sigmas 33, latent 10 | Links and `euler`/`simple` values survived; no sampler or scheduler warning/substitution |
| Refinement sampler | node 21 receives noise 31, guider 29, sampler 18, split sigmas 13, H3 latent output 1 | Links survived; no MODEL/SAMPLER output-index corruption was observed |
| Models/VAEs | H3 UNET, CLIP, video VAE, audio VAE names | Original names survived for these nodes; node 39's custom upscaler model selector was substituted as described above |
| Decoder/output | node 25 `VAEDecode` → node 42 `VHS_VideoCombine.images`; node 14 `VAEDecodeAudio` → node 42 `.audio` | Links survived. The original has no `SaveVideo` node; its final video writer is `VHS_VideoCombine` with `video/h264-mp4` |

### Latent upscaler and DynamicCombo

Original node 39 serialized its widgets in this UI order:

```text
[model_name, mode, mode.megapixels, align, device, precision, enable_chunking]
["minimax_h3_latent_upscaler_3d_fp16.safetensors", "megapixels", 1, 32,
 "cuda", "fp16", true]
```

The live V3 schema advertises the required order as:

```text
[latent, model_name, mode, align, enable_chunking, device, precision]
```

The converter correctly emitted the DynamicCombo representation:

```json
{
  "mode": "megapixels",
  "mode.megapixels": 1
}
```

That is the normalized representation observed in M8C.1. However, the same
positional conversion emitted:

```json
{
  "align": 32,
  "enable_chunking": "cuda",
  "device": "cuda",
  "precision": "fp32"
}
```

So the nested DynamicCombo itself survives, but the complete
`MinimaxH3LatentUpscaler3D` configuration does not. The live runtime's model
discovery found the selected upscaler file, but the converter only saw the
node's placeholder combo option and substituted it.

### Reference expressibility check

The existing MCP composer can represent the desired distinction after an API
graph exists. A read-only API mutation check produced the equivalent of:

```text
11.ref_images.ref_image_0       = ["9", 0]
201 = {class_type: "LoadAudio", inputs: {audio: "Audio1.wav"}}
11.ref_audios.ref_audio_0       = ["201", 0]
11.ref_video_audios.ref_video_audio_0 = absent/null
```

This proves the operation surface is sufficient to express storyboard image
plus standalone audio without turning it into paired video audio. It does not
repair the converter; the original conversion still loses the storyboard
child and the existing graph contains no Audio1 node.

## Semantic patch map for a future adapter

Only these fields should be mutable by default. Everything else should remain
frozen to the proven graph.

| Candidate | Location | Expected type | Ordinary/dynamic | Safe MCP treatment |
|---|---|---|---|---|
| Final prompt | Preferred: node 2 `PrimitiveStringMultiline.value`, `STRING`; it feeds node 11 `prompt` | STRING | Ordinary source, with an ordinary link into H3 | `set_input` on node 2 preserves topology. Directly setting node 11 `prompt` would replace its link and should not be the default. |
| Storyboard image | node 9 `LoadImage.image`, filename/COMBO; then node 11 `ref_images.ref_image_0`, `IMAGE` | IMAGE | Source widget ordinary; H3 child Autogrow/dotted | Upload/resolve the filename, then explicitly connect the H3 child. Current UI conversion does not preserve that child safely. |
| Audio1 standalone reference | Future node `LoadAudio.audio`, filename/COMBO; then node 11 `ref_audios.ref_audio_0`, `AUDIO` | AUDIO | Source ordinary; H3 child Autogrow/dotted | `add_node` + `connect` is expressible. Never write `ref_video_audios.ref_video_audio_0` for this use. |
| Seed | node 31 `RandomNoise.noise_seed`, `INT` | INT | Ordinary widget with runtime randomization policy | Set explicitly and later call enqueue with `disable_random_seed: true`; otherwise the MCP randomizes it. |
| Output prefix | node 42 `VHS_VideoCombine.filename_prefix`, `STRING` | STRING | Ordinary name-keyed widget | Safe `set_input`; preserve the final `VHS_VideoCombine` node. |
| Duration | node 17 `PrimitiveFloat.value`, `FLOAT`, feeding node 19 `values.a`; H3 `node 11.length` is a linked `INT` expression result | FLOAT → INT | Source ordinary, middle Autogrow/dotted, H3 link | Freeze by default. Directly patching node 11 length overrides the proven expression; changing node 17 is preferable only after the Autogrow conversion issue is fixed and validated. |

The upscaler mode, model, alignment, device, precision, chunking, model
names, VAEs, sampler, scheduler, sigma lists, and graph topology should remain
frozen in the first adapter.

## Producer/orchestration evaluation

The producer skill is useful as an orchestration shell, especially for:

- safe project initialization and resume behavior
- input hashing, roles, and provenance
- append-only stage/job/artifact/take bookkeeping
- prompt IDs, selected-take tracking, and stable selected copies
- declarative FFmpeg assembly and audio mixing
- technical QC, contact sheets, and a human visual-QC record

The bundled producer script checks passed: `10 passed`.

For a one-workflow micro-drama, it is also heavier than necessary:

- initialization creates roughly 30 directories and a broad project contract
- the full guided path has many stage statuses and mandatory approval/visual
  lock gates
- profile resolution, entity/character ledgers, visual development, asset
  roles, and continuity documents can cost substantial tool calls for a single
  storyboard and a single finished prompt
- profile, state, artifact, and event schemas overlap enough to create
  maintenance burden
- human contact-sheet approval is valuable for production, but should not be a
  hard gate for every exploratory take

The likely later simplification is a thin profile plus project state, shot/take
ledger, selected-artifact tracking, and the existing assembly/QC path. Keep the
full entity/continuity/visual-lock machinery when a project actually has
multiple shots, recurring characters, or human approval requirements.

The external `h3-storyboard` skill fits the planning/shot-list stage. The
external MiniMax H3 Prompt Composer fits the prompt-authority stage. They
should remain external. The stock H3 skill's `[prompt_enhance=false]` path
preserves the supplied finished prompt; enhancement is opt-in, so Codex Drama
can pass the final Prompt Composer string without a silent rewrite.

## Minimal adaptation assessment

No adapter was implemented because the “MCP successfully understands the
original workflow” condition is false.

The smallest future design is still plausible:

1. Add one explicit `storyboard-original` route to the producer-to-H3 handoff.
2. Resolve the external original UI workflow by configured path plus expected
   SHA-256; fail closed on a mismatch.
3. Use `strip_workflow`/the existing MCP conversion and a small, route-specific
   repair for V3 Autogrow links and the legacy node 39 widget order.
4. Apply only the allowlisted semantic patches above, validate against live
   `/object_info`, and retain `disable_random_seed: true` for fixed-seed runs.

That is a route-specific adapter, not a generic arbitrary-workflow framework.
It should not rewrite `prepare_workflow.py`, vendor `comfyui-mcp`, copy the
microdrama project, or modify either external prompt skill.

Deliberately unchanged in CD1: `minimax-h3-microdrama`, `modal/app.py`, the
original workflow JSON, Codex Drama's tracked source, the producer, the stock
manifest/preparer, H3 storyboard, Prompt Composer, Turbo/Larry integration,
and all generation behavior.

## Final repository state

Codex Drama checkout:

```text
HEAD db7afb07df6740ed37c79820d1e6ab96e5b73724 (detached; no branch)
?? CD1_REPORT.md
```

No commit was created because no meaningful source adaptation was safe to
ship. Nothing was pushed.

## Decision

**C — ORCHESTRATION GOOD, WORKFLOW ADAPTER NEEDS MORE WORK.**

The producer has useful resumability, provenance, take tracking, assembly,
and QC primitives. The MCP has the required arbitrary-workflow surface, but
the pinned conversion is not semantically faithful for this graph: it drops
Autogrow links silently and mis-maps the upscaler's legacy widget order. A
`storyboard-original` route should wait for that small adapter/repair to be
proven against the runtime.
