# Design — local-agent-pack

> 狀態：設計稿 v0.2（2026-09-12），供實作前審閱。
> 定位：給本地 agent 用的能力型 skills pack，不是單一 mega-skill。

## 0. 目標與邊界

### 目標

- 提供九個開箱即用的本地 agent 能力：
  1. `generate-image`
  2. `generate-video`
  3. `read-image`
  4. `read-video`
  5. `read-audio`
  6. `local-rag`
  7. `agent-memory`
  8. `generate-text`
  9. `generate-audio`
- 每個能力都是獨立 skill，可單獨安裝、單獨觸發、單獨升級。
- 共用一套 runtime adapter 與 storage schema，避免七份重複邏輯。
- **Phase 1 provider 明確鎖定 OpenRouter**，先完成 image / video / audio endpoint 對接，再開放其他 provider。
- 支援三種部署形態：
  1. **Skills-only**：只放 `SKILL.md`，agent 直接讀。
  2. **Plugin pack**：包成 `.codex-plugin` / marketplace entry。
  3. **MCP server**：把能力暴露成 tools，給支援 MCP 的 agent 使用。

### 非目標

- 不綁定任何單一 agent runtime。
- 不把所有能力塞進一個巨型 prompt。
- 不預設必須上雲。預設 local-first，雲端只是 adapter。
- 不做通用 agent framework，只做「能力 + 檔案 + 狀態」的最小可交付層。

## 1. 設計原則

1. **能力獨立，基礎共用**
   - 七個 skill 各自獨立，方便單獨觸發。
   - storage / provider / policy 共用，避免重複。

2. **Local-first**
   - 媒體讀取、索引、記憶優先使用本地工具。
   - 只有需要更強生成或理解時，才經 provider adapter 呼叫雲端。

3. **可驗收輸出**
   - 每個 skill 都有固定輸出契約。
   - 生成類輸出檔案 + metadata。
   - 理解類輸出結構化觀察 + 引用。

4. **可替換 provider**
   - skill 只定義「做什麼」，不定義「用哪個模型」。
   - provider 透過 adapter 註冊，未來換模型不改 skill。

5. **可降級**
   - 若模型不可用，至少回退到 metadata、OCR、ffmpeg、SQLite FTS。
   - 不允許無證據的幻覺輸出。

## 2. 架構

```text
User intent
    ↓
Skill trigger layer
  generate-image / generate-video
  read-image / read-video / read-audio
  local-rag / agent-memory
    ↓
Skill workflow layer
  fixed input → fixed steps → fixed output contract
    ↓
Capability adapter layer
  provider adapters: local model / cloud model / CLI tools
    ↓
Storage & state layer
  media store / rag index / memory store / logs
```

### 2.1 三層分離

1. **Skill 層**
   - 只描述「何時觸發、怎麼做、輸出什麼」。
   - 不直接綁定 provider。

2. **Adapter 層**
   - 定義統一能力介面。
   - 每個 provider 實作同一組 contract。

3. **Storage 層**
   - 統一放置生成物、索引、記憶與 log。
   - 支援 project-local 或 user-global 兩種 scope。

### 2.2 Phase 1 OpenRouter surface

Phase 1 不實作多 provider routing，只做一個 `openrouter` adapter，並把官方 endpoint 映射到 pack skills。
Adapter 支援模型探索、能力驗證、provider passthrough 預檢、text generation 與 TTS：

| Skill | OpenRouter endpoint | Mode |
|---|---|---|
| `generate-image` | `POST /api/v1/images` | Synchronous, base64 response |
| `generate-video` | `POST /api/v1/videos` + poll + download | Asynchronous job |
| `read-image` | `POST /api/v1/chat/completions` with `image_url` | Vision understanding |
| `read-video` | `POST /api/v1/chat/completions` with `video_url` | Video understanding |
| `read-audio` | `POST /api/v1/audio/transcriptions` | Dedicated STT |
| `read-audio` analysis mode | `POST /api/v1/chat/completions` with `input_audio` | Audio reasoning |
| `generate-text` | `POST /api/v1/chat/completions` | Text generation |
| `generate-audio` | `POST /api/v1/audio/speech` | TTS |
| model discovery | `/models`, `/images/models`, `/videos/models` | Capability discovery |

兼容策略：

1. OpenAI 使用 dedicated image/audio/chat endpoint。
2. Gemini 使用 vision/video/audio chat multimodal parts；local file 走 base64 data URL，public video 只允許 AI Studio route 支援的 YouTube URL。
3. Qwen 與 OpenAI 相容面走 generic text/vision chat completions。
4. MiniMax / Hailuo、Google Veo、Bytedance Seedance 走 `/videos` job state machine，並依模型 metadata 驗證 duration/resolution/aspect ratio/audio/frame input。
5. Input reference 能力依模型 metadata 判斷：image→image 檢查 image input modality 與 reference range；image→video 檢查 first/last frame metadata。text→image、text→video、image→image、image→video 為 Phase 1 支援矩陣。
6. Generic video→video editing 不在 Phase 1 generic contract 內；若模型需要影片參考，必須等 OpenRouter 提供統一欄位或新增 provider-specific adapter。
7. Provider 特有參數一律放在 `provider.options`，若有 `allowed_passthrough_parameters` 就先本地驗證。
8. Gemini agentic reasoning 保存在 artifact，可用 `--reasoning-file` 回傳續問。

完整 endpoint contract、request/response shape、error policy 與 privacy gate 在：

```text
references/openrouter.md
```

Phase 1 的本地狀態必須至少保存：

1. API request provenance：endpoint、model、usage、cost。
2. Video job state：`jobId`、`pollingUrl`、status、submittedAt。
3. Downloaded artifact：local path、media type、validation result。
4. Explicit cloud approval record.

## 3. 目錄結構

```text
local-agent-pack/
  pack.json
  generate-image/
    SKILL.md
    references/
  generate-video/
    SKILL.md
    references/
  read-image/
    SKILL.md
    references/
  read-video/
    SKILL.md
    references/
  read-audio/
    SKILL.md
    references/
  local-rag/
    SKILL.md
    references/
  agent-memory/
    SKILL.md
    references/
  shared/
    provider-contract.md
    storage-schema.md
    privacy-policy.md
    output-contract.md
  references/
    openrouter.md
  scripts/
    doctor.py
    providers/
    storage/
  templates/
    openrouter.config.json
    provider-config.json
    memory-record.schema.json
    rag-chunk.schema.json
```

### 3.1 `pack.json` 示意

```json
{
  "name": "local-agent-pack",
  "version": "0.1.0",
  "runtime": "agent-skills-v1",
  "skills": [
    "generate-image",
    "generate-video",
    "read-image",
    "read-video",
    "read-audio",
    "local-rag",
    "agent-memory"
  ],
  "capabilities": {
    "image-generation": ["local", "cloud"],
    "video-generation": ["local", "cloud"],
    "media-understanding": ["local", "cloud"],
    "retrieval": ["local"],
    "memory": ["local"]
  },
  "defaults": {
    "provider": "openrouter",
    "storageRoot": ".agents",
    "privacyMode": "local-first",
    "cloudApproval": "explicit"
  }
}
```

## 4. Skill 契約

每個 skill 的 `SKILL.md` 都應包含：

1. **Trigger**
   - 明確列出使用者會怎麼問。
   - 避免和相鄰 skill 混淆。

2. **Inputs**
   - 必填 / 選填參數。

3. **Workflow**
   - 固定步驟。
   - 模型不可用時的降級路徑。

4. **Output contract**
   - 固定欄位。
   - 引用來源或檔案。

5. **Provider**
   - 只依賴 adapter contract。
   - 不直接寫死模型名稱。

---

### 4.1 `generate-image`

#### 觸發

- 「幫我生一張圖」
- 「畫一個 icon / mockup / illustration」
- 「根據這張圖改成另一種風格」

#### 輸入

| 欄位 | 必填 | 說明 |
|------|------|------|
| prompt | 是 | 主題、風格、構圖 |
| aspectRatio | 否 | 預設 `1:1` |
| style | 否 | 攝影、插畫、UI、3D 等 |
| referenceImage | 否 | 圖生圖或編輯 |
| outputPath | 否 | 未指定則進 media store |

#### 流程

1. 判斷是「全新生成」還是「圖生圖 / 編輯」。
2. 組成 structured prompt：
   - subject
   - composition
   - style
   - lighting
   - quality
   - negative prompt
3. Phase 1 走 OpenRouter：
   - `POST /api/v1/images`
   - model 來自 `openrouter.config.json`
   - 先用 `/images/models/{model}/endpoints` 驗證參數
4. 生成圖片。
5. 驗證輸出：
   - 檔案存在
   - 可讀取
   - 尺寸正確
6. 寫入 metadata。

#### 輸出

```json
{
  "type": "image-generation",
  "outputPath": "media/images/xxx.png",
  "prompt": "...",
  "provider": "openrouter",
  "model": "...",
  "aspectRatio": "16:9",
  "seed": 123456,
  "createdAt": "2026-09-12T00:00:00Z"
}
```

#### 失敗模式

- Provider 不存在 → 提示安裝或改用 fallback。
- 檔案驗證失敗 → 不回報成功。
- 圖生圖超過尺寸限制 → 先降解析度或分區處理。

---

### 4.2 `generate-video`

#### 觸發

- 「幫我做一段影片」
- 「把這段 storyboard 變成 video」
- 「做一個 5 秒產品動畫」

#### 輸入

| 欄位 | 必填 | 說明 |
|------|------|------|
| storyboard | 是 | 鏡頭、節奏、文案 |
| duration | 否 | 預設 5 秒 |
| fps | 否 | 預設 24 |
| resolution | 否 | 預設 1080p |
| audio | 否 | 可選配音或音樂 |
| style | 否 | 動畫、電影感、產品演示 |

#### 流程

1. 把需求轉成 storyboard spec。
2. Phase 1 走 OpenRouter：
   - `POST /api/v1/videos`
   - 持久化 `jobId`、`pollingUrl` 與 status
   - poll `GET /api/v1/videos/{jobId}`
   - download `GET /api/v1/videos/{jobId}/content`
3. 生成 video。
4. 用 `ffprobe` 驗證：
   - duration
   - codec
   - fps
   - resolution
5. 若有音軌，驗證 audio stream。

#### 輸出

```json
{
  "type": "video-generation",
  "outputPath": "media/videos/xxx.mp4",
  "storyboard": "...",
  "provider": "openrouter",
  "model": "...",
  "duration": 5,
  "fps": 24,
  "resolution": "1920x1080",
  "createdAt": "2026-09-12T00:00:00Z"
}
```

#### 失敗模式

- Provider 不支援指定時長 → 提示可接受範圍。
- 影片驗證失敗 → 不回報成功。
- 只能生成圖片序列時，先交付 sequence，再問是否合成。

---

### 4.3 `read-image`

#### 觸發

- 「這張圖是什麼？」
- 「幫我 OCR」
- 「這張 UI 截圖有什麼問題？」
- 「這張圖表在講什麼？」

#### 輸入

| 欄位 | 必填 | 說明 |
|------|------|------|
| imagePath | 是 | 本地圖片路徑 |
| question | 否 | 使用者的問題 |
| detailLevel | 否 | `low` / `medium` / `high` |
| focus | 否 | `objects` / `text` / `chart` / `ui` |

#### 流程

1. 先用本地工具讀 metadata：
   - `sips`
   - `exiftool`
   - `identify`
2. 若需要 OCR，走 `tesseract` / `vision OCR`。
3. 若需要視覺理解，走 vision model。
4. 結果結構化：
   - objects
   - text
   - layout
   - colors
   - notable regions
5. 若使用者有問題，優先回答問題。

#### 輸出

```json
{
  "type": "image-reading",
  "inputPath": "input.png",
  "question": "...",
  "summary": "...",
  "observations": [
    {
      "kind": "text",
      "value": "...",
      "region": {"x": 0, "y": 0, "w": 100, "h": 20},
      "confidence": 0.94
    }
  ],
  "metadata": {
    "width": 1920,
    "height": 1080,
    "format": "png",
    "exif": {}
  }
}
```

#### 失敗模式

- 圖片過大 → 自動縮圖後再讀。
- OCR 不確定 → 標 confidence，不假裝確定。
- Vision model 不可用 → 只做 metadata + OCR，並明說限制。

---

### 4.4 `read-video`

#### 觸發

- 「這段影片在講什麼？」
- 「幫我整理這段影片重點」
- 「找出裡面有 logo 出現的時間點」

#### 輸入

| 欄位 | 必填 | 說明 |
|------|------|------|
| videoPath | 是 | 本地影片路徑 |
| question | 否 | 使用者的問題 |
| sampleRate | 否 | 每幾秒抽一幀 |
| focus | 否 | `scene` / `text` / `audio` / `motion` |

#### 流程

1. `ffprobe` 讀 metadata。
2. 抽關鍵幀。
3. 音訊轉 transcript。
4. OCR / shot detection。
5. 建立 timeline。
6. 依使用者問題合成摘要。

#### 輸出

```json
{
  "type": "video-reading",
  "inputPath": "input.mp4",
  "question": "...",
  "duration": 120,
  "scenes": [
    {
      "start": 0,
      "end": 10,
      "summary": "...",
      "objects": [],
      "text": [],
      "audio": "..."
    }
  ],
  "transcript": {
    "language": "zh",
    "segments": [
      {"start": 0, "end": 5, "text": "..."}
    ]
  }
}
```

#### 失敗模式

- 影片太長 → 先分段處理。
- 無音軌 → 只做視覺分析。
- 無法抽幀 → 只回 metadata，不硬編故事。

---

### 4.5 `read-audio`

#### 觸發

- 「這段錄音在說什麼？」
- 「幫我轉文字」
- 「這段音檔裡有誰在說話？」

#### 輸入

| 欄位 | 必填 | 說明 |
|------|------|------|
| audioPath | 是 | 本地音訊路徑 |
| question | 否 | 使用者的問題 |
| language | 否 | 自動偵測 |
| diarize | 否 | 是否區分說話者 |

#### 流程

1. `ffprobe` 讀 metadata。
2. Phase 1 轉 transcript 走 OpenRouter：
   - `POST /api/v1/audio/transcriptions`
   - `response_format: verbose_json`
   - 需要分析而非純轉文字時，改走 Chat Completions `input_audio`
3. 若需要，做 speaker diarization。
4. 依問題摘要。

#### 輸出

```json
{
  "type": "audio-reading",
  "inputPath": "input.m4a",
  "language": "zh",
  "duration": 90,
  "transcript": "...",
  "segments": [
    {"start": 0, "end": 10, "speaker": "S1", "text": "..."}
  ],
  "summary": "..."
}
```

#### 失敗模式

- ASR 不可用 → 只回 metadata，不編造內容。
- 語言混雜 → 分段處理。
- 說話者辨識失敗 → 保留 segment，但 speaker 欄位標 `unknown`。

---

### 4.6 `local-rag`

#### 觸發

- 「從我的文件裡找答案」
- 「幫我 index 這個資料夾」
- 「用本地資料回答」
- 「這個 repo 裡有沒有講 X」

#### 輸入

| 欄位 | 必填 | 說明 |
|------|------|------|
| corpusPath | 是 | 要索引的目錄或檔案 |
| query | 否 | 檢索問題 |
| filters | 否 | 副檔名、時間、路徑 |
| rerank | 否 | 是否 rerank |

#### 流程

1. Ingest：
   - documents
   - code
   - markdown
   - PDF
   - audio/video transcript
2. Chunk：
   - 依語意或段落
   - 保留 metadata
3. Index：
   - 首選 SQLite + FTS5
   - 可選 vector index
4. Retrieve：
   - keyword + vector hybrid
   - rerank
   - 回附引用

#### 輸出

```json
{
  "type": "rag-query",
  "query": "...",
  "answer": "...",
  "citations": [
    {
      "path": "docs/x.md",
      "start": 10,
      "end": 20,
      "score": 0.87
    }
  ]
}
```

#### 失敗模式

- 沒有索引 → 先建立，再回答。
- 檔案格式不支援 → 明說哪些被跳過。
- 沒有命中 → 回「沒找到」，不硬答。

---

### 4.7 `agent-memory`

#### 觸發

- 「記住我喜歡簡短回覆」
- 「這個專案上次決策是什麼？」
- 「更新你的長期記憶」
- 「忘記這件事」

#### 輸入

| 欄位 | 必填 | 說明 |
|------|------|------|
| action | 是 | `write` / `read` / `update` / `delete` |
| scope | 是 | `global` / `project` / `user` / `thread` |
| content | write/update 必填 | 記憶內容 |
| query | read 必填 | 檢索條件 |
| id | update/delete 必填 | 目標記憶 |

#### 流程

1. 判斷 scope。
2. 寫入或讀取 SQLite。
3. 保留 provenance：
   - source conversation
   - file
   - user instruction
4. 查詢時結合：
   - exact match
   - FTS
   - optional vector

#### 輸出

```json
{
  "type": "memory-write",
  "id": "mem_123",
  "scope": "project",
  "kind": "preference",
  "content": "Use concise bullet summaries.",
  "source": "conversation",
  "confidence": 0.9,
  "createdAt": "2026-09-12T00:00:00Z"
}
```

#### 失敗模式

- Scope 不明確 → 預設 `project`，不寫入 `global`。
- 內容含個人敏感資訊 → 先問是否要存。
- 查無結果 → 不猜測，回「沒有找到」。

## 5. Shared contracts

### 5.1 Provider contract

所有 provider 必須符合統一介面。

```text
image.generate(prompt, options) -> ImageResult
video.generate(storyboard, options) -> VideoResult
image.read(path, question, options) -> ImageReading
video.read(path, question, options) -> VideoReading
audio.read(path, question, options) -> AudioReading
rag.index(corpus, options) -> IndexResult
rag.query(question, options) -> RagResult
memory.write(record) -> MemoryId
memory.read(query, options) -> MemoryList
memory.update(id, patch) -> MemoryRecord
memory.delete(id) -> DeleteResult
```

### 5.2 Storage schema

#### Memory record

```json
{
  "id": "mem_123",
  "scope": "project",
  "kind": "preference",
  "content": "...",
  "confidence": 0.9,
  "source": {"type": "conversation", "uri": "..."},
  "createdAt": "...",
  "updatedAt": "...",
  "expiresAt": null
}
```

#### RAG chunk

```json
{
  "id": "chunk_123",
  "sourcePath": "docs/a.md",
  "start": 0,
  "end": 500,
  "text": "...",
  "embedding": null,
  "metadata": {"title": "..."}
}
```

### 5.3 Output contract

每個 skill 的回覆都應包含：

1. **結果摘要**
2. **檔案路徑或檢索引用**
3. **使用的 provider**
4. **限制**

## 6. Storage layout

Pack runtime artifacts use two compatible roots. The default is
project-local; the user-global root is opt-in for state that must be shared
across projects.

Default project-local:

```text
./.agents/
  media/
    images/
    videos/
    audio/
  artifacts/
  jobs/
    videos/
  approvals/
  indexes/
    rag/
      rag.sqlite3
  memory/
    working/
    semantic/
    episodic/
    procedural/
```

User-global opt-in:

```text
~/.agents/
  skills/           # installed skills, never runtime state
  media/
  artifacts/
  jobs/
  approvals/
  indexes/
  memory/
```

Selection rules:

1. `--storage-root ~/.agents` or a config value can select the global scope.
2. Project-local `.agents` remains the default so generated files stay near
   the project and are easy to ignore or delete.
3. `~/.agents/skills/` is reserved for skill installation; runtime must not
   overwrite or prune it.
4. Memory and indexes may use global scope only when their content is
   intentionally cross-project.

## 7. Privacy & permission

1. **Local-first**
   - 預設不上傳檔案。
   - 上雲需明確同意。

2. **Secrets**
   - API key 只放環境變數。
   - 不寫入 repo。

3. **Provenance**
   - 所有生成與理解結果都記錄 provider、模型、時間。
   - RAG 引用必須附 source path。

4. **Retention**
   - Memory 可設定 `expiresAt`。
   - 支援 `forget`。

## 8. Packaging

### 8.1 Skills-only

適合任何支援 `SKILL.md` 的 agent。

```text
local-agent-pack/
  generate-image/SKILL.md
  generate-video/SKILL.md
  read-image/SKILL.md
  read-video/SKILL.md
  read-audio/SKILL.md
  local-rag/SKILL.md
  agent-memory/SKILL.md
```

### 8.2 Codex plugin

適合 Codex App：

```text
local-agent-pack/
  .codex-plugin/
    plugin.json
  skills/
    generate-image/
    generate-video/
    read-image/
    read-video/
    read-audio/
    local-rag/
    agent-memory/
```

### 8.3 MCP server

適合支援 MCP 的 agent：

```text
local-agent-pack/
  mcp/
    server.py
    tools.json
```

## 9. 開發階段

### Phase 1：OpenRouter-first MVP

- 建 7 個 skill 目錄與 `SKILL.md`，觸發與輸出契約直接指向 OpenRouter adapter。
- 實作 shared contracts：
  - `provider-contract.md`
  - `storage-schema.md`
  - `privacy-policy.md`
- 實作 OpenRouter adapter：
  - `/images`
  - `/videos` submit / poll / download
  - `/chat/completions` image and video understanding
  - `/audio/transcriptions`
  - optional `/audio/speech`
- 建立 artifact 與 video job state schema。

### Phase 2：Local fallback runtime

- SQLite + FTS5
- `ffmpeg` / `ffprobe`
- `sips` / `exiftool`
- `tesseract`
- 基本 metadata 讀取

Phase 2 `local-rag` executable scope:

1. `scripts/rag.py index <corpus>`:
   - corpus manifest: relative path, size, mtime, SHA-256, language, indexedAt
   - incremental refresh and deletion of removed files
   - SQLite WAL mode and foreign-key cascading deletes
   - FTS5 trigram index for mixed English/Chinese retrieval
   - secret-like filenames and generated directories are excluded
2. `scripts/rag.py query <question>`:
   - FTS5 BM25 plus exact substring search
   - reciprocal-rank fusion
   - optional path filter
   - path/offset/heading/score citations
   - zero-result output is a valid successful retrieval, not a fabricated answer
3. Vector embeddings and local reranking remain deliberately out of Phase 2.
   The baseline must prove recall and citation precision before adding another index.

### Phase 3：Model and cost guardrails

- Model discovery caching
- endpoint capability validation
- cost estimate before request
- upload size gate
- explicit cloud approval record

### Phase 4：Other provider adapters

- local ComfyUI / SD
- local ASR
- OpenAI direct / Sora / Runway / Pika
- provider registry with per-capability routing

### Phase 5：Packaging

- `.codex-plugin`
- marketplace entry
- optional MCP server

### Phase 6：MVP 驗收

1. 在乾淨 project 中安裝 pack，設定 `OPENROUTER_API_KEY`。
2. OpenRouter 端到端完成：
   - `generate-image`：`/images` -> decode -> save -> validate
   - `generate-video`：submit -> poll -> download -> `ffprobe`
   - `read-image`：Chat Completions vision -> structured observation
   - `read-video`：Chat Completions video -> timeline summary
   - `read-audio`：`/audio/transcriptions` -> transcript + segments
3. 關閉 cloud approval 後驗證 local fallback：
   - `read-image`：metadata + OCR
   - `read-video`：metadata + 抽幀
   - `read-audio`：metadata only，明確拒絕編造 transcript
   - `local-rag`：SQLite FTS 查詢
   - `agent-memory`：寫入 / 讀取 / 刪除
4. 每個 skill 輸出一次固定格式 artifact，並記錄 provider / model / 路徑 / cost。

## 10. 待驗證假設

1. 七個 skill 是否足以涵蓋主要 local agent 媒體與記憶需求？
2. Provider adapter 是否夠穩定，能支援不同 runtime？
3. Local RAG 是否真的比直接 file search 更有價值？
4. Memory scope 是否需要更細的分層？
5. 是否需要把 `read-video` 拆成 `video-summary` / `video-search`？

## 11. 開放問題

1. Phase 2 之後是否要提供 `ComfyUI` workflow？
2. 是否需要支援 `LanceDB` / `Chroma` / `sqlite-vec`？
3. Memory 是否要引入 decay / conflict resolution？
4. Video generation 是否需要 pre-request cost estimate？
5. 是否要為每個 skill 建 `evals.json`？
