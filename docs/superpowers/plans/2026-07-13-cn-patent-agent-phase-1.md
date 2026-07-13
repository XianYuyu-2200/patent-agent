# Chinese Patent Agent Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a locally usable Codex patent-production agent with nine core skills, two domain packs, structured case state, evidence traceability, workflow gates, deterministic quality checks, and DOCX export for Chinese invention patents and utility models.

**Architecture:** Package the product as a Codex plugin whose orchestrator reads and writes a versioned case workspace. Markdown skills perform judgment-heavy patent work; Python modules enforce case schemas, workflow transitions, evidence rules, consistency checks, and document export. Phase 2, the Web case-management system, starts only after Phase 1 passes real-case quality acceptance and receives its own specification and plan.

**Tech Stack:** Codex plugin/skills, Python 3.12, Pydantic 2, Typer, python-docx, PyYAML, pytest, JSON and Markdown case artifacts.

## Global Constraints

- Support Chinese invention patents and utility models only.
- Support mechanical/equipment/structure/electronic-hardware and software/internet/AI/control-method cases only.
- Never convert `inferred`, `missing`, or `conflicted` content into confirmed technical facts.
- Keep original customer materials read-only and retain source anchors for extracted facts.
- Require human approval at technical-solution, claim-set, and final-delivery gates.
- Re-run claim dependency, specification support, and terminology checks after material claim changes.
- Do not implement CNIPA submission, office-action response, chemistry/biomedicine, PCT/US/EP rules, billing, CRM, or a Web UI in Phase 1.
- Use TDD for Python behavior and fixture-based forward tests for skills.
- Commit after every task.

---

## Planned File Structure

```text
codex-patent/
├── .codex-plugin/
│   └── plugin.json
├── agents/
│   └── cn-patent-orchestrator.md
├── skills/
│   ├── cn-patent-case-intake/
│   ├── patent-invention-mining/
│   ├── patent-prior-art-search/
│   ├── patentability-analysis/
│   ├── cn-claim-strategy/
│   ├── cn-claim-drafting/
│   ├── cn-specification-drafting/
│   ├── cn-patent-quality-review/
│   ├── patent-document-export/
│   ├── mechanical-hardware-patent/
│   └── software-ai-patent/
├── src/codex_patent/
│   ├── __init__.py
│   ├── cli.py
│   ├── models.py
│   ├── repository.py
│   ├── workflow.py
│   ├── validation.py
│   └── export_docx.py
├── templates/
│   └── cn-patent-application.docx
├── tests/
│   ├── fixtures/
│   │   ├── mechanical_case/
│   │   └── software_case/
│   ├── test_models.py
│   ├── test_repository.py
│   ├── test_workflow.py
│   ├── test_validation.py
│   ├── test_export_docx.py
│   └── test_plugin_contract.py
├── pyproject.toml
└── .gitignore
```

The skill folders contain only `SKILL.md`, `agents/openai.yaml`, and directly needed `references/`, `scripts/`, or `assets/` resources. They do not contain auxiliary README or changelog files.

### Task 1: Scaffold the Plugin and Python Test Harness

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `pyproject.toml`
- Create: `src/codex_patent/__init__.py`
- Create: `src/codex_patent/cli.py`
- Create: `tests/test_plugin_contract.py`
- Create: `.gitignore`

**Interfaces:**
- Consumes: approved design specification.
- Produces: installable Python package, `codex-patent` CLI entry point, and discoverable Codex plugin metadata.

- [ ] **Step 1: Write the failing plugin contract test**

```python
import json
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_plugin_manifest_and_skill_roots_exist():
    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "codex-patent"
    assert manifest["version"] == "0.1.0"
    assert manifest["skills"] == "./skills/"
    assert manifest["author"]["name"] == "XianYuyu-2200"
    assert manifest["interface"]["displayName"] == "中国专利撰写 Agent"
    assert manifest["interface"]["category"] == "Productivity"
```

- [ ] **Step 2: Run the test and verify the scaffold is absent**

Run: `python -m pytest tests/test_plugin_contract.py -v`

Expected: FAIL with `FileNotFoundError` for `.codex-plugin/plugin.json`.

- [ ] **Step 3: Generate the plugin scaffold, then create the project metadata**

Run the official plugin scaffold into a temporary parent directory so the existing repository remains the plugin root:

```text
python C:/Users/xiany/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py codex-patent --path .plugin-scaffold --with-skills
```

Copy the generated `.codex-plugin/plugin.json` structure into the repository root, then remove `.plugin-scaffold`. Preserve the scaffold's supported schema and use these exact values:

Create `.codex-plugin/plugin.json`:

```json
{
  "name": "codex-patent",
  "version": "0.1.0",
  "description": "Chinese patent production workflow for invention patents and utility models.",
  "author": {
    "name": "XianYuyu-2200",
    "url": "https://github.com/XianYuyu-2200"
  },
  "repository": "https://github.com/XianYuyu-2200/patent-agent",
  "skills": "./skills/",
  "interface": {
    "displayName": "中国专利撰写 Agent",
    "shortDescription": "面向中国发明专利和实用新型的专业撰写工作流",
    "longDescription": "整理客户材料，完成发明挖掘、检索、保护策略、权利要求、说明书、质量审查和文档导出。",
    "developerName": "XianYuyu-2200",
    "category": "Productivity",
    "capabilities": ["Write", "Analysis"],
    "defaultPrompt": [
      "整理当前客户材料并建立专利案件。",
      "分析当前案件的发明点并生成追问清单。",
      "根据已确认方案起草中国专利申请文件。"
    ]
  }
}
```

Create `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"

[project]
name = "codex-patent"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "pydantic>=2.8,<3",
  "typer>=0.12,<1",
  "python-docx>=1.1,<2",
  "PyYAML>=6,<7"
]

[project.optional-dependencies]
test = ["pytest>=8.2,<9"]

[project.scripts]
codex-patent = "codex_patent.cli:app"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

Create `src/codex_patent/__init__.py`:

```python
__version__ = "0.1.0"
```

Create `src/codex_patent/cli.py`:

```python
import typer


app = typer.Typer(no_args_is_help=True)


@app.command()
def version() -> None:
    from codex_patent import __version__
    typer.echo(__version__)
```

Create `.gitignore`:

```gitignore
.venv/
__pycache__/
.pytest_cache/
*.pyc
dist/
build/
.superpowers/
cases/
```

- [ ] **Step 4: Install and verify the scaffold**

Run: `python -m pip install -e ".[test]"`

Expected: installation completes without dependency resolution errors.

Run: `python -m pytest tests/test_plugin_contract.py -v`

Expected: PASS.

Run: `python C:/Users/xiany/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`

Expected: validator exits 0.

Run: `codex-patent version`

Expected: prints `0.1.0`.

- [ ] **Step 5: Commit**

```bash
git add .codex-plugin/plugin.json pyproject.toml src/codex_patent tests/test_plugin_contract.py .gitignore
git commit -m "build: scaffold Codex patent plugin"
```

### Task 2: Define the Versioned Case Schema

**Files:**
- Create: `src/codex_patent/models.py`
- Create: `tests/test_models.py`

**Interfaces:**
- Consumes: plain JSON-compatible case data.
- Produces: `PatentCase`, `TechnicalFact`, `SourceAnchor`, `ArtifactRef`, `ReviewIssue`, `FactStatus`, and `CaseStage` types.

- [ ] **Step 1: Write failing schema tests**

```python
import pytest
from pydantic import ValidationError

from codex_patent.models import FactStatus, PatentCase, TechnicalFact


def test_case_defaults_to_intake_stage():
    case = PatentCase(case_id="CN-2026-0001", title="折叠支架")
    assert case.stage.value == "intake"
    assert case.schema_version == "1.0"


def test_unconfirmed_fact_cannot_be_marked_final():
    with pytest.raises(ValidationError):
        TechnicalFact(
            fact_id="F-001",
            statement="支架采用钛合金",
            status=FactStatus.INFERRED,
            final_text_allowed=True,
        )
```

- [ ] **Step 2: Run the tests and verify failure**

Run: `python -m pytest tests/test_models.py -v`

Expected: FAIL because `codex_patent.models` does not exist.

- [ ] **Step 3: Implement the schema**

```python
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class FactStatus(StrEnum):
    CONFIRMED = "confirmed"
    SOURCE_BACKED = "source-backed"
    INFERRED = "inferred"
    MISSING = "missing"
    CONFLICTED = "conflicted"


class CaseStage(StrEnum):
    INTAKE = "intake"
    MINING = "mining"
    SEARCH = "search"
    STRATEGY = "strategy"
    CLAIMS = "claims"
    DRAFTING = "drafting"
    REVIEW = "review"
    DELIVERY = "delivery"


class SourceAnchor(BaseModel):
    source_id: str
    locator: str
    quote: str | None = None


class TechnicalFact(BaseModel):
    fact_id: str
    statement: str
    status: FactStatus
    anchors: list[SourceAnchor] = Field(default_factory=list)
    final_text_allowed: bool = False

    @model_validator(mode="after")
    def prevent_unconfirmed_final_text(self):
        if self.final_text_allowed and self.status not in {
            FactStatus.CONFIRMED,
            FactStatus.SOURCE_BACKED,
        }:
            raise ValueError("unconfirmed facts cannot enter final text")
        return self


class ArtifactRef(BaseModel):
    artifact_type: str
    version: int = Field(ge=1)
    path: str
    stale: bool = False


class ReviewIssue(BaseModel):
    issue_id: str
    severity: Literal["low", "medium", "high"]
    message: str
    closed: bool = False


class PatentCase(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    case_id: str
    title: str
    stage: CaseStage = CaseStage.INTAKE
    technical_domain: Literal["mechanical-hardware", "software-ai"] | None = None
    facts: list[TechnicalFact] = Field(default_factory=list)
    artifacts: list[ArtifactRef] = Field(default_factory=list)
    issues: list[ReviewIssue] = Field(default_factory=list)
    approvals: set[Literal["technical-solution", "claim-set", "final-delivery"]] = Field(default_factory=set)
```

- [ ] **Step 4: Run schema tests**

Run: `python -m pytest tests/test_models.py -v`

Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add src/codex_patent/models.py tests/test_models.py
git commit -m "feat: define patent case schema"
```

### Task 3: Implement the Case Repository and Immutable Source Store

**Files:**
- Create: `src/codex_patent/repository.py`
- Create: `tests/test_repository.py`
- Modify: `src/codex_patent/cli.py`

**Interfaces:**
- Consumes: `PatentCase`, a workspace path, and customer source files.
- Produces: `CaseRepository.create()`, `load()`, `save()`, `add_source()`, and CLI command `codex-patent case-create`.

- [ ] **Step 1: Write failing repository tests**

```python
from pathlib import Path

from codex_patent.models import PatentCase
from codex_patent.repository import CaseRepository


def test_repository_round_trip_and_source_copy(tmp_path: Path):
    repo = CaseRepository(tmp_path)
    case = PatentCase(case_id="CN-2026-0001", title="折叠支架")
    repo.create(case)
    source = tmp_path / "客户说明.txt"
    source.write_text("支架通过转轴折叠", encoding="utf-8")
    stored = repo.add_source(case.case_id, source)

    loaded = repo.load(case.case_id)
    assert loaded == case
    assert stored.read_text(encoding="utf-8") == "支架通过转轴折叠"
    assert stored.parent.name == "source-materials"
```

- [ ] **Step 2: Run the test and verify failure**

Run: `python -m pytest tests/test_repository.py -v`

Expected: FAIL because `CaseRepository` does not exist.

- [ ] **Step 3: Implement repository behavior**

```python
import hashlib
import json
import shutil
from pathlib import Path

from codex_patent.models import PatentCase


class CaseRepository:
    def __init__(self, root: Path):
        self.root = root

    def case_dir(self, case_id: str) -> Path:
        return self.root / case_id

    def create(self, case: PatentCase) -> Path:
        case_dir = self.case_dir(case.case_id)
        for name in ("source-materials", "technical-facts", "prior-art", "drafts", "review-log"):
            (case_dir / name).mkdir(parents=True, exist_ok=True)
        self.save(case)
        return case_dir

    def save(self, case: PatentCase) -> None:
        path = self.case_dir(case.case_id) / "case.json"
        path.write_text(case.model_dump_json(indent=2), encoding="utf-8")

    def load(self, case_id: str) -> PatentCase:
        data = json.loads((self.case_dir(case_id) / "case.json").read_text(encoding="utf-8"))
        return PatentCase.model_validate(data)

    def add_source(self, case_id: str, source: Path) -> Path:
        digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
        destination = self.case_dir(case_id) / "source-materials" / f"{digest}-{source.name}"
        shutil.copy2(source, destination)
        destination.chmod(0o444)
        return destination
```

Add to `src/codex_patent/cli.py`:

```python
from pathlib import Path

from codex_patent.models import PatentCase
from codex_patent.repository import CaseRepository


@app.command("case-create")
def case_create(case_id: str, title: str, workspace: Path = Path("cases")) -> None:
    repo = CaseRepository(workspace)
    repo.create(PatentCase(case_id=case_id, title=title))
    typer.echo(str(repo.case_dir(case_id)))
```

- [ ] **Step 4: Run repository and CLI tests**

Run: `python -m pytest tests/test_repository.py tests/test_models.py -v`

Expected: all tests pass.

Run: `codex-patent case-create CN-TEST-001 "测试案件" --workspace .tmp-cases`

Expected: prints `.tmp-cases/CN-TEST-001` and creates `case.json` plus five artifact directories.

- [ ] **Step 5: Commit**

```bash
git add src/codex_patent/repository.py src/codex_patent/cli.py tests/test_repository.py
git commit -m "feat: add versioned case workspace"
```

### Task 4: Enforce Workflow Gates and Downstream Invalidation

**Files:**
- Create: `src/codex_patent/workflow.py`
- Create: `tests/test_workflow.py`

**Interfaces:**
- Consumes: `PatentCase`, target `CaseStage`, and artifact changes.
- Produces: `advance_case(case, target)` and `invalidate_after_claim_change(case)`.

- [ ] **Step 1: Write failing workflow tests**

```python
import pytest

from codex_patent.models import ArtifactRef, CaseStage, PatentCase
from codex_patent.workflow import WorkflowError, advance_case, invalidate_after_claim_change


def test_claims_require_technical_solution_approval():
    case = PatentCase(case_id="C1", title="支架", stage=CaseStage.STRATEGY)
    with pytest.raises(WorkflowError, match="technical-solution"):
        advance_case(case, CaseStage.CLAIMS)


def test_claim_change_invalidates_drafting_and_review():
    case = PatentCase(
        case_id="C1",
        title="支架",
        artifacts=[
            ArtifactRef(artifact_type="claims", version=2, path="drafts/claims-v2.md"),
            ArtifactRef(artifact_type="specification", version=1, path="drafts/spec-v1.md"),
            ArtifactRef(artifact_type="quality-review", version=1, path="review-log/review-v1.json"),
        ],
    )
    invalidate_after_claim_change(case)
    assert [a.stale for a in case.artifacts] == [False, True, True]
```

- [ ] **Step 2: Verify failure**

Run: `python -m pytest tests/test_workflow.py -v`

Expected: FAIL because the workflow module does not exist.

- [ ] **Step 3: Implement transition rules**

```python
from codex_patent.models import CaseStage, PatentCase


class WorkflowError(ValueError):
    pass


REQUIRED_APPROVAL = {
    CaseStage.CLAIMS: "technical-solution",
    CaseStage.DRAFTING: "claim-set",
    CaseStage.DELIVERY: "final-delivery",
}


def advance_case(case: PatentCase, target: CaseStage) -> PatentCase:
    approval = REQUIRED_APPROVAL.get(target)
    if approval and approval not in case.approvals:
        raise WorkflowError(f"missing approval: {approval}")
    if target == CaseStage.DELIVERY and any(issue.severity == "high" and not issue.closed for issue in case.issues):
        raise WorkflowError("open high-severity review issues")
    case.stage = target
    return case


def invalidate_after_claim_change(case: PatentCase) -> PatentCase:
    for artifact in case.artifacts:
        if artifact.artifact_type in {"specification", "quality-review", "docx"}:
            artifact.stale = True
    return case
```

- [ ] **Step 4: Run workflow tests**

Run: `python -m pytest tests/test_workflow.py -v`

Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add src/codex_patent/workflow.py tests/test_workflow.py
git commit -m "feat: enforce patent workflow gates"
```

### Task 5: Create the Orchestrator and Nine Core Skill Contracts

**Files:**
- Create: `agents/cn-patent-orchestrator.md`
- Create: `skills/*/SKILL.md` for all nine core skills
- Create: `skills/*/agents/openai.yaml` for all nine core skills
- Modify: `tests/test_plugin_contract.py`

**Interfaces:**
- Consumes: case workspace paths and structured artifacts defined in Tasks 2–4.
- Produces: a discoverable orchestrator and skills whose contracts name exact required inputs, outputs, refusal conditions, and approval gates.

- [ ] **Step 1: Extend the contract test to enumerate required skills**

```python
import yaml


REQUIRED_SKILLS = {
    "cn-patent-case-intake",
    "patent-invention-mining",
    "patent-prior-art-search",
    "patentability-analysis",
    "cn-claim-strategy",
    "cn-claim-drafting",
    "cn-specification-drafting",
    "cn-patent-quality-review",
    "patent-document-export",
}


def test_all_core_skills_have_valid_frontmatter():
    found = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    assert REQUIRED_SKILLS <= found
    for name in REQUIRED_SKILLS:
        text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        _, frontmatter, body = text.split("---", 2)
        metadata = yaml.safe_load(frontmatter)
        assert metadata["name"] == name
        assert metadata["description"]
        assert "Inputs" in body
        assert "Outputs" in body
        assert "Stop Conditions" in body
```

- [ ] **Step 2: Run the contract test and verify missing skills**

Run: `python -m pytest tests/test_plugin_contract.py -v`

Expected: FAIL showing the nine missing skill names.

- [ ] **Step 3: Create the orchestrator contract**

The orchestrator file must contain these executable rules:

```markdown
# Chinese Patent Orchestrator

Operate only on a named case workspace. Read `case.json` before every stage.
Call exactly one production skill at a time and save its output before proceeding.
Never promote inferred, missing, or conflicted facts into final drafting inputs.
Require approvals named `technical-solution`, `claim-set`, and `final-delivery` at their workflow gates.
After a material claim change, mark specification, review, and DOCX artifacts stale.
Stop and ask for human action when a skill reports a stop condition.
```

- [ ] **Step 4: Create every core `SKILL.md` with an explicit artifact contract**

Use the following exact contracts. Every file contains `Inputs`, `Workflow`, `Outputs`, `Stop Conditions`, and `Quality Checks` headings. Every workflow begins by validating fact statuses and ends by saving unresolved questions and source anchors.

| Skill | Description and trigger | Required inputs | Outputs |
| --- | --- | --- | --- |
| `cn-patent-case-intake` | Organize mixed customer materials into a Chinese patent case; trigger for new cases, material intake, transcription intake, and completeness checks. | customer files and case identity | `intake-vN.json`, `material-index-vN.json`, `questions-vN.md` |
| `patent-invention-mining` | Extract technical problems, means, effects, variants, and interview questions; trigger after intake or when drafting lacks technical facts. | `intake-vN.json`, source anchors | `technical-facts-vN.json`, `feature-tree-vN.json`, `interview-vN.md` |
| `patent-prior-art-search` | Design and record prior-art searches for Chinese patent drafting; trigger for novelty search, classification search, and comparison evidence. | `feature-tree-vN.json` | `search-plan-vN.md`, `prior-art-vN.json`, `search-log-vN.json` |
| `patentability-analysis` | Assess novelty, inventive step, protectable contribution, and filing risk; trigger after search results are available. | `feature-tree-vN.json`, `prior-art-vN.json` | `feature-matrix-vN.json`, `patentability-vN.md` |
| `cn-claim-strategy` | Design Chinese invention or utility-model protection themes and claim hierarchy; trigger before claims are drafted or when prior art changes strategy. | `feature-tree-vN.json`, `patentability-vN.md` | `protection-strategy-vN.md` |
| `cn-claim-drafting` | Draft and revise Chinese claims with feature-source mapping; trigger after strategy approval or for claim revisions. | `protection-strategy-vN.md`, `feature-tree-vN.json`, `technical-solution` approval | `claims-vN.md`, `claim-feature-map-vN.json` |
| `cn-specification-drafting` | Draft the Chinese specification, abstract, and drawing instructions from approved claims and facts. | `claims-vN.md`, `claim-feature-map-vN.json`, `technical-facts-vN.json`, `claim-set` approval | `specification-vN.md`, `abstract-vN.md`, `drawing-plan-vN.json` |
| `cn-patent-quality-review` | Independently attack claim clarity, support, consistency, unity, subject matter, and design-around weaknesses. | current claims, specification, abstract, drawing plan, prior art | `quality-review-vN.json`, `support-matrix-vN.json` |
| `patent-document-export` | Generate a reviewable Chinese patent DOCX package; trigger only after quality issues are closed and final approval exists. | non-stale claims, specification, abstract, review report, `final-delivery` approval | `application-vN.docx`, `delivery-checklist-vN.md` |

Every skill stops on missing required inputs, conflicting source material, an unanchored conclusion, absent required approval, or an attempt to use `inferred`, `missing`, or `conflicted` facts as final text. `cn-claim-drafting` additionally stops when a claimed feature lacks a feature-tree identifier. `patent-document-export` additionally stops on stale artifacts or open high-severity issues.

- [ ] **Step 5: Generate `agents/openai.yaml` metadata and validate every skill**

Run the skill-creator generator for each folder using these exact display names: `专利案件受理`, `发明挖掘`, `现有技术检索`, `可专利性分析`, `权利要求策略`, `权利要求撰写`, `说明书撰写`, `专利质量审查`, and `专利文件导出`. Set each `short_description` to the corresponding table responsibility and set `default_prompt` to `请处理当前案件并生成本阶段规定的结构化产物。`.

Then run `quick_validate.py` against each of the nine skill directories.

Expected: all validators exit 0 and no generated metadata contains placeholder text.

- [ ] **Step 6: Run the plugin contract tests**

Run: `python -m pytest tests/test_plugin_contract.py -v`

Expected: all tests pass.

- [ ] **Step 7: Commit**

```bash
git add agents skills tests/test_plugin_contract.py
git commit -m "feat: add patent orchestrator and core skills"
```

### Task 6: Add Mechanical-Hardware and Software-AI Domain Packs

**Files:**
- Create: `skills/mechanical-hardware-patent/SKILL.md`
- Create: `skills/mechanical-hardware-patent/references/checklist.md`
- Create: `skills/software-ai-patent/SKILL.md`
- Create: `skills/software-ai-patent/references/checklist.md`
- Modify: `tests/test_plugin_contract.py`

**Interfaces:**
- Consumes: `PatentCase.technical_domain` and core skill requests.
- Produces: conditional domain rules loaded by invention mining, claim strategy, drafting, and quality review.

- [ ] **Step 1: Write failing domain-pack contract tests**

```python
def test_domain_packs_define_required_checks():
    mechanical = (ROOT / "skills/mechanical-hardware-patent/references/checklist.md").read_text(encoding="utf-8")
    software = (ROOT / "skills/software-ai-patent/references/checklist.md").read_text(encoding="utf-8")
    for phrase in ("部件关系", "连接方式", "附图标号", "实用新型"):
        assert phrase in mechanical
    for phrase in ("技术问题", "数据处理", "方法、装置、设备和存储介质", "业务规则"):
        assert phrase in software
```

- [ ] **Step 2: Run and verify failure**

Run: `python -m pytest tests/test_plugin_contract.py::test_domain_packs_define_required_checks -v`

Expected: FAIL with missing checklist files.

- [ ] **Step 3: Create domain packs**

The mechanical checklist must require explicit modeling of components, connection/location/motion relationships, alternative structures, drawing views, reference numerals, and utility-model eligibility.

The software checklist must require explicit modeling of data inputs/outputs, processing steps, model training/inference, hardware or controlled-object context, technical effect, and method/device/equipment/storage-medium claim correspondence. It must stop when the proposal contains only business rules or abstract algorithms.

Both `SKILL.md` files must instruct core skills to read their checklist only when `technical_domain` matches.

- [ ] **Step 4: Validate and test**

Run: `python -m pytest tests/test_plugin_contract.py -v`

Expected: all tests pass.

Run `quick_validate.py` for both domain skill directories.

Expected: both validators exit 0.

- [ ] **Step 5: Commit**

```bash
git add skills/mechanical-hardware-patent skills/software-ai-patent tests/test_plugin_contract.py
git commit -m "feat: add patent domain packs"
```

### Task 7: Implement Deterministic Quality Validation

**Files:**
- Create: `src/codex_patent/validation.py`
- Create: `tests/test_validation.py`
- Create: `tests/fixtures/mechanical_case/claims.json`
- Create: `tests/fixtures/mechanical_case/specification.json`

**Interfaces:**
- Consumes: structured claims, specification sections, terminology, figures, and fact statuses.
- Produces: `ValidationReport` with high/medium/low issues and checks for final-delivery eligibility.

- [ ] **Step 1: Write failing validation tests**

```python
from codex_patent.validation import validate_claim_support


def test_unsupported_claim_feature_is_high_severity():
    report = validate_claim_support(
        claims=[{"claim": 1, "features": ["F-001", "F-999"]}],
        supported_fact_ids={"F-001"},
    )
    assert report.issues[0].severity == "high"
    assert "F-999" in report.issues[0].message


def test_all_supported_features_pass():
    report = validate_claim_support(
        claims=[{"claim": 1, "features": ["F-001"]}],
        supported_fact_ids={"F-001"},
    )
    assert report.issues == []
```

- [ ] **Step 2: Verify failure**

Run: `python -m pytest tests/test_validation.py -v`

Expected: FAIL because validation functions do not exist.

- [ ] **Step 3: Implement claim-support validation**

```python
from pydantic import BaseModel, Field

from codex_patent.models import ReviewIssue


class ValidationReport(BaseModel):
    issues: list[ReviewIssue] = Field(default_factory=list)


def validate_claim_support(claims: list[dict], supported_fact_ids: set[str]) -> ValidationReport:
    issues: list[ReviewIssue] = []
    for claim in claims:
        for feature_id in claim["features"]:
            if feature_id not in supported_fact_ids:
                issues.append(
                    ReviewIssue(
                        issue_id=f"unsupported-{claim['claim']}-{feature_id}",
                        severity="high",
                        message=f"claim {claim['claim']} feature {feature_id} lacks specification support",
                    )
                )
    return ValidationReport(issues=issues)
```

- [ ] **Step 4: Add focused tests and implementations for remaining deterministic rules**

Add one failing test and minimal implementation for each rule:

- invalid claim dependency or reference number;
- inconsistent terminology across claims/specification/abstract;
- duplicate or missing drawing reference numerals;
- final text containing facts with forbidden statuses;
- stale specification, review, or DOCX artifacts;
- open high-severity review issues.

Each validator returns `ValidationReport`; each issue identifier is stable and derived from the affected artifact and feature identifier.

- [ ] **Step 5: Run validation tests**

Run: `python -m pytest tests/test_validation.py -v`

Expected: all validation tests pass.

- [ ] **Step 6: Commit**

```bash
git add src/codex_patent/validation.py tests/test_validation.py tests/fixtures/mechanical_case
git commit -m "feat: add deterministic patent quality checks"
```

### Task 8: Generate the Chinese Patent DOCX Package

**Files:**
- Create: `src/codex_patent/export_docx.py`
- Create: `tests/test_export_docx.py`
- Create: `templates/cn-patent-application.docx`
- Modify: `src/codex_patent/cli.py`

**Interfaces:**
- Consumes: approved, non-stale claims/specification/abstract artifacts and validation report.
- Produces: `export_application(case_dir, output_path)` and CLI command `codex-patent export`.

- [ ] **Step 1: Write the failing export test**

```python
from pathlib import Path

from docx import Document

from codex_patent.export_docx import export_application


def test_export_contains_required_sections(tmp_path: Path):
    output = tmp_path / "application.docx"
    export_application(
        title="折叠支架",
        claims=["1. 一种折叠支架，其特征在于……"],
        sections={
            "技术领域": "本申请涉及支架技术领域。",
            "背景技术": "现有支架存在……",
            "发明内容": "本申请提供……",
            "附图说明": "图1为……",
            "具体实施方式": "如图1所示……",
            "摘要": "本申请公开……",
        },
        output_path=output,
    )
    text = "\n".join(p.text for p in Document(output).paragraphs)
    for heading in ("权利要求书", "技术领域", "背景技术", "发明内容", "附图说明", "具体实施方式", "摘要"):
        assert heading in text
```

- [ ] **Step 2: Verify failure**

Run: `python -m pytest tests/test_export_docx.py -v`

Expected: FAIL because `export_application` does not exist.

- [ ] **Step 3: Implement the minimal exporter**

```python
from pathlib import Path

from docx import Document


SECTION_ORDER = ["技术领域", "背景技术", "发明内容", "附图说明", "具体实施方式", "摘要"]


def export_application(title: str, claims: list[str], sections: dict[str, str], output_path: Path) -> Path:
    document = Document()
    document.add_heading(title, level=0)
    document.add_heading("权利要求书", level=1)
    for claim in claims:
        document.add_paragraph(claim)
    for heading in SECTION_ORDER:
        document.add_heading(heading, level=1)
        document.add_paragraph(sections[heading])
    document.save(output_path)
    return output_path
```

- [ ] **Step 4: Add delivery guards**

Add tests proving export refuses when final approval is absent, validation contains open high-severity issues, or an input artifact is stale. Implement these checks before opening the DOCX template.

- [ ] **Step 5: Add the approved Chinese DOCX template**

Create `templates/cn-patent-application.docx` with styles for title, first-level headings, body paragraphs, claims, figure captions, page margins, Chinese fonts, paragraph spacing, and page numbering. Update the exporter to load this template rather than creating a blank document.

- [ ] **Step 6: Verify the generated document**

Run: `python -m pytest tests/test_export_docx.py -v`

Expected: all tests pass.

Open the generated DOCX in Word or LibreOffice and verify headings, Chinese font rendering, page breaks, claim numbering, and no clipped content.

- [ ] **Step 7: Commit**

```bash
git add src/codex_patent/export_docx.py src/codex_patent/cli.py tests/test_export_docx.py templates/cn-patent-application.docx
git commit -m "feat: export Chinese patent application DOCX"
```

### Task 9: Add Golden-Case End-to-End Regression

**Files:**
- Create: `tests/fixtures/mechanical_case/case.json`
- Create: `tests/fixtures/mechanical_case/expected-review.json`
- Create: `tests/fixtures/software_case/case.json`
- Create: `tests/fixtures/software_case/expected-review.json`
- Create: `tests/test_end_to_end.py`
- Modify: `agents/cn-patent-orchestrator.md`

**Interfaces:**
- Consumes: one anonymized mechanical case and one anonymized software/AI case.
- Produces: repeatable end-to-end acceptance checks for workflow gates, prohibited facts, support coverage, and export eligibility.

- [ ] **Step 1: Create anonymized golden fixtures**

The mechanical fixture must include a component relationship, an alternative structure, a drawing reference table, and one intentionally unsupported feature.

The software fixture must include input data, processing steps, hardware or controlled-object context, technical effect, and one intentionally business-only statement.

Expected review files must name the unsupported feature and business-only statement as high-severity issues.

- [ ] **Step 2: Write the end-to-end tests**

```python
import json
from pathlib import Path

from codex_patent.models import PatentCase
from codex_patent.validation import validate_claim_support


FIXTURES = Path(__file__).parent / "fixtures"


def test_mechanical_case_blocks_unsupported_feature():
    data = json.loads((FIXTURES / "mechanical_case/case.json").read_text(encoding="utf-8"))
    case = PatentCase.model_validate(data["case"])
    report = validate_claim_support(data["claims"], set(data["supported_fact_ids"]))
    assert case.technical_domain == "mechanical-hardware"
    assert any(issue.severity == "high" for issue in report.issues)


def test_software_case_flags_business_only_statement():
    expected = json.loads((FIXTURES / "software_case/expected-review.json").read_text(encoding="utf-8"))
    assert any(issue["rule"] == "business-only" and issue["severity"] == "high" for issue in expected)
```

- [ ] **Step 3: Run the complete suite**

Run: `python -m pytest -v`

Expected: all tests pass.

- [ ] **Step 4: Forward-test the orchestrator on both fixtures**

Start two fresh Codex tasks with only the plugin path and one fixture request each. Do not provide expected answers. Confirm that the mechanical case asks about the unsupported feature and that the software case refuses to treat the business-only statement as a technical contribution.

Record only anonymized prompts, emitted artifacts, detected failures, and resulting Skill changes in the corresponding fixture directories.

- [ ] **Step 5: Commit**

```bash
git add tests/fixtures tests/test_end_to_end.py agents/cn-patent-orchestrator.md skills
git commit -m "test: add patent golden-case regression"
```

### Task 10: Phase 1 Release Verification and Phase 2 Entry Gate

**Files:**
- Create: `tests/test_release.py`
- Create: `docs/phase-1-acceptance.md`

**Interfaces:**
- Consumes: completed plugin, full test suite, skill validation results, and real-case evaluation metrics.
- Produces: a release decision for Phase 1 and an explicit go/no-go gate for the future Web system specification.

- [ ] **Step 1: Add release integrity tests**

```python
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_release_contains_required_components():
    assert (ROOT / ".codex-plugin/plugin.json").exists()
    assert (ROOT / "agents/cn-patent-orchestrator.md").exists()
    assert len(list((ROOT / "skills").glob("*/SKILL.md"))) == 11
    assert (ROOT / "templates/cn-patent-application.docx").exists()
```

- [ ] **Step 2: Run all automated verification**

Run: `python -m pytest -v`

Expected: all tests pass.

Run `quick_validate.py` against all eleven skill folders.

Expected: all validators exit 0.

Run: `codex-patent version`

Expected: prints `0.1.0`.

- [ ] **Step 3: Complete real-case acceptance**

Use at least three anonymized historical or live-with-permission cases: one mechanical invention, one utility model, and one software/AI invention. Record:

- number of incorrectly stated technical facts;
- number of major claim rewrites;
- support and terminology defects found at final review;
- elapsed time from materials to reviewable draft;
- number of customer clarification rounds;
- number of open high-severity issues at attempted delivery.

Phase 1 passes only when no fabricated technical fact enters a final draft, no high-severity issue remains at delivery, and the human reviewer considers every claim set usable as a professional drafting baseline.

- [ ] **Step 4: Write the acceptance record**

Create `docs/phase-1-acceptance.md` containing the plugin version, test commands and results, anonymized case identifiers, metric table, unresolved limitations, and a signed go/no-go decision.

The Phase 2 Web specification may begin only after a `GO` decision. Phase 2 must separately design authentication, customer and case management, file storage, background jobs, audit logs, permissions, deployment, backup, and data isolation.

- [ ] **Step 5: Commit**

```bash
git add tests/test_release.py docs/phase-1-acceptance.md
git commit -m "chore: verify patent agent phase one"
```

## Final Verification

Run:

```text
python -m pytest -v
codex-patent version
git status --short
```

Expected:

- all tests pass;
- CLI prints `0.1.0`;
- all eleven skills pass `quick_validate.py`;
- both golden-case forward tests detect their seeded high-risk defects;
- a valid approved case exports a readable DOCX;
- an invalid, stale, or unapproved case cannot export;
- Git working tree is clean.
