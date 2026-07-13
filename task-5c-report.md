# Task 5C Report

## Status

Implemented only the `patent-invention-mining` Skill, its focused contract test, and its baseline/forward evidence. No other Skill was created.

## Contract-test RED

- Added `test_patent_invention_mining_has_exact_contract` before initializing the Skill.
- Focused RED command: `python -m pytest tests/test_plugin_contract.py::test_patent_invention_mining_has_exact_contract -v`.
- Observed result: `1 failed`; the expected failure was the missing `skills/patent-invention-mining/SKILL.md`.
- The contract fixes the exact inputs `intake-vN.json` plus source anchors, exact outputs `technical-facts-vN.json`, `feature-tree-vN.json`, and `interview-vN.md`, a fact-status validation first step, evidence gates, boundary rules, and unified `openai.yaml` metadata.

## Skill-disabled baseline RED

- The first fresh baseline agent did not return usable output and was interrupted rather than reused.
- A second fresh agent with no forked context completed the same pressure scenario; its only added constraint was a compact response limit.
- The complete prompt and verbatim output are stored in `tests/skill_scenarios/patent-invention-mining-baseline.md`.
- The no-Skill agent invented coarse/fine adjustment, adaptive step sizes, continuous-stability termination, and abnormal-fluctuation behavior without anchors.
- It collapsed the `conflicted` 30% and 60% statements into a supported generic conclusion that calibration time is shortened.
- It returned three non-standard products instead of the declared invention-mining artifacts.
- It crossed the mining boundary by providing search terms, claim directions, and specification content.

## Minimal implementation

- Initialized the unique Skill with the official `init_skill.py`; no scripts, references, assets, or other Skill directories were created.
- Defined a concise `Use when...` description for invention mining after intake or when anchored technical facts and inventor interview questions are needed.
- Required the Workflow to start by validating `confirmed`, `source-backed`, `inferred`, `missing`, and `conflicted` statuses.
- Allowed only `confirmed` and `source-backed` content to become final technical facts or feature-tree nodes.
- Prohibited invented facts even when labelled hypothesis, proposal, candidate, or draft.
- Required conflicts to remain separate; specifically prohibited turning the 30%/60% conflict into a value, range, average, or generic “faster” effect.
- Converted missing relationships, parameters, and algorithm steps into anchored interview questions.
- Limited output to exactly `technical-facts-vN.json`, `feature-tree-vN.json`, and `interview-vN.md`, then stopped before prior-art search, claim strategy, claim drafting, or specification drafting.
- Generated `agents/openai.yaml` with display name `发明挖掘` and the unified default prompt `请处理当前案件并生成本阶段规定的结构化产物。`.

## Fresh forward GREEN

- Used a new agent thread `/root/task_5c_implementer/mining_forward`; neither baseline agent was reused.
- Required it to read only the finished Skill and the same raw pressure scenario, while withholding implementation plans, baseline evidence, tests, reports, and other Skills.
- The complete forward prompt and verbatim output are appended to `tests/skill_scenarios/patent-invention-mining-baseline.md`.
- Result: GREEN. It produced exactly the three v1 artifacts, retained 30% and 60% as separate conflicts, kept missing connection and algorithm details out of final facts and the feature tree, created evidence-seeking interview questions, and stopped before search and drafting.
- A supplementary fresh agent `/root/task_5c_implementer/mining_status_forward` tested an `inferred` fact and the unknown status `candidate`. It kept the inferred statement unresolved, rejected the unknown status, excluded both from final facts and the feature tree, returned exactly three v2 artifacts, and refused claim work. Its complete prompt and output are preserved in the same evidence file.
- Model and runtime/environment identifiers were not recorded and are labelled `not recorded` rather than inferred.

## Validation and tests

- Official validator: `$env:PYTHONUTF8='1'; python C:\Users\xiany\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\patent-invention-mining` → `Skill is valid!`.
- Focused node: `python -m pytest tests/test_plugin_contract.py::test_patent_invention_mining_has_exact_contract -v` → `1 passed`.
- Plugin contract file: `python -m pytest tests/test_plugin_contract.py -v` → `5 passed`.
- Full suite: `python -m pytest -v` → `18 passed`.

## Attention points

- The forward test verifies agent behavior through complete response artifacts; it does not write a live case workspace.
- The Skill defines semantic artifact contracts but does not add JSON Schema files, because Task 5C requires only the Skill and forbids unrelated resources.
- The completed baseline evidence comes from the fresh retry agent after the first fresh baseline agent was interrupted without output.

## Review closure

- Corrected the validator command to enable UTF-8 explicitly on Windows.
- Hardened the contract test to require exactly two input bullets, only `intake-vN.json` as a file input, exactly three output bullets, and no additional file-like artifact token anywhere in the Inputs or Outputs sections.
- Added the complete supplementary fresh behavior scenario for `inferred` and invalid `candidate` statuses.
- Removed the inaccurate claim that the metadata description was trigger-only.
