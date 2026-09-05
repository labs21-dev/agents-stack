# System Prompt 骨架

只裝路由後屬於 prompt 的內容（prompt-principle / prompt-example /
提醒性 NEVER）。骨架各節用穩定前綴標籤分節，吃 prompt cache。

```xml
<identity>
具體職能 + 領域 + 資歷邊界（不是 "helpful assistant"）。
目標：可驗證的成功條件（success predicate），不是形容詞。
</identity>

<principles>
<!-- 每條三件套，缺一不入 -->
1. [權衡原則：寫「怎麼想」] — why: [為什麼] — signal: [什麼可觀測結果算遵循]
2. ...
衝突時優先序：安全與合規 > 正確 > 有用 > 風格
（此序須在 harness 同步強制，否則僅為願望清單）
</principles>

<constraints>
<!-- 提醒層；真正的紅線已在 harness 強制，此處 NEVER 是降發生率備份 -->
- NEVER: [紅線，註明 harness 對應強制點]
- 知識範圍僅限 [context / tools]；範圍外明說不知道，禁止補全事實。
</constraints>

<workflow>
1. ... （複雜任務才寫；每步可對應 harness 階段閘）
</workflow>

<tools>
何時用、何時**不用**、失敗時如何降級。
（複雜指引收在這裡，不碎進 tool description）
</tools>

<output>
<!-- 展示，不描述：直接貼 schema 或完整模板 -->
</output>

<examples>
<!-- 1–3 個，全部來自生產失敗，各帶推理鏈 -->
[輸入] → [為什麼這是對的動作] → [正確動作]
</examples>

<escalation>
什麼時候停、問人、承認不知道。
</escalation>
```

## 佈局規則

- 穩定塊（identity / principles / constraints / output）**前置**分節 → cache。
- 可變 context（當次任務、用戶檔案、檢索結果）**另開區塊**，不混入穩定塊。
- 長任務會漂移的行為：不靠前置原則撐——外移 harness 重注入 / 狀態檢查。
- 總量預算：規則 + 原則約 2k token 量級天花板；超過回路由，不精煉措辭。

## 每節品質要求

| 節 | 不合格特徵 | 合格特徵 |
|---|---|---|
| identity | "資深專家助手" | 職能具體到任務與邊界 |
| principles | 形容詞、無訊號 | 三件套齊 + probe 通過 |
| constraints | 紅線只在此 | 每條 NEVER 對應 harness 強制點 |
| output | 散文描述格式 | 貼 schema / 模板原文 |
| examples | 想像的 happy path | 生產失敗 + 推理鏈 |