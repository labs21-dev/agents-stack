---
name: generate-image
description: Generate or edit raster images with OpenRouter. Use when the user asks to create, draw, illustrate, or restyle an image, icon, mockup, product photo, or reference-guided image edit. Phase 1 routes through the pack's OpenRouter adapter and saves validated image artifacts locally.
---

# Generate Image

Use `scripts/openrouter.py image-generate`.

Required:

- `--prompt`

Common options:

- `--aspect-ratio`
- `--resolution`
- `--quality`
- `--output-format`
- `--reference`
- `--seed`
- `--output`

Workflow:

1. Read `references/openrouter.md`.
2. Confirm local cloud approval before uploading a reference image.
3. Build the prompt, then call the adapter.
4. Treat the returned JSON as the result contract.
5. Never claim success unless `status` is `completed` and `artifacts[0].path` exists.