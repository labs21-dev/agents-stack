---
name: structural-decision-stress-test
description: >-
  對「進入策略」類決策做多代理人結構性壓測——聯盟平台、雙邊市場、跨實體合規、多方資源博弈這類失敗成本高且不可逆的「還沒想清楚就要做決定」場景。輸出帶護欄的選定方案 + 可執行驗證劇本 (H-PLAYBOOK) + 反事實分支樹。機制：Orchestrator 只做路由與衝突裁決，七個專精 sub-agent（redliner 快速否決、lens_analyst 動態演化鏡、entity_modeler 承重實體狀態機、game_simulator 多輪博弈、red_team 隔離紅隊、branch_explorer 反事實分支、playbook_writer 驗證劇本）各帶獨立上下文與偏見執行認知重活，衝突本身就是信號。當使用者要驗證「某個方向的進入策略」、面對多邊利害關係人系統、需要降級/否決紅線、博弈湧現、紅隊攻擊腳本、或分支切換條件時使用。不適用於目標明確的執行任務、單一產品定義、純技術架構題、協議競態合約（用 protocol-adversarial-design）、或可輕易回滾的低風險決策（用 meta-thinking-framework）。
---

# Structural Decision Stress Test（結構性決策壓測引擎）

針對複雜多邊利害關係人系統的**進入策略**決策，進行高保真結構性壓測。

**對象**：要在失敗成本高、不可逆的情境下做進入策略選擇的決策者（獨立創辦人 / 小團隊 / 聯盟發起人）。

**Spirit**：Orchestrator 是交通警察，sub-agents 是專家證人。Delegation 不是為了省 token，是為了讓每個認知任務都有獨立的上下文、獨立的偏見、獨立的失敗模式——當它們衝突時，衝突本身就是信號。

## 何時觸發

使用者的請求符合以下任一特徵時啟動：
- 要驗證的是「**某個方向的進入策略**」，不是產品功能定義、不是執行任務
- 決策橫跨**多邊利害關係人**（錨點 vs 創辦人 / 監管 vs 平台 / 雙邊市場的兩側），存在抵抗與博弈
- 失敗成本高、不可逆（監管認定、跨法人資金流、控制權讓渡）
- 需要「**先否決再分析**」的紅線快篩（資源錯配、致命不可逆、零吸引力冷啟動）

**不要用在**：
- 目標明確的執行任務（寫 code、翻譯、查資料）
- 單一產品定義 / 模糊多鏡頭決策 → `meta-thinking-framework`
- 純技術架構題、協議競態合約 → `protocol-adversarial-design`
- 可輕易回滾的低風險決策 → 直接決定，不必壓測

## Hard rules

1. **Redliner 先跑。** 三條紅線任一觸發 NO-GO → 終止，不進入後續 phase。不要對已否決方向做美化分析。
2. **紅隊物理隔離。** `red_team` 不讀 `game_simulator` 輸出，避免被主線邏輯污染。隔離是它的價值來源。
3. **Orchestrator 不做認知。** 只做輸入翻譯、路由 dispatch、衝突裁決、記憶庫寫入。分析重活全委派。
4. **每層結束產出 H-PLAYBOOK。** 決策不靠推演說服，靠可執行驗證劇本。沒有 playbook 的結論不可交付。
5. **衝突不藏進整合。** 當 sub-agent 輸出矛盾時，明確列出矛盾、採信誰、為什麼。不把衝突抹平成「綜合方案」。
6. **時間預算可降級。** 複雜度低（無雙邊、無合規分歧、無跨法人）→ 允許跳過 Phase 3/4 並行組，走簡化鏈。小題大作也是損耗。

## Flow（每次調用）

### 0. 輸入翻譯（Orchestrator）

從使用者對話提取並填入 `templates/input-spec.md`：

- **DECISION_QUESTION**：要驗證的決策是什麼？（進入策略選擇，不是產品定義）
- **RESOURCE_PROFILE**：`{team_size, funding_stage, time_budget_weeks, core_competency}`
- **BOUNDARY_CONDITIONS**：`[不可妥協項, 可逆項, 不可逆項]`
- **KNOWN_EVIDENCE**：使用者已提供的證據（一律標記為「待驗證」）
- **TARGET_AUDIENCE**：決策最終消費者是誰（投資人 / 合夥人 / 自己）

### Phase 0 — Redliner（快速否決，可與 Phase 1 並行）

Dispatch `references/sub-agents.md` § redliner。只讀 `decision_question` + `resource_profile`，不依賴 lens。

- 回傳 `GO` / `NO-GO` / `DEGRADE`。
- **NO-GO** → 輸出終止報告（`templates/stop-output.md`）+ 降級建議，**結束**。不進入後續 phase。
- **DEGRADE** → 採納降級方向，重寫 DECISION_QUESTION 後續跑。
- **GO** → 繼續。

### Phase 1 — Lens Analyst（動態演化鏡，與 Phase 0 並行）

Dispatch `references/sub-agents.md` § lens_analyst。執行六鏡 + 變數驅動額外鏡頭，在 T+0 / T+6m / T+12m / T+24m 四個時間點重新評估。回傳 Top-2~3 變數 + 候選方案 + 額外鏡頭觸發清單 + 鏡頭衝突。

### Phase 2 — Entity Modeler（依賴 Phase 1）

Dispatch `references/sub-agents.md` § entity_modeler，餵入 Phase 1 的 Top 變數 + 額外鏡頭。輸出承重實體狀態機 + 瓶頸依賴鏈 + 冷啟動錨點 + 角色膨脹熱點。

### Phase 3 — Game Simulator（依賴 Phase 1/2，與 Phase 4 並行）

Dispatch `references/sub-agents.md` § game_simulator，餵入 Phase 1/2。多輪序貫博弈，每輪更新各 agent 信念，每 3 輪插入混沌事件。輸出博弈日誌 + 湧現模式 + 降級陷阱偵測。

### Phase 4 — Red Team（依賴 Phase 1/2，與 Phase 3 並行，**隔離**）

Dispatch `references/sub-agents.md` § red_team，**只餵入 Phase 1/2，不餵入 Phase 3**。四個並行攻擊模式（LEGAL / COMMERCIAL / TECHNICAL / NARRATIVE）。輸出可拿去問真實律師 / 投資人的攻擊腳本。

### Phase 5 — Branch Explorer（依賴 Phase 1-4）

Dispatch `references/sub-agents.md` § branch_explorer，餵入全部。主幹 + α/β/γ/δ 反事實分支，每分支跑簡化 3 輪，輸出分支切換矩陣。

### Phase 6 — Playbook Writer（依賴全部）

Dispatch `references/sub-agents.md` § playbook_writer，餵入全部。產出 H-PLAYBOOKs（開場白 + 核心試探 + 壓測問題 + 通過/失敗標準 + 成本 + 回退路徑）+ 護欄條款。

### 衝突裁決（Orchestrator）

當 sub-agent 輸出矛盾，按 `references/conflict-adjudication.md` 優先序採信。把裁決寫進最終報告的「衝突登記」區，不抹平。

### 記憶庫寫入

每個 phase 結束寫入 `templates/manifest.yaml` schema。最終彙整成 `templates/final-report.md`。

## Delegation 拓撲

```
ORCHESTRATOR (路由 + 裁決 + 記憶庫)
   ├─ Phase 0 redliner ─┐
   ├─ Phase 1 lens_analyst ─┘ (並行)
   ├─ Phase 2 entity_modeler (依賴 P1)
   ├─ Phase 3 game_simulator ─┐
   ├─ Phase 4 red_team (隔離) ─┘ (並行)
   ├─ Phase 5 branch_explorer (依賴 P1-4)
   └─ Phase 6 playbook_writer (依賴全部)
        │
        ▼
   MEMORY BANK /decisions/{YYYYMMDD}_{slug}/
```

並行策略：Phase 0 & 1 可並行；Phase 3 & 4 可並行（紅隊隔離）；其餘順序依賴。若運行環境不支援 sub-agent 並行，順序跑亦可——並行只省 wall-clock，不改變依賴關係。

## Required output

每次完成（非 NO-GO 終止）必須包含：

1. **EXECUTIVE_SUMMARY** — 一句話結論
2. **REDLINER_VERDICT** — GO/DEGRADE + 觸發紅線（若有）
3. **SELECTED_BRANCH** — 主幹或哪條反事實分支
4. **LOAD_BEARING_ENTITIES** — 承重實體 + 狀態機摘要
5. **EMERGENT_PATTERNS** — 博弈湧現 + 偵測到的降級陷阱
6. **RED_TEAM_ATTACKS** — 四份攻擊腳本摘要 + 致命性標記
7. **GUARDRAILS** — 護欄條款清單
8. **H_PLAYBOOKS** — 驗證劇本清單
9. **CONFLICTS_LOG** — 衝突登記（無衝突則明說「無衝突」）
10. **CORRECTIONS_LOG** — 本次推演修正了前次記憶庫中的哪些假設
11. **NEXT_DECISION_TRIGGERS** — 哪些驗證結果會觸發重新推演 / 切換分支

NO-GO 終止只需：觸發紅線、否決理由、降級建議。

## Sibling split

| 需求 | Skill |
|------|-------|
| 模糊多鏡頭決策（單一產品/商業方向本質拆解） | `meta-thinking-framework` |
| 協議競態 / 狀態機合約 | `protocol-adversarial-design` |
| 信任 AI 生成程式碼 | `agentic-clean-discipline` |
| 多邊利害關係人**進入策略**壓測 + 驗證劇本 | **this skill** |

本 skill 的 Phase 1 鏡頭分析與 `meta-thinking-framework` 同源；當決策仍處於「連問題本質都還沒拆清楚」的階段，先跑 `meta-thinking-framework`，產出核心變數後再進入本 skill 的 Phase 0/1。

## References

- `references/sub-agents.md` — 七個 sub-agent 的完整 prompt（redliner / lens_analyst / entity_modeler / game_simulator / red_team / branch_explorer / playbook_writer）
- `references/conflict-adjudication.md` — 衝突裁決優先序 + 鏡頭採信規則
- `references/memory-bank.md` — 記憶庫 schema + 跨決策重用規則
- `references/failure-patterns.md` — 本 skill 的失敗模式（orchestrator 越界做分析、紅隊被污染、衝突被抹平）
- `references/degradation-checkpoint.md` — 何時降級走簡化鏈

## Templates

- `templates/input-spec.md` — Phase 0 輸入規格
- `templates/stop-output.md` — NO-GO 終止報告
- `templates/manifest.yaml` — 記憶庫 manifest
- `templates/final-report.md` — 最終報告骨架
- `templates/h-playbook.md` — 驗證劇本骨架
- `templates/branch-tree.md` — 反事實分支樹骨架

## Evals

- `evals/evals.json` — L1 評估用 test prompts（5 個邊緣案例，覆蓋完整鏈 / 雙邊冷啟動 / 合規分歧 / 降級判斷 / sibling split 不適用）

## Design

- `DESIGN.md` — delegation 拓撲的設計取捨、與既有 skills 的引用關係、待驗證假設、反身性自檢

## Self-loop

若使用者在後續對話回報「這個推演 / 方案不準」、或某個 H-PLAYBOOK 的驗證結果推翻了主幹假設：
1. 定位問題出在哪個 sub-agent（redliner 漏掉紅線？lens 抓錯變數？entity_modeler 遺漏承重實體？game_simulator 沒偵測到降級陷阱？red_team 攻擊腳本不可執行？branch_explorer 分支切換條件失靈？）
2. 只重跑該 sub-agent + 受影響的下游 phase，不從頭重跑。
3. 把修正寫進記憶庫的 `corrections_log`，作為下次同類決策的路由參考。
4. 若驗證結果命中某分支的觸發條件 → 切換到該分支為新主幹，重跑 Phase 5/6。