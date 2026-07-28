# 降級 Checkpoint（何時走簡化鏈）

Hard rule 6：複雜度低 → 允許跳過 Phase 3/4 並行組，走簡化鏈。小題大作也是損耗。

## 降級觸發條件（全部滿足才降級）

1. **無雙邊市場特徵**：Phase 1 的 lens_analyst 未觸發 PLATFORM_DYNAMICS 額外鏡頭。
2. **無合規分歧實體**：Phase 2 的 entity_modeler 未產出「法律資格分歧點」類承重實體。
3. **無跨法人 / 跨實體資金流**：BOUNDARY_CONDITIONS 的不可逆項不涉及資金鏈 / 控制權讓渡。
4. **單一對抗組不存在**：決策不涉及「錨點 vs 創辦人」「監管 vs 平台」這類持續博弈。

## 降級後的鏈

跳過 Phase 3（game_simulator）與 Phase 4（red_team），改走：

```
Phase 0 redliner → Phase 1 lens_analyst → Phase 2 entity_modeler
  → Phase 5' branch_explorer（簡化，只跑主幹 + α 一條）
  → Phase 6 playbook_writer
```

## 降級必須顯式標記

最終報告的 EXECUTIVE_SUMMARY 卄須註明「**本決策複雜度低，已降級走簡化鏈，跳過博弈模擬與紅隊**」。不可靜默省略——靜默省略會讓讀者誤以為跑過完整壓測。

## 反降級（升級）信號

若執行簡化鏈途中，Phase 1/2 出現以下任一信號，**立即升回完整鏈**：
- lens_analyst 觸發了原本未預期的 PLATFORM_DYNAMICS / COMPLIANCE
- entity_modeler 產出了「法律資格分歧點」或「控制權爭奪」承重實體
- BOUNDARY_CONDITIONS 出現新的不可逆項

升級時不從頭重跑，只補跑 Phase 3/4 及受影響的 Phase 5/6。