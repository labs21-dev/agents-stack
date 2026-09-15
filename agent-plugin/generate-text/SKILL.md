---
name: generate-text
description: Generate text through an OpenRouter text model. Use when the user asks for a written answer, summary, rewrite, translation, structured draft, or project-specific generation that should use the pack's configured model.
---

# Generate Text

Use `scripts/openrouter.py text-generate`.

Required:

- One of `--prompt` or `--file`

Common options:

- `--model`
- `--temperature`
- `--max-tokens`
- `--seed`
- `--provider-options`

Workflow:

1. Put the full user request in `--prompt`; use `--file` for a document or long input.
2. Keep provider-specific settings in `--provider-options` as JSON.
3. Read the returned JSON envelope; use `output.answer` as the result.
4. Never claim success unless `status` is `completed`.
