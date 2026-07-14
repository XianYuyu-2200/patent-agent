from collections import Counter

from pydantic import BaseModel, Field

from codex_patent.models import ArtifactRef, FactStatus, ReviewIssue, TechnicalFact


class ValidationReport(BaseModel):
    issues: list[ReviewIssue] = Field(default_factory=list)

    @property
    def eligible_for_final_delivery(self) -> bool:
        return not any(
            issue.severity == "high" and not issue.closed for issue in self.issues
        )


def validate_artifact_freshness(artifacts: list[ArtifactRef]) -> ValidationReport:
    guarded_types = {"specification", "quality-review", "docx"}
    issues = [
        ReviewIssue(
            issue_id=f"stale-artifact-{artifact.artifact_type}-v{artifact.version}",
            severity="high",
            message=f"{artifact.path} is stale and cannot be delivered",
        )
        for artifact in artifacts
        if artifact.artifact_type in guarded_types and artifact.stale
    ]
    return ValidationReport(issues=issues)


def validate_open_high_issues(
    review_issues: list[ReviewIssue],
) -> ValidationReport:
    return ValidationReport(
        issues=[
            issue
            for issue in review_issues
            if issue.severity == "high" and not issue.closed
        ]
    )


def validate_final_fact_statuses(
    facts: list[TechnicalFact], final_fact_ids: set[str]
) -> ValidationReport:
    allowed_statuses = {FactStatus.CONFIRMED, FactStatus.SOURCE_BACKED}
    issues: list[ReviewIssue] = []
    for fact in facts:
        if fact.fact_id in final_fact_ids and fact.status not in allowed_statuses:
            issues.append(
                ReviewIssue(
                    issue_id=f"final-fact-{fact.fact_id}-{fact.status.value}",
                    severity="high",
                    message=(
                        f"final text uses fact {fact.fact_id} with forbidden status "
                        f"{fact.status.value}"
                    ),
                )
            )
    return ValidationReport(issues=issues)


def validate_drawing_reference_numerals(
    reference_table: list[dict], referenced_numerals: list[str]
) -> ValidationReport:
    counts = Counter(entry["numeral"] for entry in reference_table)
    issues: list[ReviewIssue] = []
    for numeral in dict.fromkeys(entry["numeral"] for entry in reference_table):
        if counts[numeral] > 1:
            issues.append(
                ReviewIssue(
                    issue_id=f"drawing-numeral-{numeral}-duplicate",
                    severity="medium",
                    message=f"drawing reference numeral {numeral} is duplicate",
                )
            )
    for numeral in dict.fromkeys(referenced_numerals):
        if numeral not in counts:
            issues.append(
                ReviewIssue(
                    issue_id=f"drawing-numeral-{numeral}-missing",
                    severity="medium",
                    message=f"drawing reference numeral {numeral} is missing",
                )
            )
    return ValidationReport(issues=issues)


def _terminology_issue(
    *, artifact: str, location: str, term_id: str, actual: str, expected: str
) -> ReviewIssue:
    return ReviewIssue(
        issue_id=f"terminology-{artifact}-{location}-{term_id}",
        severity="medium",
        message=(
            f"{artifact} {location} uses {actual!r} for {term_id}; "
            f"expected {expected!r}"
        ),
    )


def validate_terminology_consistency(
    claims: list[dict],
    specification_sections: dict[str, dict],
    abstract: dict,
    terminology: dict[str, str],
) -> ValidationReport:
    issues: list[ReviewIssue] = []
    for claim in claims:
        for term_id, actual in claim.get("terms", {}).items():
            expected = terminology.get(term_id)
            if expected is not None and actual != expected:
                issues.append(
                    _terminology_issue(
                        artifact="claim",
                        location=str(claim["claim"]),
                        term_id=term_id,
                        actual=actual,
                        expected=expected,
                    )
                )
    for section, content in specification_sections.items():
        for term_id, actual in content.get("terms", {}).items():
            expected = terminology.get(term_id)
            if expected is not None and actual != expected:
                issues.append(
                    _terminology_issue(
                        artifact="specification",
                        location=section,
                        term_id=term_id,
                        actual=actual,
                        expected=expected,
                    )
                )
    for term_id, actual in abstract.get("terms", {}).items():
        expected = terminology.get(term_id)
        if expected is not None and actual != expected:
            issues.append(
                _terminology_issue(
                    artifact="abstract",
                    location="abstract",
                    term_id=term_id,
                    actual=actual,
                    expected=expected,
                )
            )
    return ValidationReport(issues=issues)


def validate_claim_dependencies(claims: list[dict]) -> ValidationReport:
    claim_numbers = {claim["claim"] for claim in claims}
    issues: list[ReviewIssue] = []
    for claim in claims:
        claim_number = claim["claim"]
        for reference in claim.get("references", []):
            if reference == claim_number:
                reason = "self"
            elif reference not in claim_numbers:
                reason = "missing"
            elif reference > claim_number:
                reason = "future"
            else:
                continue
            issues.append(
                ReviewIssue(
                    issue_id=(
                        f"claim-reference-{claim_number}-{reference}-{reason}"
                    ),
                    severity="high",
                    message=(
                        f"claim {claim_number} has {reason} reference to claim "
                        f"{reference}"
                    ),
                )
            )
    return ValidationReport(issues=issues)


def validate_claim_support(
    claims: list[dict], supported_fact_ids: set[str]
) -> ValidationReport:
    issues: list[ReviewIssue] = []
    for claim in claims:
        for feature_id in claim["features"]:
            if feature_id not in supported_fact_ids:
                issues.append(
                    ReviewIssue(
                        issue_id=f"unsupported-{claim['claim']}-{feature_id}",
                        severity="high",
                        message=(
                            f"claim {claim['claim']} feature {feature_id} "
                            "lacks specification support"
                        ),
                    )
                )
    return ValidationReport(issues=issues)
