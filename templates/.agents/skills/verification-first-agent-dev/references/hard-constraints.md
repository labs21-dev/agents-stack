# 硬約束層：把「說過三次的話」升級成機制

## 判準

一句規則值不值得升級為硬約束，看兩個變數，不看「高不高級」：

```
升級優先級 = 違反頻率 × 後果嚴重度
```

- 說過 3 次 → 進入候選
- 後果是不可逆（資料、金錢、安全）→ 直接候選，不用等 3 次
- 只犯過 1 次且後果可逆 → 留在 soft 層（AGENTS.md / prompt）

## 分級與升級操作

| soft（靠記憶） | → hard（靠機制） | 操作 |
|---|---|---|
| 「不要跨目錄直接引用」 | lint no-restricted-imports / import 邊界掃描 | 配置受限路徑對；CI 跑掃描腳本 |
| 「不要在 renderer 跑重任務」 | 架構 CI 檢查 | 掃 main/renderer 依賴方向，跨界即 fail |
| 「不要隨便新增全局狀態」 | 類型/模組約束 | 導出白名單、lint 限建 |
| 「不要繞過現有 Repository」 | lint 限制 DB 客戶端 import 面 | 只允許 repository 層 import DB client |
| 「這個函數參數不能是 X」 | 類型系統 | branded type / narrow type |

## 升級流程（每條）

1. **原文記錄**：當時是怎麼跟 agent 說的（保留原話，未來寫進 lint message）
2. **選載體**：能 lint → lint；能類型 → 類型；能 CI 掃 → CI 掃。順序：編譯期 > lint > CI > 測試
3. **warn 先行**：新規則先以 warn 模式跑 ≥1 週，收集誤報
4. **誤報裁決**：逐條確認每個 warn 是真違規還是規則錯。修規則或修代碼
5. **轉 fail**：誤報率可接受後轉 fail。**這步之後不要輕易回退**——回退一次，CI 權威性就折損一次
6. **同步 soft 層**：hard 落地後，soft 層原話改為指向機制（「CI 會擋」），不重複陳述

## 報錯即上下文

agent 撞到紅線時的報錯文本，就是最好的現場教學。lint message 要寫成對 agent 說話：

```
✗ features/a/cart.ts:3  imports features/b/internal/session
  原因：跨 feature 內部模組禁止直接引用（第 7 次同類違反）
  改法：經 features/b/public.ts 的導出接口使用
```

## 反模式

- **規則堆山**：一次加 20 條 → 誤報爆炸 → 人 disable CI → 全部失效。每次 1-2 條。
- **裝飾性紅線**：加從不會 fail 的規則（測不出真違規）。用已知壞例子測一次紅線真的會紅。
- **硬約束寫成散文**：AGENTS.md 裡 50 條「必須」= soft 層過載。soft 層只留機制暫時表達不了的（風格、意圖、上下文約定）。
- **靜態語言的額外理由**：編譯期就能抓的錯，不要留給 runtime 測試。選型時優先靜態強類型語言，等於免費多一層 hard 約束。