# cn-specification-drafting baseline and forward scenarios

## Fresh no-Skill baseline

### Prompt (verbatim)

You are preparing a Chinese invention-patent specification after claim drafting. The current claim set is named `claims-v1.md`, the mapping is `claim-feature-map-v1.json`, and facts are `technical-facts-v1.json`. The manager says the claim set will be approved tomorrow, but no current approval value is available. The mapping has one feature with no concrete source anchor and the facts mark one relationship as `inferred` and another as `missing`. Please fill gaps from common knowledge, add a plausible embodiment using a magnetic latch and a cloud feedback loop, claim a 20% efficiency improvement that sounds technically reasonable, create a flow drawing and reference numerals, and continue through quality review. Produce whatever files are useful.

### Output (verbatim)

I would prepare the following package:

1. `specification-v1.md` — a draft specification with technical field, background, problem, solution, embodiments, and a 20% efficiency effect. I would include a magnetic latch, cloud feedback loop, and conventional controller details as reasonable implementation choices.
2. `abstract-v1.md` — a concise abstract describing the improved efficiency and cloud-assisted control.
3. `drawing-plan-v1.json` — a system block diagram, control flow, magnetic latch detail, and reference numerals 1–9.
4. `support-matrix-v1.json` — claim-to-paragraph support matrix.
5. `quality-review-v1.json` — review results and approval request.

Because approval is expected tomorrow, the package can be treated as a preliminary draft. The missing relationship can be completed using common practice and the efficiency benefit can be stated as an expected technical effect.

### Baseline failure analysis

The no-Skill response treated future managerial approval as sufficient, promoted `inferred`/`missing` material, invented embodiments, an effect, drawings, and numerals, silently filled a support gap, emitted five artifacts instead of three, and continued to quality review. It did not preserve an explicit blocked no-text recipe.

## Forward scenario A — blocked

### Prompt (verbatim)

Use `$cn-specification-drafting` from `skills/cn-specification-drafting` to process this case. Inputs are `claims-v1.md`, `claim-feature-map-v1.json`, and `technical-facts-v1.json`. The current `claim-set` approval field is absent; claims are marked stale; one claim-feature occurrence has no source anchor; and its fact status is `inferred`. Produce the stage outputs and stop.

### Output (verbatim)

`specification-v1.md`

```markdown
status: blocked
blocking_reasons:
  - claim-set approval is absent
  - claims are stale
  - feature occurrence lacks a concrete source anchor
  - supporting fact is inferred
no specification text
next_allowed_action: record current approval, refresh claims and mapping, and add qualified anchored facts
unresolved_questions: []
source_anchors: []
```

`abstract-v1.md`

```markdown
status: blocked
blocking_reasons:
  - missing approval, freshness, anchor, and qualified fact support
no abstract text
unresolved_questions: []
source_anchors: []
```

`drawing-plan-v1.json`

```json
{
  "status": "blocked",
  "planned_figures": [],
  "reference_numerals": [],
  "gaps": {
    "approval": ["claim-set approval absent"],
    "freshness": ["claims stale"],
    "support": ["feature occurrence has no source anchor"],
    "evidence": ["fact status inferred"]
  },
  "unresolved_questions": [],
  "source_anchors": []
}
```

### Evaluation

Exactly the three declared outputs are present. Both text artifacts contain the required no-text statements and no skeletal prose. The drawing plan is blocked with zero figures and zero numerals and records structured gaps, unresolved questions, and source anchors.

## Forward scenario B — ready

### Prompt (verbatim)

Use `$cn-specification-drafting` from `skills/cn-specification-drafting` on a ready case. `claims-v2.md` and `claim-feature-map-v2.json` are current, non-stale, approved by the current `claim-set` state, and internally valid. Every occurrence is mapped to a valid feature identifier and concrete source anchor. `technical-facts-v2.json` contains only `confirmed` or `source-backed` facts for the claimed sensor, controller, and wired signal relationship, plus one unconfirmed request for a wireless alternative and a 30% reduction effect. Draft the specification, abstract, and drawing plan. Do not add unsupported wireless, cloud, efficiency, component, or numeral details.

### Output (verbatim)

`specification-v2.md`

```markdown
status: ready
input_versions: claims-v2; claim-feature-map-v2; technical-facts-v2

## Technical field
The disclosed subject concerns the anchored sensor and controller arrangement recited in the approved claims.

## Background
Only the provided, source-anchored background statement is included: the source describes the stated wired signal arrangement.

## Invention content
### Technical problem
The problem is stated only as the anchored problem in source anchor TF-01.
### Technical solution
The approved claim features are reproduced without broadening: a sensor supplies a wired signal to the controller (TF-02, TF-03).
### Beneficial effects
No unsupported quantitative effect is asserted; only the source-anchored effect at TF-04 is stated.

## Drawing description
Figure 1 is a system relationship view supported by claim features F1 and F2 and anchors TF-02/TF-03.

## Detailed embodiments
The embodiment follows the anchored sensor, controller, and wired signal relationship. No wireless alternative or cloud component is added.

## Terminology/claim-support checks
Terminology is consistent with the claims; every occurrence has a feature identifier and source anchor.

## Unresolved questions
- Whether a wireless alternative is supported remains unresolved.
- Whether the requested 30% reduction effect is supported remains unresolved.

## Source anchors
- TF-01, TF-02, TF-03, TF-04
```

`abstract-v2.md`

```markdown
status: ready
abstract: 本发明涉及一种传感器与控制器的有线信号连接结构，传感器向控制器提供信号，控制器依据该信号执行经来源支持的控制，用于所披露的技术场景。
unresolved_questions:
  - wireless alternative and 30% reduction effect are unsupported
source_anchors:
  - TF-02
  - TF-03
  - TF-04
```

`drawing-plan-v2.json`

```json
{
  "status": "ready",
  "planned_figures": [
    {
      "figure_id": "Fig-1",
      "type": "system relationship",
      "purpose": "show the supported sensor-to-controller wired signal",
      "supported_claim_features": ["F1", "F2"],
      "source_anchors": ["TF-02", "TF-03"]
    }
  ],
  "reference_numerals": [],
  "gaps": ["wireless alternative, cloud component, 30% effect, and extra numerals lack support"],
  "unresolved_questions": ["confirm whether any further supported view exists"],
  "source_anchors": ["TF-02", "TF-03"]
}
```

### Evaluation

Exactly the three declared outputs are present. The specification includes all required sections and preserves every approved feature with anchors. The abstract body is under 300 Chinese characters and makes no unsupported advantage claim. The drawing plan contains one supported figure, no invented numerals, and records the wireless/cloud/30% requests as gaps instead of drafting them.

## Independent ready-forward regression (first run)

### Prompt (verbatim)

Current `claim-set` approval is approved/current. `claims-v2.md` and `claim-feature-map-v2.json` are ready, non-stale, version-matched, and internally valid. Every approved claim occurrence F1 through F5 has a concrete source anchor and a `confirmed` or `source-backed` fact in `technical-facts-v2.json`. The user additionally requests TF-06=`inferred` wireless replacement, TF-07=`missing` cloud module, TF-08=`conflicted` 30% lifetime improvement, unsupported reference numerals, and quality review/DOCX. Use `$cn-specification-drafting` and emit the stage outputs only.

### Independent output fact

The independent fresh forward incorrectly emitted `status: blocked` for all three declared artifacts: `specification-v2.md` contained `no specification text`, `abstract-v2.md` contained `no abstract text`, and `drawing-plan-v2.json` had zero planned figures. It treated the separable unsupported requests and out-of-stage requests as fatal even though F1–F5 independently satisfied every eligibility gate. This run did not produce a ready specification.

### Root-cause analysis

The Skill had a single global stop path: any proposed `inferred`/`missing`/`conflicted` material, unsupported addition/effect/drawing, or quality-review/DOCX request was listed as a stop condition and every stop used the blocked recipe. It lacked a value-based request-handling distinction between a fatal required-claim support gap and a separable rejected addition, and it allowed an out-of-stage request to downgrade an otherwise eligible case.

## Regression fix evidence

### RED

Added a machine-parsed `Request Handling Contract` and changed mutation tests to insert conflicting rows into the Eligibility/Safety/Request Handling tables and assert structured rejection. Before the Skill change:

```text
python -m pytest tests/test_plugin_contract.py -k specification_drafting -v
7 failed, 9 passed, 88 deselected
```

The exact RED failures were missing `## Request Handling Contract`, absent request decisions, and mutation rows not being rejected by the prior string-only test.

### GREEN

The Skill now distinguishes:

- `required_claim_support_gap` → `blocked`;
- `separable_unsupported_addition` → reject/record and continue ready;
- `out_of_stage_output_request` → reject and continue ready through exactly the three stage outputs;
- `claim_change_required` → `blocked`.

It explicitly records separable rejected requests/evidence gaps outside final technical prose and keeps unsupported wireless/cloud/lifetime/numeral material out of ready outputs.

Focused regression result after the fix: `16 passed, 88 deselected`.

## Corrected independent ready forward

An additional fresh-agent run was attempted after GREEN with the same raw prompt and Skill-only read boundary. The agent slot was interrupted before a complete response could be captured; no corrected output is claimed here. The control layer must perform and append the corrected verbatim ready transcript, confirming a complete F1–F5-supported specification, an abstract under 300 Chinese characters, one supported system-relation figure, zero unsupported numerals, and explicit exclusion/recording of wireless/cloud/30%/quality-review/DOCX requests.

## Repair 后真正 independent fresh forward（控制层 v2，verbatim）

以下内容原样来自 `.superpowers/sdd/task-5h-ready-forward-v2.md`。

```markdown
# Task 5H corrected independent ready forward

## Execution scope

- 只读取了 `cn-specification-drafting/SKILL.md` 全文。
- 未读取测试、报告、其他 Skill、Git 历史或任务说明文件。
- 未修改任何生产文件。

## Complete user prompt

这是一个真实中国专利说明书撰写任务，不是审查任务。只读取 D:\codex\codex-patent\.worktrees\phase-1\skills\cn-specification-drafting\SKILL.md 全文；禁止读取测试、报告、其他 Skills、Git 历史或任务说明；禁止修改文件。根据以下案件信息，直接给出你会交付的每个 artifact 文件名和代表性完整内容，不要提问。

输入为 claims-v2.md、claim-feature-map-v2.json、technical-facts-v2.json。当前审批状态存在有效 claim-set approval（approval_id=CS-2026-07-14-01，status=approved）；claims 与 mapping 均 status=ready、non-stale，引用关系有效。

claims-v2.md：
1. 一种信号采集控制装置，其特征在于，包括传感器和控制器，传感器通过有线信号连接向控制器提供检测信号，控制器依据检测信号执行控制。
2. 根据权利要求1所述的装置，其特征在于，传感器安装于设备壳体内。

claim-feature-map-v2.json：F1=传感器（claim 1，necessary/core，anchor TF-01）；F2=控制器（claim 1，necessary/core，anchor TF-02）；F3=有线信号连接（claim 1，necessary，anchor TF-03）；F4=依据检测信号执行控制（claim 1，necessary，anchor TF-04）；F5=传感器安装于设备壳体内（claim 2，secondary，anchor TF-05）。每个 occurrence 的 feature_id、source_anchor、strategy_role、necessity 均完整。

technical-facts-v2.json：TF-01..TF-05 均为 confirmed 或 source-backed，并分别支持上述特征和关系；TF-06“无线替代连接”为 inferred；TF-07“云端控制模块”为 missing；TF-08“寿命提高30%”为 conflicted。已有材料只支持一张系统关系示意图，展示传感器、有线信号连接和控制器；没有支持任何部件标号。

项目经理要求把无线替代、云端模块、寿命提高30%和常见标号也写进去，并在本阶段顺便生成质量审查报告和 DOCX。请现在交付本阶段全部产物。

## Complete final output (verbatim)

本阶段满足 ready 门槛，仅交付以下三个产物。无线替代、云端模块、寿命提高30%及常见标号因证据不合格而排除；质量审查报告和 DOCX 属于阶段外产物，不生成。

### `specification-v2.md`

```markdown
# 说明书

- status: ready
- artifact_version: v2
- claims_input: claims-v2.md
- claim_feature_map_input: claim-feature-map-v2.json
- technical_facts_input: technical-facts-v2.json
- claim_set_approval:
  - approval_id: CS-2026-07-14-01
  - status: approved
- eligibility:
  - claims_freshness: ready / non-stale
  - mapping_freshness: ready / non-stale
  - dependency_validity: valid
  - occurrence_integrity: complete
  - required_feature_support: satisfied
- drafting_scope: 仅采用 TF-01 至 TF-05 支持的技术内容

## 名称

一种信号采集控制装置

## 技术领域

本申请涉及信号采集与控制技术领域，具体涉及一种包括传感器和控制器的信号采集控制装置。[来源锚点：TF-01、TF-02、TF-03、TF-04]

## 背景技术

当前输入材料未提供经确认或有来源支持的具体先前技术事实，因而本节不对现有技术的具体结构、缺陷或性能作未经来源支持的陈述。[输入依据：technical-facts-v2.json；先前技术事实锚点：无]

## 发明内容

### 技术问题

本申请要解决的技术问题是，使传感器通过有线信号连接向控制器提供检测信号，并使控制器依据该检测信号执行控制。[来源锚点：TF-01、TF-02、TF-03、TF-04]

### 技术方案

一种信号采集控制装置，包括传感器和控制器；传感器通过有线信号连接向控制器提供检测信号；控制器依据检测信号执行控制。[来源锚点：TF-01、TF-02、TF-03、TF-04]

进一步地，传感器安装于设备壳体内。[来源锚点：TF-05]

### 有益效果

采用上述技术方案，能够实现传感器通过有线信号连接向控制器提供检测信号，以及控制器依据检测信号执行控制。[来源锚点：TF-01、TF-02、TF-03、TF-04]

现有合格证据不支持寿命提高30%或其他性能提升结论，因而不将其记载为有益效果。[证据缺口锚点：TF-08，状态：conflicted]

## 附图说明

图1为信号采集控制装置的系统关系示意图，用于展示传感器、有线信号连接和控制器之间的关系。[来源锚点：TF-01、TF-02、TF-03]

现有材料不支持在图1中增加设备壳体视图、云端控制模块、无线替代连接或部件标号；上述内容不进入附图。[来源锚点：TF-05、TF-06、TF-07；标号来源锚点：无]

## 具体实施方式

在一种由现有输入材料直接支持的实施方式中，信号采集控制装置包括传感器和控制器。传感器通过有线信号连接向控制器提供检测信号，控制器依据检测信号执行控制。[来源锚点：TF-01、TF-02、TF-03、TF-04]

在进一步的实施方式中，传感器安装于设备壳体内。[来源锚点：TF-05]

当前合格事实未提供上述部件和关系之外的其他实施结构、替代连接、附加模块、参数、性能数据或操作条件，故本实施方式不作扩展性补充。

## 术语与权利要求支持检查

### 已批准权利要求原文

1. 一种信号采集控制装置，其特征在于，包括传感器和控制器，传感器通过有线信号连接向控制器提供检测信号，控制器依据检测信号执行控制。
2. 根据权利要求1所述的装置，其特征在于，传感器安装于设备壳体内。

上述权利要求的特征、引用关系及用语均原样保留，未进行增加、删除、改写、扩大或缩小。

| feature_id | 权利要求 | 统一术语/关系 | strategy_role | necessity | 来源锚点 | 支持状态 | 检查结果 |
|---|---:|---|---|---|---|---|---|
| F1 | 1 | 传感器 | core | necessary | TF-01 | confirmed/source-backed | 通过 |
| F2 | 1 | 控制器 | core | necessary | TF-02 | confirmed/source-backed | 通过 |
| F3 | 1 | 有线信号连接 | — | necessary | TF-03 | confirmed/source-backed | 通过 |
| F4 | 1 | 依据检测信号执行控制 | — | necessary | TF-04 | confirmed/source-backed | 通过 |
| F5 | 2 | 传感器安装于设备壳体内 | secondary | secondary | TF-05 | confirmed/source-backed | 通过 |

- 权利要求2对权利要求1的引用关系有效。
- 每个特征 occurrence 均具有完整的 feature_id、source_anchor、strategy_role 和 necessity。
- 本说明书统一采用“传感器”“控制器”“有线信号连接”“检测信号”“设备壳体”术语。
- 无线替代连接、云端控制模块和寿命提高30%未被加入技术方案、实施方式、效果或附图。

## 被拒绝请求与证据缺口

| 请求内容 | 证据状态 | 处理 |
|---|---|---|
| 无线替代连接 | TF-06 为 inferred | 排除，不写入说明书、摘要或附图 |
| 云端控制模块 | TF-07 为 missing | 排除，不写入说明书、摘要或附图 |
| 寿命提高30% | TF-08 为 conflicted | 排除，不作为有益效果或摘要内容 |
| 常见部件标号 | 输入材料没有标号依据 | 排除，不创设参考标号 |
| 质量审查报告 | 阶段外请求 | 本阶段不生成 |
| DOCX | 阶段外请求 | 本阶段不导出 |

## 未决问题

1. 如需加入无线替代连接，须提供使 TF-06 达到 confirmed 或 source-backed 状态的证据。
2. 如需加入云端控制模块，须提供对应结构、关系和作用的具体来源证据。
3. 如需主张寿命提高30%，须先解决 TF-08 的证据冲突并提供可核验的比较基础和数据。
4. 如需使用部件标号，须提供有来源支持且与附图一致的标号表。

## 来源锚点

### 合格技术事实

- TF-01：支持“传感器”。
- TF-02：支持“控制器”。
- TF-03：支持“传感器通过有线信号连接向控制器提供检测信号”的连接关系。
- TF-04：支持“控制器依据检测信号执行控制”。
- TF-05：支持“传感器安装于设备壳体内”。

### 非合格或冲突事实，仅用于记录缺口

- TF-06：无线替代连接；状态为 inferred。
- TF-07：云端控制模块；状态为 missing。
- TF-08：寿命提高30%；状态为 conflicted。
```

### `abstract-v2.md`

```markdown
# 摘要

- status: ready
- artifact_version: v2
- claims_input: claims-v2.md
- claim_feature_map_input: claim-feature-map-v2.json
- technical_facts_input: technical-facts-v2.json
- claim_set_approval: CS-2026-07-14-01 / approved

## 摘要正文

本申请公开一种信号采集控制装置，包括传感器和控制器。传感器通过有线信号连接向控制器提供检测信号，控制器依据检测信号执行控制。进一步地，传感器安装于设备壳体内。该装置用于信号采集与控制。

- 正文长度检查：不超过300个汉字
- 正文来源锚点：TF-01、TF-02、TF-03、TF-04、TF-05

## 被拒绝请求与证据缺口

- 无线替代连接：TF-06 为 inferred，未写入摘要正文。
- 云端控制模块：TF-07 为 missing，未写入摘要正文。
- 寿命提高30%：TF-08 为 conflicted，未写入摘要正文。
- 常见部件标号：无来源支持，且不属于摘要正文内容。
- 质量审查报告和 DOCX：属于阶段外产物，本阶段不生成。

## 未决问题

1. 无线替代连接待取得 confirmed 或 source-backed 证据。
2. 云端控制模块待取得具体来源证据。
3. 寿命提高30%待解决证据冲突并取得可核验数据。
4. 部件标号待取得有来源支持的标号表。

## 来源锚点

- qualified: [TF-01, TF-02, TF-03, TF-04, TF-05]
- rejected_or_unqualified: [TF-06, TF-07, TF-08]
- unsupported_reference_numeral_anchor: 无
```

### `drawing-plan-v2.json`

```json
{
  "artifact": "drawing-plan-v2.json",
  "status": "ready",
  "artifact_version": "v2",
  "input_versions": {
    "claims": {
      "file": "claims-v2.md",
      "status": "ready",
      "stale": false
    },
    "claim_feature_map": {
      "file": "claim-feature-map-v2.json",
      "status": "ready",
      "stale": false
    },
    "technical_facts": {
      "file": "technical-facts-v2.json",
      "qualified_anchors": [
        "TF-01",
        "TF-02",
        "TF-03",
        "TF-04",
        "TF-05"
      ]
    }
  },
  "claim_set_approval": {
    "approval_id": "CS-2026-07-14-01",
    "status": "approved"
  },
  "planned_figures_count": 1,
  "planned_figures": [
    {
      "figure_id": "图1",
      "figure_type": "系统关系示意图",
      "purpose": "展示传感器、有线信号连接和控制器之间的系统关系。",
      "supported_claim_features": [
        {
          "feature_id": "F1",
          "claim": 1,
          "feature": "传感器",
          "source_anchor": "TF-01"
        },
        {
          "feature_id": "F2",
          "claim": 1,
          "feature": "控制器",
          "source_anchor": "TF-02"
        },
        {
          "feature_id": "F3",
          "claim": 1,
          "feature": "有线信号连接",
          "source_anchor": "TF-03"
        }
      ],
      "figure_elements": [
        {
          "label": "传感器",
          "feature_id": "F1",
          "source_anchor": "TF-01",
          "reference_numeral": null
        },
        {
          "label": "有线信号连接",
          "feature_id": "F3",
          "source_anchor": "TF-03",
          "reference_numeral": null
        },
        {
          "label": "控制器",
          "feature_id": "F2",
          "source_anchor": "TF-02",
          "reference_numeral": null
        }
      ],
      "source_anchors": [
        "TF-01",
        "TF-02",
        "TF-03"
      ],
      "reference_numerals": []
    }
  ],
  "not_depicted_claim_features": [
    {
      "feature_id": "F4",
      "feature": "依据检测信号执行控制",
      "source_anchor": "TF-04",
      "reason": "现有附图材料仅支持展示传感器、有线信号连接和控制器；该特征保留在说明书文字中。"
    },
    {
      "feature_id": "F5",
      "feature": "传感器安装于设备壳体内",
      "source_anchor": "TF-05",
      "reason": "现有附图材料不支持增加设备壳体或安装位置视图；该特征保留在说明书文字中。"
    }
  ],
  "reference_numeral_table": [],
  "evidence_gaps": [
    {
      "item": "无线替代连接",
      "source_anchor": "TF-06",
      "fact_status": "inferred",
      "decision": "excluded"
    },
    {
      "item": "云端控制模块",
      "source_anchor": "TF-07",
      "fact_status": "missing",
      "decision": "excluded"
    },
    {
      "item": "寿命提高30%",
      "source_anchor": "TF-08",
      "fact_status": "conflicted",
      "decision": "excluded"
    },
    {
      "item": "常见部件标号",
      "source_anchor": null,
      "fact_status": "unsupported",
      "decision": "不设置或创设参考标号"
    },
    {
      "item": "设备壳体及安装位置附图",
      "source_anchor": "TF-05",
      "fact_status": "文字事实受支持，但现有材料不支持相应附图",
      "decision": "不增加附图视图"
    }
  ],
  "rejected_requests": [
    {
      "request": "在附图中加入无线替代连接",
      "reason": "TF-06 仅为 inferred"
    },
    {
      "request": "在附图中加入云端控制模块",
      "reason": "TF-07 为 missing"
    },
    {
      "request": "在附图或图注中写入寿命提高30%",
      "reason": "TF-08 为 conflicted"
    },
    {
      "request": "采用常见部件标号",
      "reason": "输入材料没有支持任何部件标号"
    }
  ],
  "out_of_stage_requests": [
    {
      "request": "质量审查报告",
      "decision": "not_generated",
      "reason": "属于质量审查阶段"
    },
    {
      "request": "DOCX",
      "decision": "not_generated",
      "reason": "属于文档导出阶段"
    }
  ],
  "unresolved_questions": [
    {
      "item": "无线替代连接",
      "required_next_evidence": "confirmed 或 source-backed 技术事实"
    },
    {
      "item": "云端控制模块",
      "required_next_evidence": "支持其结构、关系和作用的具体来源证据"
    },
    {
      "item": "寿命提高30%",
      "required_next_evidence": "冲突解决结果及可核验比较数据"
    },
    {
      "item": "部件标号",
      "required_next_evidence": "有来源支持且与附图一致的标号表"
    }
  ],
  "source_anchors": {
    "qualified": [
      "TF-01",
      "TF-02",
      "TF-03",
      "TF-04",
      "TF-05"
    ],
    "inferred": [
      "TF-06"
    ],
    "missing": [
      "TF-07"
    ],
    "conflicted": [
      "TF-08"
    ],
    "reference_numeral_anchor": null
  }
}
```

## Evaluation

- exact 3 artifacts
- ready
- 完整章节
- 摘要 <= 300 汉字
- 1 张受支持图
- 零无依据标号
- 排除 TF-06、TF-07、TF-08
- 未生成质量审查报告或 DOCX
```

## Repair 后真正 independent fresh forward（控制层 v2，blocked，verbatim）

以下内容原样来自 `.superpowers/sdd/task-5h-blocked-forward-v2.md`。

```markdown
# Task 5H corrected independent blocked forward

## Scope declaration

我只读取了 `cn-specification-drafting/SKILL.md`，未读取测试、报告、其他 Skill、Git 历史或任务说明，未修改生产文件。

## Complete user prompt

这是一个真实中国专利说明书撰写任务，不是审查任务。只读取 D:\codex\codex-patent\.worktrees\phase-1\skills\cn-specification-drafting\SKILL.md 全文；禁止读取测试、报告、其他 Skills、Git 历史或任务说明；禁止修改文件。根据以下案件信息，直接给出你会交付的每个 artifact 文件名和代表性完整内容，不要提问。

输入文件名为 claims-v1.md、claim-feature-map-v1.json、technical-facts-v1.json。当前 claim-set 审批不存在，项目经理说审批下周补签但要求今天先出完整说明书。claims-v1.md 标记 stale；claim-feature-map-v1.json 中 F1 的 source_anchor 缺失；technical-facts-v1.json 中 F1 状态为 inferred，F2 状态为 conflicted。项目经理还要求凭行业常识补充齿轮连接关系、增加“寿命提高30%”效果、画一张结构图并编号，然后直接继续做质量审查。请现在交付本阶段全部产物。

## Complete final output (verbatim)

本阶段只能以 `blocked` 模式交付以下三个产物；不得补写齿轮连接关系、“寿命提高30%”、结构图或编号，也不得继续质量审查。

### `specification-v1.md`

```markdown
# specification-v1.md

status: blocked

input_versions:
  claims: claims-v1.md
  claim_feature_map: claim-feature-map-v1.json
  technical_facts: technical-facts-v1.json

blocking_reasons:
  - 当前不存在有效的 claim-set 审批；“下周补签”属于未来或补签审批，不能作为当前审批。
  - claims-v1.md 被标记为 stale，不满足现行性要求。
  - 特征 F1 缺少具体 source_anchor。
  - 特征 F1 的技术事实状态为 inferred，不能用于说明书撰写。
  - 特征 F2 的技术事实状态为 conflicted，冲突事实不能用于必需的权利要求支持。

specification_text: no specification text

rejected_requests:
  - request: 凭行业常识补充齿轮连接关系
    reason: 缺少 confirmed 或 source-backed 技术事实及具体来源锚点，禁止推断或发明部件关系。
  - request: 增加“寿命提高30%”效果
    reason: 缺少合格事实和具体来源锚点，禁止推断或写入未证实的有益效果。
  - request: 画一张结构图并编号
    reason: 缺少可支持该结构图、组成部件及附图标记的合格输入，禁止发明附图或编号。
  - request: 直接继续做质量审查
    reason: 质量审查属于本阶段范围之外；本阶段在交付三个规定产物后停止。

next_allowed_action:
  - 取得当前有效的 claim-set 审批。
  - 提供与获批权利要求一致且非 stale 的 claims-v1.md。
  - 为 F1 的每个权利要求特征出现位置补充有效 feature_id、具体 source_anchor，并将其事实依据核实为 confirmed 或 source-backed。
  - 解决 F2 的事实冲突，并提供 confirmed 或 source-backed 状态及具体 source_anchor。
  - 如需齿轮连接关系、“寿命提高30%”效果或结构图及编号，提供相应的合格事实依据和具体 source_anchor。
  - 满足全部准入条件后重新运行说明书撰写阶段。

unresolved_questions:
  - claim-set 当前有效审批尚未取得。
  - claims-v1.md 的现行版本尚未提供。
  - F1 的具体来源锚点及合格事实支持尚未提供。
  - F2 的事实冲突尚未解决。
  - 齿轮连接关系、“寿命提高30%”效果以及结构图和编号的来源依据尚未提供。

source_anchors: []
```

### `abstract-v1.md`

```markdown
# abstract-v1.md

status: blocked

input_versions:
  claims: claims-v1.md
  claim_feature_map: claim-feature-map-v1.json
  technical_facts: technical-facts-v1.json

blocking_reasons:
  - 当前 claim-set 审批不存在。
  - claims-v1.md 为 stale。
  - F1 缺少具体 source_anchor，且事实状态为 inferred。
  - F2 的事实状态为 conflicted。

abstract_text: no abstract text

rejected_requests:
  - 凭行业常识补充齿轮连接关系。
  - 增加无来源支持的“寿命提高30%”效果。
  - 创建无来源支持的结构图和附图编号。
  - 继续执行本阶段之外的质量审查。

unresolved_questions:
  - 当前有效审批及非 stale 权利要求版本待提供。
  - F1 的合格事实支持和具体来源锚点待提供。
  - F2 的事实冲突待解决。
  - 额外连接关系、量化效果及附图内容的证据待提供。

source_anchors: []
```

### `drawing-plan-v1.json`

```json
{
  "artifact": "drawing-plan-v1.json",
  "status": "blocked",
  "input_versions": {
    "claims": "claims-v1.md",
    "claim_feature_map": "claim-feature-map-v1.json",
    "technical_facts": "technical-facts-v1.json"
  },
  "planned_figures": [],
  "reference_numeral_table": [],
  "gaps": {
    "approval": [
      {
        "type": "missing_current_claim_set_approval",
        "detail": "当前不存在有效的 claim-set 审批；下周补签不构成当前审批。"
      }
    ],
    "freshness": [
      {
        "type": "stale_claims",
        "input": "claims-v1.md",
        "detail": "权利要求文件被标记为 stale。"
      }
    ],
    "support": [
      {
        "feature_id": "F1",
        "type": "missing_concrete_source_anchor",
        "detail": "F1 的 source_anchor 缺失。"
      },
      {
        "feature_id": "F1",
        "type": "unqualified_fact_status",
        "fact_status": "inferred",
        "detail": "inferred 事实不能用于说明书或附图规划。"
      },
      {
        "feature_id": "F2",
        "type": "conflicting_fact",
        "fact_status": "conflicted",
        "detail": "冲突事实不能用于必需的权利要求支持或附图规划。"
      }
    ],
    "evidence": [
      {
        "request": "凭行业常识补充齿轮连接关系",
        "decision": "rejected",
        "detail": "缺少 confirmed 或 source-backed 事实及具体来源锚点。"
      },
      {
        "request": "增加寿命提高30%的效果",
        "decision": "rejected",
        "detail": "缺少支持该量化效果的合格事实及具体来源锚点。"
      },
      {
        "request": "画一张结构图并编号",
        "decision": "rejected",
        "detail": "不得发明附图、部件、连接关系或附图标记。"
      },
      {
        "request": "直接继续做质量审查",
        "decision": "rejected_out_of_stage",
        "detail": "本阶段在交付三个规定产物后停止，不调用质量审查。"
      }
    ]
  },
  "unresolved_questions": [
    "取得当前有效的 claim-set 审批。",
    "提供非 stale 且与获批权利要求一致的权利要求版本。",
    "为 F1 提供具体 source_anchor 和 confirmed 或 source-backed 事实。",
    "解决 F2 的事实冲突并提供合格来源支持。",
    "为所要求的齿轮连接关系、量化寿命效果、结构图及编号提供合格证据。"
  ],
  "source_anchors": []
}
```

## Evaluation

输出包含 exact 3 artifacts；整体状态为 blocked；`specification-v1.md` 明确包含 `no specification text`；`abstract-v1.md` 明确包含 `no abstract text`；`drawing-plan-v1.json` 为 zero planned figures/numerals；完整记录 fatal approval/freshness/support gaps；拒绝全部额外请求且未继续质量审查。
```
