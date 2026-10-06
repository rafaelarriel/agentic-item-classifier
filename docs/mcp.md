# MCP — Model Context Protocol

MCP padroniza como um cliente de IA descobre e invoca ferramentas. O servidor deste projeto expõe `list_categories`, `get_category`, `search_categories` e `get_category_examples` via Streamable HTTP em `/mcp`. Ele funciona no Windows e em containers sem subprocessos Unix.

O agente recebe tools por `langchain-mcp-adapters`; em paralelo, `CategoryCatalogClient` usa MCP para obter o catálogo e validar a saída. Portanto uma categoria inventada pelo LLM é rejeitada antes da resposta HTTP.

REST poderia expor os mesmos dados, mas exigiria integrar um contrato específico para cada cliente de agente. MCP padroniza descoberta, schema e invocação de tools. Colocar categorias no prompt seria menor para um demo estático, mas acoplaria conhecimento à versão do código, desperdiçaria tokens e não permitiria atualização independente.
