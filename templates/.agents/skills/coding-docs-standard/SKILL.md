---
name: coding-docs-standard
description: >-
  Decide what docs an agentic-coding repo needs and author them so an AI agent
  can navigate, verify, and continue work without a human guide. Use when the
  user asks "what docs do I need", "set up docs for agents", wants an AGENTS.md,
  plan/handoff files, ADRs, SECURITY.md, or CONSTITUTION.md, or is seeding docs
  for a repo meant to be worked on by agents. Core rule: docs record ONLY what
  cannot be found by scanning code/tests/types/commit/CI — everything else is a
  second source of truth that decays. NOT for human-facing PRDs, design specs,
  marketing copy, or general documentation writing.
---

# Coding Docs Standard

On-demand SOP for authoring the **agent-facing** doc set of a repo. The reader
is a **context-limited AI agent**, not a human. Every doc must answer one
question: *"if this doc did not exist, where would the agent go wrong after
scanning the repo?"*

## Iron rule (the whole skill hangs on this)

**Docs record only what scanning cannot find.** Anything derivable from
**code / tests / types / commit history / CI config / package manifest** is
banned from docs. Reasons:

- Code is alive, docs are inert → once separated they monotonically diverge
  (entropy). A stale doc is worse than no doc: the agent trusts it and is
  *confidently wrong*.
- One fact in two places = two truths decaying at different rates; the agent
  may draw the older copy.
- One exception: **ADRs record the "why" and the "rejected alternatives"** —
  neither is ever scannable from code. §4.

**Self-check before writing any line of doc:** *can I get this from `grep`, a
type signature, or `git log`?* If yes → delete it, replace with a pointer.

## Hard rules

1. **Scan-first.** No fact that code already states.
2. **Single source.** Any rule lives in exactly one file; others point.
3. **Layered loading.** Don't dump L2 docs into L0; pointers only.
4. **Decay detectable.** If a constraint can be a CI/lint/type gate, it must be
   — not a doc sentence. Living docs carry `last-updated`; completed work is
   archived.
5. **Verify command is non-negotiable.** `AGENTS.md` must list the build/test/run
   commands the agent runs to self-prove completion. Without it, the agent
   silently declares success — the #1 failure mode (see `references/failure-patterns.md`).

## Flow (every invocation)

### 0. Scope the repo — what's already scannable?

Read the repo. List what `grep`/types/CI already give the agent for free. Only
the **gaps** are doc candidates. Run `references/scoping.md`. Most repos need
far fewer docs than their authors think.

### 1. Classify the gaps

Map each gap to a doc class (`references/doc-classes.md`):

| Class | Records what scan can't find | File |
|---|---|---|
| Entry | Rules, don'ts, pointers, verify cmds | `AGENTS.md` |
| Living state | Where we are, what's tried, next | `docs/plan/*.md`, `docs/handoff/*.md` |
| Constraint | Trust boundaries / principles | `docs/SECURITY.md`, `docs/CONSTITUTION.md` |
| Decision | Why + rejected alternatives | `docs/ADR/*.md` |

If a gap maps to nothing → it doesn't need a doc. Close it with code/comment/CI.

### 2. Apply decay defense

For every doc drafted, run `references/decay-defense.md`:
- single source (grep the repo — the sentence must not appear elsewhere),
- detectable failure (push the constraint into CI/lint/type if possible),
- `last-updated` on living docs, archive completed plans.

### 3. Layer the loading

Per `references/loading.md`:
- **L0** always-in-context: `AGENTS.md` (rules + pointers + verify; no content).
- **L1** task-relevant: current `docs/plan/*` + relevant ADR.
- **L2** boundary-triggered: `SECURITY.md` (touching auth/trust), `CONSTITUTION.md`
  (architecture decisions).

### 4. Author from templates

Copy from `templates/`. Each template has a `<!-- scan-can-find? delete -->`
self-check section the author must clear before saving.

### 5. Anti-pattern sweep

Run `references/anti-patterns.md` over the drafted set. Most failures are
duplicating a scannable fact, or two files holding the same rule.

## Required output

1. **Scannable inventory** — what the repo already gives the agent for free.
2. **Gap → class map** — each doc justified by a gap scan can't close.
3. **File set** — the drafted docs, each clearing the scan-self-check.
4. **Decay defense** — per doc: single-source check, detectability, timestamps.
5. **Loading plan** — what's L0/L1/L2 and why.
6. **Rejected docs** — what was considered and *not* written, with reason
   (prevents doc bloat; records the negative space).

## Sibling split

| Need | Skill |
|------|-------|
| Fuzzy multi-lens decision | `meta-thinking-framework` |
| Trusting AI-generated code via gates | `agentic-clean-discipline` |
| Dangerous protocol contract | `protocol-adversarial-design` |
| Authoring agent-facing docs | **this skill** |

This skill is **upstream** of `agentic-clean-discipline`: good agent docs are
what make its spec/verify gates even possible. If the doc question is itself a
fuzzy decision (which trade-offs to accept), run `meta-thinking-framework` first.

## References

- `references/scoping.md` — read repo → list scannable facts → find real gaps
- `references/doc-classes.md` — the four classes + what belongs/doesn't
- `references/loading.md` — L0/L1/L2 layered loading + pointer discipline
- `references/decay-defense.md` — single-source, detectability, archive rules
- `references/failure-patterns.md` — how agent docs fail (entropy, overload, silent success)
- `references/anti-patterns.md` — duplicating scannable facts, multi-source rules

## Templates

- `templates/AGENTS.md` — entry doc skeleton
- `templates/plan.md` — living task state
- `templates/handoff.md` — session handoff
- `templates/SECURITY.md` — trust boundary record
- `templates/CONSTITUTION.md` — non-negotiable principles
- `templates/adr.md` — decision record (the "why" + rejected)

## Self-loop

If a later agent goes wrong despite the docs: locate the leak — was the doc
duplicating a scannable fact (decayed), missing a gap (under-coverage),
overloaded (ignored), or lacking a verify command (silent success)? Fix only
that doc's class.