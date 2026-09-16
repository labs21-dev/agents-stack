# Episodic memory

Duty: a concrete experience with context. Answers "what happened before."
When to use: starting a similar task, a past failure may recur, or you need how the last attempt succeeded or failed.
Purpose: so the agent can consult experience, not nostalgia, and not a chat archive treated as memory.
Store: context, action, result, lesson. Lesson is required.
Do not store: full chats, conclusions that can be distilled into stable facts (that is semantic), procedure bodies ready to graduate (that is procedural), secrets.
When to update: do not rewrite history. A new event is a new file. Delete only when the entry is noise, wrong, or sensitive.
Every entry must also have `last_updated`; `when` records the event time, not the file revision time.

CRUD lives only in [`../../skills/agent-memory/SKILL.md`](../../skills/agent-memory/SKILL.md). Drawer rule: append-only. Distill a fact into semantic as a separate write, and it must pass the gate, so a one-off does not become a long-term rule.

## Catalog

| slug | one-liner | when | last_updated | file |
|------|-----------|------|--------------|------|

0 entries.
