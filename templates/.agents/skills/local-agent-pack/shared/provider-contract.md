# Provider Contract

All Phase 1 skills call providers through one adapter surface:

```text
image.generate(prompt, options) -> Envelope
video.submit(prompt, options) -> Envelope
video.poll(jobId, options) -> Envelope
video.download(jobId, options) -> Envelope
image.read(path, question, options) -> Envelope
video.read(path, question, options) -> Envelope
audio.transcribe(path, options) -> Envelope
audio.read(path, question, options) -> Envelope
```

Every method returns:

```json
{
  "provider": "openrouter",
  "endpoint": "/images",
  "model": "model-slug",
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

Statuses:

- `completed`
- `pending`
- `in_progress`
- `failed`
- `declined`

The adapter owns request construction, media encoding, local saving, state persistence, and validation. Skills never call OpenRouter directly.