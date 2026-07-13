# Task 5B Report

## Status

Implemented only the `cn-patent-case-intake` production Skill and its focused contract test. No other production Skill was created, and no forward test was run.

## RED evidence

- Stored the fresh no-skill prompt and complete verbatim output in `tests/skill_scenarios/cn-patent-case-intake-baseline.md`.
- The baseline created many non-standard files and crossed the intake boundary into limited invention mining and an internal drafting work product.
- Added `test_cn_patent_case_intake_has_exact_intake_contract` before production implementation.
- Focused RED command: `python -m pytest tests/test_plugin_contract.py::test_cn_patent_case_intake_has_exact_intake_contract -v`.
- Observed result: `1 failed`; the expected failure was the missing `skills/cn-patent-case-intake/SKILL.md`.

## Implementation

- Initialized the unique Skill with the official `init_skill.py` generator.
- The first initialization attempt stopped because the generated `short_description` was 22 characters, below the generator's 25-character minimum. The incomplete template was removed and initialization was rerun successfully with a compliant description.
- Added a trigger-only `Use when...` description for new Chinese patent cases, mixed materials, transcriptions, images, code, completeness, conflicts, disclosure risk, and uncertain inventor or applicant identity.
- Defined `Inputs`, `Workflow`, `Outputs`, `Stop Conditions`, and `Quality Checks`.
- Limited outputs exactly to `intake-vN.json`, `material-index-vN.json`, and `questions-vN.md`.
- Required read-only originals, per-fact source anchors, preserved conflicts, explicit missing/conflicted identity and disclosure data, no inference from blurred images, and no execution of unknown code.
- Required an intake stop before invention mining or drafting.
- Generated `agents/openai.yaml` with display name `专利案件受理` and the plan's unified default prompt.

## Verification

- Focused GREEN: `1 passed`.
- `quick_validate.py` with `PYTHONUTF8=1`: `Skill is valid!`.
- Focused plugin contract suite: `4 passed`.
- Full suite: `17 passed`.

## Review focus

- Confirm whether the intake boundary is intentionally absolute even when the customer asks to start drafting immediately.
- Confirm whether later schema work should further constrain the internal JSON fields; this task intentionally contracts artifact names and intake behavior only.
