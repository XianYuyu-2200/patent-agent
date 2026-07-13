# Task 5D Report

## Status

Implemented only the `patent-prior-art-search` Skill, its exact contract and mutation tests, and its baseline/forward evidence. No other Skill was created.

## Contract-test RED

- Added `test_patent_prior_art_search_has_exact_contract` before initializing the Skill.
- Focused RED command: `python -m pytest tests/test_plugin_contract.py::test_patent_prior_art_search_has_exact_contract -v`.
- Observed result: `1 failed`; the expected failure was the missing `skills/patent-prior-art-search/SKILL.md`.
- The contract fixes the only input as `feature-tree-vN.json`, the only outputs as `search-plan-vN.md`, `prior-art-vN.json`, and `search-log-vN.json`, and the first workflow step as fact-status and feature-status validation.
- The contract also requires core-feature and combination searches, keywords, synonyms, IPC/CPC, applicant/inventor paths, complete database/query/date/screening logs, anchored quotations for key documents, anti-fabrication rules, and the prior-art-search stage boundary.

## Mutation-resistant artifact contract

- Reused the existing `_artifact_tokens` collector rather than introducing a weaker filename parser.
- Added prefix/suffix mutations for extra input and output files: `case_v3.json`, `search-brief-v3.md`, `citations_v3.json`, and `novelty-opinion-v3.md`.
- The tests prove any extra file-like token changes the exact allowed artifact set.

## Skill-disabled baseline RED

- Used a fresh agent with no inherited context, Skill, repository access, tools, or expected answer.
- The complete prompt and verbatim output are stored in `tests/skill_scenarios/patent-prior-art-search-baseline.md`.
- The baseline resisted the request to fabricate publications and refused a positive novelty conclusion.
- It nevertheless returned four non-standard artifacts, limited the plan to Chinese keyword variants, omitted IPC/CPC and applicant/inventor search paths, omitted database-level complete query logs and screening records, and crossed the boundary by creating a novelty chart and novelty opinion.

## Minimal implementation

- Initialized the unique Skill with the official `init_skill.py`. The first metadata attempt correctly rejected a 20-character short description; the Skill directory was retained and `agents/openai.yaml` was then generated with the official generator using a valid description.
- Created no scripts, references, assets, README files, or other Skill directories.
- Kept `SKILL.md` to 497 word-like tokens and 41 lines.
- Required the workflow to validate fact statuses separately from feature statuses before search planning. Only `confirmed` and `source-backed` facts and features may enter formal search; `inferred`, `missing`, `conflicted`, and unknown values block and stop.
- Defined `core` and `core-combination` as roles rather than statuses.
- Required one independent branch for every `core` feature and one branch for every `core-combination`; a combination never replaces FT-001-only or FT-002-only coverage.
- Required keywords, synonyms, IPC/CPC, applicant/inventor, and combination planning for each branch.
- Kept generic concept expressions in the search plan only. An executable record must contain database, collection, fields, verified dialect, and query.
- When a database dialect is not verified, required `verified_dialect=false`, `query=null`, `blocked-missing-verified-dialect`, the intended database/collection/fields, the generic concept expression, and a reason. The generic expression must not be described as executable syntax.
- Required missing verified classifications and applicant/inventor identities to be explicit null-query branches with `blocked-missing-verified-classification` or `blocked-missing-identity`, never guessed values.
- Required key documents to include verified publication number, publication/priority dates, retrieval source/date, feature matches, a claim/paragraph/page/figure anchor, and verbatim quotation.
- Required inaccessible or unanchored hits to remain leads, never formal evidence.
- When database access or dialect verification is absent, required empty verified results, blocked query records, full failure logs, and stop conditions rather than plausible patents or invented syntax.
- Limited output to exactly three artifacts and stopped before final novelty/inventive-step conclusions, patentability analysis, claim strategy, claim drafting, or specification drafting.
- Required `unresolved_questions` and `source_anchors` inside all three existing artifacts, with no fourth file.
- Generated `agents/openai.yaml` with display name `现有技术检索` and the project-wide default prompt `请处理当前案件并生成本阶段规定的结构化产物。`.

## Forward iterations and control-review GREEN

- The first fresh forward `/root/task_5d_implementer/prior_art_forward` was retained as `PARTIAL RED`: it respected the evidence and artifact boundaries but lacked applicant/inventor branches and a proper blocked classification record.
- Independent review then found the undefined feature-status vocabulary, the metadata prompt mismatch, and missing database binding for planned queries. Each issue first received a failing contract assertion before the Skill was changed.
- The intermediate `/root/task_5d_implementer/prior_art_forward_retry` prompt/output was not preserved verbatim before review and is explicitly marked `not recorded`; no claim is made that it is saved. Its observed failure was leaving ordinary database/syntax fields null.
- `/root/task_5d_implementer/prior_art_forward_final` is preserved completely, but control review reclassified it as partial because it described a generic Boolean expression as CNIPA syntax.
- Control-review forward `/root/task_5d_implementer/prior_art_invalid_status_forward` used the original baseline scenario unchanged. It rejected `core`/`core-combination` as illegal feature statuses before search and still returned exactly the three standard artifacts, each with unresolved questions and source anchors.
- Corrected supplementary forward `/root/task_5d_implementer/prior_art_branch_forward` produced distinct FT-001-only, FT-002-only, and FT-C01 combination branches.
- The supplementary forward kept generic Boolean expressions in the plan, set CNIPA, Google Patents, and Espacenet query records to `query=null`, `verified_dialect=false`, and `blocked-missing-verified-dialect`, and did not call them executable.
- Both control-review forwards kept verified documents empty, refused invented publications, and stopped without novelty, inventive-step, claim-strategy, or drafting conclusions.
- Model and runtime/environment identifiers were not recorded and are labelled `not recorded` rather than inferred.

## Review closure

- Fixed all three Important review findings before submission.
- Locked the unified generic default prompt from the implementation plan.
- Made status/role semantics executable and testable.
- The earlier review fix bound ordinary planned expressions to named databases while reserving null queries for classification and identity evidence gaps.
- Control review then corrected this rule: database identity alone is insufficient. Only dialect-verified records may be executable; otherwise the database branch is blocked with a null query and the generic expression remains in the search plan.
- Added exact tests and fresh forwards for independent core branches, illegal status rejection, honest dialect blocking, and unresolved/source-anchor fields in all three artifacts.

## Validation and tests

- Official validator: `$env:PYTHONUTF8='1'; python C:\Users\xiany\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\patent-prior-art-search` -> `Skill is valid!`.
- Focused contract and mutation tests: `python -m pytest tests/test_plugin_contract.py::test_patent_prior_art_search_has_exact_contract tests/test_plugin_contract.py::test_prior_art_search_artifact_token_detection_rejects_mutations -v` -> `5 passed`.
- Plugin contract file: `python -m pytest tests/test_plugin_contract.py -v` -> `14 passed`.
- Full suite: `python -m pytest -v` -> `27 passed`.
- Diff hygiene: `git diff --check` exited 0; Git only reported the existing Windows LF-to-CRLF conversion warning for the modified test file.

## Attention points

- The forward test validates behavior through emitted response artifacts; it does not access live patent databases or write a case workspace.
- IPC/CPC and applicant/inventor searches must be populated from verified seeds or supplied actor data. The Skill forbids guessing classifications or names when those sources do not exist.
- `prior-art-vN.json` may be intentionally empty when access or verification is unavailable; the paired plan and log make that absence auditable rather than misleading.
