# 額外鏡頭育成日誌（Emerging Lenses Log）

這個檔案記錄六標準鏡頭之外被引入過的額外鏡頭。目的：讓「該加的鏡頭沒加」與「反覆出現的鏡頭該畢業成標準鏡頭」這兩件事可追蹤，使框架隨使用演化。

## 記錄格式

每筆一個區塊：

```
## [日期] 額外鏡頭名稱 — 用於什麼問題
- 問題類型（見 routing-table.md）：
- 觸發變數：步驟 2 抽出的哪個核心變數需要它
- 反事實對比：硬套六鏡哪一個會漏掉什麼
- 觀察推論摘要：（該鏡頭產出的關鍵洞察）
- 事後驗證：這個鏡頭的洞察事後被證實有效 / 無效 / 待驗
- 累計使用次數：（同類問題）
- 是否達畢業門檻：（是 → 提議納入 routing-table；否 → 仍為臨時鏡頭）
```

## 畢業門檻（建議）

- 同類問題累計 ≥ 3 次，且事後驗證至少 1 次有效 → 提議納入 `routing-table.md`。
- 累計 ≥ 3 次但全部無效 → 標記為「偽需求鏡頭」，不再輕易引入（記錄其失敗原因）。

## 記錄

## [2026-07-22] 機制一致性（mechanism coherence）— 用於 system prompt 設計
- 問題類型：系統/agent 架構設計
- 觸發變數：「prompt 與運行機制的一致性」——prompt 教的做法若與 runner 實際行為不符，造成 self-reinforcing loop
- 反事實對比：硬套底層邏輯鏡頭會把 prompt 當封閉狀態機、漏掉 prompt 教的動作與外部 runner 的介面契約（runner 行為不在 prompt 詞彙內）；硬套逆向只列「prompt 可能錯」，看不到「prompt 與機制互相強化錯誤」的死循環結構。此為教訓筆記 §2.1（`<USER_TOOLS>` 教裸 bun → frontmatter 死循環）root cause，六鏡原框架會漏
- 觀察推論摘要：prompt 是與引擎機制共同構成的契約，非獨立文件；每一條「教的做法」必須對 runner 實測，不一致時改 prompt 或改 runner 但不可兩邊各自看起來對。prompt 設計第一道驗證 = 教法 vs runner 實際行為逐條對齊，這是傳統 prompt engineering 沒有的維度
- 事後驗證：待驗（同類問題累積中）
- 累計使用次數：1
- 是否達畢業門檻：否（需同類 ≥3 次且驗證有效）。候選觀察：疊加利害關係人矩陣時，「引擎機制」可作為非人 stakeholder，其「抵抗」= 機制漂移——此疊加效應支持鏡頭獨立性

## [2026-07-22] 反身性 / 自舉（recursion / self-reference）— 用於 meta-skill 系統設計
- 問題類型：系統/agent 架構設計
- 觸發變數：「反身性」——meta-skill 作用對象是 skill 本身，與自己同 substrate；用自己的標準評自己的產出
- 反事實對比：硬套底層邏輯會把 meta-skill 建模成單向狀態機、把「好 skill 標準」當固定輸入，漏掉此標準是 self-defined 且須 bootstrap；硬套心理學只說 confirmation bias，但此處失敗不是人類認知偏誤，而是驗證函數與生成函數共用同一 substrate、內部驗證不獨立——再客觀的內部 reviewer 也跟 generator 同源，抓不到同源的錯
- 觀察推論摘要：meta-skill 用自定標準評自產 skill → 自我驗證平庸化（一切過自己 bar、品質單調漂移到 self-consistent but mediocre）。外部 anchor 是結構性必要非 nice-to-have——這解釋 extract-methodology 硬人類 gate 與進化設計人類批准的必然性，不是 governance 偏好而是反身性失敗的唯一解。與機制一致性區別：後者=skill vs 外部 runner（兩系統契約，失敗=death loop）；反身性=skill vs 自己產出用自己標準評（一系統自摺，失敗=self-validating mediocrity）
- 事後驗證：待驗（待驗假設 #1：是否可被心理學+底層邏輯涵蓋，若可則鏡頭多餘）
- 累計使用次數：1
- 是否達畢業門檻：否。候選觀察：與機制一致性同屬「非人 stakeholder 的結構性抵抗」家族，但失敗模式不同（漂移 vs 死循環），支持獨立

## [2026-07-22] 認識論遞迴（epistemic recursion）— 用於 extract-methodology review
- 問題類型：系統/agent 架構設計
- 觸發變數：「抽取器本身是被同一 substrate 抽取的對象」——extract-methodology 從 worked example 抽 methodology，而抽取動作用的 methodology（六步 protocol）本身也是從某 worked example 抽出的產物；外部 anchor（CCA laws）也非公理，也是抽出物
- 反事實對比：硬套反身性鏡頭會說「外部 anchor 解」，但此處外部 anchor 本身也是 N=1 抽出物、非公理，反身性鏡頭看不到 anchor 也待校準這層；硬套底層邏輯會把六步 protocol 當不變規則，漏掉 protocol 有效性不能用自己定義的 Self-check 驗（Self-check 是內部分）
- 觀察推論摘要：extract-methodology 誠實承認此威脅（v0/N=1 標記、re-calibrated by own output），其外部 anchor 實為跨 case 收斂+人類立法+step 5 驗證 fold 是否讓輸出更銳利，非 CCA 種子。有效性循環依賴足夠 case 疊代——case 不足時抽取品質不可信，產出是候選非定論。與反身性區別：反身性=generator=evaluator 同源（解=外部 anchor）；認識論遞迴=anchor 本身也待校準（解=跨 case 疊代收斂，無終點公理）。可補強缺口：CASE.md 應標 N 值（當時累積 case 數）讓讀者知可信度
- 事後驗證：待驗（待驗假設：increment-only step 4 能否真擋重述已知——擬用本對話跑一次驗證）
- 累計使用次數：1
- 是否達畢業門檻：否。候選觀察：與反身性同屬「meta-層自我威脅」家族，但反身性解於外部 anchor、認識論遞迴解於跨 case 疊代（anchor 非公理），失敗模式與解法不同，支持獨立