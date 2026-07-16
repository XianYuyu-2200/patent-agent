# Phase 1 Acceptance Record

Date: 2026-07-15 (Asia/Shanghai)

Plugin: `codex-patent`

Version: `0.1.0`

## Decision summary

- Automated release readiness: **PASS**.
- Commercial Phase 1 release: **NO-GO**.
- Phase 2 Web specification entry: **NO-GO**.

The repository contains no authorized real-case acceptance records for the required set of one mechanical invention, one utility model, and one software/AI invention. Synthetic golden fixtures and skill forward tests are automated regression evidence; they are not substitutes for historical or live-with-permission cases, measured drafting outcomes, or a professional human usability judgment. No case identifier or metric is invented in this record.

## Automated verification

All commands were run from the repository root with `PYTHONUTF8=1`.

| Verification | Exact command | Result |
| --- | --- | --- |
| Release-test RED | `python -m pytest tests/test_release.py -v` before this record existed | Expected RED: `1 failed, 2 passed`; failure was the missing `docs/phase-1-acceptance.md` |
| Full suite after acceptance record | `python -m pytest -v` | PASS: `492 passed in 10.55s` |
| Golden forward and export acceptance | `python -m pytest tests/test_end_to_end.py tests/test_export_docx.py -v` | PASS: `118 passed in 3.66s` |
| Twelve skill validators | PowerShell loop shown below | PASS: 12 of 12 printed `Skill is valid!` |
| Plugin validator | `python C:\Users\xiany\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .` | PASS: `Plugin validation passed` |
| CLI version | `codex-patent version` | PASS: `0.1.0` |

Exact twelve-skill validation command:

```powershell
$quick='C:\Users\xiany\.codex\skills\.system\skill-creator\scripts\quick_validate.py'
Get-ChildItem skills -Directory | Where-Object { Test-Path ($_.FullName + '\SKILL.md') } | Sort-Object Name | ForEach-Object { python $quick $_.FullName }
```

The focused acceptance run confirms that both golden-case forward records detect their seeded high-risk defects, a valid approved case exports a DOCX, and invalid, stale, unapproved, placeholder-bearing, or open-high-severity cases are refused. These are synthetic acceptance checks only.

## Real-case acceptance evidence

A read-only search of tracked repository materials found no permission-backed real-case evaluation records. Therefore anonymized identifiers and measured values are unavailable rather than inferred.

| Required case category | Anonymized case identifier | Incorrect technical facts | Major claim rewrites | Final-review support and terminology defects | Materials-to-reviewable-draft time | Customer clarification rounds | Open high-severity issues at attempted delivery | Human baseline judgment |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| Mechanical invention | Not available - no authorized case record | Not measured | Not measured | Not measured | Not measured | Not measured | Not measured | Not performed |
| Utility model | Not available - no authorized case record | Not measured | Not measured | Not measured | Not measured | Not measured | Not measured | Not performed |
| Software/AI invention | Not available - no authorized case record | Not measured | Not measured | Not measured | Not measured | Not measured | Not measured | Not performed |

The Phase 1 real-case pass criteria cannot be evaluated: there is no evidence that zero fabricated technical facts entered each final draft, zero high-severity issues remained at each attempted delivery, or a human patent professional considered every claim set usable as a professional drafting baseline.

## Controls that remain mandatory

- Keep source provenance and anchors for extracted technical facts; never fabricate an anchor or technical fact.
- Never promote `inferred`, `missing`, or `conflicted` content into final drafting inputs.
- Preserve all three human gates: `technical-solution`, `claim-set`, and `final-delivery`.
- Re-run claim dependency, specification support, and terminology checks after material claim changes.
- Do not treat automated tests, synthetic fixtures, or an agent decision as permission for external delivery or filing.

## Unresolved limitations and required actions

Before changing either NO-GO decision to GO:

1. Obtain documented authorization to use and anonymize at least three historical or live cases covering the three required categories.
2. Run each case through the complete Phase 1 workflow while retaining source anchors, artifact versions, timestamps, review findings, and the three human approvals.
3. Record all six required metrics without estimates or reconstructed values.
4. Have a qualified human patent reviewer confirm for every case that no fabricated technical fact entered the final draft, no high-severity issue remained at attempted delivery, and the claim set is usable as a professional drafting baseline.
5. Append the anonymized identifiers, measured metrics, reviewer identity or approved signing role, review date, and decision evidence to this record; rerun the automated verification and issue a signed GO/NO-GO decision.

If Phase 2 later receives a GO decision, its separate specification must design authentication, customer and case management, file storage, background jobs, audit logs, permissions, deployment, backup, and data isolation. None of those Web-system concerns is authorized by this Phase 1 record.

## Signed decision

Decision: **NO-GO - commercial Phase 1 release and Phase 2 entry are blocked pending authorized real-case acceptance.**

Recorded by: Codex Task 10 verification implementer (automated evidence recorder; not a substitute for the required human patent reviewer or product decision authority)

Recorded on: 2026-07-15

Human/product-owner GO signature: Not available
