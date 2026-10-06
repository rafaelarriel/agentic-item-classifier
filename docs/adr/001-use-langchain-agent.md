# ADR 001 — Usar agente LangChain

**Decisão:** usar `create_agent` moderno com tools MCP. **Contexto:** o catálogo é dinâmico. **Consequência:** integração de tools é clara, mas há latência/custo adicional. Para classificação estática, uma chamada direta estruturada é alternativa melhor.
