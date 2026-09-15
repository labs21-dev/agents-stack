---
name: generate-audio
description: Generate spoken audio through OpenRouter text-to-speech. Use when the user asks to synthesize speech, narrate text, create a voiceover, or save a script as audio.
---

# Generate Audio

Use `scripts/openrouter.py audio-generate`.

Required:

- `--input`

Common options:

- `--model`
- `--voice`
- `--response-format mp3|pcm`
- `--speed`
- `--provider-options`

Workflow:

1. Pass the exact spoken text in `--input`.
2. Treat the returned JSON as the result contract.
3. Never claim success unless `status` is `completed` and `artifacts[0].path` exists and is playable.
