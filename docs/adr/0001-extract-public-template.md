# ADR 0001 — 從真實知識庫專案萃取成公開模板

- **狀態 (Status)**：已採納 (Accepted)
- **日期 (Date)**：2026-06-17
- **作者 (Author)**：Dennis Wei
- **對應討論**：GitHub issue [#1](https://github.com/DennisWei9898/knowledge-base-training-template/issues/1)（保留作為公開討論入口；本檔為正式紀錄）

> ADR = Architecture Decision Record（架構決策紀錄）。記錄「當初為什麼這樣決定」，方便日後維護與外部讀者理解設計理由。

---

## 背景 (Context)

本模板萃取自一個真實的內部「產品/營運知識庫」專案（已完全去敏）。原專案把約 300 份散落來源，做到 **97% 正確、零捏造、逐句可溯源**的問答 KB，方法被驗證有效。目標：把這套方法變成任何人都能套用的**公開模板**，而非外流任何實際內容。

## 決策 (Decision)

### 1. 形式：打包成 Claude Skill，而非純文件
- `SKILL.md` 當路由入口（漸進式揭露），細節放 `references/` 按需載入。
- 理由：可直接 `cp` 到 `~/.claude/skills/` 使用；對人類也是可讀文件。

### 2. 內容：只搬方法論，不搬知識庫本體
- 只放「怎麼做」（流程、原則、QA/稽核關卡、踩坑），不放任何實際領域內容。
- 真實數據改寫為「匿名案例（數字僅供示意）」。

### 3. 去敏範圍（已逐詞 + 子字串雙重掃描驗證零洩漏）
- 移除：公司/產品名、人員代號、NotebookLM/Figma ID、API token、領域專名（券種、搖珠珠、載具、OP單等）。
- 保留：與工具無關的方法價值（一源兩出口 SSOT、extractive 逐字、時序去重、忠於原文≠正確、NotebookLM code-block 被丟棄的踩坑）。

### 4. 授權與聯絡
- MIT License。
- README 附 Gmail / GitHub / LinkedIn；明確排除公司信箱。

### 5. README 雙語 + ELI5
- 中文在前、英文在後（2026-06-17）。
- 全面白話化（圖書館員比喻），降低閱讀門檻（2026-06-17）。

### 6. 索引保留方法論出處
- 在 `SKILL.md` 與 README 索引保留兩篇 Anthropic 官方來源連結：
  - Contextual Retrieval — https://www.anthropic.com/news/contextual-retrieval
  - Agent Skills best practices — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

### 7. 決策紀錄放 repo 檔案（本檔），而非只靠 issue
- 理由：issue 語意是「待辦/會關閉」，ADR 是「長存歷史」，更適合進版控與程式碼一起保存。issue #1 保留作為公開討論入口。

## 結果與後續 (Consequences)

- `scripts/make_nlm_upload.py` 已通用化（加 `--out`，輸出預設 `./upload`）。
- 若 NotebookLM 行為改變，需回頭更新 `references/05-qa-tool-gotchas.md`。
- 方法與工具無關，但 Stage 4/5 指令為 NotebookLM 專屬；換工具需重測那五個 gotcha。
- 未來若新增重大決策，新增 `docs/adr/0002-*.md` 接續編號。
