---
name: patent-document-export
description: Use when exporting or finalizing a Chinese patent DOCX package and delivery checklist after final approval, including stale-artifact checks and closed quality issues.
---

# Patent Document Export

Package an approved, current Chinese invention-patent or utility-model application for human review. Export only through the available deterministic path; never draft, repair, file, or deliver externally from this Skill.

## Inputs

- `claims-vN.md`
- `claim-feature-map-vN.json`
- `specification-vN.md`
- `abstract-vN.md`
- `drawing-plan-vN.json`
- `prior-art-vN.json`
- `quality-review-vN.json`

`final-delivery` is a workflow-state approval, not a file artifact. Require its current value to cover all seven current input versions, their provenance dependencies, and the export action.

## Workflow

1. Resolve the exact version `N` requested for export and inspect all seven inputs without changing them.
2. Evaluate every row of the Export Eligibility Contract from actual workspace state and actual file content. Treat an unknown, unavailable, or not-assessable delivery-critical fact as a failed gate.
3. Select exactly one Output Mode Contract row. Never issue duplicate or conflicting ready/blocked decisions.
4. If any gate fails, follow the Blocked Output Recipe and stop. Do not invoke an exporter or create any DOCX representation.
5. If every gate passes, invoke only the designated deterministic exporter with its required template. Do not hand-author or simulate a binary document.
6. Inspect the generated DOCX using the available deterministic verification path. Record only observed results.
7. Follow the Ready Output Recipe and stop after exactly the two outputs.

## Export Eligibility Contract

| gate | actual condition | decision |
| --- | --- | --- |
| `input_set` | all seven inputs exist, are readable, current, non-stale, mutually version-matched, provenance-resolved, and identify the same approved application set | `required` |
| `substantive_text` | claims, specification, and abstract contain substantive final review text, not blocked, no-text, or placeholder artifacts | `required` |
| `quality_review` | the current completed review covers the exact input versions, recommends ready-for-human-review, has zero open critical/high issues, and has no unresolved delivery-blocking support, dependency, subject-matter, unity, or prior-art issue | `required` |
| `final_delivery` | a current final-delivery approval explicitly covers all seven exact versions and the export action; promised, oral, managerial, future, back-signed, placeholder, or version-unspecified approval is invalid | `required` |
| `export_path` | the designated deterministic exporter and required DOCX template are actually available and complete successfully | `required` |

Any failed gate requires blocked mode. Authority, urgency, deadline, or customer pressure cannot convert a failed or unknown gate into ready status.

## Output Mode Contract

| mode | condition | artifacts | count |
| --- | --- | --- | --- |
| `ready` | all eligibility gates pass | application-vN.docx and delivery-checklist-vN.md | `exactly-two` |
| `blocked` | any eligibility gate fails | delivery-checklist-vN.md only; docx_generated: false; literal no DOCX generated | `exactly-one` |

The blocked row is the required exception to the declared two-output ready contract. Never create, attach, encode, simulate, or present a placeholder DOCX as delivered.

## Text Immutability Contract

Preserve claims, specification, and abstract text byte-for-byte as approved. Never repair terminology, numbering, dependency, punctuation, section wording, effects, embodiments, or metadata during export. Do not summarize, broaden, narrow, normalize, translate, or invent application text. If upstream text requires correction, block export and identify the upstream human action instead of editing it.

Exclude internal review findings, prompts, source-anchor tables, unresolved questions, and approval metadata from the patent application body. Include a delivery cover page only when the approved template explicitly requires one outside that body.

## DOCX Verification Contract

Invoke only the designated deterministic DOCX exporter and template. Record their actual identities and availability. Never pretend to create a binary DOCX or substitute another format when the exporter or template is absent or fails.

After successful generation, verify a valid readable DOCX and inspect Chinese text, headings, claim numbering and dependencies, section order, symbols, and abstract without truncation or placeholder text; record actual verification results rather than inferring success. Record a checksum or hash only when the exporter or verification path actually provides one.

## Safety Invariants

| invariant | decision |
| --- | --- |
| `premature_or_unscoped_approval` | `forbidden` |
| `stale_or_version_mismatched_export` | `forbidden` |
| `open_blocking_issue_export` | `forbidden` |
| `not_assessable_as_pass` | `forbidden` |
| `silent_upstream_rewrite` | `forbidden` |
| `blocked_or_placeholder_docx` | `forbidden` |
| `fabricated_exporter_template_or_verification` | `forbidden` |
| `pdf_zip_cover_letter_or_submission_material` | `forbidden` |
| `filing_email_upload_or_external_delivery` | `forbidden` |
| `extra_artifact` | `forbidden` |
| `duplicate_or_conflicting_decision` | `forbidden` |

Apply these invariants regardless of language, synonym, authority, urgency, deadline, customer pressure, or placement. Never submit to CNIPA, email, upload, send externally, create billing or CRM records, or claim filing completion.

## Outputs

- `application-vN.docx`
- `delivery-checklist-vN.md`

Ready mode creates exactly both declared outputs. Blocked mode creates only the checklist and never creates or presents the DOCX.

## Ready Output Recipe

Create `application-vN.docx` only after every eligibility gate passes and the designated exporter completes successfully. Keep approved application text unchanged and use only the available approved template structure.

Create `delivery-checklist-vN.md` with structured fields for:

- export status, all seven current input versions and provenance dependencies;
- readability, stale, version-match, and application-set checks;
- quality-review completion, recommendation, open critical/high counts, and delivery-blocking issue status;
- final-delivery approval ID, status, scope, and currentness;
- exporter and template identity, availability, and actual execution result;
- DOCX filename, generated/readable/verified status, section/content checks, and an actual checksum or hash when provided;
- the statement that human final review is still required;
- the statement that no filing or external submission occurred;
- unresolved questions and source anchors.

Stop after exactly the mode-specific outputs. Do not create any additional format, delivery message, filing material, or operational record.

## Blocked Output Recipe

Create only `delivery-checklist-vN.md`. Include:

- `status: blocked`;
- `docx_generated: false`;
- the literal statement `no DOCX generated`;
- structured approval, freshness, version, review, exporter, and template gaps;
- the next allowed human or upstream action;
- unresolved questions and source anchors.

Do not name a DOCX as created, attach sample application content, include base64 or package bytes, create an empty archive, invent a checksum, or report exporter/template/readability success.

## Stop Conditions

Stop in blocked mode when any of the seven required inputs is missing, unreadable, stale, version-mismatched, internally inconsistent, provenance-unresolved, or non-substantive; when review coverage is absent, stale, incomplete, not ready, or has an open delivery-blocking issue; when current seven-version scoped final approval is absent; or when the deterministic exporter/template is absent or fails.

Stop after producing the allowed mode-specific outputs. Never continue to filing, submission, email, upload, external delivery, archiving, billing, CRM, or another format.

## Quality Checks

- Confirm exactly seven file inputs and treat final-delivery solely as current workflow state.
- Confirm blocked mode has exactly one checklist, `docx_generated: false`, and `no DOCX generated`, with no DOCX placeholder or simulated content.
- Confirm ready mode has exactly one verified DOCX plus exactly one checklist.
- Compare the exported application content against approved source text without silently correcting it.
- Confirm actual exporter/template identity, DOCX readability, required section/content presence, and observed verification results.
- Confirm checklist approval, freshness, version, review, export, human-review, no-filing, unresolved-question, and source-anchor fields.
- Confirm no extra artifact and no filing, submission, email, upload, or external action.
