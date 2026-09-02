# Role pipeline

Uncle Bob's Specifier → Coder → Refactorer → Architect, mapped onto this
skill's gates. The value is **role separation**, not the four-role shape.

## Core rule (do not violate)

**The verifier must not be the generator.** No role grades its own work.

- Multi-agent run: verify-gate and metric-gate run from a distinct agent.
- Single-agent run: verify runs from a separate prompt stage, instructed to
  *refute*, not confirm.

Self-grading is the `self-declared gate pass` anti-pattern
(`anti-patterns.md` #6). It silently re-enables the silent-failure mode the
gates exist to prevent. Role separation is the mechanism that keeps the gates
honest; without it the whole pipeline collapses to the coder marking its own
homework.

## Role → gate mapping

| Uncle Bob role | This skill | Output |
|---|---|---|
| Specifier | spec gate + spec self-check | hard spec, invariants |
| Coder | generate | code |
| Refactorer | metric-gate fail → back to Coder → re-run verify | cleaner code |
| Architect | metric gate (dependency/structure) + L3 human line-read | structure verdict |

No new steps. Roles organize existing gates by who runs them.

## Refactorer loop (the missing piece)

Metric gate fails (complexity high, cohesion low) → Coder refactors → re-run
verify gate → re-run metric gate.

This is a specialization of `feedback-upgrade.md`, not a new mechanism:
downstream evidence (metric fail) reopens upstream work (refactor) before the
grade itself changes. If refactor still fails after a bounded number of loops →
re-grade up or STOP.

## Formalization progression

Each role is more formal than the last; human intervention decreases:

| Stage | Formality | Human |
|---|---|---|
| Specifier | natural → hard spec | high (spec self-check) |
| Coder | execution | low |
| Refactorer | metric-driven | low |
| Architect | structural judgment | low (L3: human read) |

## Runtime-agnostic

In single-agent runs, "role" = distinct prompt stage, not distinct agent. The
core rule still holds: the verify stage's prompt must instruct refutation, and
it must not share context-state with the generate stage that biases it toward
confirmation.