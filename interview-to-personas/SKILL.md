---
name: interview-to-personas
description: >
  Interview the user, then distill durable interaction, decision, and risk
  preferences into versioned persona files for later agent sessions. Use when
  the user asks for a persona, personalization, "remember how I like answers",
  "interview me", "update my personas", or when a session repeatedly uncovers
  the same user correction or preference. Produces `.agents/memory/personas/INDEX.md`
  and `.agents/memory/personas/{slug}.md`; never invents a persona without
  user-confirmed evidence.
metadata:
  version: "1.2.1"
  category: ["personas", "interview", "memory", "personalization"]
  tags:
    - persona
    - interview
    - personalization
    - preference
    - agent-memory
  triggers:
    - create my persona
    - personalize responses
    - interview me about preferences
    - update personas
    - remember how I like answers
---

# Interview-to-Personas

Turn a real interview into a compact, reusable persona contract. A persona is
not a demographic label; it is the user's operating protocol: how they want the
agent to communicate, decide, challenge them, prioritize tradeoffs, and avoid
known failure modes.

This skill owns the interview and the clause format. Load, CRUD, caps, and the
shared write-back gate live in `agent-memory`. Agent-memory runs without this
skill; this skill is only required to run a persona interview.

## Core rules

- INDEX-first: read `INDEX.md`, open only relevant persona files.
- Evidence-first: every hard clause comes from the user's words or explicit
  confirmation. Mark anything inferred as `derived` and never treat it as hard.
- Question bank: templates retain reusable questions and field names only.
  A specific user's answers belong only in that user's persona file; never
  promote an individual case into the default questionnaire or sample clauses.
- One layer at a time: do not dump twenty questions. Interview in short batches.
- Upgrade gate: one correction is a note; repeated correction, explicit
  instruction, or high-severity risk can become a persona clause.
- User confirms writes: show the proposed clauses and ask before saving.
  If the user already explicitly requested the save, do not re-ask.
- No therapy: do not write medical, diagnostic, identity, or sensitive claims.
  Prefer behavior language over diagnostic language.
- No worship: persona clauses must not instruct any agent to be agreeable or
  deferential. The user may explicitly require disagreement and assumption
  hunting.
- Real-world facts stay current-session facts unless separately stored in the
  proper memory drawer.

## Flow

1. Read `INDEX.md` and the relevant persona file, if one exists.
2. Orient the interview in one short reply: state the current persona, missing
   layers, and the next question batch.
3. Interview by layer. Recommended order:
   1. Interaction protocol: language, structure, directness, fact boundary.
   2. Judgment system: product priority, known failure modes, consensus rule.
   3. Risk and relevance: operating constraints, cross-domain analogies,
      prohibited agent styles.
   4. Persona split: decide whether one persona or role-specific personas are
      clearer.
4. Draft clauses as `Must / Should / Avoid`, each with evidence and scope.
5. Apply the write gate:
   - user-confirmed or explicit request;
   - durable across sessions;
   - useful to future work;
   - not secret, sensitive, diagnostic, or a transcript;
   - no silent conflict with an existing persona clause.
6. Resolve conflicts explicitly: replace, narrow, split, or deprecate.
7. Update `INDEX.md` first, then the persona file.
8. Show the saved path and the three most important clauses.

## Interview questions

Ask only what is missing. Use `templates/interview.md` as a starting batch.
Good probes:

- How should answers be structured in this kind of task?
- What makes a reply feel wasted? What makes it feel worth the round?
- When should the agent challenge you, and how directly?
- Which real-world facts must the agent never assume?
- Which priority wins when speed, elegance, sellability, and feasibility collide?
- Which mistakes recur often enough to deserve a standing rule?
- How many objections should be surfaced at once?
- Which agent voices are explicitly banned?

Do not ask for examples the user considers private. If they volunteer a
sensitive example, store the transferable rule, not the story.

## Write format

Each persona file must stay compact:

```markdown
# {Persona title}

- slug: {slug}
- version: X.Y.Z
- last_updated: YYYY-MM-DD
- status: active | deprecated
- scope: all sessions | engineering | product | research | ...
- source: user-interview

## Must

- {Clause.} Evidence: {short source or "user-confirmed interview"}.

## Should

- {Clause.} Evidence: {short source}.

## Avoid

- {Clause.} Evidence: {short source}.

## Upgrade signals

- {Repeated correction, contradiction, or high-severity signal and the next
  action.}
```

Keep one clause per bullet. Prefer behavior, preference, and decision language.
If the file exceeds 80 lines, split the persona by scope or remove stale
clauses instead of compressing meaning into vague language.

## Update policy

| Change | Action |
|---|---|
| Clarification | Revise in place; bump patch version. |
| New clause in current scope | Add evidence and bump minor version. |
| Contradiction | Resolve first; do not append both sides. |
| Scope change | Narrow, split, or create a separate persona. |
| Deprecated persona | Set `status: deprecated`; keep the index row. |

## Verification

Before claiming completion, check:

- `INDEX.md` has one row per persona file and no row without a file.
- Every saved clause has evidence or is marked `derived`.
- No `derived` clause is phrased as a hard rule.
- Every conflict has a resolution note.
- The persona is actionable by a future agent, not just descriptive.
- The final reply explicitly reports the persona update, its slug, and what
  changed.

## References

- `templates/interview.md` — compact interview batch and field guide.
- `.agents/memory/personas/INDEX.md` — project persona catalog.
- `agent-plugin/agent-memory/SKILL.md` — memory load, CRUD, and write-back gate.
