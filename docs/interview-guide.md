# Guia de entrevista

1. **Por que FastAPI?** Tipagem, validação Pydantic, ASGI e documentação OpenAPI automática.
2. **Por que separar rota e serviço?** HTTP fica fino; o caso de uso é testável sem servidor.
3. **Por que Pydantic?** Define contratos, valida entrada/saída e reduz estados inválidos.
4. **Por que LangChain?** Uniformiza modelo, tools e structured output em uma integração legível.
5. **O problema precisa de agent?** Não necessariamente; com catálogo fixo, chamada estruturada direta é mais simples.
6. **Quando o agent se justifica?** Quando precisa descobrir/usar ferramentas e conhecimento dinâmico via MCP.
7. **O que é MCP?** Um protocolo para descoberta e chamada de tools por clientes de IA.
8. **MCP versus REST?** REST é API geral; MCP padroniza contrato/tooling para agentes.
9. **Por que não hard-code categorias?** Atualização independente, menos acoplamento e validação no catálogo atual.
10. **Por que Streamable HTTP?** É servidor-servidor, multiplataforma e serve local/Docker.
11. **Por que structured output?** Evita interpretar prosa e torna resposta validável.
12. **Por que ainda validar após structured output?** Schema não prova que IDs pertencem ao request nem que a categoria existe.
13. **Como IDs são preservados?** O serviço compara conjuntos e reconstrói resultado na ordem original.
14. **Por que batching?** Controla tokens e número de chamadas sem serializar tudo.
15. **Por que asyncio?** Chamadas de rede esperam I/O; o loop atende outros batches nesse intervalo.
16. **Por que semaphore?** Evita concorrência ilimitada, rate limits, custos e instabilidade.
17. **Como escolher tamanho do batch?** Medindo tokens, precisão, latência e limites do modelo.
18. **Como funciona retry?** Tentativas limitadas com backoff exponencial; cancelamento é propagado.
19. **Por que falhar request inteira?** O contrato atual exige lote completo; parcialidade requer schema e idempotência próprios.
20. **Como erros chegam ao cliente?** Falhas esperadas viram 503 sem expor detalhes do provedor.
21. **Como observabilidade funciona?** Logs registram contagem, batches, duração e retries, nunca segredos/payloads inteiros.
22. **Como testa sem pagar LLM?** Fakes/mocks nas fronteiras; testes de contrato separados e opcionais.
23. **Como trata prompt injection?** Entrada é delimitada como JSON, prompt trata texto como dado, tools são controladas e output é validado.
24. **O que ocorre se MCP cair?** A classificação falha claramente com 503; não uso catálogo stale silencioso.
25. **E se OpenAI rate-limit?** Retry limitado reduz falhas transitórias; concorrência/configuração deve ser ajustada ao limite.
26. **Como escalar?** Processos stateless, réplicas, limite distribuído, fila para lotes longos e métricas.
27. **Como proteger a API?** Auth, TLS, rate limit por cliente, secret manager e logs minimizados.
28. **O que mudaria em produção?** Catálogo persistido/versionado, circuit breaker, tracing, avaliações e SLOs.
29. **Por que Docker não é obrigatório?** A aplicação é Python puro e Windows é ambiente de desenvolvimento suportado.
30. **Como mantém parity?** Mesma imagem/código; somente URLs, bind host e networking variam por configuração.
