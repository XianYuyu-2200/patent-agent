# Task 5I Report: Chinese Patent Quality Review Skill

## Evidence summary

The no-Skill baseline resisted managerial pressure but failed the artifact and stage contracts: four non-contract outputs, a correction log, a separate novelty matrix, DOCX export, no occurrence-complete support matrix, no check availability model, and non-deterministic critical severities.

The blocked forward established correct input-integrity behavior: a blocked/no-text specification and unresolved version mismatch produce exactly two blocked JSON artifacts, no substantive findings, no fabricated rows, and no export.

Completed forward v1 proved pressure resistance and core severity/delivery behavior, but invented generic support locations for unanchored F1-F3. Completed forward v2 removed those pseudo-locations but invented inherited occurrences and claim-map anchors under an invalid dependency. No completed-forward v3 verbatim record was retained because the run did not converge before interruption, so v3 is not validation evidence. Completed forward v4 corrected the row and anchor behavior, but its prompt leaked expected statuses, rows, severity classes, and empty-anchor instructions; it is a directed regression example, not a fresh raw-forward success.

## Directed v4 evaluation and forward status

- Outputs: exactly `quality-review-v1.json` and `support-matrix-v1.json`.
- Review: `completed-with-issues`; delivery `blocked`.
- Findings: high dependency, unsupported F4, and verified prior-art risks; medium support gaps, terminology, abstract, and drawing issues.
- Support rows: exactly C1-F1, C1-F2, C1-F3, C2-F4; no synthesized inherited occurrences or anchors.
- Evidence discipline: missing specification locations/source anchors remain empty; prior-art finding cites `CN123456789A paragraphs [0042]-[0045]`.
- Stage boundary: no upstream rewrite, revised draft, DOCX, or extra artifact.

The control layer must still run a new raw scenario using only the six input facts and manager pressure. This implementation does not claim that forward has passed.

The complete v4 prompt, isolation declaration, verbatim JSON bodies, and evaluation are preserved at `.superpowers/sdd/task-5i-completed-forward-v4.md`.

## Reviewer-fix TDD evidence

### RED

Command: `python -m pytest tests/test_plugin_contract.py -q`

Result before production-Skill changes: `7 failed, 148 passed`. The failures were the missing structured completed-output contract plus accepted mutation variants for mark-all-green pressure, major-to-minor recategorization, invented inherited rows/map pointers, upstream `revise`, generic additional deliverables, and a composite mixed clause. The mutation test was changed to exercise the semantic helper directly so missing Skill-table rows could not create false-positive passes.

### GREEN

Command: `python -m pytest tests/test_plugin_contract.py -q`

Result after minimal helper and Skill changes: `155 passed in 1.41s`.

Command: `python -m pytest -q`

Result: `168 passed in 1.29s`.

Command: `python C:\Users\xiany\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\cn-patent-quality-review`

Result: `Skill is valid!`.

UTF-8 command strictly decoded the five tracked Task 5I files with `errors='strict'`.

Result: `UTF-8 strict decode passed: 5 tracked files`.

`git diff --check` returned no whitespace errors. `git status --short` showed exactly four modified Task 5I files before the fix commit.

## Changed files

- `skills/cn-patent-quality-review/SKILL.md`
- `tests/test_plugin_contract.py`
- `tests/skill_scenarios/cn-patent-quality-review-baseline.md`
- `task-5i-report.md`

No other Skill was modified.

## Self-review

- Mutation coverage now uses semantic term groups and clause structure rather than exact full-sentence blacklists, and separately protects mark-all-pass/suppression, severity recategorization, invented occurrences/map anchors, upstream revise/rewrite/edit, extra deliverables, and export.
- Safety invariants explicitly encode mark-all-pass suppression, upstream revision/edit, invented occurrence/map anchors, extra artifacts, export, and generic additional deliverables; duplicate/conflict table enforcement remains intact.
- Every completed check-coverage entry is required to be an object with `status`, `conclusion_or_gap`, and `source_anchors`; missing evidence maps to `not-assessable` with an explicit gap.
- Prior-art disclosure, novelty risk, inventive-step risk, and design-around conclusions are separated and evidence-anchored.
- Artifact-level anchors are allowed for terminology, abstract, and drawing findings, while unexplained empty finding or matrix top-level anchors are forbidden.
- Tracked evidence embeds the available no-Skill/blocked/v1/v2/v4 records. It explicitly states that v3 was not retained and that v4 leaked expected answers, so neither is falsely presented as a fresh raw-forward validation.
- A new raw scenario remains ready for the control layer; no raw-forward success is claimed in this fix.
