---
name: feature-dev-e2e
description: >-
  Unified agentic development system: turns a one-line feature wish or bug
  report into verified, reported code (Lane A task pipeline), hardens the repo
  so agents verify their own work (Lane B infra ladder L0→L5), and authors the
  agent-facing doc set (repo docs SOP). Lane A: analysis → spec/diagnosis →
  build → gate-verified → report, with L1/L2/L3 risk gates, reverse-gate STOP,
  artifact per phase, evidence-not-declaration. Lane B: task-shaping (模糊需求→
  驗證劇本), feature map, hard constraints (說過三次→lint/CI), eval regression,
  autonomy release checklist, AGENTS.md/ADR/SECURITY/CONSTITUTION authoring.
  Use when: a feature goal / wish item / bug-to-fix ("add X", "this crashes,
  fix it"), "do the feature workflow", reviewing or trusting AI-generated code
  via gates, "agent 又不會自己測" / "每次都要我截圖給它", granting agents
  autonomy (auto-merge, cloud agents), repeated corrections that should become
  lint/CI, or "what docs do I need" / AGENTS.md / ADR setup. NOT for: pure
  research or doc-only writing (human-facing PRDs), bug TRIAGE without a fix
  goal, skill authoring/eval (skill-creator), protocol contracts themselves
  (protocol-adversarial-design — delegate), or fuzzy product decisions
  (meta-thinking-framework — delegate).
---

# Feature Dev E2E

One skill, two lanes.

**Lane A — Task pipeline**: a one-line wish becomes verified, reported code
with at most two human touch points (the wish, and value judgments at gates).
**Lane B — Repo infrastructure**: the project is hardened so an agent can
verify its own work, and the agent-facing doc set is authored.

Core laws (all lanes):

1. **The spec is the ceiling of the whole chain.** A wrong spec executed
   perfectly is still wrong; errors correlate downstream — a later phase
   cannot detect an earlier phase's misunderstanding. That is why gates sit
   where they sit.
2. **Verification autonomy is the pivot.** Agent self-verifies ⟺ knows where
   to verify (Feature Map) × knows what passing means (Verification) × the
   environment lets it run (tools, `env-tools.md`). And the invariant:
   **放權等級 ≤ 驗證基建等級** (autonomy level ≤ verification-infrastructure
   level). Don't make the agent smarter; make the project hard to fail.
3. **Trust transfers between gates; it does not appear from nowhere.** Never
   claim "verified correct"; claim "no gate failure observed."

## Hard rules (never violated, any repo, any lane)

1. **Artifact per phase.** Lane A writes a fixed-format file to
   `.agent/features/<slug>/` before the next phase starts. Later phases read
   the files, not conversation memory.
2. **Evidence, not declarations.** Verify items cite raw evidence: test-run
   summaries, build logs, screenshots, console output paths. A bare "passed"
   without evidence is a failed check. Assertions check *results* ("the right
   three rows"), not "no error" (exit code 0 is not verification).
3. **Verifier ≠ generator.** Verification runs in a fresh subagent context
   (or a refutation-instructed separate stage), never the context that wrote
   the code self-certifying.
4. **Human triggers commits/deploys.** The agent never commits, pushes, or
   deploys unless the human explicitly asked in this session. Repo branch
   rules (CLAUDE.md/AGENTS.md) override defaults.
5. **STOP beats guess.** Any gate failure, reverse-gate screen failure,
   preflight failure, or unresolvable ambiguity → stop with a written STOP
   note (`00-stop.md`). Silent guessing is banned.
6. **One fact, one home.** Rules live in exactly one artifact or one doc;
   everything else points. Two copies decay at different rates and the agent
   draws the older one.
7. **Grade reopens on evidence.** Downstream gate results can falsify the
   Phase 0 grade (`feedback-upgrade.md`). Re-grade up by default when cost is
   high.

## Routing — which lane, which mode

| Input looks like | Run |
|---|---|
| Feature wish / bug-to-fix / "run the e2e flow" | Lane A (full pipeline) |
| Fuzzy one-liner to hand an agent ("加搜索功能") | Lane A → task-shaping (用法 A) |
| "Agent can't self-verify / keeps needing my screenshots" | Lane B → infra ladder (usage B) |
| "Said it three times, agent keeps forgetting" | Lane B → hard constraints (L3) |
| "Let agents auto-merge / run autonomously" | Lane B → autonomy release (L5) |
| "What docs do I need / write AGENTS.md / ADR" | Lane B → repo docs SOP |
| "Can I trust this generated code without line review?" | Lane A gates run standalone (below) |

Out of scope: pure research, doc-only writing for humans, bug triage without
a fix goal, skill authoring (→ skill-creator), protocol contracts themselves
(→ protocol-adversarial-design, see `delegation.md`), irreducibly fuzzy
product decisions (→ meta-thinking-framework).

---

# Lane A — Task pipeline

## Phase 0 — Preflight (always)

Run the environment check before any work (recipe in `delegation.md`):
build tool works, test runner lists tests, required services reachable
(check, don't log in). Any failure → `00-stop.md`, tell the human what's
missing. Do not limp through.

**Risk-grade** per `risk-gates.md`. State grade (L1/L2/L3) + confidence +
cross-bucket corners in one line. One L3 corner → whole task is L3.

Also at Phase 0: if the repo lacks AGENTS.md / verify commands, note it —
flag Lane B (repo docs SOP) as a follow-up. Do not block the feature on it.

## Phase A — Spec (agent solo)

Read the wish. Produce:

- `01-spec.md` — scope, behavior spec (frontend + backend), happy path,
  unhappy paths, edge cases, broken scenarios, industry practice notes, test
  cases (FE + BE), verifiable steps. One page for the human; overflow goes to
  appendix sections (`artifact-contracts.md` for the format).
- `02-quadrant.md` — the magic quadrant: what humans know / don't know, what
  AI knows / doesn't know. AI fills its best guess for every cell; the human
  corrects cell Q3 at the gate.

While drafting, detect value-judgment landmines (money, user rights,
irreversible data, product voice). Any → L3 for the gate.

Before generation, run the **spec self-check** (`spec-self-check.md`):
score < 3 and not cheaply raisable → STOP. Cage strength = spec strength.

**Gate A:**
- **L3 → STOP and present.** Human corrects the quadrant, answers the single
  pivotal question, and signs off. No code before sign-off. The most
  expensive mistake is blocked at the cheapest point.
- **L1/L2 → continue automatically.** Log the grade + spec path in the
  running notes; the human can veto retroactively at Gate D.

**Task-shaping entry (用法 A)** — when the input is a bare one-liner and the
human wants a prompt to hand an agent (not the full pipeline yet): rewrite it
into a verification script — 造數據 → 操作 → 斷言 (results, not
no-error) → ≥2 邊界 → 失敗協議 (fix until all pass) → environment tools
per `env-tools.md`. Examples: `rewrite-examples.md`. This is the 15-minute
first win; the full pipeline subsumes it.

## Phase B — Build (agent solo)

Implement frontend + backend changes. Generate tests directly from the
spec's test-case section (traceability: every spec case maps to a test).
Protocol character (concurrency, retries/idempotency, trust boundaries) →
delegate spec tightening to `protocol-adversarial-design` (`delegation.md`).

Bound retries and steps (`failure-patterns.md`).

Write `03-build-report.md`: files changed with one-line intent, spec-case →
test mapping table, deviations from spec (**must be empty**; any deviation
sends you back to the spec via Gate A, not a workaround).

## Phase C — Verify (fresh context)

In a subagent or separate run (hard rule 3):

1. Build passes.
2. Unit/integration tests pass (cite the run summary).
3. **Gate depth by grade**: L1 = smoke only. L2 = coverage +
   mutation(sampled) + metric combo. L3 = mutation(full) + trust-boundary
   review + flag for human line-read. Rules: `spec-self-check.md`,
   `metric-combo-rules.md`, `role-pipeline.md`.
4. UI-affecting change: exercise the feature on simulator/device; screenshots;
   golden path + top unhappy paths (`env-tools.md` for capability mapping).
5. Walk the spec's verifiable steps one by one; each gets evidence.
6. Reverse-gate screens were checked at Phase 0; re-check if the task's
   character changed mid-run (`reverse-gate.md`).

Write `04-verify-report.md`. Mandatory sections: **"What AI could not
verify"** (never empty on a UI-affecting change), **category disclosure**
(defects gating cannot catch: abstract smell, cross-module emergence,
naming-intent drift), **assumptions to verify**.

**Feedback upgrade** (`feedback-upgrade.md`): failure density far above the
grade's prediction, or a delegated run reporting danger above the initial
grade → re-grade (usually up), re-run denser gates. Grade is not fixed.

## Phase D — Report (agent solo, then human)

Write `05-final-report.md` (updated quadrant — especially Q2: what AI now
knows that the human may not realize — deviations, judgment calls) and
`06-checklist.md` (human acceptance: each row verifiable by a human in under
a minute).

**Gate D: human acceptance.** Human runs the checklist, gives value
judgments, decides on commit. Report ends with an explicit
"waiting-for-human" line listing exactly what the human must do.

## Bug-fix mode

Same pipeline; Phase A becomes a **diagnosis** (evidence-first root-causing),
regression test mandatory, minimal fix. Artifact degradation for L1/L2 (3
artifacts only). Full differences: `bugfix-mode.md`. Risk grading unchanged —
a billing bug is L3 exactly like a billing feature.

## Standalone gate runs (Lane A without the pipeline)

When the ask is "can I trust this AI-generated code without line review?",
run the gate chain directly — no artifacts, no phases:

**Grade** (`risk-gates.md`) → **reverse gate** (`reverse-gate.md` — any
screen fails → STOP, fall back to human reading) → **spec gate**
(`spec-self-check.md`; L2+ use Gherkin or stated invariants) → **generate**
(bounded retries) → **verify gate** (unit → coverage → mutation per grade;
verifier ≠ generator, `role-pipeline.md`) → **metric gate**
(`metric-combo-rules.md` — combine and read, never single-metric) → **L3
human line-read of core paths** → **feedback upgrade** if evidence demands.

Required output of a standalone run: grade + confidence + corners;
reverse-gate screen results; spec self-check score (RED if < 3); gates
opened with results; combined metric reading; category disclosure (filled
in); assumptions to verify. STOP runs: failed screen(s), reason, recommended
alternative.

---

# Lane B — Repo infrastructure

Two usages, one ladder. **一次只推進一層；每一層用中建** (advance one layer at
a time; each layer earns a win in current work before the next is built).
Every layer has a **降級出口**: one-off scripts, exploration prototypes,
easily-reverted changes stop at L1 — L2+ is negative effort there. Say so
and stop; don't push.

```
L0 人肉驗證循環     human in the screenshot-log loop; 1-2 agents max
L1 任務級可驗證     every handoff carries a verification script (用法 A) — first win
L2 項目級地圖       feature-map.md + verification.md persisted; new tasks zero exploration
L3 硬約束層         said-three-times → lint / types / CI boundary scans
L4 基建自校準       eval regression + the four-question error loop
L5 放權             auto-merge / cloud agents / parallel agents — only with L2+L3 coverage and both rulers green
```

## L1 — Task-shaping

Covered in Lane A Phase A (用法 A). The rewritten script *is* the L1
deliverable; 15-minute positive return is the signal to keep going.

## L2 — Project map

One card per feature: 入口 / 驗證步驟 / 相關代碼 / 常見問題 — templates
`feature-map-template.md` + `verification-template.md`. Placement follows
the repo docs SOP classes: living agent-facing state → `.agent/` working
area (feature maps, verification specs) is acceptable, or `docs/plan/` if
the repo standardizes there; pick one home and point to it.

**地圖腐爛防禦**：每張卡必須附驗證錨——驗證步驟失敗本身就是「地圖過期」的
偵測信號。驗證不過先懷疑地圖，不先懷疑代碼。

**Positioning rule (single source)**: a feature map card records *pointers*
and *verification steps* — never re-state what code/types/git already show
(repo docs SOP iron rule). If a fact is scannable, link, don't copy.

## L3 — Hard constraints

Upgrade 口頭規矩 to mechanisms. Priority = violation frequency × consequence
severity (irreversible consequence → candidate immediately, no
three-strikes needed).

| soft (memory) | → hard (mechanism) | operation |
|---|---|---|
| 「不要跨目錄直接引用」 | lint no-restricted-imports / import boundary scan | restricted path pairs; CI runs the scan |
| 「不要在 renderer 跑重任務」 | architecture CI check | scan main/renderer dependency direction, fail on crossing |
| 「不要隨便新增全局狀態」 | type/module constraints | export allowlist, lint limits |
| 「這個函數參數不能是 X」 | type system | branded / narrow types |

Upgrade flow per rule: record original words → pick carrier (compile-time >
lint > CI > test) → **warn-first** ≥1 week collecting false positives →
adjudicate each warning (fix rule or fix code) → flip to fail (don't roll
back after — one rollback costs CI's authority) → soft-layer wording becomes
a pointer to the mechanism. Lint messages speak *to the agent*: cause +
corrected path.

Anti-patterns: rule mountain (20 at once → false-positive flood → human
disables CI → all dead; add 1-2 at a time); decorative red lines (never
reverse-tested against a known bad example); prose where a gate belongs.

## L4 — Infrastructure self-calibration

- **Eval regression**: 5 real tasks (including one trap task with a stale
  map / weak assertion). After every change to verification.md / this skill,
  re-run all: did the agent find the right module, launch, actually repro,
  fix, re-verify, report evidence?
- **犯錯四連問** (the shared error ledger — every lane's self-loop
  converges here): after any agent mistake, ask — ① 能不能寫進 Skill？②
  能不能加進 Verification？③ 能不能變成 lint/類型？④ 能不能讓 CI 永遠
  禁止？Land what has an answer; each error leaves one more guardrail.
- **Reverse-test assertions**: feed known-bad examples to the verification
  script — an assertion that can't catch a planted bug is a fake-green
  generator.
- **Vanity metric defense**: throughput (PR count) is an *outcome* of
  infrastructure, never an input to autonomy decisions.

## L5 — Autonomy release

前置清單 `autonomy-checklist.md` — all ✅ before releasing, re-run on every
domain expansion:

- L2 map covers the domain; L3 red lines cover its common violations; L4
  evals stable (3 consecutive full-green runs).
- **兩把尺** both pass: trust axis (revert rate + post-hoc bug rate) AND
  autonomy axis (question rate — human interruptions per 10 tasks). Revert
  low + question high = greenhouse autonomy; question low + revert high =
  silent guessing. Both low is real autonomy.
- Task scripts passed question audit: every decision point is one of — has a
  default (log it) / answerable from the environment / registered as a legal
  escalation point. **禁止靜默猜測** — default, assert, or ask; there is no
  fourth path.
- Questions pushed to the edges: intake (one round) → zero interruption in
  execution → delivery with a 「此處我選了X，因為…」 decision list for
  spot-checking.
- Rollback path defined: who, how, how fast (< minutes); either ruler over
  threshold → automatic demotion.

Progression: single-task self-verification → single-domain auto-merge →
multi-domain → cloud agents.

## Repo docs SOP

When the task is the doc set itself (AGENTS.md / plan / handoff / ADR /
SECURITY / CONSTITUTION): `repo-docs-sop.md`. Iron rule: docs record only
what scanning cannot find. The doc set is the upstream input that makes Lane
A's spec and verify gates possible.

---

# Shared outputs

Every invocation states: which lane + mode; for Lane A the artifacts of the
run; for Lane B the current ladder position + this layer's minimal
deliverable + next-layer trigger; the downgrade-exit declaration if the task
is "L1 is the endpoint"; the four-question ledger entries if an agent error
occurred; and for autonomous runs the 「我選了X」 decision list.

## Self-loop

If a shipped feature later turns out defective, or the human corrects a
judgment this skill should have caught: locate the leaking point (preflight /
spec / build / verify / report / grade / doc / map / constraint), fix only
that output, and run the four-question loop (L4) to land the lesson as a
guardrail. Three leaks of the same point = the format is wrong, not the
attention.

## References

- `references/risk-gates.md` — the single L1/L2/L3 matrix, six L3 triggers,
  cross-bucket rule
- `references/reverse-gate.md` — STOP screens before any gate opens
- `references/spec-self-check.md` — spec quality scoring (cage = spec)
- `references/role-pipeline.md` — verifier ≠ generator, role separation
- `references/metric-combo-rules.md` — combine-and-read + anti-gaming
- `references/feedback-upgrade.md` — reopen grade from downstream evidence
- `references/failure-patterns.md` — agent failure modes checklist
- `references/anti-patterns.md` — the merged anti-pattern list
- `references/artifact-contracts.md` — fixed formats for 00–06 artifacts
- `references/bugfix-mode.md` — bug-fix phase mapping + disciplines
- `references/delegation.md` — protocol/fuzzy delegation + preflight recipe
- `references/env-tools.md` — per-environment verification capability
- `references/rewrite-examples.md` — one-liner → verification script library
- `references/repo-docs-sop.md` — agent-facing doc set (scoping, classes,
  layering, decay defense)
- `references/hard-constraints.md` — 說過三次 → mechanism upgrade flow

## Templates

- `templates/00-stop.md` … `templates/06-checklist.md` — Lane A artifacts
- `templates/feature-map-template.md`, `templates/verification-template.md` — L2 cards
- `templates/autonomy-checklist.md` — L5 release checklist
- `templates/AGENTS.md`, `plan.md`, `handoff.md`, `SECURITY.md`,
  `CONSTITUTION.md`, `adr.md` — repo docs SOP templates

## Evals

- `evals/evals.json` — trigger + behavior regression (17 cases: task-shaping,
  infra lane, gates, anti-patterns, self-loop)