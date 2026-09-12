# 本 Skill 的失敗模式（Orchestrator 自檢）

逐項檢查是否有對應防禦：

- [ ] **Orchestrator 越界做分析**：Orchestrator 是否自己產出認知內容（變數、實體、博弈預測），而非委派？防禦 = Hard rule 3。Orchestrator 只路由、裁決、寫庫。
- [ ] **紅隊被污染**：red_team 是否讀到了 game_simulator 的輸出？防禦 = Hard rule 2 + sub-agents.md § red_team 隔離規則。隔離一旦破壞，紅隊退化成主線的回聲。
- [ ] **衝突被抹平**：最終報告是否把 sub-agent 衝突藏進「綜合方案」？防禦 = Hard rule 5 + CONFLICTS_LOG 必填區。無衝突要明說「無衝突」，有衝突要顯式裁決。
- [ ] **Redliner 被跳過**：是否在未跑 Phase 0 的情況下直接進入分析？防禦 = Hard rule 1。對已否決方向做美化分析是最大浪費。
- [ ] **無 playbook 的結論**：是否輸出了方案卻沒有對應 H-PLAYBOOK？防禦 = Hard rule 4。沒有驗證劇本的結論不可交付。
- [ ] **攻擊腳本不可執行**：red_team 的腳本是否停留在「可能會被監管盯上」這類空泛層級，而非「拿去問律師的具體問題」？防禦 = sub-agents.md § red_team 輸出要求「具體到可以拿去問真實世界的律師/投資人」。
- [ ] **分支切換條件失靈**：branch_explorer 的 trigger_condition 是否可觀測、可觸發？若條件是「市場感覺變了」這類不可觀測描述，分支形同虛設。防禦 = trigger_condition 必須是具體可驗證事件。
- [ ] **小題大作**：決策複雜度低（無雙邊、無合規分歧、無跨法人）卻跑完整七層？防禦 = Hard rule 6 + `degradation-checkpoint.md`。降級走簡化鏈。
- [ ] **記憶庫未寫入**：phase 結束後是否跳過 manifest 寫入？防禦 = SKILL.md 記憶庫寫入步驟。不寫庫則跨決策重用與自我迭代斷鏈。
- [ ] **自我宣稱完成**：Orchestrator 是否未經 playbook_writer 就宣布方案定案？防禦 = Phase 6 必跑。決策靠驗證劇本，不靠推演說服。