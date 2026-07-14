---
name: cn-specification-drafting
description: Use when a Chinese patent specification, abstract, embodiments, drawing descriptions, drawing plans, or support for approved claims must be drafted from current claim and source-backed technical facts for an invention patent or utility model.
---

# Chinese Specification Drafting

Draft the Chinese specification stage after an approved claim set and before quality review. This Skill covers invention patents and utility models in mechanical/hardware and software/AI domains without importing a domain pack. It emits exactly three artifacts in either ready or blocked mode.

## Inputs

- `claims-vN.md`
- `claim-feature-map-vN.json`
- `technical-facts-vN.json`

`claim-set` approval is a required current workflow-state gate, not a file artifact. Approval must be a value that exists now; future, oral, managerial, filename-based, or placeholder approval is not current (promised and back-signed approval is also not current).

## Workflow

1. Apply a value-based eligibility gate before writing any specification text. Verify that current `claim-set` approval actually exists, claims and mapping are current and non-stale, claim dependencies are internally valid, Every claim-feature occurrence has a valid feature identifier and concrete source anchor, and every occurrence is supported by a `confirmed` or `source-backed` technical fact. Reject missing inputs, unknown statuses, stale versions, mismatches, conflicts, or unsupported occurrences. Do not treat a filename, expected field, role label, placeholder anchor, future, oral, managerial, or back-signed approval as proof.
2. Preserve the approved claim set exactly. Do not silently broaden, narrow, rewrite, omit, or add claim features. If a support gap requires a claim change, stop and report the gap; do not repair the claim in this Skill.
3. In ready mode, draft `specification-vN.md` with status and input versions; technical field; anchored background; invention content (technical problem, technical solution, and beneficial effects); drawing description; detailed embodiments; terminology/claim-support checks; unresolved questions; and source anchors. Write only material traceable to the claims, claim-feature mapping, or qualified technical facts. Background statements require an anchor or a clearly identified cited prior-art fact.
4. Draft the technical solution and detailed embodiments only from `confirmed` or `source-backed` facts. Keep every approved claim feature and its supported relationships in consistent terminology. Every material embodiment statement and beneficial effect must cite a concrete source anchor. Never infer an effect from plausibility. Unconfirmed material may appear only as an explicit unresolved question or evidence gap.
   Do not invent embodiments, alternatives, components, relationships, parameters, effects, drawings, reference numerals, algorithms, data flows, or operating conditions.
5. Draft `abstract-vN.md` as a concise factual abstract of the disclosed technical solution and main use. Keep the abstract body within 300 Chinese characters and exclude unsupported advantages or promotional wording. Include status, unresolved questions, and source anchors in the artifact.
6. Draft `drawing-plan-vN.json` with status, planned figures, figure type/purpose, supported claim features, source anchors, and a reference-numeral table only when supported by inputs. Create no unsupported view, component, flow step, module, or numeral. When support is absent, record the gap instead. Include unresolved questions and source anchors.
7. In blocked mode, still create exactly the three declared outputs. `specification-vN.md` must explicitly state `no specification text` and contain no sample, skeletal, placeholder, or substantive specification prose. `abstract-vN.md` must explicitly state `no abstract text` and contain no sample, skeletal, placeholder, or substantive abstract prose. `drawing-plan-vN.json` must have blocked status, zero planned figures, zero invented reference numerals, structured approval/freshness/support/evidence gaps, unresolved questions, and source anchors.
8. Make all three outputs self-contained. Record explicit empty values when no unresolved questions or source anchors remain. Stop after these three outputs; do not invoke quality review or document export.

## Drafting Eligibility Contract

| condition | rule | decision |
|---|---|---|
| `approval_state` | current claim-set approval exists; future, oral, managerial, filename-based, placeholder, or back-signed approval is not current | `required` |
| `claim_freshness` | claims-vN.md is current/non-stale and matches the approved claim set | `required` |
| `mapping_freshness` | claim-feature-map-vN.json is current/non-stale and matches claims | `required` |
| `dependency_validity` | all claim dependencies are internally valid and every occurrence has a valid feature_id and concrete source_anchor | `required` |
| `feature_support` | each claim-feature occurrence is supported by a confirmed or source-backed technical fact | `required` |

Feature-tree or claim presence alone is not factual support. Do not promote `inferred`, `missing`, or `conflicted` facts into final drafting text. A conflicting source blocks the affected statement. A requested claim modification, unsupported effect, invented embodiment/alternative, drawing, or numeral is a stop condition.

## Safety Invariants

| invariant | decision |
|---|---|
| `claim_set_rewrite` | `forbidden` |
| `unsupported_fact_promotion` | `forbidden` |
| `invented_embodiment_or_drawing` | `forbidden` |
| `blocked_placeholder_text` | `forbidden` |
| `quality_review_or_export` | `forbidden` |

## Outputs

- `specification-vN.md`
- `abstract-vN.md`
- `drawing-plan-vN.json`

## Ready Output Recipe

`specification-vN.md` must contain the required sections: status/input versions, technical field, background, invention content with technical problem/technical solution/beneficial effects, drawing description, detailed embodiments, terminology/claim-support checks, unresolved questions, and source anchors. Every material sentence and every approved claim feature must be traceable to a concrete source anchor.

`abstract-vN.md` must contain a factual abstract body of at most 300 Chinese characters, plus status, unresolved questions, and source anchors. Do not add an unsupported effect or promotional statement.

`drawing-plan-vN.json` must contain ready status, planned figures, each figure's type and purpose, supported claim features, source anchors, and a reference-numeral table only for supported numerals. Record explicit gaps rather than inventing drawings.

## Blocked Output Recipe

`specification-vN.md` records blocked status, blocking reasons, `no specification text`, next allowed action, unresolved questions, and source anchors, with no sample or placeholder specification prose. `abstract-vN.md` records blocked status, blocking reasons, `no abstract text`, unresolved questions, and source anchors, with no sample or placeholder abstract prose. `drawing-plan-vN.json` records blocked status, zero planned figures, zero invented reference numerals, structured approval/freshness/support/evidence gaps, unresolved questions, and source anchors.

## Stop Conditions

Stop on any missing required input; absent or unverified current `claim-set` approval; stale claims or mapping; invalid dependency; claim/mapping mismatch; a claim feature lacking a valid identifier, concrete anchor, or qualified fact; `inferred`, `missing`, or `conflicted` material proposed as final text; conflicting sources; unsupported effect; invented embodiment, alternative, drawing, or numeral; requested claim modification; or a request to continue to quality review or document export. In every blocked case emit exactly the three declared outputs using the blocked recipe.

## Quality Checks

- Confirm all three inputs exist, versions match, claims and mapping are current/non-stale, dependencies are valid, and current approval is a real workflow value rather than an artifact or promise.
- Confirm every claim-feature occurrence has a valid feature identifier and concrete source anchor and is backed by a `confirmed` or `source-backed` fact. Never promote `inferred`, `missing`, or `conflicted` facts.
- Confirm the approved claim set is preserved without silent rewrite, omission, broadening, narrowing, or addition.
- Confirm background, technical solution, embodiments, effects, drawings, and numerals are each anchored; do not fill gaps with common knowledge or plausible details.
- Confirm the specification has all required sections and consistent terminology; the abstract body is at most 300 Chinese characters and factual.
- Confirm blocked outputs contain literal no-text statements, no skeletal prose, zero planned figures, and zero invented numerals.
- Confirm each artifact is self-contained with unresolved_questions and source_anchors, and delivery contains exactly the three declared outputs.
- Do not invoke quality review or document export.
