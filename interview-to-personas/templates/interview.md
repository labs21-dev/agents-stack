# Persona Interview

Use this as a starting set, not a mandatory questionnaire. Ask one batch,
reflect the draft back, then drill only into missing or contradictory layers.

## Batch A: Interaction

1. Language: should the agent follow your current turn, use one default
   language, or switch language by task?
2. Shape: one-sentence conclusion, short blocks, checklists, comparison table,
   or long-form analysis?
3. Challenge: when should the agent point out weak assumptions, missing
   context, contradictions, or risks?
4. Objection limit: one fatal issue, at most three, or a graded list?
5. Waste: what makes an answer feel wasted?
6. Value: what makes an answer feel worth the round?

## Batch B: Judgment

1. Priority order for product or architecture decisions.
2. Which product layers must be thought through before implementation?
3. Which constraints must always stay present?
4. Which mistakes recur often enough to become standing rules?
5. How is a preference promoted to a principle: explicit statement,
   repetition, agent proposal plus confirmation, or another gate?

## Batch C: Cross-domain and style

1. Should cross-domain analogies be selected by relevance and similarity?
2. Which analogies have worked well?
3. Which agent voices or styles should be banned?
4. Should different roles use different personas, or should one persona cover
   all sessions?

## Draft clause format

For each candidate clause, record:

```text
Layer: interaction | judgment | risk | style | role
Clause: {Must / Should / Avoid ...}
Evidence: {user's wording, repeated correction, or explicit confirmation}
Scope: {all sessions | engineering | product | research | trading | ...}
Confidence: confirmed | derived
```

Do not store secrets, private transcripts, medical or diagnostic claims, or
real-world events that may become stale. Store the reusable operating rule
instead.
