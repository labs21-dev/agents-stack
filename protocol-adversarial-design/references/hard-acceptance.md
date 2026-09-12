# Hard acceptance — invariants

Hard acceptance is the **source contract**. Model checking and tests serve it.

## Form

Prefer one of:

- `If <decision/state>, then <must hold>.`
- `It is impossible that <A> and <B> simultaneously.`
- `After <event>, eventually <state>` (liveness — use sparingly; harder to check)

Write 1–3 sentences max for the first shot.

## Rules

1. **No weasel words:** should, try, usually, as much as possible, reasonably.
2. **No derived names in the source sentence.** If workspace is the truth, do not
   say "path jail must…". Say what must be true of path/decision/workspace; treat
   jails as implementations that must be entailed by that truth.
3. **Name observables** the system can decide: roles, flags, ids, paths, epochs,
   statuses — not vibes.
4. **One truth.** If two rules can disagree, the invariant must state the
   precedence or the collapse into one predicate.

## Promotion ladder

```
fuzzy acceptance  →  hard sentence  →  (optional) executable / formal check of that sentence
```

Only promote when screens pass. Many protocols stop at the hard sentence + table.

## Smell test

Ask: *Would a hostile colleague accept this as pass/fail in a design review
without debating taste?* If no, rewrite.

## Examples (domain-agnostic shape)

| Weak | Hard |
|------|------|
| Uploads should be safe | `status=committed ⇒ object exists ∧ checksum matches`
| Don't double charge | `∀ paymentId: charge events ≤ 1`
| Cancel should work | `userRejected=true ⇒ no later toolResult append for that callId`
| Stay in workspace | `decision=allow ⇒ resolvedPath ∈ workspace`

## Next

Encode variables/actions so the invariant is checkable —
`thin-state-machine.md`.
