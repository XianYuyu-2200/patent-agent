# Task 8 Fix4 Report: Require Explicit Prior-Art Assessment

## Status

The remaining Task 8 critical export bypass is fixed. A completed official
quality-review JSON can no longer omit `prior_art_assessment` while marking
novelty and inventive step complete. Missing or malformed prior-art assessment
data fails closed before the DOCX template is opened. A coherent official
recipe with verified disclosure, claim-level novelty risk, and claim-level
inventive-step risk remains exportable.

## Root Cause

`_CompletedQualityReview.prior_art_assessment` was optional, and its internal
consistency validator only ran when the field was present. Consequently,
completed novelty/inventive-step checks with plain string anchors could pass
without the separate verified-disclosure and risk records required by the
quality-review Completed Output Recipe.

## Changes

- Made `prior_art_assessment` a required strict review field in
  `src/codex_patent/export_docx.py`.
- Updated the official test recipe with a verified disclosure, separate
  claim-level novelty and inventive-step risks, and matching structured
  disclosure anchors.
- Added a regression proving that completed checks with plain anchors and no
  `prior_art_assessment` are refused and preserve the output path.

## TDD Evidence

### RED

Before the production change:

```text
python -m pytest tests/test_export_docx.py::test_export_refuses_completed_review_without_prior_art_assessment -q
1 failed: DID NOT RAISE
```

The failure reproduced the omission bypass.

### GREEN

After the minimal change:

```text
python -m pytest tests/test_export_docx.py::test_export_refuses_completed_review_without_prior_art_assessment tests/test_export_docx.py::test_export_accepts_official_completed_quality_review_recipe -q
2 passed

python -m pytest tests/test_export_docx.py -q
110 passed
```

## Verification

- Full suite: `PYTHONUTF8=1 python -m pytest -q` -> **481 passed**.
- Compilation: `PYTHONUTF8=1 python -m compileall -q src tests` -> exit 0.
- CLI version: `codex-patent version` -> `0.1.0`.
- Diff whitespace: `git diff --check` -> exit 0.
- Fresh wheel: `codex_patent-0.1.0-py3-none-any.whl`, 51,312 bytes,
  SHA-256 `6832907ef7f96d8270050aa27d503db0ee0e0e595b0542eed805d31492b5eea2`.
- Isolated install: import resolved from the temporary `pip --target`
  directory; the packaged template resolved inside that install; a real
  application export completed and reopened with `python-docx`.
- Isolated output size: 38,037 bytes. Packaged template size: 37,730 bytes.
- Tracked template SHA-256 remains
  `d8a99f09eae58c2833d19486034fb2409f3113c84ed7adb2c0344a68e28e351e`.
  No template or COM render changes were made.

## Files Changed

- `src/codex_patent/export_docx.py`
- `tests/test_export_docx.py`
- `task-8-fix4-report.md`
