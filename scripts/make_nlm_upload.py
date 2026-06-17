#!/usr/bin/env python3
"""Convert SSOT Markdown into a NotebookLM-uploadable version.

Why this exists
---------------
NotebookLM silently drops fenced code blocks (```) from its retrieval layer,
so SQL / commands / JSON inside fences become un-answerable and the model may
hallucinate fake SQL. (Verified: in a 109-question audit every SQL-detail
question failed/hallucinated because of this; un-fencing lifted pass rate from
~54% to ~84% and cleared hallucinations from 9 to 0.)

What it does
------------
Replaces each fenced code block with plain-text markers while keeping the
content byte-for-byte identical, so the code becomes retrievable as prose.
Your SSOT keeps the real fences for humans; only the uploaded copy is converted.

Usage
-----
    python3 make_nlm_upload.py <file.md> [more.md ...]
    python3 make_nlm_upload.py --out ./upload <file.md>

Output: <out-dir>/<same-name>.md  (default out-dir: ./upload next to this run)

Monthly sync rule: every file containing a code block must pass through this
script before being uploaded to NotebookLM.
"""
import sys
import pathlib

DEFAULT_OUT = pathlib.Path("upload")
NOTE = (
    "\n> Note: this is the NotebookLM-upload version. The original SSOT's code "
    "blocks have been converted to plain text (content is byte-identical) so "
    "that SQL/commands stay retrievable. The fenced SSOT original is kept "
    "separately for humans.\n"
)


def convert(path: pathlib.Path, out_dir: pathlib.Path) -> pathlib.Path:
    lines = path.read_text(encoding="utf-8").split("\n")
    out, in_code = [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            if not in_code:
                in_code = True
                lang = ln.strip().lstrip("`").strip() or "code"
                out.append(f"[begin {lang} code — copy verbatim line by line]")
            else:
                in_code = False
                out.append("[end code]")
            continue
        out.append(ln)
    new = "\n".join(out)
    # Insert the note right after a leading YAML frontmatter block, if present.
    parts = new.split("---\n", 2)
    if len(parts) == 3 and parts[0].strip() == "":
        new = "---\n" + parts[1] + "---\n" + NOTE + parts[2]
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / path.name
    dest.write_text(new, encoding="utf-8")
    return dest


def main(argv):
    out_dir = DEFAULT_OUT
    files = []
    it = iter(argv)
    for arg in it:
        if arg in ("--out", "-o"):
            out_dir = pathlib.Path(next(it))
        elif arg in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            files.append(arg)
    if not files:
        print(__doc__)
        return 1
    for arg in files:
        p = pathlib.Path(arg)
        print(convert(p, out_dir), "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
