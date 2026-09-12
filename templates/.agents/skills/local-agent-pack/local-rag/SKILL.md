---
name: local-rag
description: Build a local SQLite full-text index for project files and answer questions with path-backed citations. Use when the user asks to search local files, index a folder, answer from project documents, or find where a concept appears in the repo.
---

# Local RAG

Phase 1 defines the contract; the executable local index is Phase 2.

Workflow:

1. Validate `corpusPath`.
2. Ingest text-like project files and skip unsupported binaries with a report.
3. Chunk by paragraph while preserving source paths and character offsets.
4. Store chunks and FTS data locally in `.local-agent-pack/indexes/rag/`.
5. Retrieve with SQLite FTS5.
6. Answer only from returned chunks and include path, start, end, and score.
7. If there are no matches, return no citations rather than guessing.