---
name: agent-memory
description: Store, retrieve, update, and delete durable project or user memory locally. Use when the user asks the agent to remember a preference, recall a prior decision, update long-term knowledge, or forget something.
---

# Agent Memory

Phase 1 defines the contract; the executable local store is Phase 2.

Workflow:

1. Infer action: `write`, `read`, `update`, or `delete`.
2. Infer scope; default to `project`, never silently write `global`.
3. Store content, kind, scope, confidence, provenance, and timestamps.
4. Search with exact match and FTS.
5. Return the record ID for writes.
6. Support explicit forget/delete.
7. Ask before storing obviously sensitive personal information.