# Roteiro de estudo

1. `app/main.py` — veja composição FastAPI, lifespan e handlers. Pergunta: por que a rota não conhece OpenAI?
2. `app/schemas/classifier.py` — examine contratos e validação. Pergunta: como IDs duplicados tornariam a consolidação ambígua?
3. `app/api/routes/classifier.py` — veja HTTP, DI e status. Pergunta: por que o endpoint é `async`?
4. `app/services/classifier_service.py` — estude batching, semaphore, retries e invariantes. Pergunta: por que preservar a ordem no fim?
5. `app/agents/item_classifier_agent.py` — acompanhe `create_agent`, tool calling e `response_format`. Pergunta: quando esse agente seria excessivo?
6. `app/prompts/item_classifier_prompt.py` — observe delimitação de dados e defesa contra injection. Pergunta: um prompt basta como controle de segurança?
7. `app/mcp/server.py` — execute e inspecione as quatro tools. Pergunta: por que o catálogo é processo separado?
8. `app/mcp/client.py` — compare o cliente de validação com o adaptador LangChain. Pergunta: por que ambos usam MCP?
9. Volte ao batching e altere `CLASSIFIER_BATCH_SIZE`. Pergunta: que trade-off isso cria em tokens e custo?
10. `tests/` — comece pelos fakes e depois pelos casos negativos. Pergunta: quais fronteiras não devem tocar OpenAI real?

Depois, leia os ADRs e tente defender (ou contestar) cada decisão sem olhar as respostas.
