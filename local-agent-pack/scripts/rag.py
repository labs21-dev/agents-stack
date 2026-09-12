#!/usr/bin/env python3
"""Zero-dependency local RAG index and hybrid retrieval for local-agent-pack."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import sqlite3
import sys
from typing import Any


CONFIG_PATH = pathlib.Path(__file__).resolve().parents[1] / "templates" / "openrouter.config.json"
DEFAULT_STORAGE_ROOT = ".agents"
TEXT_EXTENSIONS = {
    ".md", ".markdown", ".txt", ".rst", ".py", ".js", ".ts", ".tsx", ".jsx",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".sh", ".bash", ".zsh",
    ".css", ".html", ".sql", ".go", ".rs", ".java", ".kt", ".rb", ".php", ".c",
    ".h", ".cpp", ".hpp", ".cs", ".swift",
}
EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".agents", "dist", "build",
}
EXCLUDED_NAMES = {".env", ".env.local", ".env.production", "id_rsa", "credentials.json"}
MAX_FILE_BYTES = 10 * 1024 * 1024


class RagError(Exception):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def load_config(config_path: pathlib.Path | None) -> dict[str, Any]:
    path = config_path or CONFIG_PATH
    if not path.is_file():
        return {"storageRoot": DEFAULT_STORAGE_ROOT}
    return json.loads(path.read_text(encoding="utf-8"))


def database_path(config_path: pathlib.Path | None, storage_root: pathlib.Path | None) -> pathlib.Path:
    configured = storage_root or load_config(config_path).get("storageRoot", DEFAULT_STORAGE_ROOT)
    root = pathlib.Path(configured).expanduser()
    if not root.is_absolute():
        root = pathlib.Path.cwd() / root
    return (root / "indexes" / "rag" / "rag.sqlite3").resolve()


def connect(path: pathlib.Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("pragma foreign_keys = on")
    connection.execute("pragma journal_mode = wal")
    connection.execute("pragma synchronous = normal")
    return connection


def initialize_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        create table if not exists meta (
          key text primary key,
          value text not null
        );
        create table if not exists files (
          id integer primary key,
          path text not null unique,
          size_bytes integer not null,
          mtime_ns integer not null,
          sha256 text not null,
          language text,
          indexed_at text not null
        );
        create table if not exists chunks (
          id integer primary key,
          file_id integer not null references files(id) on delete cascade,
          path text not null,
          start integer not null,
          end integer not null,
          heading text,
          language text not null,
          text text not null
        );
        create index if not exists chunks_file_id_idx on chunks(file_id);
        create index if not exists chunks_path_idx on chunks(path);
        create virtual table if not exists chunks_fts using fts5(
          text,
          path,
          heading,
          language,
          tokenize = 'trigram'
        );
        """
    )


def language_for(path: pathlib.Path) -> str:
    extension = path.suffix.lower()
    if extension in {".md", ".markdown"}:
        return "markdown"
    if extension in {".py"}:
        return "python"
    if extension in {".js", ".jsx", ".ts", ".tsx"}:
        return "typescript"
    if extension in {".txt", ".rst"}:
        return "text"
    return extension.removeprefix(".") or "text"


def should_index(path: pathlib.Path) -> bool:
    return (
        path.suffix.lower() in TEXT_EXTENSIONS
        and path.name not in EXCLUDED_NAMES
        and path.stat().st_size <= MAX_FILE_BYTES
    )


def iter_corpus_files(corpus: pathlib.Path) -> list[pathlib.Path]:
    if corpus.is_file():
        return [corpus]
    if not corpus.is_dir():
        raise RagError(f"corpus path not found: {corpus}")
    files: list[pathlib.Path] = []
    for current, dirs, names in corpus.walk():
        dirs[:] = sorted(name for name in dirs if name not in EXCLUDED_DIRS)
        for name in sorted(names):
            path = pathlib.Path(current) / name
            files.append(path)
    return [path for path in files if should_index(path)]


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def chunk_text(text: str, path: pathlib.Path, language: str) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    headings: list[str] = []
    start = 0
    paragraph_start: int | None = None
    paragraph_end = 0

    def append_chunk(begin: int, end: int) -> None:
        value = text[begin:end].strip()
        if not value:
            return
        chunks.append(
            {
                "start": begin,
                "end": end,
                "heading": " / ".join(headings) or None,
                "language": language,
                "text": value,
            }
        )

    lines = text.splitlines(keepends=True)
    for line in lines:
        match = HEADING_RE.match(line.rstrip())
        if match and language == "markdown":
            if paragraph_start is not None:
                append_chunk(paragraph_start, paragraph_end)
                paragraph_start = None
            level, title = len(match.group(1)), match.group(2).strip()
            while headings and len(headings) >= level:
                headings.pop()
            headings.append(title)
        stripped = line.strip()
        if stripped:
            if paragraph_start is None:
                paragraph_start = start
            paragraph_end = start + len(line)
        elif paragraph_start is not None:
            append_chunk(paragraph_start, paragraph_end)
            paragraph_start = None
        start += len(line)
    if paragraph_start is not None:
        append_chunk(paragraph_start, paragraph_end)

    if not chunks:
        append_chunk(0, len(text))
    return chunks


def index_file(connection: sqlite3.Connection, path: pathlib.Path, corpus: pathlib.Path) -> dict[str, Any]:
    stat = path.stat()
    relative = path.resolve().relative_to(corpus.resolve()).as_posix()
    existing = connection.execute(
        "select id, size_bytes, mtime_ns, sha256 from files where path = ?",
        (relative,),
    ).fetchone()
    if existing and existing["size_bytes"] == stat.st_size and existing["mtime_ns"] == stat.st_mtime_ns:
        return {"path": relative, "status": "unchanged"}

    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if existing and existing["sha256"] == digest:
        connection.execute(
            "update files set size_bytes = ?, mtime_ns = ?, indexed_at = ? where id = ?",
            (stat.st_size, stat.st_mtime_ns, utc_now(), existing["id"]),
        )
        return {"path": relative, "status": "refreshed"}

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return {"path": relative, "status": "skipped", "reason": "not UTF-8 text"}
    language = language_for(path)
    chunks = chunk_text(text, path, language)
    if existing:
        connection.execute(
            "delete from chunks_fts where rowid in (select id from chunks where file_id = ?)",
            (existing["id"],),
        )
        connection.execute("delete from files where id = ?", (existing["id"],))
    cursor = connection.execute(
        """insert into files(path, size_bytes, mtime_ns, sha256, language, indexed_at)
           values (?, ?, ?, ?, ?, ?)""",
                (relative, stat.st_size, stat.st_mtime_ns, digest, language, utc_now()),
    )
    file_id = cursor.lastrowid
    for chunk in chunks:
        cursor = connection.execute(
            """insert into chunks(file_id, path, start, end, heading, language, text)
               values (?, ?, ?, ?, ?, ?, ?)""",
            (
                file_id,
                relative,
                chunk["start"],
                chunk["end"],
                chunk["heading"],
                chunk["language"],
                chunk["text"],
            ),
        )
        connection.execute(
            "insert into chunks_fts(rowid, text, path, heading, language) values (?, ?, ?, ?, ?)",
            (cursor.lastrowid, chunk["text"], relative, chunk["heading"] or "", language),
        )
    return {"path": relative, "status": "indexed", "chunks": len(chunks)}


def prune_missing(connection: sqlite3.Connection, corpus: pathlib.Path, known: set[str]) -> int:
    rows = connection.execute("select id, path from files").fetchall()
    removed = 0
    for row in rows:
        if row["path"] not in known:
            connection.execute("delete from files where id = ?", (row["id"],))
            removed += 1
    return removed


def index_corpus(args: argparse.Namespace) -> dict[str, Any]:
    corpus = pathlib.Path(args.corpus).expanduser().resolve()
    files = iter_corpus_files(corpus)
    connection = connect(database_path(args.config, args.storage_root))
    try:
        initialize_schema(connection)
        known: set[str] = set()
        results: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []
        for path in files:
            result = index_file(connection, path, corpus)
            if result["status"] == "skipped":
                skipped.append(result)
                continue
            known.add(result["path"])
            results.append(result)
        removed = prune_missing(connection, corpus, known)
        connection.execute(
            "insert into meta(key, value) values ('lastIndexedAt', ?) "
            "on conflict(key) do update set value = excluded.value",
            (utc_now(),),
        )
        connection.commit()
        return {
            "status": "completed",
            "corpusPath": str(corpus),
            "database": str(database_path(args.config, args.storage_root)),
            "indexed": sum(item["status"] == "indexed" for item in results),
            "refreshed": sum(item["status"] == "refreshed" for item in results),
            "unchanged": sum(item["status"] == "unchanged" for item in results),
            "removed": removed,
            "skipped": len(skipped),
            "skippedFiles": skipped,
            "files": results,
        }
    finally:
        connection.close()


def fts_query(question: str) -> str:
    terms = re.findall(r"[\w\-.]+|[\u3400-\u9fff]{2,}", question, flags=re.UNICODE)
    normalized: list[str] = []
    for term in terms:
        if len(term) >= 2:
            normalized.append('"' + term.replace('"', '""') + '"')
    return " OR ".join(normalized)


def exact_query(question: str) -> list[str]:
    terms = re.findall(r"[\w\-.]+|[\u3400-\u9fff]{2,}", question, flags=re.UNICODE)
    return list(dict.fromkeys(term for term in terms if len(term) >= 2))


def reciprocal_rank(position: int, k: int = 60) -> float:
    return 1.0 / (k + position)


def query_index(args: argparse.Namespace) -> dict[str, Any]:
    db_path = database_path(args.config, args.storage_root)
    if not db_path.is_file():
        raise RagError(f"RAG index not found; run index first: {db_path}")
    connection = connect(db_path)
    try:
        initialize_schema(connection)
        fts = fts_query(args.query)
        scores: dict[int, float] = {}
        rows: dict[int, sqlite3.Row] = {}
        if fts:
            for position, row in enumerate(
                connection.execute(
                    """select c.*, bm25(chunks_fts) as bm25_score
                       from chunks_fts f
                       join chunks c on c.id = f.rowid
                       where chunks_fts match ? and (? is null or c.path like ?)
                       order by bm25(chunks_fts)
                       limit ?""",
                    (fts, args.path_filter, f"%{args.path_filter}%", args.limit * 5),
                ),
                start=1,
            ):
                scores[row["id"]] = scores.get(row["id"], 0.0) + reciprocal_rank(position)
                rows[row["id"]] = row
        for term in exact_query(args.query):
            matches = connection.execute(
                """select id from chunks where (? is null or path like ?) and text like ?
                   order by id limit ?""",
                (args.path_filter, f"%{args.path_filter}%", f"%{term}%", args.limit * 5),
            ).fetchall()
            for position, row in enumerate(matches, start=1):
                scores[row["id"]] = scores.get(row["id"], 0.0) + reciprocal_rank(position)
                if row["id"] not in rows:
                    rows[row["id"]] = connection.execute(
                        "select * from chunks where id = ?", (row["id"],)
                    ).fetchone()
        ranked = sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0]),
        )[: args.limit]
        citations = [
            {
                "path": row["path"],
                "start": row["start"],
                "end": row["end"],
                "score": round(score, 8),
                "heading": row["heading"],
                "language": row["language"],
                "text": row["text"],
            }
            for chunk_id, score in ranked
            if (row := rows[chunk_id]) is not None
        ]
        return {
            "status": "completed",
            "type": "rag-query",
            "query": args.query,
            "pathFilter": args.path_filter,
            "matches": len(citations),
            "citations": citations,
        }
    finally:
        connection.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=pathlib.Path, default=CONFIG_PATH)
    parser.add_argument("--storage-root", type=pathlib.Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="Index or incrementally refresh a corpus")
    index_parser.add_argument("corpus", type=pathlib.Path)

    query_parser = subparsers.add_parser("query", help="Retrieve path-backed chunks")
    query_parser.add_argument("query")
    query_parser.add_argument("--limit", type=int, default=8)
    query_parser.add_argument("--path-filter")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = index_corpus(args) if args.command == "index" else query_index(args)
    except RagError as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
