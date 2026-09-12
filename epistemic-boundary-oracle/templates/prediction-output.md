# 機率輸出不可坍縮結構骨架（2a 短視野專用）

> 僅當准入檢查全通過才輸出此結構。否則降格條件式警戒（委派 SDST）或拒絕。

```yaml
query: ""
domain_class: "second-class-2a"
regime_ref: ""                                 # 制度公布的版本號 / 可觀測定義引用
regime_source: "institutional"                 # 必須 institutional；analyst-drawn → 不該出現在此路徑
regime_definition_observables:                 # R 由哪些可觀測量定義
  - ""
p_outcome_given_regime:                        # 條件機率，不是機率
confidence_interval: [, ]
calibration:
  precommitted_domain: ""
  historical_forecasts:
  timespan_years:
  brier_score:
  calibration_curve_ref: ""
horizon: ""
horizon_stability_ratio:                       # 必須低於閾值（否則視野閘應已攔截）
trip_wires:                                    # 任一斷裂 → 機率失效、樣本歸零
  - {observable: "", break: ""}
soft_redefinition_suspect_index:               # 調節 confidence_tier
symptoms_monitored:                            # 軟改症狀（描述性，可回測）
  - {symptom: "", current: "", baseline: ""}
confidence_tier: ""                            # high | medium | low | exit-to-SDST
reform_history:                                # 描述性，非預測性
  changes:
  years:
  note: "descriptive, not predictive — not a P(regime stable) input"
tail_class: "third-class uncalibratable"
residual: |
  soft-redefinition may be underway with symptoms not yet visible;
  uneliminable; only suppressed by short horizon (heuristic, not calibrated)
output_form_justification: |
  2a + institutional boundary + short horizon + trip_wires set + suspect index low
  → eligible for probability output with confidence tier
```

## 准入檢查（輸出前全部成立）
- [ ] domain_class = second-class-2a
- [ ] regime_source = institutional
- [ ] horizon_stability_ratio 低於閾值
- [ ] trip_wires 已挂
- [ ] soft_redefinition_suspect_index 低於上閾
- [ ] reform_history 標為 descriptive, not predictive
- [ ] residual 欄已填且標記 uneliminable + heuristic

任一不成立 → 不輸出此結構，降格或拒絕。

## 降級路徑（confidence_tier 由嫌疑指數調節）
- 低 → high
- 中 → medium
- 高 → low
- 超上閾 → exit-to-SDST（協議層：下游拿不到 p_outcome_given_regime，強制路由 SDST）