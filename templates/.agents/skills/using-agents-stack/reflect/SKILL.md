---
name: reflect
description: On-demand mistake/learning logger. Records errors, corrections, and insights to `.agents-stack/learnings/` for cross-session recall. Also queries past learnings on request.
trigger: On demand. User says "remember this mistake," "log this error," "show me past learnings," "recall," or similar.
inputs:
  - user's natural language description of the mistake or learning
outputs:
  - .agents-stack/learnings/<date>--<slug>.md (record), or printed recall results (query)
boundaries: Read and write `.agents-stack/learnings/` only. No code changes. No pipeline integration.
---

# Reflect Worker

Record a learning or recall past learnings — on demand, when the user says so.

## Record a Learning

When the user says something like "remember this mistake" or similar:

1. Extract the learning from context (what went wrong, why, what to do instead)
2. Write to `.agents-stack/learnings/<YYYY-MM-DD>--<slug>.md`

Format:

```yaml
---
title: Short, specific title
type: error | correction | insight
source: <workstream-id or context>
trigger: When does this apply? Be specific enough for future recall.
---

## What happened

What went wrong or what was learned.

## Root cause

Why it happened — not the symptom.

## Prevention rule

What to do instead — actionable, not abstract.

## Related

Optional: workstream IDs, phase, or file paths.
```

### Type Guide

| Type | When |
|------|------|
| `error` | A mistake was made (wrong approach, bug introduced) |
| `correction` | User corrected the agent's behavior or preference |
| `insight` | Non-obvious solution or pattern discovered |

## Recall Past Learnings

When the user says "show me past learnings," "recall," or similar:

1. Read all files from `.agents-stack/learnings/`
2. Filter by any keywords or type the user specifies
3. Print a concise summary grouped by type

If the user asks about a specific area (e.g., "what did we learn about auth"), filter by keyword match on title, trigger, and content.

## Rules

- One learning per file. If the same issue recurs, create a new entry with a later date.
- Prevention rules must be actionable ("always do X") — not vague ("be more careful").
- Do not edit or delete existing learnings. Create new ones.
- Recall reads only — never modify during recall.
