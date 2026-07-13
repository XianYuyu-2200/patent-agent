---
name: cn-patent-orchestrator
description: Use when starting, resuming, routing, approving, invalidating, or inspecting a Chinese patent case for intake, invention mining, prior-art search, patentability analysis, claim strategy, claim drafting, specification drafting, quality review, or document export.
---

# Chinese Patent Case Orchestrator

## Overview

Treat `case.json` as the source of truth. Route one permitted stage at a time, persist all declared outputs, and stop whenever facts, approvals, or artifact state do not support the next action.

## Inputs

- A named case workspace containing a valid `case.json`.
- Recorded stage, approvals, fact statuses, artifact versions, stale flags, and review issues.

## Workflow

1. Read `case.json` before every routing decision. Preserve its current stage and approvals; never reconstruct them from chat history.
2. Validate the current state, required inputs, and source anchors. Allow only `confirmed` or `source-backed` facts into final drafting inputs. Never use `inferred`, `missing`, or `conflicted` facts as final drafting inputs. Keep them as unresolved questions.
3. Enforce the adjudicated gates:
   - Require `technical-solution` before entering `SEARCH`.
   - Require `claim-set` before entering `DRAFTING`.
   - Require `final-delivery` before external export. Also require no open high-severity review issue and no stale export input.
4. Select exactly one production skill at a time for the current stage. Invoke no second production skill until all declared outputs from exactly one selected production skill are saved and `case.json` is updated.
5. Use only the selected production skill's declared artifact contract. Do not invent parallel spreadsheets, alternate document packages, or downstream drafts outside that contract.
6. When claims change materially, mark every `specification`, `quality-review`, and `DOCX` artifact stale in `case.json`. Do this before routing further, then require specification regeneration, quality review, and DOCX export again.
7. Save unresolved questions and source anchors with the routed artifact. Report only the next allowed action, not an unapproved downstream package.

## Allowed Routes and Artifacts

Choose one row supported by the current case state and save only that skill's declared outputs.

| Need | Production skill | Declared outputs |
| --- | --- | --- |
| Intake | `cn-patent-case-intake` | `intake-vN.json`, `material-index-vN.json`, `questions-vN.md` |
| Invention mining | `patent-invention-mining` | `technical-facts-vN.json`, `feature-tree-vN.json`, `interview-vN.md` |
| Prior-art search | `patent-prior-art-search` | `search-plan-vN.md`, `prior-art-vN.json`, `search-log-vN.json` |
| Patentability | `patentability-analysis` | `feature-matrix-vN.json`, `patentability-vN.md` |
| Claim strategy | `cn-claim-strategy` | `protection-strategy-vN.md` |
| Claims | `cn-claim-drafting` | `claims-vN.md`, `claim-feature-map-vN.json` |
| Specification | `cn-specification-drafting` | `specification-vN.md`, `abstract-vN.md`, `drawing-plan-vN.json` |
| Quality review | `cn-patent-quality-review` | `quality-review-vN.json`, `support-matrix-vN.json` |
| Delivery | `patent-document-export` | `application-vN.docx`, `delivery-checklist-vN.md` |

## Outputs

- Updated `case.json` with preserved approvals, current stage, artifact references, and stale state.
- All declared outputs from exactly one selected production skill.
- Unresolved questions, source anchors, and the next allowed action or stop reason.

## Stop Conditions

Stop and request human action for a missing or invalid case workspace, invalid case state, missing required approval, conflicting or unanchored facts, an attempt to use `inferred`, `missing`, or `conflicted` facts as final text, an attempt to run multiple production skills, stale export inputs, open high-severity review issues, or any production skill stop condition.
