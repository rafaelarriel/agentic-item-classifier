# Testes

Execute `python -m pytest` sem chave OpenAI, Docker ou servidor MCP. Fakes delimitam as fronteiras externas.

- Schemas: vazios, whitespace e IDs duplicados.
- Serviço: divisão, ordenação, erro do LLM, erro MCP e categoria inexistente.
- Agente: chama `create_agent` e envia descrições como JSON, inclusive texto de injection.
- API: health, validação e injeção da dependência do serviço.

Para produção, adicione testes de contrato contra um MCP efêmero, testes de carga e um conjunto versionado de exemplos para avaliar precisão do modelo.
