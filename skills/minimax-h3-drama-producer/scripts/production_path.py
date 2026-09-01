#!/usr/bin/env python3
"""Run the smallest Producer -> Prompt Composer -> H3 preparer proof path."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import profile_tool


SCRIPT_DIR = Path(__file__).resolve().parent
PREPARER = SCRIPT_DIR.parent.parent / "minimax-h3-comfyui" / "scripts" / "prepare_workflow.py"
COMPOSER_COMMIT = "0548331876476934a081927017041bcc2bedab81"
COMPOSER_VERSION = "5.43.4"
MODEL = "10Eros_Max_h3_TURBO-hybrid_beta4_int8_convrot.safetensors"
TEXT_ENCODER = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
VIDEO_VAE = "minimax_h3_video_vae_fp16.safetensors"
AUDIO_VAE = "minimax_h3_audio_vae_fp32.safetensors"


class PathError(RuntimeError):
    pass


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def require(mapping: dict[str, Any], key: str) -> Any:
    value = mapping.get(key)
    if value in (None, ""):
        raise PathError(f"missing {key}")
    return value


def load_project(project_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    state = profile_tool.load_data(project_root / "project.yaml")
    shot_list = profile_tool.load_data(project_root / "planning" / "shot-list.yaml")
    shots = [shot for shot in shot_list.get("shots", []) if shot.get("id") == "S01"]
    if len(shots) != 1:
        raise PathError(f"expected exactly one S01 shot contract, found {len(shots)}")
    jobs = [job for job in state.get("jobs", []) if job.get("shot") == "S01"]
    if not jobs:
        raise PathError("Producer state has no S01 route decision")
    return state, shots[0], jobs[-1]


def selected_references(state: dict[str, Any], shot: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = {item.get("id"): item for item in state.get("artifacts", [])}
    roles = list(require(shot, "reference_roles"))
    if any(artifacts.get(role, {}).get("role") == "storyboard" for role in roles):
        raise PathError("S01 Producer reference set unexpectedly includes a storyboard")
    result = []
    for asset_id in roles:
        artifact = artifacts.get(asset_id)
        if not artifact:
            raise PathError(f"Producer reference artifact is missing: {asset_id}")
        path = Path(require(artifact, "path"))
        result.append(
            {
                "id": asset_id,
                "role": artifact.get("role"),
                "path": str(path),
                "absolute_path": str((Path(state["project"]["workspace"]) / "outputs" / "the-last-bus" / path).resolve()),
            }
        )
    for item in result:
        item["sha256"] = sha256_file(Path(item["absolute_path"]))
    return result


def composer_fixture(shot: dict[str, Any], references: list[dict[str, Any]]) -> dict[str, Any]:
    subject = next((item for item in references if item["role"] == "character-identity"), None)
    environment = next((item for item in references if item["role"] == "environment"), None)
    if not subject or not environment:
        raise PathError("S01 Composer input requires the selected character and environment references")

    subject_id = subject["id"]
    environment_id = environment["id"]
    return {
        "format": "h3_prompt_composer_ai_import",
        "schema_version": 5,
        "operation": "replace_project",
        "project": {
            "mode": "REF",
            "duration_seconds": shot["duration_s"],
            "style": "Live-action, cinematic",
            "task_types": ["reference generation"],
        },
        "assets": {
            "subjects": [
                {
                    "id": subject_id,
                    "name": "Nora",
                    "type": "character",
                    "description": "An adult woman in her late twenties with shoulder-length dark wavy hair, a mustard-yellow raincoat over dark clothes, black ankle boots, and a small black backpack.",
                    "picture_slots": [],
                    "video_slots": [],
                    "reference_contribution": "character_sheet",
                }
            ],
            "environments": [
                {
                    "id": environment_id,
                    "name": "bus stop",
                    "description": "One modern glass-and-metal bus shelter at blue hour after light rain, with one bench, wet reflective pavement, and a road directly in front.",
                    "pictures": [],
                }
            ],
            "pictures": [],
            "audio": [],
            "videos": [],
        },
        "generations": [
            {
                "name": "S01 Waiting",
                "summary": shot["purpose"],
                "overall_ambience": shot["sound"],
                "music": "N/A",
                "shots": [
                    {
                        "cut_time_seconds": None,
                        "environment": environment_id,
                        "presence": {subject_id: "on_screen"},
                        "opening_state": shot["action"],
                        "action": shot["action"],
                        "camera": {
                            "authoring_mode": "builder",
                            "framing": "wide",
                            "primary": subject_id,
                            "view": "front",
                            "angle": "eye_level",
                            "movement": "push_in",
                            "speed": "slow",
                            "timing": "throughout_shot",
                            "stability": "locked",
                            "lens": "natural",
                        },
                        "sound_effects": shot["sound"],
                    }
                ],
            }
        ],
    }


def run_json(command: list[str], cwd: Path, *, allow_nonzero_json: bool = False) -> dict[str, Any]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode and not allow_nonzero_json:
        detail = result.stderr.strip() or result.stdout.strip()
        raise PathError(f"command failed ({result.returncode}): {' '.join(command)}\n{detail}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PathError(f"command did not return JSON: {' '.join(command)}") from exc


def validate_graph(graph: dict[str, Any], prompt: str, first_frame: str) -> dict[str, Any]:
    errors: list[str] = []
    if graph.get("104", {}).get("class_type") != "MiniMaxH3ImageToVideo":
        errors.append("native I2V node 104 is missing")
    if graph.get("104", {}).get("inputs", {}).get("prompt") != prompt:
        errors.append("prepared prompt differs from Composer output")
    if graph.get("6", {}).get("inputs", {}).get("unet_name") != MODEL:
        errors.append("10Eros beta4 is not selected")
    if graph.get("13", {}).get("inputs", {}).get("clip_name") != TEXT_ENCODER:
        errors.append("Qwen encoder differs from the existing H3 encoder")
    if graph.get("11", {}).get("inputs", {}).get("vae_name") != VIDEO_VAE:
        errors.append("video VAE differs from the existing H3 video VAE")
    if graph.get("24", {}).get("inputs", {}).get("vae_name") != AUDIO_VAE:
        errors.append("audio VAE differs from the existing H3 audio VAE")
    if graph.get("17", {}).get("class_type") != "KSamplerSelect":
        errors.append("Larry/Turbo sampler replaced the native sampler")
    if graph.get("17", {}).get("inputs", {}).get("sampler_name") != "euler":
        errors.append("sampler is not euler")
    if graph.get("9", {}).get("inputs") != {
        "model": ["6", 0],
        "scheduler": "simple",
        "steps": 8,
        "denoise": 1.0,
    }:
        errors.append("scheduler/steps/denoise differ from the locked controls")
    if graph.get("15", {}).get("inputs", {}).get("noise_seed") != 4101:
        errors.append("S01 seed is not the existing Producer seed 4101")
    if graph.get("104", {}).get("inputs", {}).get("first_frame") != ["114", 0]:
        errors.append("first frame is not bound through node 114")
    if graph.get("114", {}).get("inputs", {}).get("image") != first_frame:
        errors.append("first-frame filename differs from S01")
    if "116" in graph or any("last_frame" in node.get("inputs", {}) for node in graph.values()):
        errors.append("last-frame input is present")
    video_inputs = graph.get("104", {}).get("inputs", {})
    if (video_inputs.get("width"), video_inputs.get("height"), video_inputs.get("length")) != (1344, 768, 124):
        errors.append("resolution or frame length differs from 1344x768x124")
    classes = {node.get("class_type") for node in graph.values()}
    if any("Lora" in str(name) or "Upscale" in str(name) or "TurboSampler" in str(name) for name in classes):
        errors.append("graph contains a Larry/LoRA/upscaler node")
    return {
        "passed": not errors,
        "errors": errors,
        "class_count": len(classes),
        "selected": {
            "checkpoint": graph.get("6", {}).get("inputs", {}).get("unet_name"),
            "text_encoder": graph.get("13", {}).get("inputs", {}).get("clip_name"),
            "video_vae": graph.get("11", {}).get("inputs", {}).get("vae_name"),
            "audio_vae": graph.get("24", {}).get("inputs", {}).get("vae_name"),
            "sampler": graph.get("17", {}).get("inputs", {}).get("sampler_name"),
            "scheduler": graph.get("9", {}).get("inputs", {}).get("scheduler"),
            "steps": graph.get("9", {}).get("inputs", {}).get("steps"),
            "denoise": graph.get("9", {}).get("inputs", {}).get("denoise"),
            "seed": graph.get("15", {}).get("inputs", {}).get("noise_seed"),
            "width": video_inputs.get("width"),
            "height": video_inputs.get("height"),
            "frames": video_inputs.get("length"),
            "first_frame": graph.get("114", {}).get("inputs", {}).get("image"),
            "larry_lora": False,
            "latent_upscaler": False,
        },
    }


def build_path(args: argparse.Namespace) -> dict[str, Any]:
    project_root = args.project_root.resolve()
    workspace = project_root.parents[1]
    state, shot, job = load_project(project_root)
    producer_route = require(job, "route")
    if producer_route != shot.get("route_later"):
        raise PathError(f"Producer route mismatch: state={producer_route!r}, contract={shot.get('route_later')!r}")
    if producer_route != "frame-to-video":
        raise PathError(f"CD5.1 only proves the existing S01 frame-to-video route, got {producer_route!r}")
    references = selected_references(state, shot)
    first_frame_asset = next(
        (
            item
            for item in state.get("artifacts", [])
            if item.get("id") == "keyframe-s01" and item.get("role") == "first-frame"
        ),
        None,
    )
    if not first_frame_asset:
        raise PathError("Producer state has no keyframe-s01 first-frame artifact")
    first_frame_path = (project_root / require(first_frame_asset, "path")).resolve()
    first_frame_name = first_frame_path.name
    first_frame_sha = sha256_file(first_frame_path)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    fixture_path = output_dir / "composer-input.json"
    fixture = composer_fixture(shot, references)
    fixture_bytes = (json.dumps(fixture, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    fixture_path.write_bytes(fixture_bytes)

    composer = run_json(
        ["node", str(args.composer_harness.resolve()), str(fixture_path)],
        workspace,
        allow_nonzero_json=True,
    )
    if composer.get("composer", {}).get("commit") != COMPOSER_COMMIT or composer.get("composer", {}).get("version") != COMPOSER_VERSION:
        raise PathError("external Composer version or commit is not pinned")
    prompt_check = composer.get("prompt_check", {})
    one_shot_passed = (
        composer.get("prompt", {}).get("generated")
        and not prompt_check.get("blocking_errors")
        and composer.get("import", {}).get("generations") == 1
        and composer.get("import", {}).get("shots") == 1
    )
    if not one_shot_passed:
        raise PathError(f"external Composer did not pass its prompt check: {composer.get('prompt_check')}")
    prompt = composer["prompt"]["text"]
    prompt_path = output_dir / "composer-prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    composer_result_path = output_dir / "composer-result.json"
    composer_result_path.write_text(json.dumps(composer, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prepared_path = output_dir / "s01-prepared-i2v.json"
    preparer_args = [
        sys.executable,
        str(PREPARER),
        "--mode",
        "i2v",
        "--project-root",
        str(workspace),
        "--prompt-file",
        str(prompt_path),
        "--output",
        str(prepared_path),
        "--no-turbo",
        "--fl2va",
        MODEL,
        "--text-encoder",
        TEXT_ENCODER,
        "--video-vae",
        VIDEO_VAE,
        "--audio-vae",
        AUDIO_VAE,
        "--width",
        "1344",
        "--height",
        "768",
        "--duration",
        str(shot["duration_s"]),
        "--seed",
        "4101",
        "--sampler",
        "euler",
        "--scheduler",
        "simple",
        "--steps",
        "8",
        "--denoise",
        "1.0",
        "--first-frame",
        str(first_frame_path),
        "--filename-prefix",
        "cd5-1/s01_i2v_composer",
    ]
    preparer_meta = run_json(preparer_args, workspace)
    graph = json.loads(prepared_path.read_text(encoding="utf-8"))
    graph_check = validate_graph(graph, prompt, str(first_frame_path))
    if not graph_check["passed"]:
        raise PathError(f"prepared graph dry-run failed: {graph_check['errors']}")

    manifest = {
        "shot": shot,
        "producer_route": producer_route,
        "h3_mode": "i2v",
        "references": references,
        "first_frame": {
            "id": first_frame_asset["id"],
            "path": str(first_frame_path),
            "sha256": first_frame_sha,
        },
        "composer": {
            "harness": str(args.composer_harness.resolve()),
            "checkout": composer.get("composer", {}).get("path"),
            "commit": composer.get("composer", {}).get("commit"),
            "version": composer.get("composer", {}).get("version"),
            "input": str(fixture_path),
            "input_sha256": sha256_file(fixture_path),
            "result": str(composer_result_path),
            "prompt": str(prompt_path),
            "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
            "mode": composer.get("import", {}).get("composer_mode"),
            "one_shot_prompt_check_passed": one_shot_passed,
            "harness_generic_acceptance_passed": composer.get("acceptance_passed"),
        },
        "preparer": {
            "script": str(PREPARER),
            "prepared_graph": str(prepared_path),
            "prepared_graph_sha256": sha256_file(prepared_path),
            "metadata": preparer_meta,
        },
        "controls": {
            "checkpoint": MODEL,
            "text_encoder": TEXT_ENCODER,
            "video_vae": VIDEO_VAE,
            "audio_vae": AUDIO_VAE,
            "sampler": "euler",
            "scheduler": "simple",
            "steps": 8,
            "denoise": 1.0,
            "seed": 4101,
            "width": 1344,
            "height": 768,
            "frames": 124,
            "fps": 24,
            "last_frame": False,
            "storyboard": False,
            "latent_upscaler": False,
            "larry_lora": False,
        },
        "dry_run": {
            "passed": True,
            "external_composer_invoked": True,
            "composer_one_shot_check_passed": one_shot_passed,
            "graph_validation": graph_check,
        },
    }
    manifest_path = output_dir / "dry-run.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--project-root", type=Path, required=True)
    result.add_argument("--composer-harness", type=Path, required=True)
    result.add_argument("--output-dir", type=Path)
    return result


def main() -> int:
    args = parser().parse_args()
    if args.output_dir is None:
        args.output_dir = args.project_root / "cd5-1"
    try:
        manifest = build_path(args)
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    except (OSError, PathError, profile_tool.ProfileError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
