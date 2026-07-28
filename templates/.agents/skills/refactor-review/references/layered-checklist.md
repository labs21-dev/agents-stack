# Layered checklist — question types

Fill each layer with items from the specialization card. Do not invent a
40-item universal list. Prefer **≤10 domain checks total** across layers.

## Layer 1 — Correctness & assumptions

Ask:

- Is the diagnosis severity-ordered and evidenced, or symptom-as-root-cause?
- What capabilities does the proposal assume that this system may not have?
- Which specialization INVARIANTS are at risk? (hard only; hypotheses → open Qs)
- Are messaging/consistency semantics preserved or silently changed?

## Layer 2 — System completeness

Ask:

- Timeouts, retries, dead letters, compensation, human intervention — covered?
- Who owns state? How recovered? Split-brain avoided?
- Trace / metric / structured log / business events — still enough to debug?
- Authn/authz/webhook verification/least privilege — relaxed or preserved?
- Map specialization FAILURE_MODES → concrete handling in the proposal

## Layer 3 — Complexity & maintainability

Ask:

- New concepts/abstractions: necessary for the stated goals, or elegance debt?
- Can a solo owner still debug the critical path in one sitting?
- Cost to add one more similar feature: down or up?
- Did a simple sync flow become hard-to-reason async choreography?
- Cross-check specialization DO_NOT — is the proposal doing any of them?

## Layer 4 — Migration & risk

Ask:

- Staged rollout possible? Or forced big-bang?
- Rollback cost and trigger conditions?
- Client / traffic / data blast radius?
- Hidden latency, cost, or operational load regression?
- What EVIDENCE_REQUIRED is still missing before Accept?

## How to use with a valid card

1. Copy INVARIANTS into Layer 1 as gates (hard) or questions (hypothesis).
2. Copy FAILURE_MODES into Layer 2; demand a handling row each.
3. Copy DO_NOT into Layer 3; flag matches as Modify/Reject candidates.
4. Copy EVIDENCE_REQUIRED into Layer 4; missing evidence → cannot Accept at L2+.
