---
name: feature-dev-e2e
description: End-to-end agentic feature development AND bug-fix workflow. Use when the user gives a feature goal or wish item (e.g. "make calorie detection automatic", "add X to the app", "I want Y behavior") OR reports a bug to be fixed (e.g. "the banner can't be cleared", "this crashes when...", "this shows the wrong language") and expects AI to handle analysis → scope/diagnosis → behavior spec (frontend+backend) → happy/unhappy/edge paths → industry practice → test cases → verifiable steps → code → self-run verification → final report. Also use when the user says "do the feature workflow", "run the e2e flow", "fix this via the workflow", or after a vague feature wish / bug report that would previously trigger ad-hoc exploration. Produces fixed-format artifact documents at every phase. NOT for pure research questions or doc-only tasks; bug TRIAGE without a fix goal is out of scope, bug FIX is in scope.
---

# Feature Dev E2E

Turn a one-line feature wish into verified, reported code with at most two
human touch points. The human provides the wish and (at risk gates) value
judgments; the agent does the cognitive labor and proves its own work with
environment evidence, never self-declaration.

Core law: **the spec is the ceiling of the whole chain.** A wrong spec
executed perfectly is still wrong, and errors correlate downstream — a later
phase cannot detect an earlier phase's misunderstanding. That is why gates sit
where they sit.

## Hard rules (never violated, any repo)

1. **Artifact per phase.** Each phase writes a fixed-format file to
   `.agent/features/<slug>/` before the next phase starts. Later phases read
   the files, not conversation memory. Conversation memory is not durable
   state.
2. **Evidence, not declarations.** Verify-report items cite raw evidence:
   test-run summaries, build logs, screenshots, console output paths. A bare
   "passed" without evidence is a failed check.
3. **Verifier ≠ generator.** Verification runs in a fresh subagent context
   (or a separate non-interactive command), never the same context that wrote
   the code self-certifying.
4. **Human triggers commits/deploys.** The agent never commits, pushes, or
   deploys unless the human explicitly asked in this session. Repo branch
   rules (if a CLAUDE.md/AGENTS.md declares them) override defaults.
5. **STOP beats guess.** Any gate failure, environment preflight failure, or
   unresolvable ambiguity → stop with a written STOP note. Silent guessing is
   banned.

## Flow

### Is it a bug fix?

If the input is a bug report ("X is broken", "Y shows wrong", "Z crashes")
rather than a new capability, run **bug-fix mode** — same pipeline, Phase A
becomes a diagnosis with evidence-first root-causing, and a regression test
is mandatory. See `references/bugfix-mode.md` for the mode's differences
(artifact degradation for L1/L2, repro rules, minimal-fix rule). Everything
else in this file applies unchanged, including risk gates.

### Phase 0 — Preflight (always)

Run the environment check before any work:
- Build tool works (`xcodebuild -list` / `npm test` dry call / equivalent for
  the repo).
- Test runner lists tests without error.
- Required services reachable (check, don't log in).

Any failure → STOP note in `.agent/features/<slug>/00-stop.md`, tell the human
what's missing. Do not limp through.

Risk-grade the feature per `references/risk-gates.md`. State the grade
(L1/L2/L3) and confidence in one line. One L3 corner → whole task is L3.

### Phase A — Spec (agent solo)

Read the wish. Produce two artifacts:

- `templates/01-spec.md` → `.agent/features/<slug>/01-spec.md` — scope,
  behavior spec (frontend + backend), happy path, unhappy paths, edge cases,
  broken scenarios, industry practice notes, test cases (FE + BE), verifiable
  steps. One page for the human; failure-mode detail goes in an appendix
  section.
- `templates/02-quadrant.md` → `02-quadrant.md` — the magic quadrant draft:
  what humans know / don't know, what AI knows / doesn't know. AI fills its
  best guess for every cell; the human corrects cell Q3 (known-to-human,
  unknown-to-AI) at the gate.

While drafting, detect value-judgment landmines (money, user rights,
irreversible data, product-voice decisions). If any exist → the feature is L3
for the gate.

**Gate A:**
- **L3 → STOP and present.** Human corrects the quadrant, answers the single
  pivotal question, and signs off. No code before sign-off. The most expensive
  mistake is blocked at the cheapest point.
- **L1/L2 → continue automatically.** Log the grade + spec path in the
  running notes; the human can veto retroactively at Gate D.

### Phase B — Build (agent solo)

Implement frontend + backend changes. Generate tests directly from the spec's
test-case section (traceability: every spec case maps to a test). For
high-risk protocol character (concurrency, idempotency, retries, trust
boundaries), delegate the spec tightening to the repo's adversarial-design
skill if present (see `references/delegation.md`).

Write `templates/03-build-report.md` → `03-build-report.md`: files changed
with one-line intent each, spec-case → test mapping table, deviations from
spec (must be empty; any deviation sends you back to the spec, not a
workaround).

### Phase C — Verify (agent self-runs, fresh context)

In a subagent or separate run (rule 3):

1. Build passes.
2. Unit/integration tests pass (cite the run summary).
3. If the repo has UI and the change is UI-affecting: exercise the feature on
   simulator/device; capture screenshots; check the golden path and the top
   unhappy paths from the spec.
4. Walk the spec's verifiable steps one by one; each gets evidence.

Write `templates/04-verify-report.md` → `04-verify-report.md`. Include the
mandatory section **"What AI could not verify"** — things needing real
hardware, real users, production data, or human taste. This section is never
allowed to be empty on a UI-affecting change; if it is, the verification was
too narrow.

### Phase D — Report (agent solo, then human)

Write `templates/05-final-report.md` → `05-final-report.md` (updated quadrant
— especially cell Q2: what AI now knows that the human may not realize —
deviations, judgment calls made) and `templates/06-checklist.md` →
`06-checklist.md` (human acceptance: goal → check → done table, each row
verifiable by a human in under a minute).

**Gate D: human acceptance.** Human runs the checklist, gives value
judgments, decides on commit. Report ends with an explicit
"waiting-for-human" line listing exactly what the human must do.

## Grading summary

| Grade | Gate A | Verify depth | Typical |
|---|---|---|---|
| L1 | auto | build + smoke + human skim | copy tweaks, flags, prototypes |
| L2 | auto | full tests + UI walk + evidence | routine features |
| L3 | **STOP, human sign-off** | L2 + adversarial spec + line-read flag | money, quota, data loss, privacy, product voice, deploys |

Grade rules live in `references/risk-gates.md`. Bug-fix mode differences in
`references/bugfix-mode.md`. Delegation rules in
`references/delegation.md`. Artifact contracts in
`references/artifact-contracts.md`.

## Anti-patterns (this workflow fails when…)

- The human skips Gate D review because the report "looks professional."
  Mitigation: the "What AI could not verify" section is mandatory and visible.
- Spec grows past one page → human stops reading → Gate A rubber-stamps even
  when required. If L3 spec exceeds a page, the spec is the defect — rewrite
  it, do not demand more human attention.
- Artifacts skipped "because this run is small." Even a one-file fix writes a
  minimal spec + checklist; the format is the contract.
- AI edits the spec to match what the code ended up doing. Deviations go
  back to Gate A, not into a silent rewrite. (If the human ordered the change,
  the spec is amended and re-logged — never silently.)

## Self-loop

If a shipped feature later turns out defective, or the human corrects a
judgment the workflow should have caught: locate the leaking gate (preflight /
spec / build / verify / report), fix only that gate, and record the correction
in `.agent/features/<slug>/corrections.md`. Three leaks of the same gate =
the gate's format is wrong, not the AI's attention.