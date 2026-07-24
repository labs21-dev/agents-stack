# Delegation to protocol-adversarial-design

Delegate only on protocol character. Narrow handoff, not a merge.

## When

The task involves any of: shared mutable state / concurrency, retry /
idempotency, distributed handoff, trust boundary / authorization, lifecycle
state machine / approval-cancel race.

## How

1. Hand the protocol slice to `protocol-adversarial-design`.
2. It runs its own gate. If it STOPs → the protocol isn't dangerous enough for
   a formal contract. Write ordinary acceptance criteria; don't force a model.
3. If it passes → it returns hard invariants + alignment tests (3-5 cases).
4. Adopt invariants as this task's spec. Feed alignment tests into the verify
   gate as required-pass core. Copy "model boundaries / uncovered surfaces"
   into the category disclosure and assumptions-to-verify.

## Feedback arrow

If the delegated run reports danger above the initial grade → trigger
`feedback-upgrade.md`: re-grade (usually up), re-run denser gates.

## Do not delegate

- CRUD with a single writer
- Pure generation with no shared state
- Any case where the dangerous interleaving isn't real (ceremony, not
  discipline)