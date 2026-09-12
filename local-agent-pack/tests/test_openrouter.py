from __future__ import annotations

import base64
import importlib.util
import json
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "openrouter.py"
CONFIG = Path(__file__).resolve().parents[1] / "templates" / "openrouter.config.json"
spec = importlib.util.spec_from_file_location("local_agent_pack_openrouter", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class FakeTransport:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def request(self, method, url, body=None, headers=None):
        self.requests.append(
            {
                "method": method,
                "url": url,
                "body": json.loads(body.decode()) if body else None,
                "headers": headers,
            }
        )
        if not self.responses:
            raise AssertionError("unexpected extra HTTP request")
        return self.responses.pop(0)


def http_response(status=200, payload=None, body=b""):
    if payload is not None:
        body = json.dumps(payload).encode()
    return module.HttpResponse(
        status,
        {"x-request-id": "req_1", "x-generation-id": "gen_1"},
        body,
        body.decode(),
    )


def write_image(path: Path, content=b"image-bytes") -> Path:
    path.write_bytes(content)
    return path


def write_media(path: Path, content: bytes, suffix: str) -> Path:
    path.write_bytes(content)
    return path


def args_for(command: str, **overrides):
    defaults = {"config": CONFIG, "storage_root": None}
    if command == "image-read":
        defaults["reasoning_file"] = None
    if command == "video-read":
        defaults["reasoning_file"] = None
    if command == "video-submit":
        defaults["last_frame"] = None
    defaults.update(overrides)
    return type("Args", (), defaults)


def model_payload(records):
    return {"data": records}


def test_image_generate_saves_artifact_and_provenance(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    image_data = base64.b64encode(b"fake-png").decode()
    transport = FakeTransport(
        http_response(
            payload={
                "data": [
                    {
                        "id": "openai/gpt-image-1",
                        "architecture": {
                            "input_modalities": ["text"],
                            "output_modalities": ["image"],
                        },
                        "supported_parameters": {
                            "aspect_ratio": {"type": "enum", "values": ["16:9"]},
                            "resolution": {"type": "enum", "values": ["2K"]},
                        },
                    }
                ]
            }
        ),
        http_response(
            payload={
                "created": 123,
                "data": [{"b64_json": image_data, "media_type": "image/png"}],
                "usage": {"cost": 0.04},
            }
        )
    )
    args = args_for(
        "image-generate",
        prompt="a calm desk",
        aspect_ratio="16:9",
        resolution="2K",
        model=None,
        reference=None,
        provider_options=None,
        quality=None,
        output_format=None,
        background=None,
        seed=None,
        count=None,
    )
    result = module.image_generate(args, transport)

    assert result["status"] == "completed"
    assert result["provider"] == "openrouter"
    assert result["artifacts"][0]["path"].endswith(".png")
    assert Path(result["artifacts"][0]["path"]).read_bytes() == b"fake-png"
    assert Path(result["artifactRecord"]).is_file()
    assert json.loads(Path(result["artifactRecord"]).read_text())["usage"]["cost"] == 0.04

    assert len(transport.requests) == 2
    assert transport.requests[0]["url"].endswith("/images/models")
    request = transport.requests[1]
    assert request["method"] == "POST"
    assert request["url"] == "https://openrouter.ai/api/v1/images"
    assert request["body"] == {
        "model": "openai/gpt-image-1",
        "prompt": "a calm desk",
        "aspect_ratio": "16:9",
        "resolution": "2K",
    }
    assert request["headers"]["Authorization"] == "Bearer test-key"


def test_cloud_upload_is_declined_without_approval(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", raising=False)
    monkeypatch.chdir(tmp_path)
    image = write_image(tmp_path / "input.png")
    args = args_for("image-read", path=image, question="What is this?", model=None)
    result = module.image_read(args, FakeTransport(http_response()))

    assert result["status"] == "declined"
    assert "cloud approval" in result["output"]["reason"]
    assert not list((tmp_path / ".agents" / "approvals").glob("*.json"))


def test_image_read_builds_vision_chat_request(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    image = write_image(tmp_path / "input.png", b"png-data")
    transport = FakeTransport(
        http_response(
            payload={
                "data": [
                    {
                        "id": "google/gemini-3-flash-preview",
                        "architecture": {
                            "input_modalities": ["text", "image"],
                            "output_modalities": ["text"],
                        },
                    }
                ]
            }
        ),
        http_response(
            payload={"choices": [{"message": {"content": "A small test image."}}]},
        )
    )
    config = json.loads(CONFIG.read_text())
    config_path = tmp_path / "openrouter.config.json"
    config_path.write_text(json.dumps(config))
    args = args_for("image-read", path=image, question="What is this?", model=None, config=config_path)
    result = module.image_read(args, transport)

    assert result["status"] == "completed"
    assert result["output"]["answer"] == "A small test image."
    assert len(transport.requests) == 2
    request = transport.requests[1]
    assert request["url"].endswith("/chat/completions")
    content = request["body"]["messages"][0]["content"]
    assert content[0]["type"] == "text"
    assert content[1]["type"] == "image_url"
    expected = "data:image/png;base64," + base64.b64encode(b"png-data").decode()
    assert content[1]["image_url"]["url"] == expected
    assert "test-key" not in Path(result["artifactRecord"]).read_text()


def test_video_submit_poll_download_state_machine(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)

    submit_transport = FakeTransport(
        http_response(
            payload={
                "data": [
                    {
                        "id": "google/veo-3.1",
                        "supported_durations": [5],
                        "generate_audio": True,
                    }
                ]
            }
        ),
        http_response(
            payload={
                "id": "job_123",
                "polling_url": "https://openrouter.ai/api/v1/videos/job_123",
                "status": "pending",
            }
        )
    )
    submit_args = args_for(
        "video-submit",
        prompt="a neon sign",
        duration=5,
        model=None,
        no_audio=False,
        resolution=None,
        aspect_ratio=None,
        first_frame=None,
        reference=None,
        provider_options=None,
    )
    submitted = module.video_submit(submit_args, submit_transport)
    assert submitted["status"] == "pending"
    job_path = tmp_path / ".agents" / "jobs" / "videos" / "job_123.json"
    assert json.loads(job_path.read_text())["status"] == "pending"
    assert len(submit_transport.requests) == 2
    assert submit_transport.requests[1]["body"]["generate_audio"] is True

    poll_transport = FakeTransport(
        http_response(
            payload={
                "id": "job_123",
                "status": "completed",
                "generation_id": "gen_video",
                "unsigned_urls": ["https://openrouter.ai/api/v1/videos/job_123/content?index=0"],
                "usage": {"cost": 0.25},
            }
        )
    )
    poll_args = args_for("video-poll", job_id="job_123")
    polled = module.video_poll(poll_args, poll_transport)
    assert polled["status"] == "completed"
    assert json.loads(job_path.read_text())["unsignedUrls"][0].endswith("index=0")
    assert poll_transport.requests[0]["method"] == "GET"

    download_transport = FakeTransport(http_response(body=b"video-bytes"))
    download_args = args_for("video-download", job_id="job_123", index=0)
    downloaded = module.video_download(download_args, download_transport)
    assert downloaded["artifacts"][0]["path"].endswith(".mp4")
    assert Path(downloaded["artifacts"][0]["path"]).read_bytes() == b"video-bytes"
    assert json.loads(job_path.read_text())["status"] == "completed"


def test_audio_transcription_uses_verbose_json(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    audio = write_media(tmp_path / "meeting.mp3", b"audio-bytes", ".mp3")
    transport = FakeTransport(
        http_response(
            payload={
                "data": [
                    {
                        "id": "openai/whisper-large-v3",
                        "architecture": {
                            "input_modalities": ["audio"],
                            "output_modalities": ["transcription"],
                        },
                    }
                ]
            }
        ),
        http_response(
            payload={
                "text": "hello",
                "segments": [{"id": 0, "start": 0, "end": 1, "text": "hello"}],
                "usage": {"seconds": 1, "cost": 0.001},
            }
        )
    )
    args = args_for("audio-transcribe", path=audio, language="en", model=None)
    result = module.audio_transcribe(args, transport)

    assert result["output"]["text"] == "hello"
    assert len(transport.requests) == 2
    request = transport.requests[1]
    assert request["url"].endswith("/audio/transcriptions")
    assert request["body"]["response_format"] == "verbose_json"
    assert request["body"]["timestamp_granularities"] == ["segment"]
    assert request["body"]["input_audio"]["data"] == base64.b64encode(b"audio-bytes").decode()
    assert request["body"]["input_audio"]["format"] == "mp3"
    assert result["usage"]["cost"] == 0.001


def test_text_generate_saves_answer_and_usage(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    config = json.loads(CONFIG.read_text())
    config["validateCapabilities"] = False
    config_path = tmp_path / "openrouter.config.json"
    config_path.write_text(json.dumps(config))
    transport = FakeTransport(
        http_response(
            payload={
                "choices": [{"message": {"content": "A concise answer."}}],
                "usage": {"cost": 0.002},
            }
        )
    )
    args = args_for(
        "text-generate",
        prompt="Summarize this.",
        file=None,
        model=None,
        temperature=None,
        max_tokens=None,
        seed=None,
        provider_options='{"openai":{"instructions":"Be concise."}}',
        config=config_path,
    )
    result = module.text_generate(args, transport)

    assert result["status"] == "completed"
    assert result["output"]["answer"] == "A concise answer."
    assert result["usage"]["cost"] == 0.002
    request = transport.requests[0]
    assert request["url"].endswith("/chat/completions")
    assert request["body"]["messages"][0]["content"] == "Summarize this."
    assert request["body"]["provider"]["options"]["openai"]["instructions"] == "Be concise."


def test_audio_generate_saves_raw_audio(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    config = json.loads(CONFIG.read_text())
    config["validateCapabilities"] = False
    config_path = tmp_path / "openrouter.config.json"
    config_path.write_text(json.dumps(config))
    transport = FakeTransport(
        module.HttpResponse(
            200,
            {"X-Generation-Id": "gen_tts"},
            b"audio-bytes",
            "",
        )
    )
    args = args_for(
        "audio-generate",
        input="Hello from local-agent-pack.",
        model=None,
        voice="alloy",
        response_format="mp3",
        speed=None,
        provider_options=None,
        config=config_path,
    )
    result = module.audio_generate(args, transport)

    assert result["status"] == "completed"
    assert result["artifacts"][0]["path"].endswith(".mp3")
    assert Path(result["artifacts"][0]["path"]).read_bytes() == b"audio-bytes"
    assert result["provenance"]["generationId"] == "gen_tts"
    assert transport.requests[0]["url"].endswith("/audio/speech")


def test_video_capability_validation_rejects_unsupported_duration(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    model_record = {
        "id": "bytedance/seedance-2.0",
        "generate_audio": True,
        "supported_durations": [4, 8],
        "supported_resolutions": ["720p"],
        "supported_aspect_ratios": ["16:9"],
    }
    transport = FakeTransport(http_response(payload=model_payload([model_record])))
    with pytest.raises(module.AdapterError, match="durations"):
        module.validate_video_capabilities(
            model_record,
            args_for("video-submit", duration=5, resolution="720p", aspect_ratio="16:9", first_frame=None),
        )


def test_gemini_video_url_requires_youtube(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    config = json.loads(CONFIG.read_text())
    config["validateCapabilities"] = False
    config_path = tmp_path / "openrouter.config.json"
    config_path.write_text(json.dumps(config))
    args = args_for(
        "video-read",
        path=None,
        url="https://example.com/video.mp4",
        question="What happens?",
        model="google/gemini-2.5-flash",
        processing="agentic",
        config=config_path,
    )
    with pytest.raises(module.AdapterError, match="YouTube"):
        module.video_read(args, FakeTransport(http_response()))


def test_gemini_video_read_preserves_reasoning_details(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    config = json.loads(CONFIG.read_text())
    config["validateCapabilities"] = False
    config_path = tmp_path / "openrouter.config.json"
    config_path.write_text(json.dumps(config))
    video = write_media(tmp_path / "clip.mp4", b"video-data", ".mp4")
    reasoning = [{"type": "encrypted_reasoning", "data": "encrypted"}]
    transport = FakeTransport(
        http_response(
            payload={
                "choices": [
                    {
                        "message": {
                            "content": "A dark city scene.",
                            "reasoning_details": reasoning,
                        }
                    }
                ]
            }
        )
    )
    args = args_for(
        "video-read",
        path=video,
        url=None,
        question="What happens?",
        model="google/gemini-2.5-flash",
        processing="agentic",
        config=config_path,
    )
    result = module.video_read(args, transport)

    assert result["output"]["answer"] == "A dark city scene."
    assert result["output"]["reasoningDetails"] == reasoning
    request = transport.requests[0]
    assert request["body"]["messages"][0]["content"][1]["video_url"]["processing"] == "agentic"


def test_video_download_requires_completed_job(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.chdir(tmp_path)
    job_dir = tmp_path / ".agents" / "jobs" / "videos"
    job_dir.mkdir(parents=True)
    (job_dir / "job_pending.json").write_text(json.dumps({"id": "job_pending", "status": "pending", "model": "m"}))
    args = args_for("video-download", job_id="job_pending", index=0)
    with pytest.raises(module.AdapterError, match="not completed"):
        module.video_download(args, FakeTransport(http_response()))


def test_upload_size_gate(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    image = write_image(tmp_path / "large.png", b"x" * 11)
    config = json.loads(CONFIG.read_text())
    config["limits"]["imageUploadBytes"] = 10
    config_path = tmp_path / "openrouter.config.json"
    config_path.write_text(json.dumps(config))
    args = args_for(
        "image-read",
        path=image,
        question="What is this?",
        model=None,
        config=config_path,
    )
    with pytest.raises(module.AdapterError, match="exceeds upload limit"):
        module.image_read(args, FakeTransport(http_response()))


def test_models_list_and_show_use_discovery(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    config = json.loads(CONFIG.read_text())
    config_path = tmp_path / "openrouter.config.json"
    config_path.write_text(json.dumps(config))
    record = {
        "id": "bytedance/seedance-2.0",
        "name": "Seedance 2.0",
        "allowed_passthrough_parameters": ["safety_tolerance"],
    }
    transport = FakeTransport(
        http_response(payload=model_payload([record])),
        http_response(payload=model_payload([record])),
    )

    listed = module.models_list(args_for("models-list", surface="video-generation", config=config_path), transport)
    shown = module.model_show(
        args_for("model-show", model="bytedance/seedance-2.0", surface="video-generation", config=config_path),
        transport,
    )

    assert listed["models"][0]["id"] == "bytedance/seedance-2.0"
    assert shown["model"]["allowed_passthrough_parameters"] == ["safety_tolerance"]
    assert all(request["url"].endswith("/videos/models") for request in transport.requests)


def test_provider_passthrough_is_rejected_before_paid_request():
    model_record = {"id": "bytedance/seedance-2.0", "allowed_passthrough_parameters": ["safety_tolerance"]}
    with pytest.raises(module.AdapterError, match="not allow provider passthrough parameters: seed"):
        module.validate_provider_passthrough(
            model_record,
            module.parse_provider_options('{"seed": 123}'),
        )


def test_image_reference_count_and_modality_are_validated():
    model_record = {
        "id": "test/image",
        "architecture": {
            "input_modalities": ["text", "image"],
            "output_modalities": ["image"],
        },
        "supported_parameters": {
            "input_references": {"type": "range", "min": 0, "max": 1},
        },
    }
    with pytest.raises(module.AdapterError, match="image references"):
        module.validate_image_capabilities(
            model_record,
            {"input_references": [{}, {}]},
        )

    text_only_record = {
        "id": "test/text-image",
        "architecture": {
            "input_modalities": ["text"],
            "output_modalities": ["image"],
        },
        "supported_parameters": {
            "input_references": {"type": "range", "min": 1, "max": 1},
        },
    }
    with pytest.raises(module.AdapterError, match="does not accept image input"):
        module.validate_image_capabilities(
            text_only_record,
            {"input_references": [{}]},
        )


def test_video_last_frame_capability_is_validated(tmp_path):
    first = write_image(tmp_path / "first.png", b"first")
    last = write_image(tmp_path / "last.png", b"last")
    args = args_for(
        "video-submit",
        duration=None,
        resolution=None,
        aspect_ratio=None,
        first_frame=first,
        last_frame=last,
        no_audio=True,
    )
    module.validate_video_capabilities(
        {"id": "test/video", "generate_audio": True, "supported_frame_images": ["first_frame", "last_frame"]},
        args,
    )

    with pytest.raises(module.AdapterError, match="last-frame"):
        module.validate_video_capabilities(
            {"id": "test/video", "generate_audio": True, "supported_frame_images": ["first_frame"]},
            args_for(
                "video-submit",
                duration=None,
                resolution=None,
                aspect_ratio=None,
                first_frame=None,
                last_frame=last,
                no_audio=True,
            ),
        )

    with pytest.raises(module.AdapterError, match="different files"):
        module.validate_video_capabilities(
            {"id": "test/video", "generate_audio": True, "supported_frame_images": ["first_frame", "last_frame"]},
            args_for(
                "video-submit",
                duration=None,
                resolution=None,
                aspect_ratio=None,
                first_frame=first,
                last_frame=first,
                no_audio=True,
            ),
        )


def test_video_capability_validation_rejects_unsupported_audio():
    model_record = {"id": "test/video", "generate_audio": False}
    with pytest.raises(module.AdapterError, match="generated audio"):
        module.validate_video_capabilities(
            model_record,
            args_for(
                "video-submit",
                duration=None,
                resolution=None,
                aspect_ratio=None,
                first_frame=None,
                no_audio=False,
            ),
        )


def test_video_reasoning_file_round_trip(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("LOCAL_AGENT_PACK_ALLOW_CLOUD", "1")
    monkeypatch.chdir(tmp_path)
    config = json.loads(CONFIG.read_text())
    config["validateCapabilities"] = False
    config_path = tmp_path / "openrouter.config.json"
    config_path.write_text(json.dumps(config))
    video = write_media(tmp_path / "clip.mp4", b"video-data", ".mp4")
    prior = tmp_path / "prior.json"
    prior.write_text(json.dumps({"output": {"reasoningDetails": [{"type": "encrypted_reasoning", "data": "x"}]}}))
    transport = FakeTransport(
        http_response(
            payload={
                "choices": [
                    {
                        "message": {
                            "content": "Follow-up answer.",
                            "reasoning_details": [{"type": "encrypted_reasoning", "data": "y"}],
                        }
                    }
                ]
            }
        )
    )
    args = args_for(
        "video-read",
        path=video,
        url=None,
        question="What changed?",
        model=None,
        processing="agentic",
        reasoning_file=prior,
        config=config_path,
    )

    result = module.video_read(args, transport)

    messages = transport.requests[0]["body"]["messages"]
    assert messages[0] == {
        "role": "assistant",
        "content": "",
        "reasoning_details": [{"type": "encrypted_reasoning", "data": "x"}],
    }
    assert result["output"]["reasoningDetails"] == [{"type": "encrypted_reasoning", "data": "y"}]
