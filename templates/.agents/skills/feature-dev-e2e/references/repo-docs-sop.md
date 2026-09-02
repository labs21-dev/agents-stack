# Repo docs SOP — the agent-facing doc set (Repo Lane, Lane B)

Use when the task is *what docs does this repo need / write me an AGENTS.md /
plan / handoff / ADR / SECURITY / CONSTITUTION*. This SOP feeds Lane A: good
agent docs are what make the spec and verify gates possible in the first
place.

The reader is a **context-limited AI agent**, not a human. Every doc must
answer one question: *if this doc did not exist, where would the agent go
wrong after scanning the repo?*

## Iron rule

**Docs record only what scanning cannot find.** Anything derivable from
code / tests / types / commit history / CI config / package manifest is
banned. A stale doc is worse than no doc — the agent trusts it and is
*confidently wrong*. One exception: ADRs record the "why" and rejected
alternatives, neither ever scannable.

Self-check before writing any line: *can I get this from grep, a type
signature, or git log?* If yes → delete it, replace with a pointer.

## What is scannable (do NOT document)

| Source | Gives the agent for free |
|---|---|
| `package.json` / `Cargo.toml` / `pyproject.toml` | language, framework, scripts, deps |
| Type signatures | function shape, inputs/outputs, optionality |
| Tests | intended behavior, edge cases the author cared about |
| `git log` | what changed, when, by whom |
| CI config | how the project is built/tested/deployed |
| Directory structure | module layout, entry points |
| Code comments | local "why this line" |

## What is NOT scannable (needs docs)

- **Hidden conventions** no lint/type enforces (*if* one can enforce it →
  hard constraint instead, see `hard-constraints.md`).
- **Why a decision was made / what was rejected** → ADR.
- **Where we are mid-task** — "tried X, failed, next is Y" → plan/handoff.
- **Trust boundaries** — code shows *that* a check exists, not *why* → SECURITY.
- **Deliberately-unchanging principles** → CONSTITUTION.

## Four doc classes

| Class | Records what scan can't | File |
|---|---|---|
| Entry (L0) | rules, don'ts, pointers, verify cmds | `AGENTS.md` |
| Living state (L1) | where we are, what's tried, next | `docs/plan/*.md`, `docs/handoff/*.md` |
| Constraint (L2) | trust boundaries / principles | `docs/SECURITY.md`, `docs/CONSTITUTION.md` |
| Decision | why + rejected alternatives | `docs/ADR/*.md` |

Class specifics:

- **Entry (AGENTS.md)** — three parts, no facts: how we work here (only rules
  no lint enforces); where things are (pointer index, never summarize); how to
  verify (build/test/run commands, named explicitly — the silent-success
  defense; this is the one scannable fact still written, because the *intent*
  "run these to self-prove" is not in the manifest).
- **Living state** — every file carries `last-updated`; completed plans move
  to `docs/archive/plan/` immediately. A live list mixing done and in-progress
  makes the agent misjudge state. Handoffs record why work stopped + the
  successor's first action; they point to plan files, never re-copy them.
- **Constraint** — SECURITY records trust boundaries + assumptions (why drawn
  here); CONSTITUTION records non-negotiables + deliberate non-goals. Loaded
  only on boundary trigger.
- **Decision (ADR)** — numbered, append-only, never edited, **never
  archived**: supersede in place with `status: superseded-by-NNN`. The
  rejected-alternatives field is mandatory — it is what stops an agent from
  re-opening a dead debate. An ADR without it is rejected.

Archive vs supersede: **living → `docs/`; dead → `docs/archive/`; ADRs stay
and supersede.**

## Layered loading

- **L0 always in context**: `AGENTS.md` only — rules + pointers + verify.
  Never inline L2 content (a copied SECURITY rule rots independently).
- **L1 task-relevant**: current `docs/plan/*` + relevant ADRs. `docs/archive/`
  is not L1.
- **L2 boundary-triggered**: SECURITY (touching auth/trust), CONSTITUTION
  (architecture decisions). AGENTS.md tells the agent *when* to pull L2; the
  content stays L2.

## Decay defense (per drafted doc)

1. **Single source** — grep the repo; the rule's key sentence must appear in
   exactly one doc. Otherwise pick one home, pointer from the other.
2. **Detectable failure** — if a constraint can be CI/lint/type-enforced, it
   must be. The doc only holds the *why* the gate can't express.
3. **Timestamps + archive** — living docs carry `last-updated`; completed
   work archives; ADRs supersede in place.

## Procedure

1. Scope: list scannable sources → only gaps are doc candidates.
2. Classify gaps → doc class; a gap mapping to nothing is closed with
   code/comment/CI, not a doc.
3. Draft from `templates/` (AGENTS.md, plan.md, handoff.md, SECURITY.md,
   CONSTITUTION.md, adr.md) — each template carries a scan-self-check the
   author must clear.
4. Decay defense per doc above.
5. Record **rejected docs** — what was considered and not written, with
   reason. This prevents silent re-bloating.

## How this doc set fails

| Failure | Leak | Defense |
|---|---|---|
| Stale ground truth | Entry/Living | scan-first + timestamps + archive + automation |
| Context overload | Loading | L0/L1/L2 triggers, pointer-only entry |
| Silent success | Entry | mandatory verify command |
| Multi-source conflict | any | single-source grep |
| Reopened dead debate | ADR | rejected-alternatives field, supersede-in-place |
| Under-coverage | scoping | gap → class mapping; boundary triggers |