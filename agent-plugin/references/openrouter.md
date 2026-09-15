# OpenRouter Phase 1 Adapter

> Phase 1 只做 OpenRouter。其他 provider 之後透過同一個 adapter contract 接入。
> 所有請求使用 `Authorization: Bearer $OPENROUTER_API_KEY`。

## Base

```text
https://openrouter.ai/api/v1
```

## Endpoint map

| Pack skill | OpenRouter surface | Phase 1 default |
|---|---|---|
| `generate-image` | `POST /images` | Dedicated Image API |
| `generate-video` | `POST /videos` -> poll -> download | Dedicated async Video API |
| `read-image` | `POST /chat/completions` with `image_url` | Vision model via Chat Completions |
| `read-video` | `POST /chat/completions` with `video_url` | Video model via Chat Completions |
| `read-audio` | `POST /audio/transcriptions` | Dedicated STT API |
| `generate-text` | `POST /chat/completions` | Text model |
| `read-audio` (analysis mode) | `POST /chat/completions` with `input_audio` | Audio-capable model |
| `generate-audio` | `POST /audio/speech` | Dedicated TTS API |

### Model discovery

```text
GET /models
GET /images/models
GET /videos/models
GET /models?input_modalities=image
GET /models?input_modalities=video
GET /models?input_modalities=audio
GET /models?output_modalities=text
GET /models?output_modalities=speech
GET /models?output_modalities=transcription
```

CLI surfaces:

```bash
scripts/openrouter.py models-list --surface all
scripts/openrouter.py models-list --surface video-generation
scripts/openrouter.py model-show --model google/veo-3.1 --surface video-generation
```

Use discovery before generation. Do not hardcode model capabilities; model and provider support differ.
The adapter validates input/output modalities, image parameters, video duration/resolution/aspect ratio,
first/last-frame input, image reference count, generated audio, and provider passthrough keys before paid requests.

Input-reference matrix:

| Input | Output | Adapter support | Capability source |
|---|---|---|---|
| text | image | Yes | `architecture.input_modalities` |
| image | image | Yes | `architecture.input_modalities` + `supported_parameters.input_references` |
| text | video | Yes | `/videos/models` generation request |
| image | video | Yes | `supported_frame_images` and provider routing |

Image-to-video has two forms:

- `--first-frame` maps to `frame_images[].frame_type = first_frame`.
- `--last-frame` maps to `frame_images[].frame_type = last_frame`.
- `--reference` maps to `input_references`; use it for reference-to-video where the selected model/provider supports it.
- A model that does not expose first/last-frame metadata is rejected before a paid request when frame input is requested.

OpenRouter Phase 1 does not expose a generic video reference endpoint for video-to-video editing. Models such as
FLUX Video Edit advertise video input in their descriptions, but the required video reference shape is still
provider-specific. Do not claim generic video-to-video support until OpenRouter exposes and documents that field.

Provider-specific values belong in:

```json
{"options": {"safety_tolerance": 2}}
```

When model metadata contains `allowed_passthrough_parameters`, unsupported keys are rejected locally.
Models without that field keep OpenRouter's default passthrough behavior.

## Authentication

```text
Authorization: Bearer $OPENROUTER_API_KEY
```

The API key is read from the environment. It is never copied into project files, logs, generated metadata, or memory records.

## Image generation

### Request

```text
POST /api/v1/images
```

```json
{
  "model": "openai/gpt-image-1",
  "prompt": "A calm product photo on a walnut desk",
  "n": 1,
  "resolution": "2K",
  "aspect_ratio": "16:9",
  "quality": "high",
  "output_format": "png",
  "seed": 123456
}
```

Supported options depend on the selected model and endpoint. `GET /images/models/{model}/endpoints` is the source of truth for:

- accepted parameters
- resolution and aspect-ratio values
- provider routing
- pricing
- allowed passthrough parameters

Reference images use `input_references`:

```json
{
  "input_references": [
    {
      "type": "image_url",
      "image_url": {
        "url": "data:image/png;base64,..."
      }
    }
  ]
}
```

### Response

```json
{
  "created": 1748372400,
  "data": [
    {
      "b64_json": "<base64>",
      "media_type": "image/png"
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 4175,
    "total_tokens": 4175,
    "cost": 0.04
  }
}
```

Normalization:

1. Decode `data[].b64_json`.
2. Save to `.agents/media/images/`.
3. Infer extension from `media_type`; do not trust the prompt for the file type.
4. Write metadata with model, provider, request parameters, usage, cost, and generation time.
5. Validate the image with `sips` or an equivalent decoder.

## Video generation

Video generation is asynchronous. The adapter must persist job state locally so the agent can stop and resume safely.

### Submit

```text
POST /api/v1/videos
```

```json
{
  "model": "google/veo-3.1",
  "prompt": "A cinematic push-in on a neon coffee-shop sign at night",
  "duration": 5,
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "generate_audio": true
}
```

Response:

```json
{
  "id": "abc123",
  "polling_url": "https://openrouter.ai/api/v1/videos/abc123",
  "status": "pending"
}
```

Persist immediately:

```json
{
  "id": "abc123",
  "polling_url": "https://openrouter.ai/api/v1/videos/abc123",
  "status": "pending",
  "model": "google/veo-3.1",
  "submittedAt": "2026-09-12T00:00:00Z"
}
```

### Poll

```text
GET /api/v1/videos/{jobId}
```

Default polling interval: 30 seconds.

Terminal states:

- `completed`
- `failed`
- `cancelled`
- `expired`

A completed job contains:

```json
{
  "id": "abc123",
  "status": "completed",
  "unsigned_urls": [
    "https://openrouter.ai/api/v1/videos/abc123/content?index=0"
  ],
  "usage": {
    "cost": 0.25,
    "is_byok": false
  }
}
```

### Download

```text
GET /api/v1/videos/{jobId}/content?index=0
```

The download still requires the OpenRouter Authorization header. Save the response bytes to:

```text
.agents/media/videos/{jobId}.mp4
```

Then validate with `ffprobe`:

- duration
- codec
- fps
- resolution
- audio stream presence when `generate_audio` was requested

Video generation is not eligible for OpenRouter Zero Data Retention. Do not send video generation requests when ZDR is enforced.

## Image reading

Use Chat Completions with a vision-capable model.

```text
POST /api/v1/chat/completions
```

```json
{
  "model": "google/gemini-3-flash-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Describe this image and list all visible text."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,..."
          }
        }
      ]
    }
  ]
}
```

Rules:

- Put the text prompt before the image content part.
- Local files use `data:{mime};base64,{bytes}`.
- Public files may use an HTTP(S) URL.
- Supported image MIME types include `image/png`, `image/jpeg`, `image/webp`, and `image/gif`.
- Before upload, inspect image dimensions and size; downscale only when needed.

## Video reading

Use Chat Completions with a video-capable model.

```text
POST /api/v1/chat/completions
```

```json
{
  "model": "google/gemini-2.5-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Summarize this video and give timestamps for key scenes."
        },
        {
          "type": "video_url",
          "video_url": {
            "url": "data:video/mp4;base64,...",
            "processing": "agentic"
          }
        }
      ]
    }
  ]
}
```

Rules:

- Local files use a base64 data URL.
- Public URL support varies by provider; Google Gemini AI Studio only accepts YouTube URLs.
- `processing` may be `agentic` or `static` where supported.
- Supported formats include `video/mp4`, `video/mpeg`, `video/mov`, and `video/webm`.
- For large local videos, prefer local extraction plus transcript first. Sending a full local video as base64 should be an explicit size-gated path, not the default.

## Audio reading

### Transcription mode

```text
POST /api/v1/audio/transcriptions
```

```json
{
  "model": "openai/whisper-large-v3",
  "input_audio": {
    "data": "<base64>",
    "format": "wav"
  },
  "response_format": "verbose_json",
  "timestamp_granularities": ["segment"]
}
```

Response:

```json
{
  "text": "Hello there.",
  "language": "en",
  "duration": 9.2,
  "segments": [
    {
      "id": 0,
      "start": 0,
      "end": 3.2,
      "text": "Hello there."
    }
  ],
  "usage": {
    "seconds": 9.2,
    "cost": 0.000508
  }
}
```

Rules:

- JSON requests require base64 bytes, not a data URI.
- For long recordings, split before upload; upstream processing can time out around 60 seconds.
- Prefer compressed input such as MP3 or Opus for long audio.
- Diarization is provider-specific and is passed through `provider.options`.

### Analysis mode

For question answering about audio, use Chat Completions:

```text
POST /api/v1/chat/completions
```

```json
{
  "model": "google/gemini-2.5-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is the speaker asking for?"
        },
        {
          "type": "input_audio",
          "input_audio": {
            "data": "<base64>",
            "format": "wav"
          }
        }
      ]
    }
  ]
}
```

Use STT for transcripts; use analysis mode only when the user needs interpretation, sentiment, speaker intent, or audio-specific reasoning.

## Optional audio generation

OpenRouter also exposes TTS. This is not one of the original seven skills, but it is a natural Phase 1 extension.

```text
POST /api/v1/audio/speech
```

```json
{
  "model": "openai/gpt-4o-mini-tts-2025-12-15",
  "input": "Hello from agent-plugin.",
  "voice": "alloy",
  "response_format": "mp3"
}
```

The response is raw audio bytes, not JSON. Save directly to:

```text
.agents/media/audio/{generationId}.mp3
```

Use the `X-Generation-Id` response header for provenance.

## Gemini compatibility notes

- Local video files are encoded as base64 data URLs.
- Public video URLs are only accepted for YouTube on the Google Gemini AI Studio route.
- `--processing agentic` or `static` is passed through when requested.
- Gemini agentic reasoning is preserved in `output.reasoningDetails`.
- For follow-up questions, pass the previous result JSON with `--reasoning-file`; the adapter sends it back as assistant `reasoning_details`.
- This round-trip is provider-dependent. If a provider rejects the preserved state, surface the provider error rather than silently dropping it.

## Normalized output envelope

Every OpenRouter call returns the same internal shape:

```json
{
  "provider": "openrouter",
  "endpoint": "/images",
  "model": "openai/gpt-image-1",
  "status": "completed",
  "artifacts": [],
  "usage": {},
  "provenance": {
    "requestId": null,
    "generationId": null,
    "jobId": null
  }
}
```

Artifact rules:

- Generated media is downloaded to the local media store.
- Understanding output is persisted as JSON in `.agents/artifacts/`.
- Every artifact records model, endpoint, request parameters, usage, cost, and creation time.
- API keys and full prompts containing secrets are never persisted.

## Error policy

| HTTP status | Meaning | Adapter behavior |
|---|---|---|
| `400` | Invalid request or unsupported model parameter | Surface the supported values from discovery metadata |
| `401` | Missing or invalid key | Stop and report configuration error |
| `402` | Insufficient credits | Stop and report billing issue |
| `413` | Payload too large | Compress, split, or downscale if possible |
| `429` | Rate limited | Retry with exponential backoff |
| `5xx` | Upstream/provider failure | Retry bounded, then report |
| `524` | Edge timeout | Retry bounded, then report |
| `529` | Provider overloaded | Retry bounded, then report |

Video polling has no request-payload retry loop. Poll until a terminal state, but keep a configurable maximum wait time.

## Privacy gate

OpenRouter is a cloud provider. Before any Phase 1 request that uploads local media:

1. Check `cloudApproval: explicit`.
2. Show what will be uploaded: file path, MIME type, size, model, and endpoint.
3. Do not upload if the environment forbids cloud providers.
4. Do not use OpenRouter for video generation when ZDR is required.
