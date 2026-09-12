---
name: feedback-to-workflow-learning
description: >
  從 Human-in-the-Loop 長對話中的人類糾偏（Correction）學習，歸納、驗證並版本化沉澱為可執行工作流/方法論；
  同時判定新反饋是執行偏差還是方法缺口，決定是否更新原工作流。
---

# Skill: Feedback-to-Workflow Learning (F2W)

## One-liner

從 Human-in-the-Loop 長對話中的人類糾偏（Correction）學習，歸納、驗證並**版本化**沉澱為可執行工作流/方法論；同時判定新反饋是執行偏差還是方法缺口，決定是否更新原工作流。

---

## When to use

- 存在較長 Agent 軌跡，且人類在中途多次糾正、補約束、改方向或給價值判斷
- 目標是把「這次好不容易做對」變成「可複用工作流 / SOP / playbook」
- 已有工作流 vN，需要根據新反饋決定 **是否升級** 及 **如何升級**
- 需要從反饋過程提取可遷移的 correction skills、規則、門禁與階段方法
- 需要可審計產物：證據鏈、diff、版本決策，而不只是一段總結散文

## When NOT to use

- 只有單次文風潤色、語氣偏好，且不需要制度化
- 純創意發散、無穩定任務結構、也無糾偏信號
- 反饋完全是需求重寫，但用戶只要新答案、明確不需要沉澱方法
- 安全合規的法定流程已固定，禁止從對話「學出」替代流程（此時僅可做執行輔助，不可改主流程）
- 輸入不足以支持歸納（無人類介入、或介入與任務結果無關）

---

## Success looks like

1. **CI Log**：人類糾偏事件被切分、可回溯
2. **Classification**：每個 CI 有 A/B/C/D 判定與證據
3. **Rule Candidates**：`IF–THEN–UNTIL` 級可執行規則
4. **Update Decision**：明確 `No-change | Exception | Patch | Minor | Major`
5. **Workflow 產物**：可運行方法論（步驟 / 分支 / 門禁 / DoD / 例外）
6. **Versioning**：版本號 + changelog +（可選）Agent-facing checklist
7. **Validation**：說明預期減少哪類人類介入，或為何暫不改流程

---

## Core principles

1. **Correction 是監督信號，不是指令洪水**
   先理解意圖與可遷移結構，再決定是否升格為方法。

2. **先分類，後改流程**
   未完成 A/B/C/D 前，禁止重寫主工作流。

3. **可遷移性優先於情節復述**
   抽取「觸發 → 動作 → 完成條件」，去掉一次性專有名詞綁定（除非領域硬約束）。

4. **最小可行更新（Minimum Viable Update）**
   能 Exception 就不改主路徑；能 Patch 就不 Major。

5. **默認不改主流程**
   升級必須跨過明確門檻；一次反饋默認記筆記，不默認改憲法。

6. **證據綁定**
   進入 core 的每條規則至少掛一個 CI；無證據不進主方法。

7. **可執行且可驗證**
   規則必須能寫成步驟或檢查項，並有成功信號 / 失敗信號。

8. **衝突顯式化**
   與舊規則衝突時必須寫 resolve（替換 / 收窄 / 分叉 / 棄用），禁止靜默覆蓋。

9. **骨架硬、肌肉活、產出契約硬**
   判定與輸出結構不自由；分析深度、命名、組織方式可發揮。

10. **保留自主性，但要可解釋**
    在不違反 Must 與門禁的前提下可選擇更優路徑，並簡述理由。

---

## Key concepts

| 術語 | 含義 |
|------|------|
| **CI (Correction Incident)** | 一次人類糾偏事件：含前文狀態、人類輸入、意圖、後果 |
| **Move** | 人類糾偏的原子動作（如 Scope Freeze、Veto Tool、Add Gate） |
| **Rule Candidate** | 候選規則：`IF signal AND stage THEN action UNTIL DoD` |
| **Workflow / Methodology** | 可執行方法資產：階段、分支、門禁、DoD、例外、版本 |
| **A/B/C/D** | 執行偏差 / 方法缺口 / 情境例外 / 需求變更 |
| **Induce / Evolve / Audit-only** | 從零歸納 / 修訂舊版 / 只審計不改版 |
| **DoD** | Definition of Done，步驟或規則的完成定義 |
| **Gate** | 進入下一步前必須滿足的檢查門禁 |

---

## Decision framework（最硬，不可跳過）

### 1) 模式選擇

| 條件 | Mode |
|------|------|
| 無舊工作流，要沉澱方法 | **Induce** |
| 有工作流 vN，有新反饋 | **Evolve** |
| 只分析問題、用戶不要求改版 | **Audit-only** |

### 2) A/B/C/D 分類（每個 CI 必做）

| 類型 | 含義 | 默認處置 |
|------|------|----------|
| **A. 執行偏差** | 方法基本對，未遵守或執行質量差 | 加強提示、清單、校驗；**不改主流程** |
| **B. 方法缺口** | 即使按舊方法做仍會錯/必撞牆 | 進入更新評審 |
| **C. 情境例外** | 主方法仍對，但本 case 合法特殊 | Exception 手冊；慎改主路徑 |
| **D. 需求變更** | 目標/驗收變了，不是原方法「做錯」 | 先更新目標與 DoD，再評估流程連帶影響 |

**輔助判定問題（Should 全問）：**
1. 若嚴格按舊工作流執行，是否仍會出現同類反饋？是 → 偏 B
2. 是否可復現於同類任務？否 → 偏 C
3. 是不是目標/範圍本身變了？是 → 偏 D
4. 是不是遺漏已知步驟/門禁？是 → 偏 A

### 3) 是否升級工作流（Upgrade Gate）

滿足任一 **Must 條件** 才可改主方法：
- 同類 **B** 信號 ≥ **N 次**（默認 N=3，可配置但需顯式寫出）
- 或 **單次高嚴重性**（安全、不可逆、合規、嚴重客戶/資金風險）
- 或舊工作流 **無法表達** 該約束（缺階段 / 缺分支 / 缺門禁）
- 且能寫成可執行規則，並有至少 1 條 CI 證據

否則：`No-change` 或 `Exception` + 記入 backlog。

### 4) 變更級別

| 級別 | 何時 | 做什麼 |
|------|------|--------|
| **No-change** | A 為主，或證據不足 | 只給執行強化建議 |
| **Exception** | C，或低頻特殊 | 旁路規則，不污染主路徑 |
| **Patch** | 小約束/清單/一句 policy | 補門禁或 DoD，主路徑不變 |
| **Minor** | 需加步驟/局部分支 | 主路徑結構仍可識別 |
| **Major** | 階段重排、目標重定義、原則衝突 | 新版本 + 強化回歸 |

### 5) Must / Should / May

- **Must**：模式選擇；CI 切分；A/B/C/D；升級門檻判定；證據綁定；版本化輸出或明確 no-update
- **Should**：回歸 2–3 場景；給出 Agent-facing checklist；衝突檢測
- **May**：擴展二級標籤、畫流程圖、多方案對比、量化介入次數

---

## Operating procedure（薄流程，允許聲明後跳步）

> 若 CI 總數 < 3：可壓縮聚類與大規模整合，直接給 **lightweight patch / exception** 建議，並標註 `confidence: low|medium|high`。
> 跳步時 Must 聲明：跳過了什麼、為何、風險是什麼。

### Step 0 — Orient（定位）
- **目標**：鎖定 Mode 與評價標準
- **Must**：確認任務類型、是否已有 Workflow vN、用戶要 Induce 還是 Evolve
- **May**：讓用戶確認 N 閾值、風險偏好
- **Done when**：寫出 `Mode`、`Current version`、`N`、成功標準

### Step 1 — Capture & Unitize（採集切分）
- **目標**：把長對話變成分析原子
- **Must**：切分 CI；每條含：階段、人類原文、糾偏前症狀、糾偏後短效
- **Should**：映射到粗階段（如 Clarify / Plan / Execute / Verify / Deliver）
- **Done when**：CI 列表可被獨立引用（CI-01…）

### Step 2 — Code & Classify（編碼分類）
- **目標**：理解「人在改什麼、為何改」
- **Must**：為每條 CI 標：
  - Trigger（偏什麼）
  - Target（goal/plan/evidence/tool/style/risk/process）
  - Move（原子動作名）
  - Intent
  - A/B/C/D
- **Should**：歸一命名（動詞+對象），合併同義 move
- **Done when**：分類表完成；B/D 條目標註「可能影響方法」

### Step 3 — Extract Rule Candidates（提規則）
- **目標**：從反饋抽出可執行候選，不直接改憲法
- **Must**：每條候選寫成：
  `IF <signal> AND stage=<...> THEN <action> UNTIL <DoD>`
  並掛 CI 證據、頻率/嚴重性、遷移級別（task-local / domain / global）
- **Should**：區分 human-facing 說明 vs agent-facing 規則
- **Done when**：Rule Candidate 列表（含「不升格」的也保留）

### Step 4 — Decide Update（升級決策）
- **目標**：判定是否更新原工作流
- **Must**：走 Upgrade Gate + 變更級別；寫 Decision Record
- **Must**：衝突檢測（新規則 vs vN）
- **Done when**：明確 `No-change / Exception / Patch / Minor / Major` 之一

### Step 5 — Integrate（整合方法資產）
- **目標**：變成可運行工作流/方法論
- **Must（Induce 或確定更新時）** 輸出：
  - 目標與範圍
  - 階段步驟序列
  - 關鍵決策分支
  - Gates 與 DoD
  - 例外手冊
  - 失敗恢復（何時回退）
  - 版本號
- **Should**：附「Agent 可執行檢查清單」或 policy 條款
- **May**：給出 skill cards（原子 move 目錄）
- **Done when**：vN+1 draft（或 no-update 說明）+ diff 摘要

### Step 6 — Validate & Publish（驗證發布）
- **目標**：證明學到了，而不是寫了更長的文檔
- **Must**：至少 2 個場景走查（可桌面推演）：舊典型失敗案 + 新案
- **Must**：寫預期：哪些 correction 應下降；殘留風險
- **Should**：給出回歸清單與監控指標（如同類 CI 頻率）
- **Done when**：changelog + validation notes + 發布文本（vX.Y）

### Step 7 — Stop（停止條件）

出現以下情況應停止繼續「優化方法論」：
- DoD 已滿足，且用戶未要求更深版本
- 證據不足，僅能 exception/backlog
- 繼續抽象開始過擬合或空洞化

並輸出：`Status: complete | blocked | needs-human-decision`

---

## Intermediate artifacts（中間產物）

按順序積累，不必一次完美：
1. Mode Card
2. CI Log
3. Classification Table
4. Move Inventory（可選）
5. Rule Candidates
6. Update Decision Record
7. Workflow Diff
8. Validation Notes

---

## Output templates（產出契約，結構硬）

### Template A — Mode Card
```text
Mode: Induce | Evolve | Audit-only
Current workflow version: vN | none
Task domain:
N threshold: 3 (default)
Risk posture: normal | strict
User preference notes:
```

### Template B — CI Log（每條）
```text
CI_ID:
Stage:
Pre-state (drift symptom):
Human utterance:
Move (atomic):
Target: goal | plan | evidence | tool | style | risk | process | other
Intent:
Immediate outcome: recovered | partial | failed | unknown
A/B/C/D:
Evidence pointer: (quote or turn ref)
```

### Template C — Rule Candidate
```text
Rule_ID:
IF:
AND stage:
THEN:
UNTIL (DoD):
Because (intent):
Evidence: CI_xx, CI_yy
Frequency/Severity:
Migration scope: task-local | domain | global
Promotion suggestion: backlog | exception | patch | minor | major
Conflict with existing: none | describe
```

### Template D — Update Decision Record
```text
Decision_ID:
Related CIs:
Dominant class: A/B/C/D
Upgrade gate passed: yes | no
Reason:
Change level: No-change | Exception | Patch | Minor | Major
What changes:
What does NOT change:
Conflicts & resolve:
Validation plan:
New version: vX.Y | n/a
Confidence: low | medium | high
```

### Template E — Workflow / Methodology（主交付）
```text
# <Workflow Name> vX.Y

## Purpose
## Scope (in / out)
## Inputs
## Outputs
## Roles (human vs agent)
## Stages
### Stage 1: <name>
- Goal:
- Actions:
- Gate (enter next only if):
- DoD:
- Common failures:
- Human checkpoint: yes/no
## Branching rules
## Global constraints / policies
## Exception playbook
## Recovery / rollback
## Agent-facing checklist
## Changelog
## Validation notes
```

### Template F — Changelog（短）
```text
## vX.Y
- Type: Patch|Minor|Major
- Driven by: CI_..
- Added:
- Changed:
- Deprecated:
- Exceptions added:
- Expected correction drop:
```

### Template G — Lightweight output（CI < 3 或證據不足時）
```text
Findings (brief):
Classified signals:
Suggested temporary exceptions / patches:
Why not full methodology yet:
What data would unlock v1.0:
Confidence:
```

---

## Quality bar（Definition of Done）

- [ ] 已聲明 Mode 與（若有）舊版本
- [ ] CI 已切分且可引用
- [ ] 每個 CI 有 A/B/C/D + 證據
- [ ] 規則為 IF–THEN–UNTIL，而非雞湯
- [ ] 先判定升級門檻，再改流程
- [ ] 變更級別明確；no-update 也有理由
- [ ] 主路徑與例外分離
- [ ] 有版本號與 changelog，或明確 n/a
- [ ] 有驗證預期或阻塞原因
- [ ] 沒有把單次情節過擬合成全局教條
- [ ] **任何進入 core 的規則，必須掛一句人類原話作為證據（Evidence Quote），禁止 paraphrase 或編造**

---

## Anti-patterns（禁止/避免）

1. **一條反饋重寫全世界**（過擬合）
2. **只總結「要注意/要仔細」**，沒有 IF–THEN 與 DoD
3. **A/B 倒置**：把執行失敗當方法失敗，或方法缺口只怪執行
4. **靜默覆蓋舊規則**，無 diff、無棄用說明
5. **例外寫進主路徑**，導致主流程膨脹、不可用
6. **無證據規則**進入 core
7. **微觀劇本 50 步**（僵化）或 **純原則無產出契約**（空轉）
8. **永遠不停地再優化一版**方法論
9. **用文風偏好污染任務正確性流程**（除非用戶明確要求制度化）
10. **偽造驗證**：無走查卻宣稱「已減少糾偏」

---

## Collaboration with humans（如何協作）

當不確定時，**問高槓桿問題**，不要連環追問：
1. 這是 **一次性例外**，還是 **以後默認**？
2. 更傾向 **補門禁（patch）** 還是 **加旁路（exception branch）**？
3. 成功標準是什麼？什麼叫「夠好可以停」？
4. 有沒有絕對不可改的合規/安全硬約束？
5. 若規則衝突，優先保：速度 / 正確性 / 可審計 / 成本？

**衝突時默認優先級（可被用戶覆蓋）：**
安全合規 > 正確性/可驗證 > 可審計/可維護 > 效率 > 文風偏好

人類未裁決前：
- 可給 **臨時 Exception + 待決問題**
- 不要假裝已經發布正式 vN+1

---

## Suggested move vocabulary（可擴展，先映射後新增）

| Move | 典型用途 |
|------|----------|
| Freeze-Scope | 防止範圍膨脹 |
| Redirect-Goal | 拉回真實目標 |
| Lock-Priority | 明確先後與取捨 |
| Demand-Evidence | 要求證據/來源 |
| Veto-Tool | 禁止錯誤工具/路徑 |
| Add-Gate | 增加進入下一步的檢查 |
| Slow-Down | 禁止跳步，先完成前序 |
| Inject-Example | 用正/反例校準 |
| Refute-Assumption | 推翻錯誤假設 |
| Tighten-DoD | 收緊完成定義 |
| Allow-Exception | 批准一次性旁路 |
| Stop-Overrun | 停止過度生成/過度優化 |
| Rollback-Stage | 退回上一穩定階段 |
| Separate-Track | 分軌（主路徑/實驗路徑） |

新增 move 時：先映射到上表；確實沒有再新增，並給定義。

---

## Examples

### Example 1 — Good（Evolve + Patch）
**輸入信號：**
同一工作流下 3 次人類都說：「不要一上來寫結論，先列證據再判斷。」

**正確行為摘要：**
- CI×3 → 多為 B（舊流程缺「證據門禁」）
- Rule：`IF 進入結論階段 AND 無證據列表 THEN 先輸出 Evidence Gate UNTIL 每條結論有依據`
- Decision：Upgrade gate 通過；**Patch**
- v1.2：在 Verify 前加 Gate，不改整體階段順序
- Validation：預期「過早結論」類 CI 下降

### Example 2 — Good（No-change，A 類）
**輸入信號：**
工作流已要求「先澄清範圍」，但 Agent 跳過；人類再次要求澄清。

**正確行為：**
- 判 A
- 不改 SOP 主文
- 強化 Agent checklist + 進入 Plan 前的硬門禁提醒

### Example 3 — Bad（過擬合 Major）
**錯誤行為：**
因一次客戶專名拼寫糾正，重寫整套研究方法論，並新增 12 個僅適用該客戶的強制步驟。

**為何壞：**
把 C/局部偏好當成全局 B；無升級門檻；主路徑被污染。

### Example 4 — Boundary（D 類需求變更）
**信號：**
人類：目標從「競品調研」改為「只做定價對比」。

**正確行為：**
- 判 D：先改 Scope/DoD
- 再評估是否需要 Minor（刪調研分支、保留對比分支）
- 不是簡單「執行沒遵守」

---

## Escalation & uncertainty

| 情況 | 行為 |
|------|------|
| CI 不足 / 意圖不清 | Lightweight 輸出 + 問題清單；confidence=low |
| A/B 難辨 | 並行給出兩套處置，請人類點頭 |
| 高嚴重性但樣本=1 | 可 Patch/臨時硬約束，標註 「provisional」 |
| 與法定/安全流程衝突 | **停止演化主流程**；僅建議執行層遵從官方流程 |
| 用戶只要答案不要方法 | 交付任務結果；F2W 產物改為 optional brief |
| 多利益相關方優先級衝突 | 升級給人類決策，不擅自選價值 |

---

## Operating styles（允許發揮的邊界）

**可發揮（May）：**
- 抽象命名、類別合併、文檔組織、舉例方式
- 在多種等價工作流結構中選擇更清晰的一種（說明理由）
- 同時給 human-facing SOP 與 agent-facing checklist

**不可發揮（Must not break）：**
- 跳過 A/B/C/D 與升級門檻直接改主流程
- 無證據寫 core 規則
- 無版本/無 diff 的「悄悄進化」
- 用不可驗證空話替代 IF–THEN–UNTIL

---

## Final response shape（對外交付時的推薦順序）

1. **Executive summary**（模式、是否改流程、變更級別、置信度）
2. **CI & classification 摘要**（可附表）
3. **Rule candidates → 採納/不採納**
4. **Decision record**
5. **Workflow vX.Y 全文** 或 **No-update + 執行強化建議**
6. **Changelog + Validation + 未決問題**

---

## Appendix A — Quick classification checklist

- 按舊流程做仍會失敗？ → B
- 只是沒遵守已知步驟？ → A
- 僅本 case 特殊且可接受？ → C
- 目標/驗收變了？ → D
- 會反覆出現且可寫成門禁？ → 考慮升格
- 嚴重但單次？ → provisional patch + 監控
- 不能遷移？ → 別進 global

## Appendix B — Minimal stage map（無舊流程時可用）

`Intake → Clarify → Plan → Execute → Verify → Deliver → Retrospective`

將 CI 掛到階段；高頻爆破階段優先加 Gate，而非先改文風。

## Appendix C — Config（可調參數）

```text
N_threshold: 3
default_risk_posture: normal
prefer_minimum_update: true
require_validation_scenes: 2
allow_major_without_human_approval: false  # 建議 false
```

---

## Skill self-check（開跑前默念）

1. 我在學「正確步驟」還是學「如何從糾偏進化方法」？後者才是本 skill。
2. 我是否先分類再改流程？
3. 我的產出能否被版本 diff？
4. 我是否給了停止條件與驗證預期？

---

**End of Skill**
