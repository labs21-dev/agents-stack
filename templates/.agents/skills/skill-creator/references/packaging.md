# Packaging

Package a finished skill for distribution. Runtime-agnostic — produces a portable artifact regardless of where the skill will be mounted.

## Package format

A skill package is a single archive (`.skill` — a zip with a convention) containing the skill directory verbatim:

```
<skill-name>.skill  (zip)
  <skill-name>/
    SKILL.md
    references/
      *.md
    templates/
      *
    evals/                 ← optional; strip if distributing to end-users who don't run evals
      evals.json
      files/
```

## What to include

- `SKILL.md` (required) — with final frontmatter.
- `references/` and `templates/` — everything the body points to.
- `evals/` — optional. Keep it if the recipient will run L1 evals; strip it for end-user distribution to reduce size and avoid leaking test prompts.

## What to strip

- `.DS_Store`, `__pycache__`, editor cruft, absolute paths.
- Any `evals/runs/` output artifacts from your own eval cycles.
- Any adapter scripts you wrote locally — adapters are environment-specific and not part of the skill.

## Distribution checklist

- [ ] `name` in frontmatter matches the directory name.
- [ ] `description` is the tuned version (best held-out test score).
- [ ] Every reference the body links to exists in `references/`.
- [ ] Every template the body mentions exists in `templates/`.
- [ ] No runtime-specific paths or commands baked into the body.
- [ ] No local adapter code included.

## After packaging

The recipient mounts the skill via *their* runtime's discovery mechanism (Claude Code commands, Cursor rules, Codex AGENTS.md, ARC `<SKILLS>` injection, etc.). The package doesn't prescribe how — that's the runtime's job, consistent with the adapter seam.