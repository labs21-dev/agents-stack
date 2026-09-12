# Design Quality Scorecard

> Three-layer metric system for AI-assisted design work.
> Apply to every generated frontend, visual, image, or video deliverable.

---

## 1. Efficiency metrics

| Metric | Definition | Target |
|---|---|---|
| First draft time | Time from spec to first AI draft. | Shorter is better |
| Revision rounds | Number of back-and-forth corrections. | ≤ 3 for standard tasks |
| Automation coverage | Share of checks run by AI vs human. | ≥ 70% |
| Spec-to-output drift | How much the output deviates from spec. | 0 |

## 2. Quality metrics

| Metric | Definition | Check method |
|---|---|---|
| Spec adherence | Follows all tokens, layout, motion, asset rules. | Rule-based audit |
| Visual consistency | Looks like one system, not a collage. | Human review |
| Component reusability | Components are generic enough to reuse. | Code review |
| Accessibility | Contrast, focus, reduced motion, alt text. | Automated + spot check |
| Responsive completeness | Works across breakpoints. | Visual test |
| Motion discipline | Motivated, reduced-motion fallback, performant. | Code + human review |
| Asset fidelity | Images / videos match style rules. | Human review |
| Copy quality | No generic names, no filler verbs, no AI-slop phrases. | Automated scan + human |

## 3. Effectiveness metrics

| Metric | Definition | When measured |
|---|---|---|
| Task completion rate | Users complete the intended task. | After launch |
| Conversion / CTR | Key action rate. | After launch |
| Error / complaint rate | Issues or negative feedback. | After launch |
| Engagement | Time on page, scroll depth, return rate. | After launch |

---

## Scorecard format

For each design iteration, record:

```markdown
## Design Iteration: ___

### Input
- Spec version: ___
- Assets used: ___
- AI model / tool: ___

### Output
- Deliverable: ___
- Link / path: ___

### Scores
| Layer | Metric | Score | Notes |
|---|---|---|---|
| Efficiency | First draft time | ___ | ___ |
| Efficiency | Revision rounds | ___ | ___ |
| Quality | Spec adherence | ___ | ___ |
| Quality | Visual consistency | ___ | ___ |
| Quality | Accessibility | ___ | ___ |
| Effectiveness | Task completion | ___ | ___ |
| Effectiveness | Conversion | ___ | ___ |

### Human review
- What worked: ___
- What failed: ___
- Decision: ship / revise / reject

### Actions
- Update spec: ___
- Update library: ___
- Update prompts: ___
```

---

## Human vs AI responsibility

| Layer | AI | Human |
|---|---|---|
| Efficiency | Collect timing, count rounds, calculate coverage. | Set targets and interpret. |
| Quality | Run rule checks, contrast scans, visual diffs, lint. | Judge consistency, taste, brand fit. |
| Effectiveness | Fetch analytics, summarize trends. | Decide what the numbers mean and what to change. |

---

## Minimum viable tracking

For small projects, track only:

1. Did the output follow the spec? (yes / no / partial)
2. Did it pass visual consistency? (human yes/no)
3. Did it pass accessibility basics? (automated yes/no)
4. What changed in the spec after review?
