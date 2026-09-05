# 出廠審計清單

步驟 4。全部通過才交付；不通過回路由或組裝，不硬交。

## 覆蓋性

- [ ] Worksheet 上每一條約束都有路由結果；無「盤點了但沒路由」的孤兒。
- [ ] 每條 prompt 原則：帶 **why** + 帶**可觀測訊號** + 帶 **capability probe
      結果（或標 pending 並列入交付清單）**。
- [ ] 沒有任何紅線**只**存在於 prompt。
- [ ] 每條原則的 worksheet 上綁定了覆蓋它的 eval case；無 case 不准入。

## 注意力預算

- [ ] 規則 + 原則總量在天花板內（約 2k token 量級）；超過 → 重新路由
      或降階合併，**不是**改寫得更精煉。
- [ ] 範例 ≤ 3 個，全部來自真實失敗，各帶推理鏈。

## 佈局

- [ ] 穩定內容（identity / principles / constraints / output contract）前置
      分節，吃 prompt cache。
- [ ] 可變 context（當次任務 / 用戶檔案 / 檢索結果）獨立區塊，不污染
      cache key。
- [ ] 長任務行為已外移 harness（重注入 / 狀態檢查）；prompt 內只留緩解。
- [ ] 複雜指引在 system prompt，未碎進 tool description；tool schema 只留
      「何時不用」類短政策。

## 契約

- [ ] 輸出格式用**展示**（貼 schema / 模板），不用描述。
- [ ] 知識邊界寫死：只知道 X；範圍外明說不知道，禁止補全。
- [ ] 升級 / 棄答路徑存在：什麼時候停、問人、承認不知道。

## 移植與修訂

- [ ] 跨模型：結構與路由結果可搬；每個模型重跑 capability probe。
      換模型不改 probe 就沿用原則 = 移植神話。
- [ ] Worksheet 已交付（它是修訂時的 blast-radius 地圖）。
- [ ] 標記為 pending / TBD 的項目已彙總成清單，交用戶事後審計
      （登記的人類閘在交付時觸發，不在執行中）。