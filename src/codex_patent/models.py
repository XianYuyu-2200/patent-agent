from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, model_validator


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


ApprovalName = Literal["technical-solution", "claim-set", "final-delivery"]


class ApprovalScope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claims: str = Field(pattern=r"^v[1-9]\d*$")
    specification: str = Field(pattern=r"^v[1-9]\d*$")
    abstract: str = Field(pattern=r"^v[1-9]\d*$")
    quality_review: str = Field(pattern=r"^v[1-9]\d*$")
    action: Literal["DOCX export"]


class ApprovalRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approval_id: str = Field(min_length=1)
    type: Literal["final-delivery"]
    status: Literal["approved"]
    current: StrictBool
    application_set: str = Field(min_length=1)
    scope: ApprovalScope


class PatentCase(BaseModel):
    schema_version: Literal["1.0"] = "1.0"
    case_id: str
    title: str
    stage: CaseStage = CaseStage.INTAKE
    technical_domain: Literal["mechanical-hardware", "software-ai"] | None = None
    facts: list[TechnicalFact] = Field(default_factory=list)
    artifacts: list[ArtifactRef] = Field(default_factory=list)
    issues: list[ReviewIssue] = Field(default_factory=list)
    approvals: list[ApprovalName | ApprovalRecord] = Field(default_factory=list)
