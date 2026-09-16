# Agent Workspace Index

Use this file as the first-stop index. Open only the section and linked file
needed by the current task; do not load every skill into context.

## Decide

- [Meta Thinking Framework](meta-thinking-framework/SKILL.md) — six-lens analysis for complex decisions.
- [Interview to Build](interview-to-build/SKILL.md) — product discovery before implementation.

## Specify

- [System Prompt SOP](system-prompt-sop/SKILL.md) — route prompt constraints to enforcement layers.
- [Design Context](design-context/SKILL.md) — define visual and UX context before generation.
- [Plain Sales Copy](plain-sales-copy/SKILL.md) — concise business copy with no puff.
- [Marketing Director](marketing-director/SKILL.md) — brief-first marketing and multimedia planning.

## Build

- [Agentic Dev E2E](agentic-dev-e2e/SKILL.md) — feature or bugfix from spec to evidence.

## Meta Skills

- [Skill Creator](skill-creator/SKILL.md) — create, evaluate, and package skills.
- [Skill Evolution](skill-evolution/SKILL.md) — evolve skills from real usage.
- [Conversation to Skills](conversation-to-skills/SKILL.md) — turn corrections into versioned skills.
- [Interview to Personas](interview-to-personas/SKILL.md) — interview users and maintain persona memory.

## Learning

- [Learn Anything About X](learn-anything-about-x/SKILL.md) — adaptive domain mentorship.

## Agent Runtime

- [OpenRouter Adapter](agent-plugin/scripts/openrouter.py) — shared provider adapter for media and text skills.
- [Runtime Doctor](agent-plugin/scripts/doctor.py) — prerequisite check.
- [Generate Image](agent-plugin/generate-image/SKILL.md)
- [Generate Video](agent-plugin/generate-video/SKILL.md)
- [Generate Text](agent-plugin/generate-text/SKILL.md)
- [Generate Audio](agent-plugin/generate-audio/SKILL.md)
- [Read Image](agent-plugin/read-image/SKILL.md)
- [Read Video](agent-plugin/read-video/SKILL.md)
- [Read Audio](agent-plugin/read-audio/SKILL.md)
- [Agent Memory](agent-plugin/agent-memory/SKILL.md) — five-duty memory protocol.

## Memory Drawers

- [Working](agent-plugin/templates/memory/working/INDEX.md) — current task desk.
- [Semantic](agent-plugin/templates/memory/semantic/INDEX.md) — stable facts.
- [Episodic](agent-plugin/templates/memory/episodic/INDEX.md) — experience with lessons.
- [Procedural](agent-plugin/templates/memory/procedural/INDEX.md) — verified methods and skill pointers.
- [Personas](agent-plugin/templates/memory/personas/INDEX.md) — user collaboration protocol.

## Project Operations

- [README](README.md) — repository overview, installation, and runtime commands.
- Tests live under `agent-plugin/tests`; run them with:

```bash
pytest agent-plugin/tests
```

Generated runtime state belongs under `.agents/`. Do not treat memory entries,
generated artifacts, or credentials as project source.
