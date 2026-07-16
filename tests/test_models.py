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
