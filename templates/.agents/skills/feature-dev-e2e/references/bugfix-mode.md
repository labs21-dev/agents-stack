# Bug-Fix Mode: same pipeline, different Phase A

A bug report is a wish whose spec is "expected behavior". The pipeline is
identical — only Phase A's artifact shape and three extra disciplines change.
Risk grading is unchanged: a bug in billing logic is L3 exactly like a billing
feature. (Real case: "should this failure refund?" was a bug-fix L3 gate.)

## Phase mapping

| Standard phase | Bug-fix shape |
|---|---|
| 0 Preflight + grade | unchanged |
| A Spec | **Diagnosis doc** (see below) → `01-spec.md` |
| B Build | the fix + regression test |
| C Verify | repro no longer reproduces + regression test passes + existing suite green |
| D Report | unchanged |

## Artifact degradation

- **L1/L2 bug:** 3 artifacts only — `01-spec.md` (diagnosis, half page),
  `04-verify-report.md`, `06-checklist.md`. 02/03/05 are merged into the
  diagnosis and final chat message.
- **L3 bug:** full artifact set; Gate A STOP applies (money/quota/privacy/
  product-voice bugs need the human's value verdict before the fix lands).

## 01-spec.md in bug-fix mode

```markdown
# Diagnosis: <bug name>
REPORT: <the user's bug description, verbatim>
GRADE: <L1|L2|L3> · confidence <1-10>
STATUS: draft

## Repro
<numbered exact steps + environment; must cite evidence: screenshot, log
path, DB row. NO repro = write the speculative fix but the verify report
must say "could not verify — repro unavailable".>

## Root cause
<The mechanism, with EVIDENCE for each link in the causal chain — a log
line, a D1 row, an actual output, a stack frame. A cause inferred from
reading code alone is a HYPOTHESIS: label it so, then go get the evidence
before fixing.>

## Expected behavior after fix
<the spec — what the user sees when this is fixed>

## Blast radius
<what else this code path touches; regression scenarios to test>
```

## Three bug-fix disciplines (feature mode doesn't need these)

1. **Evidence before root cause.** "I read the code and it looks like X" is
   a hypothesis, not a diagnosis. The root-cause section must cite at least
   one runtime artifact (log, DB query result, network trace, actual
   output). No evidence → stop and gather it first; code-reading
   root-causing is how "it's stuck in running" stories get written while the
   real cause is a missing migration.
2. **Regression test is mandatory.** A fix without a test that fails before
   the fix and passes after is incomplete — record it in the verify report
   as "repro test: fails-before / passes-after" (cite both runs). If the bug
   is genuinely untestable (pure visual, device-only), the verify report
   says so explicitly and leans on the manual checklist instead.
3. **Minimal fix.** The fix repairs the bug; it does not refactor, clean up,
   or harden surroundings. Surrounding issues found on the way go into
   "Known gaps / follow-ups", not into this diff.

## What "done" means in bug-fix mode

- Repro steps no longer reproduce (evidence), AND
- regression test fails-before/passes-after (evidence), AND
- existing suite green (evidence), AND
- blast-radius scenarios from the diagnosis checked or explicitly listed as
  unverifiable.