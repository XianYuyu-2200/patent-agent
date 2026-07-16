# Task 9 Software Stable-Output Fix 4 Report

Status: DONE

Base: `3993ef22f8cd4ee8345b59eb04394ef7daaaee94`

## Review findings addressed

1. Added the stable issue-level field `blocks_export: true` to the baseline `S-B001` `business-only` high-severity finding. The delivery refusal now explicitly identifies the open high `S-B001` business-only issue instead of relying on unrelated implementation questions.
2. Removed the regression's permissive `issue.blocks_export OR overall delivery refusal` condition. Each seeded issue must now carry its own exact `blocks_export: true` field.
3. Persisted the exact source-grounded controlled-object/feedback question from `case.json` in both software independent emitted artifacts, including `S-F003` and `SRC-S-02#控制链段落1` provenance.
4. Persisted and asserted an explicit blocked delivery decision and a `mining` / `patent-invention-mining` next action for both software emitted artifacts. The next action keeps `S-B001` outside the technical contribution and preserves the unresolved controlled-object and feedback gaps.
5. Preserved oracle isolation, anonymization, technical-chain provenance, no-fabrication constraints, and the real exporter refusal path. No production Python or Skill behavior changed.

## Root cause

`tests/test_end_to_end.py` accepted either the affected issue's `blocks_export` field or any artifact-level refusal. The baseline software artifact therefore passed even though `S-B001` itself lacked the required stable field and the refusal reason referred only to unrelated clarification gaps. The regression also did not require the independent unresolved question, delivery decision, or next action.

## TDD evidence

### RED

Command:

```text
python -m pytest tests/test_end_to_end.py::test_golden_case_forward_artifacts_match_stable_findings_without_oracle_leakage -v
```

Result: `1 failed`.

The failure was the intended reproduction: the baseline `S-B001` candidate returned `None` for `issue.get("blocks_export")`, where the regression now requires `True`.

### GREEN

After the minimal durable-record update, the same focused command produced `1 passed`.

## Verification evidence

- Focused Task 9 plus actual workflow/export refusal:
  `python -m pytest -q tests/test_end_to_end.py tests/test_workflow.py::test_delivery_blocks_open_high_issues_without_requiring_final_approval tests/test_export_docx.py::test_export_refuses_open_high_issue_from_persisted_case_state`
  -> `10 passed`.
- Full suite: `python -m pytest -q` -> `489 passed`.
- Python compilation: `python -m compileall -q src tests` -> exit 0.
- All 12 skill directories passed the official `quick_validate.py` with `PYTHONUTF8=1`.
- Official plugin validator -> `Plugin validation passed`.
- `git diff --check` -> exit 0; Git reported only existing LF/CRLF normalization warnings.

## Files changed

- `tests/fixtures/software_case/forward-test.md`
- `tests/test_end_to_end.py`
- `task-9-fix4-report.md`

## Scope confirmation

The change is limited to Task 9's anonymized software forward evidence, executable stable-output assertions, and this report. It does not read the oracle during an independent forward, invent technical facts or anchors, relax any human gate, or alter the exporter. The real open-high exporter refusal remains exercised by the focused verification.
