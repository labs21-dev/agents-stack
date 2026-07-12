# Context Co-Authoring (CCA)

A domain-agnostic collaboration methodology. The thesis: **AI output's ceiling is set by context clarity, not by model capability.** Most "correct but mediocre" output is a context problem wearing a capability mask.

CCA is the operationalized form of that thesis — philosophy + mechanism, not philosophy alone.

## What it is not

- **Not a Skill.** It is always-on thinking discipline, not pull-based reference knowledge. Putting it in `skills/` would let it be opt-in, which defeats the thesis (there is no scenario that is *not* a context-collaboration scenario — it IS the work).
- **Not an agent.** It has no territory. Agents have territory + tools + job. CCA is the operating layer *under* agents, not one of them.
- **Not a modification of meta-agent.** `examples/meta-agent/` is already scenario-specialized (ARC agent design) and stays as-is. meta-agent is CCA's proof-of-mechanism (its 4-module protocol is the ARC-specialized instance of CCA's protocol), not its deployment target.

## The two documents

| Document | For | How it takes effect |
|---|---|---|
| [`CONSTITUTION.md`](./CONSTITUTION.md) | The human, read once and internalized | You carry it into every collaboration. AI does not load this. |
| [`AI-MODULE.md`](./AI-MODULE.md) | The AI, every turn | Pasted as the base layer of an agent's system prompt (cache: static), with territory appended. |

The two are symmetric and complementary. The human half sharpens questions; the AI half externalizes its own gaps. Either alone is inert — the human half without the AI half is a grimoire you forget; the AI half without the human half has no co-author on the other side.

## Relationship to existing work

- **vs thariq's four-unknowns framework**: CCA adopts the four unknowns verbatim. CCA's increment over it is (a) mechanism that runs without the human remembering to run it, (b) the *Shape > Volume* principle (context ordering is itself a lever), (c) *Specificity matches the phase* (the double-edge of instruction, calibrated by phase), (d) bidirectional co-authorship (the AI externalizes its own gaps, not just the human interviewing).
- **vs `examples/meta-agent/system_prompt/`**: meta-agent is CCA's reference implementation in the ARC domain. Its `02-method.md` (4-module protocol, inversion gate, over-correction + second-truth guard) is the ARC-specialized form of CCA's AI-MODULE. meta-agent is not edited; CCA is written fresh beside it.

## Status

CCA has no live consumer yet (meta-agent untouched, no new agent wired). This is honest: **constitution first, first adopting state later.** Forcing a deployment now would be pre-design.

- The **Human Constitution** is usable immediately — you have already used its eight手法 in this conversation.
- The **AI Module** is a standing reference, adopted the next time a new agent is built on CCA.

## Naming

CCA (Context Co-Authoring) is a working name. Rename freely — naming is an Unknown Known (you'll know it's right when you see it).