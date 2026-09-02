---
from: {session / person}
to: {session / person or "next agent"}
last-updated: {YYYY-MM-DD}
---

# Handoff: {work unit}

<!-- Cross-session continuity. WHY work stopped + what the successor's FIRST action is.
     Single source: this file points to docs/plan/* for tried/failed detail — it does
     NOT re-copy it. Two copies of "what was tried" = two truths that rot apart. -->

## State at stop
<!-- REQUIRED. Where the work actually is — the snapshot code can't give. -->

## Why it stopped
<!-- REQUIRED. Blocker, end of session, waiting on review, etc. -->

## First action for the successor
<!-- REQUIRED. The single thing to do first, so they don't re-derive the entry point. -->

## Carry-over context
<!-- fill if relevant. POINT, don't copy. -->
- Decisions already made → `docs/ADR/NNN` (don't relitigate)
- Tried-and-failed approaches → `docs/plan/{task}.md` § Tried (don't retry, don't re-list here)
- Open questions →

<!-- SELF-CHECK:
- [ ] "First action" is concrete and actionable.
- [ ] "Tried-and-failed" is NOT re-listed here — it points to docs/plan/* (single source).
- [ ] last-updated is set.
- [ ] Nothing here duplicates the plan file's content.
-->