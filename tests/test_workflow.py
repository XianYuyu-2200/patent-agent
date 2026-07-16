import pytest

from codex_patent.models import ArtifactRef, CaseStage, PatentCase, ReviewIssue
from codex_patent.workflow import WorkflowError, advance_case, invalidate_after_claim_change


def test_search_requires_technical_solution_approval():
    case = PatentCase(case_id="C1", title="支架", stage=CaseStage.MINING)
    with pytest.raises(WorkflowError, match="technical-solution"):
        advance_case(case, CaseStage.SEARCH)


def test_drafting_requires_claim_set_approval():
    case = PatentCase(case_id="C1", title="支架", stage=CaseStage.CLAIMS)
    with pytest.raises(WorkflowError, match="claim-set"):
        advance_case(case, CaseStage.DRAFTING)


def test_delivery_blocks_open_high_issues_without_requiring_final_approval():
    case = PatentCase(
        case_id="C1",
        title="支架",
        stage=CaseStage.REVIEW,
        issues=[ReviewIssue(issue_id="R-1", severity="high", message="缺少支持")],
    )
    with pytest.raises(WorkflowError, match="open high-severity"):
        advance_case(case, CaseStage.DELIVERY)

    case.issues[0].closed = True
    advance_case(case, CaseStage.DELIVERY)
    assert case.stage == CaseStage.DELIVERY


def test_claim_change_invalidates_drafting_and_review():
    case = PatentCase(
        case_id="C1",
        title="支架",
        artifacts=[
            ArtifactRef(
                artifact_type="claims", version=2, path="drafts/claims-v2.md"
            ),
            ArtifactRef(
                artifact_type="specification", version=1, path="drafts/spec-v1.md"
            ),
            ArtifactRef(
                artifact_type="quality-review",
                version=1,
                path="review-log/review-v1.json",
            ),
            ArtifactRef(artifact_type="docx", version=1, path="exports/application.docx"),
        ],
    )
    invalidate_after_claim_change(case)
    assert [artifact.stale for artifact in case.artifacts] == [
        False,
        True,
        True,
        True,
    ]
