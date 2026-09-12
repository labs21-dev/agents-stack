---
name: read-audio
description: Transcribe or analyze local audio through OpenRouter. Use when the user supplies an audio file and asks what it says, wants a transcript, requests timestamps, or asks about speaker intent or content.
---

# Read Audio

Use:

```bash
scripts/openrouter.py audio-transcribe
scripts/openrouter.py audio-read
```

`audio-transcribe` is the default for transcripts. `audio-read` is for audio reasoning and question answering.

Required:

- `--path`
- `--question` for `audio-read`

Workflow:

1. Read audio metadata and enforce the upload limit.
2. Require explicit cloud approval.
3. Prefer `audio-transcribe` with `verbose_json` when the output is a transcript.
4. Split long audio before upload rather than relying on provider timeout behavior.
5. Never fabricate a transcript when the request is declined or unavailable.