# Phase 1 Skill Metadata Encoding Fix

Date: 2026-07-16 (Asia/Shanghai)

Base: `2f0646f2e0459f724262274c8e3d10c718f9527d`

## Scope

Closed the final independent signoff Important finding that the specification-
drafting and quality-review Skill interface metadata contained literal mojibake
and that the exact contract tests treated those corrupted strings as correct.

The repair is limited to the two affected `agents/openai.yaml` files, their two
exact metadata assertions, and this report. No Skill workflow body, Python
runtime behavior, template, fixture, acceptance decision, or provenance logic
changed.

## TDD RED

The contract expectations were changed before the metadata files:

- `cn-specification-drafting` requires display name `说明书撰写`, short
  description `根据已批准权利要求和技术事实起草说明书、摘要与附图方案`, and the normal
  Chinese stage prompt.
- `cn-patent-quality-review` requires display name `专利质量审查`, short
  description `审查中国专利的支持性、清楚性、一致性与交付风险`, and the same normal
  Chinese stage prompt.

Focused RED command:

```text
python -m pytest -q -p no:cacheprovider \
  tests/test_plugin_contract.py::test_cn_specification_drafting_has_exact_contract \
  tests/test_plugin_contract.py::test_cn_patent_quality_review_has_exact_contract
```

RED result: **2 failed in 0.52s**. Each failure showed the persisted mojibake
display name differing from the readable plan-required Chinese value.

## Implementation

- Replaced the corrupted specification-drafting display name, short
  description, and default prompt with readable UTF-8 Chinese matching its
  Skill purpose.
- Replaced the corrupted quality-review display name, short description, and
  default prompt with readable UTF-8 Chinese matching its Skill purpose.
- Tightened both contract tests to exact values so nonempty but corrupted
  metadata cannot pass again.

## GREEN and verification

- Exact RED nodes -> **2 passed in 0.42s**.
- Complete plugin-contract suite -> **338 passed in 1.54s**.
- Full suite -> **516 passed in 8.97s**.
- All twelve official Skill validators -> **12/12 `Skill is valid!`**.
- Official plugin validator -> **`Plugin validation passed`**.
- `python -m compileall -q -f src tests` -> exit 0.
- `git diff --check` -> exit 0; Git emitted only Windows LF/CRLF working-copy
  notices.
- Independent parse of every `skills/*/agents/openai.yaml` rejected replacement
  or Unicode private-use characters and completed with
  **`metadata unicode audit: PASS`**.

## Files changed

- `skills/cn-specification-drafting/agents/openai.yaml`
- `skills/cn-patent-quality-review/agents/openai.yaml`
- `tests/test_plugin_contract.py`
- `.superpowers/sdd/phase-1-metadata-fix-report.md`
