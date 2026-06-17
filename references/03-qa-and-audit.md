# 03 · QA Loop & Integrity Audit

The two quality gates that take a KB from "it answers" to "it answers correctly and completely." **Always run both before declaring done.**

---

## A. The QA loop (Stage 5)

### Method
1. **Write the questions your real audience would ask.** Start with the 30–60 most likely operational questions. Cover the boring-but-critical: exact numbers, sizes, status codes, edge cases, "who do I contact for X."
2. **Ask the Q&A tool programmatically** (e.g. `nlm notebook query`) so it's repeatable.
3. **Grade each answer against the original source** with a sub-agent, using a three-level rubric:

| Grade | Meaning |
|---|---|
| ✅ | Matches source, fully and correctly |
| ⚠️ | Partial — fact is in the cited passage but the synthesized answer omitted/softened it ("synthesis omission"), or it's vague |
| ❌ | Wrong / fabricated — contradicts source or invents facts |

4. **Fix, then re-test.** Drive ❌ to zero (no fabrication) and convert ⚠️ where possible.

### What the grades tell you
- **❌ (fabrication)** is the emergency. Common root causes: the tool can't retrieve a passage (see code-block gotcha in `05`), or two similar items got cross-contaminated. Fix the source, don't patch the prompt.
- **⚠️ "synthesis omission"** usually means the fact *is* retrievable — a follow-up question surfaces it. Acceptable in volume; not a content gap.

### Representative convergence (anonymized real runs)
- 30-question back-office audit: **67% → 97%** all-correct after one fix round.
- 109-question ops audit, three converging rounds: **✅93 / ⚠️16 / ❌0** (85%), hallucinations cleared to zero.
- The QA question bank becomes a **monthly regression test** — keep it as `master.json`.

### Fix patterns that recur
- **Cross-item contamination** (assistant mixes sizes/rules across similar items) → build ONE authoritative reference table as the single source of truth.
- **Pseudo-empty retrieval** (content exists but tool returns "not found") → almost always the code-block-dropping gotcha, or content buried mid-document where chunking skipped it (add a plain-text logic summary beside it).
- **Speculation as fact** → the source itself was a draft/contradiction; annotate ⚠️ and route to human arbitration, don't invent.

---

## B. Integrity audit (Stage 6)

**Purpose**: kill the "the source HAS it, but the KB is MISSING it" class of silent omissions. Triggered the first time a domain expert spots a feature the source documented but the KB dropped.

### The three-way cross-check
> **Original source ↔ Knowledge base ↔ live Q&A-tool test.**
> If any one side has it and another doesn't → that's a gap.

### Four detection layers
1. **Whole-feature gap** — a feature is entirely missing. Use the source's own table-of-contents/overview (e.g. a parent/child list in the spec CSV) as the master checklist.
2. **In-feature element gap** — a feature exists but a key field/option is missing. Prioritize known-fragile targets: list-import mechanisms, validation/anti-mistake rules.
3. **Pseudo-empty (retrieval gap)** — content is in the KB but the tool can't find it. Reverse-QA: ask specifically and confirm it surfaces.
4. **Orphan scan** — design pages whose file lives outside the main design project, image-only content, or unlinked parent items that were never collected.

### Run it as fan-out
Multiple agents scan different domains/files in parallel; collect findings into a single `findings-*.json` (severity high/med/low) + a `fix-list.md`. Then fix, re-upload, re-test.

### The hardest lesson: faithful ≠ correct
Source docs can contain **requirement-vision, cross-feature mis-pastes, or unimplemented items**. Verbatim consolidation drags them in. Examples seen in practice:
- A spec listed 4 options for a feature; the real product had only 2. The other 2 were planning vision / pasted from another feature.
- **Source contamination spreads to multiple files** — when you fix one, `grep` the whole KB for the same wrong passage; it was copied elsewhere too.

Only a **domain expert sampling answers** catches these. Every catch → add to the regression test bank so it can't regress.

### Arbitration backlog
Gaps that are drafts / self-contradictions in the *source itself* (e.g. a metric stated three inconsistent ways, a length constraint written differently in two places) can't be auto-filled. Keep a "to-confirm list," route to the product/eng owner, and once decided, backfill with a **"decided: {date}"** annotation.
