# 預承諾日志與不可坍縮輸出

## 第一類域 — 預承諾日志（純記賬紀律）

第一類域的邊界被機制釘死，沒判斷空間可過擬合。預承諾協議在這裡的角色是**純記賬紀律**（防事後改定義 / 跨域平均），不是校準來源——校準來自機制本身 + 同分布樣本累積。

### 預承諾協議

每次預測前必須先寫下（不可事後改）：

```
- 被預測事件的精確定義（可觀測、可判定兌現）
- 兌現時間
- 兌現判定方法（誰、依什麼證據）
- 自稱屬於哪個「預承諾域」（該域邊界必須在本次預測前已登記，不能事後新建）
```

預測兌現後：

```
- 記錄結果
- 只在「預承諾域」內累積 Brier，不允許跨域平均
- 任何「我這次預測其實屬於另一個域」的事後重分類 → 標記為污染，不計入校準
```

這把不可校準的部分（域邊界判斷）凍結在預測發生的那一刻——必須在不知道結果時就承諾這是哪個域的樣本。事後重畫邊界會被協議抓到。

### 適用範圍（誠實收緊）

預承諾協議**只在邊界已被機制釘死、但樣本需要累積的域裡有用**——純記賬紀律。它**不能**把一個邊界是判斷的域（2b / 第三類）變成可校準域。對那些域，凍結的還是個判斷，不是事實。

對第三方預登記的誠實結論：補不干净。第三方要麼先窮盡未來問題的分類（= 先造一個預言機，循環），要麼針對查詢臨時制定邊界（= 換個人過擬合）。第三方獨立性擋不住事前過擬合，因為第三方面對的是同一個開放問題空間。

## 第二類 2a — 不可坍縮輸出結構

2a 短視野窗口內的機率輸出必須是不可坍縮結構（見 `tail-defense.md` § 防禦 A）。完整欄位：

```yaml
# 不可坍縮機率輸出（2a 短視野專用）
query: "..."
domain_class: "second-class-2a"
regime_ref: "FED_DUAL_MANDATE_v2012"           # 制度公布的版本號 / 可觀測定義引用
regime_source: "institutional"                  # institutional = 2a；analyst-drawn = 2b（不該出現在這條路徑）
regime_definition_observables:                  # R 由哪些可觀測量定義
  - "statutory mandate text v2012"
  - "FOMC meeting schedule (8/yr)"
  - "dot plot publication format"
p_outcome_given_regime: 0.62                    # 條件機率，不是機率——鍵名本身重述條件性
confidence_interval: [0.55, 0.69]
calibration:
  precommitted_domain: "FOMC_NEAR_TERM_RATE_PATH"
  historical_forecasts: 47
  timespan_years: 12
  brier_score: 0.31
  calibration_curve_ref: "..."
horizon: "18mo"
horizon_stability_ratio: 0.3                    # horizon / regime 歷史穩定半衰期；超閾則不該出現在這條路徑
trip_wires:                                     # 任一斷裂 → 機率失效、樣本歸零、從零重校
  - {observable: "statutory mandate text", break: "version change"}
  - {observable: "FOMC meeting schedule", break: "frequency change"}
  - {observable: "dot plot publication", break: "discontinued"}
soft_redefinition_suspect_index: 0.15           # 症狀加權；調節 confidence_tier
symptoms_monitored:                             # 軟改症狀清單（描述性，可回測）
  - {symptom: "committee vote dispersion", current: 0.12, baseline: 0.09}
  - {symptom: "decision-language semantic drift", current: "low", note: "embedding distance vs 5yr baseline"}
confidence_tier: "high"                         # high | medium | low | exit-to-SDST（由嫌疑指數調節）
reform_history:                                 # 描述性，非預測性
  changes: 3
  years: 40
  note: "descriptive, not predictive — not a P(regime stable) input"
tail_class: "third-class uncalibratable"        # 尾巴的本質
residual: |
  soft-redefinition may be underway with symptoms not yet visible;
  uneliminable; only suppressed by short horizon (heuristic, not calibrated)
output_form_justification: |
  2a + institutional boundary + short horizon + trip_wires set + suspect index low
  → eligible for probability output with confidence tier
```

### 准入檢查（輸出此結構前必須全部成立）

- [ ] domain_class = second-class-2a（不是 2b、不是長視野）
- [ ] regime_source = institutional（制度公布，非預測者畫）
- [ ] horizon_stability_ratio 低於閾值（否則防禦 B 閘應已攔截，不該走到這裡）
- [ ] trip_wires 已挂（硬改可觀測量已列）
- [ ] soft_redefinition_suspect_index 低於上閾（否則應 exit-to-SDST）
- [ ] reform_history 標為 descriptive, not predictive
- [ ] residual 欄已填且標記為 uneliminable + heuristic

任一不成立 → 不輸出此結構，降格條件式警戒（委派 SDST）或拒絕。

### 降級路徑

`confidence_tier` 由 `soft_redefinition_suspect_index` 調節：
- 低 → high
- 中 → medium（輸出仍為機率，但置信等級降）
- 高 → low
- 超上閾 → `exit-to-SDST`（退出機率路徑，轉條件式警戒）

降級是協議層行為，不是註腳——tier = exit-to-SDST 時，下游拿不到 `p_outcome_given_regime`，結構強制路由去 SDST。