---
name: read-video
description: Understand, summarize, inspect, or answer questions about a local video using an OpenRouter video-capable model. Use when the user supplies a video file and asks what happens, wants key moments, asks about speech or scenes, or requests a timeline.
---

# Read Video

Use `scripts/openrouter.py video-read`.

Required:

- `--path`
- `--url`
- `--question`

Workflow:

1. Read local video metadata and size first.
2. Use the direct upload path only within the configured size limit.
3. For larger videos, use local extraction and transcription instead of silently uploading.
4. Require explicit cloud approval.
5. Encode local files as `data:{mime};base64,...`.
6. For Google Gemini public URLs, use YouTube only; other URLs are rejected.
7. For follow-up questions, pass the previous result JSON with `--reasoning-file`; this resumes Gemini agentic reasoning safely.
8. Return the structured answer with limitations; do not invent scenes.
