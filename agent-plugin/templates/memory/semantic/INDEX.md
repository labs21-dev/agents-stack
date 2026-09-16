# Semantic memory

Duty: facts and concepts detached from a specific episode. Answers "what is true."
When to use: when you need stable knowledge: user preferences, project facts, terms, domain rules, confirmed relationships.
Purpose: so the next task does not have to re-ask something already confirmed.
Store: confirmed or verified facts. Every entry must have `last_updated`, `as_of`, `source`, and `scope`.
Do not store: guesses, one-off workarounds, episode detail, procedure steps, secrets.
When to update: revise when source, time, or scope changes; expire or delete when stale or contradicted. `derived` must not be used as a hard constraint.

CRUD lives only in [`../../skills/agent-memory/SKILL.md`](../../skills/agent-memory/SKILL.md). Drawer rule: one fact per file; facts expire.

## Catalog

| slug | one-liner | status | last_updated | as_of | source | file |
|------|-----------|--------|--------------|-------|--------|------|

0 entries.
