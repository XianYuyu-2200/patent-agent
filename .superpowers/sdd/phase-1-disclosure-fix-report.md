# Phase 1 Disclosure Exact-Set Fix

Date: 2026-07-15 (Asia/Shanghai)

Base: `8a0dddf555144cbfe11bbde4fca81c707aa0757d`

## Scope

Closed the final independent-review Critical finding without changing unrelated
workflow, Skill, template, fixture, acceptance, or release behavior.

## Root cause

`_validate_quality_review_provenance()` normalized the explicit eligible
persisted prior-art disclosure set, but then iterated only over the completed
review's `verified_disclosures`. That enforced `review disclosures` as a subset
of `persisted disclosures` and did not reject an eligible persisted disclosure
omitted from novelty and inventive-step review.

## TDD RED

Added a black-box export regression that appends a second top-level persisted
prior-art disclosure with `status=eligible`, a nonblank document ID, and an
exact disclosure anchor while leaving the completed quality review unchanged.
The test requires export refusal and verifies that no DOCX exists.

RED result:

- `python -m pytest tests/test_export_docx.py::test_export_refuses_eligible_persisted_disclosure_omitted_from_review -q`
  -> `1 failed`; expected failure was `DID NOT RAISE`.

The existing synthetic-review disclosure regression was also tightened to
require an explicit `extra in review` diagnostic. Before the fix, the two-node
run produced `2 failed`: the omitted persisted disclosure exported, and the
synthetic review disclosure raised only the previous generic resolution error.

## Implementation

- Normalize the completed review disclosures to the same
  `(casefolded document ID, stripped exact disclosure anchor)` tuple set used
  for explicit eligible persisted disclosures.
- Require exact set equality before template access.
- Reject both directions with one deterministic diagnostic containing
  `missing from review` and `extra in review`, including sorted disclosure
  identities and `none` when one side has no entries.
- Preserve the existing exact-match export path unchanged.

## GREEN and verification

- Exact missing/extra/valid nodes -> `3 passed in 0.52s`.
- Focused export suite -> `134 passed in 6.20s`.
- Full suite -> `516 passed in 13.42s`.
- All twelve Skill validators -> 12 of 12 printed `Skill is valid!`.
- Official plugin validator -> `Plugin validation passed`.
- `python -m compileall -q src tests` -> exit 0.
- `git diff --check 8a0dddf` -> exit 0; only Windows LF/CRLF working-copy
  notices were emitted.
- The interpreter does not have the optional `build` module, so
  `python -m build --wheel` failed with `No module named build`. The repository's
  tested packaging path, `python -m pip wheel . --no-deps`, then succeeded.
- Fresh wheel -> `codex_patent-0.1.0-py3-none-any.whl`, 52,980 bytes, SHA-256
  `A6E5E98520E2E17D78A75E23C7407F669D652D149B7197C62DE305E2B35E5DEA`.
  The packaged member
  `codex_patent/templates/cn-patent-application.docx` was present.

The temporary wheel directory was removed automatically.

## Files changed

- `src/codex_patent/export_docx.py`
- `tests/test_export_docx.py`
- `.superpowers/sdd/phase-1-disclosure-fix-report.md`

No Skill contract, template byte, fixture, acceptance record, or unrelated
product file changed.
