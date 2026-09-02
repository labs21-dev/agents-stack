# Env tools: letting the agent run its own verification

The third precondition of verification autonomy: the environment allows the
agent to run. Per project shape, what capability the agent gets and what an
assertion reads.

| Project shape | Tool surface | Verification action | Assertion reads |
|---|---|---|---|
| Web | Chrome DevTools Protocol (CDP) | open page, click, read DOM | DOM structure + no new console errors + network responses |
| Web (performance) | CDP Performance / Trace | capture trace, heap snapshot | specific metrics (LCP, memory curve), not "feels faster" |
| iOS | Simulator + callable tools | launch, tap, screenshot, read logs | screenshot comparison + log keywords |
| CLI | shell execution | run the command itself | stdout content + stderr + exit code — check all three; exit 0 alone is a fake green |
| Electron / desktop | launch dev build + screenshots + log reading | launch, operate, screenshot, read main-process logs | screenshot state + log assertions |
| Library / SDK | test runner | run unit/integration tests | assertion count and content, not "all green" in one sentence |

## Granting principles

1. **Grant tools, not screenshot loops.** A human screenshotting for the agent
   = human still in the loop. Let the agent screenshot itself.
2. **Triple-check assertions**: exit code / stdout / stderr all inspected.
   Exit code alone is a fake green.
3. **Performance and resources must be numeric assertions** (trace metrics,
   heap size). "Should be fast" is unverifiable.
4. **Browser agents get an operable browser** (CDP-class tooling), not an
   imagined page.

## Anti-patterns

- "Write it, then tell me you tested it" — self-declared completion is not
  verification (verifier ≠ generator, `role-pipeline.md`).
- Happy-path-only assertions. Boundaries are where agents fail.
- A "human confirms" step inside the script — see anti-pattern 14 in
  `anti-patterns.md`.