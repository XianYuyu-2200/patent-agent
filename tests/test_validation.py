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


def test_terminology_uses_structured_occurrences_across_final_text_artifacts():
    report = validate_terminology_consistency(
        claims=[
            {
                "claim": 1,
                "text": "一种折叠支架，包括支撑臂。",
                "terms": {"T-001": "支撑臂"},
            }
        ],
        specification_sections={
            "具体实施方式": {
                "text": "支承臂通过转轴连接。",
                "terms": {"T-001": "支承臂"},
            }
        },
        abstract={
            "text": "本申请公开一种具有支撑臂的折叠支架。",
            "terms": {"T-001": "支撑臂"},
        },
        terminology={"T-001": "支撑臂"},
    )

    assert [issue.issue_id for issue in report.issues] == [
        "terminology-specification-具体实施方式-T-001"
    ]
    assert report.issues[0].severity == "medium"
    assert "支承臂" in report.issues[0].message


def test_drawing_reference_numerals_distinguish_duplicate_and_missing():
    report = validate_drawing_reference_numerals(
        reference_table=[
            {"numeral": "10", "component": "支撑臂"},
            {"numeral": "10", "component": "底座"},
            {"numeral": "20", "component": "转轴"},
        ],
        referenced_numerals=["10", "20", "30"],
    )

    assert [issue.issue_id for issue in report.issues] == [
        "drawing-numeral-10-duplicate",
        "drawing-numeral-30-missing",
    ]
    assert "duplicate" in report.issues[0].message
    assert "missing" in report.issues[1].message


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
        "stale-artifact-specification-v1",
        "stale-artifact-quality-review-v1",
        "stale-artifact-docx-v1",
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
