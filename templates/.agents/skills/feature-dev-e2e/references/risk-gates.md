# Risk Gates: L1/L2/L3 + when the agent must stop

Grading happens at Phase 0 (task pipeline) or at intake (standalone gate run).
One line in the spec: grade + confidence + any cross-bucket corner.
**One L3 corner makes the whole task L3** — never average down.

## Axes

Risk is continuous; three buckets are a lossy approximation. State grade
confidence (high / med / low).

### Axis A — Failure cost

| | What a defect causes |
|---|---|
| Low | mild UX miss, cosmetic, easily reverted, no data |
| Med | user-facing bug, lost work, rework, minor trust hit |
| High | data loss, double charge, authz escape, safety, irreversible migration |

### Axis B — Reversibility

| | How hard to undo once shipped |
|---|---|
| Reversible | one deploy to roll back, no migration |
| Half | needs migration / data fix / coordinated rollout |
| Irreversible | schema burnt, money moved, external side effect sent |

## Buckets

| Grade | Failure cost | Reversibility | Gate A behavior | Verify / gate depth |
|---|---|---|---|---|
| L1 | low | reversible | auto-continue | build + smoke + human skim of critical path; spec light; **no** mutation, no full metrics |
| L2 | medium | half (revertible with effort) | auto-continue | hard spec + unit + coverage + mutation(sampled) + metric combo + UI walk with cited evidence |
| L3 | high | irreversible or trust/price-sensitive | **STOP — human sign-off before any code** | L2 all + mutation(full) + trust-boundary review + human line-read of core paths |

Low confidence on a task with any irreversible corner → grade L3 by default.

## Six L3 triggers (high-risk, must stop at Gate A)

A task is L3 if any of these is true — the agent checks each explicitly and
states which applied:

1. **Money / quota / billing** — payment, credits, refunds, subscription
   state, paywalls, or what the user pays for. (Includes "should this consume
   a credit?" and "should this refund?")
2. **Data loss / migration** — deletes, overwrites, or reshapes persisted
   user data; schema migrations; store format changes.
3. **Privacy / permissions** — new data collection, new permission prompts,
   changed data-sharing surface, auth flows.
4. **Irreversible deployment** — production deploy, store submission, DNS or
   infra changes. (Deploy itself is always human-triggered regardless of
   grade — this row is about *designing* something that will be deployed
   irreversibly.)
5. **Product voice / value judgment** — copy or behavior where the "right
   answer" is a taste or philosophy call the codebase cannot derive: tone of
   the assistant character, what the product refuses vs allows, fairness-ish
   defaults, refusal/queue/policy behavior.
6. **User-facing automation with judgment** — AI decisions that act on user
   content where a false positive harms (moderation, auto-reject, auto-send).

Items 5 and 6 are the ones most often missed: they rarely look "technical."
For every behavioral rule written into the spec, ask: *is this rule derivable
from the codebase, or is it a choice someone has to make?* If a human has to
make it → L3.

## Project overrides

A repo may extend or tighten this list via a project file — look for
`feature-dev-e2e.overrides.md` in the repo root or `.claude/` dir. Project
files may ADD L3 triggers; they may not REMOVE the six above.

## Cross-bucket corners

L2-looking tasks with an L3 corner (routine CRUD that also writes a payment
ledger; a UI tweak that also changes a refund rule; a one-line diff to an
endpoint that already handles idempotency keys) run the whole task at L3.
State the corner explicitly. The corner list goes in the spec so the Gate A
human reads what matters first. Single-use / one-time scripts do not lower
the grade.

## Grade reopens on evidence

Downstream results can falsify the Phase 0 grade: if verify finds a failure
density far above what the grade predicts, or build surfaces an
irreversibility not visible at spec time, re-grade (usually up) and re-open
the matching gate. Grade is not fixed at step 0 — see
`feedback-upgrade.md`.