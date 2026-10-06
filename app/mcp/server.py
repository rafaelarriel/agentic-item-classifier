"""Servidor MCP HTTP que expõe o catálogo como ferramentas para agentes."""

from mcp.server.fastmcp import FastMCP

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.mcp.catalog import CATEGORY_EXAMPLES, find_category, list_catalog

settings = get_settings()
mcp = FastMCP(
    "Category Catalog",
    host=settings.mcp_server_host,
    port=settings.mcp_server_port,
    stateless_http=True,
)


@mcp.tool()
def list_categories() -> list[dict[str, str]]:
    """Lista todas as categorias que podem ser usadas para classificar produtos."""

    return [category.model_dump() for category in list_catalog()]


@mcp.tool()
def get_category(category_id: str) -> dict[str, str] | None:
    """Obtém uma categoria pelo seu identificador."""

    category = find_category(category_id)
    return category.model_dump() if category else None


@mcp.tool()
def search_categories(query: str) -> list[dict[str, str]]:
    """Busca categorias por texto no identificador ou nome."""

    normalized = query.casefold().strip()
    return [
        category.model_dump()
        for category in list_catalog()
        if normalized in category.id.casefold() or normalized in category.name.casefold()
    ]


@mcp.tool()
def get_category_examples(category_id: str) -> list[str]:
    """Retorna exemplos breves para desambiguar uma categoria conhecida."""

    return CATEGORY_EXAMPLES.get(category_id, [])


def main() -> None:
    """Inicializa o transporte Streamable HTTP em /mcp."""

    configure_logging(settings.log_level)
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
