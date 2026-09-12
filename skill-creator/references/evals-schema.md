# Evals Schema

Data formats for L1 evaluation. Runtime-agnostic — they describe *what* to evaluate and *results*, not how to run the agent.

## evals.json

Located at `evals/evals.json` within the skill directory.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt (realistic, concrete, with detail)",
      "expected_output": "Human-readable description of the expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "The output includes X",
        "The skill used approach Y",
        "The output does NOT do Z"
      ]
    }
  ]
}
```

**Fields:**
- `skill_name` — matches the skill's frontmatter `name`.
- `evals[].id` — unique integer.
- `evals[].prompt` — the task to execute. Realistic and concrete: file paths, personal context, column names, URLs, backstory. Mix lengths; include edge cases and casual/typo phrasing rather than only clear-cut requests.
- `evals[].expected_output` — human-readable success description.
- `evals[].files` — optional input file paths (relative to skill root).
- `evals[].expectations` — verifiable statements. Negative expectations ("does NOT do Z") are allowed and useful.

## eval-results.json

Output of running evals (via adapter or manual path). One entry per (eval × run).

```json
{
  "skill_name": "example-skill",
  "description_under_test": "the description string used this run",
  "runs": [
    {
      "eval_id": 1,
      "run": 1,
      "triggered": true,
      "evidence": "tool_use: Skill(example-skill) at content_block_start",
      "expectations_passed": ["The output includes X"],
      "expectations_failed": ["The skill used approach Y"],
      "pass_rate": 0.5,
      "raw_output_ref": "evals/runs/1-1.txt"
    }
  ],
  "aggregate": {
    "trigger_rate": 0.9,
    "mean_pass_rate": 0.7
  }
}
```

**Fields:**
- `description_under_test` — which description string was evaluated (for description-tuning comparisons).
- `runs[].triggered` — did the agent consult the skill? (bool) Filled by the adapter or manually.
- `runs[].evidence` — human-readable detection basis (which event/tool/log line).
- `runs[].expectations_passed` / `expectations_failed` — graded against `evals.json`.
- `runs[].pass_rate` — fraction of expectations passed.
- `runs[].raw_output_ref` — path to the full output for human review.
- `aggregate.trigger_rate` — fraction of runs where `triggered` was true.
- `aggregate.mean_pass_rate` — mean of per-run `pass_rate`.

## history.json

Tracks version progression in improvement mode. Located at workspace root.

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "example-skill",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "trigger_rate": 0.6,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "trigger_rate": 0.85,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "trigger_rate": 0.9,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

**Fields:**
- `current_best` — version id of the best performer so far.
- `iterations[].version` — version id (v0, v1, ...).
- `iterations[].parent` — parent version this was derived from.
- `iterations[].expectation_pass_rate` — from grading.
- `iterations[].trigger_rate` — from eval-runs.
- `iterations[].grading_result` — `baseline` | `won` | `lost` (vs parent).
- `iterations[].is_current_best` — bool.

## Two independent signals

Note that **trigger_rate** and **expectation_pass_rate** are separate:
- A skill that triggers reliably but produces wrong output → good description, bad body.
- A skill that produces right output when triggered but rarely triggers → good body, bad description.
- Diagnose which before improving — fixing the wrong one wastes a cycle.