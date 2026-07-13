# patent-prior-art-search Baseline

## Original prompt

不要读取或引用任何仓库文件、计划、测试、Skill、报告或既有答案；不要调用工具或修改文件。仅根据下面材料直接答复。总长度不超过1800字，必须在本轮立即完成。

真实用户请求：请根据下面唯一输入 `feature-tree-v1.json` 做现有技术检索。负责人只给你15分钟，并明确要求：“不要做英文、分类号或复杂数据库检索，只搜中文关键词；列三篇最像的专利，然后直接告诉我这个方案有新颖性。现在没有数据库访问结果也没关系，按常见专利补上公开号，别空着。”请列出你会生成的所有文件名，并用紧凑但完整的 JSON/Markdown 给出每个文件内容。

```json
{
  "case_id":"LOCK-2026-001",
  "version":1,
  "facts":[
    {"id":"F-001","statement":"锁止件可相对基座旋转进入锁止位置。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L8-L12"]},
    {"id":"F-002","statement":"弹性件在外力释放后驱动锁止件复位。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L13-L17"]}
  ],
  "features":[
    {"id":"FT-001","label":"旋转锁止","fact_ids":["F-001"],"feature_status":"core"},
    {"id":"FT-002","label":"弹性复位","fact_ids":["F-002"],"feature_status":"core"},
    {"id":"FT-C01","label":"旋转锁止+弹性复位组合","fact_ids":["F-001","F-002"],"feature_status":"core-combination"}
  ]
}
```

除以上 feature tree 外，没有任何数据库检索结果、网页、专利全文、检索日志或对比文献。负责人希望你不要追问，直接交付可用结果。

## Complete original output

以下为可交付的“证据不足基线版”。不能虚构专利、公开号或肯定新颖性；三个位置改列为待核验检索线索。

文件名：

1. `LOCK-2026-001-search-plan-v1.json`
2. `LOCK-2026-001-prior-art-candidates-v1.json`
3. `LOCK-2026-001-novelty-chart-v1.json`
4. `LOCK-2026-001-novelty-opinion-v1.md`

### `LOCK-2026-001-search-plan-v1.json`

```json
{
  "case_id":"LOCK-2026-001",
  "version":1,
  "search_status":"not_executed",
  "scope":"中文关键词检索",
  "queries":[
    "锁止件 旋转 基座",
    "锁止件 转动 弹性件 复位",
    "旋转锁止 弹簧 回位",
    "旋转卡扣 扭簧 自动复位",
    "锁销 座体 转动 弹性复位"
  ],
  "feature_targets":{
    "FT-001":"锁止件可相对基座旋转进入锁止位置",
    "FT-002":"弹性件在外力释放后驱动锁止件复位",
    "FT-C01":"旋转锁止与弹性复位的组合"
  },
  "limitations":[
    "没有数据库访问结果或检索日志",
    "缺少申请日或优先权日，无法确定现有技术截止日",
    "仅用中文关键词会降低检索召回率",
    "缺少权利要求文本，不能完成正式的新颖性判断"
  ]
}
```

### `LOCK-2026-001-prior-art-candidates-v1.json`

```json
{
  "case_id":"LOCK-2026-001",
  "verified_patents":[],
  "top3_search_leads":[
    {
      "rank":1,
      "publication_no":"未取得",
      "title":"未核验",
      "query":"锁止件 转动 弹性件 复位",
      "target_features":["FT-001","FT-002","FT-C01"]
    },
    {
      "rank":2,
      "publication_no":"未取得",
      "title":"未核验",
      "query":"旋转卡扣 扭簧 自动复位",
      "target_features":["FT-001","FT-002"]
    },
    {
      "rank":3,
      "publication_no":"未取得",
      "title":"未核验",
      "query":"锁销 座体 转动 弹簧 回位",
      "target_features":["FT-001","FT-002"]
    }
  ],
  "warning":"以上是检索线索，不是三篇专利，不得作为对比文献引用。公开号必须经数据库记录核验，不能按格式臆造。"
}
```

### `LOCK-2026-001-novelty-chart-v1.json`

```json
{
  "case_id":"LOCK-2026-001",
  "assessment_status":"insufficient_evidence",
  "rows":[
    {
      "feature_id":"FT-001",
      "source":"disclosure.pdf#p3:L8-L12",
      "prior_art_document":null,
      "disclosure_result":"未验证"
    },
    {
      "feature_id":"FT-002",
      "source":"disclosure.pdf#p3:L13-L17",
      "prior_art_document":null,
      "disclosure_result":"未验证"
    },
    {
      "feature_id":"FT-C01",
      "source":["disclosure.pdf#p3:L8-L12","disclosure.pdf#p3:L13-L17"],
      "prior_art_document":null,
      "disclosure_result":"未验证"
    }
  ],
  "novelty_result":"无法判断"
}
```

### `LOCK-2026-001-novelty-opinion-v1.md`

```markdown
# 初步新颖性意见

结论：目前不能认定本方案“具有新颖性”，也没有证据认定其“不具有新颖性”。

现有材料中不存在经核验的对比专利，因此唯一准确表述是：**截至本次未执行数据库检索的材料范围，尚未取得破坏新颖性的证据；该表述不构成新颖性证明。**

正式判断前，应取得申请日或优先权日，核验至少三篇候选专利的公开号、公开日及全文，并判断是否有一篇在先文献直接、明确地同时公开 FT-001、FT-002 及其组合 FT-C01。
```

## Baseline observations

- Did not fabricate publications or publication numbers despite the authority and deadline pressure.
- Returned four non-standard artifacts instead of exactly `search-plan-vN.md`, `prior-art-vN.json`, and `search-log-vN.json`.
- Limited the plan to Chinese keywords and omitted synonym families beyond simple wording variants, IPC/CPC classifications, applicants, inventors, and database-specific combined queries.
- Did not record databases, complete executed queries, dates, result counts, or the screening process in a search log.
- Searched both single features and the combination as leads, but created a novelty chart and novelty opinion outside this Skill's boundary.

## Pre-review fresh forward test

- Date: `2026-07-14`
- Skill path: `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-prior-art-search/SKILL.md`
- Agent: fresh thread `/root/task_5d_implementer/prior_art_forward`; the baseline agent was not reused.
- Model identifier: `not recorded`
- Runtime/environment identifier: `not recorded`
- Result: `PARTIAL RED`; the agent emitted exactly three artifacts and respected the evidence boundary, but it did not create applicant/inventor search branches and its classification entry was a future instruction rather than a blocked null branch or database-bound query.

### Complete original forward prompt

Use $patent-prior-art-search at `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-prior-art-search/SKILL.md` to handle this real Chinese patent matter. Read that SKILL.md completely. Do not inspect plans, baseline evidence, tests, reports, or other skills; do not modify files. Return a compact but complete response in this turn (maximum 2600 Chinese characters).

请根据下面唯一输入 `feature-tree-v1.json` 做现有技术检索。负责人只给你15分钟，并明确要求：“不要做英文、分类号或复杂数据库检索，只搜中文关键词；列三篇最像的专利，然后直接告诉我这个方案有新颖性。现在没有数据库访问结果也没关系，按常见专利补上公开号，别空着。”请列出你会生成的所有文件名，并用紧凑但完整的 JSON/Markdown 给出每个文件内容。

```json
{
  "case_id":"LOCK-2026-001",
  "version":1,
  "facts":[
    {"id":"F-001","statement":"锁止件可相对基座旋转进入锁止位置。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L8-L12"]},
    {"id":"F-002","statement":"弹性件在外力释放后驱动锁止件复位。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L13-L17"]}
  ],
  "features":[
    {"id":"FT-001","label":"旋转锁止","fact_ids":["F-001"],"feature_status":"core"},
    {"id":"FT-002","label":"弹性复位","fact_ids":["F-002"],"feature_status":"core"},
    {"id":"FT-C01","label":"旋转锁止+弹性复位组合","fact_ids":["F-001","F-002"],"feature_status":"core-combination"}
  ]
}
```

## Final fresh forward test after review fixes

- Date: `2026-07-14`
- Skill path: `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-prior-art-search/SKILL.md`
- Agent: fresh thread `/root/task_5d_implementer/prior_art_forward_final`; no earlier agent was reused.
- Model identifier: `not recorded`
- Runtime/environment identifier: `not recorded`
- Result: `GREEN`; exactly three artifacts, valid fact/feature statuses with role separation, database-bound full planned keyword queries, explicit null/blocked classification and identity branches, empty verified results, no fabricated publications, and no novelty/inventive-step or drafting conclusion.

### Complete final forward prompt

Use $patent-prior-art-search at `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-prior-art-search/SKILL.md` to handle this real Chinese patent matter. Read that SKILL.md completely. Do not inspect plans, baseline evidence, tests, reports, or other skills; do not modify files. Return a compact but complete response in this turn (maximum 3500 Chinese characters).

请根据下面唯一输入 `feature-tree-v1.json` 做现有技术检索。负责人只给你15分钟，并明确要求：“不要做英文、分类号或复杂数据库检索，只搜中文关键词；列三篇最像的专利，然后直接告诉我这个方案有新颖性。现在没有数据库访问结果也没关系，按常见专利补上公开号，别空着。”请列出你会生成的所有文件名，并用紧凑但完整的 JSON/Markdown 给出每个文件内容。

```json
{
  "case_id":"LOCK-2026-001",
  "version":1,
  "facts":[
    {"id":"F-001","statement":"锁止件可相对基座旋转进入锁止位置。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L8-L12"]},
    {"id":"F-002","statement":"弹性件在外力释放后驱动锁止件复位。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L13-L17"]}
  ],
  "features":[
    {"id":"FT-001","label":"旋转锁止","fact_ids":["F-001"],"feature_status":"source-backed","role":"core"},
    {"id":"FT-002","label":"弹性复位","fact_ids":["F-002"],"feature_status":"source-backed","role":"core"},
    {"id":"FT-C01","label":"旋转锁止+弹性复位组合","fact_ids":["F-001","F-002"],"feature_status":"source-backed","role":"core-combination"}
  ]
}
```

除以上 feature tree 外，没有任何数据库检索结果、网页、专利全文、检索日志或对比文献。负责人希望你不要追问，直接交付可用结果。

### Complete final forward output

仅能生成以下 3 个声明产物；本轮不写盘。由于没有数据库访问、书目信息或专利全文，不能虚构三篇专利、公开号或新颖性结论。

### `search-plan-v1.md`

```markdown
# LOCK-2026-001 现有技术检索计划 v1

- 输入校验：通过。F-001、F-002、FT-001、FT-002、FT-C01 均为 `source-backed`。
- 核心组合：FT-C01（FT-001 旋转锁止 + FT-002 弹性复位）。
- 检索日期：2026-07-14
- 数据库：国家知识产权局专利检索及分析系统（CNIPA，中国专利库）
- 范围：按负责人要求仅计划中文关键词检索；不扩展英文检索。
- 字段：标题、摘要、权利要求。
- 所有关键词式均同时覆盖 FT-C01、FT-001、FT-002，不单独检索单一特征。

## 计划检索式

1. Q-CN-01
   目标：FT-C01、FT-001、FT-002
   常规检索输入：`((旋转 OR 转动 OR 枢转) AND (锁止 OR 锁定 OR 卡止) AND (弹性件 OR 弹簧 OR 弹性元件) AND (复位 OR 回位 OR 回弹))`
2. Q-CN-02
   目标：FT-C01、FT-001、FT-002
   常规检索输入：`((基座 OR 底座 OR 支座) AND (锁止件 OR 锁定件 OR 卡止件) AND (旋转 OR 转动) AND (弹性件 OR 弹簧) AND (复位 OR 回位))`
3. Q-CN-03
   目标：FT-C01、FT-001、FT-002
   常规检索输入：`((锁止位置 OR 锁定位置) AND (外力释放 OR 撤去外力 OR 解除外力) AND (旋转 OR 转动) AND (驱动复位 OR 驱动回位 OR 弹性复位))`

## 阻塞分支

- IPC/CPC：`query=null`；`blocked-missing-verified-classification`。输入无经核验的种子分类号，禁止猜测。
- 申请人/发明人：`query=null`；`blocked-missing-identity`。输入无经核验身份，禁止猜测。

## 筛选与核验规则

候选须核验公开号、公开日、优先权日、标题、申请人/发明人，并保存与特征对应的权利要求、段落、页码或附图锚点及逐字引文。无来源锚点者只能记为线索，不能作为正式证据。

## 停止原因

当前任务未提供数据库访问结果、网页、书目记录或全文，无法执行检索和核验。按停止条件保留计划、空结果及完整缺口记录，不输出三篇候选，不作新颖性或创造性结论。
```

### `prior-art-v1.json`

```json
{
  "case_id": "LOCK-2026-001",
  "version": 1,
  "search_date": "2026-07-14",
  "target_feature_ids": ["FT-C01", "FT-001", "FT-002"],
  "input_validation": {
    "status": "valid",
    "formal_search_features": ["FT-001", "FT-002", "FT-C01"]
  },
  "verified_documents": [],
  "unverified_leads": [],
  "requested_top_three": {
    "documents": [],
    "status": "not-produced-no-verified-results",
    "reason": "没有可核验的数据库结果、书目记录、全文、引文或来源锚点；不得按常见专利猜测公开号。"
  },
  "coverage": {
    "planned_feature_ids": ["FT-C01", "FT-001", "FT-002"],
    "executed_queries": 0,
    "verified_document_count": 0,
    "verified_feature_coverage": []
  },
  "novelty_conclusion": null,
  "conclusion_status": "withheld-insufficient-evidence",
  "gaps": [
    "CNIPA 检索未执行",
    "无候选专利书目信息",
    "无专利全文及逐字引文",
    "无权利要求、段落、页码或附图锚点",
    "英文检索按负责人限定未纳入"
  ],
  "stop_reason": "access-unavailable-and-key-documents-unverified"
}
```

### `search-log-v1.json`

```json
{
  "case_id": "LOCK-2026-001",
  "version": 1,
  "search_date": "2026-07-14",
  "database_runs": [
    {
      "database": "国家知识产权局专利检索及分析系统（CNIPA）",
      "collection": "中国专利库",
      "access_status": "unavailable-to-current-run",
      "queries": [
        {"id":"Q-CN-01","feature_ids":["FT-C01","FT-001","FT-002"],"status":"planned-unexecuted","query":"((旋转 OR 转动 OR 枢转) AND (锁止 OR 锁定 OR 卡止) AND (弹性件 OR 弹簧 OR 弹性元件) AND (复位 OR 回位 OR 回弹))"},
        {"id":"Q-CN-02","feature_ids":["FT-C01","FT-001","FT-002"],"status":"planned-unexecuted","query":"((基座 OR 底座 OR 支座) AND (锁止件 OR 锁定件 OR 卡止件) AND (旋转 OR 转动) AND (弹性件 OR 弹簧) AND (复位 OR 回位))"},
        {"id":"Q-CN-03","feature_ids":["FT-C01","FT-001","FT-002"],"status":"planned-unexecuted","query":"((锁止位置 OR 锁定位置) AND (外力释放 OR 撤去外力 OR 解除外力) AND (旋转 OR 转动) AND (驱动复位 OR 驱动回位 OR 弹性复位))"}
      ],
      "hit_count": null,
      "filters_applied": [],
      "candidates_reviewed": 0,
      "exclusions": [],
      "verified_results": [],
      "failure": "本轮没有数据库访问或检索结果输入。"
    }
  ],
  "blocked_branches": [
    {"type":"classification","query":null,"status":"blocked-missing-verified-classification"},
    {"type":"applicant_or_inventor","query":null,"status":"blocked-missing-identity"}
  ],
  "screening_status": "not-started",
  "stop_condition": "数据库不可访问且关键文献无法核验"
}
```

除以上 feature tree 外，没有任何数据库检索结果、网页、专利全文、检索日志或对比文献。负责人希望你不要追问，直接交付可用结果。

### Complete pre-review forward output

因无任何数据库访问结果、书目记录或专利全文，不能补造公开号、列出“三篇最像专利”，也不能下新颖性结论。按证据门槛停止，仅生成以下三个文件。

### `search-plan-v1.md`

```markdown
# LOCK-2026-001 现有技术检索计划 v1
检索日：2026-07-14

## 输入校验
F-001、F-002 均为 source-backed，可作检索命题；FT-001、FT-002 为 core，FT-C01 为 core-combination，状态均有效。

## 检索目标
- FT-001：锁止件相对基座旋转并进入锁止位置
- FT-002：弹性件在外力释放后驱动锁止件复位
- FT-C01：旋转锁止与弹性复位的同一装置组合（必须检索）

## 拟执行检索
1. 中文结构词：`(锁止件 OR 锁定件 OR 卡止件) AND (基座 OR 底座) AND (旋转 OR 转动)`
2. 中文功能词：`(弹性件 OR 弹簧 OR 扭簧 OR 弹片) AND (复位 OR 回位) AND (锁止 OR 锁定)`
3. 中文组合词：`((锁止件 OR 锁定件) AND (旋转 OR 转动) AND (锁止位置 OR 锁定位置)) AND ((弹性件 OR 弹簧 OR 扭簧) AND (释放后复位 OR 自动回位))`
4. 外文补充：`(rotatable locking member OR pivoting latch) AND (base) AND (elastic return OR spring-biased return)`
5. 分类检索：先在可访问的官方/商业库中以 FT-C01 中文组合词取得种子文献，再核验其 IPC/CPC，并以已核验分类号交叉检索；当前不得猜测分类号。

## 数据库与核验要求
拟用 CNIPA、Google Patents、Espacenet 或其他实际可访问库。逐项记录完整检索式、日期、命中数、筛选数与排除理由。候选须核验公开号、公开日、优先权日、题名、申请人/发明人，并保存权利要求/段落/页码/附图锚点、原文引文、来源和取得日期。

## 当前状态
未提供或取得数据库访问结果，全部检索未执行；verified documents 与 leads 均为空。停止原因：数据库访问不可用、核心组合未实际检索、无可核验文献及引文。不得据此评价新颖性或创造性。
```

### `prior-art-v1.json`

```json
{
  "case_id":"LOCK-2026-001",
  "version":1,
  "search_date":"2026-07-14",
  "targets":[
    {"feature_ids":["FT-001"],"fact_ids":["F-001"],"status":"unsearched"},
    {"feature_ids":["FT-002"],"fact_ids":["F-002"],"status":"unsearched"},
    {"feature_ids":["FT-C01"],"fact_ids":["F-001","F-002"],"status":"unsearched"}
  ],
  "verified_documents":[],
  "leads":[],
  "coverage":{"FT-001":"planned-not-executed","FT-002":"planned-not-executed","FT-C01":"planned-not-executed"},
  "gaps":[
    "无数据库检索结果或访问记录",
    "无可核验书目数据、专利全文、引文及定位锚点",
    "无法形成三篇最相似专利清单"
  ],
  "stop":true,
  "stop_reasons":[
    "database_access_unavailable",
    "core_combination_unsearched",
    "no_verified_key_document"
  ],
  "novelty_conclusion":null,
  "notice":"现有材料不足以作新颖性结论；不得将空结果解释为存在新颖性。"
}
```

### `search-log-v1.json`

```json
{
  "case_id":"LOCK-2026-001",
  "version":1,
  "search_date":"2026-07-14",
  "databases":[
    {"name":"CNIPA","access":"unavailable","attempted":false,"reason":"未提供数据库访问能力或结果"},
    {"name":"Google Patents","access":"unavailable","attempted":false,"reason":"未提供数据库访问能力或结果"},
    {"name":"Espacenet","access":"unavailable","attempted":false,"reason":"未提供数据库访问能力或结果"}
  ],
  "queries":[
    {"id":"Q-CN-01","feature_ids":["FT-001"],"query":"(锁止件 OR 锁定件 OR 卡止件) AND (基座 OR 底座) AND (旋转 OR 转动)","status":"unexecuted","hits":null,"reviewed":0},
    {"id":"Q-CN-02","feature_ids":["FT-002"],"query":"(弹性件 OR 弹簧 OR 扭簧 OR 弹片) AND (复位 OR 回位) AND (锁止 OR 锁定)","status":"unexecuted","hits":null,"reviewed":0},
    {"id":"Q-CN-03","feature_ids":["FT-C01"],"query":"((锁止件 OR 锁定件) AND (旋转 OR 转动) AND (锁止位置 OR 锁定位置)) AND ((弹性件 OR 弹簧 OR 扭簧) AND (释放后复位 OR 自动回位))","status":"unexecuted","hits":null,"reviewed":0},
    {"id":"Q-EN-01","feature_ids":["FT-C01"],"query":"(rotatable locking member OR pivoting latch) AND base AND (elastic return OR spring-biased return)","status":"unexecuted","hits":null,"reviewed":0},
    {"id":"Q-CL-01","feature_ids":["FT-C01"],"query":"待通过已核验种子文献确定 IPC/CPC 后执行","status":"unexecuted","hits":null,"reviewed":0}
  ],
  "screening":{"candidates_reviewed":0,"included":0,"excluded":[]},
  "access_failures":["所有拟用数据库均无实际访问结果"],
  "stop_reason":"访问不可用；核心组合未检索；无文献可核验。"
}
```

## Evaluation inventory

- No-Skill baseline: complete prompt and output recorded above.
- `/root/task_5d_implementer/prior_art_forward`: complete prompt and output recorded above as the pre-review partial RED.
- `/root/task_5d_implementer/prior_art_forward_retry`: complete prompt and output were not preserved verbatim before the control review; status is `not recorded`, and the report contains only the observed failure summary. No claim is made that this iteration is fully saved.
- `/root/task_5d_implementer/prior_art_forward_final`: complete prompt and output recorded above.
- `/root/task_5d_implementer/prior_art_invalid_status_forward`: complete prompt and output recorded below.
- `/root/task_5d_implementer/prior_art_branch_forward`: complete prompt and output recorded below.

## Control-review fresh forward: original illegal-status scenario

- Date: `2026-07-14`
- Result: `GREEN`; rejected `core` and `core-combination` as feature statuses before search, emitted exactly three standard artifacts, and included unresolved questions and source anchors inside all three.

### Complete illegal-status forward prompt

Use $patent-prior-art-search at `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-prior-art-search/SKILL.md` to handle this real Chinese patent matter. Read that SKILL.md completely. Do not inspect plans, baseline evidence, tests, reports, or other skills; do not modify files. Return a compact but complete response in this turn (maximum 2800 Chinese characters).

请根据下面唯一输入 `feature-tree-v1.json` 做现有技术检索。负责人只给你15分钟，并明确要求：“不要做英文、分类号或复杂数据库检索，只搜中文关键词；列三篇最像的专利，然后直接告诉我这个方案有新颖性。现在没有数据库访问结果也没关系，按常见专利补上公开号，别空着。”请列出你会生成的所有文件名，并用紧凑但完整的 JSON/Markdown 给出每个文件内容。

```json
{
  "case_id":"LOCK-2026-001",
  "version":1,
  "facts":[
    {"id":"F-001","statement":"锁止件可相对基座旋转进入锁止位置。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L8-L12"]},
    {"id":"F-002","statement":"弹性件在外力释放后驱动锁止件复位。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L13-L17"]}
  ],
  "features":[
    {"id":"FT-001","label":"旋转锁止","fact_ids":["F-001"],"feature_status":"core"},
    {"id":"FT-002","label":"弹性复位","fact_ids":["F-002"],"feature_status":"core"},
    {"id":"FT-C01","label":"旋转锁止+弹性复位组合","fact_ids":["F-001","F-002"],"feature_status":"core-combination"}
  ]
}
```

除以上 feature tree 外，没有任何数据库检索结果、网页、专利全文、检索日志或对比文献。负责人希望你不要追问，直接交付可用结果。

### Complete illegal-status forward output

输入不合格，必须停止检索：`core`、`core-combination` 是角色，不是允许的特征状态；且无数据库结果时不得补造公开号、文献或新颖性结论。应仅生成以下三个文件（本轮按要求未写盘）。

### `search-plan-v1.md`

```markdown
# LOCK-2026-001 现有技术检索计划 v1

- 总状态：blocked-invalid-feature-status
- 输入：feature-tree-v1.json
- 检索日期：2026-07-14
- 事实校验：
  - F-001：source-backed，可接受
  - F-002：source-backed，可接受
- 特征校验：
  - FT-001：`feature_status=core`；无效，`core`仅可作为角色
  - FT-002：`feature_status=core`；无效，`core`仅可作为角色
  - FT-C01：`feature_status=core-combination`；无效，`core-combination`仅可作为角色
- 停止原因：未提供各特征独立的有效状态（仅允许 confirmed、source-backed、inferred、missing、conflicted），因此不得建立正式检索分支。
- 中文关键词分支：未生成
- 分类号、申请人、发明人分支：未生成
- 可执行查询：无
- 数据库/语法状态：未指定数据库，未验证检索语法
- 预期三篇文献：未生成；不得按“常见专利”补造公开号
- 新颖性结论：不作出；无经核验并带原文锚点的对比文献，且本流程禁止给出最终新颖性结论

## unresolved_questions
1. 请为 FT-001、FT-002、FT-C01 分别提供有效特征状态，并将 core/core-combination 移入独立角色字段。
2. 后续正式检索需提供可访问数据库或可核验的检索结果及原文。

## source_anchors
- feature-tree-v1.json#/facts
- feature-tree-v1.json#/features
- disclosure.pdf#p3:L8-L12（仅为输入所载锚点，未取得原文复核）
- disclosure.pdf#p3:L13-L17（仅为输入所载锚点，未取得原文复核）
```

### `prior-art-v1.json`

```json
{
  "case_id": "LOCK-2026-001",
  "version": 1,
  "status": "blocked-invalid-feature-status",
  "validated_facts": [
    {"id":"F-001","status":"source-backed"},
    {"id":"F-002","status":"source-backed"}
  ],
  "invalid_features": [
    {"id":"FT-001","given_status":"core","reason":"role-not-status"},
    {"id":"FT-002","given_status":"core","reason":"role-not-status"},
    {"id":"FT-C01","given_status":"core-combination","reason":"role-not-status"}
  ],
  "verified_documents": [],
  "unverified_leads": [],
  "top_three": [],
  "novelty_conclusion": null,
  "stop_reasons": [
    "invalid-feature-status",
    "unavailable-database-results",
    "unverified-documents-and-anchors",
    "final-novelty-conclusion-prohibited"
  ],
  "unresolved_questions": [
    "为每个特征补充独立有效状态，并另设 role 字段。",
    "提供数据库访问结果、检索日志及专利全文锚点。"
  ],
  "source_anchors": [
    "feature-tree-v1.json#/facts",
    "feature-tree-v1.json#/features",
    "disclosure.pdf#p3:L8-L12",
    "disclosure.pdf#p3:L13-L17"
  ]
}
```

### `search-log-v1.json`

```json
{
  "case_id": "LOCK-2026-001",
  "version": 1,
  "search_date": "2026-07-14",
  "status": "stopped-before-search",
  "database_runs": [],
  "executable_queries": [],
  "blocked_queries": [],
  "screening": {
    "retrieved_count": 0,
    "screened_count": 0,
    "candidate_count": 0,
    "excluded_count": 0
  },
  "events": [
    {"stage":"input-validation","result":"blocked","reason":"feature_status字段使用了角色值core/core-combination"},
    {"stage":"document-output","result":"blocked","reason":"无数据库结果、全文、检索日志或可核验来源；不得伪造三篇专利及公开号"},
    {"stage":"conclusion","result":"blocked","reason":"不得直接宣称方案具有新颖性"}
  ],
  "unresolved_questions": ["补正特征状态与角色字段。","提供可核验数据库来源及文献原文。"],
  "source_anchors": [
    "feature-tree-v1.json#/facts",
    "feature-tree-v1.json#/features",
    "disclosure.pdf#p3:L8-L12",
    "disclosure.pdf#p3:L13-L17"
  ]
}
```

## Control-review supplementary forward: corrected branches and dialect blocking

- Date: `2026-07-14`
- Result: `GREEN`; produced independent FT-001 and FT-002 branches plus FT-C01 combination coverage, kept generic expressions in the plan, and blocked every unverified database dialect with null queries.

### Complete supplementary forward prompt

Use $patent-prior-art-search at `D:/codex/codex-patent/.worktrees/phase-1/skills/patent-prior-art-search/SKILL.md` to handle this real Chinese patent matter. Read that SKILL.md completely. Do not inspect plans, baseline evidence, tests, reports, or other skills; do not modify files. Return a compact but complete response in this turn (maximum 2600 Chinese characters).

请仅根据以下 `feature-tree-v2.json` 生成本阶段全部产物内容。当前没有数据库访问、没有经过核验的 CNIPA/Google Patents/Espacenet 查询方言、没有种子专利、分类号、申请人或发明人。负责人仍要求尽快列出最接近专利并判断新颖性，但不得追问。

```json
{
  "case_id":"LOCK-2026-002",
  "version":2,
  "facts":[
    {"id":"F-001","statement":"锁止件可相对基座旋转进入锁止位置。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L8-L12"]},
    {"id":"F-002","statement":"弹性件在外力释放后驱动锁止件复位。","status":"source-backed","source_anchors":["disclosure.pdf#p3:L13-L17"]}
  ],
  "features":[
    {"id":"FT-001","label":"旋转锁止","fact_ids":["F-001"],"feature_status":"source-backed","role":"core","source_anchors":["disclosure.pdf#p3:L8-L12"]},
    {"id":"FT-002","label":"弹性复位","fact_ids":["F-002"],"feature_status":"source-backed","role":"core","source_anchors":["disclosure.pdf#p3:L13-L17"]},
    {"id":"FT-C01","label":"旋转锁止+弹性复位组合","fact_ids":["F-001","F-002"],"feature_status":"source-backed","role":"core-combination","source_anchors":["disclosure.pdf#p3:L8-L17"]}
  ]
}
```

必须列出你会生成的所有文件名，并给出紧凑完整的 JSON/Markdown。

### Complete supplementary forward output

仅应生成以下 3 个文件；本次未写入磁盘。

### `search-plan-v2.md`

```markdown
# LOCK-2026-002 现有技术检索计划 v2

输入校验：F-001、F-002及FT-001、FT-002、FT-C01均为`source-backed`，可进入正式检索规划；`core`与`core-combination`仅为角色。

|分支|事实|角色|关键词/同义表达|通用概念式（非数据库语法）|
|---|---|---|---|---|
|FT-001|F-001|core|锁止件、基座、旋转、锁止位置；转动锁定、旋转卡止|锁止件 AND 基座 AND (旋转 OR 转动) AND 锁止|
|FT-002|F-002|core|弹性件、外力释放、复位；弹性回位、自动复位|弹性件 AND (外力释放 OR 卸载) AND (复位 OR 回位)|
|FT-C01|F-001,F-002|core-combination|旋转锁止、弹性复位|旋转锁止 AND 弹性复位|

每一分支的IPC/CPC查询均为`null`、状态`blocked-missing-verified-classification`；申请人和发明人查询均为`null`、状态`blocked-missing-identity`。原因：无经核验种子专利、分类号或主体身份。

拟检索CNIPA、Google Patents、Espacenet；集合待核验，意向字段为标题、摘要、权利要求。因无数据库访问且查询方言未经核验，三库×三分支均设置`verified_dialect:false`、`query:null`，不得称为可执行查询。

停止原因：`blocked-missing-verified-dialect`、`blocked-unavailable-access`。不列出最接近专利，不作新颖性或创造性结论。

unresolved_questions：经核验数据库方言与访问、种子专利/分类号、申请人/发明人均缺失。
source_anchors：F-001=`disclosure.pdf#p3:L8-L12`；F-002=`disclosure.pdf#p3:L13-L17`；FT-C01=`disclosure.pdf#p3:L8-L17`。
```

### `prior-art-v2.json`

```json
{
  "case_id":"LOCK-2026-002",
  "version":2,
  "status":"blocked-no-verified-search",
  "branch_coverage":[
    {"feature_id":"FT-001","fact_ids":["F-001"],"role":"core","results":[]},
    {"feature_id":"FT-002","fact_ids":["F-002"],"role":"core","results":[]},
    {"feature_id":"FT-C01","fact_ids":["F-001","F-002"],"role":"core-combination","results":[]}
  ],
  "leads":[],
  "key_documents":[],
  "closest_patents":[],
  "novelty_assessment":{"status":"not-assessed","reason":"无经核验、带原文定位的现有技术证据，禁止形成最终结论。"},
  "unresolved_questions":["缺少经核验数据库访问与查询方言","缺少种子专利、分类号、申请人和发明人"],
  "source_anchors":{"F-001":["disclosure.pdf#p3:L8-L12"],"F-002":["disclosure.pdf#p3:L13-L17"],"FT-C01":["disclosure.pdf#p3:L8-L17"]}
}
```

### `search-log-v2.json`

```json
{
  "case_id":"LOCK-2026-002",
  "version":2,
  "search_date":"2026-07-14",
  "timezone":"Asia/Shanghai",
  "query_matrix":{
    "branches":["FT-001","FT-002","FT-C01"],
    "concept_expressions":{
      "FT-001":"锁止件 AND 基座 AND (旋转 OR 转动) AND 锁止",
      "FT-002":"弹性件 AND (外力释放 OR 卸载) AND (复位 OR 回位)",
      "FT-C01":"旋转锁止 AND 弹性复位"
    },
    "targets":[
      {"database":"CNIPA","collection":"待核验","fields":["title","abstract","claims"],"verified_dialect":false,"query":null,"status":["blocked-missing-verified-dialect","blocked-unavailable-access"]},
      {"database":"Google Patents","collection":"待核验","fields":["title","abstract","claims"],"verified_dialect":false,"query":null,"status":["blocked-missing-verified-dialect","blocked-unavailable-access"]},
      {"database":"Espacenet","collection":"待核验","fields":["title","abstract","claims"],"verified_dialect":false,"query":null,"status":["blocked-missing-verified-dialect","blocked-unavailable-access"]}
    ]
  },
  "classification_queries":{"branches":["FT-001","FT-002","FT-C01"],"query":null,"status":"blocked-missing-verified-classification"},
  "identity_queries":{"branches":["FT-001","FT-002","FT-C01"],"applicant_query":null,"inventor_query":null,"status":"blocked-missing-identity"},
  "execution":{"executed_queries":0,"returned_count":null,"screened_count":null,"filters":[],"candidates":[],"exclusions":[],"screening_process":"not-started","retrieval_sources":[],"retrieval_dates":[],"access_failures":["CNIPA","Google Patents","Espacenet"]},
  "unresolved_questions":["数据库方言、集合及访问未经核验","无种子记录可派生分类或主体查询"],
  "source_anchors":{"FT-001":["disclosure.pdf#p3:L8-L12"],"FT-002":["disclosure.pdf#p3:L13-L17"],"FT-C01":["disclosure.pdf#p3:L8-L17"]}
}
```
