# Docker

Docker é uma segunda forma de executar a mesma imagem e o mesmo código:

```text
Host
 ├─ :8000 -> classifier-api
 └─ :8001 -> mcp-server
```

Crie `.env`, preencha `OPENAI_API_KEY` e execute `docker compose up --build`. No Compose, `classifier-api` usa `MCP_SERVER_URL=http://mcp-server:8001/mcp`: `mcp-server` é o DNS interno do serviço. Já `localhost` dentro do container aponta para aquele próprio container, não para seu Windows nem para o outro serviço.

Não há implementação Docker-específica: ambiente e rede são as únicas diferenças. Pare com `docker compose down`.
