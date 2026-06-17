# 知識庫訓練模板 · Knowledge Base Training Template

> 中文說明在前，English below ↓

---

# 中文說明

一套**與工具無關、可重複套用的方法**，把散落各處的產品／營運文件、設計稿、教學影片，整理成乾淨、**逐段可溯源、可問答**的知識庫——讓非技術同事用打字就能查到答案，而且每個答案都附上「這是從哪份文件來的」。

本模板打包成一個 [Claude Skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)（`SKILL.md` + `references/`），但方法本身與你用哪個 AI 助理無關。

> 萃取並去敏自一個真實的內部專案：約 300 份散落來源，最終做到 **97% 正確、零捏造、逐句可溯源**的問答知識庫。所有公司、產品、人員相關資料都已移除——這裡放的是**方法**，不是任何人的實際知識庫內容。

## 一個核心觀念

> **維護「一份」乾淨的結構化 Markdown（單一真實來源 SSOT），同時餵給「兩個」出口：**
> 1. 一個**零程式碼問答工具**（例如 NotebookLM），給非技術同事用；
> 2. 一個**可重用的 Claude Skill**，給進階查詢與自動化。
>
> 更新只改一處 → 兩邊同步，永不各說各話。

四個不可妥協的原則撐起品質：**逐字搬運（extractive）不改寫摘要**、**每段標來源**、**新版優先的時序去重**、以及**「忠於原文 ≠ 正確」——靠領域專家抽測驗證**。

## 建置流程

| 階段 | 內容 |
|---|---|
| 0 | 盤點與分類（互斥分桶，避免重複處理） |
| 1 | 文字整併——去重、時序去重、逐字搬運、每段埋來源標籤 |
| 2 | 影片 → 帶時間戳的圖文步驟 |
| 3 | 設計稿 → 文字規格（REST API render + 視覺判讀） |
| 4 | 上線到問答工具（依受眾分本） |
| 5 | QA 驗收——出題、評分 ✅/⚠️/❌、修正、重測 |
| 6 | 完整性稽核——三方交叉比對（來源 ↔ 知識庫 ↔ 實測） |
| ∞ | 每月自動更新；人工只做矛盾裁決與抽樣 |

## 檔案結構

```
SKILL.md                          # 方法論 Skill（路由 + 四大原則）
references/
  01-method-overview.md           # 白話版「為什麼」+ 工具選型理由
  02-technical-pipeline.md        # 架構 + 濃縮管線
  03-qa-and-audit.md              # QA 評分量表 + 四層完整性稽核
  04-monthly-update-sop.md        # 每月更新 SOP + CI 式覆蓋率 diff
  05-qa-tool-gotchas.md           # NotebookLM 會默默搞砸品質的坑
scripts/
  make_nlm_upload.py              # 把 code block 轉純文字，讓 NotebookLM 能檢索 SQL/指令
```

## 當成 Claude Skill 使用

```bash
git clone https://github.com/DennisWei9898/knowledge-base-training-template.git
cp -r knowledge-base-training-template ~/.claude/skills/sourced-kb-builder
```

之後在任何 Claude Code session 說「幫我建一個可溯源的知識庫」／「把這些文件整併成可問答的 KB」，Skill 的方法就會引導你完成。你提供自己的來源（放在 `knowledge/` 樹下）；本模板提供方法、QA／稽核關卡，以及上傳工具。

## 最重要的一個坑

NotebookLM 會**默默把 ```` ``` ```` 程式碼區塊丟出檢索層**。含 SQL／JSON／指令的檔案，上傳前一定要先過 `scripts/make_nlm_upload.py`，否則助理會答不出那些問題、甚至腦補假 SQL。完整清單見 `references/05-qa-tool-gotchas.md`。

---

# English

A reusable, **tool-agnostic method** for turning scattered product/operations documents, design files, and tutorial videos into a clean, **citation-grounded, queryable knowledge base** — so non-technical teammates can ask questions by typing and every answer cites its source.

It is packaged as a [Claude Skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) (`SKILL.md` + `references/`), but the method works regardless of which assistant you use.

> Distilled and anonymized from a real internal deployment that took ~300 scattered source files to a **97%-correct, zero-hallucination, fully-traceable** Q&A knowledge base. All company-, product-, and person-specific data has been removed — this is the *method*, not anyone's actual knowledge base.

## The one idea

> **Maintain ONE clean set of structured Markdown (the Single Source of Truth), and feed it to TWO outputs:**
> 1. a **no-code Q&A tool** (e.g. NotebookLM) for non-technical staff, and
> 2. a **reusable Claude Skill** for advanced queries & automation.
>
> Update one place → both stay in sync.

Four non-negotiable principles drive the quality: **extractive (verbatim) not abstractive**, **per-section source tags**, **newest-version-wins conflict resolution**, and **"faithful-to-source ≠ correct" — verify with a domain expert.**

## The pipeline

| Stage | What |
|---|---|
| 0 | Inventory & taxonomy (mutually-exclusive topic buckets) |
| 1 | Consolidate text — dedupe, time-order, extractive move, source-tag |
| 2 | Videos → timestamped illustrated steps |
| 3 | Design files → text specs (via REST API render + visual reading) |
| 4 | Publish to the Q&A tool (split by audience) |
| 5 | QA loop — ask likely questions, grade ✅/⚠️/❌, fix, re-test |
| 6 | Integrity audit — three-way cross-check (source ↔ KB ↔ live test) |
| ∞ | Monthly auto-update; human only arbitrates & samples |

## Repository layout

```
SKILL.md                          # the method skill (router + principles)
references/
  01-method-overview.md           # plain-language "why" + tool-selection rationale
  02-technical-pipeline.md        # architecture + the condensing pipeline
  03-qa-and-audit.md              # QA grading rubric + four-layer integrity audit
  04-monthly-update-sop.md        # repeatable monthly refresh + CI-style coverage diff
  05-qa-tool-gotchas.md           # NotebookLM quirks that silently wreck quality
scripts/
  make_nlm_upload.py              # un-fence code blocks so NotebookLM can index SQL/commands
```

## Use it as a Claude Skill

```bash
git clone https://github.com/DennisWei9898/knowledge-base-training-template.git
cp -r knowledge-base-training-template ~/.claude/skills/sourced-kb-builder
```

Then in any Claude Code session, ask to "build a sourced knowledge base" / "consolidate these docs into a queryable KB" and the Skill's method will guide the build. You supply your own sources under a `knowledge/` tree; this template supplies the method, the QA/audit gates, and the upload tooling.

## The single most important gotcha

NotebookLM **silently drops fenced code blocks from retrieval**. Run any file containing SQL/JSON/commands through `scripts/make_nlm_upload.py` before uploading, or the assistant will fail those questions and may hallucinate fake SQL. Full list of quirks in `references/05-qa-tool-gotchas.md`.

---

## 作者與聯絡 · Author & contact

**Dennis Wei**
- GitHub: [@DennisWei9898](https://github.com/DennisWei9898)
- Email: dennis.xd.wei@gmail.com
- LinkedIn: [dennis-wei](https://www.linkedin.com/in/dennis-wei-47393a14a/)

## 授權 · License

[MIT](./LICENSE) — free to use, adapt, and share.
