# 05 · Q&A Tool Gotchas (NotebookLM, empirically verified)

Hard-won behaviors of NotebookLM that will silently wreck answer quality if you don't account for them. Verified in a real deployment. If you use a different tool, re-test these with your own probe questions.

---

## ⚠️ #1 — Fenced code blocks are dropped from retrieval (the big one)
- **Symptom**: any content inside a ```` ``` ```` fence (SQL, JSON, shell commands, table names) **never enters the retrieval layer**. The model then can't answer table-name/command questions — and may **hallucinate fake SQL** instead.
- **Impact measured**: in a 109-question audit, all SQL-detail questions failed/hallucinated because of this; un-fencing lifted pass rate from ~54% → ~84% and cleared hallucinations from 9 → 0.
- **Fix**: before uploading any file that contains a code block, run **`scripts/make_nlm_upload.py`**. It converts fences to plain-text markers (`〔code begins, copy verbatim〕 … 〔code ends〕`) with content byte-identical. Keep the fenced version in your SSOT for humans; upload the converted version.
- **Rule for monthly sync**: every file containing a code block must pass through this script before upload.

## ⚠️ #2 — Some bullet patterns get eaten
- A bullet like `- > 1000` (a dash followed by a comparison) can be swallowed. Rewrite as prose: "greater than 1000."

## ⚠️ #3 — Mid-document chunking can skip long sections
- In long single-page docs, a middle section may be skipped by chunking. Add a plain-text logic summary beside it so the fact is retrievable from more than one place.

## ⚠️ #4 — Generation layer rewrites literal regex/ranges
- A literal regex like `[0-9]` can be rewritten by the generation layer into a numeric range. You can't fix this at the document layer — add an anti-distortion note flagging the literal.

## ⚠️ #5 — Citations resolve only to source-file level
- NotebookLM's inline citation points at the *source file*, not a line/page. To get finer provenance, embed `> Source: {file} | {date}` at the top of every section yourself (this is principle #2 in the method).

---

## Anti-prompt-injection hook interaction
If you run a local hook that blocks risky tool calls, it will (correctly) block NotebookLM **MCP writes** (`source_add` / `source_delete`) as a prompt-injection defense. **Do not disable the hook.** Route uploads through the official `nlm` CLI instead. This workaround is justified only when all three hold, and should be disclosed in your report:
1. zero untrusted/web content is involved,
2. you're writing to your own notebook,
3. it's an established, repeatable workflow.

---

## General probe-before-trust
Whatever tool you pick, before you rely on it: upload one file containing a number, a code block, a long section, and a literal pattern, then ask a question that targets each. You'll find its quirks in ten minutes instead of after a 100-question audit.
