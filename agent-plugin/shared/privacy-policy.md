# Privacy Policy

1. Local metadata extraction is always allowed.
2. Uploading local media to OpenRouter requires explicit cloud approval.
3. The adapter refuses cloud requests when `AGENT_PLUGIN_ALLOW_CLOUD` is not `1`.
4. The API key is read from `OPENROUTER_API_KEY`; it is never written to artifacts, logs, jobs, or memory.
5. Upload the smallest viable media payload. Enforce configured size limits.
6. Record every approved upload in `.agents/approvals/`, or in the selected global storage root.
7. Video generation is not used when Zero Data Retention is required.
