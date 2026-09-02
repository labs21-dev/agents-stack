# Build Report: <feature name>

STATUS: draft

## Files changed

### Frontend
- `<path>` — <one-line intent>

### Backend / service
- `<path>` — <one-line intent>

## Spec → test mapping

| Spec case (01) | Test file/case | Kind |
|---|---|---|
| <every spec test case appears here> | `<file>::<case>` | BE unit / FE ui |

<If a spec case has no test, the row exists with a reason. An unmapped case
without a reason is a failed gate.>

## Spec deviations

<Must be "none". If the code does something the spec doesn't say: STOP —
amend the spec through Gate A (or note the human ordered it, with a line of
reason), never rationalize silently.>