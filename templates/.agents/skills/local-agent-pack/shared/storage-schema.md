# Storage Schema

The pack uses two compatible storage scopes. The default is project-local; the
global root is opt-in and is intended only for state that should be shared
across projects.

## Roots

### Project-local (default)

```text
./.agents/
```

### User-global (opt-in)

```text
~/.agents/
```

Selection rules:

1. Use the project-local root unless the caller explicitly selects a global
   root with `--storage-root ~/.agents` or a config override.
2. `~/.agents/skills/` belongs to installed agent skills and is never managed,
   overwritten, or pruned by pack runtime state.
3. Pack runtime state uses the same child directories under either root, except
   `skills/`, which is reserved for skill installation.

## Runtime layout

```text
<storage-root>/
  media/
    images/
    videos/
    audio/
  artifacts/{YYYYMMDD}/{id}.json
  jobs/videos/{jobId}.json
  approvals/{id}.json
  indexes/rag/rag.sqlite3
  memory/memory.sqlite
```

For the default scope, paths look like:

```text
./.agents/media/images/
./.agents/media/videos/
./.agents/media/audio/
./.agents/artifacts/{YYYYMMDD}/{id}.json
./.agents/jobs/videos/{jobId}.json
./.agents/approvals/{id}.json
./.agents/indexes/rag/rag.sqlite3
./.agents/memory/memory.sqlite
```

For the global scope, replace `./.agents/` with `~/.agents/`.

## Artifact JSON

```text
<storage-root>/artifacts/{YYYYMMDD}/{id}.json
```

Required:

```json
{
  "id": "artifact-id",
  "type": "image-generation",
  "provider": "openrouter",
  "endpoint": "/images",
  "model": "model-slug",
  "input": {},
  "output": {},
  "artifacts": [],
  "usage": {},
  "provenance": {},
  "createdAt": "RFC3339"
}
```

## Video Jobs

```text
<storage-root>/jobs/videos/{jobId}.json
```

Required:

```json
{
  "id": "jobId",
  "provider": "openrouter",
  "endpoint": "/videos",
  "model": "model-slug",
  "status": "pending",
  "pollingUrl": "https://openrouter.ai/api/v1/videos/jobId",
  "request": {},
  "submittedAt": "RFC3339",
  "updatedAt": "RFC3339"
}
```

## Approval Records

```text
<storage-root>/approvals/{id}.json
```

Required:

```json
{
  "provider": "openrouter",
  "kind": "upload",
  "path": "absolute-path",
  "bytes": 123,
  "approvedAt": "RFC3339"
}

## RAG Index

```text
<storage-root>/indexes/rag/rag.sqlite3
```

Tables:

- `files`: relative path, size, mtime, SHA-256, language, indexed timestamp
- `chunks`: source file, character offsets, heading breadcrumb, language, text
- `chunks_fts`: FTS5 trigram index over text, path, heading, and language
- `meta`: index metadata such as `lastIndexedAt`

Query output must retain:

```json
{
  "path": "docs/x.md",
  "start": 10,
  "end": 220,
  "heading": "Overview / Usage",
  "language": "markdown",
  "score": 0.03278689,
  "text": "..."
}
```

The SQLite database is generated local state and must not be committed. An index
may live in the global scope only when its corpus and citations are safe to
reuse across projects.
