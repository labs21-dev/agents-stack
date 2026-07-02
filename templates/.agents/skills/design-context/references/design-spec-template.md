# Design Spec Template

> Machine-readable design spec for AI-assisted frontend, visual, image, and video work.
> Fill every section before generation. Use numbers, not adjectives.

---

## 00. Principles

### Design philosophy
- One-sentence design philosophy for this project.

### AI role
- What AI is allowed to generate autonomously.
- What AI must propose but not decide.
- What AI must never do.

### Global priorities
1. ___
2. ___
3. ___

### Global do / don't
- DO: ___
- DON'T: ___

### Exception handling
- If a rule conflicts with the brief, escalate to human.

---

## 01. Intent

### Product goal
> What outcome must this design support?

### Audience
> Who is this for? Include device, mindset, literacy.

### User tasks
1. ___
2. ___
3. ___

### Success criteria
- [ ] ___
- [ ] ___
- [ ] ___

### Mood / vibe
- ___
- ___
- ___

### References
- ___
- ___
- ___

### Non-negotiables
- ___
- ___
- ___

---

## 02. Visual Language

### Brand personality
> 2-3 sentences.

### Color
| Token | Light mode | Dark mode |
|---|---|---|
| Primary accent | ___ | ___ |
| Neutral base | ___ | ___ |
| Text primary | ___ | ___ |
| Text secondary | ___ | ___ |
| Surface | ___ | ___ |
| Surface elevated | ___ | ___ |
| Error | ___ | ___ |
| Success | ___ | ___ |

### Typography
| Role | Font | Size desktop | Size mobile | Weight | Line height |
|---|---|---|---|---|---|
| Display | ___ | ___ | ___ | ___ | ___ |
| H1 | ___ | ___ | ___ | ___ | ___ |
| H2 | ___ | ___ | ___ | ___ | ___ |
| Body | ___ | ___ | ___ | ___ | ___ |
| Caption | ___ | ___ | ___ | ___ | ___ |
| Mono | ___ | ___ | ___ | ___ | ___ |

### Spacing / density
- Density scale: ___ / 10
- Section gap desktop: ___
- Section gap mobile: ___
- Content max-width: ___

### Shape
- Corner radius rule: ___
- Shadow rule: ___
- Border rule: ___

---

## 03. Layout

### Grid system
- ___

### Breakpoints
- sm: ___
- md: ___
- lg: ___
- xl: ___
- 2xl: ___

### Section order
1. ___
2. ___
3. ___
4. ___

### Responsive collapse rules
- For every multi-column layout, declare the `< 768px` behavior.

### Immutable layout rules
- ___
- ___

---

## 04. Components

### Reusable components
| Component | Location | States | Notes |
|---|---|---|---|
| Button | ___ | default, hover, active, disabled, loading | ___ |
| Card | ___ | default, hover, focus | ___ |
| Input | ___ | default, focus, error, disabled | ___ |
| Nav | ___ | default, mobile, scroll | ___ |
| Footer | ___ | default | ___ |

### New components needed
| Component | Purpose | States |
|---|---|---|
| ___ | ___ | ___ |

### Forbidden changes
- ___
- ___

---

## 05. Motion

### Motion intensity
- ___ / 10

### Easing
- Default: ___
- Enter: ___
- Exit: ___

### Timing
- Micro: ___
- Reveal: ___
- Page transition: ___

### Scroll behavior
- ___

### Motivation rule
Every animation must serve one of: hierarchy, storytelling, feedback, state transition.

### Reduced motion
- For intensity > 3, all motion degrades to instant/static under `prefers-reduced-motion`.

### Motion do / don't
- DO: ___
- DON'T: ___

---

## 06. Assets

### Photography style
- ___

### Illustration style
- ___

### SVG rules
- ___

### Icon family
- ___

### Image generation prompt template
```
Subject: ___
Style / medium: ___
Lighting: ___
Mood / atmosphere: ___
Composition / camera: ___
Color palette: ___
Negative prompts: ___
Technical specs: ___
```

### Video generation prompt template
```
Subject: ___
Style / medium: ___
Motion description: ___
Lighting / atmosphere: ___
Camera moves: ___
Pacing / transitions: ___
Color palette: ___
Negative prompts: ___
Technical specs: ___
```

### Asset checklist
- [ ] Hero image / video
- [ ] Key section visuals
- [ ] Icons
- [ ] SVG decorations
- [ ] Social / OG image

---

## 07. States

### Loading
- Skeletons, spinners, or inline placeholders?
- Color and timing?

### Empty
- Visual + copy + next action.

### Error
- Inline or contextual?
- Copy tone?

### Success
- Visual feedback and copy.

### Form validation
- Inline error placement?
- Focus behavior?
- Helper text rule?

---

## 08. Acceptance

### Must pass
- [ ] ___
- [ ] ___
- [ ] ___

### Must fail
- [ ] ___
- [ ] ___

### Human review points
- ___
- ___

### Automated checks
- [ ] Lint / type check
- [ ] Visual regression
- [ ] Accessibility (contrast, focus, reduced motion)
- [ ] Performance (LCP, INP, CLS)
- [ ] Responsive

### Sign-off
- Design: ___
- Product: ___
- Engineering: ___
