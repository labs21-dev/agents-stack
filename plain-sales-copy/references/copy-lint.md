# Copy lint

Run after every draft. One fail → rewrite the unit. Do not patch with a
parenthetical glossary.

## 1. Sentence cap

The core unit is 3-5 sentences. Count sentences, not lines.

- Subject lines and headlines: 1 sentence or fragment. Still no puff.
- Sequence surfaces: each unit 3-5. The page may be longer; no unit may be.

## 2. Grandma test

Read the unit out loud as if to someone who does not work in the industry.

- Pass: they can repeat what the buyer does today, what it costs, and what
  changes, in their own words.
- Fail: they ask what a word *means*. That is confusion, not curiosity.
- Curiosity ("how do they connect to LINE?", "what does it cost?") is allowed
  and is the point. Do not pre-answer it inside the unit.

If the product is technical, the unit gets simpler, not denser.

## 3. Puff adjectives — banned

Evaluative and atmospheric words. Non-exhaustive; the test is "does this word
assert quality without a number?"

English: `leading`, `revolutionary`, `powerful`, `seamless`, `ultimate`,
`cutting-edge`, `robust`, `best-in-class`, `innovative`, `holistic`,
`end-to-end` (as praise), `next-generation`, `world-class`, `unprecedented`,
`effortless`, `intelligent`, `smart` (as praise), `scalable` (as praise),
`intuitive`, `premium`, `synergistic`, `transformative`, `comprehensive`,
`full-stack` (as praise), `AI-driven` (as praise), `unique`, `perfect`.

Chinese: `領先`, `革命性`, `強大`, `極致`, `流暢`, `全方位`, `賦能`, `高效`
(without a number), `完美`, `智慧` (as praise), `新一代`, `顛覆性`, `卓越`,
`端到端` (as praise).

Empty nouns in the same family: `digital transformation`, `synergy`, `ecosystem`
(as fog), `paradigm`, `數位轉型`, `綜效`, `生態系` (as fog), `賦能`.

`AI-driven` / `powered by AI` is puff unless the mechanism sentence already
said what the software *does* in visible steps. Then drop the AI claim; the
steps are enough.

## 4. Allowed modifiers

Keep words that classify a real category or carry a unit:

- `manual`, `monthly`, `retail`, `in-store`, `3-day`, `40-hour`, `POS`
- numbers, dates, product names, role names

If you can delete the word and the fact remains, it was puff. Delete it.

## 5. Pronoun count

Count `you/your/你們/你的` vs `we/our/I/我們/我的`.

- Fail if we-side ≥ you-side.
- Names of the customer's role (`store manager`, `店長`) count as you-side.

## 6. CTA friction

Fail if the first ask is a close: contract, payment, hour-long meeting, "book
my calendar", "start a trial".

Pass if the ask is a 2-minute artifact, a one-screen, a reply with a number,
or a 15-minute look at *their* existing data.

## 7. Unexplained terms

List every acronym or coined term. Each one must either be (a) in the
audience's daily vocabulary, or (b) replaced with the thing it names.

`POS` is allowed for restaurant operators. `FTS5` is not allowed in a
restaurant pitch. When unsure, replace.

## Scores to report

```
sentences: <n>
puff: []
you: <n>
we: <n>
cta: micro | close
unexplained: []
grandma: pass | fail
```

All of `puff`, `cta=close`, `grandma=fail`, `we >= you`, `sentences > 5`
are hard fails.
