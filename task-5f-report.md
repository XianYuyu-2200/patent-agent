# Task 5F Report

## Status

Implemented only the `cn-claim-strategy` Skill, its contract/mutation tests, and complete baseline/forward evidence. No other Skill was created.

## TDD RED evidence

- Added the exact input/output, full-body artifact, numeric-extension, Chinese-basename, and appended-contradiction tests before the Skill existed.
- Initial focused command collected eleven claim-strategy tests and produced `11 failed`; each failure was caused by the missing Skill.
- The fresh no-Skill baseline proposed three artifacts instead of one, including a claim-set and evidence matrix.
- The baseline wrote invention, utility-model, and conditional software-method claim skeleton sentences despite the strategy-only boundary.
- The baseline supplied concrete unsupported substitute/design-around structures, gave formal dual-filing and independent-claim counts, and rated business/risk values even though the current prompt did not contain the required protectable-contribution and risk values.

## Exact contract and evidence gate

- Inputs are exactly `feature-tree-vN.json` and `patentability-vN.md`.
- Output is exactly `protection-strategy-vN.md`.
- The reused artifact collector scans the complete Skill body and accepts numeric extensions and Chinese basenames while rejecting numeric workflow labels.
- Input/output and elsewhere mutations cover prefix/suffix placement, `.7z`, `.2026`, and a Chinese numeric-extension basename.
- A parsed Safety Invariants table fixes `essential_feature_removal`, `unanchored_alternative_inclusion`, `blocked_mode_claim_text`, and `utility_model_method_software_object` to `forbidden`.
- Sixteen Chinese, English, and synonymous appended contradictions cover deleting necessary features for breadth, inventing unanchored substitutes, drafting claim text while blocked, and treating software-control methods as utility-model objects. A valid body plus any opposite instruction fails the contract.
- Workflow Step 1 is a value-based gate. A formal feature requires an actual `confirmed` or `source-backed` value, a concrete source anchor, and actual protectable-contribution or risk values in the current inputs.
- Filenames, role labels, statements that an input should contain evidence, and placeholder anchors do not pass the gate.
- `inferred`, `missing`, `conflicted`, and `evidence-insufficient` material remains provisional, unavailable downstream, and outside every formal feature tier.
- If the core contribution, necessary feature, concrete anchor, or decision values are insufficient, formal strategy is `evidence-insufficient` or `blocked`, never filing-ready.

## Strategy responsibilities and boundaries

- The single strategy artifact covers protection subjects, Chinese invention/utility-model layout, proposed independent subjects and counts, core/secondary/fallback tiers, business value, design-around paths, and unity/support/subject-matter risk.
- Necessary features cannot be deleted merely to broaden scope.
- Unsupported alternatives, effects, contributions, business values, and workarounds cannot be invented.
- Mechanical and hardware product shape/structure/combination may be evaluated for utility-model protection.
- Pure methods, software, algorithms, and software itself cannot be repackaged as utility models.
- The Skill produces strategy structure only. It forbids claim sentences, claim text, claim drafting, specification drafting, and any additional artifact.
- The output directly contains its own `unresolved_questions` and `source_anchors`.

## Minimal implementation and metadata

- Called the official `init_skill.py` exactly once. It created the Skill directory and template, then stopped because the initial short description was below the validator length. The initializer was not called again; the generated files were completed with `apply_patch`.
- Created only `SKILL.md` and `agents/openai.yaml` inside the new Skill.
- Added no scripts, references, assets, examples, README, or auxiliary output definitions.
- Metadata uses readable UTF-8 values: display name `权利要求策略` and generic prompt `请处理当前案件并生成本阶段规定的结构化产物。`.

## Forward testing

- Complete baseline and forward evidence is stored in `tests/skill_scenarios/cn-claim-strategy-baseline.md`.
- The fresh same-scenario forward produced only `protection-strategy-v1.md`.
- It set `formal_strategy_status: evidence-insufficient`, `downstream_availability: blocked`, and `claim_drafting_status: blocked` because F1 lacked the current protectable-contribution and risk values.
- It preserved F1 only as a provisional, non-deletable candidate; excluded F2 from all formal tiers; and did not invent concrete substitutes.
- It rejected software-control methods as utility-model subject matter and did not write any claim sentence or claim text.
- The output was self-contained with unresolved questions and source anchors. No corrected forward was needed.

## Review closure

- Initial independent review identified the then-in-progress missing forward transcript; the complete verbatim forward was subsequently appended and the temporary marker removed.
- Final re-review against the completed evidence and repository convention found no remaining Critical or Important issues.
- A later review correctly identified that the metadata test had locked mojibake and that fixed rejection-sentence counts were weaker than a machine-parsed decision contract. RED produced `17 failed, 6 passed`; GREEN produced `23 passed` after adding the invariant table, multilingual/synonymous mutation cases, and exact readable UTF-8 metadata.

## Validation results

- Focused claim-strategy tests: `23 passed`.
- Complete plugin contract file: `56 passed`.
- Full suite: `69 passed`.
- Official UTF-8 validator: `Skill is valid!` with `PYTHONUTF8=1`.
- Strict UTF-8 decoding succeeded for the Skill and metadata; the final verification also covers the scenario evidence and report.

## Submission

The initial implementation and this review correction are submitted as Codex-identity commits.
