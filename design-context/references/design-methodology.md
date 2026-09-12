# D.C.G.R.R. — the full methodology (depth reference)

> Loaded when you need the *why* behind the rules in SKILL.md, or when building a full
> design system. SKILL.md carries the one-line rules; this file carries the reasoning,
> full tables, and edge cases. Not meant to be loaded for trivial or component-level tasks.

---

## Coverage checklist (10 design axes)

Use as a review aid and as a self-check that the skill covers a dimension. Each axis points
to where it lives below or in another reference.

| Axis | Covered in | Note |
|---|---|---|
| Layout / grid | 2.2 | grid family, max width, rhythm, breakpoints |
| Spacing | 2.1 spacing scale | 4px or 8px base, integer multiples only |
| Color palette | 2.1 accent + neutrals | one accent unless explicitly multi-brand |
| Typography | 2.1 display + body | one display face, neutral body |
| Shape language | 2.1 radius + border + shape rule | radius/border tiers ≤ 3, aligned with elevation |
| Elevation / depth | 2.1 elevation scale | surface-0..3, each a fixed shadow + blur/overlay |
| Visual hierarchy | 2.2 narrative cadence + density + Step 4 intent self-check | what the user sees first |
| States / feedback | 2.3 states + degradation ladder | risk-matched, not all-states-for-all |
| Motion / interaction | 2.4 + 2.7 | easing exception, image-sequence, compositor-only |
| Icons / imagery | `asset-generation.md` | medium choice, sequence rules |
| Accessibility / responsiveness | 2.2 breakpoints + Step 4 checklist | contrast, focus, reduced-motion, collapse rules |

If an axis is empty for a given task, that is a gap to close, not a section to skip silently.

---

## Core idea

Most AI design output looks formulaic because the AI receives a "make a page" task but not
enough "brand and experience" rules. This methodology fixes that by turning design intent
and constraints into structured, machine-readable context **before** any generation happens.

The loop: **Define → Constrain → Generate → Review → Refine.**

| Phase | Key question | Who owns it |
|---|---|---|
| **Define** | What problem, for whom, and what does success look like? | Human (with AI drafting) |
| **Constrain** | What are the brand, token, layout, motion, asset, technical rules? | Human writes; AI follows |
| **Generate** | Drafts, components, layouts, images, videos, copy, SVG, motion. | AI |
| **Review** | Does it match intent, spec, brand, a11y, performance? | Human + automated checks |
| **Refine** | Update spec, tokens, prompts, library from learnings. | Human decides; AI executes |

---

## 1. Define — required fields

| Field | Question it answers |
|---|---|
| Product goal | What business or user outcome must this design support? |
| Audience | Who will see/use it? Device, mindset, literacy? |
| User task | What 1-3 things must they do or feel? |
| Success criteria | How do we know it works? |
| Mood / vibe | 3-5 adjectives describing the intended feel. |
| References | URLs, brands, screenshots, products to emulate or avoid. |
| Existing assets | Logo, colors, fonts, photo style, illustration style, icons. |
| Non-negotiables | A11y, legal, brand, performance, regulatory constraints. |
| Deliverable scope | Component, page, site, image, video, or full design system. |

### 1.1 If a field is missing

- In an interactive session: ask **one** clarifying question. Do not guess on intent.
- In a non-interactive / automated pipeline: fill the field with an **explicitly labeled
  assumption** and proceed. A labeled guess the human can correct beats a silent guess
  they never see.

### 1.2 Convert vague adjectives into concrete comparisons

- "modern" → "clean, minimal, high contrast, single accent, generous whitespace"
- "premium" → "restrained motion, large type, real photography, tight spacing hierarchy"
- "alive" → "immediate feedback, micro-interactions, staggered motion, human copy"

---

## 2. Constrain — full tables and reasoning

Constraints are what separate generic output from on-brand output. Write them as rules with
values, not feelings. The SKILL.md rules are the one-line versions; what follows is the depth.

### 2.1 Visual language tokens

| Token | Example value | Notes |
|---|---|---|
| Primary accent | #0ea5e9 | One accent per screen **unless** the brief is explicitly multi-brand (dual-brand systems exist — document the rule, don't assert a universal). |
| Neutral base | zinc-50 → zinc-950 | Full neutral ramp, not two grays. |
| Text primary | zinc-900 / zinc-100 | Light + dark. |
| Font display | Geist, Satoshi, Cabinet Grotesk, or brand font | One display face max. |
| Font body | same family or Inter Tight / IBM Plex Sans | Body can be the display family's text cut or a neutral sans. |
| Spacing scale | 4px base × {0,1,2,3,4,6,8,12,16} = {0,4,8,12,16,24,32,48,64} — OR 8px base × {0,0.5,1,2,3,4,6,8,12} = {0,4,8,16,24,32,48,64,96} | Pick 4px **or** 8px base, document it, and never mix. Every `padding`/`margin`/`gap` is a base integer multiple. Density is abstract (1-10); this scale is the concrete number you actually type. |
| Corner radius | 0px / 8px / 12px / 16px / 999px | See shape-language rule below — keep tiers ≤ 3 and align with elevation. |
| Border weight | 0 / 1 / 2 px | See shape-language rule below. |
| Shadow scale | none / subtle / pronounced | With exact values, not adjectives. (See elevation scale for the full system.) |
| Elevation scale | surface-0 / surface-1 / surface-2 / surface-3 | See elevation system below. |
| Density | 1-10 | 1 = gallery airy, 10 = cockpit dense. (Operational definition: roughly "information units per viewport at desktop default zoom.") |

#### Shape-language rule

A system's shape language is radius + border weight + line treatment treated as one system,
not independent tokens. The rule that makes it read as a brand rather than a pile of values:

- **Radius tiers ≤ 3**, **border-weight tiers ≤ 2**. More tiers reads as inconsistency.
- **Radius aligns with elevation**: the more a surface floats (higher elevation), the larger
  its radius and the softer/larger its shadow. Ground-level surfaces are sharper and flatter.
  e.g. `surface-0` → radius 0–8px, no shadow; `surface-2` → radius 12–16px, pronounced shadow.
- A pill (`999px`) is a CTA/control signal, not a card shape — reserve it for interactive
  elements, and keep the rest of the system on the small tier set.

#### Elevation system

| Level | Use | Shadow (example) | Other |
|---|---|---|---|
| surface-0 | page background, full-bleed sections | none | — |
| surface-1 | resting cards, inputs, default tiles | `0 1px 2px rgba(0,0,0,.08)` (subtle) | — |
| surface-2 | sticky headers, dropdowns, floating cards | `0 4px 12px rgba(0,0,0,.12)` (pronounced) | optional backdrop `blur(8px)` on overlays |
| surface-3 | modals, popovers, top-of-stack | `0 12px 32px rgba(0,0,0,.20)` + overlay scrim | `backdrop-filter: blur(12px)` + dim the scrim |

Define each level once; reference it by name everywhere (`elevation: surface-2`). Never
inline a one-off shadow — if you reach for one, you are missing a tier.

### 2.2 Layout

- Grid family: 12-col, 6-col, bento, asymmetric, or editorial.
- Max content width, e.g. `max-w-[1400px] mx-auto`.
- Section rhythm, e.g. `py-24` desktop, `py-16` mobile.
- Breakpoints: `sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`.
- Mobile collapse rule for **every** multi-column layout.
- **Narrative cadence (time, not just space):** core value (title) → supporting copy
  (subtitle) → action (button), revealed with **temporal offset** (stagger 0.15–0.25s) and
  **spatial masking** (mask wipes left→right or bottom→top), instead of all-at-once. This
  manufactures a reading rhythm. Do NOT justify this with "F-pattern / Z-pattern" — that is
  a contested eye-tracking simplification, not a law; the valid insight is the stagger +
  mask, not the eye-path claim.

### 2.3 Components

- Inventory: what exists, what is new, what must not be altered.
- State coverage: default, hover, focus, active, disabled, loading, empty, error, success.
  - Not every element needs all states — a plain link has no "done"; reserve "done" for
    commits/submits. Match state coverage to the element's actual risk.
- Allowed / forbidden third-party libraries.
- **Graceful-degradation ladder** (tiered Plan B, not a single fallback):
  - Image fails → placeholder color / blurhash / blur-up
  - Font fails → system font stack (preload + `font-display: swap`)
  - Video / Canvas-frame extraction fails → `<video>` element or single end-frame still
  - Heavy animation jitters or is unsupported → static end state (never a broken half-animation)
  - JS fails to hydrate → server-rendered HTML still legible and navigable

### 2.4 Motion

| Rule | Value | Exception |
|---|---|---|
| Intensity | 1-10 (1-3 static, 4-7 fluid CSS, 8-10 choreography) | — |
| Default easing | `cubic-bezier(0.16, 1, 0.3, 1)` for objects with mass entering/exiting | **Linear is allowed** for mass-less, steady-state motion: progress bars, spinners, mechanical/digital UI, uniform rotation, breathing glows. Do NOT force easing onto motion that should feel mechanical — it reads as wrong. |
| Default duration | 0.2-0.4s micro, 0.6-0.9s reveal | — |
| Scroll behavior | none / reveal / pin / horizontal pan | — |
| Reduced motion | all motion > 3 must honor `prefers-reduced-motion` | none — this is non-negotiable |

**Implementation per motion type** (pick the cheapest that satisfies the look; do not
default to hand-written SVG path animation):

| Motion need | Default implementation | Why |
|---|---|---|
| Rich / photographic / 3D-rendered motion | Image sequence / video / Canvas-frame scrub | Real texture; AI generates frames reliably; SVG path math is error-prone. |
| Scalable icons, logos, line-art UI, small graphics | SVG (static, or CSS `transform`-driven) | Vector-crisp, KB-sized, no pixel cost. |
| Simple pan / scale / rotate / fade | CSS `transform` / `opacity` | Zero asset cost. |

### 2.5 Assets

Full asset/sequence/SVG guidance lives in `asset-generation.md` — it is split out because a
pure image/video request does not need the component and layout tables loaded. See that file
for: medium selection, single-image prompt structure, image-sequence frame budgets,
seed-locking and single-parameter-delta rules, fallback frames, and SVG scope rules.

### 2.6 Do / Don't

- DO: use one accent color across the whole page — **unless** the brief is explicitly multi-brand; then document the rule.
- DON'T: add a second CTA with the same intent.
- DO: generate real images for hero + key sections.
- DON'T: build fake product UIs from styled `<div>` rectangles.
- DO: compose rich motion from an image sequence (AI is reliable at generating frames).
- DON'T: default to hand-authored SVG path animation for rich/photographic motion — AI gets the path math wrong.
- DO: use `linear` easing for mass-less steady-state motion (progress bars, spinners, uniform rotation).
- DON'T: force easing onto motion that should feel mechanical — it reads as wrong.

### 2.7 Performance

Performance is UX — any interaction that drops frames cancels its own visual beauty. Budget
the render cost up front.

- Prefer compositor-only properties for animation: `transform` and `opacity`. Avoid animating
  `width / height / top / left / margin` (they trigger Layout) unless you have a deliberate
  reason (e.g. FLIP with batched measurements) and have documented it.
- Move heavy work off the main thread: offscreen Canvas, Web Workers, `requestAnimationFrame`
  batching, `ImageBitmap` for decoded frames. Do not drive smooth motion directly from
  `mousemove` / `scroll` — interpolate via rAF instead.
- Smooth mouse/pointer tracking: read input on the event, apply via rAF interpolation
  (lerp), never write layout in the event handler.
- Video / sequence playback: prefer pre-extracted frames (Canvas / `ImageBitmap`) over
  directly driving many `<video>` elements; the latter is expensive on the main thread.
- Budget: aim for no long task > 50ms during interaction; LCP / INP targets come from the
  project's perf baseline if one exists.

---

## 3. Generate

AI generates within the constraints.

- Generate **parts**, not a whole finished page, when the spec is thin.
- Prefer reusable components over one-off markup.
- Every interactive element must include states matched to its risk (Section 2.3).
- Every animation must be motivated: hierarchy, storytelling, feedback, or state transition.
- Use real assets or clearly labeled placeholders; never fake screenshots.
- For txt-to-image / txt-to-video: build the prompt from the asset rules (see
  `asset-generation.md`) and the visual language in 2.1.

---

## 4. Review

### 4.1 Pre-flight checklist

- [ ] Intent is clear and served.
- [ ] Tokens from 2.1 applied consistently.
- [ ] Layout works at all breakpoints.
- [ ] Components have the states their risk requires.
- [ ] Motion is motivated with a reduced-motion fallback.
- [ ] Contrast passes WCAG AA for body text.
- [ ] No duplicate CTA intent on the same page.
- [ ] No generic placeholder copy ("Lorem ipsum", "Acme Co", "Jane Doe").
- [ ] Assets match style rules.
- [ ] Accessibility basics covered (alt text, focus, reduced motion).
- [ ] No long task > 50ms during interaction; motion uses compositor properties, not Layout-triggering ones.
- [ ] If motion is image-sequence-driven: a reduced-motion / load-failure end-frame still exists, and no meaning is encoded only in the animation.
- Intent self-check (per screen): where should the user be looking? What should they feel? Where do they go next?

### 4.2 Quality layers

| Layer | Indicators |
|---|---|
| Efficiency | first-draft time, revision rounds, automation coverage |
| Quality | spec adherence, visual consistency, reusability, a11y, responsive |
| Effectiveness | task completion, conversion, error rate, engagement |

For measurable metrics, see `evaluation-scorecard.md`.

---

## 5. Refine (only for persistent projects)

Close the loop by writing learnings back into the system. **This phase assumes an ongoing
repo / design system. For one-shot requests, skip it entirely** — there is nothing to refine
against.

1. Record what worked and what failed in `docs/design/feedback-log.md`.
2. Update the design spec with corrected rules.
3. Update the component library / token file.
4. Update prompt templates used for image/video generation.

---

## AI vs Human division

Full ownership table and decision flowchart live in `ai-human-division.md`. Summary:

- AI: draft generation, asset generation, code/CSS, automated checks, prompt templating.
- Human: define intent, brand/taste judgment, constraint decisions, user interviews, final approval.

Rule of thumb: if the answer is rule-checkable, lean AI. If it requires understanding people,
context, values, or consequences, lean human.

---

## File structure for a full project (System-level)

```
docs/design/
  00-principles.md      # philosophy, AI role, global do/don't
  01-intent.md          # product goal, audience, success criteria
  02-visual-language.md # tokens, type, color, density
  03-layout.md          # grid, breakpoints, responsive rules
  04-components.md      # inventory, states, reuse rules
  05-motion.md          # intensity, easing, reduced motion
  06-assets.md          # photo, illustration, SVG, image-gen prompts
  07-states.md          # loading, empty, error, success, forms
  08-acceptance.md      # pass/fail criteria and review checkpoints
```

The template for these files is in `design-spec-template.md`.