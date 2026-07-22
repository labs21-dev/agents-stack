# Design — skill-evolution（meta-skill 進化機制）

> 狀態：設計定稿待批准（2026-07-22）。批准後才實作 scaffold 檔。
> 母分析：本對話以 meta-thinking-framework v2 跑的「meta-skill 系統元素與設計」分析。
> 起點：方案 B（扁平 skill-creator + 可選演化套件）→ 目標演化向 A（完整四層 stack）。

## 0. 目標與邊界

- **目標**：給任何 skill 一個可選附掛的進化能力——收集案例 → 累積證據 → 達門檻 → AI 提議升格 patch → 人類批准 → 升格（對稱下架）。作為 `skill-evolution` skill + 可複製模板雙軌。
- **邊界**：
  - 不修改官方 `skill-creator` 本體（外部依賴，plugin marketplace）。
  - 不碰 skill-creator 的 eval loop——進化層附加其上，eval 仍人類驅動。
  - 對齊 ARC `mechanism not policy`：提供機制，skill 自決是否掛載。
- **可逆性**：中。單 skill 可回退；但 meta-criteria 若錯，汙染面廣 → 偏好可選附掛、保守升格、before-snapshot 可回退。

## 1. 四層模型（B 起點做到哪、A 目標補哪）

| 層 | 職責 | B 階段 | A 目標 |
|---|---|---|---|
| **L0 生成** | intent → skill draft | 借官方 skill-creator，不重造 | 同 |
| **L1 評估** | 量測 skill 品質 | 借官方 skill-creator eval；**加指標↔真實案例雙向校準** | 完整雙向校準機制 |
| **L2 演化** | 案例 → 升格/下架 | **本 skill 主體** | 同 + 更強 patch 工具 |
| **L3 元標準** | 定義「什麼是好 skill」 | **輕量 accumulate-only**（compound/ 收案例，人類獨佔立法權，只 accumulate 不 legislate） | 跨 skill 收斂 N≥3 → 人類立法折進 constitution |

> B 階段不強行做完整 L3——反身性鏡頭指出 L3 必須有外部 anchor，而外部 anchor 要靠跨 skill 案例累積才能形成。現在硬建 L3 = 自生標準 = 反身性失敗。故 B 階段只 accumulate，案例夠了再正式化立法。

## 2. 反身性防禦（結構必要，非偏好）

核心洞察（emerging lens：反身性/自舉）：meta-skill 用自己的標準評自己的產出 → **自我驗證平庸化**——品質單調漂移到 self-consistent but mediocre，無外部信號打斷。

**因此本設計的硬界線**：
- L3 立法權**人類獨佔**（AI 只 accumulate、只 flag、只 draft patch）。
- 案例須**被動收集 + 事後驗證**，非 AI 自評（防偽案例灌水）。
- 升格 patch **AI draft、人類 gate**（AI 不自改作業系統）。
- L3 種子標準**不自生**——冷啟動錨點為已運作的 `emerging-lenses-log` 經驗（門檻、畢業 gate 已在 meta-thinking-framework 上實跑）+ 跨 case 自收斂，不發明新標準。

## 3. 雙軌形狀

```
templates/.agents/skills/skill-evolution/        ← 規範與流程集中處（skill）
  SKILL.md                       ← 進化機制總覽 + 觸發 + 升格流程
  DESIGN.md                      ← 本文件
  references/
    evolution-protocol.md        ← 升格/下架流程 + 風險分級 + 門檻
    patch-draft-format.md        ← AI 升格 patch 格式規範
    l3-accumulate.md             ← 輕量 L3 accumulate-only 規範
  templates/                     ← 可複製附掛進任何 skill
    evolution-log.md             ← 案例累積 log（被掛載 skill 用）
    evolution-attach.md          ← 給被掛載 skill 的 SKILL.md 附掛片段（說明如何收案例、何時 flag）

任意被掛載的 skill/  （如 meta-thinking-framework/）
  references/
    evolution-log.md             ← 從模板複製，就地累積該 skill 的案例
  SKILL.md                       ← 附掛 evolution-attach 片段（指向 skill-evolution 規範）
```

**雙軌理由**：
- **skill 軌**——規範與流程集中、單一真理、可隨使用演化（改一處所有掛載 skill 受益）。
- **模板軌**——每個被掛載 skill 就地有自己的 `evolution-log.md`（案例是該 skill 私有資料），自包含、無跨 skill 執行期依賴（只在規範層引用 skill-evolution）。

## 4. 升格流程（狀態機）

```
IDLE(被動收集案例)
  → 案例 ≥N 次 且 ≥1 次事後驗證有效      → FLAG(升格候選)
  → 案例 反效果 ≥M 次                    → FLAG(下架候選)
FLAG
  → AI 產具體 patch（scope 限定 + diff + 證據摘要 + 風險標籤 + before-snapshot 指令）
  → DRAFTED
DRAFTED
  → 人類 review：批准 / 退回 / 改         → APPROVED | REJECTED
APPROVED
  → 套用 patch + 留 before-snapshot + 寫 changelog
  → MERGED
MERGED
  → 下一輪真實使用驗證升格是否讓輸出更銳利
  → 退步則回退 before-snapshot
REJECTED
  → 回 IDLE；或反效果持續 → 進 DEPRECATE
```

**雙向**：升格與下架對稱。案例反覆打臉既有規則 → 下架流程（同一狀態機，FLAG 觸發條件不同）。

## 5. 升格門檻

- **升格候選**：單一規則/鏡頭/觸發的**有效案例 ≥3 次**，**且**其中 **≥1 次事後驗證有效**（非自評）。
- **下架候選**：**反效果案例 ≥3 次**。
- **門檻理由**：純頻率會誤升「常用但無效」的規則；雙門檻（頻率 + 驗證）擋偽案例。
- **門檻可調**：N/M 是初始值，本身也是 evolution-log 累積對象——若驗證發現門檻過鬆/過緊，作為 L3 議題 accumulate。

## 6. 風險分級（決定 gate 鬆緊）

| 改動類型 | 風險 | Gate 鬆緊 | before-snapshot |
|---|---|---|---|
| 加範例、補觸發條件、補範例段 | 低 | 批次快速審 | 建議 |
| 升格候選鏡頭/規則進標準集 | 中 | 逐個審 | 必須 |
| 改核心規則、下架既有規則 | 高 | 逐個嚴審 + 雙人確認 | 必須 |

## 7. L3 accumulate-only（B 階段）

- 在 `skill-evolution/` 下設 `compound/`（或參數化路徑）：
  ```
  compound/
    INDEX.md          ← 案例索引（一 case 一行，AI auto-append）+ recurring-patterns 區（人類 only）+ legislation-log（人類 only）
    {date}-{slug}/
      CASE.md         ← 跨 skill 收斂的單一議題記錄（如「反身性鏡頭是否該畢業」）
      input.txt       ← 證據（territory beside map）
  ```
- **寫入界線**（common-law loop 的 accumulate/legislate 分離）：
  - INDEX cases-list：AI auto-append（additive、reversible）。
  - INDEX recurring-patterns / legislation-log：**人類 only**（這是 N≥3 收斂決策點；AI auto-fill = AI 立法 = 違反反身性防禦）。
  - CASE.md：AI 寫一次後 frozen（additive only）。
- **B 階段只 accumulate**：AI 收案例、寫 CASE.md、在 CASE.md 內 flag 候選 pattern（`Flags for human立法` 欄）。**不 legislate**——摺進 constitution 是人類動作，留到 A 階段正式化。

## 8. AI patch 權限界線（對齊你的裁決）

- **AI 可**：被動收案例、flag 達門檻候選、產具體升格 patch（diff + scope + 證據 + 風險標籤 + 可逆性 + before-snapshot 指令）。
- **AI 不可**：自行套用 patch、改 L3 constitution、auto-fill recurring-patterns / legislation-log、自評案例有效（須事後驗證）。
- **人類**：review patch、批准/退回/改、執行套用、立法。

## 9. 與既有 skill 的關係

- **官方 skill-creator**：L0/L1 借用它，不修改。本 skill 是其進化層補充。
- **已刪的 extract-methodology**：本 skill 的 L3 accumulate-only 機制血緣上源自一個更早的 extract-methodology skill（已刪——無 live consumer、N=1 未校準、其唯一有價值的 common-law loop 已被本 skill 吸收）。血緣註記於 `l3-accumulate.md`，無運行期依賴。
- **meta-thinking-framework**：第一個掛載 evolution scaffold 的示範 skill（其 `emerging-lenses-log.md` 已是 evolution-log 的運作雛形）。

## 10. 實作階段劃分（批准後）

- **Phase 1**：建 `skill-evolution/` scaffold——SKILL.md + references（evolution-protocol / patch-draft-format / l3-accumulate）+ templates（evolution-log / evolution-attach）+ compound/ INDEX 種子。
- **Phase 2**：把 meta-thinking-framework 作為首個掛載示範——其 `emerging-lenses-log.md` 對齊 evolution-log 格式、SKILL.md 附掛 evolution-attach 片段。
- **Phase 3**：跑 3-5 次真實進化事件，校準門檻 N/M、驗證被動收集負擔、驗證 patch-draft 格式可讀性。累積 compound/ CASE.md。
- **Phase 4（A 目標）**：案例夠後，正式化 L3——跨 skill 收斂 N≥3 → 人類立法 → 折進 constitution。此為後續，不在本次實作。

## 11. 待驗證假設 + 驗證方法論

1. **被動案例收集不造成顯著負擔** → 在 meta-thinking-framework 上跑 5 次真實分析，量測每次多耗 token/步驟。超過 skill 本身價值的 10% 則需減重。
2. **頻率+驗證雙門檻擋偽案例** → 回查 emerging-lenses-log 首兩筆（機制一致性、反身性），看「事後驗證」欄能否被客觀填寫，還是退化成自評。退化 → 需外部驗證來源。
3. **L3 冷啟動錨點（emerging-lenses-log 經驗）足以度冷啟動** → 拿 meta-thinking-framework v2 回推其 L3 標準，看能否從已運作的 emerging-lenses-log 經驗推出，還是得另覓外部 anchor。後者 → 種子需換。
4. **N=3 / M=3 門檻合宜** → Phase 3 累積後量測：過鬆（誤升）或過緊（該升未升）則調。

## 12. 反身性自檢（本設計對自己）

本設計本身是 meta-skill，受反身性威脅。自檢：
- 本設計的「好進化機制標準」是否自生？→ 否：L3 種子借已運作的 emerging-lenses-log 經驗 + 跨 case 自收斂，門檻值借其已實跑經驗，非憑空發明。
- 本設計是否用自己標準評自己？→ 部分：Phase 3 驗證即外部 anchor（真實使用事後驗證）。但本設計未經 N≥3 跨 skill 收斂，**目前是 N=1 設計**——誠實標記，需 Phase 3-4 累積才算定案。