---
name: mechanical-hardware-patent
description: Use when a core Chinese patent skill is processing a PatentCase whose technical_domain is exactly mechanical-hardware and needs reusable mechanical, equipment, structural, electronic-hardware, drawing, or utility-model checks.
---

# Mechanical and Hardware Patent Domain Pack

Provide conditional mechanical and hardware checks to a calling core Skill. Keep the core Skill's evidence gates, workflow boundaries, outputs, and stop conditions controlling.

## Loading Contract

Load `references/checklist.md` only when `PatentCase.technical_domain` is exactly `mechanical-hardware`.

Do not load this domain pack when `PatentCase.technical_domain` is missing, `None`, `software-ai`, or any other value. Do not infer the domain from product names, drawings, customer labels, or technical content.

## Use by Core Skills

- In invention mining, apply the component, relationship, alternative-structure, and drawing-evidence checks.
- In claim strategy and claim drafting, apply the structural-subject, necessary-relationship, fallback-structure, and utility-model checks.
- In specification drafting, apply the drawing-view, reference-numeral, terminology, and embodiment-support checks.
- In quality review, apply every relevant checklist section and record unsupported or inconsistent structure as findings under the core review contract.

Read only the sections relevant to the calling stage. Do not run a standalone workflow or produce standalone artifacts.

## Boundaries

- Treat the checklist as supplemental domain guidance, never as permission to bypass a core Skill contract.
- Preserve source anchors and fact statuses. Convert unsupported structures, relationships, views, numerals, and alternatives into gaps or questions instead of inventing them.
- Return control to the calling core Skill after applying the requested checks.
