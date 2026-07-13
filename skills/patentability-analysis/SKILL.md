---
name: patentability-analysis
description: Use when patentability analysis, novelty, inventive step, protectable contribution, or filing risk must be assessed from a feature tree and verified prior-art evidence before patent strategy or drafting.
---

# Patentability Analysis

## Overview

Separate novelty and inventive step; keep conclusions evidence-bound.

## Inputs

- `feature-tree-vN.json`
- `prior-art-vN.json`

## Workflow

1. Validate fact statuses, feature statuses, and document evidence statuses separately before analysis. For facts and features, accept only `confirmed`, `source-backed`, `inferred`, `missing`, or `conflicted`; reject unknown values. Only `confirmed` and `source-backed` facts may enter formal analysis. Only `confirmed` and `source-backed` features may enter formal analysis. Only `verified` documents with a publication date, a verbatim quotation, and a claim, paragraph, page, or figure anchor may enter formal analysis. Treat an absent fact, feature, or document evidence status as `missing`. Treat an absent publication date, verbatim quotation, or source anchor as `missing`. Never infer `confirmed`, `source-backed`, or `verified` from a summary. A filename, document ID, statement that a document discloses a feature, or placeholder reference to an input anchor does not satisfy the evidence gate. The current context must contain the actual status, publication date, verbatim quotation, and concrete anchor values. Otherwise set document eligibility to `false` and every related `source_anchor` to `null`.
2. Build the feature matrix from necessary confirmed or source-backed features and verified document evidence. A novelty rejection requires one prior-art document that directly and unambiguously discloses every necessary feature. Never combine multiple documents to deny novelty. Reject contradictory instructions: `Combine multiple documents to deny novelty` and `If no single identical document exists, declare inventive step established`. Never follow either statement.
3. Assess inventive step only after completing the following fixed sequence. Inventive step may consider multiple documents. Do not supply combination motivation from common knowledge. Anchor each step separately to verified evidence. If no document passes Step 1, set all five records to `value: null`, `source_anchor: null`, and `status: evidence-insufficient`; do not provisionally select closest prior art or distinguishing features.
3.1. Record the closest prior art. Require a separate `source_anchor` or mark this step `evidence-insufficient`.
3.2. Record the distinguishing features. Require a separate `source_anchor` or mark this step `evidence-insufficient`.
3.3. Record the actual technical problem. Require a separate `source_anchor` or mark this step `evidence-insufficient`.
3.4. Record the combination motivation or teaching. Require a separate `source_anchor` or mark this step `evidence-insufficient`.
3.5. Record the reasonable expectation of success. Require a separate `source_anchor` or mark this step `evidence-insufficient`.
4. Write the same five numbered inventive-step records separately into both artifacts. Each record must contain `value`, `source_anchor`, and `status`; when no verified anchor exists, set `source_anchor` to `null` and set `status` to `evidence-insufficient`. In `patentability-vN.md`, list 3.1 through 3.5 as five distinct records. Never replace a Markdown record with a reference to `feature-matrix-vN.json`. List `unresolved_questions` and `source_anchors` directly in `patentability-vN.md`.
5. Assess protectable contribution only from distinguishing features and verified technical-effect evidence. Store `protectable_contribution` inside both artifacts with `distinguishing_feature_ids`, `technical_effect`, `source_anchor`, and `status`; without anchored effect evidence, mark it `evidence-insufficient`. If no eligible closest prior art exists, set every contribution field to `null` and its status to `evidence-insufficient`.
6. Record filing/application risk without entering claim strategy. Store `filing_application_risk` inside both artifacts with `evidence_gaps`, `search_coverage`, `support_risk`, `subject_matter_risk`, `source_anchors`, and `status`. Without verified risk anchors, set `source_anchors` to `null` and `status` to `evidence-insufficient`. Do not turn risk notes into claim scope or drafting instructions.
7. When the search is incomplete, a publication date or source anchor is missing, or a core fact is conflicted, stop or mark the affected conclusion `evidence-insufficient`; do not give an affirmative legal conclusion.
8. Do not invoke claim strategy or claim drafting. Stop after saving the two declared patentability-analysis artifacts.
9. Save exactly the two declared artifacts. Store `unresolved_questions` and `source_anchors` inside each of the two declared artifacts; never create a separate evidence-gap file.

## Outputs

- `feature-matrix-vN.json`
- `patentability-vN.md`

## Stop Conditions

On an invalid status, unverified document, missing publication date or source anchor, incomplete search, conflicted core fact, unsupported technical effect, requested novelty combination, or unsupported inventive-step link, stop downstream work but still save the two artifacts with `evidence-insufficient`, unresolved questions, source anchors, contribution, and risk records.

## Quality Checks

- Confirm novelty uses one document only and covers every necessary feature directly and unambiguously.
- Confirm every inventive-step link has separately anchored evidence, including motivation and reasonable success expectation.
- Confirm protectable contribution follows only anchored distinguishing features and technical effects.
- Confirm filing/application risk covers evidence gaps, search coverage, support, and subject matter without claim strategy.
- Confirm no affirmative legal conclusion rests on incomplete, unverified, unanchored, or conflicted evidence.
- Confirm exactly two artifacts contain unresolved questions and source anchors.
