---
name: release
description: Write changelog, update reference docs, archive completed workstream.
trigger: When qa-report.md exists with PASS verdict.
inputs:
  - spec.md
  - plan.md
  - tasks.md
  - handoff.md
  - qa-report.md
outputs:
  - .agents-stack/workstream/<ws-id>_{YYYYMMDD}/changelog.md
  - .agents-stack/workstream/<ws-id>_{YYYYMMDD}/status.json
  - updated reference docs if needed
boundaries: Read-only except changelog.md, status.json, and reference/. Archive is move not copy.
---

# Release Worker

Close out a completed workstream. Read all artifacts, write the changelog, update project knowledge if needed, archive the workstream.

## Input

Read all workstream artifacts from `.agents-stack/<id>/`:
- `spec.md` — original requirements
- `plan.md` — planned architecture
- `tasks.md` — task breakdown
- `handoff.md` — implementation evidence
- `qa-report.md` — QA verdict (must be PASS)

## Output: changelog.md

```markdown
# Changelog

## Workstream
- ID: [WORKSTREAM-ID]
- Title: [title]

## Summary
[2-3 sentences: what was accomplished]

## Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `src/file1.ts` | add | [brief description] |
| `src/file2.ts` | modify | [brief description] |

## Deviations from PLAN

| Planned | Actual | Rationale |
|---------|--------|-----------|
| [original approach in plan.md] | [what was actually done] | [why it changed] |

## Deployment Checklist

- [ ] Environment variables: [list additions/changes]
- [ ] Database migrations: [list migration files]
- [ ] Configuration changes: [list config changes]

## Reference Update Suggestions

- [ ] Update architecture.md: [what changed structurally]
- [ ] Update design.md: [what changed in design]
- [ ] No reference update needed
```

## Reference Update

After writing changelog, assess whether this workstream produced lasting project knowledge:

- Did the architecture change? → Update `.agents-stack/reference/architecture.md`
- Did the design language change? → Update `.agents-stack/reference/design.md`
- Nothing structurally new → Leave reference/ unchanged

**Rule**: reference/ is read-optimized. Only update for decisions that affect future workstreams. Not every workstream needs a reference update.

## Archive

1. Move `.agents-stack/<id>/` to `.agents-stack/archive/<id>/`
2. Update `.agents-stack/tracked-work.json`:
   - Clear `active` field
   - If relevant, move to `parked` or leave null
   - Set `evidence_path` to archive location
3. Update `status.json` before archiving: `phase: "archived"`

## Workflow

1. Read all workstream artifacts
2. Compare plan vs actual, note deviations
3. Write `changelog.md`
4. Assess if reference/ needs update, update if yes
5. Archive workstream directory
6. Update `tracked-work.json`

## Done

`changelog.md` written. Reference updated (if needed). Workstream archived in `.agents-stack/archive/`. Ready for next workstream.

**→ End of pipeline. Ready for next workstream.**
