---
name: local-rag
description: Build a local SQLite full-text index for project files and answer questions with path-backed citations. Use when the user asks to search local files, index a folder, answer from project documents, or find where a concept appears in the repo.
---

# Local RAG

Use `scripts/rag.py`.

Index a corpus:

```bash
scripts/rag.py index path/to/corpus
```

Retrieve path-backed chunks:

```bash
scripts/rag.py query "how does image capability validation work" --limit 8
scripts/rag.py query "OpenRouter" --path-filter docs/
```

Workflow:

1. Index the corpus first. Indexing is incremental and safe to rerun.
2. Treat the index as local state under `.agents/indexes/rag/` by default; do not commit it.
   Use `--storage-root ~/.agents` only when the index must be shared across projects.
3. Search with the hybrid BM25 plus exact-match query.
4. Read returned chunks before answering.
5. Cite `path`, `start`, `end`, heading, and score for every claim.
6. If there are no matches, return no citations rather than guessing.

Ingestion rules:

- Index UTF-8 text, Markdown, code, JSON, YAML, TOML, HTML, CSS, and SQL files.
- Skip binaries, ignored/generated directories, oversized files, and secret-like filenames.
- Markdown chunks preserve heading breadcrumbs.
- Chunk boundaries follow paragraphs and headings; no text is silently split mid-paragraph by default.
- The FTS5 trigram tokenizer supports mixed English and Chinese queries.
