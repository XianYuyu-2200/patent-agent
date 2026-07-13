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
