# Structured output

`AgentBatchOutput` é o contrato final do LLM: cada elemento possui `id` e `category_id`. LangChain envia o schema ao provedor via `response_format`; Pydantic valida a estrutura recebida. Não há regex ou parsing de prosa.

Depois disso, o serviço valida invariantes de negócio que schema sozinho não conhece: todos os IDs da entrada aparecem uma vez, nenhum foi alterado e cada categoria está no catálogo MCP atual. Por fim, nomes de categorias vêm do catálogo, e não do modelo.
