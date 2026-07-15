import json
import re
from pathlib import Path

import pytest

from codex_patent.models import CaseStage, PatentCase, ReviewIssue
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


def _emitted_forward_artifacts(case_name: str) -> list[dict]:
    record = (FIXTURES / case_name / "forward-test.md").read_text(
        encoding="utf-8"
    )
    blocks = re.findall(
        r"## (?:Baseline|Forward) emitted artifact\n\n```json\n(.*?)\n```",
        record,
        flags=re.DOTALL,
    )
    assert len(blocks) == 2
    return [json.loads(block) for block in blocks]


def _fact_and_anchor(data: dict, fact_id: str, source_anchor: str) -> tuple[dict, dict]:
    fact = next(
        fact for fact in data["case"]["facts"] if fact["fact_id"] == fact_id
    )
    source_id, locator = source_anchor.split("#", maxsplit=1)
    anchor = next(
        anchor
        for anchor in fact["anchors"]
        if anchor["source_id"] == source_id and anchor["locator"] == locator
    )
    return fact, anchor


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


def test_mechanical_relationship_fields_match_their_cited_fact_and_anchor():
    data = _fixture("mechanical_case", "case.json")
    relationship = next(
        relationship
        for relationship in data["component_relationships"]
        if relationship["relationship_id"] == "M-R002"
    )
    fact, anchor = _fact_and_anchor(
        data, relationship["fact_id"], relationship["source_anchor"]
    )

    assert relationship["subject"] == "弹性定位件"
    assert relationship["relation"] == "进入并与定位槽配合"
    assert relationship["object"] == "定位槽"
    assert relationship["subject"] in fact["statement"]
    assert relationship["subject"] in anchor["quote"]
    assert relationship["object"] in fact["statement"]
    assert relationship["object"] in anchor["quote"]


def test_software_golden_case_keeps_business_rule_out_of_technical_contribution():
    data = _fixture("software_case", "case.json")
    expected = _fixture("software_case", "expected-review.json")
    case = PatentCase.model_validate(data["case"])

    assert case.technical_domain == "software-ai"
    assert data["input_data"]
    assert data["processing_steps"]
    assert data["execution_context"]["hardware"]
    assert data["execution_context"]["control_command"]
    assert data["execution_context"]["unresolved_controlled_object"]
    assert data["technical_effects"]

    business_issue = next(
        issue for issue in expected["issues"] if issue["rule"] == "business-only"
    )
    assert business_issue["severity"] == "high"
    assert business_issue["fact_id"] == data["business_only_statement"]["fact_id"]
    assert business_issue["statement"] == data["business_only_statement"]["statement"]
    assert business_issue["fact_id"] not in data["technical_contribution_fact_ids"]
    assert expected["blocks_export"] is True

    effect_fact = next(
        fact for fact in data["case"]["facts"] if fact["fact_id"] == "S-F004"
    )
    assert effect_fact["status"] == "source-backed"
    assert effect_fact["final_text_allowed"] is True
    assert "停机" not in effect_fact["statement"]
    assert all("停机" not in anchor.get("quote", "") for anchor in effect_fact["anchors"])


def test_software_execution_context_only_finalizes_the_cited_control_command():
    data = _fixture("software_case", "case.json")
    context = data["execution_context"]
    command = context["control_command"]
    unresolved = context["unresolved_controlled_object"]
    fact, anchor = _fact_and_anchor(
        data, command["fact_id"], command["source_anchor"]
    )

    assert "controlled_object" not in context
    assert command == {
        "action": "向电机驱动器发送降速指令",
        "fact_id": "S-F003",
        "source_anchor": "SRC-S-02#控制链段落1",
        "final_text_allowed": True,
    }
    assert command["action"] in anchor["quote"]
    assert "向驱动器发送降速指令" in fact["statement"]
    assert unresolved["object"] is None
    assert unresolved["feedback"] is None
    assert unresolved["status"] == "unresolved"
    assert unresolved["final_text_allowed"] is False


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

    blocked_delivery = case.model_copy(deep=True)
    blocked_delivery.stage = CaseStage.REVIEW
    blocked_delivery.issues = [
        ReviewIssue(
            issue_id="golden-high",
            severity="high",
            message="seeded unsupported feature",
        )
    ]
    with pytest.raises(WorkflowError, match="open high-severity"):
        advance_case(blocked_delivery, CaseStage.DELIVERY)


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


def test_golden_case_forward_artifacts_match_stable_findings_without_oracle_leakage():
    expected_stable = {
        "mechanical_case": ("unsupported-feature", "high", "M-F999"),
        "software_case": ("business-only", "high", "S-B001"),
    }
    for case_name, (rule, severity, affected_id) in expected_stable.items():
        artifacts = _emitted_forward_artifacts(case_name)
        for artifact in artifacts:
            encoded = json.dumps(artifact, ensure_ascii=False)
            assert "expected-review.json" not in encoded
            assert "MECH-HIGH-001" not in encoded
            assert "SOFT-HIGH-001" not in encoded
            candidates = list(artifact.get("issues", []))
            if artifact.get("business_only"):
                candidates.append(
                    {
                        **artifact["business_only"],
                        "rule": artifact["business_only"].get("classification"),
                    }
                )
            issue = next(
                issue
                for issue in candidates
                if issue.get("rule") == rule
                or issue.get("fact_id") == affected_id
                or issue.get("feature_id") == affected_id
            )
            assert issue.get("rule") == rule
            assert issue["severity"] == severity
            assert issue.get("fact_id", issue.get("feature_id")) == affected_id
            assert issue.get("blocks_export") is True or artifact.get(
                "delivery_export", {}
            ).get("allowed") is False
            if case_name == "mechanical_case":
                assert issue["fact_status"] == "inferred"
                assert issue["source_anchors"] == []
                assert issue["final_text_allowed"] is False
            else:
                assert issue["fact_status"] == "source-backed"
                assert issue["source_anchors"] == ["SRC-S-03#运营说明段落1"]
                assert "停机" not in encoded
                assert "受电机驱动的旋转设备" not in encoded
                assert "旋转设备控制" not in encoded
                if assessment := artifact.get("technical_solution_assessment"):
                    assert assessment["conclusion"] == (
                        "振动传感器采样—窗口化和频域判定—向电机驱动器发送降速指令—"
                        "缩短超阈值振动持续时间形成来源可追溯的技术链。"
                    )
                    assert artifact["unresolved_context"] == {
                        "fact_id": "S-F003",
                        "supported_statement": "向电机驱动器发送降速指令",
                        "unresolved_fields": ["controlled_object", "feedback"],
                        "status": "unresolved",
                        "final_text_allowed": False,
                    }
