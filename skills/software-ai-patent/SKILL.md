---
name: software-ai-patent
description: Use when a core Chinese patent skill is processing a PatentCase whose technical_domain is exactly software-ai and needs reusable software, internet, artificial-intelligence, data-processing, control-method, or computer-implemented invention checks.
---

# Software and AI Patent Domain Pack

Provide conditional software and AI checks to a calling core Skill. Keep the core Skill's evidence gates, workflow boundaries, outputs, and stop conditions controlling.

## Loading Contract

Load `references/checklist.md` only when `PatentCase.technical_domain` is exactly `software-ai`.

Do not load this domain pack when `PatentCase.technical_domain` is missing, `None`, `mechanical-hardware`, or any other value. Do not infer the domain from labels such as AI, platform, algorithm, model, automation, or smart.

## Use by Core Skills

- In invention mining, apply the technical-problem, data-flow, processing-step, training/inference, execution-context, and technical-effect checks.
- In claim strategy and claim drafting, apply the technical-solution gate and the method/device/equipment/storage-medium correspondence checks.
- In specification drafting, apply the end-to-end data-flow, implementation, model, deployment, execution-context, and effect-support checks.
- In quality review, apply every relevant checklist section and treat business-rule, abstract-algorithm, correspondence, support, and subject-matter gaps under the core review contract.

Read only the sections relevant to the calling stage. Do not run a standalone workflow or produce standalone artifacts.

## Boundaries

- Treat the checklist as supplemental domain guidance, never as permission to bypass a core Skill contract.
- Preserve source anchors and fact statuses. Do not manufacture training, inference, hardware, network, control, data, or effect details to make a proposal appear technical.
- Return control to the calling core Skill after applying the requested checks.
