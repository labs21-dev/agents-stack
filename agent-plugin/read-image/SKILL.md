---
name: read-image
description: Understand, describe, OCR, inspect, or answer questions about a local image using an OpenRouter vision model. Use when the user provides an image and asks what it shows, what text it contains, whether a UI is wrong, or what a chart means.
---

# Read Image

Use `scripts/openrouter.py image-read`.

Required:

- `--path`
- `--question`

Optional:

- `--model`
- `--reasoning-file` for a follow-up that reuses prior reasoning state

Workflow:

1. Read local image dimensions and MIME type first.
2. Enforce the upload size gate.
3. Require explicit cloud approval.
4. Encode local files as `data:{mime};base64,...`.
5. Return the adapter's structured answer and cite the local input path.

If cloud approval is unavailable, provide local metadata only and explicitly state that visual understanding was not performed.
