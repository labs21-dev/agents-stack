# Review output skeleton

Omit sections marked tier-optional when below that tier. Keep verdicts crisp.

```markdown
# Refactor review

## Meta
- specialization: valid | weak | invalid | absent
- card_adversarial: done | skipped
- tier: L1 | L2 | L3
- tier_confidence: high | medium | low
- adversarial_review: skipped | same-model | cross-model | human

## Goals echo
- Primary goals (priority):
- Hard constraints:
- Success metrics:
- Acceptable trade-offs:

<!-- If incomplete on L2/L3: replace body with GOALS-REQUIRED + gap list; stop. -->

## Specialization summary
- DOMAIN:
- Hard invariants (gates):
- Hypotheses (not gates):
- OUT_OF_SCOPE:

## 1. Diagnosis check
- Accurate / partial / wrong — evidence notes
- Symptom-as-root-cause flags:

## 2. Core changes (3–5)
| # | Change | Verdict | Why |
|---|--------|---------|-----|
| 1 |  | Accept / Modify / Reject |  |

## 3. Before / After (L2+)
| Component | Responsibility | Data flow | Failure handling | State ownership |
|-----------|----------------|-----------|------------------|-----------------|
|  |  |  |  |  |

## 4. Critical paths (L2 recommended / L3 required)
### Path A (happy)
### Path B (failure / retry / duplicate)
- Races / gaps:

## 5. Layer findings
### L1 Correctness & assumptions
### L2 Completeness (map each FAILURE_MODE)
### L3 Complexity & maintainability (map DO_NOT hits)
### L4 Migration & risk (missing EVIDENCE_REQUIRED)

## 6. Risks & migration
- High-risk points:
- Staged plan / big-bang:
- Rollback:
- Pilot slice: (L3 required)

## 7. Observability & debug
- How to locate faults after change:

## 8. Do not do (L2+)
- (from card + kernel anti-patterns that apply)

## 9. Adversarial findings (L3 required)
1. …
5. …

## 10. ADR stubs (L2+ Accepts)
### ADR: <change>
- Context:
- Decision:
- Consequences:
- Rejected alternatives:

## 11. Open hypotheses + cheapest falsifiers
| Hypothesis | Falsifier (interview / experiment / existing data) |
|------------|-----------------------------------------------------|
|  |  |
```
