"""Rota de classificação de itens."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_classifier_service
from app.core.config import Settings, get_settings
from app.schemas.classifier import BatchClassifierRequest, BatchClassifierResponse
from app.services.classifier_service import ClassifierService

router = APIRouter(tags=["classifier"])
ClassifierServiceDependency = Annotated[ClassifierService, Depends(get_classifier_service)]
SettingsDependency = Annotated[Settings, Depends(get_settings)]


@router.post(
    "/batch_item_classifier",
    response_model=BatchClassifierResponse,
    status_code=status.HTTP_200_OK,
)
async def batch_item_classifier(
    request: BatchClassifierRequest,
    service: ClassifierServiceDependency,
    settings: SettingsDependency,
) -> BatchClassifierResponse:
    """Classifica a coleção, mantendo os ids e a ordem recebidos."""

    if len(request.items) > settings.max_items_per_request:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"O máximo configurado é {settings.max_items_per_request} itens por request",
        )
    return await service.classify(request.items)
