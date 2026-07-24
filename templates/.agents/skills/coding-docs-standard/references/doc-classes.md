# Doc classes — what belongs, what doesn't

Four classes. Everything not fitting one is **not a doc** — it's code, a test, a
lint rule, or a comment.

## Entry — `AGENTS.md` (L0, mandatory)

The only always-loaded file. Three parts, **no facts**:

- **How we work here** — conventions and don'ts that no lint/type/test enforces.
  If a lint *does* enforce it, drop it — the lint is the source.
- **Where things are** — pointer index to other docs and the main modules. Do
  not summarize the target's content; just point.
- **How to verify** — the build/test/run commands the agent runs to self-prove
  completion. Even if scannable from a manifest, name them explicitly: this is
  the silent-success defense (see `failure-patterns.md`).

## Living state — `docs/plan/*.md`, `docs/handoff/*.md` (L1)

Records **where we are now**, which code (a snapshot) cannot hold:
- current task, what's been tried and failed (so it isn't retried), next step,
  blockers.
- Every file carries `last-updated`. Stale living docs are not ground truth.
- **Completed plans move to `docs/archive/plan/` immediately.** A live list
  mixing done and in-progress makes the agent misjudge state.

`handoff/` is for cross-session continuity — why work stopped, what the
successor's first action is. Superseded handoffs likewise go to
`docs/archive/handoff/`.

## Constraint — `docs/SECURITY.md`, `docs/CONSTITUTION.md` (L2)

Loaded only on a boundary trigger (touching auth/trust → SECURITY; architecture
decision → CONSTITUTION). Record what scanning can't:
- SECURITY: trust boundaries, what's trusted, what's not, attack-surface
  assumptions. Code shows the check exists, not *why the boundary is here*.
- CONSTITUTION: deliberately-unchanging principles. Code shows current shape,
  not "this is non-negotiable."

When a whole SECURITY/CONSTITUTION is retired (not just a section updated), move
the file to `docs/archive/security/` or `docs/archive/constitution/` and leave a
one-line stub at the original path pointing to the replacement. A section-level
update is just an edit with `last-updated` — not an archive.

## Decision — `docs/ADR/*.md` (on demand)

The **only** class allowed to record the "why." Records:
- the decision, the context, **and the rejected alternatives + why rejected**.
  The rejected list is the highest-value field — code can never show it, and
  it's what stops an agent from re-opening a dead debate.
- Numbered, append-only. Never edit; supersede with a new ADR pointing back.
- **ADRs are never archived.** A superseded ADR stays in `docs/ADR/` in place
  with `status: superseded-by-NNN`; it is not moved to `archive/`. The whole
  point of an ADR is the history — archiving hides exactly the record an agent
  needs to see when it stumbles onto the old decision.

## Archive vs supersede — two different "outdated"

| | Archive | Supersede |
|---|---|---|
| Means | "No longer relevant — get it out of the live set" | "Still relevant; *being replaced* is the information" |
| Applies to | completed plans, retired SECURITY/CONSTITUTION | ADRs |
| Where | `docs/archive/<class>/` | in place, append `superseded-by-NNN` |
| Why | keeps the live set as pure ground truth | preserves decision history; the pointer is the payload |

The rule in one line: **living → `docs/`; dead → `docs/archive/`; but ADRs
stay — they supersede, they don't archive.**

## What NEVER becomes a doc

- Module reference docs ("`foo.ts` exports `bar()`...") → read the code.
- API docs the types already express → read the types.
- "Getting started" narrating the manifest → read the manifest.
- Any fact already stated by CI/lint/package/types/tests.