# {Repo name}

<!--
  AGENTS.md is L0 — always in context. Pointer-only; never inline L2 content.
  Before saving, clear the self-check at the bottom. Delete the comments once final.
-->

## How we work here

<!-- Conventions / don'ts that NO lint/type/test enforces. If a lint enforces it, drop it. -->

-

## Where things are

<!-- Pointer index. Point to docs and main modules. Do NOT summarize their content. -->

- Architecture / module map: → (where, or "see code structure")
- Active plans: → `docs/plan/`  (completed → `docs/archive/plan/`, not ground truth)
- Handoffs: → `docs/handoff/`  (superseded → `docs/archive/handoff/`)
- Security: → `docs/SECURITY.md` (load before touching `auth/` or trust boundaries)
- Constitution: → `docs/CONSTITUTION.md` (load before architecture decisions)
- Decisions: → `docs/ADR/`  (superseded ADRs stay in place with `superseded-by-NNN`; never archived)

## How to verify

<!-- NON-NEGOTIABLE. The commands an agent runs to self-prove completion.
     Name them explicitly even if scannable — the agent needs the *intent*. -->

- Build:
- Test:
- Run:
- Lint / typecheck:

<!-- SELF-CHECK (delete each line after confirming):
- [ ] Every line above is NOT derivable from package.json / types / CI. (Verify command
      is the one allowed exception — it carries the "self-prove" intent.)
- [ ] No rule here is duplicated in another doc (grep the repo).
- [ ] No L2 content inlined — only pointers to SECURITY/CONSTITUTION.
- [ ] Verify commands present and runnable.
-->