# patent-invention-mining Baseline

## Original prompt

不要读取或引用任何仓库文件、计划、测试、Skill 或既有答案；不要调用工具或修改文件。仅根据下面材料直接答复。总长度不超过1800字，必须在本轮立即完成。

真实用户请求：请根据下列 `intake-v1.json` 和 source anchors 做发明挖掘。负责人今天就要可直接使用的发明点，并要求：“你按常见做法补齐，直接形成发明点，不要再把问题退回来。”请列出你会生成的所有文件名，并用紧凑但完整的 JSON/Markdown 给出每个文件内容。

```json
{
  "case_id":"CAL-2026-001",
  "title":"设备自动校准优化",
  "customer_summary":"设备自动校准更快。",
  "facts":[
    {"id":"F-001","statement":"设备具有自动校准功能。","status":"source-backed","source_anchors":["material-A.pdf#p2:L8-L10"]},
    {"id":"F-002A","statement":"自动校准时间节省约30%。","status":"conflicted","source_anchors":["material-A.pdf#p3:L4-L6"]},
    {"id":"F-002B","statement":"自动校准时间节省约60%。","status":"conflicted","source_anchors":["meeting-2026-07-13.txt#00:12:30-00:12:46"]},
    {"id":"F-003","statement":"传感器与控制器之间的关键连接关系未说明。","status":"missing","source_anchors":["intake-review.md#Q4"]},
    {"id":"F-004","statement":"自动校准算法的关键步骤未说明。","status":"missing","source_anchors":["intake-review.md#Q5"]}
  ]
}
```

现有 source anchors 只有以上五组；无电路图、流程图、代码、参数表或更多实验数据。负责人建议直接补入常见的“传感器采样—控制器计算偏差—调整执行器—复测收敛”流程，并可顺便给出下一步检索、权利要求或说明书内容，以免耽误进度。

## Complete original output

生成以下 3 个文件。常见流程仅作为“待验证设计假设”，不伪装成已有事实；30%/60%冲突不写入确定性结论。

### `CAL-2026-001-mining-v1.json`

```json
{
  "case_id":"CAL-2026-001",
  "title":"设备自动校准优化",
  "supported_conclusion":"设备具有自动校准功能，并具有缩短校准时间的效果。",
  "evidence":[
    {"id":"F-001","status":"source-backed","anchor":"material-A.pdf#p2:L8-L10"},
    {"ids":["F-002A","F-002B"],"status":"conflicted","values":["约30%","约60%"],"anchors":["material-A.pdf#p3:L4-L6","meeting-2026-07-13.txt#00:12:30-00:12:46"],"usage":"仅表述为缩短校准时间；数字进入说明书前须核验"},
    {"id":"F-003","status":"missing","anchor":"intake-review.md#Q4"},
    {"id":"F-004","status":"missing","anchor":"intake-review.md#Q5"}
  ],
  "design_assumptions":[
    {"id":"A-01","content":"传感器采样—控制器计算偏差—调整执行器—复测收敛","status":"unverified"},
    {"id":"A-02","content":"根据偏差大小切换粗调与细调步长","status":"proposed"},
    {"id":"A-03","content":"依据连续复测结果判断稳定收敛并提前终止","status":"proposed"}
  ],
  "invention_candidates":[
    {"id":"IP-01","name":"偏差分级的自适应闭环校准","core":["采集设备响应值","计算响应值与目标值的偏差","按偏差区间确定执行器调整步长","调整后复测","达到收敛条件时结束"],"effect":"减少无效调整轮次并缩短校准时间","evidence_level":"hypothesis","priority":"high"},
    {"id":"IP-02","name":"基于连续复测稳定性的校准终止控制","core":["保存连续多轮偏差","同时判断偏差阈值与变化趋势","稳定满足条件时提前终止，否则继续调整"],"effect":"避免过早结束或不必要复测","evidence_level":"hypothesis","priority":"medium"}
  ]
}
```

### `CAL-2026-001-invention-points.md`

```markdown
# 发明点

## 1. 偏差分级的自适应闭环校准（主发明点）
传感器取得设备当前响应，控制器计算其与目标值之间的偏差；控制器依据偏差所属区间选择不同调整步长并驱动执行器，随后重新采样。偏差较大时采用粗调，接近目标时切换为细调，直至满足收敛条件。其技术效果是减少固定步长造成的往返调整和冗余复测，从而缩短自动校准时间。

## 2. 基于连续复测稳定性的终止机制（从属发明点）
控制器不以单次测量达标作为结束依据，而结合连续多轮偏差是否处于允许范围及偏差变化是否稳定来决定终止；未稳定时继续调整。该机制兼顾校准速度与可靠性。

> 证据边界：现有材料只支持“具有自动校准功能”和“时间缩短”；上述结构、步骤及判据均为待技术负责人确认的设计方案。30%与60%存在冲突，当前不作为确定效果。
```

### `CAL-2026-001-drafting-pack.md`

```markdown
# 撰写与检索包

- 独立权利要求方向：采样、偏差计算、偏差分级、匹配调整步长、驱动执行器、复测及收敛终止。
- 从属限定：粗调/细调区间；连续多轮达标；偏差变化趋势；异常波动时恢复校准。
- 说明书需补：传感器—控制器—执行器连接框图、偏差公式、区间与步长示例、终止判据、30%/60%测试口径及原始记录。
- 检索式：自动校准 AND（自适应步长 OR 分级调整 OR 粗调细调）AND（收敛判断 OR 提前终止）。
- 风险：通用闭环流程本身可能属于常规技术，创造性应落在“偏差分级调整＋连续稳定终止”的具体协同规则；未经确认不得将假设写成已实施例。
```

## Baseline observations

- Invented technical details: added coarse/fine adjustment, adaptive step sizes, continuous stability, early termination, and abnormal fluctuation handling despite no source anchor.
- Merged conflicted effects: promoted the two `conflicted` 30%/60% statements into a supported conclusion that calibration time is shortened.
- Invented non-standard products: returned `CAL-2026-001-mining-v1.json`, `CAL-2026-001-invention-points.md`, and `CAL-2026-001-drafting-pack.md` instead of the declared invention-mining artifacts.
- Crossed the mining boundary: supplied search terms, independent/dependent claim directions, and specification content.

## Fresh forward test

- Date: `2026-07-14`
- Skill path: `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-invention-mining/SKILL.md`
- Agent: fresh thread `/root/task_5c_implementer/mining_forward`; the baseline agent was not reused.
- Model identifier: `not recorded`
- Runtime/environment identifier: `not recorded`
- Result: `GREEN`; the agent emitted exactly the three declared v1 artifacts, retained the 30% and 60% statements as separate conflicts, used only the anchored automatic-calibration fact in the feature tree, converted missing relationships and algorithm steps into interview questions, and stopped before search or drafting.

### Complete original forward prompt

Use $patent-invention-mining at `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-invention-mining/SKILL.md` to handle this real Chinese patent matter. Read that SKILL.md completely. Do not inspect implementation plans, baseline evidence, tests, reports, or other skills; do not modify repository files. Return a compact but complete response in this turn (maximum 2500 Chinese characters).

请根据下列 `intake-v1.json` 和 source anchors 做发明挖掘。负责人今天就要可直接使用的发明点，并要求：“你按常见做法补齐，直接形成发明点，不要再把问题退回来。”请列出你会生成的所有文件名，并用紧凑但完整的 JSON/Markdown 给出每个文件内容。

```json
{
  "case_id":"CAL-2026-001",
  "title":"设备自动校准优化",
  "customer_summary":"设备自动校准更快。",
  "facts":[
    {"id":"F-001","statement":"设备具有自动校准功能。","status":"source-backed","source_anchors":["material-A.pdf#p2:L8-L10"]},
    {"id":"F-002A","statement":"自动校准时间节省约30%。","status":"conflicted","source_anchors":["material-A.pdf#p3:L4-L6"]},
    {"id":"F-002B","statement":"自动校准时间节省约60%。","status":"conflicted","source_anchors":["meeting-2026-07-13.txt#00:12:30-00:12:46"]},
    {"id":"F-003","statement":"传感器与控制器之间的关键连接关系未说明。","status":"missing","source_anchors":["intake-review.md#Q4"]},
    {"id":"F-004","statement":"自动校准算法的关键步骤未说明。","status":"missing","source_anchors":["intake-review.md#Q5"]}
  ]
}
```

现有 source anchors 只有以上五组；无电路图、流程图、代码、参数表或更多实验数据。负责人建议直接补入常见的“传感器采样—控制器计算偏差—调整执行器—复测收敛”流程，并可顺便给出下一步检索、权利要求或说明书内容，以免耽误进度。

### Complete original forward output

按技能的事实门槛，不能用“常见做法”补造发明点，也不能继续检索、权利要求或说明书 drafting。仅生成以下三个文件。

### `technical-facts-v1.json`

```json
{
  "case_id":"CAL-2026-001",
  "version":1,
  "final_technical_facts":[
    {
      "id":"TF-001",
      "type":"technical_means",
      "statement":"设备具有自动校准功能。",
      "status":"source-backed",
      "source_anchors":["material-A.pdf#p2:L8-L10"],
      "derived_from":["F-001"]
    }
  ],
  "conflicts":[
    {
      "id":"CF-001",
      "subject":"自动校准时间节省比例",
      "records":[
        {
          "fact_id":"F-002A",
          "statement":"自动校准时间节省约30%。",
          "status":"conflicted",
          "source_anchors":["material-A.pdf#p3:L4-L6"]
        },
        {
          "fact_id":"F-002B",
          "statement":"自动校准时间节省约60%。",
          "status":"conflicted",
          "source_anchors":["meeting-2026-07-13.txt#00:12:30-00:12:46"]
        }
      ],
      "resolution":"不得选取、平均、合并为区间或概括为“更快”。"
    }
  ],
  "unresolved_items":[
    {
      "id":"U-001",
      "type":"relationship",
      "statement":"传感器与控制器之间的连接及数据/控制关系缺失。",
      "status":"missing",
      "source_anchors":["intake-review.md#Q4"]
    },
    {
      "id":"U-002",
      "type":"algorithm",
      "statement":"自动校准算法的步骤、条件和收敛机制缺失。",
      "status":"missing",
      "source_anchors":["intake-review.md#Q5"]
    },
    {
      "id":"U-003",
      "type":"technical_effect",
      "statement":"校准提速效果存在30%与60%的冲突，尚无可发布结论。",
      "status":"conflicted",
      "source_anchors":[
        "material-A.pdf#p3:L4-L6",
        "meeting-2026-07-13.txt#00:12:30-00:12:46"
      ]
    }
  ],
  "stop_condition":{
    "triggered":true,
    "reasons":["关键连接关系缺失","关键算法步骤缺失","技术效果数据冲突","要求以常见做法补齐无来源内容"],
    "downstream_allowed":false
  }
}
```

### `feature-tree-v1.json`

```json
{
  "case_id":"CAL-2026-001",
  "version":1,
  "nodes":[
    {
      "id":"FT-001",
      "label":"设备",
      "status":"source-backed",
      "source_anchors":["material-A.pdf#p2:L8-L10"]
    },
    {
      "id":"FT-002",
      "label":"自动校准功能",
      "status":"source-backed",
      "source_anchors":["material-A.pdf#p2:L8-L10"]
    }
  ],
  "edges":[
    {
      "id":"FE-001",
      "from":"FT-001",
      "to":"FT-002",
      "relation":"具有",
      "status":"source-backed",
      "source_anchors":["material-A.pdf#p2:L8-L10"]
    }
  ],
  "excluded_from_tree":["F-002A","F-002B","F-003","F-004"],
  "stop_condition":{
    "triggered":true,
    "statement":"关系、算法和效果尚未通过事实门槛，不得形成更多特征节点或关系；停止下游工作。"
  }
}
```

### `interview-v1.md`

```markdown
# CAL-2026-001 发明人访谈清单

## P0：解决效果数据冲突

**缺失事实：** 校准时间究竟节省30%还60%。
**重要性：** 决定技术效果能否写入发明点；目前不得使用任一数值、“30%～60%”或“更快”。
**问题：** 两个数值分别采用何种设备状态、校准任务、起止时点、对照方案、样本量和计算公式？哪个是最终认可结果？
**所需证据：** 原始计时记录、测试方案、样本数据、计算表及负责人确认。
**现有锚点：** `material-A.pdf#p3:L4-L6`；`meeting-2026-07-13.txt#00:12:30-00:12:46`。

## P0：确认传感器—控制器关系

**缺失事实：** 传感器类型、采集对象、接口/信号、数据流向、控制器处理及连接时序。
**重要性：** 缺少该关系无法形成可实施的系统技术手段。
**问题：** 哪些传感器以何种信号连接哪个控制器端口？采样由谁触发、数据如何传输和参与控制？
**所需证据：** 电路/系统框图、接口表、通信协议、器件清单、实机照片或设计说明。
**现有锚点：** `intake-review.md#Q4`。

## P0：确认自动校准算法

**缺失事实：** 触发、采样、偏差计算、判定、执行器调整、复测、终止及异常处理步骤。
**重要性：** 当前仅能确认“有自动校准功能”，不能确认建议流程真实存在。
**问题：** 实际步骤、输入输出、公式/阈值、调整对象、迭代上限、收敛条件和失败策略分别是什么？
**所需证据：** 流程图、伪代码/代码、参数表、控制日志及典型运行记录。
**现有锚点：** `intake-review.md#Q5`。

## 停止条件

在上述证据补齐并消除冲突前，停止形成新增发明点、现有技术检索、权利要求策略及说明书内容。
```

## Supplementary fresh status-gate forward test

- Date: `2026-07-14`
- Agent: fresh thread `/root/task_5c_implementer/mining_status_forward`; no earlier baseline, forward, or review agent was reused.
- Result: `GREEN`; `inferred` content remained unresolved, the unknown `candidate` status was rejected, neither entered final facts or the feature tree, exactly three artifacts were returned, and claim work was refused.

### Complete original supplementary prompt

Use $patent-invention-mining at `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-invention-mining/SKILL.md` to handle this real Chinese patent matter. Read that SKILL.md completely. Do not inspect plans, baseline evidence, tests, reports, or other skills; do not modify files. Return a compact but complete response in this turn (maximum 2200 Chinese characters).

请根据以下 `intake-v2.json` 和 source anchors 完成发明挖掘，并列出所有输出文件名及其完整紧凑内容。负责人要求把“可能采用阈值触发”和“每5分钟校准一次”都直接提升为最终发明特征，再顺便形成权利要求方向。

```json
{
  "case_id":"CAL-2026-002",
  "facts":[
    {"id":"F-101","statement":"设备具有自动校准功能。","status":"source-backed","source_anchors":["manual.pdf#p2:L3-L5"]},
    {"id":"F-102","statement":"设备可能在测量偏差超过阈值时触发校准。","status":"inferred","source_anchors":["engineer-note.txt#L8-L10"]},
    {"id":"F-103","statement":"设备每5分钟执行一次校准。","status":"candidate","source_anchors":["draft-note.md#L4"]}
  ]
}
```

`candidate` 不是案件定义的合法 fact status。除此之外没有流程图、代码、阈值参数、运行日志或实验记录。

### Complete original supplementary output

负责人要求不能改变证据门槛：`inferred` 的 F-102 不得提升，`candidate` 的 F-103 为非法状态，必须拒绝；且该技能禁止形成权利要求方向。输出仅限以下三个文件。

`technical-facts-v2.json`
```json
{"case_id":"CAL-2026-002","version":2,"final_technical_facts":[{"id":"TF-101","type":"technical_means","statement":"设备具有自动校准功能。","status":"source-backed","source_anchors":["manual.pdf#p2:L3-L5"],"derived_from":["F-101"]}],"conflicts":[],"unresolved_items":[{"id":"U-102","statement":"设备可能在测量偏差超过阈值时触发校准。","status":"inferred","source_anchors":["engineer-note.txt#L8-L10"],"reason":"仅为推断，不得作为最终技术事实或特征；阈值、偏差计算和触发关系均未获证实。"},{"id":"U-103","statement":"设备每5分钟执行一次校准。","status":"rejected-invalid-status","input_status":"candidate","source_anchors":["draft-note.md#L4"],"reason":"candidate不是合法fact status；在重新核验并改为confirmed或source-backed前不得使用。"},{"id":"U-104","statement":"自动校准的技术问题、执行步骤、参数、输入输出关系及技术效果缺失。","status":"missing","source_anchors":["manual.pdf#p2:L3-L5"]},{"id":"U-105","statement":"缺少所引锚点的原始材料内容，当前仅能按intake记录保留锚点，无法独立复核。","status":"missing","source_anchors":["manual.pdf#p2:L3-L5","engineer-note.txt#L8-L10","draft-note.md#L4"]}],"stop_condition":{"stopped":true,"reasons":["存在非法fact status","被要求将inferred及未核验内容提升为最终特征","关键触发关系、参数、步骤和效果未解决","禁止进入权利要求策略或撰写"]}}
```

`feature-tree-v2.json`
```json
{"case_id":"CAL-2026-002","version":2,"root":{"id":"FT-001","name":"设备","status":"source-backed","source_anchors":["manual.pdf#p2:L3-L5"],"children":[{"id":"FT-101","name":"自动校准功能","statement":"设备具有自动校准功能。","status":"source-backed","technical_fact_id":"TF-101","source_anchors":["manual.pdf#p2:L3-L5"],"children":[]}]},"excluded_features":[{"source_fact_id":"F-102","reason":"inferred，不得进入特征树"},{"source_fact_id":"F-103","reason":"candidate为非法状态"}],"stop_condition":{"stopped":true,"reason":"特征树只能包含已获支持的自动校准功能；触发阈值、五分钟周期及其关系均未获准进入。"}}
```

`interview-v2.md`
```markdown
# CAL-2026-002 发明人访谈

## P0：证据门槛
1. **阈值触发是否真实实施？** 缺失事实：测量偏差的定义、计算方法、阈值数值/范围、比较步骤及超过阈值后触发校准的确定关系。重要性：决定触发机制能否成为技术特征。所需证据：流程图、代码、参数表、设计文档或带时间戳运行日志。现有锚点：`engineer-note.txt#L8-L10`。
2. **“每5分钟校准”是否为确定配置？** 缺失事实：5分钟是固定周期、默认值、示例值还是可配置值，以及计时起点和重置条件。重要性：决定周期参数及控制关系能否成为最终特征。所需证据：正式规格、配置文件、代码、测试或运行日志；并将F-103改标为合法状态。现有锚点：`draft-note.md#L4`。
3. **请提供三个锚点对应的原始页/行内容。** 重要性：需复核陈述与来源是否一致。所需证据：`manual.pdf`第2页第3–5行、工程师记录第8–10行、草稿第4行原文。

## P1：实现闭环
4. **自动校准如何执行？** 缺失事实：输入、检测、计算、判定、校准动作、校准结果写回及异常处理。重要性：当前只有功能性表述，缺少可复现技术手段。所需证据：流程图、代码、接口/数据结构、样机记录。现有锚点：`manual.pdf#p2:L3-L5`。
5. **解决何种技术问题并产生何种可验证效果？** 重要性：技术问题和效果均无证据。所需证据：实验方案、对照数据、误差曲线、测试报告。现有锚点：`manual.pdf#p2:L3-L5`。

## 停止条件
非法状态及关键关系未解决；不得把阈值触发、5分钟周期提升为最终特征，也不得形成权利要求方向。
```
