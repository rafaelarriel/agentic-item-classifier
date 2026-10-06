import pytest
from pydantic import ValidationError

from app.schemas.classifier import BatchClassifierRequest


def test_request_rejects_duplicate_ids() -> None:
    with pytest.raises(ValidationError, match="únicos"):
        BatchClassifierRequest.model_validate(
            {"items": [{"id": "1", "description": "A"}, {"id": "1", "description": "B"}]}
        )


def test_request_rejects_blank_description() -> None:
    with pytest.raises(ValidationError, match="não pode ser vazio"):
        BatchClassifierRequest.model_validate({"items": [{"id": "1", "description": "  "}]})


def test_request_strips_text_fields() -> None:
    request = BatchClassifierRequest.model_validate(
        {"items": [{"id": "  1 ", "description": " arroz "}]}
    )
    assert request.items[0].id == "1"
    assert request.items[0].description == "arroz"
