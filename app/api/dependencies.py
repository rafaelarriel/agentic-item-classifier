"""Composição de dependências da aplicação na borda HTTP."""

from functools import lru_cache

from app.agents.item_classifier_agent import LangChainItemClassifierAgent
from app.core.config import get_settings
from app.mcp.client import CategoryCatalogClient, LangChainMCPToolProvider
from app.services.classifier_service import ClassifierService


@lru_cache
def get_classifier_service() -> ClassifierService:
    """Monta o caso de uso com as implementações reais de infraestrutura."""

    settings = get_settings()
    tool_provider = LangChainMCPToolProvider(settings)
    agent = LangChainItemClassifierAgent(settings, tool_provider)
    catalog_client = CategoryCatalogClient(settings)
    return ClassifierService(agent=agent, catalog_client=catalog_client, settings=settings)
