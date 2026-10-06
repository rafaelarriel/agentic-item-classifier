from fastapi.testclient import TestClient

from app.api.dependencies import get_classifier_service
from app.main import app
from app.schemas.classifier import BatchClassifierResponse, Category, ClassifiedItem


class SuccessfulService:
    async def classify(self, _items: list[object]) -> BatchClassifierResponse:
        return BatchClassifierResponse(
            items=[
                ClassifiedItem(id="123", category=Category(id="electronics", name="Eletrônicos"))
            ]
        )


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_classifier_endpoint_with_dependency_override() -> None:
    app.dependency_overrides[get_classifier_service] = lambda: SuccessfulService()
    try:
        with TestClient(app) as client:
            response = client.post(
                "/batch_item_classifier",
                json={"items": [{"id": "123", "description": "Smartphone"}]},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["items"][0]["id"] == "123"


def test_classifier_endpoint_rejects_duplicate_ids() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/batch_item_classifier",
            json={"items": [{"id": "1", "description": "A"}, {"id": "1", "description": "B"}]},
        )
    assert response.status_code == 422
