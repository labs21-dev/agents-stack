# Delegation: when this workflow hands work to other skills

This workflow is the orchestrator. It does not re-implement capabilities that
sibling skills own — it delegates at fixed points and adopts their outputs as
its own artifacts.

## Delegation table

| Situation | Delegate to | What this workflow adopts |
|---|---|---|
| Phase B: task has protocol character (concurrency, retries/idempotency, distributed handoff, authz/trust boundary, lifecycle state machine, cancel races) | repo's adversarial/protocol-design skill (e.g. `protocol-adversarial-design`) | its invariants + alignment tests become the spec's backend section and the verify gate's core |
| Phase 0/Phase C: deciding how much verification a grade deserves | repo's clean-discipline skill (e.g. `agentic-clean-discipline`) | its risk matrix for L1/L2/L3 detail; its gate chain for L2/L3 verify depth |
| Phase C: UI-affecting change needs simulator/device evidence | repo's device-interaction skill, or direct simulator tooling | screenshots + hierarchy dumps cited as evidence rows |
| Phase A: the wish itself is fuzzy at the product level (not just technically vague) | repo's multi-lens analysis skill (e.g. `meta-thinking-framework`) | its output becomes the spec's "Open judgment calls" section |
| Tests need modernizing to repo-standard test style | repo's test-modernizer skill if present | modernized test cases in the build report mapping |

Rules:
- Delegation is per-phase and named; the build report records which skill
  produced which section.
- If the repo has no matching skill, do the work inline — never block on a
  missing sibling. The delegation table is opportunistic, not a hard
  dependency.
- Never delegate Gate decisions. Gates belong to the human; skills inform
  them, they don't replace them.

## Environment preflight recipe

Phase 0's check adapts to the repo; the shape:

1. Identify repo type: `ls` for package.json / xcodeproj / go.mod / Cargo.toml
   / pyproject.toml etc.
2. Run the cheapest non-mutating command that proves the toolchain works
   (`xcodebuild -list`, `npm test -- --help`, `go build ./...`).
3. If UI verification is planned: confirm a simulator/device exists
   (`xcrun simctl list devices available` head, or repo equivalent).
4. Note results in the spec's Environment line or the verify report.
5. Any hard failure → 00-stop.md, tell the human exactly what's missing.

Known-flaky-environment lessons (from real runs, generalized):
- Simulator names change between Xcode versions — look the device up, never
  hardcode a name.
- Some test runners mutate config files as a side effect; check `git status`
  after a test run and note (not revert) any unexpected diff.
- If a tool silently succeeds while producing empty/garbage output (e.g.
  upscaling with a wrong model path), treat "empty output with exit 0" as a
  failure — evidence rules apply to tools too.