# Phase 1 Provenance/Export Fix

Date: 2026-07-15 (Asia/Shanghai)

## Scope

Closed the Important whole-branch review finding that DOCX export accepted a quality-review report without resolving its declared upstream artifacts or evidence. The deterministic gate now requires current, unique, same-version `ArtifactRef` records for claims, claim-feature-map, specification, abstract, drawing-plan, prior-art, and quality-review. Final-delivery approval scope covers all seven versions and the DOCX export action.

## Provenance rules

- Quality-review source-anchor strings and structured `artifact` anchors must equal a selected persisted `ArtifactRef.path` and resolve to an existing file inside the case workspace.
- Structured `source_id` + `locator` anchors must exactly match a persisted `PatentCase.facts[*].anchors` pair. Partial or arbitrary nonblank anchors fail closed.
- Every declared quality-review upstream artifact path must be referenced by the review's top-level/check/finding source anchors.
- Every verified prior-art disclosure `(document_id, disclosure_anchor)` must exactly resolve (case-insensitive document ID, exact anchor) to a structured record in the current `prior-art-vN.json` artifact. Synthetic IDs, missing records, and missing anchors are rejected.
- The official DOCX template/export path is unchanged; all provenance checks run before opening the template.

## TDD evidence

- RED: two focused tests failed before the fix because export produced a DOCX for a missing claim-feature-map and a synthetic prior-art disclosure (`2 failed`).
- GREEN: focused provenance tests passed (`5 passed` across missing, synthetic, valid cross-artifact, arbitrary-anchor, and persisted-fact-anchor cases).

## Verification

- `PYTHONUTF8=1 python -m pytest -q` -> `509 passed`.
- `PYTHONUTF8=1 python -m pytest tests/test_export_docx.py -q` -> `127 passed`.

No template bytes were changed.
