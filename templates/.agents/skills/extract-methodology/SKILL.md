---
name: extract-methodology
description: Pull-based. Extracts reusable methodology from a worked example (a conversation, transcript, or doc that already produced unexpected value) and produces a case-study artifact. Available to all agents. Does NOT modify the CCA constitution — accumulation is automatic, evolution is human-gated.
---

# Extract Methodology

## What this skill does

Pulls reusable methodology out of a **worked example** — an input that already produced value worth generalizing. Produces a case-study artifact. Accumulates precedents. Does not legislate.

## Carrier distinction (read before first run)

- **This skill** = pull-based extraction → writes a case-study (reversible, additive only).
- **CCA constitution** (`docs/cca/AI-MODULE.md`, `docs/cca/CONSTITUTION.md`) = always-on → modified only by the **human**, via convergence of N≥3 case-studies.

**Hard boundary: this skill MUST NOT write to `AI-MODULE.md` or `CONSTITUTION.md`.** It only writes to the `compound/` directory below. Crossing this line turns "AI accumulates precedents" into "AI rewrites its own operating system" — that violates CCA Law 7 (human gates the irreversible). The skill's job is accumulation; evolution is legislated, not auto-applied.

## Output structure (compound/)

```
{root}/compound/                       # {root} defaults to docs/cca/, parameterizable
├── INDEX.md                           # legislation surface — see boundary below
├── 2026-07-04-cca-derivation/
│   ├── CASE.md                        # the extraction (this skill writes, then never edits)
│   └── input.txt                      # the source input (the territory; optional, lives beside the map)
├── 2026-07-10-<slug>/
│   └── CASE.md
```

Each case-study gets its own folder so the **territory lives beside the map** (Law 4: the input is the territory, the extraction is the map — keeping them co-located lets future runs verify the extraction didn't over-abstract).

`INDEX.md` is the **legislation surface** — where compounding actually happens (linear accumulation is in the cases; non-linear convergence is in INDEX). Write boundary:

| Region | Who writes | Why |
|---|---|---|
| INDEX cases-list (one line per case) | **skill auto-appends** | additive, reversible |
| INDEX recurring-patterns section | **human only** | this is the N≥3 convergence decision-point — AI auto-filling it = AI legislating, violates Law 7 |
| INDEX legislation log (which pattern folded into which law, when) | **human only** | record of amendments to the constitution |
| `{id}/CASE.md` | **skill, once, then frozen** | additive only — never edit prior CASE.md from this skill |
| `{id}/input.txt` | skill or human | evidence, untouched after placement |

## When to invoke

- User drops a file/transcript and asks to analyze, extract, or find what's reusable.
- A collaboration just produced value worth generalizing and the user asks to capture it.
- Explicit triggers: "analyze this", "extract from this", "what's reusable here".

**Do NOT invoke mid-work to extract from the live conversation.** That is navels-gazing — the agent stops doing the job to narrate its own methodology. Extraction is retrospective and triggered, never ambient.

## Protocol — six steps

### 1. Gate
Confirm the input actually produced value. Don't extract from arbitrary chatter. If no value was produced, say so and stop — forcing an extraction from nothing yields fabricated patterns.

### 2. Layer
Separate two layers; extract both, don't mix:
- **Content layer** — what the work surface-did (the review, the design, the debug).
- **Process layer** — how the human-AI interaction itself shaped context (the moves that made the content layer come out sharp).

### 3. Run Module 2 on each layer
CCA AI-MODULE §02's four first-principles steps, retargeted from "code node" to "worked example":
- **Strip the surface**: what was this *fundamentally* solving? (not the surface task)
- **Reveal invariants**: which moves hold across *any* similar example, not just this one?
- **Causal-chain check**: do these moves *necessarily* produce the good output, or did they just co-occur?
- **Over-correction check**: at what level of abstraction does this lose the specificity that made it work? Mark the threshold.

### 4. Cross-reference existing frameworks
Compare the extract against what already exists — thariq's four unknowns, CCA's eight laws, the existing case-studies in `docs/cca/case-studies/`. **Keep only the increment.** Pure restatement of a known framework has negative value (it dilutes the signal). Tag each finding as `matches X` / `extends X` / `new`.

### 5. Operationalize
Philosophy → mechanism. "Ask the right question" becomes "name ≥3 failure modes or return to Module 1". If a finding won't operationalize into a runnable gate/checklist/protocol step, **mark it `not-yet-mechanized`** — do not fake completion with vague phrasing. A philosophy that won't run is a quotation, not a method.

### 6. Output
Write `{root}/compound/{YYYY-MM-DD}-{slug}/CASE.md` using the template below. Co-place the input as `input.txt` in the same folder when available (Law 4 — territory beside map). Then append one line to `{root}/compound/INDEX.md` cases-list (auto-append only; do NOT touch the recurring-patterns or legislation-log sections — those are human-gated). One folder per extraction. Additive only — never edit prior CASE.md from within this skill.

## Case-study template

```
# <slug> — <one-line description>

## Input
<what was dropped, one line>

## Content-layer extract
<what the surface work was doing; the reusable product-level patterns>

## Process-layer extract
<the reusable interaction moves — how context was shaped to produce sharp output>

## Increment over existing frameworks
- matches <framework>: <what restates known stuff — kept for context, not claimed as new>
- extends <framework>: <what adds to it>
- new: <what no existing framework covers>

## Mechanism
- <philosophy> → <runnable gate/step>   [mechanized]
- <philosophy> → ...                    [not-yet-mechanized]

## Self-check
- Did extraction surface something non-obvious? (if only restatement → extraction failed; flag it)
- Is the increment cleanly distinguished? (if not → over-claim)
- What did this run teach about the *protocol itself*? (this calibrates the extractor — see below)

## Flags for human立法
<if a pattern recurs across case-studies, name it here so the human can find it at convergence time>
```

## The common-law loop (how self-evolution actually happens)

```
1. invoke  →  AI runs this skill  →  one case-study folder + INDEX line appended  [automatic]
2. accumulate  →  cases pile in compound/{id}/, INDEX cases-list grows            [automatic]
3. converge  →  human reads INDEX, spots a repeating pattern across N≥3 cases     [human reads, AI may flag in CASE.md "Flags for human立法"]
4. legislate  →  human folds pattern into constitution (replace, don't stack — Law 8), logs in INDEX legislation-log  [HUMAN GATE]
5. validate  →  next extraction checks: did the fold make output sharper?         [automatic, feeds back]
```

This skill drives steps 1, 2, and 5. **Steps 3–4 are human-only** — the skill may *flag* a candidate pattern inside a CASE.md, but the decision to fold it into the constitution and the act of folding are the human's. The skill is not "AI edits its own constitution" — it is "AI accumulates precedents and surfaces candidates; the human legislates." That asymmetry is the whole point.

## Self-check — Review baked in

CCA constitution §07 requires every produced artifact to carry its own failure-mode check. This skill applies to itself: after producing a case-study, answer the Self-check fields honestly. If a run extracts nothing non-obvious, **the failure is in the extraction, not the input** — note it in the case-study's Self-check so the human sees the protocol miscalibrated, not a fake success.

## v0 status — this skill is calibrated from N=1

The six steps above are derived from a single worked example (the CCA derivation transcript, 2026-07-04). Some steps may be example-specific. **Each case-study this skill produces is also evidence about the skill itself** — the "what did this run teach about the protocol" field is the calibration signal. After N≥3 case-studies, the human reviews whether the six steps are the right six; some may merge, split, or drop. The skill is designed to be re-calibrated by its own output, not frozen.

This is "methodology extraction itself being extracted" operationalized: the skill does not assume its protocol is correct — it accumulates the evidence to revise it.