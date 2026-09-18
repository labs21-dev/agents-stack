# Memory design review: core-first load

- last_updated: 2026-09-16
- when: 2026-09-16
- task: review and enhance agent-memory for 80% portable markdown use

Context:
The protocol already split four CoALA duties plus personas, with INDEX-first routing and a write-back gate. Task start still required reading all five INDEX files. DESIGN.md still described SQLite and optional vectors.

Action:
Mapped the design to CoALA, Letta core vs archival, and Claude Code MEMORY.md. Kept five directories. Changed load to core-first. Made personas and interview-to-personas optional. Dropped the SQLite/vector contract.

Result:
Protocol now matches the industry minimum without adding a database or a sixth drawer.

Lesson:
The overweight was equal load, not extra drawers. Personas can stay as optional core. Archival INDEX files must wait until a fact, failure, or method is actually needed.
