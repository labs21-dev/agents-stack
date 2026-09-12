---
name: local-rag
description: Build a local SQLite index over text, documents, screenshots, images, audio, and video-derived text, then answer with source-backed citations. Use when the user asks to search local files, index a folder, answer from project documents, find a concept in the repo, or locate content inside media files.
---

# Local RAG

Use `scripts/rag.py`. One index serves every media type; extractors differ,
the chunk and citation contract stays the same.

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
5. Cite the source locator for every claim. For text, cite `path`, `start`,
   `end`, heading, and score. For media, cite the media locator such as a bbox
   or time range.
6. If there are no matches, return no citations rather than guessing.
7. Do not treat agent memory as corpus. Memory search belongs to agent-memory.

Ingestion rules:

- Phase 1 index UTF-8 text, Markdown, code, JSON, YAML, TOML, HTML, CSS, SQL,
  PDF/DOCX text, image metadata, screenshot OCR, and image OCR.
- Phase 2 adds audio metadata and transcript-derived chunks.
- Phase 3 adds video metadata, keyframe-derived OCR, and transcript chunks.
- Skip binaries, ignored/generated directories, oversized files, and secret-like filenames.
- Markdown chunks preserve heading breadcrumbs.
- Chunk boundaries follow paragraphs and headings; no text is silently split mid-paragraph by default.
- The FTS5 trigram tokenizer supports mixed English and Chinese queries.
- Media chunks must record extractor, extractor version, capability, and
  confidence. If an extractor is unavailable, index only safe metadata and
  report the degraded capability rather than inventing content.
- Optional visual embedding backends may be added later, but SQLite FTS5 and
  source locators remain the baseline and source of truth.
