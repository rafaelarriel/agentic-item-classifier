# Agentic Item Classifier

Projeto de estudo e portfólio: uma API FastAPI que classifica produtos em batches usando um agente LangChain, OpenAI, saída estruturada Pydantic e ferramentas de um servidor MCP independente.

> Docker é opcional. A aplicação completa funciona nativamente com Python no Windows.

## Arquitetura

```text
Client -> FastAPI -> ClassifierService -> LangChain agent -> OpenAI
                                   |                 |
                                   +-> MCP catalog <-+
```

O serviço busca o catálogo MCP uma vez para validar a resposta. O agente recebe as mesmas ferramentas via `langchain-mcp-adapters` e deve consultá-las antes de produzir structured output.

## Executar localmente no Windows

Pré-requisito: Python 3.11+ instalado e disponível como `python`.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
```

Preencha `OPENAI_API_KEY` em `.env`. No CMD, ative com `.venv\Scripts\activate.bat`.

Terminal 1:

```powershell
python -m app.mcp.server
```

Terminal 2:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Abra <http://localhost:8000/docs>. Os atalhos opcionais são `./scripts/run_mcp.ps1` e `./scripts/run_api.ps1`; os comandos Python acima não dependem de política de execução do PowerShell.

Exemplo:

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/batch_item_classifier -ContentType 'application/json' -Body '{"items":[{"id":"123","description":"Smartphone Samsung Galaxy S24 256GB"},{"id":"456","description":"Arroz branco tipo 1 pacote 5kg"}]}'
```

## Testes e qualidade

```powershell
python -m pytest
ruff check .
mypy app
```

`make test` e `make lint` são somente atalhos opcionais para quem usa Make.

## Docker (alternativa)

Depois de criar `.env` com `OPENAI_API_KEY`:

```bash
docker compose up --build
```

No Compose, a única diferença é a configuração: a API usa `http://mcp-server:8001/mcp`, pois `localhost` em um container significa o próprio container.

## Documentação

- [Arquitetura](docs/architecture.md), [desenvolvimento local](docs/local-development.md), [Docker](docs/docker.md)
- [LangChain](docs/langchain.md), [MCP](docs/mcp.md), [batching assíncrono](docs/async-batching.md), [structured output](docs/structured-output.md)
- [testes](docs/testing.md), [segurança](docs/security.md), [troubleshooting](docs/troubleshooting.md)
- [guia de entrevista](docs/interview-guide.md), [evolução](docs/evolution.md), [avaliação](docs/evaluation.md), [plano de commits](docs/commit-plan.md)
- [ADRs](docs/adr/)

Comece pelo [STUDY_GUIDE.md](STUDY_GUIDE.md).
