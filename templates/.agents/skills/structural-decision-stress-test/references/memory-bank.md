# 記憶庫 Schema 與跨決策重用

所有推演寫入記憶庫，供後續同類決策重用與自我迭代。

## 目錄結構

```
/memory_bank/decisions/{YYYYMMDD}_{slug}/
├── manifest.yaml          # 本次推演的委派追蹤 + 產物索引
├── phase0-redlines.json
├── phase1-lenses.json
├── phase2-entities.json
├── phase3-sim/            # 博弈日誌可能多輪，用目錄
├── phase4-redteam/        # 四份攻擊腳本
├── phase5-branches.json
├── phase6-playbooks.yaml
└── corrections_log.md     # 本次修正了前次記憶庫的哪些假設
```

## manifest.yaml

```yaml
decision_id: "20260728_coalition_loyalty_entry"
orchestrator_version: "2.5.0"
slug: "coalition_loyalty_entry"
created: "2026-07-28"

delegation_trace:
  - agent: "redliner"
    verdict: "GO"
    tokens_used: 340
  - agent: "lens_analyst"
    top_variables: ["V1", "V2", "V3"]
    tokens_used: 2800
  - agent: "entity_modeler"
    load_bearing_entities: ["E5", "E9", "E8"]
    tokens_used: 4100
  # ... 完整 trace

artifacts:
  phase0: "redlines.json"
  phase1: "lens_analysis.json"
  phase2: "entity_state_machines.json"
  phase3: "game_simulation_log.json"
  phase4: "red_team_scripts.json"
  phase5: "counterfactual_branches.json"
  phase6: "h_playbooks.yaml"

cross_references:
  - entity_id: "E9"
    first_defined_in: "20260728_coalition_loyalty_entry"
    referenced_by:
      - "20260815_agent_dns_mesh"
    note: "跨決策重用：控制權爭奪結構相似"

human_validation_status:
  H1: "pending"
  H2: "pending"
  H3: "completed → H3 成立，維持主幹"

conflicts_adjudicated:
  - conflict_id: 1
    agents: ["game_simulator", "lens_analyst"]
    winner: "game_simulator"
    rule: "優先序1 + 優先序3"
```

## 跨決策重用規則

承重實體（如 E9 積分法律資格）常跨決策復現。當新決策的 entity_modeler 產出與記憶庫既有實體結構相似時：
1. 在新 manifest 的 `cross_references` 記錄引用關係。
2. 標注「結構相似」而非「相同」——上下文不同，狀態機轉換可能不同。
3. 不直接拷貝舊結論；重跑該實體的狀態機，只把舀結論當先驗。

## 自我迭代

`corrections_log.md` 記錄本次推演修正了前次記憶庫中的哪些假設。格式：

```
## [日期] 修正項
- 被修正的舊假設: ...
- 來自哪個舊決策: {decision_id}
- 修正為: ...
- 觸發證據: ...（哪個 H-PLAYBOOK 的驗證結果）
```

> 對應 SKILL.md 的 Self-loop：不從頭重跑，只重跑受影響 sub-agent + 下游 phase，並把修正寫進這裡。