# Quality report template

## Task
<one line — what was generated/modified>

## Grade
- Level: L1 / L2 / L3
- Grade confidence: high / med / low
- Cross-bucket flag: <corner if any, else none>

## Reverse gate
- Screen 1 (gate-catchable): pass / STOP
- Screen 2 (spec hardenable): pass / STOP
- Screen 3 (generate, not comprehend): pass / STOP
- Screen 4 (reversible enough): pass / STOP

## Spec self-check
- Score: N/5
- Cage-strength-equals-spec-strength warning: [RED if N<3]
- Delegated to protocol-adversarial-design? yes/no — if yes, invariants + alignment tests adopted

## Gates opened
| Gate | Result | Notes |
|---|---|---|
| Unit | | |
| Coverage | | |
| Mutation (sampled/full) | | |
| Metric combo | | |
| L3 human line-read | | |

## Metric combo reading
<combined reading, not per-metric PASS lines>

## Feedback upgrade
- Re-graded? yes/no — if yes, from _ to _, evidence: _

## Category disclosure (mandatory)
This task's quality judgment is **gate-based**. Structurally uncatchable by
gating: [abstract smell / cross-module emergent / naming-intent drift]. Task
sensitive to those? → fall back to human reading.

## Assumptions to verify
| Assumption | Risk | Lowest-cost test |
|---|---|---|