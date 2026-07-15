# Task 9 Provenance Fix 3 Report

Status: DONE

Base: `e3e75af40e35e8e8846ce20af64ff6d9bce74b61`

## Review findings addressed

1. Corrected mechanical relationship `M-R002` so its subject, relation, and object match `M-F002` and `SRC-M-01#段落3`: the elastic positioning member enters and cooperates with the positioning groove. The fixture no longer fabricates that the groove belongs to the support arm.
2. Replaced the software fixture's unsupported rotating-equipment identity, motor-speed assertion, and later-sample feedback assertion with the only final statement supported by `S-F003` and `SRC-S-02#控制链段落1`: sending a slowdown command to the motor driver.
3. Preserved controlled-object and feedback gaps as explicit unresolved, non-final fields with `final_text_allowed: false` rather than treating them as source-backed context.
4. Narrowed the durable software forward conclusion to the motor-driver slowdown command and added an `unresolved_context` record for controlled-object identity and feedback. It no longer calls rotating-equipment control part of a traceable chain.
5. Strengthened the regression to assert exact relationship/context values, cited fact and anchor resolution, final-text eligibility, unresolved fields, and the exact durable forward conclusion instead of checking only that containers exist.

The seeded `M-F999` unsupported-feature and `S-B001` business-only high-severity findings, workflow gates, and export refusal behavior remain unchanged.

## TDD evidence

### RED

Command: `python -m pytest tests/test_end_to_end.py -q`

Result: `3 failed, 5 passed`.

- `M-R002` still used relation `在展开位置与定位槽配合` and object `支撑臂` instead of the anchored positioning-groove relationship.
- The software fixture lacked the anchored `control_command` and unresolved/non-final controlled-object record.
- The durable forward artifact still asserted `旋转设备控制` as part of a source-traceable chain.

### GREEN

Command: `python -m pytest tests/test_end_to_end.py -q`

Result: `8 passed`.

## Verification evidence

- Focused golden-case/workflow/validation/export suite: `python -m pytest tests/test_end_to_end.py tests/test_workflow.py tests/test_validation.py tests/test_export_docx.py -q` -> `141 passed`.
- Full suite: `python -m pytest -q` -> `489 passed`.
- Python compilation: `python -m compileall -q src tests` -> exit 0.
- All 12 skill directories validated with `PYTHONUTF8=1` and the official `quick_validate.py` -> `Skill is valid!` for each.
- Official plugin validator -> `Plugin validation passed`.
- All 15 repository JSON files parsed successfully as UTF-8 JSON.
- `git diff --check` -> exit 0 (Git emitted only existing line-ending normalization warnings).

## Files changed

- `tests/fixtures/mechanical_case/case.json`
- `tests/fixtures/software_case/case.json`
- `tests/fixtures/software_case/forward-test.md`
- `tests/test_end_to_end.py`
- `task-9-fix3-report.md`

## Scope confirmation

No production Python or Skill behavior changed. This follow-up is limited to golden fixture provenance, durable forward evidence, exact regression coverage, and this report.
