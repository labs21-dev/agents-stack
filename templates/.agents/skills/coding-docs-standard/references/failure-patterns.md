# Failure patterns — how agent docs fail

These are the recurring ways an agent-facing doc set goes wrong. Each has a
defense this skill builds in.

## 1. Entropy (stale ground truth)

A doc states a fact; the fact changes in code; the doc stays. The agent reads
the doc and is *confidently wrong*. Worse than no doc, because the agent trusts it.

**Defense:** scan-first (never write a scannable fact), single-source, timestamps
on living docs, prefer automation over prose. See `decay-defense.md`.

## 2. Overload (context dilution)

Too many docs, or one huge doc. The agent can't hold it all, starts skipping
or skimming → equivalent to no docs, but with token cost.

**Defense:** layered loading (L0/L1/L2), `AGENTS.md` stays pointer-only, L2
triggered not habitual. See `loading.md`.

## 3. Silent success

Docs are thorough but there's no verify command. The agent changes code,
declares "done," and nothing catches a broken build/missing behavior. The #1
killer for agentic coding.

**Defense:** `AGENTS.md` must list the build/test/run commands the agent runs to
self-prove. This is non-negotiable and the one place a scannable fact (from a
manifest) is still written explicitly — because the agent needs the *intent*
("run these to self-prove"), not just the command's existence.

## 4. Multi-source conflict

The same rule in two docs. One gets updated, the other rots. The agent draws
the rotted copy.

**Defense:** single-source grep before saving. See `decay-defense.md`.

## 5. Reopened dead debate

No ADR, or an ADR missing the rejected-alternatives field. An agent re-litigates
a decision the team already settled and may "improve" it back to a rejected path.

**Defense:** ADRs append-only, mandatory rejected-alternatives field. See
`doc-classes.md`.

## 6. Under-coverage (missing gap)

A real gap the agent hits has no doc. The agent guesses — sometimes catastrophically
(security/trust boundaries).

**Defense:** scoping step lists the scannable inventory and maps surviving gaps
to classes; security/architecture work triggers L2 docs. See `scoping.md`.