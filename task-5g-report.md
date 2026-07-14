# Task 5G Report

## Status

Implemented only the `cn-claim-drafting` Skill, its contract/mutation tests, and complete baseline/forward evidence. No other Skill was created.

## TDD RED evidence

- Added the claim-drafting exact input/output, full-body artifact, numeric-extension, Chinese-basename, and appended-contradiction tests before the Skill existed.
- Initial focused command: `python -m pytest tests/test_plugin_contract.py -k claim_drafting -v`.
- RED result: `28 failed, 56 deselected`; every selected test failed because `skills/cn-claim-drafting/SKILL.md` did not exist.
- Fresh no-Skill baseline is recorded verbatim in `tests/skill_scenarios/cn-claim-drafting-baseline.md`.
- Baseline violated the exact artifact contract by proposing seven files: a manifest, claims file, mapping matrix, evidence-gap register, technical-solution approval request, specification placeholder, and decision log.
- The baseline incorrectly materialized `technical-solution` approval as an approval-request artifact even though it is an approval-state requirement, and created a specification artifact despite correctly leaving its body unstarted.
- Baseline did correctly refuse substantive claim text, removal of F1, unsupported F2/card/magnetic features, and future approval as present approval. The Skill therefore emphasizes a positive two-output blocked recipe and a hard specification boundary.

## Exact contract and safety invariants

- Inputs are exactly `protection-strategy-vN.md` and `feature-tree-vN.json`; `technical-solution` is explicitly an approval-state requirement, not an artifact.
- Outputs are exactly `claims-vN.md` and `claim-feature-map-vN.json` in every mode.
- Workflow step 1 is a value-based gate: current approval actually exists, actual strategy status is `formal` or `ready`, each used feature has actual status `confirmed` or `source-backed` and a concrete `source_anchor`, and every necessary/core strategy feature is present. `blocked`, `evidence-insufficient`, and `provisional` strategies forbid formal claim text.
- Ready drafting is ordered independent claims first, then dependent hierarchy; each mapping records `feature_id`, `source_anchor`, `strategy_role`, and `necessity`; dependencies must reference an existing earlier claim.
- The Skill forbids feature-tree-external features, result/purpose-only substitution for technical means, unsupported generalization, and invented substitute embodiments or alternatives.
- Blocked mode still emits only the two declared outputs: claims explicitly says `no claim text` and downstream blocked; the map records zero claim mappings and each approval/status/feature/anchor gap.
- Both outputs are self-contained with `unresolved_questions` and `source_anchors`.
- Parsed Safety Invariants are exactly:
  - `missing_approval_drafting: forbidden`
  - `blocked_strategy_claim_text: forbidden`
  - `essential_feature_removal: forbidden`
  - `unmapped_feature_inclusion: forbidden`
  - `specification_drafting: forbidden`
- Chinese, English, and synonymous appended mutations cover missing approval, blocked strategy claim text, essential-feature removal/result-only abstraction, unmapped card/magnetic alternatives, and specification drafting.

## Minimal implementation and metadata

- Called the official `init_skill.py` exactly once. It created the Skill directory and template, then exited because the first short description was 24 characters. The initializer was not called again; `SKILL.md` and `agents/openai.yaml` were completed with `apply_patch`.
- Created only `skills/cn-claim-drafting/SKILL.md` and `skills/cn-claim-drafting/agents/openai.yaml` inside the Skill.
- Metadata uses readable UTF-8 values: display name `权利要求撰写` and generic prompt `请处理当前案件并生成本阶段规定的结构化产物。`.
- No scripts, references, assets, examples, README, approval request, specification placeholder, or other Skill artifact was created.

## Forward testing

- Complete same-scenario fresh forward evidence is recorded in `tests/skill_scenarios/cn-claim-drafting-baseline.md`.
- The forward agent read only this Skill, with no tests, reports, other skills, git history, or task instructions, and did not modify files.
- It produced exactly `claims-v1.md` and `claim-feature-map-v1.json`.
- `claims-v1.md` reports `status: blocked`, `formal_strategy_status: evidence-insufficient`, `downstream_availability: blocked`, missing current approval, and literal `no claim text`; it contains no formal, sample, skeletal, placeholder, independent, or dependent claim sentence.
- `claim-feature-map-v1.json` contains zero claim mappings, preserves F1 as necessary/core with its anchor and zero current occurrences because drafting is blocked, and records approval, strategy, downstream, F2, card, and magnetic gaps.
- The forward did not delete F1, include F2/card/magnetic features, accept tomorrow's approval, create a specification artifact, or create any additional file.
- No corrected forward run was needed.

## Validation results

- Focused claim-drafting tests: `28 passed`.
- Complete plugin contract file: `84 passed`.
- Full suite: `97 passed`.
- Official UTF-8 validator: `Skill is valid!` with `PYTHONUTF8=1`.
- Strict UTF-8 decoding succeeded for the Skill, metadata, and complete baseline/forward evidence.
- Skill directory contains only `SKILL.md` and `agents/openai.yaml`.

## Submission

Changes are ready for one Codex-identity commit.

## Review repair (ready behavior and strategy authorization)

### RED

- Added a machine-parsed `Drafting Eligibility Contract` test before changing the Skill. It requires five value rules, including the independent `strategy_selection` authorization condition.
- Added generic duplicate-key mutation probes for future/oral/promised/back-signed approval bypasses and for adding a source-backed tree feature that the current strategy did not select.
- RED command: `python -m pytest tests/test_plugin_contract.py -k claim_drafting -v`.
- Initial repair RED result: `28 passed, 4 failed`; the four new authorization mutations failed to raise and the exact contract failed because the new eligibility section was absent.
- After correcting only the test parser's table-cell backtick handling, the focused suite still showed the intended four mutation failures (`28 passed, 4 failed`).

### Minimal GREEN change

- Added a structured `## Drafting Eligibility Contract` table to the Skill with required current approval, ready strategy status, explicit current-strategy selection/authorization, feature-tree qualification, and necessary-feature rules.
- Clarified that Feature-tree status and anchor are necessary but not sufficient; every claim feature requires both strategy selection/authorization and feature-tree qualification.
- Applied the same dual gate to ready workflow derivation, dependent additions, mapping, stop conditions, and quality checks.
- Preserved the exact two inputs, exact two outputs, and all five existing Safety Invariants.
- Repair GREEN command: `python -m pytest tests/test_plugin_contract.py -k claim_drafting -q`.
- Repair GREEN result: `32 passed, 56 deselected`.

### Ready forward evidence

- Added a fresh ready-state forward transcript to `tests/skill_scenarios/cn-claim-drafting-baseline.md`.
- Scenario supplied current approved `technical-solution`, `formal_strategy_status: ready`, available downstream, authorized F1 independent/core and F2 dependent features, plus F3 as a source-backed/anchored feature-tree feature deliberately omitted from strategy selection.
- The fresh agent produced exactly `claims-v2.md` and `claim-feature-map-v2.json`.
- It drafted one independent claim followed by one valid dependent claim, mapped every explicit/inherited occurrence with `feature_id`, `source_anchor`, `strategy_role`, and `necessity`, and recorded strategy selection/authorization for each occurrence.
- F3 was explicitly excluded despite its source-backed feature-tree status and anchor; the map records that current strategy selection/authorization is false.
- The ready transcript also confirms rejection of result-only wording, unsupported generalization, invented relationships, and substitute embodiments.

### Repair self-audit

- No other Skill was changed.
- No additional production artifact or output was added; the Skill still declares only the two required inputs and two required outputs.
- The blocked forward evidence remains intact and still records zero claim mappings and `no claim text`.
- The ready forward evidence now exercises the previously missing positive path and the exact strategy-selection boundary.

### Repair final verification

- Focused claim-drafting contract: `32 passed, 56 deselected`.
- Complete `tests/test_plugin_contract.py`: `88 passed`.
- Full test suite: `101 passed`.
- Official validator with `PYTHONUTF8=1`: `Skill is valid!`.
- Strict UTF-8 decoding passed for the Skill, metadata, complete blocked/ready evidence, and report.
- `git diff --check` returned exit 0; only the repository's existing LF-to-CRLF working-copy warnings were emitted.
