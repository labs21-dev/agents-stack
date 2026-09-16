# Personas memory

Duty: a compact operating protocol for how the user wants agents to think,
communicate, decide, challenge assumptions, and avoid recurring failure modes.
Answers "how should this agent work with this user."
When to use: task start, personalization, answer style choices, product or
architecture judgment, user corrections, or conflict with a previously stated
preference.
Purpose: make the interaction protocol durable without turning every session
into a new interview.
Store: user-confirmed clauses with evidence, scope, and `last_updated`;
role-specific personas when scopes conflict.
Do not store: demographics, identity labels, medical or diagnostic claims,
private transcripts, secrets, stale real-world facts.
When to update: user confirms a new preference, a correction repeats, an
inference is validated, or an existing clause conflicts with newer evidence.

CRUD and the write gate live in
[`../../../interview-to-personas/SKILL.md`](../../../interview-to-personas/SKILL.md).
Drawer rule: one persona per file; INDEX first; every clause needs evidence.

## Catalog

| slug | one-liner | scope | status | last_updated | file |
|------|-----------|------|--------|--------------|------|
| founder-operator | Compact, direct, evidence-first collaboration protocol | all sessions | active | 2026-09-16 | `founder-operator.md` |
