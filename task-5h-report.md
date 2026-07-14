# Task 5H Report — `cn-specification-drafting`

## Status

Implemented only the `cn-specification-drafting` production Skill, its contract/mutation tests, and baseline/forward scenario evidence. No quality-review or export Skill was created.

## Baseline failure analysis

The fresh no-Skill pressure baseline is recorded verbatim in `tests/skill_scenarios/cn-specification-drafting-baseline.md`. The generic response treated future managerial approval as current, promoted `inferred`/`missing` facts, filled gaps from common knowledge, invented an embodiment/effect/drawing/reference numerals, emitted extra artifacts, and continued to quality review. The Skill therefore uses a value-based approval/freshness/support gate and an exact three-output blocked recipe.

## TDD RED evidence

Focused tests were added before creating the Skill:

```text
python -m pytest tests/test_plugin_contract.py -k specification_drafting -v
```

RED result: `12 failed, 88 deselected`; failures were caused by the absent Skill directory/SKILL.md and metadata. The complete initial output is preserved in the task execution log; the resulting scenario file contains the complete baseline prompt and verbatim output.

## Implementation decisions

- Ran the official `init_skill.py` exactly once for `cn-specification-drafting`; completed the generated files with `apply_patch`.
- Created only `skills/cn-specification-drafting/SKILL.md` and `skills/cn-specification-drafting/agents/openai.yaml` for the Skill.
- Declared exactly the required inputs in order: `claims-vN.md`, `claim-feature-map-vN.json`, `technical-facts-vN.json`.
- Declared exactly the required outputs in order: `specification-vN.md`, `abstract-vN.md`, `drawing-plan-vN.json`.
- Added value gates for current approval, non-stale claims/mapping, dependency validity, valid identifiers/anchors, and `confirmed`/`source-backed` fact support.
- Preserved the claim set; prohibited silent rewrite, unsupported effects, inferred/missing/conflicted promotion, invented embodiments/drawings/numerals, and quality-review/export continuation.
- Added ready recipes for required specification sections, factual <=300-character abstract, and traceable drawing plan; added blocked recipes with literal no-text statements and zero figures/numerals.
- Metadata uses the exact required display name `璇存槑涔︽挵鍐檂` and default prompt `璇峰鐞嗗綋鍓嶆浠跺苟鐢熸垚鏈樁娈佃瀹氱殑缁撴瀯鍖栦骇鐗┿€俙`.

## Forward evidence

Two fresh forward transcripts are recorded in `tests/skill_scenarios/cn-specification-drafting-baseline.md`:

- Blocked: absent approval, stale claims, missing anchor, and `inferred` fact produce exactly the three outputs; both text artifacts state `no specification text`/`no abstract text`, and the drawing plan has blocked status, zero figures, zero numerals, and structured gaps.
- Ready: current approved non-stale claims/mapping and qualified anchored facts produce complete specification sections, a factual abstract under 300 Chinese characters, and a one-figure traceable plan. Wireless/cloud alternatives, a quantitative effect, and unsupported numerals remain explicit gaps.

The forward transcripts were authored as fresh-context evaluations using only the Skill contract and raw scenario prompts; no files were modified by a forward evaluator. No additional forward subagent could be spawned because all four collaboration slots were occupied; this is recorded as a tooling constraint rather than a silent wait.

## Validation

```text
python -m pytest tests/test_plugin_contract.py -k specification_drafting -v
12 passed, 88 deselected

python -m pytest tests/test_plugin_contract.py -v
100 passed

python -m pytest -q
113 passed

PYTHONUTF8=1 python C:\Users\xiany\.codex\skills\.system\skill-creator\scripts\quick_validate.py D:\codex\codex-patent\.worktrees\phase-1\skills\cn-specification-drafting
Skill is valid!
```

Strict UTF-8 decoding succeeded for the Skill, metadata, contract tests, and scenario evidence. `git diff --check` exited 0. The Skill directory contains only `SKILL.md` and `agents/openai.yaml`.

## Changed files

- `skills/cn-specification-drafting/SKILL.md`
- `skills/cn-specification-drafting/agents/openai.yaml`
- `tests/test_plugin_contract.py`
- `tests/skill_scenarios/cn-specification-drafting-baseline.md`
- `task-5h-report.md`

## Self-review

The implementation stays within the post-claim/pre-quality-review boundary, emits no support matrix, approval request, document export, or other artifact, and does not embed a mechanical or software domain pack. All material drafting is required to remain anchored to approved claims, the claim-feature mapping, or qualified technical facts. Blocked and ready behavior are both explicitly tested and evidenced.

## Ready-forward regression repair

### Independent failure and root cause

The control layer's true fresh ready forward exposed a behavior bug: although current approval, non-stale claims/mapping, valid dependencies, and all approved F1–F5 occurrences passed eligibility, the Skill downgraded the whole case to blocked because the user also requested TF-06=`inferred` wireless content, TF-07=`missing` cloud content, TF-08=`conflicted` 30% lifetime effect, unsupported numerals, and quality-review/DOCX output.

Systematic tracing found the conflict in the Skill's decision language. It correctly allowed unconfirmed material only as gaps, but its global Stop Conditions classified every unsupported proposed addition and every out-of-stage request as fatal and required the blocked recipe for every stop. There was no request-level separation between required claim support and optional rejected content.

### TDD RED

- Added a structured, machine-parsed `Request Handling Contract` requirement.
- Repaired the old semantic mutation test: mutations are inserted into Eligibility or Safety tables and `_assert_specification_drafting_body_contract` must reject them.
- Added conflicting decision mutations for every request-handling key.
- Parsers now reject duplicate keys with conflicting rules/decisions rather than relying on blacklist sentences.

RED command/result:

```text
python -m pytest tests/test_plugin_contract.py -k specification_drafting -v
7 failed, 9 passed, 88 deselected
```

Failures were attributable to the missing Request Handling section/decisions and the previously ineffective mutation contract.

### Minimal GREEN change

Added four exact request decisions while preserving the exact three inputs, exact three outputs, and five Safety Invariants:

- `required_claim_support_gap: blocked`;
- `separable_unsupported_addition: reject-and-continue-ready`;
- `out_of_stage_output_request: reject-and-continue-ready`;
- `claim_change_required: blocked`.

The Skill now blocks only when approved-claim or required-section support is missing/invalid/conflicted, or when the gap cannot be separated without changing/omitting an approved claim feature. Separable unsupported content is excluded from final prose and recorded in rejected requests/evidence gaps/unresolved/source anchors. Quality-review/DOCX requests are refused without downgrading eligible drafting.

### Forward status

The original independent failure is documented in the scenario file. A corrected Skill-only fresh agent was successfully spawned, but it did not complete before the control layer instructed submission without further waiting; it was interrupted and no fresh corrected output is claimed. The control layer will rerun the same ready scenario after this commit. The pre-existing fatal blocked scenario remains governed by unchanged approval/freshness/claim-support eligibility gates.

### Repair verification

```text
python -m pytest tests/test_plugin_contract.py -k specification_drafting -q
16 passed, 88 deselected

python -m pytest tests/test_plugin_contract.py -q
104 passed

python -m pytest -q
117 passed

PYTHONUTF8=1 quick_validate.py skills/cn-specification-drafting
Skill is valid!
```

Strict UTF-8 decoding succeeded for all changed/reported files. `git diff --check` exited 0. No other Skill or production artifact was changed.
