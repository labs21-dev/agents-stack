---
name: verification-first-agent-dev
description: >-
  把一個項目逐步改造成「Agent 能自己驗證自己」的推進教練。核心命題：人不離開驗證循環
  （截圖、貼日誌、開 DevTools），人就永遠是系統裡最慢的一環；放權等級 ≤ 驗證基建等級，
  所以要改的是生產線，不是 Prompt 技巧。用法有兩個入口——(A) 派活入口：把一句模糊需求
  改寫成帶驗證劇本的任務（造數據 → 操作 → 斷言 → 邊界 → 失敗重修），15 分鐘內產生正回報；
  (B) 建設入口：沿 L0→L5 成熟度階梯把項目補齊四件套——Feature Map（Agent 知道東西在哪）、
  Verification（Agent 自己證明功能能用）、硬約束（說過三次的話變 lint/類型/CI 邊界掃描）、
  Eval（五個真實任務回歸，判斷基建有沒有真變好）。Use when the user asks how to let agents
  verify their own work, wants a feature map / verification doc / agent CI gate, is
  granting agents more autonomy (auto-merge, cloud agents, parallel agents), or says
  things like "agent 又不會自己測" / "每次都要我截圖給它". Do NOT use for reviewing
  already-generated code (use agentic-clean-discipline), evaluating a skill's own quality
  (skill-creator), or agent-facing repo docs in general (coding-docs-standard).
---

# Verification-First Agent Dev（驗證前置的 Agent 開發教練）

## 一句話

把「Agent 寫、人驗證」翻轉成「Agent 寫、Agent 驗證、人管生產線」。
**不要努力把 Agent 變聰明，要把項目設計到笨 Agent 也很難做錯。**

## 何時觸發

- 使用者派活給 agent 時只給了一句模糊需求（「給歷史記錄加搜索」），要幫忙改成可驗證任務
- 使用者抱怨總是在截圖、貼日誌、開 DevTools 餵 agent —— 人還在循環裡
- 使用者想要 feature map / verification doc / agent-facing 項目地圖
- 使用者想把某條「說過三次的規矩」升級成 lint / 類型 / CI 紅線
- 使用者在考慮放權：自動合併、雲端 agent、多 agent 並行
- 使用者問「怎麼知道我的 skill / verification 真的有用」（eval 回歸）

## 何時不觸發（鄰居分工）

| 需求 | 去哪 |
|---|---|
| 已生成的代碼能不能信（grade → gates 審查） | `agentic-clean-discipline` |
| 寫一個新 skill 並給它做 eval | `skill-creator` |
| skill 長期演化 / 畢業 / 廢棄 | `skill-evolution` |
| Agent-facing repo 文件整體規劃（AGENTS.md 等） | `coding-docs-standard` |
| 模糊決策的多鏡拆解 | `meta-thinking-framework` |

本 skill 與 `agentic-clean-discipline` 是上下游：本 skill 管**驗證權怎麼交給 agent**（上游輸入端與項目基建），它管**交出去之後生成的代碼怎麼審**（下游門禁）。一個項目可以兩個都用。

## 核心心法

> 1. **驗證權歸屬是樞紐。** Agent 能自己驗證 ⟺ 知道去哪驗證（Feature Map）× 知道怎麼算通過（Verification）× 環境允許它跑（工具面）。
> 2. **放權等級 ≤ 驗證基建等級。** 這是不變規則。連一個 agent 都不信就開一百個，只會得到一百份要人 review 的結果。放權由基建覆蓋率決定，不由意願決定。
> 3. **說過三次的話不要再靠模型記住。** 能 lint 的 lint，能類型的類型，能讓 CI 掛的讓 CI 掛。報錯本身就是最實在的上下文反饋，比教育模型可靠。
> 4. **斷言查結果，不查無報錯。** exit code 0 不是驗證。「搜出正確的三條」才是驗證。
> 5. **Agent 犯錯後的四連問**：能不能寫進 Skill？能不能加進 Verification？能不能變成 lint/類型？能不能讓 CI 永遠禁止？——每次犯錯都讓系統多一條護欄，這是從「派活」到「改生產線」的轉變。
> 6. **Vanity metric 防線**：吞吐量（PR 數）是基建的結果指標，不作放權決策的輸入。放權只看兩把尺：信任軸（revert rate + 事後 bug 率）+ 自主軸（question rate）。
> 7. **全自主 = 閘門分級自動化，不是沒有閘門。** 每個「想問用戶」的瞬間按序走：有預設就預設（log 它）→ 可查就問環境（repo/日誌/eval 證據）→ 可逆就自己選（交付時標記「我選了X，因為…」）→ 同時滿足「改變結論 ∧ 推不出來 ∧ 不可逆或爭議大」才問人。**禁止靜默猜測**——有預設、有斷言、問人，三者之外不存在第四條路。

## 成熟度階梯 L0→L5（建設路徑的骨架）

```
L0 人肉驗證循環     人是瓶頸；1-2 個 agent 上限；截圖-貼日誌循環
L1 任務級可驗證     每次派活自帶驗證劇本（見用法 A）——第一格，15 分鐘正回報
L2 項目級地圖       feature-map.md + verification.md 持久化；新任務零探索
L3 硬約束層         說過三次的話變 lint / 類型 / CI 邊界掃描；錯誤代碼進不來
L4 基建自校準       eval 回歸 + 犯錯四連問沉澱迴路
L5 放權             自動合併 / 雲端 agent / 多 agent 並行；
                    僅當 L2+L3 覆蓋充分 且 兩把尺（信任軸+自主軸）都過線
```

推進規則：
- **一次只推進一層**。跳層是放權不等式的違反形態。
- **每一層用中建**：先讓 L1 在當前派活裡賺到一次正回報，再考慮 L2。先建完再用永遠到不了第一步。
- **每層有降級出口**：小項目、一次性腳本、探索原型、可隨手回滾的改動——L1 即終點，L2+ 是負收益。明說出口，不硬推。
- **問題邊緣化**：所有需要人回答的問題集中在 intake（一輪問完）或 delivery（標記清單事後抽查），執行中零插手。這是 L4→L5 的必修課——執行中還會打斷人的流程，放權了也跑不快。

## 用法 A：派活入口（L1，最高頻）

把一句模糊需求改寫成帶驗證劇本的任務。流程：

1. **抓功能名與入口**（若有 L2 feature map 先查；沒有就問 agent 項目或讓它探索一次）
2. **造數據**：這個功能要工作，先需要什麼測試數據？幾條？什麼樣？
3. **正路徑**：操作 → 看到什麼才算對？（斷言查**結果**，不查無報錯）
4. **邊界**：空輸入 / 中文 / 大數據量 / 大小寫 / 恢復原狀——至少 2 個真實邊界
5. **失敗協議**：任何一步失敗 → 繼續修 → 重跑全部步驟，直到全部通過
6. **環境工具對齊**（見 `references/env-tools.md`）：Web→CDP；iOS→Simulator；CLI→stdout/stderr/exit code；桌面→啟動 + 截圖 + 日誌

### 改寫範例（原文）

之前：
> 給歷史記錄增加搜索功能。

之後：
> 完成歷史記錄搜索功能。
> 啟動開發版本。創建三條測試數據。搜索其中一個關鍵詞。
> 確認搜索結果只出現匹配內容。清空關鍵詞，確認完整列表恢復。
> 測試中文、英文和空搜索。
> 如果任何一步失敗，繼續修復，直到驗證全部通過。

差別不是字數，是**驗證權**：前者驗證在人手上，後者驗證在劇本裡。

### 怎麼低成本寫出劇本

不需要每句 prompt 都手寫。語音閒談式說出理解 → 用「Grill me」類 skill 層層逼問出需求與驗證點 → 收斂成劇本。劇本是輸出的**收斂形**，不是起點。

## 用法 B：建設入口（L2→L5，按需逐層）

### L2 — 項目地圖（用 `templates/feature-map-template.md` + `templates/verification-template.md`）

每個 feature 一張卡：入口 / 驗證步驟 / 相關代碼 / 常見問題。放置：

```
.agent/
  skills/
    verification.md
  feature-map.md
```

**地圖腐爛防禦**：每條 feature map 卡必須附驗證錨——驗證步驟失敗本身就是「地圖過期」的偵測信號。驗證不過先懷疑地圖，不先懷疑代碼。

### L3 — 硬約束層（用 `references/hard-constraints.md`）

收集口頭規矩 → 分級 → 逐條升級：

| 級別 | 載體 | 例 |
|---|---|---|
| soft | AGENTS.md / prompt | 「必須使用 Repository」 |
| hard | lint 規則 / 類型 | no-restricted-imports、satisfies |
| hard | CI 邊界掃描 | 掃 import，發現 `features/a → features/b/internal` 直接掛 |
| hard | CI 架構檢查 | Electron main/renderer 依賴方向檢查 |

**護欄誤傷防禦**：新約束先 warn 模式跑一段，誤報率確認可接受後才轉 fail。CI 誤傷會教人 disable CI——整層約束失效比沒有更糟。

### L4 — 基建自校準

- **Eval 回歸**：準備 5 個真實任務（含一個壞地圖/弱斷言的陷阱），每次改 verification.md / skill 就全量重跑。看 agent 是否：找對模組、啟動應用、真正復現、修復、再驗證、給出驗證結果。
- **犯錯四連問**（見核心心法 5）：每次 agent 犯錯，走一遍，把經驗沉澱進基建而不是鞭打 agent。
- **反向測試斷言**：拿已知壞例子測驗證腳本——抓不住壞例子的斷言是假綠生成器。

### L5 — 放權

放權前置檢查清單（全部 ✅ 才放權，用 `templates/autonomy-checklist.md`）：

- [ ] L2 地圖覆蓋要放權的功能域
- [ ] L3 紅線覆蓋該域的常見違規
- [ ] L4 eval 在該域的通過率穩定（近 3 次全綠）
- [ ] 兩把尺都過線：**信任軸**（revert rate + 事後 bug 率）且**自主軸**（question rate——每 10 個任務人被介入次數）。revert 低但 question 高是溫室自主；question 低但 revert 高是悶頭猜。兩低才真自主
- [ ] 任務劇本已過 question audit：每個決策點三選一——有預設 / 可查環境 / 註冊為合法升級點；無靜默猜測路徑
- [ ] 問題邊緣化：intake 一輪問完 → 執行零插手 → 交付附「此處我選了X」標記清單
- [ ] 放權監控指標 = 兩把尺（不是吞吐量）
- [ ] 出事時的收權路徑明確（誰、怎麼、多久收回；任一把尺超閾自動降級）

漸進路徑：單任務自驗證 → 單域自動合併 → 多域 → 雲端 agent。**每次擴域重跑本清單。**

## 必要輸出（每次調用）

1. **用法聲明**：A（派活改寫）/ B-第幾層（建設）/ 混合
2. **用法 A**：改寫後的完整驗證劇本（含造數據、正路徑、≥2 邊界、失敗協議、環境工具）
3. **用法 B**：當前階梯位置判定 + 本層最小交付物 + 下一層觸發條件
4. **降級出口聲明**：若本任務屬於「L1 即終點」類，明說並停
5. **基建四連問**（若本次交互中有 agent 犯錯）：四連問逐條過，有產出就落地
6. **決策標記清單**（自主執行的任務）：列出所有「Level-2 自主選擇」——此處我選了 X，因為…——供用戶事後抽查，不阻塞交付

## 參考檔案

- 環境工具對照（CDP / Simulator / CLI / 桌面各怎麼給 agent 自驗證能力）→ `references/env-tools.md`
- 硬約束分級與升級操作 → `references/hard-constraints.md`
- 派活改寫範例庫（從一句話到劇本的更多例子）→ `references/rewrite-examples.md`
- 模板：feature map 卡 → `templates/feature-map-template.md`
- 模板：verification 規格 → `templates/verification-template.md`
- 模板：放權前置清單 → `templates/autonomy-checklist.md`
- Eval：觸發與行為回歸 → `evals/evals.json`