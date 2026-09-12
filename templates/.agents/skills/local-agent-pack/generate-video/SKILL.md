---
name: generate-video
description: Generate video clips through OpenRouter's asynchronous video API. Use when the user asks for a video, animated clip, image-to-video, reference-to-video, storyboard-to-video, or short product animation. Persists job state and downloads the completed clip locally.
---

# Generate Video

Use:

```bash
scripts/openrouter.py video-submit
scripts/openrouter.py video-poll
scripts/openrouter.py video-download
```

Common generation options:

- `--first-frame`
- `--last-frame`
- `--reference`
- `--duration`
- `--resolution`
- `--aspect-ratio`
- `--no-audio`

Required for submit:

- `--prompt`

Common options:

- `--model`
- `--duration`
- `--resolution`
- `--aspect-ratio`
- `--first-frame`
- `--reference`
- `--no-audio`

Workflow:

1. Read `references/openrouter.md`.
2. Check the model's supported durations, resolutions, and aspect ratios.
3. Submit once and persist the returned job state.
4. Poll at the configured interval; do not submit duplicate jobs.
5. Download only after `completed`.
6. Validate the MP4 with `ffprobe` before reporting success.
