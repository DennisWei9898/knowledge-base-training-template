# 01 · Method Overview — how we "grow" an assistant that answers with citations

> One sentence: turn scattered product docs, design files, and tutorial videos into a clean, **sourced**, AI-queryable knowledge base, so non-technical teammates can find answers just by typing — and every answer comes with "which document this came from."

---

## 1. The problem we solve

Looking up product knowledge used to be like **finding one sentence in a library with no catalog**:

- Docs scattered across several places (a notes app, a design tool, tutorial videos), no single entrance.
- Newcomers can only ask senior teammates; senior teammates are busy.
- The same thing often has several versions — nobody knows which is the latest/correct one.

Result: **knowledge is stuck in a few people's heads; asked once, answered once, never accumulates.**

Goal: hire an **always-online, always-answering, always-cites-its-source digital librarian.**

---

## 2. Choosing the approach (why this one)

Treat the options like "picking a library system":

| Candidate | Adopted? | Why |
|---|---|---|
| **NotebookLM** (Google's document Q&A) | ✅ Yes | Every answer carries inline citations you can click back to; chat-like, zero learning curve for non-technical staff; near-free (comes with a Google account). |
| **Claude Projects** (another document Q&A) | Backup | Excellent, but the web version doesn't guarantee a citation on every sentence — weaker on "answers must be verifiable." |
| **Build a custom Q&A system from scratch** | ✕ No | Most flexible, but needs ongoing engineering an ops team can't maintain. |
| **Enterprise search platform** (e.g. Glean) | ✕ No | Most complete, but expensive (tens of thousands USD/yr) with seat minimums — overkill for a small team. |

> Pick the tool that fits **your** audience and budget. The method below is tool-agnostic; only Stage 4/5 commands are NotebookLM-specific.

### The key decision: one source, two outputs

Don't build a separate pipeline per output. Maintain **one clean set of text files** that simultaneously feeds:

1. **The Q&A tool** — for non-technical staff to ask by typing.
2. **A reusable knowledge skill** — for advanced queries and automation.

Benefit: **maintenance touches only this one set**; both sides update together and never contradict each other.

---

## 3. The build-and-tune stages

The whole process is like "training a new librarian": give clean material first, then test, correct, and tutor.

### Stage 1 — Inventory (dump everything out and sort it)
- Count all source files (a real deployment had **~300**).
- Discover that only a fraction (~85 in that case) actually had content; the rest were blank pages, drafts, or duplicates. Flag them first.

### Stage 2 — Refine & consolidate (merge many notebooks into one clean book)
Three rules:
1. **Drop duplicates and stale content.**
2. **Newest wins**: when there are old/new versions of the same thing, use the newest; older only backfills what the new one omitted.
3. **Tag every section with its source** (which file, which date) — this is what later lets answers carry citations.

### Stage 3 — Turn tutorial videos into text (so videos become searchable)
- Watch each operation/tutorial video frame by frame, then write it up as **illustrated steps**.
- Result: content that "could only be watched" becomes **text you can search**.

### Stage 4 — Let the assistant "read" design files (turn screens into text)
- Admin/back-office screens often live only in a design tool. Have the assistant read each screen and write it up as a text spec (fields, buttons, flows).

### Stage 5 — Publish to the Q&A tool
- Build separate "libraries" by audience, e.g.:
  - **Operations knowledge base** (daily ops & support)
  - **Back-office spec knowledge base** (PM, engineering, advanced ops)

### Stage 6 — Test & correct (this is the real "fine-tuning")
- Write the **questions ops is most likely to ask**, put them to the Q&A tool, then compare answer-by-answer against the original docs to catch wrong or vague spots.
- In the real case, the all-correct rate went from **67% → 97%**, with zero fabrication and every answer traceable.
- Example fix: build a single authoritative "size reference table" as the one source of truth, eliminating the assistant mixing up sizes across similar items.

### Stage 7 — Integrity audit (prevent "the source has it, but the KB is missing it")
Build a **three-way cross-check**:

> **Original source ↔ Knowledge base ↔ live Q&A-tool test.** If any one side has it and another doesn't, that's a gap.

Use four layers to catch gaps: ① a whole feature is missing ② a key field within a feature is missing (especially list-imports, validation rules) ③ content exists but the tool can't retrieve it ④ orphan pages whose design lives elsewhere and was never collected.

---

## 4. The outcome (from the anonymized real deployment)

| Item | Result |
|---|---|
| KB source files | ~85 content-bearing files consolidated into clean knowledge docs |
| Tutorial videos | dozens of videos → searchable illustrated steps |
| Back-office design | ~21 modules / hundreds of screens → text specs |
| Q&A tool | two knowledge bases (ops, back-office spec) live |
| Answer accuracy | a representative 30-question audit: 67% → **97% all-correct, zero fabrication, verifiable** |
| Integrity audit | hundreds of sources reviewed, dozens of gaps filled |
| Maintenance | single source, per-section citations, update one place |

> Numbers are illustrative from one deployment — yours will differ. They're here to show the method converges.

**For non-technical teammates, remember just one thing:** open the Q&A tool → ask by typing → check the citations it shows.

---

## 5. Where to go next
- A **monthly auto-update mechanism** — like a library adding new books and retiring old ones. See `04-monthly-update-sop.md`.
- **Turn gaps into a system** — every update auto-compares "did new sources make it into the KB," and recycles each caught gap into the next round's test bank.

> **In one line:** this knowledge base isn't "build once and done" — it's a **living asset that grows and self-checks every month.**
