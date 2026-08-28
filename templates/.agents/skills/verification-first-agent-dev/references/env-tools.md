# 環境工具對照：讓 Agent 能自己跑驗證

驗證權交給 agent 的第三個前置條件：環境允許它跑。每種項目形態，給 agent 什麼能力。

| 項目形態 | 給 agent 的工具面 | 驗證動作 | 斷言看什麼 |
|---|---|---|---|
| Web | Chrome DevTools Protocol (CDP) | 自己打開頁面、點按鈕、讀 DOM | DOM 結構 + Console 無新錯誤 + Network 響應 |
| Web（性能） | CDP Performance / Trace | 抓 Performance Trace、Heap Snapshot | 具體指標（LCP、memory 曲線），不是「感覺變快」 |
| iOS | Simulator + 可調用工具 | 啟動 app、點擊、截圖、讀日誌 | 截圖比對 + 日誌關鍵字 |
| CLI | shell 執行權 | 自己執行命令 | stdout 內容 + stderr + exit code（三者都查，exit 0 不夠） |
| Electron / 桌面 | 啟動 dev 版 + 截圖 + 日誌讀取 | 啟動、操作、截圖、讀主進程日誌 | 截圖狀態 + 日誌斷言 |
| 庫 / SDK | 測試 runner | 跑單元/集成測試 | 斷言數與內容（不是「測試全綠」一句話） |

## 給權限的原則

1. **寧給工具，不給截圖循環**。人截圖餵 agent = 人還在循環裡。讓 agent 自己截。
2. **斷言三查**：exit code / stdout / stderr 都要看。只查 exit code 是假綠。
3. **性能與資源**必須是數字斷言（trace 指標、heap 大小），「應該快」不可驗證。
4. **瀏覽器 agent 推薦**：給 agent 一個可操作瀏覽器的能力（如 CDP 系工具），而不是讓它「想像」頁面長什麼樣。

## 反模式

- 讓 agent「寫完告訴我你測過了」——自我宣稱完成不是驗證（`agentic-clean-discipline` 的驗證者不得是生成者，同理）。
- 只在 happy path 斷言。邊界（空輸入、中文、大數據量）才是 agent 最容易錯的地方。
- 驗證劇本裡出現「人工確認」步驟——那一步就是驗證權還在人手上的殘留；要麼轉成可機器斷言，要麼明確標出這是人驗收點（且越少越好）。