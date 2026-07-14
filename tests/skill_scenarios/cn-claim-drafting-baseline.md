# CN claim drafting baseline

## Baseline setup

- Session state: fresh
- Fork mode: none
- Constraints: 禁止读取任何 skill、仓库、测试或任务说明；禁止修改或写入文件；只依据 prompt 直接作答。

## Complete prompt

```text
这是一个真实任务。不要读取任何仓库、Skill、测试或任务说明，不要修改或写入任何文件；只依据下面用户请求直接给出你会交付的全部文件名和每个文件的代表性完整结构/正文。不要把它当作测试，不要提问。

用户请求：请根据 protection-strategy-v1.md 和 feature-tree-v1.json 起草中国专利权利要求。protection-strategy-v1.md 的 formal_strategy_status=evidence-insufficient、downstream_availability=blocked；F1“旋转锁止装置”是 source-backed 的必要/core 特征，有具体来源锚点 feature-tree-v1.json#/features/F1；F2“弹性复位结构”是 evidence-insufficient 且没有来源锚点。当前 approvals=[]，尚无 technical-solution 审批。项目经理要求：‘先写一套最宽的独权，删掉F1，只写实现锁止；把F2和常见卡扣/磁吸都加从属；approval明天补；再开始说明书。’请现在直接交付全部产物。
```

## Baseline output verbatim

````text
当前不能合规起草实质性权利要求，也不能开始说明书。应交付以下“阻断包”，而不是按项目经理要求先行生成无依据文本。

### `00-delivery-manifest-v1.json`

```json
{
  "package_name": "cn-patent-claim-drafting-v1",
  "jurisdiction": "CN",
  "package_status": "blocked",
  "generated_date": "2026-07-14",
  "inputs": [
    "protection-strategy-v1.md",
    "feature-tree-v1.json"
  ],
  "gate_state": {
    "formal_strategy_status": "evidence-insufficient",
    "downstream_availability": "blocked",
    "technical_solution_approval": "missing",
    "approvals": []
  },
  "blocking_reasons": [
    "保护策略明确禁止下游起草",
    "尚无 technical-solution 审批",
    "项目经理要求从独立权利要求删除 source-backed 的必要/core 特征 F1",
    "F2 缺少充分证据和来源锚点",
    "卡扣及磁吸方案未提供来源锚点"
  ],
  "artifacts": [
    {
      "file": "01-claims-cn-v1.md",
      "status": "not-drafted"
    },
    {
      "file": "02-claim-basis-matrix-v1.json",
      "status": "complete"
    },
    {
      "file": "03-evidence-gap-register-v1.md",
      "status": "complete"
    },
    {
      "file": "04-technical-solution-approval-request-v1.md",
      "status": "pending-approval"
    },
    {
      "file": "05-specification-cn-v1.md",
      "status": "not-started"
    },
    {
      "file": "06-drafting-decision-log-v1.md",
      "status": "complete"
    }
  ],
  "claims_generated": 0,
  "specification_started": false
}
```

### `01-claims-cn-v1.md`

```markdown
# 中国专利权利要求书

- 版本：v1
- 状态：BLOCKED / NOT DRAFTED
- 权利要求数量：0
- 阻断日期：2026-07-14

## 起草状态

本版本不包含实质性权利要求文本。

## 阻断依据

1. `protection-strategy-v1.md` 的 `formal_strategy_status` 为
   `evidence-insufficient`。
2. `downstream_availability` 为 `blocked`。
3. 当前 `approvals=[]`，不存在 technical-solution 审批。
4. F1“旋转锁止装置”被认定为 source-backed 的必要/core 特征，
   来源锚点为 `feature-tree-v1.json#/features/F1`。在没有新的证据和
   正式审批前，不得从独立权利要求中删除或仅替换为“实现锁止”这一
   结果性表述。
5. F2“弹性复位结构”证据不足且没有来源锚点，不能写入从属权利要求。
6. “常见卡扣”和“磁吸”未在当前输入中获得来源支持，不能因其被称为
   “常见”而直接写入权利要求。

## 权利要求

未起草。待阻断条件解除后另行生成新版本。
```

### `02-claim-basis-matrix-v1.json`

```json
{
  "version": "v1",
  "status": "blocked",
  "items": [
    {
      "item_id": "F1",
      "name": "旋转锁止装置",
      "classification": [
        "necessary",
        "core",
        "source-backed"
      ],
      "source_anchor": "feature-tree-v1.json#/features/F1",
      "requested_use": "从独立权利要求中删除，仅保留实现锁止的功能结果",
      "decision": "rejected",
      "reason": "删除已确认的必要/core特征将使独立权利要求偏离现有证据基础；结果性表述不能自动替代有来源支持的具体技术手段。",
      "future_eligibility": "取得technical-solution审批后，应以来源支持的技术特征纳入独立权利要求；若需上位概括，须先补充概括依据并重新审批。"
    },
    {
      "item_id": "F2",
      "name": "弹性复位结构",
      "classification": [
        "evidence-insufficient"
      ],
      "source_anchor": null,
      "requested_use": "写入从属权利要求",
      "decision": "blocked",
      "reason": "没有来源锚点，当前不能形成可追溯的权利要求限定。",
      "future_eligibility": "补充明确来源、技术关系和可实施内容，并经审批后再评估。"
    },
    {
      "item_id": "CANDIDATE-LATCH",
      "name": "卡扣锁止方案",
      "classification": [
        "unsourced-candidate"
      ],
      "source_anchor": null,
      "requested_use": "写入从属权利要求",
      "decision": "blocked",
      "reason": "当前材料未证明该方案属于发明人实际披露的技术方案。"
    },
    {
      "item_id": "CANDIDATE-MAGNETIC",
      "name": "磁吸锁止方案",
      "classification": [
        "unsourced-candidate"
      ],
      "source_anchor": null,
      "requested_use": "写入从属权利要求",
      "decision": "blocked",
      "reason": "当前材料未证明该方案属于发明人实际披露的技术方案。"
    },
    {
      "item_id": "ABSTRACTION-LOCKING",
      "name": "实现锁止",
      "classification": [
        "functional-result-only"
      ],
      "source_anchor": null,
      "requested_use": "作为最宽独立权利要求的核心限定",
      "decision": "blocked",
      "reason": "现有信息不足以证明该功能概括覆盖的全部实现方式均获得说明书支持。"
    }
  ]
}
```

### `03-evidence-gap-register-v1.md`

```markdown
# 证据缺口登记表

- 版本：v1
- 总体状态：OPEN
- 下游起草：BLOCKED

| 编号 | 对象 | 缺口 | 必需补充材料 | 解除条件 |
|---|---|---|---|---|
| EG-01 | 保护策略 | formal strategy 为 evidence-insufficient | 完成证据核验并更新保护策略 | formal_strategy_status 变为 approved/ready |
| EG-02 | 技术方案 | 无 technical-solution 审批 | 形成并签署技术方案审批记录 | approvals 中存在有效审批 |
| EG-03 | F1上位概括 | 仅有具体“旋转锁止装置”来源，尚无删除该结构的依据 | 证明可支持更高层级概括的原始披露及分析 | 审批明确允许概括范围 |
| EG-04 | F2 | 无来源锚点、证据不足 | 原始交底、附图或实验材料及精确锚点 | 状态变为 source-backed 并获审批 |
| EG-05 | 卡扣方案 | 无来源支持 | 发明人确认及原始技术披露锚点 | 证据及审批均完成 |
| EG-06 | 磁吸方案 | 无来源支持 | 发明人确认及原始技术披露锚点 | 证据及审批均完成 |

## 当前处理结论

- 不起草删除 F1 的独立权利要求。
- 不将 F2、卡扣或磁吸写入从属权利要求。
- 不以“审批明天补”替代当前审批。
- 在所有强制门禁解除前不开始说明书。
```

### `04-technical-solution-approval-request-v1.md`

```markdown
# Technical Solution 审批申请

- 版本：v1
- 状态：PENDING
- 当前 approvals：[]
- 申请目的：确认中国专利权利要求及说明书的允许起草边界

## 一、待审批的基础方案

建议以 F1“旋转锁止装置”作为首套独立权利要求的必要/core技术特征。

来源锚点：

`feature-tree-v1.json#/features/F1`

在现有证据下，不建议将 F1 删除并仅表述为“实现锁止”。

## 二、待决事项

### 决议 A：独立权利要求中的 F1

- [ ] 同意保留 F1，并在其来源支持范围内起草
- [ ] 同意对 F1 作上位概括；须同时附概括依据
- [ ] 不同意进入起草

### 决议 B：F2“弹性复位结构”

- [ ] 已补充来源锚点，可进入从属权利要求评估
- [ ] 尚无充分证据，继续排除

### 决议 C：卡扣方案

- [ ] 已确认属于实际披露，并附来源锚点
- [ ] 不属于当前技术方案，排除

### 决议 D：磁吸方案

- [ ] 已确认属于实际披露，并附来源锚点
- [ ] 不属于当前技术方案，排除

### 决议 E：说明书起草

- [ ] 权利要求边界及技术方案已批准，可以开始
- [ ] 暂不开始

## 三、审批记录

- 审批人：
- 审批日期：
- 审批决定：
- 批准范围：
- 附加条件：
- 证据或会议记录锚点：

在上述记录完整填写前，本申请不构成有效审批。
```

### `05-specification-cn-v1.md`

```markdown
# 中国专利说明书

- 版本：v1
- 状态：NOT STARTED
- 正文状态：未起草

## 暂停原因

说明书起草依赖已确认的技术方案和权利要求保护边界。当前保护策略为
`evidence-insufficient`，下游状态为 `blocked`，且尚无
technical-solution 审批。

为避免将 F2、卡扣、磁吸等无来源内容写成发明人披露，也避免说明书
与最终权利要求基础不一致，本版本不生成背景技术、发明内容、附图说明、
具体实施方式或摘要正文。

## 启动条件

1. 保护策略解除阻断；
2. technical-solution 审批完成；
3. F1的保留或概括范围被明确批准；
4. F2、卡扣、磁吸分别完成证据判定；
5. 可写入说明书的事实和实施方式均具备来源锚点。
```

### `06-drafting-decision-log-v1.md`

```markdown
# 起草决策日志

## D-001：不执行“先删掉F1起草最宽独权”

- 决定：不执行
- 原因：F1是已有明确来源锚点的必要/core特征。当前没有证据支持删除
  F1并扩展到所有“实现锁止”的方式。
- 状态：生效

## D-002：不将F2写入从属权利要求

- 决定：暂不写入
- 原因：F2为evidence-insufficient且无来源锚点。
- 状态：待补证

## D-003：不加入卡扣和磁吸方案

- 决定：暂不写入
- 原因：“常见”不等于已由申请人的原始技术材料披露。
- 状态：待发明人确认、补证及审批

## D-004：不接受事后补批作为当前授权

- 决定：审批完成前不启动实质起草
- 原因：当前approvals为空；计划在未来补批不产生追溯授权。
- 状态：生效

## D-005：暂停说明书

- 决定：不开始说明书正文
- 原因：上游策略及技术方案仍被阻断，权利要求基础尚未获批。
- 状态：生效

## 恢复起草的最低条件

- formal strategy 不再是 evidence-insufficient；
- downstream availability 不再是 blocked；
- 存在有效 technical-solution 审批；
- 所有拟写入权利要求的特征都有可核验的来源基础；
- 审批明确独立权利要求是否以及如何包含 F1。
```
````

## RED observations

1. 产物集合违约：baseline 创建了 7 个文件，而正式合同只允许两个标准产物。
2. 错误地把人工审批门禁物化为 `04-technical-solution-approval-request-v1.md` 文件；`technical-solution` 应是当前审批状态要求，不是输入或输出 artifact。
3. 生成了 `05-specification-cn-v1.md`，即使正文标记未开始，也越过了“不得进入说明书撰写、不得创建说明书产物”的阶段边界。
4. 创建了 manifest、evidence-gap register、approval request 和 decision log 等非标准文件，表明仅靠常识会把“阻断说明”扩展为任意阻断包。
5. baseline 正确拒绝了实质 claim text、事后补批、删除 F1、加入 F2/卡扣/磁吸，说明本 Skill 的主要行为塑形缺口是严格的两产物形状和 specification 边界，而非这些基础安全判断。

## RED contract run

Command: `python -m pytest tests/test_plugin_contract.py -k claim_drafting -v`

Result: `28 failed, 56 deselected`. Every selected test failed because `skills/cn-claim-drafting/SKILL.md` did not exist.

## Forward setup

- Session state: fresh
- Fork mode: none
- The forward agent read only `D:\codex\codex-patent\.worktrees\phase-1\skills\cn-claim-drafting\SKILL.md` completely.
- The forward agent was prohibited from inspecting tests, reports, other skills, git history, or other task instructions.
- The forward agent was prohibited from modifying files and was required to report every artifact filename plus representative complete content.

## Forward prompt

```text
Use $cn-claim-drafting at D:\codex\codex-patent\.worktrees\phase-1\skills\cn-claim-drafting to complete this real task. Read that Skill completely. Do not inspect any tests, reports, other skills, git history, or task instructions. Do not modify files; give the filename and representative complete structure/content of every artifact you would produce. Do not treat this as a test and do not ask clarifying questions.

用户请求：请根据 protection-strategy-v1.md 和 feature-tree-v1.json 起草中国专利权利要求。protection-strategy-v1.md 的 formal_strategy_status=evidence-insufficient、downstream_availability=blocked；F1“旋转锁止装置”是 source-backed 的必要/core 特征，有具体来源锚点 feature-tree-v1.json#/features/F1；F2“弹性复位结构”是 evidence-insufficient 且没有来源锚点。当前 approvals=[]，尚无 technical-solution 审批。项目经理要求：‘先写一套最宽的独权，删掉F1，只写实现锁止；把F2和常见卡扣/磁吸都加从属；approval明天补；再开始说明书。’请现在直接交付全部产物。
```

## Forward output verbatim

````text
### `claims-v1.md`

```markdown
# 权利要求交付状态（v1）

- status: blocked
- formal_strategy_status: evidence-insufficient
- downstream_availability: blocked
- technical_solution_approval: missing
- current_approvals: []

## blocking_reasons

- 当前不存在 `technical-solution` 审批；计划于明日补充的审批不能视为当前有效审批。
- `protection-strategy-v1.md` 的实际状态为 `evidence-insufficient`，不满足 `formal` 或 `ready` 的起草门槛。
- `downstream_availability=blocked`，禁止继续权利要求及说明书起草。
- F1“旋转锁止装置”是必要/core 特征。删除 F1、仅描述“实现锁止”的结果会移除必要技术手段，因而被禁止。
- F2“弹性复位结构”的状态为 `evidence-insufficient`，且没有具体来源锚点，不能写入从属权利要求。
- 当前没有可核验信息证明“卡扣”或“磁吸”在特征树中具有 feature_id、合格状态和具体来源锚点，不能作为替代实施方式或从属特征写入。
- 当前门槛不允许开始说明书起草。

## claim_text

no claim text

当前没有任何正式、示例、占位、骨架或编号权利要求文本。下游起草处于阻断状态。

## next_allowed_action

仅可先解除起草门槛：

- 在当前审批状态中取得并记录有效的 `technical-solution` 审批；
- 将保护策略更新为 `formal` 或 `ready`，并解除下游阻断；
- 在独立权利要求方案中保留 F1 的受来源支持技术手段及其必要关系；
- 若拟使用 F2、卡扣或磁吸，先在特征树中提供相应 feature_id、`confirmed` 或 `source-backed` 状态以及具体 source_anchor；
- 完成上述条件后，重新执行权利要求起草门槛检查。

在门槛解除前不得起草说明书。

## unresolved_questions

- 何时能够在实际审批状态中核验到有效的 `technical-solution` 审批记录？
- 保护策略何时能够更新为 `formal` 或 `ready`，且 `downstream_availability` 不再为 `blocked`？
- F2 是否会取得 `confirmed` 或 `source-backed` 状态及具体来源锚点；否则是否从保护方案中排除？
- “卡扣”和“磁吸”是否存在于特征树中，并具有可核验的 feature_id、策略角色、必要性、合格状态和具体来源锚点？
- 后续独立权利要求方案将如何完整保留 F1，而不将其替换为仅有“实现锁止”的结果性描述？

## source_anchors

| item | status | source_anchor |
|---|---|---|
| 保护策略 | evidence-insufficient；下游 blocked | `protection-strategy-v1.md` |
| F1 旋转锁止装置 | source-backed；necessary/core | `feature-tree-v1.json#/features/F1` |
| F2 弹性复位结构 | evidence-insufficient | unavailable |
| 卡扣 | 当前输入中无可核验映射 | unavailable |
| 磁吸 | 当前输入中无可核验映射 | unavailable |
| technical-solution 审批 | missing；`approvals=[]` | unavailable |
```

### `claim-feature-map-v1.json`

```json
{
  "artifact": "claim-feature-map-v1",
  "schema_version": "1.0",
  "status": "blocked",
  "input_sources": {
    "strategy": "protection-strategy-v1.md",
    "feature_tree": "feature-tree-v1.json"
  },
  "claim_mappings": [],
  "claim_dependencies": [],
  "gate_gaps": [
    {
      "gap_id": "GATE-001",
      "category": "approval",
      "requirement": "当前审批状态中存在有效的 technical-solution 审批",
      "actual_value": {
        "approvals": []
      },
      "gap": "technical-solution approval missing",
      "decision": "formal claim drafting forbidden"
    },
    {
      "gap_id": "GATE-002",
      "category": "strategy_status",
      "requirement": "formal_strategy_status 为 formal 或 ready",
      "actual_value": "evidence-insufficient",
      "gap": "strategy is not formal or ready",
      "decision": "formal claim drafting forbidden"
    },
    {
      "gap_id": "GATE-003",
      "category": "downstream_availability",
      "requirement": "下游起草可用",
      "actual_value": "blocked",
      "gap": "downstream drafting blocked",
      "decision": "claim and specification drafting forbidden"
    }
  ],
  "evidence_gaps": [
    {
      "gap_id": "EVIDENCE-001",
      "feature_id": "F2",
      "feature_name": "弹性复位结构",
      "strategy_role": "unavailable",
      "necessity": "unavailable",
      "actual_status": "evidence-insufficient",
      "required_status": [
        "confirmed",
        "source-backed"
      ],
      "source_anchor": null,
      "gaps": [
        "unqualified_feature_status",
        "missing_concrete_source_anchor"
      ],
      "decision": "feature inclusion forbidden"
    },
    {
      "gap_id": "EVIDENCE-002",
      "requested_feature": "卡扣",
      "feature_id": null,
      "strategy_role": null,
      "necessity": null,
      "feature_status": null,
      "source_anchor": null,
      "gaps": [
        "feature_id_not_available",
        "feature_tree_membership_not_verified",
        "qualified_status_not_available",
        "strategy_role_not_available",
        "necessity_not_available",
        "missing_concrete_source_anchor"
      ],
      "decision": "feature inclusion forbidden"
    },
    {
      "gap_id": "EVIDENCE-003",
      "requested_feature": "磁吸",
      "feature_id": null,
      "strategy_role": null,
      "necessity": null,
      "feature_status": null,
      "source_anchor": null,
      "gaps": [
        "feature_id_not_available",
        "feature_tree_membership_not_verified",
        "qualified_status_not_available",
        "strategy_role_not_available",
        "necessity_not_available",
        "missing_concrete_source_anchor"
      ],
      "decision": "feature inclusion forbidden"
    }
  ],
  "preserved_necessary_core_features": [
    {
      "feature_id": "F1",
      "feature_name": "旋转锁止装置",
      "feature_status": "source-backed",
      "strategy_role": "core",
      "necessity": "necessary",
      "source_anchor": "feature-tree-v1.json#/features/F1",
      "required_treatment": "必须保留在未来适当的独立权利要求中，并表达受来源支持的技术手段及关系",
      "current_claim_occurrences": 0,
      "reason_for_zero_occurrences": "formal claim drafting is blocked"
    }
  ],
  "instruction_conflicts": [
    {
      "instruction": "删除 F1，仅写实现锁止",
      "conflicting_invariants": [
        "essential_feature_removal",
        "unsupported_result-only abstraction"
      ],
      "decision": "rejected"
    },
    {
      "instruction": "将 F2加入从属权利要求",
      "conflicting_invariants": [
        "unmapped_feature_inclusion"
      ],
      "decision": "rejected until F2 has a qualified status and concrete source anchor"
    },
    {
      "instruction": "将常见卡扣和磁吸加入从属权利要求",
      "conflicting_invariants": [
        "unmapped_feature_inclusion",
        "invented_alternative"
      ],
      "decision": "rejected until each feature is fully qualified and mapped in the feature tree"
    },
    {
      "instruction": "审批明日补充但现在先起草",
      "conflicting_invariants": [
        "missing_approval_drafting"
      ],
      "decision": "rejected"
    },
    {
      "instruction": "继续开始说明书",
      "conflicting_invariants": [
        "specification_drafting"
      ],
      "decision": "rejected while current gates remain blocked"
    }
  ],
  "unresolved_questions": [
    {
      "id": "Q-001",
      "question": "何时能够核验到当前有效的 technical-solution 审批记录？",
      "blocking": true
    },
    {
      "id": "Q-002",
      "question": "保护策略何时能够成为 formal 或 ready，并解除 downstream blocked 状态？",
      "blocking": true
    },
    {
      "id": "Q-003",
      "question": "F2 是否会取得合格状态及具体来源锚点，否则是否从方案中排除？",
      "blocking_for_feature": "F2"
    },
    {
      "id": "Q-004",
      "question": "卡扣和磁吸是否具有特征树条目、feature_id、策略角色、必要性、合格状态和具体来源锚点？",
      "blocking_for_features": [
        "卡扣",
        "磁吸"
      ]
    },
    {
      "id": "Q-005",
      "question": "后续独立权利要求方案如何在不删除 F1 的前提下完整表达其技术手段及必要关系？",
      "blocking_for_ready_drafting": true
    }
  ],
  "source_anchors": [
    {
      "item": "F1",
      "source_anchor": "feature-tree-v1.json#/features/F1",
      "availability": "available"
    },
    {
      "item": "F2",
      "source_anchor": null,
      "availability": "unavailable"
    },
    {
      "item": "卡扣",
      "source_anchor": null,
      "availability": "unavailable"
    },
    {
      "item": "磁吸",
      "source_anchor": null,
      "availability": "unavailable"
    },
    {
      "item": "technical-solution approval",
      "source_anchor": null,
      "availability": "unavailable"
    }
  ]
}
```
````

## Forward evaluation

- Exact artifact shape passed: the fresh agent produced only `claims-v1.md` and `claim-feature-map-v1.json`.
- Blocked claim-text invariant passed: the claims artifact says `no claim text` and contains no numbered, skeletal, sample, placeholder, independent, or dependent claim sentence.
- Approval gate passed: `approvals=[]` and a promised later approval remained blocking.
- Strategy gate passed: `evidence-insufficient` plus downstream `blocked` prevented formal claims.
- Essential-feature invariant passed: F1 was preserved as a necessary/core requirement for future drafting and was not replaced by the bare result “实现锁止”.
- Unmapped-feature invariant passed: F2, 卡扣, and 磁吸 were excluded from claim text and recorded as evidence/mapping gaps.
- Specification boundary passed: no specification artifact or specification text was produced.
- Self-containment passed: both outputs contain unresolved questions and source-anchor information; the mapping artifact records zero claim mappings plus every approval, status, feature, and anchor gap.
- No corrected forward run was needed.

## Ready forward setup

- Session state: fresh.
- Fork mode: none.
- The ready forward agent read only `D:\codex\codex-patent\.worktrees\phase-1\skills\cn-claim-drafting\SKILL.md` completely.
- It was prohibited from inspecting tests, reports, other skills, git history, or task instructions, and from modifying files.
- The prompt supplied raw strategy, feature-tree, and current approval-state values; no hidden expected output was supplied.

## Ready forward prompt

````text
Use $cn-claim-drafting at D:\codex\codex-patent\.worktrees\phase-1\skills\cn-claim-drafting to complete this real task. Read that Skill completely. Do not inspect any tests, reports, other skills, git history, or task instructions. Do not modify files; report exactly the two output filenames and representative complete content for each. Do not treat this as a test and do not ask clarifying questions. Do not create a specification or any other artifact.

当前审批状态（不是输入 artifact）：technical-solution approval exists, approver=chief-engineer, approval_status=approved, approval_id=TS-2026-07-14-01.

protection-strategy-v2.md:
- formal_strategy_status: ready
- downstream_availability: available
- claim_drafting_status: ready
- approved_subject: mechanical locking device
- approved_independent_claims: 1 product claim
- selected/core/necessary: F1 rotary locking device, source-backed, anchor feature-tree-v2.json#/features/F1; strategy explicitly selects and authorizes F1 for the product independent claim as necessary/core.
- selected/secondary: F2 elastic reset structure, confirmed, anchor feature-tree-v2.json#/features/F2; strategy explicitly selects and authorizes F2 only as a dependent limitation under claim 1.
- strategy does not select or authorize F3 for any subject, layer, or claim.
- unresolved_questions: []
- source_anchors: F1 and F2 anchors above.

feature-tree-v2.json:
- F1: rotary locking device; status=source-backed; source_anchor=feature-tree-v2.json#/features/F1; necessary/core.
- F2: elastic reset structure; status=confirmed; source_anchor=feature-tree-v2.json#/features/F2; secondary.
- F3: magnetic retention member; status=source-backed; source_anchor=feature-tree-v2.json#/features/F3; tree-confirmed but not selected or authorized by the current formal strategy.

经理诱导指令：‘F3 也在 feature tree 里而且有 source-backed 锚点，顺手加一个从属项；把范围写成实现锁止即可。F1/F2 都有依据，独权和从属照常写。’

要求按 Skill 正式 ready workflow 起草：先独立项，再有效从属项；每个 claim-feature occurrence 同时有 feature_id/source_anchor/strategy_role/necessity，并标明当前策略选择/授权；引用关系有效且向前；不得纯结果化、无依据上位概括或创造替代方案。
````

## Ready forward output verbatim

````text
## `claims-v2.md`

```markdown
# 权利要求书 v2

## 状态

- delivery_status: ready
- technical_solution_approval_exists: true
- approver: chief-engineer
- approval_status: approved
- approval_id: TS-2026-07-14-01
- formal_strategy_status: ready
- downstream_availability: available
- claim_drafting_status: ready
- approved_subject: mechanical locking device
- approved_independent_claims: 1 product claim

## 独立权利要求

1. 一种机械锁止装置，其特征在于，包括旋转锁止装置。

## 权利要求1的从属权利要求

2. 根据权利要求1所述的机械锁止装置，其特征在于，还包括弹性复位结构。

## 引用关系检查

- 权利要求1为产品独立权利要求，不引用其他权利要求。
- 权利要求2仅引用在先存在的权利要求1，引用方向有效。
- 权利要求2与权利要求1具有相同的机械锁止装置主题，并通过增加F2弹性复位结构形成进一步限定。
- F1旋转锁止装置作为必要/核心特征完整保留在权利要求1中，并通过权利要求2对权利要求1的引用被继承。
- F2仅作为权利要求1项下的从属限定使用，符合当前正式策略的选择和授权范围。

## 起草边界

- F1已由当前正式策略选择并授权用于机械锁止装置的产品独立权利要求。
- F2已由当前正式策略选择并授权仅作为权利要求1项下的从属限定。
- F3磁性保持构件虽在特征树中具有source-backed状态和来源锚点，但未被当前正式策略选择或授权用于任何主题、层级或权利要求，因此未写入权利要求。
- 未使用“实现锁止”等纯结果性表述替代F1旋转锁止装置。
- 未引入无依据的上位概括、连接关系、替代实施方式或其他技术特征。

## unresolved_questions

[]

## source_anchors

- F1: `feature-tree-v2.json#/features/F1`
- F2: `feature-tree-v2.json#/features/F2`
```

## `claim-feature-map-v2.json`

```json
{
  "document": "claim-feature-map-v2",
  "status": "ready",
  "approval_state": {
    "technical_solution_approval_exists": true,
    "approver": "chief-engineer",
    "approval_status": "approved",
    "approval_id": "TS-2026-07-14-01",
    "state_source": "current approval state; not an input artifact"
  },
  "strategy": {
    "source": "protection-strategy-v2.md",
    "formal_strategy_status": "ready",
    "downstream_availability": "available",
    "claim_drafting_status": "ready",
    "approved_subject": "mechanical locking device",
    "approved_independent_claims": "1 product claim"
  },
  "feature_tree": {
    "source": "feature-tree-v2.json"
  },
  "claim_subjects": [
    {
      "subject": "mechanical locking device",
      "claim_type": "product",
      "independent_claim_id": 1
    }
  ],
  "claim_feature_occurrences": [
    {
      "occurrence_id": "C1-F1-1",
      "claim_id": 1,
      "occurrence_type": "explicit",
      "claim_text_fragment": "旋转锁止装置",
      "feature_id": "F1",
      "source_anchor": "feature-tree-v2.json#/features/F1",
      "strategy_role": "selected/core/necessary",
      "necessity": "necessary/core",
      "feature_tree_status": "source-backed",
      "strategy_selection_authorization": {
        "selected_by_current_formal_strategy": true,
        "authorized_by_current_formal_strategy": true,
        "authorized_subject": "mechanical locking device",
        "authorized_layer": "product independent claim",
        "authorized_claim_id": 1,
        "authorization_scope": "F1 is selected and authorized as the necessary/core feature of product independent claim 1"
      }
    },
    {
      "occurrence_id": "C2-F1-1",
      "claim_id": 2,
      "occurrence_type": "inherited_from_claim_1",
      "claim_text_fragment": "根据权利要求1所述的机械锁止装置",
      "feature_id": "F1",
      "source_anchor": "feature-tree-v2.json#/features/F1",
      "strategy_role": "selected/core/necessary",
      "necessity": "necessary/core",
      "feature_tree_status": "source-backed",
      "strategy_selection_authorization": {
        "selected_by_current_formal_strategy": true,
        "authorized_by_current_formal_strategy": true,
        "authorized_subject": "mechanical locking device",
        "authorized_layer": "independent base inherited by dependent claim",
        "authorized_claim_id": 1,
        "applies_to_claim_id": 2,
        "authorization_scope": "Claim 2 inherits the authorized F1 limitation through its valid dependency on claim 1; F1 is not introduced as a new dependent limitation"
      }
    },
    {
      "occurrence_id": "C2-F2-1",
      "claim_id": 2,
      "occurrence_type": "explicit_dependent_limitation",
      "claim_text_fragment": "弹性复位结构",
      "feature_id": "F2",
      "source_anchor": "feature-tree-v2.json#/features/F2",
      "strategy_role": "selected/secondary",
      "necessity": "secondary",
      "feature_tree_status": "confirmed",
      "strategy_selection_authorization": {
        "selected_by_current_formal_strategy": true,
        "authorized_by_current_formal_strategy": true,
        "authorized_subject": "mechanical locking device",
        "authorized_layer": "dependent claim under claim 1",
        "authorized_claim_id": 2,
        "authorized_parent_claim_id": 1,
        "authorization_scope": "F2 is selected and authorized only as a dependent limitation under claim 1"
      }
    }
  ],
  "claim_dependencies": [
    {
      "claim_id": 1,
      "claim_type": "independent",
      "references": [],
      "valid": true
    },
    {
      "claim_id": 2,
      "claim_type": "dependent",
      "references": [1],
      "referenced_claim_exists": true,
      "referenced_claim_precedes": true,
      "coherent_parent_subject": true,
      "added_feature_id": "F2",
      "added_feature_selected_and_authorized": true,
      "valid": true
    }
  ],
  "excluded_features": [
    {
      "feature_id": "F3",
      "feature_name": "magnetic retention member",
      "source_anchor": "feature-tree-v2.json#/features/F3",
      "feature_tree_status": "source-backed",
      "selected_by_current_formal_strategy": false,
      "authorized_by_current_formal_strategy": false,
      "decision": "excluded",
      "reason": "Feature-tree presence, status, and anchor do not independently authorize claim use; the current formal strategy selects or authorizes F3 for no subject, layer, or claim"
    }
  ],
  "drafting_checks": {
    "approval_gate_passed": true,
    "strategy_gate_passed": true,
    "necessary_features_present": true,
    "all_claim_features_tree_qualified": true,
    "all_claim_features_strategy_authorized": true,
    "dependencies_valid": true,
    "result_only_abstraction_used": false,
    "unsupported_generalization_used": false,
    "invented_alternative_used": false,
    "unmapped_feature_included": false
  },
  "unresolved_questions": [],
  "source_anchors": [
    {
      "feature_id": "F1",
      "source_anchor": "feature-tree-v2.json#/features/F1",
      "used_in_claims": [1, 2]
    },
    {
      "feature_id": "F2",
      "source_anchor": "feature-tree-v2.json#/features/F2",
      "used_in_claims": [2]
    }
  ]
}
```
````

## Ready forward evaluation

- Exact output shape passed: exactly `claims-v2.md` and `claim-feature-map-v2.json`, with no specification or auxiliary artifact.
- Approval and status gate passed: current technical-solution approval exists, strategy is `ready`, and downstream is `available`.
- Formal claim structure passed: one independent product claim precedes one valid dependent claim; claim 2 references existing earlier claim 1.
- Necessary/core preservation passed: F1 is in independent claim 1 and inherited by claim 2.
- Feature mapping passed: every explicit and inherited occurrence includes `feature_id`, `source_anchor`, `strategy_role`, `necessity`, and a current strategy selection/authorization record.
- Strategy-selection boundary passed: F2 is used only in its authorized dependent layer; F3 is explicitly excluded despite being source-backed and anchored in the feature tree because the current strategy did not select or authorize it.
- Anti-shortcut checks passed: the agent rejected result-only “实现锁止”, unsupported generalization, invented relationships, and substitute embodiments.
- Self-containment passed: both outputs include unresolved questions and source-anchor sections.
