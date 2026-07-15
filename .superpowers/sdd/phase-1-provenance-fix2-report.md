# Phase 1 Provenance Fix 2

Date: 2026-07-15 (Asia/Shanghai)

Base: `be3a20f`

## Scope

Closed the final whole-branch Critical and Important findings without changing unrelated workflow, validation, template, golden-case, or acceptance behavior.

## Root causes

1. Upstream claim-feature-map, drawing-plan, and prior-art artifacts required only an eligible top-level status and a `source_anchors` list type. Empty lists and arbitrary synthetic values therefore passed.
2. Prior-art verification recursively collected any nested dictionary containing a document ID and disclosure anchor. Records explicitly marked unverified or blocked could therefore satisfy a quality-review `verified_disclosures` pair.
3. The `patent-document-export` Skill and its exact contract tests still described four inputs after the deterministic exporter and final-delivery approval scope had moved to seven current same-version artifacts.

## TDD RED

Added four real black-box exporter regressions and one Skill exact-contract regression before production/Skill changes:

- empty upstream `source_anchors`;
- synthetic non-resolving upstream anchors;
- a matching prior-art pair present only in a nested `status=unverified` lead;
- a matching pair present only in a nested `status=blocked-missing-source` record;
- exact seven-input document-export contract.

Focused RED result: **5 failed**. All four exporter cases failed with `DID NOT RAISE`, and the Skill contract failed on the old four-input list.

## Implementation

- Each claim-feature-map, drawing-plan, and prior-art artifact must have an eligible top-level status and a nonempty `source_anchors` list.
- Each upstream anchor is schema-validated and must resolve either to an existing current/non-stale persisted `ArtifactRef` path inside the case workspace or to an exact persisted case-fact `(source_id, locator)` pair.
- Prior-art disclosure resolution no longer recursively searches arbitrary JSON. The current prior-art artifact must expose a nonempty top-level `verified_disclosures` list.
- Each persisted disclosure requires `status=verified` or `status=eligible`, a nonblank document ID, and a nonblank exact disclosure anchor. Nested leads, blocked records, missing-evidence records, and unrelated dictionaries are never considered verified evidence.
- The quality-review disclosure pair must exactly match the explicit eligible persisted disclosure set.
- `patent-document-export` now declares and reasons over exactly seven inputs: claims, claim-feature-map, specification, abstract, drawing-plan, prior-art, and quality-review. Its currentness, version match, provenance, approval-scope, checklist, blocked-mode, and quality-check language now covers all seven.

## GREEN and verification

- Exact RED nodes -> **5 passed**.
- Export plus plugin-contract suites -> **471 passed in 6.85s**.
- Full suite -> **515 passed in 12.76s**.
- All twelve Skill validators -> **12/12 `Skill is valid!`**.
- Official plugin validator -> **`Plugin validation passed`**.
- `python -m compileall -q src tests` -> exit 0.
- `codex-patent version` -> `0.1.0`.
- `git diff --check` -> exit 0; only Windows LF/CRLF working-copy notices were emitted.
- Fresh wheel -> **52,824 bytes**, SHA-256 `167dee0eee63dd80d931093cfa03af6cad1713c993a689ecbd1b66769012f28f`.
- Isolated `pip --target` install resolved both code and the packaged template outside the checkout and exported a readable **38,191-byte** DOCX with `Template Sentinel` and all seven required headings.

All temporary wheel/install/case/export directories were removed automatically.

## Files changed

- `src/codex_patent/export_docx.py`
- `tests/test_export_docx.py`
- `skills/patent-document-export/SKILL.md`
- `tests/test_plugin_contract.py`
- `.superpowers/sdd/phase-1-provenance-fix2-report.md`

No template bytes or unrelated product files changed.
