"""Ponto de entrada ASGI da API FastAPI."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.classifier import router as classifier_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.exceptions import ClassifierError
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Configura recursos leves; conexões MCP são abertas por chamada."""

    configure_logging(get_settings().log_level)
    yield


app = FastAPI(
    title="Agentic Item Classifier",
    version="0.1.0",
    description="Classificação em lote com LangChain, OpenAI e MCP.",
    lifespan=lifespan,
)
app.include_router(health_router)
app.include_router(classifier_router)


@app.exception_handler(ClassifierError)
async def classifier_error_handler(_: Request, exc: ClassifierError) -> JSONResponse:
    """Evita vazar detalhes de provedores e normaliza falhas de dependências."""

    return JSONResponse(status_code=503, content={"detail": str(exc)})
