# 約束盤點 + 路由 worksheet

每次分析的起點。一列一條約束；路由表見 SKILL.md，機制見
`../references/constraint-routing.md`。交付時本表隨 prompt 一起交出
（它是修訂時的 blast-radius 地圖）。

## 脈絡

- 目標模型：
- Harness / 執行環境：
- 既有 eval / probe：（無 → 步驟 5 先建，入場券）
- 來源：既有 prompt 改寫 ／ 新建清單

## 判定表

判定欄填法（升階優先：符合多層時選最高層）：

| # | 約束（一行） | 可枚舉? | 失敗可機械檢測? | 紅線? | 模型已具備判斷?（probe） | 有生產失敗樣本? | 路由去處 | 訊號 / 檢查 | 覆蓋的 eval case | 未來升級? |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |

路由去處枚舉：`validator` / `harness` / `prompt-example` / `prompt-principle`
/ `harness-reinject`（長任務漂移項）。

## 規則

- 「失敗可機械檢測」今天寫不出檢查程式就填 No——同時在「未來升級」欄
  記下構想，暫路由 prompt-principle。
- prompt-principle 行的「訊號」欄必填：什麼可觀測結果算它被遵循。
- prompt-principle 行的「覆蓋的 eval case」必填：無 case 不准入 prompt。

## 交付時彙總

- pending（probe 未跑）：
- TBD（harness 去處待執行環境確認）：
- 未來升級候選：