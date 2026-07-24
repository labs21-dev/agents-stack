# Metric combo rules — combine and read

A single metric is gameable. An AI that knows complexity is watched splits one
coherent function into ten trivial ones. Defense: combination + mutation
cross-check.

## Required metrics (L2/L3)

- Cyclomatic complexity (per function / per module)
- Module size / file length
- Function length distribution
- Dependency structure (fan-out, cycles)
- Coverage (line + branch)
- Mutation score (the cross-check)

## Rules

1. No single metric passes the gate alone.
2. Mutation score cross-checks low complexity. Complexity dropped but mutation
   dropped too → cosmetic split, not real simplification. Flag.
3. Coverage without mutation is not trust. 100% line coverage with no assertions
   is an AI artifact; mutation testing catches tests-that-don't-test.
4. Dependency cycles: flag, not just count. Zero cycles with one giant hub is
   a different problem than a few small cycles.
5. Module size reads with cohesion. Ten 20-line fragments of one thing =
   split-to-game.

## Output

Combined reading, e.g.:

> Complexity low, but mutation score dropped 15pt after refactor — cosmetic
> split. Gate: FAIL.

Not: "complexity 4 ✓ coverage 100% ✓ gate PASS."

## Tie-breaker

When structural metrics say "clean" but mutation score is low → the code looks
clean because the tests don't exercise it. Trust mutation.