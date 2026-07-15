# Task 8 Fix2 Report: Production Review Contract and Scoped Approval

## Status

The two remaining Task 8 Critical findings are fixed.

The exporter now consumes the documented `cn-patent-quality-review` completed output recipe and requires the established structured `final-delivery` approval record to cover the exact current artifact versions and the `DOCX export` action.

## Root Causes

1. `_quality_review_report()` selected a permissive `ValidationReport` parser whenever a top-level `issues` key existed. Because `ValidationReport` ignored unrelated fields, an empty `issues` list could hide contradictory blocked/open-high delivery state. The alternate parser expected a Task-8-only legacy schema instead of the production Skill recipe.
2. `PatentCase.approvals` stored only unscoped string membership. Export could verify that `final-delivery` existed, but not which claims, specification, abstract, and quality-review versions it approved.

## Quality-Review Contract Fix

The exporter now validates one strict completed-review schema with:

- `review_status` of `completed` or `completed-with-issues`;
- all six `input_versions` from the production Skill;
- structured coverage objects for all eleven required checks;
- structured `findings`;
- `open_issue_counts` consistent with the findings;
- `delivery_recommendation`;
- `unresolved_questions` and `source_anchors`;
- the established optional `input_integrity`, `prior_art_assessment`, and `application_set` fields used by recorded forward evidence.

Export fails closed when:

- the JSON is malformed, incomplete, unknown, contains legacy `issues`, or has extra/conflicting gate fields;
- any reviewed input version differs from the selected current artifact version;
- a check is blocked;
- the recommendation is not `ready-for-human-review`;
- critical/high counts are nonzero;
- counts disagree with findings;
- any finding blocks delivery.

An arbitrary `{"issues": []}` object is no longer accepted as a completed quality review.

## Approval Scope Fix

The implementation reuses the existing approval-record format from the Task 5J workflow fixture without adding fields:

```json
{
  "approval_id": "FD-...",
  "type": "final-delivery",
  "status": "approved",
  "current": true,
  "application_set": "...",
  "scope": {
    "claims": "vN",
    "specification": "vN",
    "abstract": "vN",
    "quality_review": "vN",
    "action": "DOCX export"
  }
}
```

`PatentCase.approvals` remains compatible with the existing string approval names used by earlier workflow gates, while export requires exactly one current approved structured `final-delivery` record. Its four version fields and action must exactly match the selected current export artifacts. A retained v1 approval therefore refuses after the application artifacts are replaced by v2.

When the production review includes `application_set`, it must also match the approval record.

## TDD Evidence

### RED

Six focused adversarial tests were added and run before implementation:

- official completed review recipe is accepted;
- arbitrary `issues`-only review is rejected;
- `issues: []` cannot override blocked/open-high metadata;
- official open-high review is rejected;
- the established scoped approval record is accepted;
- v2 artifacts with a retained v1 approval are rejected before template access.

Initial result: `5 failed, 1 passed`. The one already-passing case was the open-high official artifact, which the old incompatible parser rejected generically; the other five failures reproduced the missing behavior and bypasses.

### GREEN

- New adversarial set: `6 passed`.
- Initial focused export/model/workflow/repository/packaging surface: `58 passed`.
- Initial full suite: `415 passed`.

## Post-Commit Review Closure

The required completion review found three additional fail-closed gaps. A review could mark a delivery check `not-assessable`; an approval could name a different application set while using the same versions; and optional integrity/anchor/prior-art structures could contain contradictory or empty gate evidence.

A second RED/GREEN cycle added six reviewer-probe tests:

- `not-assessable` specification-support check;
- `not-assessable` novelty check;
- blocked/stale/placeholder `input_integrity`;
- empty structured source anchor;
- unreported high prior-art risk;
- approval for `OTHER-CASE-v2` against case `CN-TEST-001`.

RED: `6 failed` for the demonstrated bypasses.

GREEN: `6 passed`. The exporter now:

- requires every delivery check to be `completed`, so `not-assessable` is never treated as pass;
- validates optional `input_integrity` only in its positive current/readable/version-matched/identifiable/no-placeholder state;
- validates structured anchors and rejects blank strings or empty objects;
- validates structured prior-art risk and requires high risk to be represented by a high/critical finding;
- derives the authoritative application-set identity as `<case_id>-v<current_version>` and compares it independently with `approval.application_set`.

Final focused surface: `64 passed`.

Final full suite: `421 passed`.

## Wheel and Isolated Installed Export

A fresh wheel was built and installed with `--target` into a temporary directory outside the checkout.

- wheel: `codex_patent-0.1.0-py3-none-any.whl`;
- size: `50,247` bytes;
- SHA-256: `b05e5b1ba3b6d2af25058fcd3e5834931b73d2b4ee41eaf708fd26ec6efa802d`;
- packaged template member: `codex_patent/templates/cn-patent-application.docx`;
- packaged template size: `37,730` bytes;
- import resolved from the isolated install target;
- default template resolved from the isolated install and existed;
- official-review plus scoped-approval export succeeded;
- output DOCX size: `38,164` bytes;
- output reopened with `python-docx`, retained `Template Sentinel`, and contained all seven required patent headings.

## Final Verification

- `PYTHONUTF8=1 python -m pytest -q` -> `421 passed in 9.36s`.
- `PYTHONUTF8=1 python -m compileall -q src tests` -> exit 0.
- `codex-patent version` -> `0.1.0`.
- `git diff --check` -> exit 0.

## Visual Evidence

The tracked template was not modified. Its SHA-256 remains `d8a99f09eae58c2833d19486034fb2409f3113c84ed7adb2c0344a68e28e351e`.

The retained four-page Microsoft Word 2024 visual evidence therefore remains applicable: correct Chinese glyphs, intended claims/specification/abstract page breaks, centered page numbers, and no clipping, overlap, replacement glyph, or margin overflow.

## Files Changed

- `src/codex_patent/models.py`
- `src/codex_patent/export_docx.py`
- `tests/test_export_docx.py`
- `task-8-fix2-report.md`
