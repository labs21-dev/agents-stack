# Runner Adapter (the de-binding seam)

The one runtime-dependent step in this skill is: *run a user query against an agent that has access to the skill, and detect whether the agent consulted the skill.* This file defines the contract that lets any runtime implement that step without the skill itself depending on any of them.

No adapter is shipped with this skill. Implementations are the user's environment knowledge. Examples (Claude Code, Codex, Cursor) are sketched in `adapter-examples.md` and marked *example, not shipped*.

## Contract

An adapter provides a single operation:

```
run_query_with_skill(
  query: str,
  skill_name: str,
  skill_description: str,
  timeout?: int,
  model?: str | None,
) -> {
  triggered: bool,
  evidence: str,
  raw_output_ref: str | null,
}
```

### Inputs
- `query` — the user's eval prompt verbatim.
- `skill_name` — the skill's frontmatter `name`.
- `skill_description` — the description string under test.
- `timeout` — optional, seconds.
- `model` — optional, for runtimes that select models.

### Outputs
- `triggered` — did the agent consult/read/invoke the skill? (bool) The detection method is the adapter's choice and varies by runtime (tool-use event, rules-file read, skill-load event, custom hook, etc.).
- `evidence` — human-readable detection basis: which event / tool call / log line led to the verdict. Used for audit and debug. Must be specific enough that a human can verify the verdict.
- `raw_output_ref` — path or handle to the full agent output, for human review and for grading `expectations`.

## What the contract deliberately does not specify

- **How the skill is made available to the agent.** Each runtime has its own discovery/injection mechanism (commands, rules, `<SKILLS>` injection, plugin manifest). The adapter handles mounting; the skill doesn't prescribe it.
- **How triggering is detected.** Different runtimes expose different signals. The adapter picks a reliable one and reports it via `evidence`.
- **Whether detection is live or replayed.** An adapter may run the agent live, or replay a recorded session, or even ask a human — as long as it returns the contract.

## Manual fallback (no adapter)

If no adapter is available, run the query in whatever environment the user has and fill the contract outputs yourself (or with an external script):

1. Run the query against the agent with the skill mounted (per the runtime's normal mechanism).
2. Observe whether the agent consulted the skill (read its file, referenced its name, followed its instructions).
3. Write `triggered`, `evidence`, and `raw_output_ref` into the corresponding `eval-results.json` run entry.

The grading and improvement logic in `improvement-loop.md` consumes `eval-results.json` identically whether it came from an adapter or the manual path. The manual path is slower but fully functional — the skill is usable with zero runtime integration.

## Reliability note

Triggering is stochastic. Run each query **≥3 times** and aggregate (the contract is per-run; the eval runner calls it repeatedly). A single run's `triggered` is a sample, not a verdict.