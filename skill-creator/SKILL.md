---
name: skill-creator
description: Create new skills, evaluate and iteratively improve them, and package them for distribution — without binding to any specific agent runtime. Use when the user wants to build a skill from scratch, draft and run evals to measure skill quality, compare candidate versions, tune a skill's description for better triggering, or package a finished skill. Triggering evaluation is done through a runtime-pluggable adapter interface (Claude Code, Codex, Cursor, or a manual fallback) so the same workflow runs in any agent environment.
---

# Skill Creator (runtime-agnostic)

A skill for creating skills and iteratively improving them — **not tied to Claude Code or any single agent runtime**. It owns two layers of the meta-skill stack:

- **L0 Generation** — turn an intent into a skill draft.
- **L1 Evaluation** — measure skill quality with evals, compare candidates, iterate.

The companion skill **skill-evolution** owns L2 (case-driven evolution) and L3 (accumulating what "a good skill" means). The two are independent and reference each other by document only; either can be used alone.

## High-level flow

1. Decide what the skill should do and roughly how.
2. Draft the skill (structure + description + references/templates).
3. Write a few test prompts (evals).
4. Run the skill against the evals via a **runner adapter** (or the manual fallback).
5. Review results with the user — qualitative + quantitative.
6. Rewrite based on feedback; repeat until satisfied.
7. Optionally tune the description for triggering accuracy.
8. Package.

Your job is to figure out where the user is in this flow and help them progress. Be flexible — if the user wants to "just vibe", do that instead of running full evals.

## Runtime-agnostic by design

This skill never calls a specific runtime directly. The one runtime-dependent step — *run a query and detect whether the agent consulted the skill* — goes through the **runner adapter interface** defined in `references/runner-adapter.md`. No adapter is shipped; examples for Claude Code, Codex, and Cursor are in `references/adapter-examples.md` (marked *example, not shipped*). With no adapter, use the **manual eval path**: run the query in whatever environment the user has, then fill `triggered` into the results JSON by hand or with an external script. The grading and improvement logic is identical either way.

## L0 — Generation

### Capture intent
Extract from the conversation where possible (tools used, steps taken, corrections made, I/O formats observed), then fill gaps with the user:
1. What should this skill enable the agent to do?
2. When should it trigger? (user phrases / contexts)
3. Expected output format?
4. Set up test cases? Skills with objectively verifiable outputs benefit; subjective-output skills often don't. Suggest a default by skill type, let the user decide.

### Pre-gate (avoid over-generation)
Before drafting, ask: *has this need recurred ≥ a few times, or is it a one-off?* A skill carries lifetime maintenance cost and consumes the agent's attention budget every session it's mounted. One-offs don't deserve a skill — write the answer inline instead. (This is the L0 gate from the meta-skill design; it prevents skill bloat.)

### Draft
Use `templates/skill-skeleton/`. Write `SKILL.md` with frontmatter (name + description) and a body that loads its heavy detail progressively from `references/` and `templates/` rather than inlining everything. See `references/skill-anatomy.md`.

The frontmatter `description` is the **primary triggering mechanism** — it must say both *what the skill does* and *specific contexts when to use it*. All "when to use" info goes here, not in the body.

### Interview & research
Proactively ask about edge cases, I/O formats, example files, success criteria, dependencies. Don't write test prompts until this is pinned down. This interview doubles as the **intake batch**: ask all Level-3 questions (see Question Audit below) in one pass here, so the drafted skill never needs to interrupt its user mid-run.

### Question Audit / autonomy profile (mandatory before finalize)
A skill that makes its user interrupt mid-run is a leaky SOP — questions are defects, and their placement is a design decision. Before finalizing any skill:

1. **Simulate a run** and count every point where the skill would want to "ask the user."
2. For each point, exactly one of three fates:
   - **Default it** — the skill carries the preset answer (e.g. "prefer CDP when a browser is present"), states it, logs it, never asks.
   - **Gatable it** — the answer is checkable from the environment (repo, logs, eval evidence, feature map). The skill queries the environment, not the human.
   - **Register it** — an explicit upgrade point for decisions that change the conclusion, cannot be derived, AND are irreversible or high-controversy. Registered points must name their trigger conditions. Escape hatches like "ask the user as needed" are not allowed — an upgrade point without criteria is a hole, not a feature.
3. **Silent guessing is banned.** Every decision point must be one of: has a default, has a checkable gate, or is a registered upgrade point. No fourth path — a silent guess is tomorrow's revert.
4. **Problems move to the edges, not into the middle.** All registered upgrade points fire at intake (batched, one pass) or at delivery (as a flagged list the user audits after the fact) — never sprinkled through execution.
5. Output an **autonomy profile** for the skill: which decisions have defaults, which are environment-answered, which are registered human gates. A skill without this profile has random autonomy.

## L1 — Evaluation

### Write evals
Use `templates/evals.json`. Each eval = `prompt` + `expected_output` + `expectations` (verifiable statements) + optional `files`. Queries should be realistic, concrete, with detail (paths, context, names) and a mix of lengths — focus on edge cases, not clear-cut ones. See `references/evals-schema.md`.

### Run evals
Via adapter or manual path, run each query **≥3 times** to get a reliable trigger rate (triggering is stochastic). See `references/runner-adapter.md`.

### Grade
Compare actual output against `expectations`; compute pass rate. For description tuning, compare *incumbent* vs *challenger* descriptions on the same eval set. See `references/improvement-loop.md`.

### Review with the user
Present results — both examples (so the user sees real outputs) and quantitative metrics. If an adapter produced an HTML report, open it; otherwise show results inline. **Review real outputs before revising the skill yourself.** The user is the external anchor; don't self-grade in a vacuum.

### Improve
Rewrite based on user feedback + quantitative results. Repeat until satisfied. Then expand the test set and try again at larger scale.

### Indicator ↔ real-case calibration (reflexivity defense)
Eval metrics must be checked against *real post-hoc usage outcomes* (the L2 layer owned by skill-evolution). A skill that aces its evals but underperforms in real use has an eval theater problem — the metrics don't predict reality. Keep eval indicators and real-case outcomes in two-way calibration. This is the L1 reflexity defense: metrics must not grade themselves.

## Description tuning

The `description` field drives whether the agent invokes the skill. After the skill is in good shape, offer to optimize it. The optimization loop (train/test split, iterate, pick by held-out score) is runtime-agnostic; only the trigger-detection step needs an adapter. LLMs generally *undertrigger* skills — so descriptions should be a little pushy, naming concrete trigger contexts even when the user doesn't explicitly ask. See `references/description-tuning.md`.

## Packaging

When done, package the skill. See `references/packaging.md`.

## Files

- `references/skill-anatomy.md` — skill structure (frontmatter, SKILL.md, progressive disclosure)
- `references/evals-schema.md` — evals.json / history.json / results schema
- `references/improvement-loop.md` — draft → test → review → improve; grading rules
- `references/packaging.md` — packaging format
- `references/runner-adapter.md` — the adapter contract (the de-binding seam)
- `references/adapter-examples.md` — Claude Code / Codex / Cursor sketches (example, not shipped)
- `references/description-tuning.md` — description optimization
- `templates/skill-skeleton/` — new-skill scaffold
- `templates/evals.json` — eval file template

## Reflexivity self-check

This skill is itself a meta-skill (a skill that makes skills). Its "what makes a good skill" standard is partly borrowed from the upstream official skill-creator (an external anchor) and partly refined through use. It is an N=1 design until validated by repeated real use. The L1↔L2 calibration above is its built-in defense against self-validating mediocrity.

The Question Audit / autonomy profile is also N=1: it encodes one autonomy philosophy ("questions are defects, batch them at the edges"). If real usage shows skills whose registered upgrade points fire too often (question rate stays high) or too rarely (reverts from silent guessing), re-examine the three-fate rule before blaming users or agents.