# Risk grading matrix

Risk is continuous; three buckets are a lossy approximation. State grade
confidence. Flag cross-bucket tasks.

## Axis A — Failure cost

| | What a defect causes |
|---|---|
| Low | mild UX miss, cosmetic, easily reverted, no data |
| Med | user-facing bug, lost work, rework, minor trust hit |
| High | data loss, double charge, authz escape, safety, irreversible migration |

## Axis B — Reversibility

| | How hard to undo once shipped |
|---|---|
| Reversible | one deploy to roll back, no migration |
| Half | needs migration / data fix / coordinated rollout |
| Irreversible | schema burnt, money moved, external side effect sent |

## Buckets

| Grade | Failure cost | Reversibility | Gates |
|---|---|---|---|
| L1 | Low | Reversible | spec(light) + smoke + human skim critical path |
| L2 | Med | Half | hard spec + unit + coverage + mutation(sampled) + metrics |
| L3 | High | Irreversible | L2 all + mutation(full) + trust-boundary review + line-level human read |

## Cross-bucket rule

An L2 task with one L3 corner (e.g. routine CRUD that also writes a payment
ledger) runs at L3. Do not average down. State the corner in the output.

## Confidence

high / med / low. Low confidence on an irreversible task → grade L3 by default.