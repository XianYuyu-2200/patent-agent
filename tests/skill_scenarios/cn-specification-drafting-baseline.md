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
