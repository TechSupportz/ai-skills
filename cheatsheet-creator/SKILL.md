---
name: cheatsheet-creator
description: >
  Build a printable, high-density exam cheatsheet as a Typst (.typ) document compiled to
  PDF, in an established house style. Use when the user asks for a cheatsheet, revision
  sheet, study guide or condensed notes from lecture slides, PDFs or a textbook; wants an
  existing sheet compressed, merged or extended; or wants formulas, diagrams or exam
  answer templates added to one.
compatibility: Requires the `typst` CLI. PDF source extraction needs Python 3 + pdfplumber.
---

# Cheatsheet Creator

A cheatsheet is not a summary. It is the page the user reads **during** the paper, under
time pressure, with one finger on the question. Every block earns its space by saving
seconds in that moment — so the sheet is built around **high-yield** content, a fixed
visual grammar the eye learns once, and a compile that actually fits the page count.

## House style

Fonts, sizes, palette and macros are fixed and live in
[`assets/house-style.typ`](assets/house-style.typ) — copy that file to `<name>.typ` and
fill it in. Do not re-derive the preamble; sheets across a course must look identical so
the reader's eye lands in the same place every time.

The style in one line: Inter 7.0pt body, SF Mono 6.15pt code, A4 portrait, 3 columns at
0.62em gutter, 0.30cm side margins, near-black ink `#141922` on white, six accent colours
bound to topic families, tinted section bars with a thick left rule, zebra `kv` tables.

[`references/typst-patterns.md`](references/typst-patterns.md) holds the block recipes
(`sec`, `kv`, `step`, callouts, ASCII diagrams), the fit dials, and the Typst failure
modes. Read it before writing content, and again when a compile errors.

## Workflow

### 1. Gather the corpus

Collect every source: lecture PDFs and slides, the syllabus, past papers, lab handouts,
and any existing sheet to merge. For PDFs:

```bash
python3 -m venv venv && source venv/bin/activate && pip install pdfplumber
python3 scripts/extract_pdfs.py   # edit LECTURE_DIR / OUTPUT_DIR at its top first
```

Read every extracted `.txt` before writing a line of Typst. Done when each source file
has been read and you can name the units the exam covers.

### 2. Coverage map

List every topic in the syllabus and mark it `covered` / `partial` / `missing` against
what the sheet currently holds (all `missing` for a new sheet). Record the specific
formula, method or trap behind each mark, not a topic label. Then rank the list by what
past papers actually ask. Done when every syllabus topic carries a mark and a rank.

### 3. Find the one question

Most papers in a course resolve to a single recurring test — "does this method operate on
state this class owns?", "which funnel stage and which metric?". Name it and put it in the
thesis box under the masthead. Done when the box holds one testable question that the
majority of ranked topics answer to.

### 4. Write the sections

Work down the ranked list, highest yield first, one `sec` per topic. Each section carries,
in this order: the shape (a code skeleton, formula, or ASCII diagram), the `kv` table of
terms, then at most one callout — `hot` for the fact that unlocks the topic, `warn` for
the **trap** made under time pressure, `good` for the habit.

Prefer the literal artifact over description: the exact command, the exact signature, the
exact formula with its units. If a line would not save a second during the paper, drop it.

Done when every topic ranked above the cut line has a section, and every `missing` mark
from step 2 is either written or consciously dropped.

### 5. Close the sheet

Add these, unless the user rules one out:

- **Master formula / signature table** — every formula or API signature in the course, in
  one place, with what each tells you. Quantitative courses live off this block.
- **Exam-answer templates** — one sentence per answer shape the paper asks for, phrased as
  the answer itself, ready to transcribe.
- **Panic list** — the six things to check in the last five minutes.
- **Footer navigation** — the running footer already names each page's topics; keep those
  strings current with the final section order.

### 6. Compile and fit

```bash
typst compile <name>.typ
```

Fix every error and warning, then look at the PDF. Turn the fit dials in
`references/typst-patterns.md` until the sheet fills its pages with no ragged tail and no
orphaned section header. Done when the compile is clean and the last page is full.

### 7. Report

Tell the user, in this order: files written, topics added or cut, the fit dials moved from
house defaults, the compile result, and the highest-value thing still missing.

## Working with an existing sheet

Read the sheet first and adopt what it already does — its macro names, accent bindings and
section order are the contract. Run steps 2–7 as a revision pass, and keep every block the
user has flagged as useful in a previous round. When something must be cut to fit, cut the
lowest-ranked block from step 2 and say so in the report.
