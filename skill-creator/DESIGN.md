# Design — skill-creator（runtime-agnostic 版）

> 狀態：設計定稿待批准（2026-07-22）。批准後才實作 scaffold 檔。
> 來源：從官方 `skill-creator`（claude-plugins-official marketplace）改編，剝除 Claude-specific 綁定。
> 定位：與 `skill-evolution` 並列的獨立 skill。本 skill 負責 L0 生成 + L1 評估；skill-evolution 負責 L2 演化 + L3 累積。兩者透過文件互相引用，各自可單獨用。

## 0. 目標與邊界

- **目標**：一個獨立存在於 agents-stack 的 skill-creator，指導如何造 skill、量測其品質、迭代改進——**不綁定 Claude Code 或任何特定 agent runtime**。
- **邊界**：
  - 不依賴 `claude -p`、`.claude/commands/`、Claude stream-json 協議、Claude.ai/Cowork 等任何 Claude 專屬介面。
  - 觸發 eval 那層抽象成 **runner adapter interface**，不預設任何 runtime 的實作。
  - 對齊 ARC `mechanism not policy`：提供機制與介面，runtime 綁定由使用者接。
- **與官方版關係**：改編自官方 skill-creator 的 runtime-agnostic 部分（skill 結構規範、evals.json schema、grading、improvement loop、packaging）。Claude-specific 部分（觸發偵測實作、環境分支）剝除或抽象化。

## 1. 從官方版保留 / 剝除 / 改編清單

| 官方元素 | 處置 | 理由 |
|---|---|---|
| skill 結構規範（frontmatter + SKILL.md + references/templates 漸進揭露） | **保留** | runtime-agnostic，是 skill 格式事實標準 |
| evals.json / history.json schema | **保留**（微調用語） | runtime-agnostic 資料格式 |
| grading（expectation pass rate、比較現任 vs 挑戰者） | **保留** | 評估邏輯與 runtime 無關 |
| improvement loop（draft → test → review → improve → repeat） | **保留** | 方法論與 runtime 無關 |
| packaging（`.skill` 打包） | **保留**（路徑中性化） | 與 runtime 無關 |
| description 優化的「pushy」理由（Claude undertrigger） | **改編** | 理由換成中性「LLM 普遍 undertrigger skills」 |
| "Claude/plumbers" 語氣段 | **剝除** | 與機制無關 |
| `run_eval.py` 的 `claude -p` + stream-json + `.claude/commands/` | **剝除實作，抽象成 adapter interface** | Claude 專屬協議 |
| Claude.ai-specific / Cowork 環境分支 | **剝除** | 改成單一 runtime-agnostic 流程 + adapter 接點 |
| description 自動優化 loop（`run_loop.py` 呼叫 `claude -p`） | **改編**：邏輯保留（train/test split、迭代、HTML 報告），觸發偵測層走 adapter | runtime-agnostic 邏輯 + 可替換偵測層 |

## 2. Runner Adapter Interface（去綁定的核心）

官方版把「跑 query 偵測是否讀 skill」硬編碼成 `claude -p` + 解析 stream event。本設計把這層抽象成 adapter 介面，任何 agent runtime 各自實作。

### Adapter 契約

一個 runner adapter 必須提供一個函式（實作形式不限：腳本、子行程、API 呼叫）：

```
run_query_with_skill(query, skill_name, skill_description) → { triggered: bool, evidence: str }
```

- **輸入**：使用者 query、skill 名稱、skill description。
- **輸出**：
  - `triggered`：agent 是否「讀取/諮詢」了這個 skill（bool）。
  - `evidence`：偵測依據的人類可讀描述（哪個事件、哪個工具呼叫、哪行 log）——用於審計與 debug。
- **不規定偵測方式**：不同 runtime 各異（Claude Code = stream event tool_use；Cursor = rules 讀取；ARC = `<SKILLS>` 注入 + skill 載入事件；自製 agent = 自訂 hook）。adapter 自決。

### 預設不實作

本 skill **不隨附任何 adapter 實作**——只定義契約。理由：
1. 對齊 mechanism-not-policy：提供介面，不預設 policy。
2. 避免重新引入綁定（附一個 Claude adapter 等於綁回 Claude）。
3. adapter 是使用者的環境知識，不該由 skill 猜。

adapter 實作以範例文件形式提供（`references/adapter-examples.md`），標註為「example, not shipped」——示範 Claude Code / ARC / 通用手動 三種接法，但不進核心。

## 3. 手動 eval fallback（繞過自動偵測）

即使沒有 adapter，本 skill 仍可用——提供一條**手動 eval 路徑**：

- evals.json 同官方格式。
- 跑法：使用者（或外部腳本）在自己的 runtime 跑 query，**人工或外部腳本填 `triggered` 結果進結果 JSON**。
- grading/improvement loop 吃這個結果 JSON，邏輯不變。

這條路徑確保「無 adapter 也能實際跑 eval」，不會拿到手不能動。自動 adapter 是加速器，不是必要條件。

## 4. 結構

```
templates/.agents/skills/skill-creator/        ← 與 skill-evolution 並列
  SKILL.md                       ← 造 skill 總覽 + 觸發 + L0生成/L1評估流程
  DESIGN.md                      ← 本文件
  references/
    skill-anatomy.md             ← skill 結構規範（frontmatter/SKILL.md/references/templates 漸進揭露）
    evals-schema.md              ← evals.json / history.json schema（從官方改編，中性化）
    improvement-loop.md          ← draft→test→review→improve 流程 + grading 規則
    packaging.md                 ← .skill 打包格式（路徑中性化）
    runner-adapter.md            ← adapter 契約定義（本設計 §2）
    adapter-examples.md          ← Claude Code / ARC / 手動 三種接法範例（標 example, not shipped）
    description-tuning.md        ← description 優化（中性用語 + adapter 接點）
  templates/                     ← 可複製
    skill-skeleton/              ← 新 skill 骨架（SKILL.md + references/ + templates/）
    evals.json                   ← evals 檔模板
```

> scripts/ 是否需要：官方版有 8 個 Python 腳本。本設計**先不隨附腳本**——grading/improvement 邏輯先以文件 + 資料格式描述，需要時再以 runtime-agnostic 方式實作（或留給使用者）。理由：腳本最容易藏 runtime 綁定，且 Phase 1 先驗證流程可跑，工具化是後續。

## 5. L0 生成 + L1 評估流程

### L0 生成
1. **Capture intent**：skill 該讓 agent 做什麼？何時觸發？預期輸出格式？是否設 test cases？（主觀輸出 skill 可免 test）
2. **Interview & research**：edge cases、輸出入格式、範例檔、成功判準、依賴。
3. **Draft**：用 `skill-skeleton` 模板寫 SKILL.md + references/templates。frontmatter description 包含「做什麼 + 何時用」。
4. **前置 gate**（對齊 meta-skill 設計）：「重複 ≥N 次的需求才值得造 skill」——避免過度生成。

### L1 評估
1. **寫 evals**：用 `evals.json` 模板，每個 eval = prompt + expected_output + expectations（可驗證語句）+ 選配 files。
2. **跑 eval**：經 runner adapter（自動）或手動路徑，每 query 跑 ≥3 次取觸發率。
3. **Grade**：比對 expectations，算 pass rate；比較「現任 description vs 挑戰者」。
4. **Review**：產結果摘要給人類看（自動 adapter 可產 HTML 報告；手動路徑在對話內呈現）。
5. **Improve**：人類回饋 + 量化結果 → 改 skill → 重跑。迭代至滿意。
6. **指標↔真實案例雙向校準**（對齊 meta-skill L1）：eval 指標必須對齊 L2 真實使用事後驗證；指標與案例雙向校準防 eval 劇場。

## 6. 與 skill-evolution 的引用關係

兩者獨立並列，透過文件引用：
- 本 skill 的 L1 eval 提供**品質信號**；skill-evolution 的 L2 用**真實案例事後驗證**校準這些信號（§5 step 6）。
- 本 skill 的 `improvement-loop.md` 是**人類驅動短週期迭代**（單次 session 內）；skill-evolution 是**案例驅動長週期演化**（跨 session）。兩者層次不同、互補。
- 一個 skill 的完整生命週期：用本 skill 造 + 短週期打磨（L0-L1）→ 部署使用 → 用 skill-evolution 收案例演化（L2-L3）。

引用是鬆耦合：兩 skill 各自可單獨用，不需要同時掛載。

## 7. 去綁定自檢

本 skill 聲稱 runtime-agnostic，自檢：

| 檢查 | 結果 |
|---|---|
| 是否任何檔案提及 `claude -p` / `.claude/` / `claude.ai` / Cowork / Anthropic SDK？ | 設計層面：無（僅 adapter-examples.md 範例示範接法，標 example）。實作時逐檔 grep 驗證。 |
| 觸發偵測是否可在非 Claude runtime 跑？ | 是——經 adapter；無 adapter 時走手動路徑。 |
| 是否預設某 runtime 的 skill 發現機制？ | 否——skill-anatomy 描述結構，不描述特定 runtime 如何注入。 |
| scripts 是否隱藏 runtime 呼叫？ | Phase 1 不隨附 scripts，規避此風險。 |

## 8. 實作階段（批准後）

- **Phase 1**：建 `skill-creator/` scaffold——SKILL.md + references（skill-anatomy / evals-schema / improvement-loop / packaging / runner-adapter / adapter-examples / description-tuning）+ templates（skill-skeleton / evals.json）。全為 md + 模板，無腳本。
- **Phase 2**：對一個既有 skill（如 meta-thinking-framework）回推示範——用本 skill 的 evals 格式寫幾個 eval，走手動路徑跑一次，驗證流程可跑、格式可用。
- **Phase 3**：視需求決定是否實作 runtime-agnostic grading 腳本（純資料處理，不呼叫 runtime）。
- **Phase 4（與 skill-evolution 共建）**：L1 指標 ↔ L2 案例雙向校準的具體機制。

## 9. 待驗證假設 + 驗證方法論

1. **adapter 介面足以涵蓋主要 runtime 的觸發偵測** → 拿 Claude Code / Cursor / ARC 三種，各自寫 adapter 草稿，看 `run_query_with_skill` 契約是否夠表達。某 runtime 無法 fit → 介面需擴。
2. **手動 eval 路徑實際可跑且負擔可接受** → Phase 2 在 meta-thinking-framework 上跑 3 個 eval，量測人工填 triggered 的負擔。過重 → 需提供更強的半自動工具。
3. **description 優化 loop 在去綁定後仍有效** → 原版靠 `claude -p` 反覆跑。去綁定後改走 adapter/手動，是否仍能收斂出更好的 description。Phase 2-3 驗證。
4. **無腳本（純 md）的 scaffold 對使用者夠用** → Phase 2 示範跑後，看是否多數使用者仍需腳本才能跑起來。是 → 提前 Phase 3。

## 10. 反身性自檢

本 skill 也是 meta-skill（造 skill 的 skill），受反身性威脅。自檢：
- 本 skill 的「好 skill 標準」是否自生？→ 部分借官方 skill-creator 已驗證設計（外部 anchor），非全自生。
- 但本 skill 未經獨立 eval 驗證（N=1 設計）——誠實標記。Phase 2 用既有 skill 回推示範，是第一個外部 anchor。
- L1 指標↔L2 案例雙向校準（§5 step 6）是本 skill 對自己的反身性防禦——eval 指標不能只自己跟自己比，要用 L2 真實案例外部校準。