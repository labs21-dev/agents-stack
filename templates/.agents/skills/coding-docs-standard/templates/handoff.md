---
from: {session / person}
to: {session / person or "next agent"}
last-updated: {YYYY-MM-DD}
---

# Handoff: {work unit}

<!-- Cross-session continuity. WHY work stopped + what the successor's FIRST action is. -->

## State at stop
<!-- Where the work actually is — the snapshot code can't give. -->

## Why it stopped
<!-- Blocker, end of session, waiting on review, etc. -->

## First action for the successor
<!-- The single thing to do first, so they don't re-derive the entry point. -->

## Carry-over context
- Decisions already made (don't relitigate — see `docs/ADR/NNN` if recorded)
- Tried-and-failed approaches (don't retry)
- Open questions

<!-- SELF-CHECK:
- [ ] "First action" is concrete and actionable.
- [ ] "Tried-and-failed" is present — the highest-value unscannable field.
- [ ] last-updated is set.
-->