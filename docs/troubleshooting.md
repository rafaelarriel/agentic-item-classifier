# Troubleshooting

| Sintoma | Solução |
|---|---|
| `python` não encontrado | Reinstale Python 3.11+ marcando PATH; reabra o terminal. |
| `pip` não encontrado | Use `python -m pip`, após confirmar `python --version`. |
| `Activate.ps1` bloqueado | Use CMD (`.venv\Scripts\activate.bat`) ou execute `.venv\Scripts\python.exe` diretamente. Não reduza a política global sem entender a política corporativa. |
| venv não parece ativa | Confirme que o prompt mostra `(.venv)` ou execute o Python explícito da venv. |
| Porta 8000/8001 ocupada | Encerre o processo que a usa ou ajuste `API_PORT`/`MCP_SERVER_PORT` e a URL MCP coerentemente. |
| `.env` não carregado | Confirme que ele está na raiz e foi copiado de `.env.example`; reinicie os processos. |
| chave OpenAI ausente | Preencha `OPENAI_API_KEY` em `.env`; não use aspas/copias parciais. |
| API não acessa MCP | Primeiro abra/inicie o MCP; localmente use `http://localhost:8001/mcp`, no Compose `http://mcp-server:8001/mcp`. |
| `ModuleNotFoundError` | Ative a venv e rode `pip install -e ".[dev]"` na raiz. |
| certificado/rede | Verifique proxy/VPN/firewall corporativo e o acesso HTTPS à OpenAI; não desative validação TLS. |
| versão Python incompatível | Use 3.11+ e recrie `.venv`. |

Para observar apenas disponibilidade HTTP, `GET /health` não chama OpenAI ou MCP. Para testar a integração real, use uma classificação após subir ambos os processos.
