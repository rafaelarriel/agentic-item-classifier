"""Adaptadores de cliente para o protocolo MCP sobre Streamable HTTP."""

import json
from collections.abc import Sequence

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import TextContent

from app.core.config import Settings
from app.core.exceptions import CatalogUnavailableError
from app.schemas.classifier import Category


class CategoryCatalogClient:
    """Cliente pequeno para consultas determinísticas usadas na validação de domínio."""

    def __init__(self, settings: Settings) -> None:
        self._url = str(settings.mcp_server_url)

    async def list_categories(self) -> list[Category]:
        """Consulta `list_categories` no servidor MCP e valida seu contrato."""

        try:
            async with streamablehttp_client(self._url) as (read_stream, write_stream, _):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("list_categories", {})
        except Exception as exc:  # biblioteca MCP expõe erros heterogêneos de transporte
            raise CatalogUnavailableError("Não foi possível consultar o catálogo MCP") from exc

        if result.isError or not result.content:
            raise CatalogUnavailableError("O catálogo MCP respondeu com erro")

        text_contents = [content for content in result.content if isinstance(content, TextContent)]
        if not text_contents:
            raise CatalogUnavailableError("O catálogo MCP não retornou conteúdo textual")

        try:
            payloads = [json.loads(content.text) for content in text_contents]
            # FastMCP pode serializar uma lista como um único bloco ou como vários blocos.
            raw_categories = (
                payloads[0] if len(payloads) == 1 and isinstance(payloads[0], list) else payloads
            )
            return [Category.model_validate(item) for item in raw_categories]
        except (AttributeError, TypeError, ValueError) as exc:
            raise CatalogUnavailableError(
                "Resposta do catálogo MCP possui formato inválido"
            ) from exc


class LangChainMCPToolProvider:
    """Carrega tools MCP em formato que o agente LangChain compreende."""

    def __init__(self, settings: Settings) -> None:
        self._url = str(settings.mcp_server_url)

    async def get_tools(self) -> Sequence[BaseTool]:
        """Converte as tools do servidor remoto para tools LangChain dinamicamente."""

        try:
            client = MultiServerMCPClient(
                {
                    "category_catalog": {
                        "transport": "streamable_http",
                        "url": self._url,
                    }
                }
            )
            return await client.get_tools()
        except Exception as exc:
            raise CatalogUnavailableError("Não foi possível carregar tools MCP") from exc
