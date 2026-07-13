# Task 5B Report

## Status

Implemented only the `cn-patent-case-intake` production Skill and its focused contract test. No other production Skill was created. A controller-run fresh forward test was performed after commit `c64384c` and is now recorded verbatim in `tests/skill_scenarios/cn-patent-case-intake-baseline.md`.

## RED evidence

- Stored the fresh no-skill prompt and complete verbatim output in `tests/skill_scenarios/cn-patent-case-intake-baseline.md`.
- The baseline crossed the intake boundary by declaring `06_撰写/技术交底工作稿_v0.1_非定稿` with the exact description: “只写已有材料能够支持的内容，所有不确定处保留来源标记和待确认项，不伪装成正式申请稿。”
- It also explicitly stated: “今天可以进入有限的技术挖掘：梳理技术问题、部件关系、软件功能、可能的改进点，并建立‘技术特征—材料来源—待验证事项’表。” These verbatim lines establish the RED gap: the no-skill agent created an internal drafting work product and proceeded into invention mining instead of stopping at intake.
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

## Fresh forward evidence

- Date: `2026-07-14`.
- Skill path: `D:\codex\codex-patent\.worktrees\phase-1\skills\cn-patent-case-intake\SKILL.md`.
- Run order: commit `c64384c`, then launch fresh controller thread `/root/task_5b_forward_test`, require it to read the Skill while withholding the implementation plan, baseline, and tests, then review its output.
- Result: GREEN. The fresh agent named exactly `intake-v1.json`, `material-index-v1.json`, and `questions-v1.md`; retained `source-backed`, `missing`, and `conflicted` states; did not infer from the blurred image or execute code; and stopped before invention mining or drafting.
- The complete original forward prompt and output are preserved verbatim in the baseline file. Model and runtime/environment identifiers were not recorded and are labelled `not recorded` rather than inferred.

## Review-fix RED/GREEN

- Tightened the same focused contract test to require the first Workflow step to validate any existing fact statuses, explicitly record an empty fact set for a new case, and only then handle customer materials.
- Review-fix RED: focused node failed because the first step was `Treat every original as read-only`.
- Minimal GREEN change: inserted the required fact-status validation as Workflow step 1 and renumbered the existing intake sequence without expanding the output contract.

## Verification layers

- Focused node: `python -m pytest tests/test_plugin_contract.py::test_cn_patent_case_intake_has_exact_intake_contract -v` → `1 passed`.
- Plugin contract file: `python -m pytest tests/test_plugin_contract.py -v` → `4 passed`.
- Full suite: `python -m pytest -v` → `17 passed`.
- Skill validation: `python C:\Users\xiany\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\cn-patent-case-intake` with UTF-8 mode enabled → `Skill is valid!`.
- Scope/diff check: compare this review-fix commit against `c64384c` and confirm only Task 5B files changed.
