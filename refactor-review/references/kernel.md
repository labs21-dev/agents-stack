# Refactor Review Kernel (immutable)

Specialization cards add domain checks. They must not contradict or waive
anything in this file.

## Goal nail (before any architecture prose)

Force explicit answers:

| Field | Meaning |
|-------|---------|
| Primary goals (priority order) | latency / throughput / reliability / cost / observability / dev velocity / security / other |
| Hard constraints | protocols, consistency, backward compat, stack, compliance, solo-maintainer capacity |
| Success metrics | prefer quantitative; name the unit |
| Acceptable trade-offs | what may be sacrificed; what must not |

If any field is missing or vague on an L2/L3 task → output **GOALS-REQUIRED**,
list the gaps, stop substantive review.

## Required proposal structure (ask proposer to use this)

1. **Current problems** — severity-ordered, with evidence
2. **Optimization overview** — 3–5 core changes only
3. **Before / After** — table: component, responsibility, data flow, failure handling, state ownership
4. **Critical paths & edge cases** — happy path + failure + retry / timeout / duplicate
5. **Risk & migration** — high-risk points, blast radius, rollback
6. **Observability & debugging** — how to locate faults after the change
7. **Do not do** — attractive optimizations that are not worth it here

If the proposal lacks this shape, the reviewer may restructure it into this
shape as a **normalization pass** (not acceptance).

## Four review layers (question types)

Always ask these *types* of questions. Concrete bullets come from the
specialization card — see `layered-checklist.md`.

1. **Correctness & assumptions** — symptom vs root cause; smuggled capabilities; broken invariants
2. **System completeness** — failure handling; state ownership/recovery; observability; security boundaries
3. **Complexity & maintainability** — excess abstraction; solo debuggability; cost of adding a similar feature; sync→opaque async
4. **Migration & risk** — staged vs big-bang; rollback cost; client/traffic blast radius; hidden perf/cost regression

## Techniques (tier-gated)

| Technique | L1 | L2 | L3 |
|-----------|----|----|-----|
| Structured output / normalize | ✓ | ✓ | ✓ |
| Layered checklist (domain-filled) | light | ✓ | ✓ |
| Before/After + verdicts | ✓ | ✓ | ✓ |
| Critical path walk (2–3 paths incl. failure) | — | recommended | required |
| Adversarial pass (reliability / security / solo maintainer) | — | optional | required |
| Short ADR per major Accept | — | required | required |
| Pilot subsystem before wide rollout | — | recommended | required |

Adversarial prompt (L3): ask for the **5 most likely breakages** with concrete
counterexamples from reliability-engineer, security-engineer, and
solo-maintainer angles. Prefer a **different model or role-isolated pass**
when available; same-model roleplay is allowed but mark `adversarial: same-model`.

## Non-negotiable anti-patterns (always flag)

- More services / more async treated as inherently "optimized"
- Happy path polished; retries, duplicates, partial failure thin
- New middleware/framework whose learning/debug cost a solo owner can't bear
- "Decoupling" that replaces explicit sync contracts with implicit event contracts
- Theoretical scalability bought by sacrificing current-stage simplicity and observability

## Kernel floors (specialization cannot lower)

- Failure paths must be reviewed at L2+
- Rollback / staged migration must be reviewed when data, protocol, or multi-component rollout is involved
- Security/auth boundary relaxation is always an L3-raising signal
- "Do not do" section required in the review output at L2+
