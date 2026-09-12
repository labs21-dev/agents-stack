from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "rag.py"
spec = importlib.util.spec_from_file_location("local_agent_pack_rag", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def run_index(tmp_path: Path, corpus: Path, storage_root: Path):
    return module.index_corpus(
        type(
            "Args",
            (),
            {
                "corpus": corpus,
                "config": None,
                "storage_root": storage_root,
            },
        )
    )


def run_query(tmp_path: Path, query: str, storage_root: Path, path_filter: str | None = None):
    return module.query_index(
        type(
            "Args",
            (),
            {
                "query": query,
                "config": None,
                "storage_root": storage_root,
                "limit": 8,
                "path_filter": path_filter,
            },
        )
    )


def test_index_and_hybrid_query(tmp_path: Path):
    corpus = tmp_path / "corpus"
    docs = corpus / "docs"
    docs.mkdir(parents=True)
    write(
        docs / "guide.md",
        "# Guide\n\nOpenRouter supports capability validation.\n\n## Storage\n\nArtifacts are local JSON files.\n",
    )
    write(corpus / "app.py", "def validate_capability():\n    return 'openrouter'\n")
    write(corpus / "ignored.bin", "\x00binary")
    (corpus / ".env").write_text("SECRET=1")
    storage = tmp_path / "storage"

    result = run_index(tmp_path, corpus, storage)

    assert result["status"] == "completed"
    assert result["indexed"] == 2
    assert result["removed"] == 0
    assert result["skipped"] == 0
    assert result["database"].endswith("rag.sqlite3")
    database = Path(result["database"])
    assert database.is_file()

    queried = run_query(tmp_path, "OpenRouter capability validation", storage)
    assert queried["status"] == "completed"
    assert queried["matches"] > 0
    assert queried["citations"][0]["path"] == "docs/guide.md"
    assert queried["citations"][0]["start"] < queried["citations"][0]["end"]
    assert "OpenRouter" in queried["citations"][0]["text"]
    assert queried["citations"][0]["heading"] == "Guide"
    assert queried["citations"][0]["score"] > 0


def test_incremental_index_and_pruning(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    first = write(corpus / "first.md", "# First\n\nalpha value\n")
    storage = tmp_path / "storage"

    first_result = run_index(tmp_path, corpus, storage)
    assert first_result["indexed"] == 1
    unchanged_result = run_index(tmp_path, corpus, storage)
    assert unchanged_result["unchanged"] == 1
    assert unchanged_result["indexed"] == 0

    first.write_text("# First\n\nbeta value\n", encoding="utf-8")
    second = write(corpus / "second.md", "# Second\n\ngamma\n")
    updated_result = run_index(tmp_path, corpus, storage)
    assert updated_result["indexed"] == 2
    assert updated_result["refreshed"] == 0

    second.unlink()
    pruned_result = run_index(tmp_path, corpus, storage)
    assert pruned_result["removed"] == 1

    connection = sqlite3.connect(first_result["database"])
    try:
        paths = {row[0] for row in connection.execute("select path from files")}
    finally:
        connection.close()
    assert paths == {"first.md"}


def test_chinese_and_heading_context(tmp_path: Path):
    corpus = tmp_path / "corpus"
    docs = corpus / "docs"
    docs.mkdir(parents=True)
    write(
        docs / "中文.md",
        "# 使用說明\n\n本地檢索需要提供引用來源。\n\n## 進階\n\n向量索引不是第一階段必要。\n",
    )
    storage = tmp_path / "storage"
    run_index(tmp_path, corpus, storage)

    result = run_query(tmp_path, "引用來源", storage)

    assert result["matches"] >= 1
    citation = result["citations"][0]
    assert citation["text"] == "本地檢索需要提供引用來源。"
    assert citation["heading"] == "使用說明"


def test_path_filter_and_zero_result(tmp_path: Path):
    corpus = tmp_path / "corpus"
    (corpus / "docs").mkdir(parents=True)
    (corpus / "src").mkdir(parents=True)
    write(corpus / "docs" / "search.md", "# Search\n\nneedle appears here\n")
    write(corpus / "src" / "app.py", "needle = 'in code'\n")
    storage = tmp_path / "storage"
    run_index(tmp_path, corpus, storage)

    filtered = run_query(tmp_path, "needle", storage, path_filter="docs/")
    assert all(citation["path"].startswith("docs/") for citation in filtered["citations"])

    empty = run_query(tmp_path, "missing concept", storage)
    assert empty["status"] == "completed"
    assert empty["matches"] == 0
    assert empty["citations"] == []
