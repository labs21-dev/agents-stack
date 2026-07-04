---
name: investor-qa-dialectic
description: Use when preparing investor Q&A, business proposals, accelerator applications, or pitch decks with AI assistance. Especially when AI defaults to generating generic functional answers, feature lists, or marketing phrases that need human push-back to reach original insight.
---

# Investor Q&A Dialectic Methodology

## Overview

Investor Q&A prep fails in a predictable pattern: AI generates generic but well-structured answers, human accepts them too early, and the result is forgettable. This methodology treats AI as **generator + sparring partner**, not answer machine. The human's job is to push back on every vague claim, false premise, and functional description — because **the best answers come from the tension, not from either side alone.**

## Core Pattern: Dialectic Loop

```
Human: draft or context
  → AI: structured answer + flag vague/functional/premise risks
  → Human: push back ("不對", "太複雜", "列功能而已")
  → AI: refine, check filter
  → Human: judge
  → [Next answer or loop again]
```

Each answer must survive at least one push-back cycle before finalizing. No exceptions.

---

## Process (Spiral, Not Linear)

Unlike a pipeline where Phase 1 → Phase 2 → Phase 3, answers and premises co-evolve. Writing one answer may expose a premise gap that rewrites previous answers.

### Phase 0: Premise Layering

Premises operate at three levels. You need all three, and you need to know which is which.

```
L1 Objective Facts: What is true now regardless of story?
   (team background, product stage, revenue, headcount)

L2 Narrative Stance: How you interpret the facts?
   (insight about the market, contrarian view, diagnosis)

L3 Forward Claim: What you will become?
   (vision, trajectory, commitment)
```

**Lock L1 first.** L2 and L3 can evolve, but L1 changes cascade across all answers.

**When L1 and L2/L3 conflict,** don't hide the gap. Write a bridge statement that explicitly connects them. Example:

> L1: "我們背景是 Enterprise" → L2: "我們自己做落地部署"
> → Bridge: "我們相信做對的 tool，自己先成為 user——所以實際下場做部署，親自驗收"

The gap isn't a weakness. An unacknowledged gap is.

### Phase 1: Per-Answer Spiral

```
Round 1 — Generate + Flag
  AI writes structured answer, flags:
    - vague verbs (完善、優化、加強)
    - functional listings
    - marketing phrases
    - premise assumptions

Round 2 — Human Push-Back
  Human questions:
    - "這是功能列舉還是解決問題？"
    - "這個 premise 從哪來的？正確嗎？"
    - "換成競品名字這句話還成立嗎？"
    - "這是我自己的 insight 還是 AI 生成的通貨？"

Round 3 — Refine
  AI incorporates push-back, passes through filter

Exit condition: answer passes filter AND reveals no new premise gaps
```

**Key rule:** If this answer reveals a premise gap, stop. Update Phase 0 premises, then re-check previous answers before continuing.

### Phase 2: Spiral Check

When you exit Phase 1 (after N consecutive answers with no new premise gaps):

```
□ Cross-check: do all answers share the same L1 premises?
□ Core thread: trace one insight through all answers — is there a contradiction?
□ Bridge check: every L1-L2 gap has an explicit bridge?
```

### Phase 3: Field Test

Read every answer aloud. If it doesn't sound natural spoken, rewrite. If you can't explain it to a non-expert, it's not clear enough. If it can't survive a skeptical follow-up, it's not defensible.

---

## Quality Filter

Every answer must pass all four:

```
L1 Premise Integrity — facts still correct?
   Check all premises from Phase 0

L2 Pain-First — solving problem or listing features?
   Test: swap in competitor name — if still works, fail

L3 Specific Thickness — pixel or blur?
   Pass: "從 A 到 B 花了 3 個月"
   Fail: "完善"

L4 Memorability — can reviewer retell in 30 seconds?
   One claim, one image, one number
```

---

## Answer Tactics by Question Type

| Question type | Core move | What to avoid |
|---------------|-----------|---------------|
| **One-line summary** | Analogy: known-thing variant | Describing what it is (too long) |
| **Project description** | Pain-Structure: problem → root cause → solution | Functional listing |
| **Differentiation** | Contrast: why existing solutions can't do this | Saying "we're better" without saying "than what" |
| **Contrarian view** | Original stance: something true that others don't see | Generic industry observation |
| **Why now** | Specific trigger: what changed in the world | "AI is growing fast" |
| **Progress** | Milestone pair: from X to Y | "完善" / "優化" |
| **Why this accelerator** | Specific resource: why this one, not others | "需要資金" |

---

## The One Number Rule

Every major answer needs at least one concrete number.

```
❌ "需要算力"
✅ "訓練一個 <100MB, <5ms 的模型，目前算力缺口約 $X"
❌ "用戶成長快"
✅ "過去三個月從 0 到 50 個 POC 客戶"
```

Reviewers won't remember your product name. They'll remember the number.

---

## Red Flags

| Thought | Reality |
|---------|---------|
| "先全部寫完再回頭修 premise" | One wrong premise cascades across 10+ answers. Fix now. |
| "先順著 AI 的版本走" | You won't come back. Push back now. |
| "功能列舉沒關係吧" | #1 killer. Every redundant sentence is negative signal. |
| "這 marketing phrase 聽起來不錯" | Reviewers are immune. It conveys nothing. |
| "隱藏弱點比較安全" | Hiding is worse than having. Explicit weakness > implicit flaw. |
| "這只是 draft，等等再 refine" | If you skip push-back now, you won't do it later. |

---

## Common Mistakes

- **Premise too shallow**: Only locking facts (L1) without L2/L3 means answers lack narrative tension
- **Linear execution**: Writing all answers then realizing premise is wrong → massive rework
- **No bridge**: Leaving L1-L2 gap unaddressed → reviewer senses something off
- **Skipping push-back**: Accepting AI's first draft is the most common failure mode
- **No oral check**: Written answers that can't be spoken fail in interviews and video

---

## Quick Reference: Writing Session Flow

```
1. Lock L1 premises (facts)
2. Define L2 narrative stance + L3 forward claim
3. Identify any L1-L2 gaps → write bridges
4. For each answer:
   a. AI generates → flags issues
   b. Human push-back
   c. Refine → check filter
   d. If premise gap surfaced → go back to step 1
5. Cross-check all answers for consistency
6. Read aloud → revise for spoken clarity
```
