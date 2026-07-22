# Patch Draft Format

An AI-drafted evolution patch must follow this format exactly. The format exists so a human can review quickly and so the patch is reversible.

```markdown
# Patch: <upgrade | deprecate | revise> — <skill name>

## Candidate
- part: <which rule / lens / trigger / section>
- candidate type: <upgrade | deprecate>
- cases: <N effective + M verified | M adverse>  (tally)
- risk: <low | medium | high>
- reversibility: <reversible | semi-reversible | irreversible>

## Scope
<Exact file(s) and section(s) affected. Nothing outside scope.>

## Evidence
<The cases that justify this, with their post-hoc verification status. Quote the relevant evolution-log entries.>

## Diff
```diff
<file path>
- <before>
+ <after>
```

## Rationale
<One paragraph: why this change, why now, what failure mode it addresses.>

## Before-snapshot instruction
<What to snapshot before applying, and where to store it, so the change can roll back.>
```

## Rules

- **Scope is binding.** A patch that touches outside its declared scope is rejected at review.
- **Evidence must cite real evolution-log entries.** A patch with no cited cases is not a patch — it's an opinion.
- **Risk tag drives the gate.** Low → batch fast review; medium → per-item; high → per-item strict + two-person.
- **Reversibility must be stated honestly.** "Irreversible" is rare but allowed; it demands the strictest gate.
- **The AI does not apply the patch.** It produces this document. The human approves and applies (or asks the AI to apply after approval).

## Anti-patterns

- A "patch" that says "improve the description" with no diff — rejected. No diff, no patch.
- A patch that cites cases the agent self-rated as effective with no post-hoc verification — rejected. That's the reflexivity failure.
- A patch whose scope quietly includes unrelated edits — rejected. Scope is binding.