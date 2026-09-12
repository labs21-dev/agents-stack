# Risk tiers (L1 / L2 / L3)

Grade by **blast radius × reversibility × invariant touch**. Specialization
`L_TRIGGERS` may raise; kernel floors may raise; never grade below a raised floor.

## Default triggers

| Tier | Typical triggers |
|------|------------------|
| **L1** Local | Single module/file area; no external contract change; easy revert; no new datastore/middleware; behavior intended equivalent |
| **L2** Subsystem | Clear boundary; may change internal APIs; shadow/dual-write or feature-flag possible; new failure modes inside one subsystem; observability changes |
| **L3** Architecture / irreversible | Protocol or wire contract break; cross-service redesign; new message bus/orchestrator/framework; data migration with hard rollback; auth/trust boundary change; multi-team or multi-client blast radius; "optimize the whole architecture" |

## Raising signals (any one → at least L2; two+ or trust/data → L3)

- Touches idempotency, exactly-once/at-least-once semantics, or consistency model
- Introduces async orchestration where sync existed
- Increases number of independently failing components
- Rollback needs data rewrite or client coordinated deploy
- Security verification / authn / authz / webhook trust changes

## Required depth

### L1

- Goal nail (short)
- Normalize or skim proposal structure
- Correctness layer light + specialization FAILURE_MODES top 3 if card valid
- Per-change Accept / Modify / Reject
- No mandatory ADR / adversarial / pilot

### L2

- Full goal nail
- Layers 1–4 with specialization fill-in
- Before/After attention on state + failure handling
- Rollback / staged path explicit
- Short ADR stub per Accept
- Path walk recommended; adversarial optional
- Pilot recommended if migration non-trivial

### L3

- Everything in L2
- Path walk required (≥2 paths including one failure/retry/duplicate)
- Adversarial pass required (5 breakages + counterexamples)
- Pilot **required** before wide rollout — name the pilot slice
- Explicit "Do not do" section in the review
- Reject big-bang when staged option exists unless human accepts documented risk

## Confidence

State `tier_confidence: high | medium | low`. If low, bias **up** one tier
when failure cost is high (same spirit as agentic-clean-discipline grade reopen).
