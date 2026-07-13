---
name: patent-prior-art-search
description: Use when a prior-art search, novelty search, classification search, or comparison evidence task must start from a feature tree and produce traceable patent-search records for Chinese patent work.
---

# Patent Prior Art Search

## Overview

Plan anchored searches around feature combinations.

## Inputs

- `feature-tree-vN.json`

## Workflow

1. Validate fact statuses and feature statuses before searching: accept `confirmed`, `source-backed`, `inferred`, `missing`, or `conflicted` for both and reject unknown values. Only `confirmed` and `source-backed` features may enter formal searches. Treat `core` and `core-combination` as roles, not statuses.
2. Identify core features and feature combinations. Keep their identifiers in every query and result; never search only single features when a core combination exists.
3. Generate keywords, synonyms, IPC/CPC classifications, applicants, inventors, and combined queries for every target. Cover Chinese and useful foreign-language structural, functional, classification, and combination wording. Derive classifications and identities only from supplied or verified seed records. If no verified classification exists, record `query` = `null`, status `blocked-missing-verified-classification`, and a reason. If no verified applicant or inventor exists, record `query` = `null`, status `blocked-missing-identity`, and a reason. Never guess a code or name.
4. Plan against named databases and execute only those available. Bind every complete query to a named database and that database's syntax. Every planned or executed keyword query must name its target database and include complete syntax even when access is unavailable; only blocked classification or identity branches may use null. Record every database, complete query, search date, and screening process, including counts, filters, reviewed candidates, exclusions, access failures, blocked branches, and unexecuted queries. If access is unavailable, record the failure, keep verified results empty, and stop.
5. Verify candidates against accessible bibliographic records and patent text. For every key document, save its publication number, publication date, priority date, title, available applicant or inventor, matched feature IDs, a claim, paragraph, page, or figure anchor, the verbatim quotation, and retrieval source/date.
6. Keep unverified hits as leads only. Do not fabricate a publication number, document, date, result, quotation, or anchor. Do not treat a result without a source anchor as formal evidence.
7. Save exactly the declared artifacts. Report coverage, verified documents, leads, gaps, and stop conditions. Do not give a final novelty or inventive-step conclusion. Do not invoke claim strategy, claim drafting, or specification drafting. Stop after saving the three declared prior-art-search artifacts.

## Outputs

- `search-plan-vN.md`
- `prior-art-vN.json`
- `search-log-vN.json`

## Stop Conditions

Stop when input or status is invalid, a core combination is unsearched, access is unavailable, a key document is unverified, a match lacks an anchor or quotation, or the request exceeds evidence. Save the three artifacts with the plan, verified results, full log, gaps, and stop reason.

Deadline or authority never permits a plausible number or remembered document to become a result without verification and anchored text.

## Quality Checks

- Cover every core feature and combination; log database syntax, dates, screening, and blocked branches.
- Require verified bibliographic data, exact anchors, and quotations; invent nothing.
- Emit exactly three artifacts and stop before legal conclusions or downstream drafting.
