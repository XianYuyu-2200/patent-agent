# Software/AI golden-case forward test

No customer, applicant, inventor, filing, dataset, or deployment identity is present in this record.

## Baseline prompt

> Use the Codex plugin at `D:\codex\codex-patent\.worktrees\phase-1` to review the anonymized golden case in `tests\fixtures\software_case\case.json`. Work read-only. Emit the review artifact you would save, unresolved questions, whether delivery/export is allowed, and the next allowed action. Do not inspect any expected-review file. Return the emitted artifact and reasoning only; do not modify files.

## Baseline emitted artifact

```json
{
  "case_id": "GOLDEN-SW-001",
  "review_status": "needs-clarification",
  "technical_contribution": {
    "fact_ids": ["S-F001", "S-F002", "S-F003", "S-F004"],
    "summary": "采集设备振动时序，经滑动窗口与频域处理判定异常分量，控制器向电机驱动器发送降速指令，以缩短超阈值振动持续时间。"
  },
  "business_only": {
    "fact_id": "S-B001",
    "classification": "business-only",
    "severity": "high",
    "fact_status": "source-backed",
    "source_anchors": ["SRC-S-03#运营说明段落1"],
    "disposition": "exclude from technical contribution/claim scope",
    "reason": "会员等级决定告警服务计费优先级，不改变 sensing/processing/control mechanism"
  },
  "delivery_export": {
    "allowed": false,
    "reason": "mining-stage review has unresolved implementation/enablement and effect-evidence questions"
  },
  "next_allowed_action": "Obtain engineering clarifications and source anchors, then rerun review before claim drafting or export."
}
```

## Baseline result

PASS. Without reading `expected-review.json`, the baseline separated the source-backed sensor-processing-control chain from S-B001, classified S-B001 as `business-only` with high severity, excluded it from technical contribution, and refused export. No behavioral failure was detected.

## Forward prompt

> Use the Codex plugin at `D:\codex\codex-patent\.worktrees\phase-1` to review the anonymized golden case in `tests\fixtures\software_case\case.json`. Work read-only. Emit the review artifact you would save, unresolved questions, whether delivery/export is allowed, and the next allowed action. Do not inspect any expected-review file. Return the emitted artifact and reasoning only; do not modify files.

## Forward emitted artifact

```json
{
  "artifact_type": "golden-case-independent-review",
  "case_id": "GOLDEN-SW-001",
  "technical_domain": "software-ai",
  "stage_reviewed": "mining",
  "review_status": "completed-with-issues",
  "issues": [
    {
      "issue_id": "business-only-S-B001",
      "rule": "business-only",
      "severity": "high",
      "fact_id": "S-B001",
      "statement": "根据客户会员等级提高告警服务的计费优先级。",
      "fact_status": "source-backed",
      "final_text_allowed": true,
      "source_anchors": ["SRC-S-03#运营说明段落1"],
      "explanation": "会员等级、计费队列和服务优先级属于经营规则；现有材料未显示其参与振动采集、频域处理、异常判定、设备控制或技术效果的因果链。",
      "suggested_action": "将 S-B001 隔离为非技术业务事实，不得作为技术贡献、必要技术特征或技术效果；不得补造硬件或算法关联。",
      "blocks_export": true
    }
  ],
  "technical_solution_assessment": {
    "status": "source-backed-but-not-approved",
    "technical_contribution_fact_ids": ["S-F001", "S-F002", "S-F003", "S-F004"],
    "conclusion": "振动传感器采样—窗口化和频域判定—降速指令—旋转设备控制—缩短超阈值振动持续时间形成来源可追溯的技术链。"
  },
  "open_issue_counts": {"critical": 0, "high": 1, "medium": 0, "low": 0},
  "delivery_decision": {
    "allowed": false,
    "blocks_export": true,
    "reasons": ["开放的 high business-only 问题", "案件仍处于 mining", "尚无 final-delivery 批准"]
  },
  "next_allowed_action": {
    "stage": "mining",
    "production_skill": "patent-invention-mining",
    "action": "保留 S-F001 至 S-F004 的来源锚点，将 S-B001 隔离为非技术业务事实，并把实现缺口写入访谈问题。"
  }
}
```

## Forward result

PASS. The fresh task independently matched the stable `business-only` rule, high severity, S-B001 identifier, technical-chain separation, no-fabrication requirement, and export block. `expected-review.json` was not used as an input.

## Resulting Skill change

Added the same domain-neutral `Golden-Case Regression` protocol to the orchestrator. The baseline exposed no software behavioral failure, so the Skill was not expanded with fixture-specific technical content; the existing software domain pack remains the source of business-rule and technical-effect judgments.
