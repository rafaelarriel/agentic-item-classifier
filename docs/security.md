# Segurança

Segredos só vêm de ambiente e `.env` é ignorado pelo Git. Nunca registre `OPENAI_API_KEY`, payloads completos ou respostas brutas. Em produção, use secret manager, TLS, autenticação/autorização na API, rate limit, limites por tenant e observabilidade com dados minimizados.

Descrição de produto é entrada não confiável. O prompt ordena que instruções nela sejam tratadas como dados e o agente recebe JSON, mas prompt injection não é resolvido apenas por prompt. As proteções decisivas são allowlist de tools, catálogo MCP controlado, saída Pydantic e validação de IDs/categorias no serviço. Considere moderação e limites mais rígidos conforme o domínio.
