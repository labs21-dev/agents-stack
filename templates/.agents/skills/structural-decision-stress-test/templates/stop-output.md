# NO-GO 終止報告

> Redliner 觸發 NO-GO 時使用此模板。**不進入後續 phase。**

## REDLINER_VERDICT
- verdict: NO-GO
- 觸發紅線: [RESOURCE_MISMATCH / IRREVERSIBILITY / ZERO_ATTRACTOR]
- rationale: （一句話）

## 否決理由詳述
（為什麼這條紅線成立、基於什麼證據）

## 降級建議
（若可降級，建議改走什麼方向；若不可降級，明說「此方向不建議推進」）

## 已消耗
- 本次僅運行 Phase 0 redliner，未進入分析階段。
- 記憶庫已寫入 `{YYYYMMDD}_{slug}/phase0-redlines.json`。