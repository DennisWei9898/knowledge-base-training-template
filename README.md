# Knowledge Base Training Template

A reusable, **tool-agnostic method** for turning scattered product/operations documents, design files, and tutorial videos into a clean, **citation-grounded, queryable knowledge base** — so non-technical teammates can ask questions by typing and every answer cites its source.

It is packaged as a [Claude Skill](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) (`SKILL.md` + `references/`), but the method works regardless of which assistant you use.

> Distilled and anonymized from a real internal deployment that took ~300 scattered source files to a **97%-correct, zero-hallucination, fully-traceable** Q&A knowledge base. All company-, product-, and person-specific data has been removed — this is the *method*, not anyone's actual knowledge base.

---

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

## Author & contact

**Dennis Wei**
- GitHub: [@DennisWei9898](https://github.com/DennisWei9898)
- Email: dennis.xd.wei@gmail.com
- LinkedIn: [dennis-wei](https://www.linkedin.com/in/dennis-wei-47393a14a/)

## License

[MIT](./LICENSE) — free to use, adapt, and share.
