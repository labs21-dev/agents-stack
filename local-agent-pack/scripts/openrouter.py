#!/usr/bin/env python3
"""Zero-dependency OpenRouter adapter for local-agent-pack Phase 1."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import mimetypes
import os
import pathlib
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote


BASE_URL = "https://openrouter.ai/api/v1"
CONFIG_PATH = pathlib.Path(__file__).resolve().parents[1] / "templates" / "openrouter.config.json"

IMAGE_MIME_TYPES = {"png", "jpeg", "jpg", "webp", "gif"}
VIDEO_MIME_TYPES = {"mp4", "mpeg", "mov", "webm"}
AUDIO_MIME_TYPES = {"wav", "mp3", "flac", "m4a", "ogg", "webm", "aac"}

RETRYABLE_STATUS = {409, 429, 500, 502, 503, 504, 524, 529}
MODEL_SURFACE_PATHS = {
    "all": "/models",
    "image-generation": "/images/models",
    "video-generation": "/videos/models",
    "text": "/models?output_modalities=text",
    "speech": "/models?output_modalities=speech",
    "transcription": "/models?output_modalities=transcription",
    "image-input": "/models?input_modalities=image",
    "video-input": "/models?input_modalities=video",
    "audio-input": "/models?input_modalities=audio",
}


class AdapterError(Exception):
    pass


@dataclass
class HttpResponse:
    status: int
    headers: dict[str, str]
    body: bytes
    text: str


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def json_dump(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_config(config_path: pathlib.Path | None = None) -> dict[str, Any]:
    path = config_path or CONFIG_PATH
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def storage_root(args: argparse.Namespace, config: dict[str, Any]) -> pathlib.Path:
    configured = args.storage_root or config["storageRoot"]
    path = pathlib.Path(configured).expanduser()
    return path if path.is_absolute() else (pathlib.Path.cwd() / path).resolve()


def media_type_for(path: pathlib.Path, allowed: set[str]) -> str:
    mime = mimetypes.guess_type(path.name)[0]
    extension = path.suffix.removeprefix(".").lower()
    if extension in allowed and mime:
        return mime
    raise AdapterError(f"unsupported file type {path.suffix!r}; allowed extensions: {sorted(allowed)}")


def extension_for_media_type(media_type: str) -> str:
    extension = mimetypes.guess_extension(media_type)
    if extension:
        return extension.removeprefix(".")
    return media_type.split("/", 1)[-1].replace("+", ".")


def data_url(path: pathlib.Path, allowed: set[str]) -> tuple[str, str, int]:
    media_type = media_type_for(path, allowed)
    raw = path.read_bytes()
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:{media_type};base64,{encoded}", media_type, len(raw)


def require_cloud_approval(
    args: argparse.Namespace,
    config: dict[str, Any],
    root: pathlib.Path,
    uploaded_path: pathlib.Path | None,
) -> dict[str, Any] | None:
    if os.environ.get("LOCAL_AGENT_PACK_ALLOW_CLOUD") != "1":
        return None

    record: dict[str, Any] = {
        "provider": "openrouter",
        "kind": "request",
        "approvedAt": utc_now(),
    }
    if uploaded_path is not None:
        record.update(
            {
                "kind": "upload",
                "path": str(uploaded_path.resolve()),
                "bytes": uploaded_path.stat().st_size,
            }
        )

    approval_id = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()[:20]
    record["id"] = approval_id
    json_dump(root / "approvals" / f"{approval_id}.json", record)
    return record


def http_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None,
    api_key: str,
    transport,
) -> tuple[int, dict[str, str], Any]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    response = transport.request(method, url, body=body, headers=headers)
    parsed: Any = None
    if response.body:
        try:
            parsed = json.loads(response.body)
        except json.JSONDecodeError:
            parsed = {"raw": response.text}
    return response.status, response.headers, parsed


def http_bytes(
    method: str,
    url: str,
    api_key: str,
    transport,
) -> tuple[int, dict[str, str], bytes]:
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/octet-stream"}
    response = transport.request(method, url, body=None, headers=headers)
    return response.status, response.headers, response.body


def request_json(
    method: str,
    url: str,
    payload: dict[str, Any],
    api_key: str,
    transport,
    max_attempts: int = 3,
) -> tuple[dict[str, str], Any]:
    last_error: Any = None
    for attempt in range(1, max_attempts + 1):
        status, headers, parsed = http_json(method, url, payload, api_key, transport)
        if 200 <= status < 300:
            return headers, parsed
        last_error = parsed or {"message": f"HTTP {status}"}
        if status not in RETRYABLE_STATUS or attempt == max_attempts:
            raise AdapterError(f"OpenRouter HTTP {status}: {json.dumps(last_error, ensure_ascii=False)}")
        time.sleep(min(2 ** (attempt - 1), 8))
    raise AdapterError(f"OpenRouter request failed: {json.dumps(last_error, ensure_ascii=False)}")


def endpoint_url(config: dict[str, Any], path: str) -> str:
    if not path.startswith("/"):
        raise AdapterError(f"invalid endpoint path: {path}")
    return config["baseUrl"].rstrip("/") + path


def envelope(
    endpoint: str,
    model: str,
    status: str,
    output: Any,
    artifacts: list[dict[str, Any]],
    usage: dict[str, Any],
    provenance: dict[str, Any],
    *,
    root: pathlib.Path | None = None,
    artifact_type: str = "openrouter-result",
    input_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "provider": "openrouter",
        "endpoint": endpoint,
        "model": model,
        "status": status,
        "input": input_data or {},
        "output": output,
        "artifacts": artifacts,
        "usage": usage,
        "provenance": provenance,
    }
    if root is not None:
        day = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")
        stable = json.dumps(result, sort_keys=True, ensure_ascii=False) + utc_now()
        artifact_id = "or_" + hashlib.sha256(stable.encode()).hexdigest()[:20]
        record = {
            "id": artifact_id,
            "type": artifact_type,
            **result,
            "createdAt": utc_now(),
        }
        json_dump(root / "artifacts" / day / f"{artifact_id}.json", record)
        result["artifactRecord"] = str(root / "artifacts" / day / f"{artifact_id}.json")
    return result


def declined(
    endpoint: str,
    model: str,
    reason: str,
    input_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return envelope(
        endpoint,
        model,
        "declined",
        {"reason": reason},
        [],
        {},
        {},
        input_data=input_data,
    )


def model_for(config: dict[str, Any], key: str, override: str | None) -> str:
    return override or config["models"][key]


def read_reasoning_details(path_text: str | None) -> list[dict[str, Any]] | None:
    if path_text is None:
        return None
    path = pathlib.Path(path_text)
    if not path.is_file():
        raise AdapterError(f"reasoning file not found: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AdapterError(f"invalid reasoning file: {path}") from exc
    if isinstance(value, dict):
        if isinstance(value.get("output"), dict) and "reasoningDetails" in value["output"]:
            value = value["output"]["reasoningDetails"]
        elif "reasoningDetails" in value:
            value = value["reasoningDetails"]
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise AdapterError(f"reasoning file must contain reasoningDetails as object array: {path}")
    return value


def parse_provider_options(value: str | None) -> dict[str, Any] | None:
    if value is None:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise AdapterError("--provider-options must be a JSON object") from exc
    if not isinstance(parsed, dict):
        raise AdapterError("--provider-options must be a JSON object")
    if "options" in parsed:
        return parsed
    return {"options": parsed}


def validate_provider_passthrough(model_record: dict[str, Any], provider_options: dict[str, Any] | None) -> None:
    if provider_options is None:
        return
    allowed = model_record.get("allowed_passthrough_parameters")
    if allowed is None:
        return
    if not isinstance(allowed, list):
        raise AdapterError(f"model {model_record.get('id')} returned invalid passthrough metadata")
    options = provider_options.get("options", {})
    if not isinstance(options, dict):
        raise AdapterError("provider.options must be a JSON object")
    unsupported = sorted(set(options) - set(allowed))
    if unsupported:
        raise AdapterError(
            f"model {model_record.get('id')} does not allow provider passthrough parameters: "
            + ", ".join(unsupported)
        )


def api_key_from(config: dict[str, Any]) -> str:
    api_key = os.environ.get(config["apiKeyEnv"])
    if not api_key:
        raise AdapterError(f"missing {config['apiKeyEnv']}")
    return api_key


def find_model(models: list[dict[str, Any]], model: str) -> dict[str, Any]:
    for record in models:
        if record.get("id") == model or record.get("canonical_slug") == model:
            return record
    raise AdapterError(f"model not found on OpenRouter: {model}")


def fetch_models(
    config: dict[str, Any],
    surface: str,
    api_key: str,
    transport,
) -> list[dict[str, Any]]:
    paths = MODEL_SURFACE_PATHS
    if surface not in paths:
        raise AdapterError(f"unsupported model surface: {surface}")
    _, response = request_json("GET", endpoint_url(config, paths[surface]), None, api_key, transport)
    models = response.get("data", []) if isinstance(response, dict) else []
    if not isinstance(models, list):
        raise AdapterError("OpenRouter returned an invalid model list")
    return models


def fetch_model_surface_path(surface: str) -> str:
    return MODEL_SURFACE_PATHS[surface]


def model_surface_allows(model_record: dict[str, Any], surface: str) -> bool:
    architecture = model_record.get("architecture", {})
    inputs = architecture.get("input_modalities", [])
    outputs = architecture.get("output_modalities", [])
    rules = {
        "all": lambda record: True,
        "image-generation": lambda record: "image" in record.get("architecture", {}).get("output_modalities", []),
        "video-generation": lambda record: "video" in record.get("supported_output_modalities", ["video"]),
        "text": lambda record: "text" in outputs and "text" in inputs,
        "speech": lambda record: "speech" in outputs and "text" in inputs,
        "transcription": lambda record: "transcription" in outputs and "audio" in inputs,
        "image-input": lambda record: "image" in inputs,
        "video-input": lambda record: "video" in inputs,
        "audio-input": lambda record: "audio" in inputs,
    }
    return rules[surface](model_record)


def summarize_model(record: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "id",
        "canonical_slug",
        "name",
        "description",
        "architecture",
        "supported_parameters",
        "supported_durations",
        "supported_resolutions",
        "supported_aspect_ratios",
        "supported_frame_images",
        "allowed_passthrough_parameters",
        "generate_audio",
        "endpoints",
    ]
    return {key: record.get(key) for key in keys if key in record}


def models_list(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    models = fetch_models(config, args.surface, api_key_from(config), transport)
    if args.surface != "all":
        models = [record for record in models if model_surface_allows(record, args.surface)]
    return {
        "provider": "openrouter",
        "endpoint": fetch_model_surface_path(args.surface),
        "surface": args.surface,
        "status": "completed",
        "models": [summarize_model(record) for record in models],
    }


def model_show(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    surface = args.surface or "all"
    models = fetch_models(config, surface, api_key_from(config), transport)
    model = find_model(models, args.model)
    if not model_surface_allows(model, surface):
        raise AdapterError(f"model {args.model} is not available on surface {surface}")
    return {
        "provider": "openrouter",
        "endpoint": fetch_model_surface_path(surface),
        "surface": surface,
        "status": "completed",
        "model": model,
    }


def validate_modality(
    model_record: dict[str, Any],
    *,
    input_modality: str | None = None,
    output_modality: str | None = None,
) -> None:
    architecture = model_record.get("architecture", {})
    inputs = architecture.get("input_modalities", [])
    outputs = architecture.get("output_modalities", [])
    if input_modality is not None and input_modality not in inputs:
        raise AdapterError(f"model {model_record.get('id')} does not accept {input_modality} input")
    if output_modality is not None and output_modality not in outputs:
        raise AdapterError(f"model {model_record.get('id')} does not produce {output_modality} output")


def descriptor_allows(descriptor: Any, value: Any) -> bool:
    if descriptor is None:
        return False
    if not isinstance(descriptor, dict):
        return True
    descriptor_type = descriptor.get("type")
    if descriptor_type == "enum":
        return value in descriptor.get("values", [])
    if descriptor_type == "range":
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return False
        return descriptor.get("min", float("-inf")) <= numeric <= descriptor.get("max", float("inf"))
    if descriptor_type == "boolean":
        return isinstance(value, bool)
    return True


def validate_image_capabilities(model_record: dict[str, Any], payload: dict[str, Any]) -> None:
    validate_modality(model_record, input_modality="text", output_modality="image")
    supported = model_record.get("supported_parameters", {})
    checked_fields = {
        "n",
        "resolution",
        "aspect_ratio",
        "quality",
        "output_format",
        "background",
        "seed",
        "input_references",
    }
    unsupported = [field for field in checked_fields if field in payload and field not in supported]
    if unsupported:
        raise AdapterError(
            f"model {model_record.get('id')} does not support image parameters: {', '.join(sorted(unsupported))}"
        )
    invalid = [
        field
        for field in checked_fields
        if field in payload
        and field in supported
        and field != "input_references"
        and not descriptor_allows(supported[field], payload[field])
    ]
    if invalid:
        raise AdapterError(
            f"invalid values for model {model_record.get('id')}: {', '.join(sorted(invalid))}"
        )
    if "input_references" in payload:
        validate_modality(model_record, input_modality="image")
        descriptor = supported.get("input_references")
        if not descriptor_allows(descriptor, len(payload["input_references"])):
            raise AdapterError(
                f"model {model_record.get('id')} does not allow {len(payload['input_references'])} image references"
            )


def validate_video_capabilities(model_record: dict[str, Any], args: argparse.Namespace) -> None:
    if args.duration is not None:
        durations = model_record.get("supported_durations")
        if durations and args.duration not in durations:
            raise AdapterError(f"model {model_record.get('id')} supports durations {durations}, not {args.duration}")
    if args.resolution is not None:
        resolutions = model_record.get("supported_resolutions")
        if resolutions and args.resolution not in resolutions:
            raise AdapterError(
                f"model {model_record.get('id')} supports resolutions {resolutions}, not {args.resolution}"
            )
    if args.aspect_ratio is not None:
        ratios = model_record.get("supported_aspect_ratios")
        if ratios and args.aspect_ratio not in ratios:
            raise AdapterError(
                f"model {model_record.get('id')} supports aspect ratios {ratios}, not {args.aspect_ratio}"
            )
    if args.first_frame is not None:
        frames = model_record.get("supported_frame_images", [])
        if frames and "first_frame" not in frames:
            raise AdapterError(f"model {model_record.get('id')} does not support first-frame image input")
    if args.last_frame is not None:
        frames = model_record.get("supported_frame_images", [])
        if frames and "last_frame" not in frames:
            raise AdapterError(f"model {model_record.get('id')} does not support last-frame image input")
    if args.first_frame is not None and args.last_frame is not None and args.first_frame == args.last_frame:
        raise AdapterError("first frame and last frame must be different files")
    if not model_record.get("generate_audio", False):
        generate_audio = not getattr(args, "no_audio", False)
        if generate_audio:
            raise AdapterError(f"model {model_record.get('id')} does not support generated audio")


def save_bytes(root: pathlib.Path, directory: str, data: bytes, extension: str) -> dict[str, Any]:
    digest = hashlib.sha256(data).hexdigest()[:20]
    path = root / "media" / directory / f"{digest}.{extension}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {
        "type": directory.removesuffix("s") if directory.endswith("s") else directory,
        "path": str(path.resolve()),
        "mediaType": mimetypes.types_map.get("." + extension, "application/octet-stream"),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def parse_data_url_image(value: str) -> tuple[str, bytes]:
    data_url_match = re.fullmatch(r"data:([^;]+);base64,(.+)", value)
    if data_url_match:
        media_type, encoded = data_url_match.group(1), data_url_match.group(2)
    else:
        media_type, encoded = "image/png", value
    try:
        return media_type, base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise AdapterError("invalid base64 image data") from exc


def image_generate(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    model = model_for(config, "imageGeneration", args.model)

    references: list[dict[str, Any]] = []
    reference_info: list[dict[str, Any]] = []
    for reference_path_text in args.reference or []:
        reference_path = pathlib.Path(reference_path_text)
        if not reference_path.is_file():
            raise AdapterError(f"reference image not found: {reference_path}")
        url, media_type, size = data_url(reference_path, IMAGE_MIME_TYPES)
        limit = int(config.get("limits", {}).get("imageUploadBytes", 10 * 1024 * 1024))
        if size > limit:
            raise AdapterError(f"reference image exceeds {limit} bytes")
        references.append({"type": "image_url", "image_url": {"url": url}})
        reference_info.append({"path": str(reference_path.resolve()), "mediaType": media_type, "bytes": size})

    approval = require_cloud_approval(
        args,
        config,
        root,
        pathlib.Path(args.reference[0]) if args.reference else None,
    )
    if approval is None:
        return declined("/images", model, "cloud approval is required; set LOCAL_AGENT_PACK_ALLOW_CLOUD=1")

    payload: dict[str, Any] = {"model": model, "prompt": args.prompt}
    optional = {
        "n": args.count,
        "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio,
        "quality": args.quality,
        "output_format": args.output_format,
        "background": args.background,
        "seed": args.seed,
        "input_references": references or None,
    }
    for key, value in optional.items():
        if value is not None:
            payload[key] = value
    api_key = api_key_from(config)
    provider_options = parse_provider_options(args.provider_options)
    if config.get("validateCapabilities", True):
        model_record = find_model(
            fetch_models(config, "image-generation", api_key, transport), model
        )
        validate_image_capabilities(model_record, payload)
        validate_provider_passthrough(model_record, provider_options)
    if provider_options is not None:
        payload["provider"] = provider_options

    headers, response = request_json("POST", endpoint_url(config, "/images"), payload, api_key, transport)
    response_data = response.get("data", []) if isinstance(response, dict) else []
    if not response_data:
        raise AdapterError("OpenRouter returned no image data")

    artifacts: list[dict[str, Any]] = []
    for index, image in enumerate(response_data):
        media_type = image.get("media_type") or "image/png"
        _, raw = parse_data_url_image(image["b64_json"])
        artifact = save_bytes(root, "images", raw, extension_for_media_type(media_type))
        artifact["index"] = index
        artifacts.append(artifact)

    return envelope(
        "/images",
        model,
        "completed",
        {"created": response.get("created")},
        artifacts,
        response.get("usage", {}),
        {
            "requestId": headers.get("X-Request-Id"),
            "generationId": headers.get("X-Generation-Id"),
            "jobId": None,
            "approvalId": approval["id"],
        },
        root=root,
        artifact_type="image-generation",
        input_data={"prompt": args.prompt, "references": reference_info, "providerOptions": provider_options},
    )


def job_path(root: pathlib.Path, job_id: str) -> pathlib.Path:
    if not re.fullmatch(r"[A-Za-z0-9._-]+", job_id):
        raise AdapterError("invalid video job id")
    return root / "jobs" / "videos" / f"{job_id}.json"


def read_job(root: pathlib.Path, job_id: str) -> dict[str, Any]:
    path = job_path(root, job_id)
    if not path.is_file():
        raise AdapterError(f"unknown video job: {job_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_job(root: pathlib.Path, job: dict[str, Any]) -> None:
    json_dump(job_path(root, job["id"]), job)


def video_submit(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    model = model_for(config, "videoGeneration", args.model)
    approval = require_cloud_approval(args, config, root, None)
    if approval is None:
        return declined("/videos", model, "cloud approval is required; set LOCAL_AGENT_PACK_ALLOW_CLOUD=1")

    payload: dict[str, Any] = {
        "model": model,
        "prompt": args.prompt,
        "generate_audio": not args.no_audio,
    }
    optional = {
        "duration": args.duration,
        "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio,
    }
    for key, value in optional.items():
        if value is not None:
            payload[key] = value
    if args.first_frame:
        path = pathlib.Path(args.first_frame)
        url, media_type, size = data_url(path, IMAGE_MIME_TYPES)
        limit = int(config.get("limits", {}).get("imageUploadBytes", 10 * 1024 * 1024))
        if size > limit:
            raise AdapterError(f"first frame exceeds {limit} bytes")
        payload["frame_images"] = [
            {"type": "image_url", "image_url": {"url": url}, "frame_type": "first_frame"}
        ]
    if args.last_frame:
        path = pathlib.Path(args.last_frame)
        url, media_type, size = data_url(path, IMAGE_MIME_TYPES)
        limit = int(config.get("limits", {}).get("imageUploadBytes", 10 * 1024 * 1024))
        if size > limit:
            raise AdapterError(f"last frame exceeds {limit} bytes")
        payload.setdefault("frame_images", []).append(
            {"type": "image_url", "image_url": {"url": url}, "frame_type": "last_frame"}
        )
    if args.reference:
        path = pathlib.Path(args.reference)
        url, media_type, size = data_url(path, IMAGE_MIME_TYPES)
        limit = int(config.get("limits", {}).get("imageUploadBytes", 10 * 1024 * 1024))
        if size > limit:
            raise AdapterError(f"reference image exceeds {limit} bytes")
        payload["input_references"] = [{"type": "image_url", "image_url": {"url": url}}]

    provider_options = parse_provider_options(args.provider_options)
    api_key = api_key_from(config)
    if config.get("validateCapabilities", True):
        model_record = find_model(
            fetch_models(config, "video-generation", api_key, transport), model
        )
        validate_video_capabilities(model_record, args)
        validate_provider_passthrough(model_record, provider_options)
    if provider_options is not None:
        payload["provider"] = provider_options
    headers, response = request_json(
        "POST", endpoint_url(config, "/videos"), payload, api_key, transport
    )
    job_id = response.get("id")
    if not job_id:
        raise AdapterError("OpenRouter returned no video job id")
    now = utc_now()
    job = {
        "id": job_id,
        "provider": "openrouter",
        "endpoint": "/videos",
        "model": model,
        "status": response.get("status", "pending"),
        "pollingUrl": response.get("polling_url"),
        "request": payload,
        "approvalId": approval["id"],
        "submittedAt": now,
        "updatedAt": now,
        "usage": {},
        "artifacts": [],
    }
    write_job(root, job)
    return envelope(
        "/videos",
        model,
        job["status"],
        job,
        [],
        {},
        {"requestId": headers.get("X-Request-Id"), "generationId": None, "jobId": job_id},
        root=root,
        artifact_type="video-generation",
        input_data={"prompt": args.prompt},
    )


def video_poll(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    job = read_job(root, args.job_id)
    api_key = os.environ.get(config["apiKeyEnv"])
    if not api_key:
        raise AdapterError(f"missing {config['apiKeyEnv']}")
    polling_url = job.get("pollingUrl") or endpoint_url(config, f"/videos/{quote(job['id'])}")
    headers, response = request_json("GET", polling_url, None, api_key, transport)
    status = response.get("status")
    if status not in {"pending", "in_progress", "completed", "failed", "cancelled", "expired"}:
        raise AdapterError(f"unknown video status: {status!r}")
    job.update(
        {
            "status": status,
            "updatedAt": utc_now(),
            "usage": response.get("usage", job.get("usage", {})),
        }
    )
    if status == "completed":
        job["unsignedUrls"] = response.get("unsigned_urls", [])
    elif status in {"failed", "cancelled", "expired"}:
        job["error"] = response.get("error")
    write_job(root, job)
    return envelope(
        "/videos",
        job["model"],
        status,
        job,
        [],
        job.get("usage", {}),
        {"requestId": headers.get("X-Request-Id"), "generationId": response.get("generation_id"), "jobId": job["id"]},
        root=root,
        artifact_type="video-poll",
        input_data={"jobId": job["id"]},
    )


def video_download(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    job = read_job(root, args.job_id)
    if job.get("status") != "completed":
        raise AdapterError("video job is not completed")
    urls = job.get("unsignedUrls") or []
    if not urls:
        raise AdapterError("completed video job has no content URL")
    index = args.index
    if index >= len(urls):
        raise AdapterError(f"video index {index} out of range; available: 0..{len(urls) - 1}")
    api_key = os.environ.get(config["apiKeyEnv"])
    if not api_key:
        raise AdapterError(f"missing {config['apiKeyEnv']}")
    status, headers, data = http_bytes("GET", urls[index], api_key, transport)
    if not 200 <= status < 300:
        raise AdapterError(f"OpenRouter video download failed with HTTP {status}")
    artifact = save_bytes(root, "videos", data, "mp4")
    artifact["index"] = index
    job["artifacts"] = [artifact]
    job["downloadedAt"] = utc_now()
    write_job(root, job)
    return envelope(
        "/videos",
        job["model"],
        "completed",
        {"jobId": job["id"], "index": index},
        [artifact],
        job.get("usage", {}),
        {"requestId": None, "generationId": None, "jobId": job["id"]},
        root=root,
        artifact_type="video-download",
        input_data={"jobId": job["id"], "index": index},
    )


def chat_reading(
    config: dict[str, Any],
    api_key: str,
    model: str,
    question: str,
    part: dict[str, Any],
    transport,
    reasoning_details: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, str], dict[str, Any], dict[str, Any]]:
    messages: list[dict[str, Any]] = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                part,
            ],
        }
    ]
    if reasoning_details:
        messages.insert(
            0,
            {
                "role": "assistant",
                "content": "",
                "reasoning_details": reasoning_details,
            },
        )
    payload = {
        "model": model,
        "messages": messages,
    }
    headers, response = request_json(
        "POST", endpoint_url(config, "/chat/completions"), payload, api_key, transport
    )
    try:
        message = response["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AdapterError("OpenRouter returned no chat content") from exc
    return headers, response, message


def image_read(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    path = pathlib.Path(args.path)
    if not path.is_file():
        raise AdapterError(f"image not found: {path}")
    url, media_type, size = data_url(path, IMAGE_MIME_TYPES)
    limit = int(config.get("limits", {}).get("imageUploadBytes", 10 * 1024 * 1024))
    if size > limit:
        raise AdapterError(f"image exceeds upload limit of {limit} bytes")
    model = model_for(config, "imageUnderstanding", args.model)
    reasoning_details = read_reasoning_details(args.reasoning_file)
    approval = require_cloud_approval(args, config, root, path)
    if approval is None:
        return declined("/chat/completions", model, "cloud approval is required", {"path": str(path.resolve())})
    api_key = api_key_from(config)
    if config.get("validateCapabilities", True):
        validate_modality(
            find_model(fetch_models(config, "image-input", api_key, transport), model),
            input_modality="image",
        )
    headers, _, message = chat_reading(
        config,
        api_key,
        model,
        args.question,
        {"type": "image_url", "image_url": {"url": url}},
        transport,
        reasoning_details,
    )
    answer = message.get("content")
    return envelope(
        "/chat/completions",
        model,
        "completed",
        {"answer": answer},
        [],
        {},
        {"requestId": headers.get("X-Request-Id"), "generationId": headers.get("X-Generation-Id"), "jobId": None, "approvalId": approval["id"]},
        root=root,
        artifact_type="image-reading",
        input_data={
            "path": str(path.resolve()),
            "mediaType": media_type,
            "bytes": size,
            "question": args.question,
            "reasoningDetails": message.get("reasoning_details"),
        },
    )


def video_read(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    model = model_for(config, "videoUnderstanding", args.model)
    reasoning_details = read_reasoning_details(args.reasoning_file)
    if args.path and args.url:
        raise AdapterError("use either --path or --url, not both")
    if not args.path and not args.url:
        raise AdapterError("one of --path or --url is required")
    if args.path:
        path = pathlib.Path(args.path)
        if not path.is_file():
            raise AdapterError(f"video not found: {path}")
        url, media_type, size = data_url(path, VIDEO_MIME_TYPES)
        limit = int(config.get("limits", {}).get("videoDirectUploadBytes", 50 * 1024 * 1024))
        if size > limit:
            raise AdapterError(f"video exceeds direct upload limit of {limit} bytes")
        input_info = {
            "path": str(path.resolve()),
            "mediaType": media_type,
            "bytes": size,
            "question": args.question,
        }
    else:
        if not re.match(r"^https?://", args.url):
            raise AdapterError("video URL must be HTTP(S)")
        if model.startswith("google/gemini") and not "youtube.com" in args.url:
            raise AdapterError(
                "Google Gemini on AI Studio only supports YouTube video URLs; use a local file or provider routing"
            )
        url = args.url
        input_info = {"url": args.url, "question": args.question}

    approval = require_cloud_approval(args, config, root, path if args.path else None)
    if approval is None:
        return declined("/chat/completions", model, "cloud approval is required", input_info)
    api_key = api_key_from(config)
    if config.get("validateCapabilities", True):
        validate_modality(
            find_model(fetch_models(config, "video-input", api_key, transport), model),
            input_modality="video",
        )
    part: dict[str, Any] = {"type": "video_url", "video_url": {"url": url}}
    if args.processing:
        part["video_url"]["processing"] = args.processing
    headers, _, message = chat_reading(
        config, api_key, model, args.question, part, transport, reasoning_details
    )
    return envelope(
        "/chat/completions",
        model,
        "completed",
        {
            "answer": message.get("content"),
            "reasoningDetails": message.get("reasoning_details"),
        },
        [],
        {},
        {"requestId": headers.get("X-Request-Id"), "generationId": headers.get("X-Generation-Id"), "jobId": None, "approvalId": approval["id"]},
        root=root,
        artifact_type="video-reading",
        input_data={**input_info, "reasoningDetails": message.get("reasoning_details")},
    )


def audio_data(path: pathlib.Path) -> tuple[str, bytes, int]:
    media_type_for(path, AUDIO_MIME_TYPES)
    raw = path.read_bytes()
    extension = path.suffix.removeprefix(".").lower()
    return extension, base64.b64encode(raw).decode("ascii"), len(raw)


def audio_transcribe(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    path = pathlib.Path(args.path)
    if not path.is_file():
        raise AdapterError(f"audio file not found: {path}")
    audio_format, encoded, size = audio_data(path)
    limit = int(config.get("limits", {}).get("audioUploadBytes", 25 * 1024 * 1024))
    if size > limit:
        raise AdapterError(f"audio exceeds upload limit of {limit} bytes")
    model = model_for(config, "audioTranscription", args.model)
    approval = require_cloud_approval(args, config, root, path)
    if approval is None:
        return declined("/audio/transcriptions", model, "cloud approval is required", {"path": str(path.resolve())})
    api_key = api_key_from(config)
    if config.get("validateCapabilities", True):
        validate_modality(
            find_model(fetch_models(config, "transcription", api_key, transport), model),
            output_modality="transcription",
        )
    payload: dict[str, Any] = {
        "model": model,
        "input_audio": {"data": encoded, "format": audio_format},
        "response_format": "verbose_json",
        "timestamp_granularities": ["segment"],
    }
    if args.language:
        payload["language"] = args.language
    headers, response = request_json(
        "POST", endpoint_url(config, "/audio/transcriptions"), payload, api_key, transport
    )
    return envelope(
        "/audio/transcriptions",
        model,
        "completed",
        response,
        [],
        response.get("usage", {}),
        {"requestId": headers.get("X-Request-Id"), "generationId": headers.get("X-Generation-Id"), "jobId": None, "approvalId": approval["id"]},
        root=root,
        artifact_type="audio-transcription",
        input_data={"path": str(path.resolve()), "format": audio_format, "bytes": size},
    )


def audio_read(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    path = pathlib.Path(args.path)
    if not path.is_file():
        raise AdapterError(f"audio file not found: {path}")
    audio_format, encoded, size = audio_data(path)
    limit = int(config.get("limits", {}).get("audioUploadBytes", 25 * 1024 * 1024))
    if size > limit:
        raise AdapterError(f"audio exceeds upload limit of {limit} bytes")
    model = model_for(config, "audioAnalysis", args.model)
    approval = require_cloud_approval(args, config, root, path)
    if approval is None:
        return declined("/chat/completions", model, "cloud approval is required", {"path": str(path.resolve())})
    api_key = api_key_from(config)
    if config.get("validateCapabilities", True):
        validate_modality(
            find_model(fetch_models(config, "audio-input", api_key, transport), model),
            input_modality="audio",
        )
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": args.question},
                    {"type": "input_audio", "input_audio": {"data": encoded, "format": audio_format}},
                ],
            }
        ],
    }
    headers, response = request_json(
        "POST", endpoint_url(config, "/chat/completions"), payload, api_key, transport
    )
    try:
        answer = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AdapterError("OpenRouter returned no chat content") from exc
    return envelope(
        "/chat/completions",
        model,
        "completed",
        {"answer": answer},
        [],
        response.get("usage", {}),
        {"requestId": headers.get("X-Request-Id"), "generationId": headers.get("X-Generation-Id"), "jobId": None, "approvalId": approval["id"]},
        root=root,
        artifact_type="audio-reading",
        input_data={"path": str(path.resolve()), "format": audio_format, "bytes": size, "question": args.question},
    )


def text_generate(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    model = model_for(config, "textGeneration", args.model)
    approval = require_cloud_approval(args, config, root, None)
    if approval is None:
        return declined("/chat/completions", model, "cloud approval is required; set LOCAL_AGENT_PACK_ALLOW_CLOUD=1")
    api_key = api_key_from(config)
    if config.get("validateCapabilities", True):
        validate_modality(
            find_model(fetch_models(config, "text", api_key, transport), model),
            input_modality="text",
            output_modality="text",
        )
    content: Any = args.prompt
    if args.file:
        path = pathlib.Path(args.file)
        if not path.is_file():
            raise AdapterError(f"input file not found: {path}")
        content = path.read_text(encoding="utf-8")
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
    }
    optional = {"temperature": args.temperature, "max_tokens": args.max_tokens, "seed": args.seed}
    for key, value in optional.items():
        if value is not None:
            payload[key] = value
    provider_options = parse_provider_options(args.provider_options)
    if provider_options is not None:
        payload["provider"] = provider_options
    headers, response = request_json(
        "POST", endpoint_url(config, "/chat/completions"), payload, api_key, transport
    )
    try:
        message = response["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AdapterError("OpenRouter returned no chat content") from exc
    return envelope(
        "/chat/completions",
        model,
        "completed",
        {"answer": message.get("content"), "reasoningDetails": message.get("reasoning_details")},
        [],
        response.get("usage", {}),
        {"requestId": headers.get("X-Request-Id"), "generationId": headers.get("X-Generation-Id"), "jobId": None, "approvalId": approval["id"]},
        root=root,
        artifact_type="text-generation",
        input_data={"prompt": args.prompt, "file": args.file},
    )


def audio_generate(args: argparse.Namespace, transport) -> dict[str, Any]:
    config = load_config(args.config)
    root = storage_root(args, config)
    model = model_for(config, "audioGeneration", args.model)
    approval = require_cloud_approval(args, config, root, None)
    if approval is None:
        return declined("/audio/speech", model, "cloud approval is required; set LOCAL_AGENT_PACK_ALLOW_CLOUD=1")
    api_key = api_key_from(config)
    if config.get("validateCapabilities", True):
        validate_modality(
            find_model(fetch_models(config, "speech", api_key, transport), model),
            input_modality="text",
            output_modality="speech",
        )
    payload: dict[str, Any] = {"model": model, "input": args.input}
    optional = {"voice": args.voice, "response_format": args.response_format, "speed": args.speed}
    for key, value in optional.items():
        if value is not None:
            payload[key] = value
    provider_options = parse_provider_options(args.provider_options)
    if provider_options is not None:
        payload["provider"] = provider_options
    body = json.dumps(payload).encode("utf-8")
    headers_dict = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/octet-stream",
    }
    response = transport.request("POST", endpoint_url(config, "/audio/speech"), body=body, headers=headers_dict)
    if not 200 <= response.status < 300:
        raise AdapterError(f"OpenRouter TTS failed with HTTP {response.status}: {response.text}")
    response_format = args.response_format or "mp3"
    if response_format not in {"mp3", "pcm"}:
        raise AdapterError("TTS response_format must be mp3 or pcm")
    artifact = save_bytes(root, "audio", response.body, response_format)
    headers = {key.lower(): value for key, value in response.headers.items()}
    generation_id = headers.get("x-generation-id")
    return envelope(
        "/audio/speech",
        model,
        "completed",
        {"format": response_format},
        [artifact],
        {},
        {"requestId": headers.get("x-request-id"), "generationId": generation_id, "jobId": None, "approvalId": approval["id"]},
        root=root,
        artifact_type="audio-generation",
        input_data={"input": args.input, "voice": args.voice, "format": response_format},
    )


def default_transport():
    class UrllibTransport:
        def request(self, method: str, url: str, body: bytes | None, headers: dict[str, str]) -> HttpResponse:
            request = urllib.request.Request(url, data=body, headers=headers, method=method)
            try:
                with urllib.request.urlopen(request, timeout=300) as response:
                    data = response.read()
                    return HttpResponse(
                        response.status,
                        {key.lower(): value for key, value in response.headers.items()},
                        data,
                        data.decode("utf-8", errors="replace"),
                    )
            except urllib.error.HTTPError as error:
                data = error.read()
                return HttpResponse(
                    error.code,
                    {key.lower(): value for key, value in error.headers.items()},
                    data,
                    data.decode("utf-8", errors="replace"),
                )

    return UrllibTransport()


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=pathlib.Path, default=CONFIG_PATH)
    parser.add_argument("--storage-root", type=pathlib.Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    commands: dict[str, argparse.ArgumentParser] = {}
    for name, help_text in [
        ("image-generate", "Generate an image"),
        ("models-list", "List models for a capability surface"),
        ("model-show", "Show a model's capability metadata"),
        ("video-submit", "Submit a video generation job"),
        ("video-poll", "Poll a video generation job"),
        ("video-download", "Download a completed video"),
        ("text-generate", "Generate text"),
        ("audio-generate", "Generate speech audio"),
        ("image-read", "Answer a question about an image"),
        ("video-read", "Answer a question about a video"),
        ("audio-transcribe", "Transcribe an audio file"),
        ("audio-read", "Answer a question about an audio file"),
    ]:
        child = subparsers.add_parser(name, help=help_text)
        add_common_arguments(child)
        commands[name] = child

    image = commands["image-generate"]
    image.add_argument("--prompt", required=True)
    image.add_argument("--model")
    image.add_argument("--aspect-ratio")
    image.add_argument("--resolution")
    image.add_argument("--quality")
    image.add_argument("--output-format")
    image.add_argument("--background")
    image.add_argument("--seed", type=int)
    image.add_argument("--count", type=int)
    image.add_argument("--reference", action="append")
    image.add_argument("--provider-options")

    models = commands["models-list"]
    models.add_argument("--surface", choices=sorted(MODEL_SURFACE_PATHS), default="all")

    model = commands["model-show"]
    model.add_argument("--model", required=True)
    model.add_argument("--surface", choices=sorted(MODEL_SURFACE_PATHS), default="all")

    video_submit_parser = commands["video-submit"]
    video_submit_parser.add_argument("--prompt", required=True)
    video_submit_parser.add_argument("--model")
    video_submit_parser.add_argument("--duration", type=int)
    video_submit_parser.add_argument("--resolution")
    video_submit_parser.add_argument("--aspect-ratio")
    video_submit_parser.add_argument("--first-frame")
    video_submit_parser.add_argument("--last-frame")
    video_submit_parser.add_argument("--reference")
    video_submit_parser.add_argument("--no-audio", action="store_true")
    video_submit_parser.add_argument("--provider-options")

    text = commands["text-generate"]
    text.add_argument("--prompt")
    text.add_argument("--file")
    text.add_argument("--model")
    text.add_argument("--temperature", type=float)
    text.add_argument("--max-tokens", type=int)
    text.add_argument("--seed", type=int)
    text.add_argument("--provider-options")

    speech = commands["audio-generate"]
    speech.add_argument("--input", required=True)
    speech.add_argument("--model")
    speech.add_argument("--voice")
    speech.add_argument("--response-format", choices=["mp3", "pcm"])
    speech.add_argument("--speed", type=float)
    speech.add_argument("--provider-options")

    poll = commands["video-poll"]
    poll.add_argument("--job-id", required=True)

    download = commands["video-download"]
    download.add_argument("--job-id", required=True)
    download.add_argument("--index", type=int, default=0)

    image_reading = commands["image-read"]
    image_reading.add_argument("--path", required=True)
    image_reading.add_argument("--question", required=True)
    image_reading.add_argument("--model")
    image_reading.add_argument("--reasoning-file")

    video_reading = commands["video-read"]
    video_reading.add_argument("--path")
    video_reading.add_argument("--url")
    video_reading.add_argument("--question", required=True)
    video_reading.add_argument("--model")
    video_reading.add_argument("--processing", choices=["agentic", "static"])
    video_reading.add_argument("--reasoning-file")

    transcription = commands["audio-transcribe"]
    transcription.add_argument("--path", required=True)
    transcription.add_argument("--model")
    transcription.add_argument("--language")

    audio_reading = commands["audio-read"]
    audio_reading.add_argument("--path", required=True)
    audio_reading.add_argument("--question", required=True)
    audio_reading.add_argument("--model")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    transport = default_transport()
    handlers = {
        "image-generate": image_generate,
        "models-list": models_list,
        "model-show": model_show,
        "video-submit": video_submit,
        "video-poll": video_poll,
        "video-download": video_download,
        "text-generate": text_generate,
        "audio-generate": audio_generate,
        "image-read": image_read,
        "video-read": video_read,
        "audio-transcribe": audio_transcribe,
        "audio-read": audio_read,
    }
    try:
        result = handlers[args.command](args, transport)
    except AdapterError as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
