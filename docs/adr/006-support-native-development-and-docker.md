# ADR 006 — Suportar desenvolvimento nativo e Docker

**Decisão:** Python nativo é caminho principal; Docker Compose é opcional. **Motivo:** Windows sem Docker é requisito e reduz atrito de estudo. **Parity:** código, MCP HTTP e variáveis são os mesmos. Apenas infraestrutura muda: local usa `localhost`; containers usam DNS `mcp-server`, porque localhost no container é o próprio processo.
