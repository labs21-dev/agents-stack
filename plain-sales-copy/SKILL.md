---
name: plain-sales-copy
description: >-
  Write or rewrite any sales or business content so a stranger gets it in 3-5
  sentences, needs no glossary, and meets zero puff adjectives. Use when the
  user asks for a sales pitch, elevator pitch, cold email, landing-page hero,
  homepage copy, one-pager, pitch-deck opener, investor blurb, about-us,
  pricing intro, LinkedIn outreach, value proposition, ICP messaging, or says
  "make this less salesy", "too much jargon", "rewrite this pitch", or "what
  do we actually say". Also use when existing copy is full of 領先 / 革命性 /
  powerful / seamless / end-to-end. Do NOT use for product discovery
  (interview-to-build), fuzzy strategy (meta-thinking-framework), visual
  generation (design-context), legal contracts, API/docs, or brand poetry
  where adjectives are the product. Method: size the surface → extract facts
  → draft a 4-element unit → lint → stop at "tell me more".
---

# Plain Sales Copy

A **gate** for sales and business writing. The job is cognitive efficiency:
buy the next 15 minutes of attention, not the contract. A unit that needs a
follow-up *explanation* has already failed. A unit that earns "how do you do
that?" or "how much?" has succeeded.

## Hard rules

1. **One core unit = 3-5 sentences.** Landing pages, decks, and one-pagers are
   a sequence of units, not one long dump. The first unit must stand alone.
2. **If they need it explained, rewrite.** Confusion ("what does that word
   mean?") is failure. Curiosity ("how?" / "how much?") is the goal.
3. **No puff adjectives.** Nouns are facts, verbs are actions, numbers are
   proof. Classifying words that name a real category (`manual`, `monthly`,
   `retail`) may stay. Evaluative words may not. Lint: `references/copy-lint.md`.
4. **Four elements, in order:** pain → cost of inaction → mechanism + result →
   low-friction CTA. See `references/four-elements.md`. Pain and cost may share
   a sentence; neither may be missing.
5. **You > we.** Count pronouns. If "we/our/I" outnumbers "you/your", rewrite.
6. **CTA is a micro-commitment.** Forbidden as the first ask: sign, buy, "1-hour
   demo", "jump on a call this week". Allowed: a 2-minute clip, a one-screen
   screenshot, "reply with X", a 15-minute look at *their* numbers.
7. **The unit's job is "tell me more", not the close.**

## Flow

0. **Size the surface** (table below). Default one level down.
1. **Extract facts.** Audience, what they do today, what that costs, the
   mechanism in grandma words, one number, one named proof (or a labeled
   assumption). Missing facts → at most one question batch; otherwise fill
   `assumptions` and proceed.
2. **Draft one 4-element unit** into `templates/copy-draft.md`. For a sequence
   surface, draft the hero unit first; later units only add proof or mechanism,
   never a second pitch.
3. **Lint** against `references/copy-lint.md`. Any fail → rewrite the unit,
   do not add a footnote.
4. **Deliver the copy + the lint scores.** Do not deliver copy that failed lint.

## Size the surface

| Size | Signal | Action |
|---|---|---|
| **Trivial** | one headline, subject line, or sentence | Rewrite in place. Still lint. No worksheet. |
| **Unit** | elevator pitch, cold email, hero, LinkedIn note | One 4-element unit. |
| **Sequence** | landing page, one-pager, deck | Hero unit + later proof/mechanism units. Each unit lints on its own. |
| **House** | messaging for multiple ICPs | One unit per audience. Do not blend audiences. |

## Sibling split

| Need | Skill |
|---|---|
| What product to build (discovery) | `interview-to-build` |
| Fuzzy strategy / irreversible decision | `meta-thinking-framework` |
| UI / image / video generation | `design-context` |
| The words that sell or explain value | **this skill** |

If the product, audience, or result number does not exist yet, stop and say so.
Do not invent a pitch on top of a missing product.

## References

- `references/four-elements.md` — pain, cost, mechanism+result, CTA; formula; allowed CTAs
- `references/copy-lint.md` — puff list, you/we count, sentence cap, grandma test
- `references/anti-patterns.md` — failed vs passing examples, including the restaurant unit

## Templates

- `templates/copy-draft.md` — facts, unit, lint scores; copy this every non-trivial run
