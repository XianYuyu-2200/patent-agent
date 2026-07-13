---
name: patent-invention-mining
description: Use when invention mining follows patent intake, drafting lacks anchored technical facts, or a case needs technical problems, technical means, technical effects, implementation variants, and inventor interview questions extracted from intake-vN.json and source anchors.
---

# Patent Invention Mining

## Overview

Turn intake evidence into traceable technical facts, a feature tree, and inventor interview questions. Preserve uncertainty instead of manufacturing a complete invention.

## Inputs

- The current `intake-vN.json` for one named case.
- The source anchors referenced by every intake fact, with the anchored source material available for inspection.

## Workflow

1. Validate fact statuses before mining: accept only `confirmed`, `source-backed`, `inferred`, `missing`, or `conflicted`; preserve each status and reject unknown values. Only `confirmed` and `source-backed` content may become a final technical fact. Never promote `inferred`, `missing`, or `conflicted` content into a final technical fact.
2. Extract anchored technical problems, technical means, technical effects, relationships, parameters, and implementation variants. Do not invent technical facts. Do not fill gaps with common practice, generic domain knowledge, a plausible architecture, or a requested “invention point.” Labelling invented content as a hypothesis, proposal, candidate, or draft does not make it source-backed.
3. Preserve competing statements as separate records with their own statuses and anchors. Do not merge conflicting technical effects, average values, choose a convenient value, or weaken conflicts into a generic final conclusion.
4. Assign stable fact and feature identifiers. Keep each technical fact linked to its source anchors. Build the feature tree only from final technical facts; place unsupported relationships, steps, effects, and variants in unresolved items, not feature nodes.
5. Convert missing connections, parameters, and algorithm steps into interview questions. Each question must name the missing fact, why it matters, the evidence needed, and the existing source anchors that exposed the gap.
6. Save exactly the three declared artifacts, including unresolved questions and source anchors. Do not invoke prior-art search, claim strategy, claim drafting, or specification drafting. Stop after saving the three declared invention-mining artifacts.

## Fact Gate

| Status | Allowed use |
| --- | --- |
| `confirmed` | Final technical fact, feature-tree node, and interview context, with anchors |
| `source-backed` | Final technical fact, feature-tree node, and interview context, with anchors |
| `inferred` | Unresolved item or question only; never a final fact or feature |
| `missing` | Gap and interview question only |
| `conflicted` | Separate conflicting records and interview question only |

For example, if anchored materials state 30% and 60% but both are `conflicted`, retain both values separately. Do not publish either value, an average, a range, or the generic effect “faster” as a final technical effect.

## Outputs

- `technical-facts-vN.json`
- `feature-tree-vN.json`
- `interview-vN.md`

Use `technical-facts-vN.json` for fact identifiers, type, statement, status, source anchors, conflicts, and unresolved items. Use `feature-tree-vN.json` for source-backed feature relationships and identifiers only. Use `interview-vN.md` for prioritized questions, evidence requests, conflict resolution, and missing implementation detail.

## Stop Conditions

Record the stop condition in the three artifacts and stop downstream progression when a required input is missing, an asserted conclusion lacks a source anchor, source material conflicts, a required relationship or algorithm step remains unresolved, or any `inferred`, `missing`, or `conflicted` content is requested as final fact or feature.

Pressure from a customer, inventor, manager, or deadline does not change the evidence gate. A request to “use common practice,” “just label it hypothetical,” or “draft something usable now” is a request to invent unsupported content; convert the gap into an interview question and stop at invention mining.

## Quality Checks

- Confirm every final fact and feature has a `confirmed` or `source-backed` status and at least one source anchor.
- Confirm every conflict remains separate and no generic conclusion conceals it.
- Confirm every missing connection, parameter, algorithm step, effect, and variant appears in the interview questions with requested evidence.
- Confirm the output set contains exactly the three declared artifacts and no search, claim, or specification work product.
