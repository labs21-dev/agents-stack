# Evolution Log — <skill name>

Passive case log for skill evolution. Copy this file into a skill's `references/` to give it evolution capability (see `skill-evolution/templates/evolution-attach.md`).

## Record format

One entry per observable-outcome use:

```
## [YYYY-MM-DD] <short label>
- context: <what task/situation triggered the skill>
- part used: <which rule / lens / trigger / section>
- outcome: effective | ineffective | adverse
- post-hoc verification: pending | verified-effective | verified-ineffective | none
- notes: <what specifically worked or failed>
```

## Rules
- Record **retrospectively**, after the outcome is observable — never mid-work (navel-gazing).
- `outcome` is not the agent's self-assessment; `post-hoc verification` must come from an external outcome (the work shipped and was judged).
- Tally per `part used` to spot threshold crossing (see skill-evolution `evolution-protocol.md`).

## Flagged candidates

When a part crosses threshold (≥3 effective + ≥1 verified-effective → upgrade; ≥3 adverse → deprecate), record the flag here:

```
### [YYYY-MM-DD] FLAG: <upgrade|deprecate> — <part>
- tally: <N effective + M verified | M adverse>
- evidence: <pointers to entries above>
- patch drafted: <link/none yet>
- status: flagged | drafted | approved | merged | rejected | rolled-back
```

## Cases

<!-- append entries below -->