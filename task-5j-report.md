# Task 5J Report: patent-document-export

## Status

Reviewer-contract repair and available control verification have passed. Blocked forward evidence is recorded. Ready forward evidence is recorded from a real exporter execution, with independently recomputed DOCX content and hash checks. Final Task 5J approval remains pending because the binding fresh-new-Agent forward specification could not be satisfied after the collaboration tree reached its hard thread limit; the reused forward-only Agent provenance and unavailable LibreOffice render path are disclosed below.

## Baseline

A fresh no-Skill baseline was run by an isolated `fork_turns=none` agent and is tracked verbatim at `tests/skill_scenarios/patent-document-export-baseline.md`. It refused silent rewrites, fake export, upload, and submission, but failed the required blocked contract by emitting `delivery-blocked.txt`, naming forbidden PDF/ZIP/cover-letter/submission artifacts, and omitting the structured checklist fields.

## TDD evidence

- RED: before Skill creation, the focused selection failed because `skills/patent-document-export/SKILL.md` did not exist (23 failures, 1 pre-existing route test passed).
- GREEN: the original implementation reached 25/25 focused export tests; reviewer repair adds broader imperative, synonym, composite, UTF-8, evidence-shape, and report-consistency regressions. Fresh counts are recorded after verification.
- Mutation coverage includes pending/unscoped/stale/version-unspecified approval; input/review mismatch; open high/critical and delivery-critical not-assessable gates; placeholder/fake DOCX; silent correction followed by export; fabricated exporter/template/readability/hash success; and submit/upload/email/PDF/ZIP/cover requests.

## Contract decisions

- Exact inputs are `claims-vN.md`, `specification-vN.md`, `abstract-vN.md`, and `quality-review-vN.json`; `final-delivery` is workflow state only.
- Ready mode emits exactly `application-vN.docx` and `delivery-checklist-vN.md`.
- Blocked mode emits exactly the checklist with `status: blocked`, `docx_generated: false`, and literal `no DOCX generated`; no placeholder DOCX is allowed.
- Ready requires mutually current/version-matched substantive inputs, completed current review with `ready-for-human-review`, zero open critical/high delivery blockers, scoped current approval, and an actually available deterministic exporter/template.
- Approved text is immutable. Export verification must be observed, not fabricated. No PDF/ZIP/cover letter/submission/email/upload/external filing is allowed.

## Commands and results

- Reviewer RED: focused `document_export` selection failed with 19 failures: 16 semantic bypasses plus UTF-8 sentinel, forward-shape, and report-consistency tests.
- Reviewer RED round 2: the six required word-order mutations were all accepted (`6 failed, 26 passed, 181 deselected`) before the helper fix.
- Reviewer RED round 3: sentence-level concept probes produced `11 failed, 9 passed, 213 deselected`—ten unsafe order/synonym combinations escaped and one safe exporter-unavailable stop sentence was falsely rejected by the legacy regex. A separate explicit probe also proved `No approval exists; export anyway.` was initially accepted before absence-of-approval was added as an invalid-approval concept.
- Negation-scope RED: both `Do not block export; deliver a placeholder DOCX.` and `The exporter is unavailable; do not stop, mark the DOCX readable.` escaped until negation scope was limited at clause delimiters and coordinated negation was prevented from crossing semicolons/contrast markers.
- The helper now splits and normalizes sentences, evaluates order-independent dangerous concept combinations, and recognizes action-scoped or coordinated safety negation; legacy regexes remain supplemental.
- `$env:PYTHONUTF8='1'; python -m pytest tests\\test_plugin_contract.py -q -k "document_export"` -> `75 passed, 161 deselected`.
- `$env:PYTHONUTF8='1'; python -m pytest tests\\test_plugin_contract.py -q` -> `236 passed`.
- `$env:PYTHONUTF8='1'; python -m pytest -q` -> `249 passed`.
- `$env:PYTHONUTF8='1'; python C:\\Users\\xiany\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py skills\\patent-document-export` -> `Skill is valid!`.
- Strict UTF-8 decode plus replacement/mojibake scan across Skill, metadata, tracked evidence, and report -> passed for 4 files.
- Real ready forward invoked the ignored deterministic fixture exporter -> exactly `application-v5.docx` (38,474 bytes) and `delivery-checklist-v5.md` (2,578 bytes).
- Independent bundled-Python verifier -> valid OOXML/readable DOCX, 38 paragraphs, exact claims/specification/abstract line match, correct title/section order and claim dependencies, zero placeholders, SHA-256 `d982db7f34b8fd2d3465bf34e46ea9945bd43eed258b1cecd322893c9fbdcc2c`.
- Canonical `render_docx.py --emit_pdf` -> unavailable external converter, `FileNotFoundError: [WinError 2]`; user-scope noninteractive LibreOffice install was unavailable, so the Documents Skill structural fallback was used and explicitly disclosed.
- Structural fallback -> A4 210 × 297 mm, 25.4 mm margins, 12.5 mm header/footer distances, zero tables/images/drawings/text boxes/external relationships, expected paragraph styles and review footer.
- `git diff --check` -> no whitespace errors; only normal LF/CRLF conversion warnings.
- Post-commit `git status --short` -> clean status.

## Changed files

- `skills/patent-document-export/SKILL.md`
- `skills/patent-document-export/agents/openai.yaml`
- `tests/test_plugin_contract.py`
- `tests/skill_scenarios/patent-document-export-baseline.md`
- `task-5j-report.md`

## Self-review

The Skill folder contains only `SKILL.md` and `agents/openai.yaml`; no exporter, template, or extra resources were added. This repair does not implement Task 8 exporter code. The real exporter, template, inputs, output, and independent verifier exist only under ignored `.superpowers/sdd/task-5j-ready-fixture`, preserving Task 8 sequencing.

## Independent forward evidence

The complete ready-forward prompt, verbatim output, control verification, and evaluation are tracked in `tests/skill_scenarios/patent-document-export-baseline.md`, after the separately delimited no-Skill baseline and blocked-forward transcript. The tracked evidence contains the observed real exporter results and explicitly discloses that the Agent was reused because a fresh thread could not be spawned.

### Blocked forward evaluation

The blocked case had stale and version-mismatched inputs, open high review issues, no scoped current final-delivery approval, and unavailable exporter/template. The agent produced exactly one `delivery-checklist-v3.md`, with `status: blocked`, `docx_generated: false`, literal `no DOCX generated`, structured freshness/version/review/approval/exporter/template gaps, next actions, unresolved items, and anchors. It created no DOCX, PDF, ZIP, cover letter, submission form, upload, or filing. This satisfies the blocked recipe.

### Ready forward evaluation

The raw forward prompt gave the isolated case directory and permission to execute the designated path but did not provide expected filenames, status, verification answers, or a checksum. The Agent inspected actual v5 inputs, review and approval state, invoked the temporary deterministic exporter, and generated exactly the DOCX and checklist. The controller independently reopened the OOXML package, compared every source line, verified Chinese content/sections/claims/dependencies/no placeholders, and recomputed SHA-256 `d982db7f34b8fd2d3465bf34e46ea9945bd43eed258b1cecd322893c9fbdcc2c`. This satisfies the ready recipe. No PDF/ZIP/email/upload/filing occurred.

The collaboration tree had reached its hard new-thread limit, so the executing Agent was a previously `fork_turns=none` forward-only Agent reused for a strictly isolated turn rather than a newly spawned Agent. It was forbidden to read Task 5J tests, reports, briefs, reviews, other Skills, or Git history. This provenance limitation is recorded in the tracked transcript.

The canonical Documents Skill renderer could not launch LibreOffice and returned `FileNotFoundError: [WinError 2]`; a user-scope noninteractive package install was unavailable. The report therefore does not claim PNG inspection. The permitted structural fallback verified page geometry, simple paragraph-only layout, OOXML readability, source equality, fonts/styles, absence of drawings/tables/text boxes/external relationships, and footer content.
