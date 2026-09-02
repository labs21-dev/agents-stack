# Artifact Contracts: fixed formats per phase

All artifacts live in `.agent/features/<slug>/` (slug = short kebab-case
feature name). `.agent/` is a working directory, not necessarily committed —
the final report and checklist SHOULD be kept (commit or paste into PR/issue)
because they are the reviewable record; intermediate files may be gitignored
if the repo prefers.

Common rules for every artifact:
- Markdown, fixed section headings (below). A missing section is a defect —
  write "N/A" with one line of reason, don't omit.
- Each artifact ends with a status line: `STATUS: <draft|signed|passed|failed|waiting-for-human>`.
- File paths and commands are literal and copy-pasteable.
- Keep 01-spec ≤ ~1 page of prose + tables. Appendix sections (failure modes,
  industry notes) carry the overflow; the human-facing page stays scannable.

## 01-spec.md

```markdown
# Spec: <feature name>
WISH: <the user's one-line wish, verbatim>
GRADE: <L1|L2|L3> · confidence <1-10> · corners: <if any>
STATUS: draft

## Scope
In: … / Out: … (one line each; out-of-scope items name where they'd belong)

## Behavior
### Frontend
<bullets: states, transitions, what user sees; per state, per language/locale if repo is multi-lang>
### Backend / service
<bullets: endpoints/jobs/schema, invariants, error codes>

## Paths
- Happy path: <numbered steps>
- Unhappy paths: <per failure: trigger → user-visible behavior → recovery>
- Edge cases: <input/domain edges>
- Broken scenarios: <what surrounding systems break if this is wrong>

## Industry practice
<2-5 bullets: how comparable products handle this, what convention we follow or consciously break>

## Test cases
### Backend
<case → expectation, one line each, derived from unhappy/edge>
### Frontend
<case → expectation; note which need simulator/device>

## Verifiable steps
<numbered steps a human or agent can run: command → expected result>

## Open judgment calls
<list every rule above that is a CHOICE not derivable from the codebase, each with the recommended default — this section feeds Gate A on L3>
```

## 02-quadrant.md

```markdown
# Magic Quadrant: <feature name>
STATUS: draft

| | Humans know | Humans don't know |
|---|---|---|
| AI knows | Q1 shared ground: <list> | Q2 AI-only knowledge: <list — repo couplings, industry patterns, AI failure modes relevant here> |
| AI doesn't know | Q3 human-only knowledge: <AI's best-guess list; HUMAN CORRECTS THIS CELL at Gate A> | Q4 double-blind: <what neither knows; must be validated by experiment/usage — these become the assumption list> |

## Pivotal question (L3 only)
<the single question whose answer changes the design — asked at Gate A>
## Human answer
<filled at gate>
```

## 03-build-report.md

```markdown
# Build Report: <feature name>
STATUS: draft

## Files changed
<path> — <one-line intent>   (repeat per file; group FE/BE)

## Spec → test mapping
| Spec case | Test file/case | Kind (BE unit / FE ui) |
|---|---|---|
| <every spec test case appears here or the row says why not> |

## Spec deviations
<must be "none". If code does something the spec doesn't say: STOP, amend the
spec via Gate A — do not rationalize here.>
```

## 04-verify-report.md

```markdown
# Verify Report: <feature name>
STATUS: draft | passed | failed

## Environment
<build tool + version, test runner, simulator/device id>

## Results
| # | Check | Command / action | Evidence (path or paste) | Result |
|---|---|---|---|---|
| 1 | build | <cmd> | <log path / summary line> | pass/fail |
| 2 | BE tests | <cmd> | <runner summary> | pass/fail |
| 3 | FE golden path | <simulator action> | <screenshot path> | pass/fail |
| 4 | … verifiable step from spec | | | |

## What AI could not verify
<list: needs real device / real users / production data / human taste /
multi-session effects. NEVER empty on UI-affecting changes.>

## Failed checks & analysis
<each failure: what happened, suspected cause, whether it's a code bug or a
spec bug>
```

## 05-final-report.md

```markdown
# Final Report: <feature name>
STATUS: waiting-for-human

## Shipped (in working tree, uncommitted)
<3-6 bullets, plain language>

## Quadrant update (post-build)
<Q2 refresh: what AI learned that humans may not realize; Q4 refresh: which
assumptions got validated/broken>

## Judgment calls made
<each value-flavored decision the agent made on L1/L2 auto-pass, with its
default — the human's chance to veto>

## Known gaps / follow-ups
<from verify failures + quadrant Q4>
```

## 06-checklist.md

```markdown
# Acceptance Checklist: <feature name>
STATUS: waiting-for-human

| # | Expected behavior | How to check | Done |
|---|---|---|---|
| 1 | <observable behavior> | <exact action, under 1 min> | ☐ |

## Waiting for human
- Run checklist above (est. <N> min)
- Value verdicts needed on: <from final report judgment calls>
- Commit? (agent does not commit unless told)
```

## 00-stop.md (only when stopping)

```markdown
# STOP: <feature name>
STATUS: failed | waiting-for-human
## Failed screens / gate
<what stopped>
## Why
<one paragraph>
## What the human should do
<specific unblock action>
```