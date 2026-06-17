---
name: sourced-kb-builder
description: A reusable method for turning scattered product/operations documents, design files, and tutorial videos into a clean, citation-grounded, queryable knowledge base — built once as Single-Source-of-Truth Markdown and served through two outputs (a no-code Q&A tool such as NotebookLM + a reusable Claude Skill). Use when someone wants to build an internal "ask-anything" assistant for ops/support/PM teams, consolidate messy docs into a sourced knowledge base, set up a low-maintenance monthly-updated KB, or wants the QA / integrity-audit / anti-hallucination workflow for a document Q&A system.
---

# Sourced Knowledge Base Builder

A battle-tested method for "growing" an assistant that answers questions about your product/operations **and cites where every answer came from**. Distilled from a real internal deployment (anonymized) that took ~300 scattered source files to a **97%-correct, zero-hallucination, fully-traceable** Q&A knowledge base.

This Skill is the **method**, not a specific knowledge base. Use it to build your own.

---

## The core idea (read this first)

> **Maintain ONE clean set of structured Markdown (the Single Source of Truth), and feed it to TWO outputs.**

1. **A no-code Q&A tool** (e.g. NotebookLM) — for non-technical teammates to ask questions by typing. Picked because it gives inline, click-back-to-source citations, has zero learning curve, and costs ~nothing.
2. **A reusable Claude Skill** (`SKILL.md` + `references/`) — for advanced queries and automation.

Update only the SSOT → both outputs stay in sync. Never maintain two copies of the truth.

**Four non-negotiable principles** (the source of the quality):
- **Extractive, not abstractive** — move and reorganize text; never paraphrase facts. Numbers, amounts, dates, rules, field names, status codes are copied **verbatim**. Abstractive summaries read nicely but hallucinate; for ops/spec knowledge, factual consistency beats fluency.
- **Per-section source tags** — every section starts with `> Source: {original-filename} | {date}`. This both improves retrieval (contextual retrieval) and lets the Q&A tool surface real provenance.
- **Time-ordering as conflict resolution** — when a topic has multiple versions, the **newest** wins; older versions only backfill gaps the new one didn't cover, with the evolution explicitly annotated.
- **Faithful-to-source ≠ correct** — source docs may contain drafts, cross-contaminated requirements, or unimplemented "vision" items. Verbatim consolidation drags these in. Only a domain expert sampling answers can catch them → recycle every catch into the regression test bank.

---

## The pipeline at a glance

Build it like training a new librarian: give clean material, then test, correct, and fill gaps.

| Stage | What | Reference |
|---|---|---|
| 0 | **Inventory & taxonomy** — list every source, flag empties/drafts/dupes, bucket topics mutually-exclusively | `references/02-technical-pipeline.md` |
| 1 | **Consolidate text** (parallel agents) — dedupe, time-order, extractive move, source-tag each section | `references/02-technical-pipeline.md` |
| 2 | **Videos → text** — scene-change frames + transcript → timestamped illustrated steps | `references/02-technical-pipeline.md` |
| 3 | **Design files → text** — REST API render of screens → read visually → write text specs | `references/02-technical-pipeline.md` |
| 4 | **Publish to the Q&A tool** — programmatic upload, split by audience | `references/05-qa-tool-gotchas.md` |
| 5 | **QA loop** — ask the most likely questions, grade vs. source, fix, re-test | `references/03-qa-and-audit.md` |
| 6 | **Integrity audit** — three-way cross-check to kill "source has it, KB missing it" gaps | `references/03-qa-and-audit.md` |
| ∞ | **Monthly update** — re-export, auto-refine, sync; human only arbitrates conflicts & samples | `references/04-monthly-update-sop.md` |

For the plain-language "why" and the tool-selection rationale, read `references/01-method-overview.md`.

---

## When you apply this Skill, do this

1. **Start with the overview** (`references/01-method-overview.md`) to confirm the approach fits the user's situation (do they need citations? non-technical audience? low maintenance?). If a fully-custom RAG or an enterprise search platform is genuinely warranted, say so.
2. **Inventory before building** — never start consolidating before Stage 0 taxonomy is done; it's what prevents the same file being processed twice.
3. **Enforce the four principles** on every consolidated file. The single most common failure is silently paraphrasing a number.
4. **Always run the QA loop and the integrity audit** before declaring done — "it answers" is not "it answers correctly and completely."
5. **Mind the Q&A-tool gotchas** (`references/05-qa-tool-gotchas.md`) — e.g. NotebookLM silently drops fenced code blocks; run `scripts/make_nlm_upload.py` on any file containing code/SQL/JSON before uploading.
6. **Hand off a monthly update SOP** — this is a living asset, not a one-shot deliverable.

## Reusable artifacts in this template
- `scripts/make_nlm_upload.py` — converts SSOT Markdown's fenced code blocks to plain-text-marked form so the Q&A tool can index SQL/commands verbatim. (Critical: see gotchas.)
- `references/03-qa-and-audit.md` — the QA grading rubric (✅/⚠️/❌) and the four-layer integrity audit.
- `references/04-monthly-update-sop.md` — the repeatable monthly refresh + CI-style coverage diff.

## Methodology sources
- Anthropic — *Contextual Retrieval* (prepend per-chunk context/source to cut retrieval failures).
- Anthropic — *Agent Skills best practices* (progressive disclosure: lean `SKILL.md` router + `references/` loaded on demand, avoid deep nesting).
- RAG chunking practice: Markdown is the most LLM-native format; heading-aware splitting beats fixed-length; extractive beats abstractive for lower hallucination.
