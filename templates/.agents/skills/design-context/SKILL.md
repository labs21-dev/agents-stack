---
name: design-context
description: |
  Use when a request will produce frontend UI, a visual asset, an image prompt, or a video
  prompt, AND the intent/style is not already fully specified by the user or an existing
  design system in the repo. Forces a minimal, checkable design-context object to exist
  before generation so output does not default to generic/templated.
  Do NOT use for: single-property edits (color, spacing, copy tweak) with no ambiguity;
  bug fixes; refactors; or when the user already gave complete visual specs and you only
  need to execute. For those, just do the work.
---

# design-context

A **gate**, not a ceremony. Its only job: force a minimal, checkable design-context object
to exist before any UI/visual/image/video generation, so the output does not fall back to
template instinct (blue-purple gradient, Inter, fade-in, three feature cards).

Keep it as cheap as the task allows. Depth lives in `references/` and loads only when needed.

## Step 0 — Size the task

Decide depth before doing anything else. Default one level *down* if unsure — ceremony
costs more than it saves below "feature" scale.

| Size | Signal | Action |
|---|---|---|
| **Trivial** | single property / copy tweak, no ambiguity | Skip everything. Just do it. |
| **Component** | one new component, or one asset; existing design system | Step 1 inline, no file. Then generate. |
| **Page / feature** | a page, a section set, a feature | Step 1 + write `docs/design/design-context.md`. |
| **System** | new brand, new product, multi-page | Full spec folder — see `references/design-spec-template.md`. |

## Step 1 — Minimum context gate (always, even Component-level)

Before generating, this object must exist — from the user, from the repo (existing tokens /
brand file), or inferred and labeled. Output it where the user can see and correct it.

```yaml
goal: <one sentence: outcome this must accomplish>
audience: <who, device, mindset>
vibe: [3-5 adjectives]
accent_color: <hex or token>
type: <display font, body font>
motion_intensity: <1-10>   # 1-3 static, 4-7 fluid CSS, 8-10 choreography
visual_density: <1-10>     # 1 gallery-airy, 10 cockpit-dense
reference: <one anchor product/brand, or "none given">
assumptions: [everything you inferred instead of being told]
```

Rules:
- Ask **at most one** clarifying question. Everything else → fill with a labeled
  `assumptions` entry and proceed. A labeled guess the human can correct beats a silent
  guess they never see.
- In a non-interactive pipeline: ask zero questions, fill every field as a labeled assumption.
- Do not use adjectives without numbers. "premium" alone is rejected; convert to concrete
  comparisons (see `references/design-methodology.md` §1.2).

## Step 2 — Non-negotiable rules (apply by default, inline)

1. **One accent color per screen** — unless the brief is explicitly multi-brand; then
   document the rule.
2. **Easing:** `linear` for mass-less / steady-state motion (spinners, progress bars,
   uniform rotation, breathing glows); `cubic-bezier(0.16, 1, 0.3, 1)` for objects with
   implied mass entering/exiting. Never reversed.
3. **Rich / photographic / 3D motion → image sequence or video**, not hand-authored SVG
   path animation. SVG stays for icons, logos, line-art UI. See
   `references/asset-generation.md`.
4. **Animate only `transform` / `opacity`.** Never `width/height/top/left/margin` unless
   you have a documented reason (e.g. FLIP). Smooth pointer tracking goes through rAF, not
   directly in the event handler. Full reasoning: `references/design-methodology.md` §2.7.
5. **States match the element's actual risk** — a link ≠ a submit button. Reserve "done"
   for commits. Cover: default, hover, focus, active, disabled, loading, empty, error,
   success as applicable.
6. **Graceful-degradation ladder, not a single fallback:** image→placeholder/blurhash,
   font→system stack, video/Canvas-frame→`<video>` or end-frame still, heavy
   animation→static end state, JS→server-rendered HTML still legible.
7. **No fake data, no styled-`<div>` fake product UI, no Lorem ipsum / Acme Co / Jane Doe.**
8. **Every animation is motivated** (hierarchy / storytelling / feedback / state transition)
   and degrades to a static end-state under `prefers-reduced-motion` or load failure.

For the full tables (tokens, spacing/elevation/shape scales, layout breakpoints, motion
duration, performance budgets) and the reasoning behind each rule, see
`references/design-methodology.md`.

## Step 3 — Generate

Build from Step 1's object + Step 2's rules, not from template instinct.

- Generate **parts**, not a whole finished page, when the spec is thin.
- Prefer reusable components over one-off markup.
- Every interactive element carries the states its risk requires.
- Use real assets or clearly labeled placeholders; never fake screenshots.
- For images / video / SVG / image sequences: build prompts from the Step 1 object — see
  `references/asset-generation.md` for medium selection, prompt structure, and sequence rules.

## Step 4 — Self-check

- [ ] Every Step 1 value is visible in the actual output (not silently dropped).
- [ ] No Step 2 rule silently broken.
- [ ] Assumptions are shown to the user, not hidden.
- [ ] Motion, if any, uses compositor properties and has a reduced-motion fallback.
- [ ] No long task > 50ms during interaction.
- Intent self-check (per screen): where should the user be looking? What should they feel?
  Where do they go next?

## File side-effects (behavior contract)

- **Component-level:** no files written. The Step 1 object lives inline in the response.
- **Page / feature:** write `docs/design/design-context.md`. **If it already exists, do not
  overwrite** — read it, reconcile the Step 1 object against it, and append/update. Ask
  before replacing a hand-written design system.
- **System-level:** create the `docs/design/` spec folder from
  `references/design-spec-template.md`. Ask before overwriting an existing folder.
- `feedback-log.md` is only written in the **Refine** phase, which applies to persistent
  projects only — skip it entirely for one-shot requests.

## Human checkpoints

- **Always:** the Step 1 `assumptions` list is the human's 10-second review surface. Surface
  it; do not bury it.
- **Component / page:** human reviews the first draft against Step 1.
- **System:** human locks tokens and brand direction before multi-page generation begins;
  human approves any asset that could carry likeness/copyright risk
  (see `references/ai-human-division.md`).

## Reference index

| When you need | File |
|---|---|
| Full token/layout/motion tables, performance budgets, the reasoning behind the rules | `references/design-methodology.md` |
| Image / video / SVG / image-sequence prompting and medium choice | `references/asset-generation.md` |
| Full spec folder template (System-level) | `references/design-spec-template.md` |
| AI vs human decision boundary | `references/ai-human-division.md` |
| Measurable quality metrics | `references/evaluation-scorecard.md` |