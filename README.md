# 知識庫訓練模板 · Knowledge Base Training Template

> 用最白話的方式，教你把一堆亂七八糟的文件，變成一個「有問必答、還會附出處」的小助理。
> 中文在前，English below ↓

---

# 中文說明（白話版）

## 這是什麼？用一個比喻

想像你有一間**沒有目錄的圖書館**：書（文件）散在好幾個櫃子、抽屜、甚至錄影帶裡，每次要找一句話都得翻半天，還只能去問館裡最資深的那位老員工。

這個模板教你做的事，就是**請一位數位圖書館員**：

- 你用打字問他問題，他馬上回答；
- 而且每個答案都會附上「我是從哪本書、哪一頁看到的」，讓你能翻回去核對。

重點：這個模板**不是那間圖書館本身**，而是**「怎麼訓練這位館員」的教學手冊**。你帶自己的書進來，照著做就好。

> 這套方法是從一個真實的內部專案整理出來的（已經把公司、產品、人名全部拿掉）。那個專案把大約 300 份散亂文件，變成一個 **97% 答對、不亂編、每句都能查出處**的問答系統。

## 一個最重要的觀念：一份正本，餵兩個嘴巴

很多人會犯的錯：替每個工具各做一份資料，結果三份資料各說各話，越維護越亂。

正確做法：

> **只養「一份」乾淨的正本（我們叫它 SSOT，單一真實來源），同時餵給「兩張嘴」：**
> 1. 一個**不用寫程式的問答工具**（例如 Google 的 NotebookLM）→ 給不懂技術的同事用打字問；
> 2. 一個**可以重複使用的 Claude Skill** → 給進階查詢和自動化用。
>
> 以後要改，**只改正本那一份**，兩張嘴自動同步、不會吵架。

## 四條鐵則（品質就靠這四條）

1. **照抄，不要自己重寫**：數字、金額、日期、規則一律一字不改地搬過來。為什麼？因為「重新講一遍」聽起來很順，但 AI 很容易講錯、甚至自己編。事實正確 > 文筆漂亮。
2. **每段都貼標籤說「我從哪來」**：像便利貼一樣，每一段開頭寫上來源檔名和日期。這樣 AI 才查得到、也才能附出處。
3. **新的蓋過舊的**：同一件事有好幾個版本時，**以最新的為準**，舊的只拿來補新的沒寫到的洞。
4. **「照著原文 ≠ 一定對」**：原始文件本身可能有寫錯、寫一半、或貼錯地方的內容。照抄會把錯也一起抄進來。所以**一定要找懂這個領域的人抽考**，抓到的錯就變成下次的考題。

## 怎麼做？七個步驟（像訓練新館員）

| 步驟 | 在做什麼（白話） |
|---|---|
| 0 | **清點家當**：把所有文件倒出來分類，挑掉空白頁、草稿、重複的 |
| 1 | **整併成一本乾淨的書**：去重、用新版、照抄、每段貼來源標籤 |
| 2 | **把教學影片變成文字**：一格一格看懂，寫成「圖文步驟」 |
| 3 | **把設計稿變成文字**：把只存在設計工具裡的畫面，讀懂後寫成文字規格 |
| 4 | **送進問答工具**：依不同對象分成不同「書庫」（例如營運一本、規格一本） |
| 5 | **考試訂正**：出最常被問的題目去考它，答錯/含糊的就修，再重考 |
| 6 | **完整性大檢查**：三方對照（原文 ↔ 知識庫 ↔ 實際問它），找出「原文有、它卻漏掉」的洞 |
| ∞ | **每月自動更新**：機器做苦工，人只負責「兩種說法時拍板」和「抽樣抽查」 |

## 一定要知道的一個大坑

NotebookLM 有個會**默默搞砸答案**的怪毛病：它會把用 ```` ``` ```` 框起來的程式碼區塊（SQL、指令、JSON）**整段丟掉、查不到**。結果就是 AI 答不出表格名稱，甚至自己**腦補假的 SQL**。

解法：含程式碼的檔案，上傳前先用 `scripts/make_nlm_upload.py` 跑一遍（把框框轉成純文字，內容一字不差）。其他坑都列在 `references/05-qa-tool-gotchas.md`。

## 檔案在哪、各做什麼

```
SKILL.md                          # 方法論主檔（路由 + 四條鐵則）
references/
  01-method-overview.md           # 白話「為什麼」+ 為什麼選這個工具
  02-technical-pipeline.md        # 技術版：架構 + 濃縮流程
  03-qa-and-audit.md              # 怎麼考試（✅/⚠️/❌）+ 四層完整性檢查
  04-monthly-update-sop.md        # 每月更新流程 + CI 式覆蓋率比對
  05-qa-tool-gotchas.md           # NotebookLM 會默默搞砸品質的坑
scripts/
  make_nlm_upload.py              # 把程式碼框轉純文字，讓 NotebookLM 查得到 SQL/指令
```

## 怎麼當成 Claude Skill 來用

```bash
git clone https://github.com/DennisWei9898/knowledge-base-training-template.git
cp -r knowledge-base-training-template ~/.claude/skills/sourced-kb-builder
```

之後在任何 Claude Code 對話裡說「幫我建一個可溯源的知識庫」或「把這些文件整併成可問答的 KB」，Skill 就會帶著你做。**你出書（放在 `knowledge/` 資料夾），模板出方法。**

## 這套方法參考了哪些 Claude 官方文章（索引）

這套做法不是憑感覺，而是對照 Anthropic（Claude）官方的兩篇方法論：

1. **Contextual Retrieval（脈絡式檢索）** — 在每段前面貼上「來源/脈絡」標籤，官方實測能讓檢索失敗率降低約 35%。這就是上面鐵則 2 的根據。
   👉 https://www.anthropic.com/news/contextual-retrieval
2. **Agent Skills best practices（Skill 最佳實踐：漸進式揭露）** — 入口檔保持精簡只做「路由」，細節放 `references/` 按需載入，不要堆太多層。這就是本模板 `SKILL.md` + `references/` 結構的根據。
   👉 https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

# English

A reusable, **tool-agnostic method** for turning scattered product/operations documents, design files, and tutorial videos into a clean, **citation-grounded, queryable knowledge base** — so non-technical teammates can ask questions by typing and every answer cites its source.

Think of it as **a manual for training a digital librarian**: you bring your own books (docs), and the assistant answers questions while always pointing back to the exact source. This template is the *training manual*, not anyone's actual library.

It is packaged as a [Claude Skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) (`SKILL.md` + `references/`), but the method works regardless of which assistant you use.

> Distilled and anonymized from a real internal deployment that took ~300 scattered source files to a **97%-correct, zero-hallucination, fully-traceable** Q&A knowledge base. All company-, product-, and person-specific data has been removed.

## The one idea: one source, two mouths

> **Keep ONE clean Single Source of Truth (SSOT) in Markdown, and feed it to TWO outputs:**
> 1. a **no-code Q&A tool** (e.g. NotebookLM) for non-technical staff, and
> 2. a **reusable Claude Skill** for advanced queries & automation.
>
> Edit one place → both stay in sync, and never contradict each other.

## Four iron rules (this is where the quality comes from)

1. **Copy verbatim, don't rewrite.** Numbers, amounts, dates, rules are moved word-for-word. Paraphrasing reads nicely but makes AI hallucinate. Facts > fluency.
2. **Tag every section with "where I came from."** Each section opens with its source file + date — this is what makes answers retrievable and citable.
3. **Newest wins.** When a topic has many versions, the latest is authoritative; older ones only backfill gaps.
4. **"Faithful to source ≠ correct."** Sources can contain drafts, mis-pastes, and unbuilt "vision" items. Only a domain expert sampling answers catches these — every catch becomes a regression test.

## The pipeline (like training a new librarian)

| Stage | What |
|---|---|
| 0 | Inventory & taxonomy (drop empties/drafts/dupes; mutually-exclusive buckets) |
| 1 | Consolidate text — dedupe, newest-wins, copy verbatim, source-tag each section |
| 2 | Videos → timestamped illustrated steps |
| 3 | Design files → text specs (via REST API render + visual reading) |
| 4 | Publish to the Q&A tool (split by audience) |
| 5 | QA loop — ask likely questions, grade ✅/⚠️/❌, fix, re-test |
| 6 | Integrity audit — three-way cross-check (source ↔ KB ↔ live test) |
| ∞ | Monthly auto-update; humans only arbitrate conflicts & sample |

## The single biggest gotcha

NotebookLM **silently drops fenced code blocks from retrieval**. Run any file containing SQL/JSON/commands through `scripts/make_nlm_upload.py` before uploading, or the assistant will fail those questions and may hallucinate fake SQL. Full list in `references/05-qa-tool-gotchas.md`.

## Repository layout

```
SKILL.md                          # the method skill (router + the four rules)
references/01..05                  # overview, pipeline, QA/audit, monthly SOP, gotchas
scripts/make_nlm_upload.py         # un-fence code blocks so NotebookLM can index SQL/commands
```

## Use it as a Claude Skill

```bash
git clone https://github.com/DennisWei9898/knowledge-base-training-template.git
cp -r knowledge-base-training-template ~/.claude/skills/sourced-kb-builder
```

Then ask Claude Code to "build a sourced knowledge base." You supply the sources; the template supplies the method, the QA/audit gates, and the upload tooling.

## Reference articles this method is built on (index)

This isn't guesswork — it maps to two official Anthropic (Claude) methods:

1. **Contextual Retrieval** — prepend per-chunk context/source to cut retrieval failures (~35% in Anthropic's tests). The basis for iron rule #2.
   👉 https://www.anthropic.com/news/contextual-retrieval
2. **Agent Skills best practices** — progressive disclosure: a lean router file + `references/` loaded on demand. The basis for this template's structure.
   👉 https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## 作者與聯絡 · Author & contact

**Dennis Wei**
- GitHub: [@DennisWei9898](https://github.com/DennisWei9898)
- Email: dennis.xd.wei@gmail.com
- LinkedIn: [dennis-wei](https://www.linkedin.com/in/dennis-wei-47393a14a/)

## 授權 · License

[MIT](./LICENSE) — free to use, adapt, and share.
