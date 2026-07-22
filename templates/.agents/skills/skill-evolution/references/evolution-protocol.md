# Evolution Protocol

The full L2 upgrade/deprecate flow and its gates. Companion to the state machine in `SKILL.md`.

## 1. Passive collection (IDLE)

After a skill is used and produces an **observable outcome**, record one case entry in the skill's `evolution-log.md`:

- **context** — what task / situation triggered the skill.
- **part used** — which rule / lens / trigger / section of the skill was exercised.
- **outcome** — `effective` | `ineffective` | `adverse`.
- **post-hoc verification** — `pending` | `verified-effective` | `verified-ineffective` | `none`. Verification comes from an external outcome (the work shipped and was judged by the user/reality), **not** the agent's self-assessment.
- **notes** — what specifically worked or failed.

Passive means: do not invoke a skill mid-work to narrate its own evolution (that is navel-gazing). Record retrospectively, after the outcome is observable.

## 2. Flag (threshold crossing)

Tally cases per `part used`:

- **Upgrade candidate**: ≥3 cases with `outcome: effective`, AND ≥1 of them `post-hoc verification: verified-effective`.
- **Deprecate candidate**: ≥3 cases with `outcome: adverse`.

Record the flag in `evolution-log.md` with the tally and the evidence pointers.

## 3. Draft patch (DRAFTED)

The AI drafts a concrete patch following `patch-draft-format.md`:

- **scope** — exactly which file/section changes; nothing outside scope.
- **diff** — the literal before/after.
- **evidence summary** — the cases that justify it, with their verification status.
- **risk tag** — low / medium / high (per the risk grading table).
- **reversibility** — how easy to undo if it regresses.
- **before-snapshot instruction** — what to snapshot so the change can roll back.

The AI does **not** apply the patch.

## 4. Gate (human review)

The human reviews the drafted patch:

- **Approve** — proceed to merge.
- **Reject** — back to IDLE; note why in the log.
- **Amend** — adjust the patch; re-review.

For **high-risk** changes (core rule change, deprecate an existing rule): per-item strict review + a second person if available.

## 5. Merge (MERGED)

On approval:

1. Take the **before-snapshot** of the affected file(s).
2. Apply the patch.
3. Write a **changelog** entry (what changed, why, which cases drove it, snapshot location).
4. Update the skill's `evolution-log.md` to mark the candidate as merged.

## 6. Validate

The next real uses of the skill check whether the change **sharpened** output:

- If output improved or held — the upgrade holds.
- If output regressed — **roll back** the before-snapshot; record the regression as a case (it becomes evidence for a future deprecate or re-revision).

Validation closes the loop: an upgrade that looked justified by cases can still be wrong in practice. The rollback is the external anchor.

## 7. Deprecate (symmetric)

The same flow, with `outcome: adverse` cases as the trigger and a **removal** diff as the patch. A rule that accumulates adverse cases and survives deprecate review is removed (with before-snapshot, so it can be restored if the removal turns out wrong).

## Threshold adjustment

If validation repeatedly shows:
- **false upgrades** (merged changes that regressed) → N is too low; raise it.
- **deserved upgrades stalling** (clear candidates not reaching N) → N is too high; lower it.

These adjustments are themselves L3 agenda items — recorded in `compound/`, human-legislated, not silently changed.