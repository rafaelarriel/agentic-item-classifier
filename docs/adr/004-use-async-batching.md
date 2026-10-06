# ADR 004 — Usar batching assíncrono

**Decisão:** dividir itens e limitar batches por semaphore. **Motivo:** explorar I/O concorrente sem sobrecarregar provider. **Trade-off:** tuning depende de tokens, limites e custo; configurações ficam em ambiente.
