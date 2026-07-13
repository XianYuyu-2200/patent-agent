---
name: patent-prior-art-search
description: Use when a prior-art search, novelty search, classification search, or comparison evidence task must start from a feature tree and produce traceable patent-search records for Chinese patent work.
---

# Patent Prior Art Search

## Overview

Plan traceable searches without converting unverified expressions or hits into evidence.

## Inputs

- `feature-tree-vN.json`

## Workflow

1. Validate fact statuses separately from feature statuses before any search planning. For both, accept only `confirmed`, `source-backed`, `inferred`, `missing`, or `conflicted`; reject unknown values. Only `confirmed` and `source-backed` facts may enter formal searches. Only `confirmed` and `source-backed` features may enter formal searches. Block and stop on `inferred`, `missing`, `conflicted`, or unknown fact statuses. Block and stop on `inferred`, `missing`, `conflicted`, or unknown feature statuses. Treat `core` and `core-combination` as roles, not statuses.
2. Identify core features and feature combinations. Create one independent search branch for each `core` feature and one combination branch for each `core-combination` role. A combination branch never replaces the independent core-feature branches. Keep feature and fact identifiers in every branch.
3. Generate keywords, synonyms, IPC/CPC classifications, applicants, inventors, and combined queries for every branch. Derive classifications and identities only from supplied or verified seed records. If none exists, record `query` = `null`, status `blocked-missing-verified-classification` or `blocked-missing-identity`, and a reason; never guess.
4. Keep generic concept expressions in the search plan only. Every executable query record requires `database`, `collection`, `fields`, `verified_dialect`, and `query`. Do not label a generic concept expression as executable database syntax. If the database dialect cannot be verified, set `verified_dialect` to false, `query` = `null`, status `blocked-missing-verified-dialect`, and record the database, collection, intended fields, concept expression, and reason.
5. Record every database, complete query, search date, and screening process for verified executable queries, plus every blocked or unexecuted branch, count, filter, candidate, exclusion, access failure, and retrieval source/date. For each key document, save its publication number, publication date, priority date, title, applicant or inventor, matched feature IDs, a claim, paragraph, page, or figure anchor, and the verbatim quotation.
6. Keep unverified hits as leads only. Do not fabricate a publication number, document, date, result, quotation, or anchor. Do not treat a result without a source anchor as formal evidence. Do not give a final novelty or inventive-step conclusion. Do not invoke claim strategy, claim drafting, or specification drafting.
7. Save exactly the three declared artifacts. Store `unresolved_questions` and `source_anchors` inside each of the three declared artifacts; never create another file for them. Include blocked statuses and stop reasons. Stop after saving the three declared prior-art-search artifacts.

## Outputs

- `search-plan-vN.md`
- `prior-art-vN.json`
- `search-log-vN.json`

## Stop Conditions

On an invalid status, missing independent branch, unverified dialect, unavailable access, unverified document, missing anchor, or excess conclusion request, stop downstream work but still save the three artifacts with empty or partial verified results, blocked branches, unresolved questions, and source anchors.

## Quality Checks

- Confirm separate branches for every core feature and combination.
- Confirm only dialect-verified queries are called executable.
- Confirm evidence is verified and anchored; invent nothing.
- Confirm exactly three artifacts contain unresolved questions and source anchors.
