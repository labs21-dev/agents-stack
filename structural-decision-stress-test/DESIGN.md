# Design — structural-decision-stress-test

> 狀態：設計定稿待批准（2026-07-28）。批准後進入 L1 eval 試跑。
> 來源：從使用者提供的「結構性決策壓測引擎 v2.5」框架改編為 agents-stack 標準 skill 格式。
> 定位：與 `meta-thinking-framework` / `protocol-adversarial-design` 並列的決策類 skill，聚焦「多邊利害關係人系統的進入策略壓測」。

## 0. 目標與邊界

- **目標**：對失敗成本高、不可逆的「進入策略」決策（聯盟平台、雙邊市場、跨實體合規、多方資源博弈）做結構性壓測，輸出帶護欄的選定方案 + 可執行驗證劇本 + 反事實分支樹。
- **邊界**：
  - 不是產品定義工具（那是 `meta-thinking-framework`）。
  - 不是協議競態合約工具（那是 `protocol-adversarial-design`）。
  - 不產生「最終答案」——產生的是「帶護欄的方案 + 驗證劇本」，決策靠驗證，不靠推演說服。
- **核心命題**：Delegation 不是為了省 token，是為了讓每個認知任務有獨立上下文、獨立偏見、獨立失敗模式——衝突本身就是信號。

## 1. 從原始框架保留 / 改編 / 補強清單

| 原始框架元素 | 處置 | 理由 |
|---|---|---|
| Orchestrator 只做路由與裁決 | **保留** | 本 skill 的核心設計命題 |
| 7 個專精 sub-agent | **保留** | 各帶獨立上下文，認知重活全委派 |
| Phase 0-6 依賴順序 + 並行組 | **保留** | 依賴關係正確，並行只省 wall-clock |
| 紅隊物理隔離 | **保留** | Hard rule 2，隔離是紅隊價值來源 |
| 衝突裁決優先序 | **保留** | 寫進 `references/conflict-adjudication.md` |
| 記憶庫 schema | **保留** | 寫進 `references/memory-bank.md` + `templates/manifest.yaml` |
| TOML `[skill]` config block | **剝除** | agents-stack 用 YAML frontmatter（`name` + `description`），無 TOML config |
| `max_tokens_per_phase = "unlimited"` 等約束 | **剝除** | 非 skill 格式欄位，屬運行環境政策 |
| 7 個 sub-agent prompt 全塞主檔 | **改編**：移到 `references/sub-agents.md` | 對齊 repo progressive disclosure 慣例（SKILL.md 只放觸發+flow+契約） |
| 無降級機制 | **補強**：新增 `references/degradation-checkpoint.md` | 小題大作也是損耗；對齊 meta-thinking 的降級 checkpoint 哲學 |
| 無失敗模式自檢 | **補強**：新增 `references/failure-patterns.md` | 對齊 repo 慣例（agentic-clean / coding-docs 都有） |
| 無 sibling split | **補強**：新增與既有 skills 的分工表 | 避免觸發重疊，對齊 protocol-adversarial / refactor-review 慣例 |
| 無 self-loop | **補強**：新增 Self-loop 段 | 對齊 meta-thinking / agentic-clean 慣例 |

## 2. Delegation 拓撲的設計取捨

### 為什麼是 7 個 sub-agent 而非單一長 prompt

單一 prompt 處理複雜多邊決策時，會出現三個衰減：
1. **上下文稀釋**：七個認知任務擠一個 context window，後段任務被前段噪聲蓋過。
2. **偏見同源**：同一個 prompt 產生的所有結論共享同一組偏見，矛盾不會湧現——而矛盾正是信號。
3. **失敗模式耦合**：一個任務失敗拖垮全部，無法定位是哪個認知層漏了。

拆成 7 個獨立 sub-agent，每個帶獨立 context 與偏見，衝突才會浮現供 Orchestrator 裁決。

### 為什麼紅隊要物理隔離

紅隊若讀到博弈模擬（game_simulator）的輸出，會被主線敘事收編——開始替「已推演出的均衡」找護欄，而非攻擊它。隔離讓紅隊保持「只看實體定義與方案描述」的純粹攻擊視角。這是本 skill 最容易被破壞的設計（見 `failure-patterns.md`），因此列為 Hard rule 2。

### 為什麼用來源可信度做裁決優先序

`red_team > game_simulator > lens_analyst > entity_modeler` 的排序邏輯：
- **紅隊**以失敗為目標、隔離運行，最不易被主線收編。
- **博弈模擬**揭示互動層湧現（單點視角看不到的）。
- **鏡頭分析**是單點視角，深度高但無互動層。
- **實體建模**是結構骨架，最穩定但也最靜態。

不可逆風險壓過成本（規則 2）、平台動態壓過經濟學（規則 3）是對來源排序的情境修正。

### 為什麼允許降級走簡化鏈

並非每個進入策略決策都涉及雙邊市場 + 跨法人合規。對低複雜度決策跑完整七層是損耗。降級條件（無雙邊、無合規分歧、無跨法人、無持續博弈）全部滿足才降級，且必須顯式標記——靜默省略會讓讀者誤以為跑過完整壓測（見 `degradation-checkpoint.md`）。

## 3. 與既有 skills 的引用關係

| 需求 | Skill | 關係 |
|------|-------|------|
| 連問題本質都還沒拆清楚 | `meta-thinking-framework` | **上游**：先跑 meta-thinking 產出核心變數，再進入本 skill Phase 0/1 |
| 協議競態 / 狀態機合約 | `protocol-adversarial-design` | **旁支**：若本 skill Phase 2 的承重實體狀態機涉及競態合約，可委派 |
| 信任 AI 生成程式碼 | `agentic-clean-discipline` | **下游**：本 skill 產出方案後若需實作，走 agentic-clean 的 gate 鏈 |

本 skill 的 Phase 1 鏡頭分析與 `meta-thinking-framework` 同源（六鏡 + 變數驅動額外鏡頭 + 反事實對比法引入規則）。這是有意的重用，不是重複——本 skill 在鏡頭之上加了時間維度（T+0/6m/12m/24m）與下游的實體/博弈/紅隊層。

## 4. 結構

```
templates/.agents/skills/structural-decision-stress-test/
  SKILL.md                       ← 觸發描述 + hard rules + flow + 輸出契約 + sibling split + self-loop
  DESIGN.md                      ← 本文件
  references/
    sub-agents.md                ← 7 個 sub-agent 完整 prompt
    conflict-adjudication.md     ← 衝突裁決優先序 + 採信規則
    memory-bank.md               ← 記憶庫 schema + 跨決策重用規則
    failure-patterns.md          ← 本 skill 失敗模式自檢
    degradation-checkpoint.md    ← 何時降級走簡化鏈 + 反降級信號
  templates/
    input-spec.md                ← Phase 0 輸入規格
    stop-output.md               ← NO-GO 終止報告
    manifest.yaml                ← 記憶庫 manifest
    final-report.md              ← 最終報告骨架
    h-playbook.md                ← 驗證劇本骨架
    branch-tree.md               ← 反事實分支樹骨架
  evals/
    evals.json                   ← L1 評估用 test prompts
```

## 5. 運行環境相依性

本 skill 的 sub-agent dispatch 依賴運行環境是否支援 sub-agent 機制：
- **支援 sub-agent 的環境**（如 Claude Code 的 Agent tool、ARC 的子 agent）：可原生跑完整 delegation 拓撲，並行組可真正並行。
- **不支援的環境**：Orchestrator 可在單一 context 內「模擬」delegation——逐個 sub-agent 換脈絡執行（如分段提示自己切換角色）。並行組退化為順序跑。依賴關係不變，只損失 wall-clock 與部分上下文隔離強度。

此相依性在 SKILL.md 的 Delegation 拓撲段已說明。不支援 sub-agent 的環境下，紅隊隔離強度會下降——這是已知限制，使用時應知會。

## 6. 待驗證假設 + 驗證方法論

1. **7 個 sub-agent 的劃分是否認知正交** → 跑 `evals/evals.json` 的 eval，檢查每個 sub-agent 是否真的產出「其他 sub-agent 產不出」的內容。若 game_simulator 與 lens_analyst 輸出高度重疊 → 劃分需合併。
2. **衝突裁決規則在實戰中可裁定** → 跑 eval 收集衝突案例，看三條規則是否覆蓋所有衝突。出現「三條都無法裁定」的頻率過高 → 規則需補。
3. **降級條件不會誤降高複雜度決策** → 跑 eval，檢查被降級的決策是否真的低複雜度。誤降 → 條件需收緊。
4. **紅隊攻擊腳本真的可執行** → 拿 eval 產出的 red_team 腳本，由人類判斷「能否真的拿去問律師/投資人」。停留空泛 → sub-agent prompt 需強化具體性要求。
5. **sub-agent 機制不存在的環境下，模擬 delegation 仍有效** → 在無 sub-agent 環境跑一次完整鏈，比較輸出品質與有 sub-agent 環境的差距。差距過大 → 需明確標示環境限制或調整 prompt。

## 7. 反身性自檢

本 skill 是決策類 meta-skill，受反身性威脅。自檢：
- 本 skill 的「好決策壓測標準」是否自生？→ 部分借 `meta-thinking-framework` 已驗證的六鏡骨架（外部 anchor），非全自生。
- 但本 skill 的 delegation 拓撲與衝突裁決規則未經獨立 eval 驗證（N=1 設計）——誠實標記。`evals/evals.json` 是第一個外部 anchor。
- Self-loop + 記憶庫 corrections_log 是本 skill 對自己的反身性防禦——推演不準時定位是哪個 sub-agent 漏了，而非整個推翻。
- L1 eval 指標須與 L2 真實決策事後驗證雙向校準（對齊 skill-creator 的反身性防線）：eval 高分但實戰決策仍翻車 → eval 劇場，需修正 eval 指標。