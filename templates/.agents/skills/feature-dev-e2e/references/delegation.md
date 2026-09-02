# Delegation: handing work to sibling skills

This skill is self-contained for grading, spec hardening, verification, and
metrics. It delegates only where a sibling owns a capability it should not
re-implement, and adopts the sibling's output as its own artifacts.

## Delegation table

| Situation | Delegate to | What this skill adopts |
|---|---|---|
| Protocol character: concurrency, retries/idempotency, distributed handoff, authz/trust boundary, lifecycle state machine, approval/cancel races | `protocol-adversarial-design` | its invariants + alignment tests become the spec's backend section and the verify gate's core |
| The wish itself is fuzzy at the product level (not just technically vague) | `meta-thinking-framework` | its output becomes the spec's "Open judgment calls" section |
| UI-affecting change needs simulator/device evidence | repo's device-interaction skill, or direct simulator tooling | screenshots + hierarchy dumps cited as evidence rows |
| Tests need modernizing to repo-standard test style | repo's test-modernizer skill if present | modernized test cases in the build report mapping |

Rules:

- Delegation is per-phase and named; the build report records which skill
  produced which section.
- If the repo has no matching skill, do the work inline — never block on a
  missing sibling. The table is opportunistic, not a hard dependency.
- Never delegate Gate decisions. Gates belong to the human; skills inform
  them, they don't replace them.

## Protocol delegation detail

1. Hand the protocol slice to `protocol-adversarial-design`.
2. It runs its own gate. If it STOPs → the protocol isn't dangerous enough
   for a formal contract. Write ordinary acceptance criteria; don't force a
   model.
3. If it passes → it returns hard invariants + alignment tests (3-5 cases).
4. Adopt invariants as this task's spec. Feed alignment tests into the verify
   gate as required-pass core. Copy "model boundaries / uncovered surfaces"
   into the category disclosure and assumptions-to-verify.
5. Feedback arrow: if the delegated run reports danger above the initial
   grade → trigger `feedback-upgrade.md` (re-grade up, denser gates).

Do NOT delegate: CRUD with a single writer; pure generation with no shared
state; any case where the dangerous interleaving isn't real (ceremony, not
discipline).

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
- If a tool silently succeeds while producing empty/garbage output, treat
  "empty output with exit 0" as a failure — evidence rules apply to tools too.