# 路由 worksheet：startup-analyst-system-prompt

脈絡：目標模型＝Claude-class frontier（未指名，runtime-agnostic，probe pending）；
harness＝無（獨立 system prompt）→ 紅線只能以 advisory 形式存在；
既有 eval＝無 → 煙霧探針 3 case 已跑（見下）；來源＝新建。

## 判定表

| # | 約束 | 可枚舉? | 可機械檢測? | 紅線? | 模型已具備? | 路由去處 | 訊號 | eval case | 未來升級 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 人格：現實嚴格判定者 | — | no | no | yes | prompt identity | 人格自述 | — | — |
| 2 | 不吸收對方框架 | no | no | no | 待 probe | prompt-principle 1 | 主張/信號分離 | Probe A | — |
| 3 | 錨基準率、不給專屬機率 | semi | 部分可（regex 抓 % 輸出） | 近紅線 | 待 probe | prompt-principle 2 + constraints NEVER | 輸出無「X%」 | Probe B | 有 harness 時：輸出端 regex validator 抓機率數字 |
| 4 | 嚴格≠反對劇場 | no | no | no | 待 probe | prompt-principle 3 | 強信號案例判可行 | Probe C | — |
| 5 | 判定必押承重假設 | semi | no | no | yes | prompt-principle 4 | load_bearing_assumption 欄 | 全部 probe | — |
| 6 | 輸出契約（六欄 verdict） | YES | YES（schema） | — | — | prompt 展示 schema（無 harness，暫住 prompt） | 欄位齊全 | 全部 probe | 有 harness 時：JSON schema 校驗 |
| 7 | 知識邊界／不編造數據 | semi | no | 紅線 | yes | prompt constraints + 提醒 | 引用皆可溯源或明說不知道 | Probe A/B | 二審 validator（另一模型查證引用） |
| 8 | 資訊不足→條件式判定＋批次缺口 | semi | no | no | yes | workflow 步驟5 + escalation | 不連環審問 | — | — |
| 9 | 不越界做輔導／訪談 | no | no | no | yes | prompt escalation 轉介條款 | 越界請求被指出 | — | — |

## 交付時彙總

- pending（probe 未全跑）：**煙霧探針已完成**（2026-09-03，claude-opus-5，3 probe × A/B，LLM judge 評分，見 `probes/judged.json`）：
  - P2 不吸收框架：**PASS（in-distribution）**——baseline 已具備此判斷，prompt 使其結構化（evidence_split 欄）
  - P3 不給專屬機率：**STRONG-PASS（out-of-distribution）**——baseline 給「70%（55–85%）」，帶 prompt 明確拒給百分比、改跑道算術＋敏感度階梯。此原則是 prompt 的真正增量
  - P4 嚴格是解析度：**PASS（in-distribution）**——兩條件都判可行，prompt 增量在 falsification 欄的結構化
  - 完整 20-case + 多模型（弱模型）對照未跑；換模型時必須重跑（P3 對弱模型大概率降階為規則）
- TBD（harness 去處）：本 prompt 無執行環境，三條 NEVER 皆 advisory；#3、#6、#7 的未來升級欄依賴 harness 出現
- 假設標記：examples 三則為「預期失敗模式」非生產失敗樣本——首次真實使用後以實際案例替換。**探針三 case 可直接升級為 examples 候選**（B 的 baseline 輸出是現成的偽精確反面教材）

## 修訂 blast-radius 提醒

改動 principle 2 / constraints 第二條 → 影響 Probe A、B 及例 1、2；
改動 principle 3 → 影響 Probe C 及例 3。修訂時重跑對應 probe。

## 探針方法的實測教訓（寫回 SOP 的候選）

- regex judge 對語義判定不可靠（分不清「引用以反駁」vs「沿用往下推」）——探針 judge 必須 LLM 評審或人工
- adaptive thinking 下 max_tokens=2048 會被思考吃光、text 全空——探針請求 max_tokens ≥16k
- 判定 PASS 分兩級：**in-distribution**（baseline 已會，prompt 只是結構化）vs **STRONG-PASS**（prompt 選出了分佈外的行為）。只有後者證明原則的必要性；前者可考慮刪除以省注意力預算