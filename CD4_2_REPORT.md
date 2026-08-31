# CD4.2 — repair S02/S03 visual prompt violations and finish The Last Bus

Date: 2026-08-31
Decision: **B — S02 REMAINS VISUALLY NONCOMPLIANT**

## Scope and locked baseline

- Ponytail: full mode.
- Repository: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`.
- Branch: `codex/cd1-1-storyboard-original`.
- Starting commit: `d30f4cf` (`docs: record CD4.1 visual gate`).
- This was one narrow visual-repair continuation, not a new production run.
- S01 was reused exactly and never regenerated, altered, replaced, or re-scored:
  - `outputs/the-last-bus/clips/cd4-1/S01-i2v-turbo.mp4`
  - SHA-256: `9471f3da372163b3e2ffe863f28bc3090386f1955be3c67c41412e0c02be2077`
- Existing CD3/CD4 assets, keyframes, routes, Turbo workflows, models, compiler fix, and Producer state were reused.
- Prepared workflow files were unchanged:
  - S02 SHA-256: `d5aa33bcc6c730425f725aabf36fec5d4c9446f2574978379dcf36ada8bd434a`
  - S03 SHA-256: `f078dc9fc16727d7c306ad2d4d84047cf3b22ea559cd6269aa6dbb7e7499258f`

## Minimal prompt repair

The only creative input change was appending the following blocks to the existing prompt files. The runner loaded each updated prompt into an in-memory copy of the existing `MiniMaxH3ImageToVideo` node; it did not rewrite the prepared workflow files.

### S02 addition

```text
ADDITIONAL CONSTRAINTS FOR THIS REPAIR: During the entire S02 shot there is no bus, no vehicle approaching, no headlights, no vehicle lights, no bus silhouette, no large moving vehicle, and no reflection suggesting an arriving bus anywhere in frame. The road remains visibly empty throughout; the bus arrival belongs exclusively to the next shot.
```

### S03 addition

```text
ADDITIONAL CONSTRAINTS FOR THIS REPAIR: The arriving bus is completely generic and unbranded. It contains absolutely no readable text, route number, destination number, destination board, logo, brand mark, lettering, advertisement, decal, signage, symbols resembling text, or readable license plate anywhere on the vehicle. Any display panel is blank/dark and contains no characters.
```

The S03 prompt was repaired in the same narrow way but was not submitted because S02 remained noncompliant after its two allowed takes.

## Modal/runtime

- Architecture: one Modal function → local ComfyUI → validate → one sequential enqueue → output → terminate.
- Requested GPU: `A100-80GB`.
- Actual GPU: `NVIDIA A100-SXM4-80GB`, `81920 MiB`, `cuda:0`.
- Volume: `minimax-h3-microdrama-cache` mounted at `/cache`.
- ComfyUI: `0.33.2`; pinned custom nodes and Turbo settings were unchanged.
- Proven compiler image was reused with `gcc` and `python3-dev`; no `g++`, plugin change, attention change, Turbo change, or system CUDA toolkit addition was made.
- Compiler sanity checks: `/usr/bin/gcc`, `gcc (Debian 12.2.0-14+deb12u1) 12.2.0`, `/usr/local/include/python3.12/Python.h`.
- The CD4.1 Triton compile/run probe was not rerun because the runtime image was not materially changed; both H3 repairs executed successfully on the proven runtime.
- S02 take 1 Modal app: `ap-2Ud4RgfIrkJYlNqxaZJcLT`; ComfyUI startup `26.109s`.
- S02 take 2 Modal app: `ap-loqkjIHYR3qWUe3NfERIXo`; ComfyUI startup `17.057s`.
- No bridge, public endpoint, persistent ComfyUI service, `min_containers`, or external editor was used.

## Repair generations

Both generations used route `frame-to-video`, variant `i2v-turbo`, the approved S02 keyframe, existing timing, and the existing Turbo graph. The first take used the locked seed; the second used the one permitted changed seed.

| Shot / take | Seed | Prompt ID | Enqueues | Generation time | Status |
|---|---:|---|---:|---:|---|
| S02 / 1 | 4102 | `171d738c-2149-457f-a127-36ab69b67915` | 1 | 190.216s runner / 180.39s ComfyUI | Rejected |
| S02 / 2 | 4104 | `63510cde-af65-4526-93c8-fb1fa70e3da1` | 1 | 183.56s runner / 178.37s ComfyUI | Rejected |

Total new H3 generations: **2**. S03 CD4.2 generations: **0**. No third S02 take, no S03 take, and no alternate S01 take were generated.

## Outputs and technical checks

Both S02 outputs were present in the persistent volume, downloaded locally, successfully read by FFprobe, and passed complete FFmpeg decode. Each contains H.264 video and AAC stereo audio at 32 kHz.

| Take | Remote output | Local output | Format / duration / size | SHA-256 |
|---|---|---|---|---|
| S02 / 1 | `/cache/cd4-2-output/s02-t1/cd4/s02_i2v_turbo_00001_.mp4` | `outputs/the-last-bus/clips/cd4-2/S02-i2v-turbo-t1.mp4` | 1344×768, 24 fps, 5.167s, 1,304,884 bytes | `20bcd45d3e96155cd61061aa26af74887000aabfe8abaacb548b4b2a77d4bb96` |
| S02 / 2 | `/cache/cd4-2-output/s02-t2/cd4/s02_i2v_turbo_00001_.mp4` | `outputs/the-last-bus/clips/cd4-2/S02-i2v-turbo-t2.mp4` | 1344×768, 24 fps, 5.167s, 1,330,241 bytes | `85cfc7b6c7452ef3ec24d815aeeb59d9b3c5b44be2c3e6a6dbadc95ef42e97e1` |

Shot-level audio was present and non-silent. `volumedetect` measured mean/max levels of take 1 `-19.2/-4.4 dB` and take 2 `-19.4/-5.9 dB`.

## Visual QC and state

- S01: **accepted unchanged**, with the locked SHA-256 above.
- S02 take 1: **rejected**; a large bus/vehicle remained visible at the left edge and vehicle/headlight cues appeared on the road before the arrival beat.
- S02 take 2: **rejected**; the same premature bus/vehicle and headlight violation persisted after the changed seed.
- S03: no CD4.2 generation. The prior CD4.1 S03 output remained unselected and was not used as a repair substitute.
- Existing Producer state was updated normally: S02 take 1 and take 2 were recorded as technically completed with visual-rejection reasons; S01 remains the only selected take; `shot-generation` remains failed.
- Final selected shot set: **S01 only**; no complete three-shot selection exists.

Because S02 remained visually noncompliant after the maximum two repair takes, final assembly was stopped. No `final/master.mp4`, final media-info, final technical QC, or final visual-QC record was produced. No source-code, plugin, model, workflow, compiler, attention, or Turbo-setting changes were made; only the two ignored prompt files and ignored Producer state were updated, plus this tracked report. The temporary runner was removed after execution. No music, TTS, dialogue, or lip-sync work was started.
