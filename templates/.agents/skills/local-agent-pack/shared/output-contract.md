# Output Contract

Every adapter response is a single JSON object. Agents must not replace it with prose alone.

Required fields:

- `provider`
- `endpoint`
- `model`
- `status`
- `artifacts`
- `usage`
- `provenance`

For completed media generation, `artifacts` must contain:

```json
{
  "type": "image",
  "path": "absolute-path",
  "mediaType": "image/png",
  "bytes": 123
}
```

For understanding output, the answer is in `output` and the source is in `input.path`.

Never report success unless:

1. HTTP status is success.
2. `status` is `completed`.
3. Generated media exists at the reported path.
4. Required validation completed without errors.