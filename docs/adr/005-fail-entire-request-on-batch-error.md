# ADR 005 — Falhar request em erro de batch

**Decisão:** não retornar resultados parciais. **Motivo:** contrato simples e sem ambiguidade para consumidor. **Trade-off:** um batch indisponível impede resposta completa; produção pode oferecer modo assíncrono/parcial explicitamente modelado.
