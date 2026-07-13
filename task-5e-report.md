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

## Exact artifact and evidence contract

- Inputs are exactly `feature-tree-vN.json` and `prior-art-vN.json`.
- Outputs are exactly `feature-matrix-vN.json` and `patentability-vN.md`.
- The artifact collector scans the complete Skill body and permits only those four file-like tokens. Its extension rule excludes numeric workflow labels such as `3.1.` while retaining real filenames.
- Prefix/suffix mutations cover Inputs and Outputs; elsewhere mutations cover Workflow, Stop Conditions, and Quality Checks.
- The first workflow step separately validates fact, feature, and document-evidence statuses. Only `confirmed`/`source-backed` facts and features and `verified` documents with publication date, verbatim quotation, and claim/paragraph/page/figure anchor may enter formal analysis.
- Search incompleteness, a missing publication date or source anchor, or a conflicted core fact forces stop or `evidence-insufficient` and forbids an affirmative legal conclusion.
- Both outputs must contain `unresolved_questions` and `source_anchors`; no third evidence-gap artifact is allowed.

## Novelty and inventive-step rules

- Novelty requires one prior-art document to directly and unambiguously disclose every necessary feature. Multiple documents may never be combined to deny novelty.
- Inventive step uses a fixed, parsed sequence: `3.1.` closest prior art, `3.2.` distinguishing features, `3.3.` actual technical problem, `3.4.` combination motivation or teaching, and `3.5.` reasonable expectation of success.
- Every step requires a separate `source_anchor`; without one, that step is `evidence-insufficient`. Combination motivation cannot be supplied from common knowledge.
- Both artifacts must mirror the five numbered records with `source_anchor` and `status`; a missing verified anchor becomes `source_anchor: null` plus `status: evidence-insufficient`.
- The Skill stops before claim strategy or claim drafting.

## Minimal implementation and metadata

- Used the official `init_skill.py` exactly once. The Skill directory count changed from four to five, and the only new Skill was `skills/patentability-analysis`.
- Created no scripts, references, assets, README, or other auxiliary Skill files.
- Final `SKILL.md` is 46 lines and under the writing-skills 500-word-like target after concise refactoring.
- `agents/openai.yaml` uses display name `可专利性分析`, a valid short description, and the project-wide generic prompt `请处理当前案件并生成本阶段规定的结构化产物。`.

## Forward testing

- Complete baseline and forward evidence is stored in `tests/skill_scenarios/patentability-analysis-baseline.md`. The baseline and final corrected forward outputs are content-complete; intermediate forward excerpts are explicitly labelled as whitespace-normalized or excerpted rather than falsely labelled verbatim.
- Initial fresh forward produced exactly two standard artifacts, kept novelty single-document only, rejected both management shortcuts, and used `evidence-insufficient` for incomplete evidence.
- After review strengthened the numbered chain, a fresh supplementary forward exposed one remaining gap: the distinguishing-feature item lacked its own anchor or insufficient status.
- The Skill was minimally refactored to require the same five records in both outputs. A final fresh corrected forward supplied `source_anchor` and `status` on all five records, used null plus `evidence-insufficient` when unsupported, retained unresolved questions/source anchors, and created no extra artifact.

## Independent review closure

- Review found no Critical issues and two Important test weaknesses: extra artifacts outside Inputs/Outputs and unordered/negatable legal substrings.
- Both were fixed with full-body token collection, real mutation cases, exact novelty sentences, parsed numbered inventive-step order, and per-step anchoring assertions.
- No additional research or unrelated work was performed after closure.

## Validation results

- Focused patentability contract/mutation tests: `12 passed`.
- Complete plugin contract file: `26 passed`.
- Full suite: `39 passed`.
- Official UTF-8 validator: `Skill is valid!` with `PYTHONUTF8=1`.
- Strict UTF-8 decoding succeeded for the Skill, metadata, and scenario-evidence files.
- `git diff --check` exited 0; Git only reported the existing Windows LF-to-CRLF warning for the modified test file.

## Submission

The Task 5E files are submitted together in one commit authored and committed with the Codex identity and subject `feat: add patentability analysis skill`.
