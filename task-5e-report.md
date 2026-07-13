# Task 5E Report

## Status

Implemented only the `patentability-analysis` Skill, its exact and mutation-resistant contract tests, and its baseline/forward evidence. No other Skill was created.

## TDD RED evidence

- Added the exact contract and four input/output prefix/suffix mutation cases before the Skill existed.
- Initial focused RED command collected five tests and produced `5 failed`; the failures were the expected missing `skills/patentability-analysis/SKILL.md`.
- The fresh no-Skill baseline refused the two explicit legal shortcuts, but proposed the non-standard artifacts `patentability-analysis-v1.md` and `evidence-gap-v1.json` and used the partially affirmative phrase “新颖性暂未被 D1、D2 破坏” despite D2's missing publication date and anchor.
- Independent review mutation RED temporarily inserted `risk-register-vN.md` outside Outputs and negated the reasonable-success requirement. The old exact-contract test incorrectly passed, proving the whole-body artifact and ordered-reasoning checks were necessary.
- The ordered `3.1.`–`3.5.` inventive-step contract was added before the numbered structure; the focused test failed on the old prose list.
- The mirrored-record contract was added before Skill revision; the focused test failed because both outputs were not yet required to carry all five `source_anchor`/`status` records.
- Control review then identified four further gaps. RED tests showed numeric extensions such as `archive.7z` and `evidence.2026` were invisible, the Skill lacked protectable-contribution and filing-risk triggers, and the earlier Markdown forward was not self-contained.
- A Chinese-basename RED case (`证据.2026`) exposed a second collector defect after numeric extensions were restored.
- Final evidence-gate review found that the control forward fabricated D1 verification and anchors. A RED contract test locked missing-by-default statuses and then a second RED locked value-based evidence after a fresh agent still used “沿用输入锚点” placeholders.

## Exact artifact and evidence contract

- Inputs are exactly `feature-tree-vN.json` and `prior-art-vN.json`.
- Outputs are exactly `feature-matrix-vN.json` and `patentability-vN.md`.
- The artifact collector scans the complete Skill body and permits only those four file-like tokens. It supports numeric extensions (`.7z`, `.2026`) and Chinese basenames while rejecting numeric workflow labels such as `3.1.` because a basename must contain a letter, underscore, hyphen, or Chinese character.
- Prefix/suffix mutations cover Inputs and Outputs; elsewhere mutations cover Workflow, Stop Conditions, and Quality Checks, including numeric-extension files.
- The first workflow step separately validates fact, feature, and document-evidence statuses. Only `confirmed`/`source-backed` facts and features and `verified` documents with publication date, verbatim quotation, and claim/paragraph/page/figure anchor may enter formal analysis.
- Missing statuses, dates, quotations, and anchors are `missing`. A filename, document ID, summary statement that a document discloses a feature, or placeholder reference to an input anchor never satisfies the gate; the current context must contain the actual values.
- When actual evidence values are absent, document eligibility is false and related anchors are null. If no document is eligible, all five inventive-step values/anchors, protectable-contribution fields, and risk anchors remain null with `evidence-insufficient`; no closest prior art or distinguishing feature may be provisional.
- Search incompleteness, a missing publication date or source anchor, or a conflicted core fact forces stop or `evidence-insufficient` and forbids an affirmative legal conclusion.
- Both outputs must contain `unresolved_questions` and `source_anchors`; no third evidence-gap artifact is allowed.

## Novelty and inventive-step rules

- Novelty requires one prior-art document to directly and unambiguously disclose every necessary feature. Multiple documents may never be combined to deny novelty.
- Inventive step uses a fixed, parsed sequence: `3.1.` closest prior art, `3.2.` distinguishing features, `3.3.` actual technical problem, `3.4.` combination motivation or teaching, and `3.5.` reasonable expectation of success.
- Every step requires a separate `source_anchor`; without one, that step is `evidence-insufficient`. Combination motivation cannot be supplied from common knowledge.
- Both artifacts must mirror the five numbered records with `value`, `source_anchor`, and `status`; a missing verified anchor becomes `source_anchor: null` plus `status: evidence-insufficient`.
- Markdown must list all five records separately and directly list its own `unresolved_questions` and `source_anchors`; it may not refer to the JSON as a substitute.
- The Skill explicitly rejects the contradictory rules `Combine multiple documents to deny novelty` and `If no single identical document exists, declare inventive step established`. Mutation tests append each opposite instruction after the valid rules and require the combined body to fail.
- The Skill stops before claim strategy or claim drafting.

## Protectable contribution and filing risk

- `protectable_contribution` is required inside both artifacts and may be based only on distinguishing features plus verified technical-effect evidence. It records `distinguishing_feature_ids`, `technical_effect`, `source_anchor`, and `status`.
- `filing_application_risk` is required inside both artifacts and records `evidence_gaps`, `search_coverage`, `support_risk`, `subject_matter_risk`, `source_anchors`, and `status`.
- Missing effect evidence makes the contribution `evidence-insufficient`. Risk reporting remains an analysis record and may not become claim-scope or drafting instructions.

## Minimal implementation and metadata

- Used the official `init_skill.py` exactly once. The Skill directory count changed from four to five, and the only new Skill was `skills/patentability-analysis`.
- Created no scripts, references, assets, README, or other auxiliary Skill files.
- Final `SKILL.md` is 50 lines and contains no auxiliary resources or narrative examples.
- `agents/openai.yaml` uses display name `可专利性分析`, a valid short description, and the project-wide generic prompt `请处理当前案件并生成本阶段规定的结构化产物。`.

## Forward testing

- Complete baseline and forward evidence is stored in `tests/skill_scenarios/patentability-analysis-baseline.md`. Excerpts and whitespace-normalized transcripts are labelled accurately.
- Initial fresh forward produced exactly two standard artifacts, kept novelty single-document only, rejected both management shortcuts, and used `evidence-insufficient` for incomplete evidence.
- After review strengthened the numbered chain, a fresh supplementary forward exposed one remaining gap: the distinguishing-feature item lacked its own anchor or insufficient status.
- The next corrected forward supplied the five JSON records, but control review correctly reclassified it as PARTIAL because Markdown compressed them into one sentence and referred to JSON for unresolved questions/source anchors.
- A fresh control forward fixed the Markdown and responsibility fields but was later reclassified FAIL because it invented D1 verification, formal eligibility, and source anchors from the summary.
- The first missing-evidence forward also failed by using placeholder phrases such as “沿用 prior-art-v1.json 中 D1 的公开日、F1原文及段落/页码锚点”.
- The final fresh value-gate forward treated D1 and D2 as ineligible, kept F1/F2 missing, left 3.1–3.5 and contribution null/insufficient, recorded risk anchors as null/insufficient, and still produced only the two self-contained artifacts.

## Independent review closure

- Initial review found no Critical issues and two Important test weaknesses: extra artifacts outside Inputs/Outputs and unordered/negatable legal substrings.
- Control review found four remaining issues: missing contribution/risk duties, non-self-contained Markdown evidence, appended semantic contradictions, and numeric-extension collector blind spots.
- Final review found one additional issue: inferred D1 verification from an unverified summary.
- All findings were fixed with full-body token collection, numeric/Chinese filename cases, appended-opposite-rule mutations, exact novelty sentences, parsed numbered inventive-step order, per-step anchoring assertions, self-contained Markdown requirements, structured contribution/risk fields, missing-by-default status rules, and a value-based evidence gate that rejects file references and placeholder anchors.
- No additional research or unrelated work was performed after closure.

## Validation results

- Focused patentability contract/mutation tests: `19 passed`.
- Complete plugin contract file: `33 passed`.
- Full suite: `46 passed`.
- Official UTF-8 validator: `Skill is valid!` with `PYTHONUTF8=1`.
- Strict UTF-8 decoding succeeded for the Skill, metadata, and scenario-evidence files.
- `git diff --check` exited 0; Git only reported the existing Windows LF-to-CRLF warning for the modified test file.

## Submission

The initial Task 5E implementation was submitted as `feat: add patentability analysis skill`, followed by `fix: complete patentability analysis contract`. The final value-based evidence-gate correction is submitted in a third Codex-identity commit with subject `fix: require explicit patent evidence values`.
