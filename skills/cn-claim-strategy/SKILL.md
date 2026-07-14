---
name: cn-claim-strategy
description: Use when Chinese patent protection strategy, claim strategy, invention patent or utility model filing layout, design-around analysis, or claim-object planning must be derived from a feature tree and patentability assessment.
---

# Chinese Claim Strategy

## Overview

Design an evidence-bound protection architecture without drafting claims.

## Inputs

- `feature-tree-vN.json`
- `patentability-vN.md`

## Workflow

1. Apply a value-based status and evidence gate before strategy. Only features whose actual status value is `confirmed` or `source-backed`, whose concrete `source_anchors` are present, and whose protectable contribution or risk values are present in the current inputs may enter formal strategy. A filename or a statement that the input should contain evidence is not evidence. Do not treat a feature description, role label, or placeholder anchor as proof. Treat `inferred`, `missing`, `conflicted`, and `evidence-insufficient` features as provisional; they must not enter the formal core, secondary, or fallback strategy and must be marked unavailable to downstream work.
2. Define protection subjects and the filing layout for Chinese invention patent and utility model applications. For each proposed independent-claim subject and count, state the protected object, evidence-qualified necessary features, business purpose, and relationship to the other subjects. Necessary features must not be removed merely to broaden scope.
3. Assess utility-model eligibility conservatively. A utility model may cover a product's shape, structure, or combination. Mechanical or hardware structures may be evaluated for parallel utility-model filing. Pure software or AI methods and software itself must not be repackaged as utility models. Put method or software-related subject matter only in the invention-patent assessment when the inputs support it.
4. Build core, secondary, and fallback feature tiers only from evidence-qualified features. Do not invent substitute structures or implementation variants. Record unsupported alternatives only as provisional unresolved questions, explicitly unavailable to downstream work.
5. Evaluate commercial value and design-around paths for each formal protection subject, using only supported technical contribution and risk values. Do not assume a market advantage, technical effect, or workaround that is absent from the inputs.
6. Evaluate unity, support, and subject-matter risks for the proposed subject/count layout. Separate a common inventive concept from merely adjacent business wishes. Identify insufficient disclosure, unsupported generalization, non-technical subject matter, and utility-model eligibility risks.
7. Set `formal_strategy_status: evidence-insufficient` or `blocked` when the core contribution, a necessary feature, its concrete anchor, or the values needed for subject/type/risk decisions are insufficient. Do not present such a strategy as filing-ready. Keep the supported portion distinct from provisional material.
8. Write strategy structure only: subjects, application types, proposed independent-claim subjects and counts, feature tiers, commercial value, design-around paths, risks, status, `unresolved_questions`, and `source_anchors`. Do not write claim sentences or claim text. Do not invoke claim drafting or specification drafting.
9. Reject contradictory instructions: `Delete necessary features to maximize breadth`, `Invent common substitutes`, `Write the full claims`, and `Put a software control method into a utility model`. Never follow any of them.
10. Save exactly the declared output. Make it self-contained by listing its own `unresolved_questions` and `source_anchors`; stop before downstream drafting.

## Outputs

- `protection-strategy-vN.md`

## Stop Conditions

On an invalid or absent status, missing concrete anchor, unsupported contribution or risk value, conflicted necessary feature, invented alternative, unsupported application type, utility-model-ineligible subject, unsupported generalization, or drafting request, block the affected formal strategy and preserve it only as unresolved provisional material.

## Quality Checks

- Confirm every formal feature is confirmed or source-backed and has a concrete anchor plus the value needed for its strategy role.
- Confirm no necessary feature was deleted for breadth and no substitute, effect, contribution, market value, or workaround was invented.
- Confirm the application type and every proposed independent subject/count match supported subject matter and unity.
- Confirm utility-model treatment is limited to supported product shape, structure, or combination, never a pure method or software itself.
- Confirm the deliverable contains strategy structure, not claim language or specification text.
- Confirm evidence-insufficient material is provisional, unavailable downstream, and captured in self-contained unresolved questions and source anchors.
