# 02 · Technical Pipeline — how to condense raw material into a queryable KB

> For the technical lead: the architecture decision, the Anthropic methods the refinement borrows from, and the concrete pipeline for condensing raw material into a sourced, queryable knowledge base.

---

## 1. Goal & architecture decision

**Goal**: consolidate scattered product docs / design files / tutorial videos into a knowledge base that is **LLM-queryable with per-section traceability**, for non-technical staff to self-serve.

**Selection**: a no-code Q&A tool with native inline citations (NotebookLM in the reference deployment) as the primary output — picked for claim-level citations, zero learning curve, near-zero cost. (See `01-method-overview.md` for the full comparison.)

**Core architecture: Single Source of Truth, one source two outputs**
- Maintain one structured Markdown tree (`knowledge/`) feeding both:
  1. the Q&A tool (uploaded as sources), and
  2. reusable reference files (advanced queries / automation).
- Update one place, both outputs sync.

---

## 2. Source universe (generalize to your own)

A real deployment drew from three modalities — adapt the categories to yours:

### Text (Markdown exported from a notes/wiki tool)
- Operations SOPs, back-office specs, product requirement docs (current + historical).
- Treat current-version docs as authoritative; keep historical exports only as backward-compatible gap-fill.

### Design files (via a design tool's REST API)
- Back-office module designs and app-side product designs.
- Plus design files cross-referenced from inside the text docs (dedupe by file key).

### Videos (screen recordings)
- Operation tutorials and back-office setup recordings (mp4/mov).

---

## 3. Refinement method — which Anthropic methods it borrows

Refinement isn't by feel; it maps to documented methods:

### 1. Per-chunk source/context tag → Anthropic *Contextual Retrieval*
- Source: Anthropic, *Contextual Retrieval* (anthropic.com/news/contextual-retrieval).
- Principle: prepend each chunk with "what context this is in / which file it came from" to materially cut retrieval-failure rate.
- Our landing: each subsection opens with `> Source: {original-filename} | {date}`. This both improves retrieval hit-rate and lets the Q&A tool surface real provenance (NotebookLM's inline citation only resolves to the *source file* level, so finer provenance must be embedded by us).

### 2. KB structure → Anthropic *Agent Skills: Progressive Disclosure*
- Principle: keep the entry file (`SKILL.md`) lean and purely a router (which file to read for which question); push detail into `references/`, loaded on demand; avoid deep nested references.
- Our landing: `SKILL.md` (routing table + glossary) + `knowledge/{domain}/{topic}.md` (two levels, not deeper).

### 3. Document format & splitting → RAG chunking best practice
- Markdown is the most LLM-native format (token efficiency, retrieval accuracy).
- Use **heading-aware** structure (H2/H3 = subtopics) so retrieval splits on heading boundaries — better than fixed-length.
- Numbers / rules / status codes go in **tables** (pipe tables are unambiguous to models).

### 4. Extractive, not abstractive (deliberate)
- **Move + reorganize, don't rewrite-summarize.** Numbers, amounts, dates, rules, field names, status codes are kept verbatim; only repetitive prose is compressed.
- Why: abstractive summaries are fluent but hallucination-prone; for ops/spec KBs, factual consistency > prose fluency.

### 5. Time-ordering as conflict resolution
- For multi-version topics, **newest timestamp wins**; older backfills only uncovered gaps, with the evolution explicitly annotated (e.g. "Feature A was replaced by Feature B", "the unified rule is still a draft; current behavior is X").

---

## 4. Condensing pipeline (the technical flow)

Run it with **multi-agent parallel orchestration** — each stage fans out to sub-agents, then aggregates.

### Stage 0 | Inventory & taxonomy
- Classify all files; flag shells / drafts / duplicates (only the content-bearing ones proceed).
- Do **mutually-exclusive bucketing** (first-match by topic) so the same file isn't processed by multiple consolidation agents.

### Stage 1 | Text consolidation (parallel agents)
- One consolidation agent per topic bucket: read source files (incl. frontmatter dates) → dedupe / time-order dedupe → extractive move → embed a source tag per section → output `spec-{topic}.md`.
- Strict rules: complementary not duplicated (don't re-copy UI already written in a design-file doc); don't force-fill drafts/contradictions — list them for human arbitration.

### Stage 2 | Video → text
- Per video, extract scene-change frames + a timestamped transcript; read the on-screen UI actions visually → produce timestamped illustrated steps (works even for narration-free recordings).

### Stage 3 | Design files (e.g. Figma) → text
- Pipeline using the design tool's REST API (no manual screenshots):
  1. `GET /v1/files/{key}?depth=4` — get canvas → frame `name` and node id.
  2. **Dedupe**: keep one representative per same-named frame; skip pure components / annotations / covers.
  3. `GET /v1/images/{key}?ids=...&format=png&scale=1|2` — render representative screens to PNG (re-fetch small text at scale=2).
  4. Read PNG visually → write text spec (fields, tabs, buttons, flows, error messages).
- On rate-limit (HTTP 429): sleep and retry.
- **Security**: keep API tokens out of any committed file; pass them at runtime and rotate after use.

### Stage 4 | Publish to the Q&A tool
- Upload programmatically (e.g. NotebookLM's `nlm` CLI: `nlm notebook create`, `nlm source add <notebook-id> --file <f> --wait`).
- Split into separate notebooks by audience (ops vs. back-office spec).
- **Critical gotchas live in `05-qa-tool-gotchas.md`** — especially: the tool drops fenced code blocks, so run `scripts/make_nlm_upload.py` first on any file with code/SQL/JSON.

### Stage 5 | QA loop
See `03-qa-and-audit.md`. Write the most-likely questions → ask programmatically → sub-agents grade each answer vs. source as ✅/⚠️/❌ → fix → re-test.

### Stage 6 | Integrity audit
See `03-qa-and-audit.md`. Three-way cross-check (source ↔ KB ↔ live test), four layers of gap detection.

---

## 5. Implementation notes worth keeping
- **CSV export BOM**: notes-tool CSV exports often carry a UTF-8 BOM in the header — read with `encoding='utf-8-sig'` when clustering.
- **Spreadsheet sources**: API/spec data living in Excel is converted with `openpyxl` (iterate rows → name + method + path + params + response), re-run on each update (it's not a notes-tool export).
- **Orchestration scripts**: in some sandboxed workflow runners `require('fs')` / Node FS is unavailable — keep scripts dependency-light.
- **Don't trust agent reports blindly** — verify a sampling against source before believing "done."
