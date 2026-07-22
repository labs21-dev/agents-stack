# Adapter Examples (Claude Code / Codex / Cursor)

> **Example, not shipped.** These are sketches showing how to implement the `runner-adapter.md` contract for three runtimes. They are not bundled — copy and adapt to your environment. Each marks where runtime-specific behavior enters.

The contract:

```
run_query_with_skill(query, skill_name, skill_description, timeout?, model?)
  -> { triggered: bool, evidence: str, raw_output_ref: str | null }
```

---

## Claude Code

Claude Code exposes a programmatic mode via the `claude` CLI. Skills surface as slash commands / command files; triggering is detectable from stream events.

### Mounting the skill
Place a command file under `.claude/commands/<name>.md` with YAML frontmatter `description:` set to the `skill_description` under test, and a body that presents the skill. Claude Code's `available_skills` list picks it up.

### Running
```
claude -p "<query>" --output-format stream-json --verbose --include-partial-messages
```
- Remove the `CLAUDECODE` env var when nesting `claude -p` inside a Claude Code session (the guard is for interactive-terminal conflicts; programmatic subprocess use is safe).
- Parse stream-json lines for `stream_event` of type `content_block_start` with `content_block.type == "tool_use"`. If the tool name is the skill/command, `triggered = true`.
- `evidence` = the tool-use event name + the accumulated partial JSON containing the skill name.
- `raw_output_ref` = path to the captured full stream.

### Caveats
- `claude -p` and the stream-json protocol are Claude Code-specific. This is *why* it lives in an example, not in the core skill.
- A query too simple for skill consultation may not trigger even with a perfect description — the agent handles trivial queries with base tools. Use substantive, multi-step eval prompts.

---

## Codex (OpenAI Codex CLI / agent)

Codex-style agents generally consult skills via project rules / instructions files rather than a named tool call. Triggering is detected by observing whether the skill's content influenced the agent's plan or output.

### Mounting the skill
Expose the skill as a rules/instructions document the Codex agent reads (e.g., an `AGENTS.md` section or a project rules file). The `skill_description` becomes the heading/summary the agent sees when deciding what to read.

### Running
Run the Codex agent headless against the query with the rules file in place. Capture the agent's plan/scratchpad and final output.

### Detecting triggered
Codex doesn't emit a "skill invoked" tool event. Detect indirectly:
- Did the agent's plan/scratchpad reference the skill's name or distinct instructions?
- Did the output follow the skill's specific approach (matching an `expectation` that *only* this skill prescribes)?
- Set `triggered = true` only if there's positive evidence the skill's content was used, not merely that it was available.
- `evidence` = the quoted scratchpad/output fragment that shows the skill's influence.
- `raw_output_ref` = path to the captured plan + output.

### Caveats
- Indirect detection is noisier than a tool-use event. Prefer an `expectation` that is *characteristic* of the skill (something it uniquely prescribes) as the trigger proxy, and keep `evidence` concrete.
- Because detection is inference, run ≥3 repeats and aggregate; a single ambiguous run should not flip the verdict.

---

## Cursor

Cursor loads rules from `.cursor/rules/*.mdc` (or project rules) into the agent's context. Triggering is detected by whether the loaded rule materially shaped the response.

### Mounting the skill
Create `.cursor/rules/<skill-name>.mdc` with a `description` matching `skill_description` under test, and the skill body as the rule content. Cursor's retrieval uses the description to decide when the rule applies.

### Running
Run the query through Cursor's agent (Composer / Chat) with the rule file present. Capture the response and any agent-step traces Cursor exposes.

### Detecting triggered
Cursor doesn't emit a skill-invocation event either. Detect by:
- Did the response follow the rule's distinctive instructions?
- If Cursor exposes which rules were attached to the request, use that directly as `triggered`.
- Otherwise infer from the response matching a characteristic `expectation`.
- `evidence` = the attached-rules indicator if available, else the quoted response fragment.
- `raw_output_ref` = path to the captured response.

### Caveats
- Cursor's rule-retrieval is description-driven and stochastic — another reason for ≥3 repeats.
- A pushy, specific `description` (per `description-tuning.md`) improves retrieval reliability here directly.

---

## Cross-runtime pattern

All three reduce to: **mount the skill in the runtime's native discovery mechanism → run the query headless → detect consultation via the runtime's most reliable signal → record `{triggered, evidence, raw_output_ref}`.** The core skill never knows which runtime; only the adapter does.