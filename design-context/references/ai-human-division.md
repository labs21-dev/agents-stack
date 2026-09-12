# AI vs Human Design Ownership

> Clear division of labor for AI-assisted design, frontend, image, and video work.

---

## Rule of thumb

If the answer can be checked by a rule, lean toward AI.  
If the answer requires understanding people, context, values, or consequences, lean toward human.

---

## AI can execute autonomously

| Task | Examples |
|---|---|
| Draft generation | Component drafts, page layouts, CSS, copy variants |
| Asset generation | Images from prompts, video clips, SVG illustrations |
| Pattern application | Apply design tokens, layout rules, motion rules |
| Refactoring | Rename, split, consolidate components |
| Automated checks | Lint, visual regression, contrast, a11y, perf metrics |
| Data summary | Extract analytics, format feedback, compare versions |
| Spec translation | Convert brief into structured spec fields |
| Prompt templating | Build repeatable image/video prompts |

---

## AI can assist but human must decide

| Task | Why human |
|---|---|
| Brand direction | Taste, positioning, competitive context |
| Visual style approval | "On-brand" is a human judgment |
| Copy tone | Authenticity, voice, legal risk |
| Major trade-offs | Performance vs aesthetics, scope vs quality |
| Final quality sign-off | Accountability for shipped work |
| Constraint changes | Changing rules affects everything downstream |

---

## Human must do directly

| Task | Notes |
|---|---|
| User interviews | AI can transcribe / summarize, not replace. |
| Stakeholder alignment | Understanding politics and hidden constraints. |
| Product strategy | Why this page/feature exists. |
| Legal / compliance | Privacy, accessibility law, copyright. |
| Ethical risk | Representation, manipulation, exclusion. |
| Exception handling | When the rules break down. |

---

## Frontend-specific division

| AI | Human |
|---|---|
| Generate component drafts | Define component boundaries |
| Write CSS / motion code | Approve architecture decisions |
| Apply tokens and spacing | Lock brand tokens |
| Write tests | Decide what quality means |
| Run accessibility scans | Interpret failures and prioritize |
| Refactor for reuse | Decide when reuse is worth it |

---

## Image / video generation division

| AI | Human |
|---|---|
| Build prompts from spec | Define style and subject intent |
| Generate candidates | Curate and select final assets |
| Upscale / extend / retouch | Approve use of generated likenesses |
| Batch variations | Ensure brand and legal safety |

---

## Decision flowchart

```
Is the task rule-checkable?
├── YES → Can AI do it safely and reversibly?
│   ├── YES → AI executes
│   └── NO → Human executes with AI assistance
└── NO → Does it involve people, values, risk, or taste?
    ├── YES → Human owns; AI assists
    └── NO → AI proposes; human confirms
```

---

## Escalation triggers

Escalate to human immediately when:

- The brief contradicts the design spec.
- A generated asset could infringe copyright or likeness rights.
- A component affects user data, payments, or legal copy.
- Accessibility or performance requirements cannot be met without trade-offs.
- The output feels off-brand but no rule explains why.
