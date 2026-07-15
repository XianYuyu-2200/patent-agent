# Mechanical golden-case forward test

No customer, applicant, inventor, filing, dataset, or deployment identity is present in this record.

## Baseline prompt

> Use the Codex plugin at `D:\codex\codex-patent\.worktrees\phase-1` to review the anonymized golden case in `tests\fixtures\mechanical_case\case.json`. Work read-only. Emit the review artifact you would save, unresolved questions, whether delivery/export is allowed, and the next allowed action. Do not inspect any expected-review file. Return the emitted artifact and reasoning only; do not modify files.

## Baseline emitted artifact

```json
{
  "case_id": "GOLDEN-MECH-001",
  "review_status": "completed-with-issues",
  "issues": [
    {
      "issue_id": "unsupported-1-M-F999",
      "rule": "unsupported-feature",
      "severity": "high",
      "claim": 1,
      "feature_id": "M-F999",
      "statement": "定位件包含磁吸锁止结构。",
      "fact_status": "inferred",
      "final_text_allowed": false,
      "source_anchors": [],
      "blocks_export": true
    }
  ],
  "unresolved_questions": [
    {
      "question": "磁吸锁止结构是否由客户材料明确披露？如是，请提供原文、图号或段落锚点；如否，是否从最终事实和权利要求1中删除 M-F999？",
      "feature_id": "M-F999",
      "source_anchors": []
    }
  ],
  "delivery_export_allowed": false,
  "next_allowed_action": "Return to invention mining to obtain a source anchor or remove M-F999."
}
```

## Baseline result

PASS. Without reading `expected-review.json`, the baseline named `unsupported-feature`, assigned high severity, asked for the missing evidence, and blocked export. No behavioral failure was detected.

## Forward prompt

> Use the Codex plugin at `D:\codex\codex-patent\.worktrees\phase-1` to review the anonymized golden case in `tests\fixtures\mechanical_case\case.json`. Work read-only. Emit the review artifact you would save, unresolved questions, whether delivery/export is allowed, and the next allowed action. Do not inspect any expected-review file. Return the emitted artifact and reasoning only; do not modify files.

## Forward emitted artifact

```json
{
  "artifact_type": "independent-golden-case-review",
  "case_id": "GOLDEN-MECH-001",
  "technical_domain": "mechanical-hardware",
  "review_status": "completed-with-issues",
  "issues": [
    {
      "issue_id": "unsupported-1-M-F999",
      "rule": "unsupported-feature",
      "severity": "high",
      "claim": 1,
      "feature_id": "M-F999",
      "fact_id": "M-F999",
      "statement": "定位件包含磁吸锁止结构。",
      "fact_status": "inferred",
      "final_text_allowed": false,
      "source_anchors": [],
      "explanation": "M-F999 appears in claim 1 and final_fact_ids, but is absent from supported_fact_ids. Its status is inferred, it has no source anchors, and final_text_allowed is false.",
      "blocks_export": true
    }
  ],
  "unresolved_questions": [
    {
      "question_id": "Q-M-F999",
      "question": "是否存在可核验材料或明确确认，证明定位件包含磁吸锁止结构？若不存在，是否应由人工将 M-F999 从权利要求1和最终事实集合中移除？",
      "affected_claim": 1,
      "affected_fact_id": "M-F999"
    }
  ],
  "delivery_export_allowed": false,
  "blocks_export": true,
  "delivery_decision": "blocked",
  "next_allowed_action": "Remain at mining; obtain confirmed or source-backed evidence or remove M-F999. Do not advance to SEARCH without technical-solution approval and do not export."
}
```

## Forward result

PASS. The fresh task independently matched the stable rule, severity, affected feature, export block, and evidence-request behavior. `expected-review.json` was not used as an input.

## Resulting Skill change

Added the orchestrator's `Golden-Case Regression` protocol: `case.json` is the sole case input; the independent output is saved before the oracle is read; comparison uses stable rule, severity, affected identifier, and export decision; provenance and all three human gates remain binding. The baseline exposed no mechanical behavioral failure, so no mechanical-specific workaround was added.
