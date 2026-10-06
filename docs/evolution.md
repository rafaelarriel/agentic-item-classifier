# Evolução para produção

O catálogo em memória favorece estudo. Evolua para banco/versionamento com cache e invalidação; mantenha a interface MCP. Adicione autenticação, quotas, circuit breaker para MCP/OpenAI, métricas (latência, tokens, erros), tracing, DLQ ou workflow assíncrono para lotes grandes e resultados parciais explicitamente modelados.

Para qualidade, mantenha um dataset rotulado, avalie precisão por categoria e monitore drift. Para escala, APIs devem ser stateless, múltiplas réplicas devem compartilhar limites distribuídos e a configuração de concorrência deve respeitar rate limits por organização/modelo.
