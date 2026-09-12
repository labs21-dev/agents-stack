# L3 Accumulate-Only

L3 is the layer that defines "what makes a good skill" — the standard the other layers are measured against. In the current phase (B), L3 **accumulates cases only; it does not legislate.** Folding a recurring pattern into a standard is a human action.

## Why accumulate-only

L3 is the most reflexivity-exposed layer. If the AI defines "what makes a good skill" and also grades skills against that definition, the standard self-validates and drifts. The only defense is an external anchor: patterns must recur across **multiple skills** (N≥3) and be **legislated by the human**, not auto-applied.

In the B phase we don't yet have enough cross-skill cases to legislate. So we only accumulate them. When enough recur, the human can legislate (A phase).

## Structure

```
skill-evolution/
  compound/
    INDEX.md                       ← legislation surface (see write boundary below)
    <YYYY-MM-DD>-<slug>/
      CASE.md                      ← one accumulated cross-skill issue
      input.txt                    ← evidence (territory beside map)
```

`INDEX.md` is where compounding happens — linear accumulation is in the cases; non-linear convergence is in INDEX.

## Write boundary

| Region | Who writes | Why |
|---|---|---|
| INDEX cases-list (one line per case) | **skill auto-appends** | additive, reversible |
| INDEX recurring-patterns section | **human only** | this is the N≥3 convergence decision-point; AI auto-filling it = AI legislating = reflexivity violation |
| INDEX legislation-log (which pattern folded into which standard, when) | **human only** | record of amendments |
| `<id>/CASE.md` | **skill, once, then frozen** | additive only — never edit a prior CASE.md from this skill |
| `<id>/input.txt` | skill or human | evidence, untouched after placement |

## CASE.md template

```markdown
# <slug> — <one-line description>

## Input
<what was dropped / observed, one line>

## Content-layer extract
<what the surface work was doing; the reusable product-level pattern>

## Process-layer extract
<the reusable interaction moves — how context was shaped to produce sharp output>

## Increment over existing frameworks
- matches <framework>: <restatement kept for context, not claimed as new>
- extends <framework>: <what adds to it>
- new: <what no existing framework covers>

## Mechanism
- <philosophy> → <runnable gate/step>   [mechanized]
- <philosophy> → ...                    [not-yet-mechanized]

## Self-check
- Did extraction surface something non-obvious?
- Is the increment cleanly distinguished?
- What did this run teach about the protocol itself?

## Flags for human立法
<if a pattern recurs across cases, name it here so the human can find it at convergence time>
```

(This CASE.md template and the common-law loop it implies were originally derived from an earlier `extract-methodology` skill, since removed. The lineage is noted here so the origin of the accumulate/legislate boundary is traceable; no external skill is referenced at runtime.)

## What the AI does at L3

- Record cases in `compound/<id>/CASE.md` (once, frozen).
- Auto-append one line to INDEX cases-list.
- Inside a CASE.md, flag candidate recurring patterns in the `Flags for human立法` field.

## What the AI does NOT do at L3

- Fill the INDEX recurring-patterns section.
- Fill the INDEX legislation-log.
- Fold a pattern into any standard / constitution.
- Auto-apply a "good skill" criterion it invented.

## Graduation to A phase

When cases accumulate and a pattern recurs across ≥3 cases, the human:
1. Reads INDEX, spots the recurrence.
2. Decides to legislate — folds the pattern into the standard (replace, don't stack).
3. Logs the amendment in INDEX legislation-log.
4. Next extraction validates: did the fold make output sharper?

Steps 1–4 are human-only. This skill only accumulates and flags. That asymmetry is the whole point.