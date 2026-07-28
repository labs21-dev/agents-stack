# Specialization card lint

Run after the card is filled (`templates/specialization-card.md`).

## Pass criteria (all required)

| Check | Rule |
|-------|------|
| Fields present | DOMAIN, INVARIANTS, FAILURE_MODES, EVIDENCE_REQUIRED, L_TRIGGERS, DO_NOT, OUT_OF_SCOPE |
| Counts | INVARIANTS 3–7; FAILURE_MODES 3–7; EVIDENCE_REQUIRED ≥ 2; DO_NOT ≥ 2 |
| DOMAIN | One concrete domain phrase (not "general software" / "architecture") |
| Falsifiers | Each INVARIANT has a one-line **falsify:** how a reviewer could prove it wrong or violated |
| No waive | Card text must not waive kernel floors (see Ban list) |
| Tighten only | L_TRIGGERS may raise tier vs kernel defaults; must not say "skip rollback" / "L1 enough for protocol break" without kernel-compatible justification |

## Ban list (instant fail)

Reject the card (or strip the clause and re-lint) if it contains intent to:

- skip / ignore failure paths, retries, idempotency, or rollback "for this task"
- treat diagrams or narrative completeness as sufficient evidence
- override kernel anti-patterns as "acceptable here" without an explicit
  **accepted-risk** verdict deferred to the human (and then still L3)

## Hypothesis downgrade

If an INVARIANT's `falsify:` is missing, vague ("looks wrong"), or untestable
in principle → mark that row `status: hypothesis`. Hypotheses appear in the
review as open questions; they must **not** be used as hard Accept gates.

If **fewer than 3** INVARIANTS remain as hard (non-hypothesis) → card is
**weak**: allow L2 max unless the human upgrades; recommend repairing
falsifiers before L3.

## Degrade policy

| Lint result | Allowed tier | Label |
|-------------|--------------|-------|
| Pass | per risk-tiers + L_TRIGGERS | `specialization: valid` |
| Weak (pass shape, <3 hard invariants) | ≤ L2 | `specialization: weak` |
| Fail after one repair attempt | L1 only | `specialization: invalid` |
| Missing card entirely | L1 only | `specialization: absent` |

On L1-only degrade, still run goal nail + light correctness questions; do
**not** claim domain completeness.

## Optional 30s adversarial on the card (L2+ recommended)

Before reviewing the proposal, answer:

> Which 2 lines in INVARIANTS / FAILURE_MODES are most likely fabricated or off-domain? Delete or rewrite with a real falsifier.

Record `card_adversarial: done | skipped`.
