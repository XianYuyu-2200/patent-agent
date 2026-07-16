import hashlib
import posixpath
from collections import Counter

from pydantic import BaseModel, Field, ValidationError

from codex_patent.models import ArtifactRef, FactStatus, ReviewIssue, TechnicalFact


class ValidationReport(BaseModel):
    issues: list[ReviewIssue] = Field(default_factory=list)

    @property
    def eligible_for_final_delivery(self) -> bool:
        return not any(
            issue.severity == "high" and not issue.closed for issue in self.issues
        )


def _report(issues: list[ReviewIssue]) -> ValidationReport:
    unique_issues: list[ReviewIssue] = []
    seen_issue_ids: set[str] = set()
    for issue in issues:
        if issue.issue_id in seen_issue_ids:
            continue
        seen_issue_ids.add(issue.issue_id)
        unique_issues.append(issue)
    return ValidationReport(issues=unique_issues)


def _high_issue(issue_id: str, message: str) -> ReviewIssue:
    return ReviewIssue(issue_id=issue_id, severity="high", message=message)


def _is_positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _stable_values(value: object) -> list[object] | None:
    if isinstance(value, (list, tuple)):
        return list(value)
    if isinstance(value, set):
        return sorted(value, key=lambda item: (type(item).__name__, repr(item)))
    return None


def _validated_claim_entries(
    claims: object,
) -> tuple[list[tuple[int, dict, int]], list[ReviewIssue]]:
    if not isinstance(claims, list):
        return [], [
            _high_issue(
                "claims-invalid-structure",
                "claims must be a JSON array of claim objects",
            )
        ]

    entries: list[tuple[int, dict, int]] = []
    structure_issues: list[ReviewIssue] = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            structure_issues.append(
                _high_issue(
                    f"claim-index-{index}-invalid-structure",
                    f"claim at index {index} must be an object",
                )
            )
            continue
        if "claim" not in claim:
            structure_issues.append(
                _high_issue(
                    f"claim-index-{index}-missing-number",
                    f"claim at index {index} is missing its claim number",
                )
            )
            continue
        claim_number = claim["claim"]
        if not _is_positive_int(claim_number):
            structure_issues.append(
                _high_issue(
                    f"claim-index-{index}-invalid-number",
                    f"claim at index {index} must use a positive integer number",
                )
            )
            continue
        entries.append((index, claim, claim_number))

    counts = Counter(claim_number for _, _, claim_number in entries)
    duplicate_issues = [
        _high_issue(
            f"claim-{claim_number}-duplicate-number",
            f"claim number {claim_number} occurs more than once",
        )
        for claim_number in dict.fromkeys(
            claim_number for _, _, claim_number in entries
        )
        if counts[claim_number] > 1
    ]
    return entries, duplicate_issues + structure_issues


def _unique_claim_entries(
    entries: list[tuple[int, dict, int]],
) -> list[tuple[int, dict, int]]:
    unique_entries: list[tuple[int, dict, int]] = []
    seen_claim_numbers: set[int] = set()
    for entry in entries:
        claim_number = entry[2]
        if claim_number in seen_claim_numbers:
            continue
        seen_claim_numbers.add(claim_number)
        unique_entries.append(entry)
    return unique_entries


def _path_identity(path: str) -> str:
    normalized = posixpath.normpath(path.replace("\\", "/")).casefold()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]


def validate_artifact_freshness(artifacts: object) -> ValidationReport:
    guarded_types = {"specification", "quality-review", "docx"}
    if not isinstance(artifacts, list):
        return _report(
            [
                _high_issue(
                    "artifacts-invalid-structure",
                    "artifacts must be a JSON array",
                )
            ]
        )
    valid_artifacts: list[ArtifactRef] = []
    issues: list[ReviewIssue] = []
    for index, artifact in enumerate(artifacts):
        try:
            valid_artifacts.append(ArtifactRef.model_validate(artifact))
        except (ValidationError, TypeError, ValueError):
            issues.append(
                _high_issue(
                    f"artifact-index-{index}-invalid-structure",
                    f"artifact at index {index} is invalid",
                )
            )
    issues.extend(
        ReviewIssue(
            issue_id=(
                f"stale-artifact-{artifact.artifact_type}-v{artifact.version}-"
                f"{_path_identity(artifact.path)}"
            ),
            severity="high",
            message=f"{artifact.path} is stale and cannot be delivered",
        )
        for artifact in valid_artifacts
        if artifact.artifact_type in guarded_types and artifact.stale
    )
    return _report(issues)


def validate_open_high_issues(
    review_issues: object,
) -> ValidationReport:
    if not isinstance(review_issues, list):
        return _report(
            [
                _high_issue(
                    "review-issues-invalid-structure",
                    "review issues must be a JSON array",
                )
            ]
        )
    valid_review_issues: list[ReviewIssue] = []
    structure_issues: list[ReviewIssue] = []
    for index, issue in enumerate(review_issues):
        try:
            valid_review_issues.append(ReviewIssue.model_validate(issue))
        except (ValidationError, TypeError, ValueError):
            structure_issues.append(
                _high_issue(
                    f"review-issue-index-{index}-invalid-structure",
                    f"review issue at index {index} is invalid",
                )
            )
    return _report(
        structure_issues
        + [
            issue
            for issue in valid_review_issues
            if issue.severity == "high" and not issue.closed
        ]
    )


def validate_final_fact_statuses(
    facts: object, final_fact_ids: object
) -> ValidationReport:
    allowed_statuses = {FactStatus.CONFIRMED, FactStatus.SOURCE_BACKED}
    issues: list[ReviewIssue] = []
    valid_facts: list[TechnicalFact] = []
    if not isinstance(facts, list):
        issues.append(
            _high_issue(
                "final-facts-invalid-structure",
                "technical facts must be a JSON array",
            )
        )
    else:
        for index, fact in enumerate(facts):
            try:
                valid_facts.append(TechnicalFact.model_validate(fact))
            except (ValidationError, TypeError, ValueError):
                issues.append(
                    _high_issue(
                        f"final-fact-index-{index}-invalid-structure",
                        f"technical fact at index {index} is invalid",
                    )
                )

    valid_final_fact_ids: list[str] = []
    final_fact_id_values = _stable_values(final_fact_ids)
    if final_fact_id_values is None:
        issues.append(
            _high_issue(
                "final-fact-ids-invalid-structure",
                "final fact IDs must be an array or set",
            )
        )
    else:
        for index, fact_id in enumerate(final_fact_id_values):
            if not isinstance(fact_id, str) or not fact_id.strip():
                issues.append(
                    _high_issue(
                        f"final-fact-id-index-{index}-invalid",
                        f"final fact ID at index {index} must be a non-blank string",
                    )
                )
                continue
            valid_final_fact_ids.append(fact_id.strip())
    final_fact_id_set = set(valid_final_fact_ids)

    fact_id_counts = Counter(fact.fact_id for fact in valid_facts)
    for fact_id in dict.fromkeys(fact.fact_id for fact in valid_facts):
        if fact_id_counts[fact_id] > 1:
            issues.append(
                ReviewIssue(
                    issue_id=f"final-fact-{fact_id}-duplicate",
                    severity="high",
                    message=f"technical facts contain duplicate fact ID {fact_id}",
                )
            )
    seen_forbidden_statuses: set[tuple[str, FactStatus]] = set()
    for fact in valid_facts:
        if fact.fact_id in final_fact_id_set and fact.status not in allowed_statuses:
            status_key = (fact.fact_id, fact.status)
            if status_key in seen_forbidden_statuses:
                continue
            seen_forbidden_statuses.add(status_key)
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
    for fact_id in sorted(final_fact_id_set - set(fact_id_counts)):
        issues.append(
            ReviewIssue(
                issue_id=f"final-fact-{fact_id}-missing",
                severity="high",
                message=f"final text references missing fact {fact_id}",
            )
        )
    return _report(issues)


def validate_drawing_reference_numerals(
    reference_table: object, referenced_numerals: object
) -> ValidationReport:
    issues: list[ReviewIssue] = []
    valid_entries: list[tuple[str, str]] = []
    if not isinstance(reference_table, list):
        issues.append(
            _high_issue(
                "drawing-reference-table-invalid-structure",
                "drawing reference table must be an array",
            )
        )
    else:
        for index, entry in enumerate(reference_table):
            if not isinstance(entry, dict):
                issues.append(
                    _high_issue(
                        f"drawing-reference-index-{index}-invalid-structure",
                        f"drawing reference entry {index} must be an object",
                    )
                )
                continue
            if "numeral" not in entry:
                issues.append(
                    _high_issue(
                        f"drawing-reference-index-{index}-missing-numeral",
                        f"drawing reference entry {index} is missing its numeral",
                    )
                )
                continue
            numeral = _drawing_token(entry["numeral"])
            if numeral is None:
                issues.append(
                    _high_issue(
                        f"drawing-reference-index-{index}-invalid-numeral",
                        f"drawing reference entry {index} has an invalid numeral",
                    )
                )
                continue
            if "component" not in entry:
                issues.append(
                    _high_issue(
                        f"drawing-reference-index-{index}-missing-component",
                        f"drawing reference entry {index} is missing its component",
                    )
                )
                continue
            component = entry["component"]
            if not isinstance(component, str) or not component.strip():
                issues.append(
                    _high_issue(
                        f"drawing-reference-index-{index}-invalid-component",
                        f"drawing reference entry {index} has an invalid component",
                    )
                )
                continue
            valid_entries.append((numeral, component.strip()))

    components_by_numeral: dict[str, list[str]] = {}
    for numeral, component in valid_entries:
        components_by_numeral.setdefault(numeral, []).append(component)
    for numeral, components in components_by_numeral.items():
        if len(set(components)) > 1:
            issues.append(
                _high_issue(
                    f"drawing-numeral-{numeral}-conflict",
                    f"drawing reference numeral {numeral} has a component conflict",
                )
            )
        elif len(components) > 1:
            issues.append(
                ReviewIssue(
                    issue_id=f"drawing-numeral-{numeral}-duplicate",
                    severity="medium",
                    message=f"drawing reference numeral {numeral} is duplicate",
                )
            )

    valid_referenced_numerals: list[str] = []
    if not isinstance(referenced_numerals, list):
        issues.append(
            _high_issue(
                "drawing-text-references-invalid-structure",
                "drawing text references must be an array",
            )
        )
    else:
        for index, raw_numeral in enumerate(referenced_numerals):
            numeral = _drawing_token(raw_numeral)
            if numeral is None:
                issues.append(
                    _high_issue(
                        f"drawing-text-reference-index-{index}-invalid",
                        f"drawing text reference {index} has an invalid numeral",
                    )
                )
                continue
            valid_referenced_numerals.append(numeral)

    table_numerals = set(components_by_numeral)
    referenced_set = set(valid_referenced_numerals)
    for numeral in dict.fromkeys(valid_referenced_numerals):
        if numeral not in table_numerals:
            issues.append(
                ReviewIssue(
                    issue_id=f"drawing-numeral-{numeral}-missing",
                    severity="medium",
                    message=f"drawing reference numeral {numeral} is missing",
                )
            )
    for numeral in components_by_numeral:
        if numeral not in referenced_set:
            issues.append(
                ReviewIssue(
                    issue_id=f"drawing-numeral-{numeral}-unused",
                    severity="medium",
                    message=f"drawing reference numeral {numeral} is unused in text",
                )
            )
    return _report(issues)


def _drawing_token(value: object) -> str | None:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        return None
    token = str(value).strip()
    return token or None


def _validate_term_location(
    *,
    artifact: str,
    location: str,
    content: object,
    terminology: dict[str, str],
) -> list[ReviewIssue]:
    prefix = f"terminology-{artifact}-{location}"
    if not isinstance(content, dict):
        return [
            _high_issue(
                f"{prefix}-invalid-structure",
                f"{artifact} {location} terminology data must be an object",
            )
        ]

    issues: list[ReviewIssue] = []
    occurrences = content.get("term_occurrences")
    if occurrences is None:
        issues.append(
            _high_issue(
                f"{prefix}-missing-occurrences",
                f"{artifact} {location} is missing term_occurrences",
            )
        )
        occurrences = []
    elif not isinstance(occurrences, list):
        issues.append(
            _high_issue(
                f"{prefix}-invalid-occurrences",
                f"{artifact} {location} term_occurrences must be an array",
            )
        )
        occurrences = []

    valid_occurrences: list[tuple[str, str, str]] = []
    occurrence_ids: list[str] = []
    for index, occurrence in enumerate(occurrences):
        if not isinstance(occurrence, dict):
            issues.append(
                _high_issue(
                    f"{prefix}-occurrence-index-{index}-invalid-structure",
                    f"{artifact} {location} occurrence {index} must be an object",
                )
            )
            continue
        occurrence_id = occurrence.get("occurrence_id")
        if not isinstance(occurrence_id, str) or not occurrence_id.strip():
            issues.append(
                _high_issue(
                    f"{prefix}-occurrence-index-{index}-invalid-id",
                    f"{artifact} {location} occurrence {index} needs a stable ID",
                )
            )
            continue
        occurrence_id = occurrence_id.strip()
        occurrence_ids.append(occurrence_id)
        term_id = occurrence.get("term_id")
        if not isinstance(term_id, str) or not term_id.strip():
            issues.append(
                _high_issue(
                    f"{prefix}-occurrence-{occurrence_id}-invalid-term-id",
                    f"occurrence {occurrence_id} needs a non-blank term ID",
                )
            )
            continue
        rendered = occurrence.get("rendered")
        if not isinstance(rendered, str) or not rendered.strip():
            issues.append(
                _high_issue(
                    f"{prefix}-occurrence-{occurrence_id}-invalid-rendered",
                    f"occurrence {occurrence_id} needs non-blank rendered text",
                )
            )
            continue
        valid_occurrences.append((occurrence_id, term_id.strip(), rendered))

    occurrence_counts = Counter(occurrence_ids)
    duplicate_ids = {
        occurrence_id
        for occurrence_id, count in occurrence_counts.items()
        if count > 1
    }
    duplicate_issues = [
        _high_issue(
            f"{prefix}-occurrence-{occurrence_id}-duplicate",
            f"occurrence ID {occurrence_id} is duplicated in {artifact} {location}",
        )
        for occurrence_id in dict.fromkeys(occurrence_ids)
        if occurrence_id in duplicate_ids
    ]

    occurrence_issues: list[ReviewIssue] = []
    seen_occurrence_ids: set[str] = set()
    present_term_ids: set[str] = set()
    for occurrence_id, term_id, rendered in valid_occurrences:
        if occurrence_id in seen_occurrence_ids:
            continue
        seen_occurrence_ids.add(occurrence_id)
        present_term_ids.add(term_id)
        expected = terminology.get(term_id)
        if expected is None:
            occurrence_issues.append(
                ReviewIssue(
                    issue_id=(
                        f"{prefix}-occurrence-{occurrence_id}-unknown-term-{term_id}"
                    ),
                    severity="medium",
                    message=f"occurrence {occurrence_id} uses unknown term ID {term_id}",
                )
            )
        elif rendered != expected:
            occurrence_issues.append(
                ReviewIssue(
                    issue_id=(
                        f"{prefix}-occurrence-{occurrence_id}-render-mismatch"
                    ),
                    severity="medium",
                    message=(
                        f"occurrence {occurrence_id} renders {rendered!r} for "
                        f"{term_id}; expected {expected!r}"
                    ),
                )
            )

    required_term_ids = content.get("required_term_ids", [])
    required_issues: list[ReviewIssue] = []
    if not isinstance(required_term_ids, list):
        required_issues.append(
            _high_issue(
                f"{prefix}-invalid-required-terms",
                f"{artifact} {location} required_term_ids must be an array",
            )
        )
    else:
        for index, term_id in enumerate(required_term_ids):
            if not isinstance(term_id, str) or not term_id.strip():
                required_issues.append(
                    _high_issue(
                        f"{prefix}-required-index-{index}-invalid",
                        f"required term at index {index} must be a non-blank string",
                    )
                )
                continue
            term_id = term_id.strip()
            if term_id not in present_term_ids:
                required_issues.append(
                    ReviewIssue(
                        issue_id=f"{prefix}-required-{term_id}-missing",
                        severity="medium",
                        message=(
                            f"{artifact} {location} is missing required term {term_id}"
                        ),
                    )
                )

    return duplicate_issues + issues + occurrence_issues + required_issues


def validate_terminology_consistency(
    claims: object,
    specification_sections: object,
    abstract: object,
    terminology: object,
) -> ValidationReport:
    issues: list[ReviewIssue] = []
    if not isinstance(terminology, dict):
        return _report(
            [
                _high_issue(
                    "terminology-invalid-structure",
                    "terminology must be a term ID to canonical rendering object",
                )
            ]
        )
    valid_terminology: dict[str, str] = {}
    for index, (term_id, rendered) in enumerate(terminology.items()):
        if (
            not isinstance(term_id, str)
            or not term_id.strip()
            or not isinstance(rendered, str)
            or not rendered.strip()
        ):
            issues.append(
                _high_issue(
                    f"terminology-entry-index-{index}-invalid",
                    f"terminology entry {index} must contain non-blank strings",
                )
            )
            continue
        valid_terminology[term_id.strip()] = rendered

    if not isinstance(claims, list):
        issues.append(
            _high_issue(
                "terminology-claims-invalid-structure",
                "claims terminology input must be an array",
            )
        )
    else:
        seen_claim_numbers: set[int] = set()
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                issues.append(
                    _high_issue(
                        f"terminology-claim-index-{index}-invalid-structure",
                        f"claim terminology entry {index} must be an object",
                    )
                )
                continue
            claim_number = claim.get("claim")
            if not _is_positive_int(claim_number):
                issues.append(
                    _high_issue(
                        f"terminology-claim-index-{index}-invalid-number",
                        f"claim terminology entry {index} needs a positive integer",
                    )
                )
                continue
            if claim_number in seen_claim_numbers:
                issues.append(
                    _high_issue(
                        f"terminology-claim-{claim_number}-duplicate-location",
                        f"claim {claim_number} occurs more than once",
                    )
                )
                continue
            seen_claim_numbers.add(claim_number)
            issues.extend(
                _validate_term_location(
                    artifact="claim",
                    location=str(claim_number),
                    content=claim,
                    terminology=valid_terminology,
                )
            )

    if not isinstance(specification_sections, dict):
        issues.append(
            _high_issue(
                "terminology-specification-invalid-structure",
                "specification sections must be an object",
            )
        )
    else:
        for index, (section, content) in enumerate(specification_sections.items()):
            if not isinstance(section, str) or not section.strip():
                issues.append(
                    _high_issue(
                        f"terminology-specification-index-{index}-invalid-location",
                        f"specification section {index} needs a non-blank name",
                    )
                )
                continue
            issues.extend(
                _validate_term_location(
                    artifact="specification",
                    location=section,
                    content=content,
                    terminology=valid_terminology,
                )
            )

    issues.extend(
        _validate_term_location(
            artifact="abstract",
            location="abstract",
            content=abstract,
            terminology=valid_terminology,
        )
    )
    return _report(issues)


def validate_claim_dependencies(claims: object) -> ValidationReport:
    entries, issues = _validated_claim_entries(claims)
    entries = _unique_claim_entries(entries)
    claim_numbers = {claim_number for _, _, claim_number in entries}
    for _, claim, claim_number in entries:
        references = claim.get("references", [])
        if not isinstance(references, list):
            issues.append(
                _high_issue(
                    f"claim-{claim_number}-invalid-references",
                    f"claim {claim_number} references must be an array",
                )
            )
            continue
        valid_references: list[tuple[int, int]] = []
        for reference_index, reference in enumerate(references):
            if not _is_positive_int(reference):
                issues.append(
                    _high_issue(
                        f"claim-{claim_number}-reference-index-"
                        f"{reference_index}-invalid",
                        f"claim {claim_number} reference at index "
                        f"{reference_index} must be a positive integer",
                    )
                )
                continue
            valid_references.append((reference_index, reference))
        reference_counts = Counter(reference for _, reference in valid_references)
        for reference in dict.fromkeys(
            reference for _, reference in valid_references
        ):
            if reference_counts[reference] > 1:
                issues.append(
                    _high_issue(
                        f"claim-{claim_number}-reference-{reference}-duplicate",
                        f"claim {claim_number} repeats reference {reference}",
                    )
                )
        seen_references: set[int] = set()
        for _, reference in valid_references:
            if reference in seen_references:
                continue
            seen_references.add(reference)
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
    return _report(issues)


def validate_claim_support(
    claims: object, supported_fact_ids: object
) -> ValidationReport:
    entries, issues = _validated_claim_entries(claims)
    valid_supported_fact_ids: set[str] = set()
    supported_fact_id_values = _stable_values(supported_fact_ids)
    if supported_fact_id_values is None:
        issues.append(
            _high_issue(
                "supported-fact-ids-invalid-structure",
                "supported fact IDs must be an array or set",
            )
        )
    else:
        for index, fact_id in enumerate(supported_fact_id_values):
            if not isinstance(fact_id, str) or not fact_id.strip():
                issues.append(
                    _high_issue(
                        f"supported-fact-id-index-{index}-invalid",
                        f"supported fact ID at index {index} must be non-blank",
                    )
                )
                continue
            valid_supported_fact_ids.add(fact_id.strip())
    entries = _unique_claim_entries(entries)
    for _, claim, claim_number in entries:
        if "features" not in claim:
            issues.append(
                _high_issue(
                    f"claim-{claim_number}-missing-features",
                    f"claim {claim_number} is missing its feature list",
                )
            )
            continue
        features = claim["features"]
        if not isinstance(features, list):
            issues.append(
                _high_issue(
                    f"claim-{claim_number}-invalid-features",
                    f"claim {claim_number} features must be an array",
                )
            )
            continue
        valid_features: list[tuple[int, str]] = []
        for feature_index, feature_id in enumerate(features):
            if not isinstance(feature_id, str) or not feature_id.strip():
                issues.append(
                    _high_issue(
                        f"claim-{claim_number}-feature-index-"
                        f"{feature_index}-invalid",
                        f"claim {claim_number} feature at index {feature_index} "
                        "must be a non-blank string",
                    )
                )
                continue
            valid_features.append((feature_index, feature_id.strip()))
        feature_counts = Counter(feature_id for _, feature_id in valid_features)
        for feature_id in dict.fromkeys(
            feature_id for _, feature_id in valid_features
        ):
            if feature_counts[feature_id] > 1:
                issues.append(
                    _high_issue(
                        f"claim-{claim_number}-feature-{feature_id}-duplicate",
                        f"claim {claim_number} repeats feature {feature_id}",
                    )
                )
        seen_features: set[str] = set()
        for _, feature_id in valid_features:
            if feature_id in seen_features:
                continue
            seen_features.add(feature_id)
            if feature_id not in valid_supported_fact_ids:
                issues.append(
                    ReviewIssue(
                        issue_id=f"unsupported-{claim_number}-{feature_id}",
                        severity="high",
                        message=(
                            f"claim {claim_number} feature {feature_id} "
                            "lacks specification support"
                        ),
                    )
                )
    return _report(issues)
