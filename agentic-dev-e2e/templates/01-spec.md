# Spec: <feature name>

WISH: <the user's one-line wish, verbatim>
GRADE: <L1|L2|L3> · confidence <1-10> · corners: <if any>
STATUS: draft

## Scope

In:
- <capability one line>
Out:
- <explicitly excluded, one line + where it would belong>

## Behavior

### Frontend
- <states, transitions, what the user sees; per state; per locale if multi-lang>

### Backend / service
- <endpoints/jobs/schema changes, invariants, error codes>

## Paths

### Happy path
1. <step>

### Unhappy paths
| Trigger | User-visible behavior | Recovery |
|---|---|---|
| <failure> | <what user sees> | <auto-retry / manual / refused> |

### Edge cases
- <input or domain edges>

### Broken scenarios
- <what surrounding systems break if this is wrong>

## Industry practice
- <2-5 bullets: how comparable products handle this; convention followed or consciously broken>

## Test cases

### Backend
| Case | Expectation |
|---|---|
| <derived from unhappy/edge> | <assertion> |

### Frontend
| Case | Expectation | Needs device? |
|---|---|---|
| | | y/n |

## Verifiable steps
1. <command or action> → <expected result>

## Open judgment calls
| # | Rule | Why it's a choice | Recommended default |
|---|---|---|---|
| <feeds Gate A on L3; empty on L1/L2 means agent made the calls and logs them in 05> |