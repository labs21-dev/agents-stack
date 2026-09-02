# Feedback upgrade — reopen grade from downstream evidence

Grade is a hypothesis set at step 0. Downstream gate results are evidence.
Evidence falsifies the hypothesis. The grade reopens.

## Triggers

After any gate, if any:

- Verify-gate / mutation failure density far above the grade's prediction →
  re-grade (usually up), re-run denser gates.
- Delegated `protocol-adversarial-design` reports danger above initial grade
  → re-grade up.
- Each verify cycle surfaces a new edge class the spec didn't list → spec was
  soft. Re-harden, or accept lower confidence (no high-quality claim).
- Cross-bucket corner found mid-run → whole task runs at the higher grade.

## How to re-grade

1. State the new grade + the evidence.
2. Re-run gates at the new density. Do not keep prior gates' results as
   "already passed" — denser gates may fail where sparse ones passed.
3. Record the re-grade in the output.

## Direction

Re-grade **up** by default when uncertain and cost is high.
Re-grade **down** (L3→L2) only on genuine evidence of over-graded simplicity
with real reversibility. Never down-grade to skip work.