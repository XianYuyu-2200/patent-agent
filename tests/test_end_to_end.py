import json
from pathlib import Path

import pytest

from codex_patent.models import CaseStage, PatentCase
from codex_patent.validation import (
    validate_claim_support,
    validate_drawing_reference_numerals,
    validate_final_fact_statuses,
)
from codex_patent.workflow import WorkflowError, advance_case


ROOT = Path(__file__).parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


def _fixture(case_name: str, file_name: str) -> dict:
    return json.loads(
        (FIXTURES / case_name / file_name).read_text(encoding="utf-8")
    )


def test_mechanical_golden_case_blocks_unsupported_feature_and_export():
    data = _fixture("mechanical_case", "case.json")
    expected = _fixture("mechanical_case", "expected-review.json")
    case = PatentCase.model_validate(data["case"])

    assert case.technical_domain == "mechanical-hardware"
    assert data["component_relationships"]
    assert data["alternative_structures"]
    assert data["drawing_reference_table"]

    drawing_report = validate_drawing_reference_numerals(
        data["drawing_reference_table"], data["referenced_numerals"]
    )
    assert drawing_report.issues == []

    support_report = validate_claim_support(
        data["claims"], set(data["supported_fact_ids"])
    )
    unsupported = next(
        issue
        for issue in expected["issues"]
        if issue["rule"] == "unsupported-feature"
    )
    assert unsupported["severity"] == "high"
    assert any(
        issue.issue_id
        == f"unsupported-{unsupported['claim']}-{unsupported['feature_id']}"
        and issue.severity == "high"
        for issue in support_report.issues
    )

    fact_report = validate_final_fact_statuses(
        data["case"]["facts"], data["final_fact_ids"]
    )
    assert any(
        unsupported["feature_id"] in issue.issue_id
        and issue.severity == "high"
        for issue in fact_report.issues
    )
    assert support_report.eligible_for_final_delivery is False
    assert expected["blocks_export"] is True

    blocked_delivery = case.model_copy(deep=True)
    blocked_delivery.stage = CaseStage.REVIEW
    blocked_delivery.issues = support_report.issues
    with pytest.raises(WorkflowError, match="open high-severity"):
        advance_case(blocked_delivery, CaseStage.DELIVERY)


def test_software_golden_case_keeps_business_rule_out_of_technical_contribution():
    data = _fixture("software_case", "case.json")
    expected = _fixture("software_case", "expected-review.json")
    case = PatentCase.model_validate(data["case"])

    assert case.technical_domain == "software-ai"
    assert data["input_data"]
    assert data["processing_steps"]
    assert data["execution_context"]["hardware"]
    assert data["execution_context"]["controlled_object"]
    assert data["technical_effects"]

    business_issue = next(
        issue for issue in expected["issues"] if issue["rule"] == "business-only"
    )
    assert business_issue["severity"] == "high"
    assert business_issue["fact_id"] == data["business_only_statement"]["fact_id"]
    assert business_issue["statement"] == data["business_only_statement"]["statement"]
    assert business_issue["fact_id"] not in data["technical_contribution_fact_ids"]
    assert expected["blocks_export"] is True


def test_golden_cases_preserve_technical_solution_claim_set_and_delivery_gates():
    data = _fixture("mechanical_case", "case.json")
    case = PatentCase.model_validate(data["case"])

    with pytest.raises(WorkflowError, match="technical-solution"):
        advance_case(case.model_copy(deep=True), CaseStage.SEARCH)

    claims_case = case.model_copy(deep=True)
    claims_case.stage = CaseStage.CLAIMS
    claims_case.approvals = ["technical-solution"]
    with pytest.raises(WorkflowError, match="claim-set"):
        advance_case(claims_case, CaseStage.DRAFTING)

    orchestrator = (
        ROOT / "skills" / "cn-patent-orchestrator" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for gate in ("technical-solution", "claim-set", "final-delivery"):
        assert gate in orchestrator


def test_orchestrator_defines_independent_golden_case_acceptance_protocol():
    orchestrator = (
        ROOT / "skills" / "cn-patent-orchestrator" / "SKILL.md"
    ).read_text(encoding="utf-8")

    for phrase in (
        "## Golden-Case Regression",
        "Do not read `expected-review.json` before saving the independent review output.",
        "unsupported-feature",
        "business-only",
        "source anchors",
        "blocks export",
    ):
        assert phrase in orchestrator


def test_golden_case_forward_records_are_anonymized_and_complete():
    for case_name in ("mechanical_case", "software_case"):
        record = (FIXTURES / case_name / "forward-test.md").read_text(
            encoding="utf-8"
        )
        for heading in (
            "## Baseline prompt",
            "## Baseline emitted artifact",
            "## Baseline result",
            "## Forward prompt",
            "## Forward emitted artifact",
            "## Forward result",
            "## Resulting Skill change",
        ):
            assert heading in record
        assert "expected-review.json" in record
        assert "No customer, applicant, inventor, filing, dataset, or deployment identity" in record
