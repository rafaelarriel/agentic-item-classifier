"""Endpoint de saúde sem dependências externas."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Indica que o processo HTTP está em execução."""

    return {"status": "ok"}
