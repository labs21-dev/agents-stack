---
task: {short task name}
status: in-progress | blocked | done-archiving
last-updated: {YYYY-MM-DD}
---

# {Task}

<!-- Living state. Records WHERE WE ARE — which code (a snapshot) cannot hold.
     On completion, move to docs/archive/plan/. Delete comments once final. -->

## Goal
<!-- One sentence. The "what" is often in code; the "why now / why this shape" usually isn't. -->

## Tried (so it isn't retried)
<!-- REQUIRED. The unscannable part: code shows the current state, not what was
     attempted and failed. Especially the failures — list them so they aren't retried. -->
- {approach} → {outcome}

## Next
<!-- REQUIRED. The concrete next action; code can't hold "what to do next." -->

## Blocked / waiting on
<!-- fill if relevant -->

## Notes
<!-- fill if relevant. GUARDRAIL: only unscannable constraints / open questions /
     things a continuing agent must know. Do NOT dump facts grep/types/code can give
     — that is context stuffing and will rot. -->

<!-- SELF-CHECK:
- [ ] "Tried" lists the failed approaches (the unscannable part) — not just successes.
- [ ] "Notes" contains nothing derivable from grep / types / code (no stuffing).
- [ ] last-updated is set.
- [ ] When status moves to done, this file moves to docs/archive/plan/ — not left in the live list.
- [ ] Nothing here duplicates docs/handoff/ — handoff points to this file, not the reverse.
-->