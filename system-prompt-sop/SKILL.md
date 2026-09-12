---
name: system-prompt-sop
description: >-
  Design-time SOP for system prompts / agent harness prompts: route every
  constraint to its correct enforcement layer (validator/schema > harness >
  prompt example > prompt principle) instead of piling rules or vibes into the
  prompt. Use when the user asks to design, write, rewrite, review, or tune a
  system prompt; convert a rule-pile into principles; complains that an agent
  ignores rules, drifts in long tasks, or breaks red lines; wants to port a
  prompt to another model; or debates "principle vs rule". Also use when a
  prompt has ballooned past ~2k tokens of rules, or when constraints are being
  scattered into tool descriptions. Do NOT use for skill authoring (use
  skill-creator — though its constraint-routing decisions may consult this
  SOP's routing table), training-time alignment/fine-tuning, prompt-injection
  security, or one-off user prompts with no recurring maintenance surface.
  Method: eval gate → constraint inventory → per-constraint routing →
  skeleton assembly → pre-ship audit → probe iteration.
---

# System Prompt SOP（約束路由）

把「設計 system prompt」從風格之爭變成工程決策：不問「原則還是規則」，
**對每一條約束單獨路由到它夠格的最高執行層**。Prompt 只收留少數 advisory
內容，且每條帶 why + 可觀測訊號 + eval 覆蓋。

## 核心機制（三條，路由表的地基）

1. **Prompt 不教判斷，只做選擇。** 原則是對「模型已具備的行為分佈」的壓縮
   錨定。採用原則的前置條件：該判斷已在目標模型能力分佈內（用探針驗證，
   見 `references/constraint-routing.md`）。
2. **Prompt 內一切皆 advisory。** `NEVER` 在 prompt 裡只是提醒；紅線只有
   外移到 harness 才為真。
3. **注意力天花板不豁免原則。** 原則是壓縮率較好的牆，不是免檢通行證；
   超預算時降階或外移，不要改寫得更「精煉」。

## Flow

0. **Intake batch**（見下，缺項一次問完，執行中不再中斷）
1. **盤點約束**：列出每一條想要的行為 → `templates/routing-worksheet.md`
2. **逐條路由**：按下方路由表判定去處（核心步驟，機制詳解見
   `references/constraint-routing.md`）
3. **組裝 prompt**：只裝路由結果中屬於 prompt 的部分 →
   `templates/prompt-skeleton.md`
4. **出廠審計**：逐項過 `references/audit-checklist.md`
5. **Probe 迭代**：原則項跑 20-case 探針；不通過就降階（規則/範例），
   不是改措辭

## Intake batch（步驟 0，一次問完）

缺以下任一項且上下文推不出來時，開頭一次問齊：

- **目標模型**（決定 capability 前檢；未定 → 寫 runtime-agnostic，探針標 pending）
- **執行環境 / harness**（決定紅線去處；未定 → 紅線去處寫抽象條款並標 TBD）
- **既有 prompt**（改寫）或**目標行為清單**（新建）
- **既有 eval / probe**（沒有 → 步驟 5 先建最小 probe，這是入場券不是收尾）

## 路由表（核心）

| 判定條件 | 去處 | 形式 |
|---|---|---|
| case 可枚舉 **且** 失敗可機械檢測 | **移出 prompt** → schema / validator / linter | 程式即規格 |
| 不可協商紅線（失敗成本不可逆） | **Harness 強制**（審核閘、權限、deny-list）；prompt 內 NEVER 僅作提醒 | 外部即法律 |
| 有生產失敗樣本的判斷行為 | **Prompt 範例**：輸入 → 推理鏈 → 正確動作 | 分佈錨定 |
| case 開放 **且** 模型已具備該判斷（探針驗證過） | **Prompt 原則**：一句話 + why + 可觀測訊號 | 能力錨定壓縮 |
| 長任務中後段會漂移的行為 | **Harness**：重注入 / 狀態檢查 / 階段閘 | 前置原則撐不住 lost-in-the-middle |

**升階優先**：同一條約束符合多個條件時，選它夠格的**最高執行層**
（validator > harness > 範例 > 原則）。只在更高層做不到或成本過高時降階。
今天寫不出檢查程式的約束 → 暫放原則層，並在 worksheet 記「未來升級」欄。

## 預設與升級點（autonomy profile）

- **預設**：runtime 未定 → runtime-agnostic + pending 標記；檢測程式今天寫不出 → 原則層 + 未來升級欄；範例未指定數量 → 1–3 個真實失敗情境。
- **環境可查**：既有 prompt、既有 eval、目標模型（通常從上下文可推）。
- **登記的人類閘**：無。所有路由判定由 worksheet 的判定欄推出；唯一回報點在交付時——把「標 pending / TBD」的項目列成清單交用戶事後審計。

## References

- `references/constraint-routing.md` — 路由機制詳解：能力探針方法、升階規則、cache 與 mid-context 遵循的衝突及解法、修訂爆炸半徑。路由表每一格的「為什麼」在這裡。
- `references/audit-checklist.md` — 出廠前逐項審計；全過才交付。
- `references/anti-patterns.md` — 九個已確認的失敗模式（含證據錯置與移植神話），改寫別人 prompt 時用來快篩。

## Templates

- `templates/routing-worksheet.md` — 約束盤點 + 路由判定表，每次分析的起點。
- `templates/prompt-skeleton.md` — 組裝骨架，含每節的品質要求與 cache 佈局。

## Reflexivity self-check

本 SOP 的「何為好 prompt」標準部分來自公開研究、部分來自一次六鏡分析
（2026-09，N=1）。其防自證機制：每條機制都綁了一個最低成本驗證法
（見 constraint-routing.md 末節）。真實使用若發現路由表誤判
（例：某類約束放 validator 反而更糟），先修 routing-table 對應欄位的
判定條件，不要急著加例外條款。