# Agent-memory protocol

- last_updated: 2026-09-16
- as_of: 2026-09-16
- source: verified
- scope: this repo
- expires: never

This repo's agent memory is markdown under `.agents/memory/`. CoALA four drawers (working, semantic, episodic, procedural) plus optional personas as core. Boot loads at most one active persona and a working file only if the task will span compact or handoff. Semantic, episodic, and procedural INDEX files load on demand. No database.
