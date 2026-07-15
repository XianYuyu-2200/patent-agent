# Task 8 Fix3 Report: Fail-Closed Evidence, Content, and Output Protection

## Status

The remaining Task 8 release blockers from the independent final quality and specification review are fixed.

The exporter now refuses contradictory or unevidenced prior-art completion, semantically empty structured anchors, placeholder application text, and every output path that aliases protected case evidence or the active template.

## Root Causes

1. `prior_art_assessment.verified_disclosures` accepted arbitrary dictionaries, while the completed-review consistency validator did not correlate verified disclosures, claim-level risk results, and novelty/inventive-step check status or evidence.
2. Structured anchors treated any truthy `overlap` list as meaningful, including `overlap: [""]`.
3. Claims and required application sections were checked only for whitespace, so TODO markers, pending-confirmation text, and punctuation-only ellipses were treated as substantive final content.
4. `output_path` was not compared with persisted case files or the active template before `Document.save()`, allowing current artifacts and `case.json` to be overwritten with DOCX bytes.

## Fixed Findings

### 1. Prior-art completion is evidence-consistent

Verified disclosures now use a strict structured object requiring:

- a nonblank document identifier;
- a nonblank exact disclosure anchor;
- nonblank optional disclosure text;
- nonempty, nonblank optional overlapping-feature identifiers.

When `prior_art_assessment` is present, export now refuses unless:

- at least one meaningful verified disclosure exists;
- novelty and inventive-step each contain a claim-level risk result;
- a `not-assessable` risk is not contradicted by a `completed` check;
- every completed novelty or inventive-step check cites a document/anchor pair present in the verified disclosures;
- the existing high-risk/finding consistency rule remains satisfied.

The regression set covers empty disclosures with `none` risk, empty disclosures with `not-assessable` risk and evidence gaps, `verified_disclosures: [{}]`, and separately contradictory novelty and inventive-step completion. A coherent verified-disclosure recipe remains exportable.

### 2. Structured anchors must be semantically meaningful

Every `overlap` entry must now be a nonblank string. Empty overlap lists and lists containing blank members cannot satisfy either top-level or per-check source-evidence requirements.

### 3. Placeholder and punctuation-only application text is blocked

Before the template is opened, export checks every claim and all six required sections for:

- `TODO`, `TBD`, and `placeholder` markers;
- Chinese pending markers including `待补充` and `待确认`;
- ASCII or Unicode ellipsis placeholders;
- text containing no alphanumeric or ideographic substance.

The regression matrix covers six representative markers in claims and in each of 技术领域、背景技术、发明内容、附图说明、具体实施方式、摘要, including `[待补充权利要求]`.

### 4. Protected case evidence cannot be overwritten

The output path is validated immediately after loading the persisted case and before content parsing, template opening, directory creation, or document saving.

Protection covers:

- `case.json` and every existing file in the case workspace;
- every path referenced by the case artifact list, including paths that resolve outside the workspace;
- customer source-material files;
- the active default or caller-selected template.

Alias detection compares resolved, OS-normalized paths and also uses filesystem identity for existing paths. This rejects `..` aliases, Windows case-only aliases, symlink-resolved aliases, and hard-link identity where supported. Regression tests verify that current claims, specification, abstract, quality-review, `case.json`, source material, and active-template bytes remain unchanged after refusal.

## TDD Evidence

### RED

Before production changes:

```text
PYTHONUTF8=1 python -m pytest tests/test_export_docx.py -q
58 failed, 50 passed
```

The failures reproduced all confirmed blockers:

- nine protected-path/alias cases either overwrote source bytes or failed to refuse;
- seven prior-art and structured-anchor contradictions were accepted;
- six placeholder claim cases and thirty-six required-section placeholder cases reached template opening.

### GREEN

After the minimal implementation:

```text
PYTHONUTF8=1 python -m pytest tests/test_export_docx.py -q
109 passed in 2.77s
```

The focused export and packaging surface then passed:

```text
PYTHONUTF8=1 python -m pytest tests/test_export_docx.py tests/test_packaging.py -q
110 passed in 8.64s
```

## Full Verification

- Full suite: `PYTHONUTF8=1 python -m pytest -q` -> `480 passed in 10.02s`.
- Compilation: `PYTHONUTF8=1 python -m compileall -q src tests` -> exit 0.
- CLI version: `codex-patent version` -> `0.1.0`.
- Diff whitespace: `git diff --check` -> exit 0.

## Wheel and Isolated Installed Export

A fresh wheel was built, installed with `--target` outside the checkout, and imported from that isolated target.

- wheel: `codex_patent-0.1.0-py3-none-any.whl`;
- size: `51,315` bytes;
- SHA-256: `5b57db7fdfcb361eef3bc24c16eaa9425c009359b24acadbaef6e924b1852328`;
- packaged template: `codex_patent/templates/cn-patent-application.docx`;
- packaged template size: `37,730` bytes;
- isolated output size: `38,042` bytes.

The smoke confirmed that the module and default template both resolved inside the isolated install, the generated DOCX reopened with `python-docx`, the `Template Sentinel` style remained present, and all required application headings were present.

## Visual Evidence

The tracked template was not modified. Its SHA-256 remains:

```text
d8a99f09eae58c2833d19486034fb2409f3113c84ed7adb2c0344a68e28e351e
```

The retained four-page Microsoft Word 2024 visual evidence therefore remains applicable: correct Chinese glyphs, intended claims/specification/abstract page separation, centered page numbers, and no clipping, overlap, replacement glyph, or margin overflow. No COM render was rerun for this logic-only fix.

## Files Changed

- `src/codex_patent/export_docx.py`
- `tests/test_export_docx.py`
- `task-8-fix3-report.md`
