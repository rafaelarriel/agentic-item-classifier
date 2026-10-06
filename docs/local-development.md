# Desenvolvimento local

## Windows (suportado oficialmente)

Instale Python 3.11+ pelo instalador oficial e marque a opção para adicioná-lo ao PATH. Em PowerShell, na raiz:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
```

Preencha `OPENAI_API_KEY` no `.env`. No CMD, a ativação é `.venv\Scripts\activate.bat`.

Abra dois terminais ativados. No primeiro, `python -m app.mcp.server`; no segundo, `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`. Acesse `http://localhost:8000/docs` e rode `python -m pytest` / `ruff check .`.

`run_*.ps1` são atalhos opcionais. Caso `Activate.ps1` seja bloqueado, use CMD ou execute `.venv\Scripts\python.exe -m pip install -e ".[dev]"` e `.venv\Scripts\python.exe -m uvicorn app.main:app --reload`; não é necessário alterar política global.

Finalize os processos com `Ctrl+C` em cada terminal.

## Linux/macOS

Troque a ativação por `source .venv/bin/activate`; os demais comandos Python são iguais.
