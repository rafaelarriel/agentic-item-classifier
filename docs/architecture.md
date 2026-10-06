# Arquitetura

O projeto usa camadas pequenas e dependências apontando para dentro: rotas traduzem HTTP, `ClassifierService` contém o caso de uso, o agente isola LangChain/OpenAI e `mcp/` isola o protocolo de catálogo. Schemas Pydantic são contratos compartilhados, não regras de infraestrutura.

```text
POST /batch_item_classifier
  -> validação Pydantic
  -> catálogo MCP (validação de IDs)
  -> N batches com semaphore
  -> agente LangChain / tools MCP / OpenAI
  -> validação de cobertura, IDs e categorias
  -> resposta na ordem original
```

O catálogo não aparece no prompt como lista fixa. A API falha a requisição inteira se um batch falhar: evita retornar uma coleção parcialmente classificada sem contrato explícito de parcialidade. Veja os ADRs para alternativas deliberadamente não adotadas.
