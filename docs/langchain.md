# LangChain

`LangChainItemClassifierAgent` usa a API atual `create_agent`, `ChatOpenAI`, `ainvoke` e `response_format=AgentBatchOutput`. Não há `AgentExecutor`, chains legadas ou parser de texto manual.

O adaptador `langchain-mcp-adapters` converte tools MCP remotas em tools LangChain. O runtime decide chamar `list_categories` (e, quando útil, as demais tools) e só então devolve o schema Pydantic. O agente é justificável aqui porque o conhecimento vem de tools dinâmicas; para um catálogo estático, `prompt -> modelo -> structured output` seria mais simples e provavelmente preferível.

O modelo padrão é configurável. Use um modelo que suporte tool calling e structured output; confirme disponibilidade em sua conta OpenAI.
