# Verify Report: <feature name>

STATUS: draft | passed | failed

> Run in a FRESH context (subagent or separate command) — never the same
> context that wrote the code self-certifying.

## Environment

- Build tool: <tool + version>
- Test runner: <runner>
- Simulator/device: <id looked up, never hardcoded from memory>

## Results

| # | Check | Command / action | Evidence (path or paste) | Result |
|---|---|---|---|---|
| 1 | build | `<cmd>` | <log path or summary line> | pass/fail |
| 2 | BE tests | `<cmd>` | <runner summary: N passed, 0 failed> | pass/fail |
| 3 | FE golden path | <simulator action> | <screenshot path> | pass/fail |
| 4 | FE unhappy path (top from spec) | <action> | <evidence> | pass/fail |
| … | verifiable steps from 01-spec | | | |

Evidence rules:
- A bare "passed" is a failed check. Cite the raw summary line, file path,
  or screenshot.
- "Empty output with exit 0" is a failure, not a success — inspect the
  output before believing a tool.
- Check `git status` after test runs; note (don't revert) unexpected config
  diffs caused by the runner.

## What AI could not verify

<Needs real device / real users / production data / human taste /
multi-session effects. NEVER empty on a UI-affecting change — if empty, the
verification was too narrow; widen it.>

## Failed checks & analysis

<Each failure: what happened, suspected cause, and the fork — code bug
(fix in Phase B) or spec bug (back to Gate A).>