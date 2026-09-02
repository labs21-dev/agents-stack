# Hard constraints: upgrade "said it three times" into a mechanism

Canonical detail for the L3 layer. The SKILL.md carries the summary; this
file carries the upgrade flow, the lint-message pattern, and the static-first
note.

## Criteria

A rule is worth hardening based on two variables, not on how "advanced" it
sounds:

```
upgrade priority = violation frequency × consequence severity
```

- Said 3 times → candidate.
- Consequence irreversible (data, money, safety) → candidate immediately, no
  three-strikes needed.
- Happened once, consequence reversible → stays soft (AGENTS.md / prompt).

## Upgrade flow (per rule)

1. **Record the original words** — how it was said to the agent (the phrasing
   later goes into the lint message).
2. **Pick the carrier**: lint if lintable, types if typeable, CI scan if
   scannable. Order: compile-time > lint > CI > test.
3. **Warn-first**: new rule runs in warn mode ≥ 1 week, collecting false
   positives.
4. **Adjudicate each warning**: real violation or wrong rule. Fix the rule or
   fix the code.
5. **Flip to fail** once the false-positive rate is acceptable. **Do not roll
   back casually after this** — one rollback costs CI's authority for the
   whole constraint layer.
6. **Sync the soft layer**: the original prompt wording becomes a pointer to
   the mechanism ("CI blocks this"), not a repeated statement.

## The error message is context

The message an agent hits when crossing a red line is the best on-site
teaching. Write lint messages *to the agent*:

```
✗ features/a/cart.ts:3  imports features/b/internal/session
  Why: cross-feature internal modules are import-forbidden (7th violation of this class)
  Fix: use the exported interface at features/b/public.ts
```

## Static languages earn a free layer

Errors a compiler can catch should not be left to runtime tests. Preferring
statically strongly-typed languages when choosing a stack is a free hard-
constraint layer.

## Anti-patterns

- **Rule mountain**: 20 constraints at once → false-positive flood → human
  disables CI → all constraints dead. 1-2 at a time.
- **Decorative red lines**: rules added but never fired — no known-bad-example
  reverse test was run. Every red line must be proven able to go red.
- **Constraints as prose**: 50 "musts" in AGENTS.md = soft-layer overload.
  Soft keeps only what mechanisms cannot express yet (style, intent, context
  conventions).