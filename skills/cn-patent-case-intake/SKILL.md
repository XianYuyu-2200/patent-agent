---
name: cn-patent-case-intake
description: Use when opening a new Chinese patent case from mixed customer materials, including chats, transcriptions, images, documents, code, or prior disclosures, and checking intake completeness, conflicts, public-disclosure risk, or uncertain inventor and applicant identity.
---

# Chinese Patent Case Intake

## Overview

Create a traceable intake record without turning uncertain customer material into patent facts. Keep intake separate from invention mining and drafting.

## Inputs

- A named case identity or enough information to assign a provisional case identifier.
- Customer-provided originals such as chats, documents, audio or transcriptions, images, archives, source code, product records, and disclosure statements.
- Known provider, receipt channel, receipt time, author or speaker, material date, inventor, applicant, and filing deadline information, including explicit unknowns.

## Workflow

1. Treat every original as read-only. Preserve the received file, message, archive, or recording; record a stable material identifier, hash when available, original name, provider, channel, receipt time, author or speaker, material date, and whether the item is original or derived.
2. Record a source anchor for every extracted fact. Use a page, message timestamp, audio time range, image region, archive path, or code file and line range. Label a transcription as a transcription and retain its confidence or uncertainty.
3. Assess each intake fact as `confirmed`, `source-backed`, `inferred`, `missing`, or `conflicted`. Never merge conflicting statements or select a convenient version. Preserve each statement with its own anchor and convert the conflict into a question.
4. Mark uncertain inventor identity, applicant identity, and public-disclosure dates as `missing` or `conflicted`. Record disclosure venue, date, audience access, confidentiality limits, and supporting evidence when known; otherwise flag public-disclosure risk without promising novelty.
5. Do not infer details from a blurred or ambiguous image. Keep enhanced or annotated copies separate from the original and label them as derived. Do not execute unknown code; index it statically and ask for provenance, repository, branch, commit history, authorship, dates, dependencies, and licences.
6. Check whether every received item is indexed, every extracted fact has an anchor, all conflicts and missing identity or disclosure data are visible, and urgent filing or confidentiality risks are prioritized.
7. Save only the three declared intake artifacts with unresolved questions and source anchors. Do not invoke invention mining or drafting. Stop after saving the three intake artifacts.

## Outputs

- `intake-vN.json`
- `material-index-vN.json`
- `questions-vN.md`

Use `intake-vN.json` for provisional case identity, intake status, completeness, conflicts, missing facts, and disclosure or identity risks. Use `material-index-vN.json` for the immutable material register and source anchors. Use `questions-vN.md` for prioritized customer questions and the evidence needed to close each item.

## Stop Conditions

Stop downstream progression when the case cannot be identified, a received original cannot be preserved or indexed, a material lacks usable provenance, a conclusion lacks a source anchor, source statements conflict, identity or disclosure facts remain `inferred`, `missing`, or `conflicted`, an image is too ambiguous, or code provenance is unknown. Record the condition in the three intake artifacts; do not resolve it by guessing.

Always stop at the intake boundary after producing the declared artifacts. A request to “start writing” does not authorize invention mining, claim drafting, specification drafting, or any additional production artifact.

## Quality Checks

- Confirm that every received material has exactly one immutable index entry and that derived copies point back to the original.
- Confirm that every extracted statement retains its own source anchor and status.
- Confirm that conflicts remain separate, uncertain identities and disclosure dates remain visibly unresolved, blurred images add no inferred structure, and unknown code was not executed.
- Confirm that the output set contains exactly the three declared artifacts and no technical-mining or drafting work product.
