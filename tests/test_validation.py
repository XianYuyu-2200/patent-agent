import hashlib
import json
import posixpath
from pathlib import Path

from codex_patent.models import ArtifactRef, FactStatus, ReviewIssue, TechnicalFact
from codex_patent.validation import (
    validate_artifact_freshness,
    validate_claim_dependencies,
    validate_claim_support,
    validate_drawing_reference_numerals,
    validate_final_fact_statuses,
    validate_open_high_issues,
    validate_terminology_consistency,
)


FIXTURES = Path(__file__).parent / "fixtures"


def _stale_issue_id(artifact_type: str, version: int, path: str) -> str:
    normalized = posixpath.normpath(path.replace("\\", "/")).casefold()
    identity = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]
    return f"stale-artifact-{artifact_type}-v{version}-{identity}"


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


def test_claim_dependencies_reject_self_future_and_missing_references():
    report = validate_claim_dependencies(
        claims=[
            {"claim": 1, "references": []},
            {"claim": 2, "references": [2]},
            {"claim": 3, "references": [4]},
            {"claim": 4, "references": [1]},
            {"claim": 5, "references": [99]},
        ]
    )

    assert [issue.issue_id for issue in report.issues] == [
        "claim-reference-2-2-self",
        "claim-reference-3-4-future",
        "claim-reference-5-99-missing",
    ]
    assert all(issue.severity == "high" for issue in report.issues)

    valid = validate_claim_dependencies(
        claims=[
            {"claim": 1, "references": []},
            {"claim": 2, "references": [1]},
            {"claim": 3, "references": [2]},
        ]
    )
    assert valid.issues == []


def test_claim_validators_report_malformed_and_duplicate_claims():
    claims = [
        {"claim": 1, "features": ["F-001"], "references": []},
        {"claim": 1, "features": ["F-002"], "references": []},
        {"claim": "2", "features": ["F-003"], "references": [1]},
        {"features": ["F-004"], "references": []},
        {"claim": 4, "references": ["2"]},
        {"claim": 5, "features": "F-005", "references": []},
    ]

    support = validate_claim_support(claims, {"F-001", "F-002"})
    dependencies = validate_claim_dependencies(claims)

    assert [issue.issue_id for issue in support.issues] == [
        "claim-1-duplicate-number",
        "claim-index-2-invalid-number",
        "claim-index-3-missing-number",
        "claim-4-missing-features",
        "claim-5-invalid-features",
    ]
    assert [issue.issue_id for issue in dependencies.issues] == [
        "claim-1-duplicate-number",
        "claim-index-2-invalid-number",
        "claim-index-3-missing-number",
        "claim-4-reference-index-0-invalid",
    ]
    assert all(issue.severity == "high" for issue in support.issues)
    assert all(issue.severity == "high" for issue in dependencies.issues)


def test_claim_validators_report_invalid_top_level_structure():
    support = validate_claim_support({"claim": 1}, set())
    dependencies = validate_claim_dependencies("not-a-claim-list")

    assert [issue.issue_id for issue in support.issues] == [
        "claims-invalid-structure"
    ]
    assert [issue.issue_id for issue in dependencies.issues] == [
        "claims-invalid-structure"
    ]


def test_claim_dependencies_allow_valid_multiple_parents():
    report = validate_claim_dependencies(
        claims=[
            {"claim": 1, "references": []},
            {"claim": 2, "references": []},
            {"claim": 3, "references": [1, 2]},
        ]
    )

    assert report.issues == []


def test_terminology_uses_structured_occurrences_across_final_text_artifacts():
    report = validate_terminology_consistency(
        claims=[
            {
                "claim": 1,
                "text": "一种折叠支架，包括支撑臂。",
                "term_occurrences": [
                    {
                        "occurrence_id": "C1-T-001-1",
                        "term_id": "T-001",
                        "rendered": "支撑臂",
                    }
                ],
                "required_term_ids": ["T-001"],
            }
        ],
        specification_sections={
            "具体实施方式": {
                "text": "支承臂通过转轴连接。",
                "term_occurrences": [
                    {
                        "occurrence_id": "SPEC-EMB-T-001-1",
                        "term_id": "T-001",
                        "rendered": "支承臂",
                    }
                ],
                "required_term_ids": ["T-001"],
            }
        },
        abstract={
            "text": "本申请公开一种具有支撑臂的折叠支架。",
            "term_occurrences": [
                {
                    "occurrence_id": "ABS-T-001-1",
                    "term_id": "T-001",
                    "rendered": "支撑臂",
                }
            ],
            "required_term_ids": [],
        },
        terminology={"T-001": "支撑臂"},
    )

    assert [issue.issue_id for issue in report.issues] == [
        "terminology-specification-具体实施方式-occurrence-"
        "SPEC-EMB-T-001-1-render-mismatch"
    ]
    assert report.issues[0].severity == "medium"
    assert "支承臂" in report.issues[0].message


def test_terminology_reports_unknown_duplicate_mismatch_and_required_missing():
    report = validate_terminology_consistency(
        claims=[
            {
                "claim": 1,
                "term_occurrences": [
                    {
                        "occurrence_id": "C1-T-001-1",
                        "term_id": "T-001",
                        "rendered": "支承臂",
                    },
                    {
                        "occurrence_id": "C1-T-404-1",
                        "term_id": "T-404",
                        "rendered": "定位块",
                    },
                    {
                        "occurrence_id": "C1-DUP",
                        "term_id": "T-001",
                        "rendered": "支撑臂",
                    },
                    {
                        "occurrence_id": "C1-DUP",
                        "term_id": "T-001",
                        "rendered": "支承臂",
                    },
                ],
                "required_term_ids": ["T-001", "T-002"],
            }
        ],
        specification_sections={},
        abstract={"term_occurrences": [], "required_term_ids": []},
        terminology={"T-001": "支撑臂", "T-002": "转轴"},
    )

    assert [issue.issue_id for issue in report.issues] == [
        "terminology-claim-1-occurrence-C1-DUP-duplicate",
        "terminology-claim-1-occurrence-C1-T-001-1-render-mismatch",
        "terminology-claim-1-occurrence-C1-T-404-1-unknown-term-T-404",
        "terminology-claim-1-required-T-002-missing",
    ]
    assert len({issue.issue_id for issue in report.issues}) == len(report.issues)


def test_drawing_reference_numerals_distinguish_conflict_and_missing():
    report = validate_drawing_reference_numerals(
        reference_table=[
            {"numeral": "10", "component": "支撑臂"},
            {"numeral": "10", "component": "底座"},
            {"numeral": "20", "component": "转轴"},
        ],
        referenced_numerals=["10", "20", "30"],
    )

    assert [issue.issue_id for issue in report.issues] == [
        "drawing-numeral-10-conflict",
        "drawing-numeral-30-missing",
    ]
    assert "conflict" in report.issues[0].message
    assert "missing" in report.issues[1].message


def test_drawing_validator_reports_malformed_duplicate_conflict_and_unused():
    report = validate_drawing_reference_numerals(
        reference_table=[
            {"component": "底座"},
            {"numeral": "", "component": "底座"},
            {"numeral": "10"},
            "not-an-entry",
            {"numeral": "20", "component": "支撑臂"},
            {"numeral": "20", "component": "支撑臂"},
            {"numeral": "30", "component": "转轴"},
            {"numeral": "30", "component": "锁止销"},
            {"numeral": "50", "component": "锁止销"},
        ],
        referenced_numerals=["20", "30", "40", ""],
    )

    assert [issue.issue_id for issue in report.issues] == [
        "drawing-reference-index-0-missing-numeral",
        "drawing-reference-index-1-invalid-numeral",
        "drawing-reference-index-2-missing-component",
        "drawing-reference-index-3-invalid-structure",
        "drawing-numeral-20-duplicate",
        "drawing-numeral-30-conflict",
        "drawing-text-reference-index-3-invalid",
        "drawing-numeral-40-missing",
        "drawing-numeral-50-unused",
    ]
    severities = {issue.issue_id: issue.severity for issue in report.issues}
    assert severities["drawing-numeral-30-conflict"] == "high"
    assert severities["drawing-numeral-50-unused"] == "medium"


def test_drawing_validator_reports_invalid_top_level_structures():
    report = validate_drawing_reference_numerals(
        reference_table="not-a-table",
        referenced_numerals={"10": True},
    )

    assert [issue.issue_id for issue in report.issues] == [
        "drawing-reference-table-invalid-structure",
        "drawing-text-references-invalid-structure",
    ]


def test_final_text_rejects_forbidden_fact_statuses_without_mutating_facts():
    facts = [
        TechnicalFact(
            fact_id="F-001",
            statement="支撑臂通过转轴与底座连接。",
            status=status,
        )
        for status in (
            FactStatus.CONFIRMED,
            FactStatus.INFERRED,
            FactStatus.MISSING,
            FactStatus.CONFLICTED,
        )
    ]
    facts[1].fact_id = "F-002"
    facts[2].fact_id = "F-003"
    facts[3].fact_id = "F-004"
    original_statuses = [fact.status for fact in facts]

    report = validate_final_fact_statuses(
        facts=facts,
        final_fact_ids={"F-001", "F-002", "F-003", "F-004"},
    )

    assert [issue.issue_id for issue in report.issues] == [
        "final-fact-F-002-inferred",
        "final-fact-F-003-missing",
        "final-fact-F-004-conflicted",
    ]
    assert all(issue.severity == "high" for issue in report.issues)
    assert [fact.status for fact in facts] == original_statuses


def test_final_fact_validation_reports_duplicate_and_unknown_fact_ids():
    facts = [
        TechnicalFact(
            fact_id="F-001",
            statement="支撑臂通过转轴与底座连接。",
            status=FactStatus.CONFIRMED,
        ),
        TechnicalFact(
            fact_id="F-001",
            statement="支撑臂通过转轴与底座连接。",
            status=FactStatus.CONFIRMED,
        ),
    ]

    report = validate_final_fact_statuses(
        facts=facts,
        final_fact_ids={"F-001", "F-404"},
    )

    assert [issue.issue_id for issue in report.issues] == [
        "final-fact-F-001-duplicate",
        "final-fact-F-404-missing",
    ]
    assert all(issue.severity == "high" for issue in report.issues)


def test_duplicate_fact_ids_do_not_hide_a_forbidden_status():
    facts = [
        TechnicalFact(
            fact_id="F-001",
            statement="支撑臂通过转轴与底座连接。",
            status=FactStatus.CONFIRMED,
        ),
        TechnicalFact(
            fact_id="F-001",
            statement="该连接关系尚待确认。",
            status=FactStatus.INFERRED,
        ),
    ]

    report = validate_final_fact_statuses(facts=facts, final_fact_ids={"F-001"})

    assert [issue.issue_id for issue in report.issues] == [
        "final-fact-F-001-duplicate",
        "final-fact-F-001-inferred",
    ]


def test_stale_delivery_artifacts_are_ineligible_for_final_delivery():
    report = validate_artifact_freshness(
        artifacts=[
            ArtifactRef(
                artifact_type="claims",
                version=2,
                path="drafts/claims-v2.json",
            ),
            ArtifactRef(
                artifact_type="specification",
                version=1,
                path="drafts/specification-v1.json",
                stale=True,
            ),
            ArtifactRef(
                artifact_type="quality-review",
                version=1,
                path="review-log/review-v1.json",
                stale=True,
            ),
            ArtifactRef(
                artifact_type="docx",
                version=1,
                path="exports/application-v1.docx",
                stale=True,
            ),
        ]
    )

    assert [issue.issue_id for issue in report.issues] == [
        _stale_issue_id(
            "specification", 1, "drafts/specification-v1.json"
        ),
        _stale_issue_id("quality-review", 1, "review-log/review-v1.json"),
        _stale_issue_id("docx", 1, "exports/application-v1.docx"),
    ]
    assert report.eligible_for_final_delivery is False


def test_open_high_review_issues_block_final_delivery():
    report = validate_open_high_issues(
        review_issues=[
            ReviewIssue(
                issue_id="review-claim-2-dependency",
                severity="high",
                message="claim 2 refers to missing claim 3",
            ),
            ReviewIssue(
                issue_id="review-term-T-001",
                severity="medium",
                message="terminology requires human decision",
            ),
            ReviewIssue(
                issue_id="review-support-F-004",
                severity="high",
                message="support gap was resolved",
                closed=True,
            ),
        ]
    )

    assert [issue.issue_id for issue in report.issues] == [
        "review-claim-2-dependency"
    ]
    assert report.eligible_for_final_delivery is False


def test_public_validator_reports_use_unique_stable_issue_ids():
    support = validate_claim_support(
        claims=[{"claim": 1, "features": ["F-999", "F-999"]}],
        supported_fact_ids=set(),
    )
    dependencies = validate_claim_dependencies(
        claims=[
            {"claim": 1, "references": []},
            {"claim": 2, "references": [99, 99]},
        ]
    )
    terminology = validate_terminology_consistency(
        claims=[
            {
                "claim": 1,
                "term_occurrences": [],
                "required_term_ids": [],
            },
            {
                "claim": 1,
                "term_occurrences": [],
                "required_term_ids": [],
            },
            {
                "claim": 1,
                "term_occurrences": [],
                "required_term_ids": [],
            },
        ],
        specification_sections={},
        abstract={"term_occurrences": [], "required_term_ids": []},
        terminology={},
    )
    drawings = validate_drawing_reference_numerals(
        reference_table=[
            {"numeral": "10", "component": "底座"},
            {"numeral": "10", "component": "底座"},
        ],
        referenced_numerals=["30", "30"],
    )
    final_facts = validate_final_fact_statuses(
        facts=[
            TechnicalFact(
                fact_id="F-001",
                statement="支撑臂通过转轴与底座连接。",
                status=FactStatus.INFERRED,
            ),
            TechnicalFact(
                fact_id="F-001",
                statement="支撑臂通过转轴与底座连接。",
                status=FactStatus.INFERRED,
            ),
        ],
        final_fact_ids={"F-001"},
    )
    stale = validate_artifact_freshness(
        artifacts=[
            ArtifactRef(
                artifact_type="specification",
                version=1,
                path="drafts/specification-a.json",
                stale=True,
            ),
            ArtifactRef(
                artifact_type="specification",
                version=1,
                path="drafts/specification-b.json",
                stale=True,
            ),
        ]
    )
    open_high = validate_open_high_issues(
        review_issues=[
            ReviewIssue(issue_id="R-1", severity="high", message="first"),
            ReviewIssue(issue_id="R-1", severity="high", message="duplicate"),
        ]
    )

    reports = {
        "support": support,
        "dependencies": dependencies,
        "terminology": terminology,
        "drawings": drawings,
        "final_facts": final_facts,
        "stale": stale,
        "open_high": open_high,
    }
    for name, report in reports.items():
        issue_ids = [issue.issue_id for issue in report.issues]
        assert len(issue_ids) == len(set(issue_ids)), name

    assert [issue.issue_id for issue in support.issues] == [
        "claim-1-feature-F-999-duplicate",
        "unsupported-1-F-999",
    ]
    assert [issue.issue_id for issue in dependencies.issues] == [
        "claim-2-reference-99-duplicate",
        "claim-reference-2-99-missing",
    ]
    expected_stale_ids = [
        _stale_issue_id("specification", 1, path)
        for path in ("drafts/specification-a.json", "drafts/specification-b.json")
    ]
    assert [issue.issue_id for issue in stale.issues] == expected_stale_ids


def test_public_validators_return_reports_for_malformed_json_inputs():
    support = validate_claim_support([], "not-a-supported-fact-list")
    final_facts = validate_final_fact_statuses(
        facts=[
            {
                "fact_id": "F-001",
                "statement": "无效状态样例。",
                "status": "not-a-status",
            },
            "not-a-fact",
        ],
        final_fact_ids=["F-001", None],
    )
    stale = validate_artifact_freshness(
        artifacts=[
            {
                "artifact_type": "specification",
                "version": 1,
                "path": None,
                "stale": True,
            },
            "not-an-artifact",
        ]
    )
    open_high = validate_open_high_issues(
        review_issues=[
            {"issue_id": "R-1", "severity": "urgent", "message": "bad"},
            "not-an-issue",
        ]
    )
    terminology = validate_terminology_consistency(
        claims="not-claims",
        specification_sections=[],
        abstract=[],
        terminology=[],
    )

    assert [issue.issue_id for issue in support.issues] == [
        "supported-fact-ids-invalid-structure"
    ]
    assert [issue.issue_id for issue in final_facts.issues] == [
        "final-fact-index-0-invalid-structure",
        "final-fact-index-1-invalid-structure",
        "final-fact-id-index-1-invalid",
        "final-fact-F-001-missing",
    ]
    assert [issue.issue_id for issue in stale.issues] == [
        "artifact-index-0-invalid-structure",
        "artifact-index-1-invalid-structure",
    ]
    assert [issue.issue_id for issue in open_high.issues] == [
        "review-issue-index-0-invalid-structure",
        "review-issue-index-1-invalid-structure",
    ]
    assert [issue.issue_id for issue in terminology.issues] == [
        "terminology-invalid-structure"
    ]


def test_mechanical_fixtures_feed_structured_validators_without_drift():
    claims_data = json.loads(
        (FIXTURES / "mechanical_case" / "claims.json").read_text(encoding="utf-8")
    )
    specification_data = json.loads(
        (FIXTURES / "mechanical_case" / "specification.json").read_text(
            encoding="utf-8"
        )
    )

    reports = [
        validate_claim_support(
            claims_data["claims"], claims_data["supported_fact_ids"]
        ),
        validate_claim_dependencies(claims_data["claims"]),
        validate_terminology_consistency(
            claims=claims_data["claims"],
            specification_sections=specification_data["sections"],
            abstract=specification_data["abstract"],
            terminology=claims_data["terminology"],
        ),
        validate_drawing_reference_numerals(
            reference_table=specification_data["reference_table"],
            referenced_numerals=specification_data["referenced_numerals"],
        ),
    ]

    assert [report.issues for report in reports] == [[], [], [], []]
