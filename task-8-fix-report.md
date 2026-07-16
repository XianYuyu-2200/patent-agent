# Task 8 Fix Report: Persisted Export Gate and Wheel Template

## Status

All Task 8 Critical and Important review findings are fixed.

Implementation commit: `e9909c0` (`fix: bind DOCX export to persisted case state`).

## Fixed Findings

### 1. Export now fails closed from persisted case state

The public API is now workspace-bound:

```python
export_application(
    case_dir: Path,
    output_path: Path,
    *,
    final_approval: bool,
    template_path: Path | None = None,
) -> Path
```

The exporter loads `case.json` through the existing `CaseRepository` and derives the authoritative title, `final-delivery` approval, review issues, artifact references, versions, stale state, and application text from the named case workspace.

Export refuses before opening the DOCX template when:

- explicit `final_approval` is not the actual boolean `True`;
- persisted `final-delivery` approval is absent;
- persisted case issues or the current quality-review artifact contain an open high-severity issue;
- claims, specification, abstract, or quality-review references are missing or stale;
- more than one current artifact exists for a required type;
- the four required artifacts do not share one version;
- a referenced path is absolute, escapes the case directory, or names a different artifact type/version;
- a referenced artifact file is missing, unreadable, empty, or the quality-review file is invalid;
- an existing DOCX artifact is stale;
- the persisted case ID does not match the case-directory identity;
- required specification sections or substantive application text are absent.

Historical stale required-artifact references may remain in `case.json`, but exactly one non-stale current reference must exist for each required type. Caller-supplied title, claims, sections, validation reports, and artifact lists are no longer accepted.

### 2. Approval is strict at API and CLI boundaries

The API uses an exact runtime boolean check. The CLI request model uses Pydantic `StrictBool`, so JSON such as `"final_approval": "yes"` is rejected rather than coerced.

The CLI command shape remains:

```text
codex-patent export INPUT_PACKAGE OUTPUT_PATH [--template TEMPLATE]
```

Its UTF-8 JSON request now contains only:

```json
{
  "case_dir": ".../cases/CN-2026-0001",
  "final_approval": true
}
```

Unknown content or guard fields are forbidden.

### 3. The default template is installed in the wheel

Hatch now force-includes:

```text
templates/cn-patent-application.docx
-> codex_patent/templates/cn-patent-application.docx
```

Installed exports resolve the default through `importlib.resources`; editable/source-checkout execution retains the tracked root-template fallback.

## TDD Evidence

### RED

The initial adversarial run produced six expected failures:

- non-boolean `"yes"` reached template opening;
- `artifacts=[]` was accepted;
- missing quality-review was accepted;
- stale claims was accepted;
- stale abstract was accepted;
- the built wheel lacked `codex_patent/templates/cn-patent-application.docx`.

The final workspace-bound regression set then failed with the old API/CLI (`33 failed, 4 passed`), proving the persisted-workspace interface and guards did not yet exist.

Additional RED/GREEN cycles covered the preserved stale-DOCX guard and an open high issue stored in the quality-review artifact itself.

### GREEN

- Focused export and packaging tests: `39 passed`.
- Full suite: `409 passed`.
- Compilation: `python -m compileall -q src tests` exited 0.
- Version smoke: `codex-patent version` printed `0.1.0`.
- Diff whitespace: `git diff --check` exited 0.

## Wheel and Isolated Install Evidence

Fresh final build:

- wheel: `codex_patent-0.1.0-py3-none-any.whl`;
- size: `48,019` bytes;
- SHA-256: `a1ca8074a57198276158f9da0c3ba091ded476c79ce3aaeb9b91865d89300ace`;
- required wheel member present: `codex_patent/templates/cn-patent-application.docx`.

The wheel was installed with `--target` outside the source package import path. The smoke confirmed:

- `codex_patent` imported from the isolated install target;
- `TEMPLATE_PATH` resolved to the installed package template;
- a persisted approved case exported with no template override;
- the installed output was readable by `python-docx`;
- the template sentinel and required headings were present;
- generated DOCX size was `38,047` bytes.

## Word Render Evidence

A fresh final DOCX sample was generated (`38,191` bytes). A new Word COM PDF render attempt was stopped after the 120-second command timeout. Only the hidden `WINWORD` process started by this task was terminated; the user's pre-existing visible Word session was left running.

No rendering/template construction code changed in this fix. The retained Task 8 Microsoft Word 2024 evidence therefore remains applicable: four rendered pages, correct Chinese glyphs, centered page numbers, intended claims/specification/abstract breaks, and no clipping, overlap, replacement glyph, or margin overflow.

## Files Changed in the Implementation Commit

- `pyproject.toml`
- `src/codex_patent/cli.py`
- `src/codex_patent/export_docx.py`
- `tests/test_export_docx.py`
- `tests/test_packaging.py`
