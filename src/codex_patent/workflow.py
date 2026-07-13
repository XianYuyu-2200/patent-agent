from codex_patent.models import CaseStage, PatentCase


class WorkflowError(ValueError):
    pass


REQUIRED_APPROVAL = {
    CaseStage.SEARCH: "technical-solution",
    CaseStage.DRAFTING: "claim-set",
}


def advance_case(case: PatentCase, target: CaseStage) -> PatentCase:
    approval = REQUIRED_APPROVAL.get(target)
    if approval and approval not in case.approvals:
        raise WorkflowError(f"missing approval: {approval}")
    if target == CaseStage.DELIVERY and any(
        issue.severity == "high" and not issue.closed for issue in case.issues
    ):
        raise WorkflowError("open high-severity review issues")
    case.stage = target
    return case


def invalidate_after_claim_change(case: PatentCase) -> PatentCase:
    for artifact in case.artifacts:
        if artifact.artifact_type in {"specification", "quality-review", "docx"}:
            artifact.stale = True
    return case
