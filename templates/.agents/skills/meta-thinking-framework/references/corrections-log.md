# 修正記錄（Corrections Log）

這個檔案是自我迭代迴圈的落地目標。當使用者回報某次分析「不準」、或事後證明某個假設錯了時，把修正記錄在這裡，作為下次同類問題的路由參考。

## 記錄格式

每筆修正一個區塊，欄位如下：

```
## [日期] 題目摘要
- 問題類型（見 routing-table.md）：
- 錯在哪個鏡頭：頂層 / 本質 / 底層邏輯 / 逆向 / 經濟 / 心理
- 原本的假設／產出：
- 實際發生什麼：
- 修正後的產出：
- 給下次的路由提示：（同類問題應該先檢查／加強哪個鏡頭）
```

## 修正記錄

## [2026-07-21] config.toml coupling → 需連同四門工程 + agent-loop
- 問題類型：系統/agent 架構設計
- 錯在哪個鏡頭：頂層（框太窄）
- 原本的假設／產出：痛點 = 檔案/schema 擁有權軟編碼；解 = role-scoped schema（engine/agent/cwd/models）
- 實際發生什麼：使用者要求把 agent-loop 與 prompt/context/harness/loop 四門工程一併納入——config 耦合是四門控制面擠在同一 bus，不是單純檔案切分問題
- 修正後的產出：以「學科 × 負載/控制面 × loop mount」矩陣重建底層模型；選定方案從「檔案分家硬化」升級為「學科控制面分家 + payload 不得進 TOML」
- 給下次的路由提示：ARC 架構題先畫四門工程 × mount points，再談 config 歸屬；勿只從 `schema.ts` / `engine-agent-split` 起手

## [2026-07-22] 四門工程框仍不夠 → GLOBAL/LOCAL + Project UX + 部署拓撲
- 問題類型：系統/agent 架構設計
- 錯在哪個鏡頭：頂層（仍漏產品軸與部署軸）
- 原本的假設／產出：以四門工程 × mount 定義控制面即可收斂 config
- 實際發生什麼：使用者指出必須同時考慮 `~/.arc` GLOBAL、`./.arc` LOCAL、Project（Open/Add folder）、Local/雲部署；且明確「不行就不要硬設計」
- 修正後的產出：第一軸改為 Global/Local/Session + Deploy-as-topology（非 config 層）；Project = shell 動作綁 pathRoot+讀 LOCAL，不進引擎實體；拒絕雙 getArcHome / 單進程多租戶 / 強行合併 desk workspace
- 給下次的路由提示：config 題先畫「GLOBAL | LOCAL | SESSION |（DEPLOY 非層）」；Open Project 對齊 pathRoot，勿發明第四底層；硬設計紅線見 CONSTITUTION Composition Outside

## [2026-07-22] 可攜 pack：雲 object storage vs 本地 ~/.arc + ./.arc
- 問題類型：系統/agent 架構設計
- 錯在哪個鏡頭：本質（「整包」語意未拆）
- 原本的假設／產出：Project = pathRoot UX 或可攜 LOCAL 政策包（二選一待裁決）
- 實際發生什麼：使用者確認要「專案帶走 agent/hooks」；雲側是 object storage 每次整包加載；問能否與本地 ~/.arc+./.arc 融合，或根本不可能，或只需 ./.arc
- 修正後的產出：拆三種「整包」——僅 LOCAL pack 可融合；整包置換 ~/.arc 與憲法衝突；純 ./.arc 不夠（缺 runtime/密鑰/session 家）。融合契約 = Pack ≡ LOCAL 目錄格式；雲=運輸層，本地=檔案層
- 給下次的路由提示：一說「整包」先問装的是 LOCAL 還是整個 arc home；雲路徑只映射 LOCAL

## [2026-07-22] 定稿落地 — user-project-home-bound-prompt.md
- 問題類型：系統/agent 架構設計
- 錯在哪個鏡頭：—（收斂完成）
- 原本的假設／產出：多輪迭代（四門工程 → GLOBAL/LOCAL → pack → BoundContext → prompt 標籤）
- 實際發生什麼：使用者同意兩層 home、專案記憶、BoundContext、prompt 最終形（無 USER_TOOLS/SNIPPETS；MEMORY 包 USER+PROJECT）；要求定稿對齊
- 修正後的產出：`docs/design/2026-07-22-user-project-home-bound-prompt.md` 為 path/pack/prompt SSOT；07-21 合併稿加補註
- 給下次的路由提示：實作先讀 07-22 文；勿再討論 USER_TOOLS 注入塊

## [2026-07-22] 高效高產出 system prompt 設計 — 實證 A/B 修正損耗清單
- 問題類型：系統/agent 架構設計
- 錯在哪個鏡頭：底層邏輯（損耗清單不全）+ 經濟（終止只算品質面、漏 budget 安全面）
- 原本的假設／產出：產出 = 能力 × (1 − 三種損耗：方向/觸發/注意力)；終止 = 交付物品質面；prompt 設計只看 prompt 內文
- 實際發生什麼：無人值守 ReAct 教訓筆記 A/B — 同一「寫 user tool」任務，厚 persona+肥 skills+錯 run 提示+無 budget = 60-90+ turns；空 persona+limits+正確 framing = 4 turns。證實核心（能力不缺、persona 膨脹是殺手、終止鋒利決定收工），但揭露兩個沒建模的殺手：(1) 環境噪音損耗 = mount 層 `<SKILLS>` 13KB 佔 59% 與 prompt 共用 attention 預算；(2) 機制矛盾損耗 = `<USER_TOOLS>` 教裸 bun 與 runner 不符 → frontmatter 死循環。另外終止缺 budget 安全面、scope framing 比觸發表更上游、人 = 外部 budget（不只補觸發）
- 修正後的產出：損耗擴為五種（+環境噪音 +機制矛盾）；設計擴為三層（層 0 注入面衛生：裁 mount + prompt 與機制一致測試；層 1 STATIC：identity+scope framing / principles / trigger table / 雙層 terminator 品質+budget；層 2 DYNAMIC）；新規則：scope framing 進 STATIC 首句、budget 預設有上限可由 FDE 放開、mount 層是 prompt 設計一部分、prompt 與機制一致性測試為新驗證維度
- 給下次的路由提示：prompt 設計題勿只看 prompt 內文，先審 mount 層體積與「教的做法 vs runner 實際行為」一致性；終止必寫雙層（交付物判準 + budget）；無人值守場景 budget 預設有界、可解開，破解 mechanism-not-policy 張力

## [2026-07-22] 整包裁決後 → loop/config/safety 一體 redesign
- 問題類型：系統/agent 架構設計
- 錯在哪個鏡頭：底層邏輯（機制太多平行旋鈕）
- 原本的假設／產出：pathRoot ≠ jail ≠ desk workspace 三分離；LOCAL 僅 .arc.toml 四鍵
- 實際發生什麼：使用者要對應整個 agent loop + config 各項處置 + safety path/jail + GLOBAL/LOCAL/雲 pack，接受跨域創新、以解決問題為先
- 修正後的產出：提出 BoundContext（projectRoot 默認即 jail）+ Pack≡./.arc + ResolvedRun 分層；config 鍵歸屬表；分階段 refactor；保留 deny-only 逃逸艙
- 給下次的路由提示：path 題先問要不要「開專案＝進籠」；若要則 BoundContext，勿再加第四旋鈕
