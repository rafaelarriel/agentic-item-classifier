# ADR 003 — Usar structured output

**Decisão:** saída final em Pydantic via `response_format`. **Motivo:** evita regex/parsing de texto e fornece contrato. **Consequência:** ainda validamos regras semânticas contra o catálogo MCP.
