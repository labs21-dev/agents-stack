# Anti-patterns — how this skill fails

## Pipeline discipline

1. **Skipping a gate "because this run is small."** Even a one-file fix writes
   a minimal spec + checklist; the format is the contract. Artifact
   degradation on L1/L2 bug-fixes is the only sanctioned shortcut, and it is
   pre-declared in `bugfix-mode.md`, not improvised.
2. **Single-metric pass.** "Coverage 100%, complexity 4, ship" without a
   mutation cross-check. A single metric never passes (`metric-combo-rules.md`).
3. **Grade fixed at step 0.** Discovering L3 reality but keeping L2 gates.
   `feedback-upgrade.md` reopens the grade.
4. **Averaging a cross-bucket corner down.** Any L3 corner runs the whole task
   at L3 — no matter how small the diff.
5. **Down-grading to dodge work.** L3→L2 only on genuine evidence + real
   reversibility.
6. **Self-declared gate pass.** The verifier is the generator; the coder
   grading its own homework. Verifier must run from a distinct agent or a
   refutation-instructed stage (`role-pipeline.md`).
7. **Suppressing the category disclosure.** It is the skill's boundary, not
   hedging. Always filled in.
8. **"What AI could not verify" left empty on a UI-affecting change.** If it
   is empty, the verification was too narrow — widen it.

## Spec integrity

9. **AI edits the spec to match what the code ended up doing.** Deviations go
   back to Gate A, not into a silent rewrite. (If the human ordered the
   change, the spec is amended and re-logged — never silently.)
10. **Spec grows past one page.** The human stops reading → Gate A
    rubber-stamps even when required. If an L3 spec exceeds a page, the spec
    is the defect — rewrite it; do not demand more human attention.
11. **Forcing protocol-adversarial-design on non-protocols.** Its own gate
    STOPs, but only after wasted motion. Delegate on protocol character only.

## Verification quality

12. **Assertions check "no error" instead of results.** Exit code 0 is not
    verification; "the search returns the right three rows" is.
13. **Happy-path-only assertions.** Boundaries (empty input, CJK text, large
    volume) are where agents fail most.
14. **"人工確認" steps left inside a script.** Each is a leftover of the human
    being in the loop. Convert to machine-checkable, or explicitly mark it as
    a human acceptance point (and minimize those).

## Gate honesty

15. **Prose where a gate belongs.** "Don't import X from Y" as a doc sentence
    → lint rule; the doc holds only the why the lint cannot express.
16. **Decorative red lines.** A rule added but never tested against a known
    bad example may never fire. Reverse-test every new constraint.
17. **Rule mountain.** Twenty new constraints at once → false-positive flood →
    human disables CI → all constraints dead. Add 1-2 at a time; warn-first
    (`hard-constraints.md`).