# Improvement Loop

The short-cycle, human-driven iteration loop within a single work session. This is L1 — distinct from skill-evolution's L2 long-cycle case-driven evolution across sessions.

## Loop

```
draft → test (run evals) → review (with user) → improve → repeat
```

1. **Draft** the skill (or a challenger version of its description/body).
2. **Test** — run the eval set. Via adapter (≥3 runs per query) or the manual path. Produce `eval-results.json`.
3. **Review** — show the user real outputs *and* quantitative metrics, before you revise anything yourself. The user is the external anchor; self-grading in a vacuum is the reflexivity failure mode.
4. **Improve** — rewrite based on user feedback + metrics. Only change the layer the diagnosis points at (see below).
5. **Repeat** until satisfied, then expand the test set and try at larger scale.

## Grading rules

For each eval run:
- `triggered` (bool) — from adapter or manual fill.
- `pass_rate` = `expectations_passed / total_expectations`.
- `trigger_rate` = `triggered_runs / total_runs` (across the ≥3 repeats of a query).

For version comparison (improvement mode):
- Compare **incumbent** vs **challenger** on the *same* eval set.
- A challenger **wins** if it improves on a target signal without regressing the other below an acceptable floor.
- Record in `history.json`: `version`, `parent`, `expectation_pass_rate`, `trigger_rate`, `grading_result` (`won`/`lost`/`baseline`).

## Two-signal diagnosis (fix the right layer)

Triggering and output quality are independent signals:

| Symptom | Diagnosis | Fix layer |
|---|---|---|
| High trigger_rate, low pass_rate | Triggers fine, body wrong | Body / references |
| Low trigger_rate, high pass_rate (when triggered) | Body fine, description wrong | Description |
| Low on both | Both, or description mismatched to intent | Description first (else you're testing the wrong skill) |
| High on both | Done (but check real-case calibration below) | — |

Fixing the wrong layer wastes a full cycle. Diagnose before editing.

## Description tuning vs body tuning

- **Body tuning**: change `SKILL.md` body, `references/`, or `templates/`. Re-run evals; compare `expectation_pass_rate`.
- **Description tuning**: change only the frontmatter `description`. Re-run evals; compare `trigger_rate` (and check pass_rate didn't drop — a pushier description that triggers on lookalikes will *lower* pass_rate). See `description-tuning.md`.

## Train / test split (for description tuning)

To avoid overfitting a description to its eval set:
- Split evals ~60% train / 40% held-out test.
- Iterate on train; select the challenger by **test** score, not train score.
- A challenger that wins on train but loses on test is overfit — keep the incumbent.

## Reflexivity defense: indicator ↔ real-case calibration

Eval metrics grade the skill in a controlled setting. Real quality is what happens in uncontrolled real use — which is L2's territory (skill-evolution). Keep them calibrated:

- If a skill aces its evals but real-use post-hoc outcomes are poor → **eval theater**. The metrics don't predict reality; redesign the evals (more realistic prompts, sharper expectations) and feed the real cases back in.
- If real-use outcomes are good but evals fail → the evals are miscalibrated, not the skill.

This two-way check is the L1 defense against self-validating mediocrity: metrics must answer to an external anchor (real outcomes), not just to themselves.