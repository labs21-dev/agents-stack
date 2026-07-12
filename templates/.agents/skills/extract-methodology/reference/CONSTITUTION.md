# CCA Constitution — for the Human

> Read once, internalize, carry into every collaboration. The AI does not load this; it has its own symmetric half in `AI-MODULE.md`.

## Founding Axiom

The ceiling of your collaboration with AI is set by **context clarity**, not by model capability. Most "correct but mediocre" output is a context problem wearing a capability mask.

When output isn't sharp enough, suspect your context before you suspect the model. You are the complexity immune system for context: the AI's default is to add structure and answer generally; you cut, sharpen, and force focus.

## The Eight Basic Laws

Shared with the AI. Carried during all work.

1. **Context is the bottleneck, not capability.** When output is fair, suspect context before the model.
2. **Shape beats volume.** The arrangement of what you feed matters more than how much. Order, framing, and omission are levers; more words are not.
3. **Unknowns are the unit of work.** Every collaboration converts unknowns to knowns. Four kinds — known-knowns (deliver), known-unknowns (clarify), unknown-knowns (externalize via prototype), unknown-unknowns (scan). Technique must match the kind. Unknowns must be surfaced as a visible artifact, not kept in your head.
4. **The map is not the territory.** Your prompt is the map; the real problem is the territory. The gap is never zero. Assume you are under-specified.
5. **Specificity matches the phase.** Loose in discovery, tight in execution. Too-tight-too-early: the AI holds a line when it should turn. Too-loose-too-late: it retreats to "industry best practice" and drifts from your intent. This is the double-edge of instruction.
6. **Context is co-authored.** You sharpen questions; the AI externalizes what it lacks. Clarity is not one party's job.
7. **The human gates the irreversible.** Your non-delegable duties are exactly two: authorize irreversible actions, and apply the weighting function (what matters more). Everything else is delegable.
8. **Replace, don't stack.** When new understanding overturns old, mark it `[discarded] ... [new] ...` and replace. Never stack wrappers around superseded logic. This is the self-cleaning discipline that keeps the other seven from rotting into structure debt.

## Your Eight 手法 (techniques)

Extracted from real collaboration and generalized. Roughly ordered from "starting a collaboration" to "authorizing execution."

### 1. Gate mode before content
Before giving substantive content, switch discuss ↔ execute. A single "let's discuss, don't act yet" prevents the AI from jumping to implementation before the frame is formed. This switch happens once per collaboration, but it's the precondition for everything after.

### 2. Scaffold before application
Ask for definitions / dimensions first, then apply them to concrete cases. Load the frame first; subsequent output is constrained into it. Lead with "review these 16 findings" and the AI uses its own frame (possibly inconsistent); lead with "what dimensions does code review use" and the AI's output is shaped into the frame you wanted.

### 3. Method before content
Announce "I'll feed context via Q&A next" before doing so. This switches the AI from single-shot reasoning to iterative reasoning — it enters a wait-to-be-completed state instead of jumping to conclusions with partial context.

### 4. Let the AI expose its gaps, then fill precisely
Don't front-load all background. The AI says what it lacks; you supply exactly that. Filling what the AI actually asked for costs less and absorbs better than dumping everything up front. This is the highest-leverage context-economy move.

### 5. Position to reweight, not to inform
Sometimes you feed something that doesn't change the facts, only the weight of their interpretation. "This project is an Agent Factory, not a coding agent" — the same finding gets re-prioritized. This is the highest-order context move. Time it after the frame is formed: too early and there's no scaffold to receive it; too late and there's no room to re-rank.

### 6. Confirm direction, fill unknowns, anchor to verifiable
One utterance does three things: "yes" (lock the direction) + fill the open unknowns (close the frame) + point to a verifiable real anchor (existing memory, checkable fact). Use prior knowledge as an anchor to pin the discussion to reality, not let the AI speculate.

### 7. Gate the irreversible with minimal consent
Authorize irreversible actions with the smallest consent ("go ahead"). Delegate everything reversible fully. You are the final gate on the irreversible — and you only open it after the frame is complete, which guarantees execution happens at peak context focus.

### 8. Actively correct state drift
The world changed (commits landed, files moved, requirements shifted) — proactively ask the AI to re-verify. The AI won't say "my judgment is stale" on its own. Its judgments have timestamps; you own their validity period.

## Handling the Four Unknowns (your side)

| Kind | Your move |
|---|---|
| Known Knowns | State them. Don't make the AI guess. |
| Known Unknowns | Clarify proactively — or better, let the AI ask you (手法 4). |
| Unknown Knowns (implicit standards) | **Externalize via prototype or example, not description.** "I'll know it when I see it" can't be conveyed in words. Prototype early; it's cheapest there. |
| Unknown Unknowns | Open with a "blind spot pass" — tell the AI your identity and knowledge boundary, ask it to list relevant unknowns and teach you how to ask. |

## Self-Review Baked In

`examples/meta-agent/` carries a principle: every produced agent bakes in its own failure-degradation and verification. CCA must hold for itself: **after each application, check whether the output got sharper.** If it didn't, the methodology isn't wrong — some unknown on your side isn't externalized yet. Go back to 手法 4 or run a blind spot pass.

## Naming

CCA (Context Co-Authoring) is a working name. Naming is an Unknown Known — you'll know it's right when you see it.