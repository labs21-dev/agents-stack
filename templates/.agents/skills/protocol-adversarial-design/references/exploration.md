# Exploration — adversarial search inside the model

Goal: find a path to an invariant violation, or gain justified confidence
**inside model assumptions**.

Spirit (one line): same idea as TLA+/TLC — Init / Next / Inv, search for a
bad trace — adapted as a software-dev SOP. Tooling is whatever can check the
contract; no language is canonical.

## Mode A — Hand combination table (default first)

1. List variables with small domains (booleans, enums, 2–3 path shapes).
2. List actions.
3. Enumerate interesting interleavings (especially: cancel vs finish; retry vs
   ack; resolve vs policy reload).
4. For each row: does the invariant hold?

**Pass:** no violating row in the interesting set; document what you did not
enumerate.  
**Fail:** write the **trace** (state₀ —action→ state₁ …) that breaks the invariant.

Escalate when domains grow, interleavings explode past what you can table, or
the user asks for a **runnable** check → Mode B (then Mode C only if needed).

## Mode B — Executable bounded explore (any runner)

Same thin machine as Mode A, executed by **any** bounded enumerator that can:

1. Apply actions from Init
2. Check Inv on each reached state
3. Print a **counterexample trace** on violation

Runner may be a short script, a small program, or an existing test harness —
**language-agnostic**. Do not treat one language as the skill default.

**When:** user asks for runnable/code check, or Mode A cannot honestly cover
the interleavings.

**Rules:** keep domains tiny; bound depth/breadth; green ≠ prove — list
assumptions in Boundaries. Shape: `templates/bounded-explore-stub.md`.

## Mode C — Formal model checker (optional)

Encode the same thin machine in a checker (e.g. TLA+/TLC). See
`tool-tla-plus.md`.

**When:** user wants a `.tla` (or equivalent) artifact, CI-able formal check,
or Mode B is the wrong fit for the concurrency shape.

Checker output that matters: the **error trace**. Read it as a design story,
not a stack trace.

## Reading a counterexample

Ask, in order:

1. Which invariant clause died?
2. Which two movers interleaved?
3. Is the bug **dual truth / missing precedence** or a missing state variable?
4. What is the smallest design change that removes the class of traces?

Then update the hard acceptance / machine; re-explore.

## What exploration will not find

Anything not in the model: OS races you omitted, social engineering, prompt
injection, dependency CVEs, mis-mounted volumes, human runbooks. Say so in
**Boundaries**.

## Relation to adversarial QA

| | This step | Human adversarial QA |
|--|-----------|----------------------|
| Spirit | Hostile to the protocol | Hostile to the deployed system |
| Coverage | Systematic in-model | Sampled / creative out-of-model |
| Output | Trace against invariant | Exploit / failing scenario |

Use both; do not substitute.
