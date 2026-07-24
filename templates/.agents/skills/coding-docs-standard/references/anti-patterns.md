# Anti-patterns

Concrete smells to sweep the drafted set for. Most failures reduce to these.

## Duplicating a scannable fact

- ❌ `AGENTS.md`: "This project uses TypeScript and React with Vite."
  → `package.json` already says all of that.
- ❌ A doc describing "what `foo.ts` does." → read the code.
- ❌ "Getting started: `npm install` then `npm run dev`." → the manifest's
  scripts are the source; point, don't restate (exception: the *verify* intent
  for the agent — see below).

## Two files, one rule

- ❌ A convention in both `AGENTS.md` and `CONSTITUTION.md`. → pick one home,
  pointer from the other.
- ❌ A security rule in `SECURITY.md` copied into `AGENTS.md` "for convenience."
  → rots independently. Pointer only.

## Inlining L2 into L0

- ❌ `AGENTS.md` carrying the full trust-boundary list. → bloats L0, single-point
  decay. `AGENTS.md` only says *when* to load `SECURITY.md`.

## Living list mixing done and in-progress

- ❌ A `plan/` directory with finished tasks still in the live index. → the
  agent can't tell what's actually open. Archive to `docs/archive/plan/` on
  completion.

## Archiving an ADR

- ❌ Moving a superseded ADR into `docs/archive/`. → ADRs supersede **in place**
  with `status: superseded-by-NNN`; they are never archived. Archiving hides the
  very record an agent needs to avoid re-opening a dead decision.

## No verify command

- ❌ `AGENTS.md` with rules and pointers but no "run these to self-prove."
  → silent success. The one scannable fact that must still be written, because
  the *intent* ("self-prove completion") isn't in the manifest.

## ADR without rejected alternatives

- ❌ An ADR that records the decision but not what was rejected and why.
  → loses the field with the highest anti-relitigation value. Reject any ADR
  missing it.

## Prose where a gate belongs

- ❌ "Don't import `X` from `Y`" written as a doc sentence. → make it a lint
  rule; the doc only holds the *why* the lint can't express.

## Doc for a one-off

- ❌ A `plan/` file for a finished, shipped, never-revisited change. → don't
  author; or if it changed a decision, it's an ADR, not a living plan.