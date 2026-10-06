# Batching assíncrono

Uma request com 100 itens pode ser particionada em cinco batches de 20. `asyncio.gather` agenda trabalho, mas `asyncio.Semaphore(MAX_CONCURRENT_BATCHES)` limita quantos batches chegam ao LLM ao mesmo tempo.

Concorrência ilimitada aumenta rate limits, picos de custo, contenção de conexões e instabilidade. Batches maiores reduzem chamadas, mas elevam tokens, latência e probabilidade de uma resposta inválida afetar mais itens. Os parâmetros ficam em ambiente para ajuste sem alterar código.

O serviço usa backoff exponencial limitado: 1s, 2s, ... até `CLASSIFIER_MAX_RETRIES`. Timeout e retries tornam falhas visíveis no log e terminam em 503; nunca há loop infinito.
