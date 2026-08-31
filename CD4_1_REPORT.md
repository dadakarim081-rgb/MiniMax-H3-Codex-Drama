# CD4.1 — unblock Triton compiler and resume The Last Bus

Date: 2026-08-31  
Decision: **C — GENERATION RUNS BUT ONE OR MORE SHOTS FAIL PRODUCTION QUALITY**

## Scope and baseline

- Ponytail: full mode.
- Repository: `/home/karim/Documents/MiniMax-H3-Codex-Drama-cd1`.
- Branch: `codex/cd1-1-storyboard-original`.
- Starting commit: `dc08a8d` (`docs: record CD4 generation blocker`).
- Existing CD3/CD4 character master, scene master, storyboard, keyframes, prompts, workflows, routes, and seeds were reused.
- No character master, scene master, storyboard, keyframe, prompt, plugin source, workflow, model setting, sampling setting, attention setting, or persistent volume was changed.
- The CD2 bridge was not used.

## Temporary Modal runtime fix

- Temporary image compiler packages: `gcc`, `python3-dev`.
- `g++`: not added; no build error required it.
- Full CUDA toolkit: not installed.
- GCC path: `/usr/bin/gcc`.
- GCC version: `gcc (Debian 12.2.0-14+deb12u1) 12.2.0`.
- Python executable: `/usr/local/bin/python`.
- Python header: `/usr/local/include/python3.12/Python.h`.
- Triton: `3.7.1`, imported from `/usr/local/lib/python3.12/site-packages/triton/__init__.py`.
- Triton target: CUDA, architecture 80, warp size 32.
- Probe: a 128-element Triton CUDA add kernel compiled and executed on the A100; every output value was verified as `3.0` before ComfyUI or H3 generation.

## Modal execution

- Architecture: one Modal GPU function, local ComfyUI on `127.0.0.1:8188`, graph validation, sequential enqueue, volume output retrieval, process termination, exit.
- Requested GPU: `A100-80GB`.
- Volume: `minimax-h3-microdrama-cache` mounted at `/cache`.
- S01 worker GPU: `NVIDIA A100 80GB PCIe`.
- S02/S03 worker GPU: `NVIDIA A100-SXM4-80GB` (`85094825984` bytes reported).
- ComfyUI: `0.33.2`; S02/S03 startup timer: `22.08s`; S01 became ready and generated successfully, but its first pre-JSON return could not be deserialized by the host, so its startup timer was not retained. This was bookkeeping only; the output was present in the volume.
- No public endpoint, bridge, persistent server, `min_containers`, concurrency, or deployment framework was used.
- Prepared-graph validation against the live ComfyUI `/object_info` passed for all three graphs (17 nodes each; 1148 node types exposed):
  - S01 workflow SHA-256: `f98d0ca85b7ec9ae56f619dabb9a772e35314fc268d5ec3452ca6c52fcd12734`
  - S02 workflow SHA-256: `d5aa33bcc6c730425f725aabf36fec5d4c9446f2574978379dcf36ada8bd434a`
  - S03 workflow SHA-256: `f078dc9fc16727d7c306ad2d4d84047cf3b22ea559cd6269aa6dbb7e7499258f`

## Generation

All shots used route `frame-to-video` / variant `i2v-turbo` and the locked seeds.

| Shot | Seed | Prompt ID | Enqueued | Generation time | Visual status |
|---|---:|---|---:|---:|---|
| S01 | 4101 | `4b020efd-78d6-4fa2-943f-9af81e9a686a` | 1 | 182.17s ComfyUI execution | Accepted |
| S02 | 4102 | `508b2182-15d8-4a50-8e9c-98e505c89ad6` | 1 | 162.79s runner time / 161.73s ComfyUI execution | Rejected |
| S03 | 4103 | `855cb3bb-6348-447e-a894-fc6ce3a26429` | 1 | 186.399s runner time / 183.77s ComfyUI execution | Rejected |

CD4.1 enqueue count: **3**. No alternate creative take was generated.

### Outputs and shot-level technical checks

All three outputs were present in the persistent volume and downloaded locally. FFprobe succeeded, complete FFmpeg decode succeeded, and each clip contained H.264 video plus AAC stereo audio at 32 kHz.

| Shot | Remote output | Local output | Format / duration / size | SHA-256 |
|---|---|---|---|---|
| S01 | `/cache/cd4-1-output/cd4/s01_i2v_turbo_00001_.mp4` | `outputs/the-last-bus/clips/cd4-1/S01-i2v-turbo.mp4` | 1344×768, 24 fps, 5.167s, 2,104,389 bytes | `9471f3da372163b3e2ffe863f28bc3090386f1955be3c67c41412e0c02be2077` |
| S02 | `/cache/cd4-1-output/cd4/s02_i2v_turbo_00001_.mp4` | `outputs/the-last-bus/clips/cd4-1/S02-i2v-turbo.mp4` | 1344×768, 24 fps, 5.167s, 1,251,652 bytes | `17d10af0b7db3a8933d6c7335b5c9e8bca3dd7314d4f83c099dcf260c77b32f4` |
| S03 | `/cache/cd4-1-output/cd4/s03_i2v_turbo_00001_.mp4` | `outputs/the-last-bus/clips/cd4-1/S03-i2v-turbo.mp4` | 1344×768, 24 fps, 6.583333s, 3,685,853 bytes | `a284939402abb68925d0da060469b86872f6f9c22097e40ac3b3c64000268499` |

Shot audio was present and non-silent. `volumedetect` measured mean/max levels of S01 `-22.6/-7.3 dB`, S02 `-21.5/-6.7 dB`, and S03 `-19.5/-5.6 dB`.

## Visual QC

- S01: **pass**. Nora, mustard raincoat, dark hair, backpack, shelter, bench, wet road, screen-right axis, and waiting/roadward motion remained coherent; no bus or visible headlights appeared before the end beat.
- S02: **fail**. A vehicle/bus is visible at the left edge and headlights/vehicle lights appear down the road before the arrival beat, violating the locked prompt constraint to not show the bus or headlights.
- S03: **fail**. The arriving bus visibly carries route number `27` and additional side lettering, violating the locked prompt constraints for no readable bus text and no route numbers.

Because S02 and S03 failed the production-quality gate, the intended waiting → concern/check road → bus arrival → relief/step chronology was not assembled. No final master, timeline assembly, final media-info, final technical QC report, or final visual-QC record was produced.

## State and source changes

- Existing Producer state was updated through its normal state utility: S01 selected as accepted; S02 and S03 recorded as technically completed but visually rejected; `shot-generation` marked failed with the rejection reasons.
- Tracked source changes: `CD4_1_REPORT.md` only.
- The temporary runner was removed after execution.
- Generated media, logs, contact sheets, and Producer state remain ignored/local and were not added to Git.
- No music, TTS, dialogue, protected-audio, or lip-sync work was started.
