# Description Tuning

The frontmatter `description` is the primary mechanism that determines whether an agent invokes a skill. After the skill's body is in good shape, optimize the description for triggering accuracy.

## Why it matters

Agents generally **undertrigger** skills — they don't consult them even when it would help, because many needs look handleable with base tools. A description that only says *what the skill does* will be skipped. A description that also names *concrete contexts when to use it*, including ones the user might not explicitly voice, triggers reliably.

So descriptions should be a little pushy. Not "build a dashboard" but "build a dashboard. Use this whenever the user mentions metrics, internal data, visualization, or wants to display any company data, even without saying 'dashboard'."

## Two failure directions

- **Undertrigger** (too narrow / too abstract) — misses real opportunities. Pushier, more concrete contexts fix this.
- **Overtrigger** (too broad / pushy on lookalikes) — fires on things it shouldn't, lowering `pass_rate` and wasting attention. A challenger that raises `trigger_rate` but drops `pass_rate` is overtriggering — reject it.

Tuning is the search for the boundary between these.

## Optimization loop (runtime-agnostic)

1. **Collect eval queries** — realistic, concrete, edge-case-heavy (see `evals-schema.md`).
2. **Split** ~60% train / 40% held-out test.
3. **Baseline** — run the current description on train, ≥3 runs per query, record `trigger_rate` and `pass_rate`.
4. **Propose a challenger** — rewrite the description to address observed under/overtriggering.
5. **Evaluate challenger** on *both* train and test.
6. **Select by test score** — a challenger that wins on train but loses on test is overfit to the eval set; keep the incumbent. This is why the held-out split exists.
7. **Iteruate** up to ~5 times; record each version in `history.json`.
8. **Pick** the version with the best held-out test `trigger_rate` that doesn't regress `pass_rate` below the floor.

## What to vary

- Add concrete trigger phrases the user might say (including indirect ones).
- Add contexts where the skill helps even if the user doesn't ask for it by name.
- Remove phrasing that matches lookalike-but-wrong contexts (cuts overtriggering).
- Keep *what the skill does* present — it's still the primary signal.

## What not to vary here

- The body, references, templates — those are body-tuning (see `improvement-loop.md`). Description tuning changes only the `description` field. Mixing the two in one iteration confounds which change caused the result.

## Reflexivity reminder

A description that triggers great on your eval set but poorly in real use is overfit. Check real-use trigger outcomes (L2, skill-evolution) against eval `trigger_rate`. If they diverge, the eval queries don't represent real needs — redesign them, not just the description.