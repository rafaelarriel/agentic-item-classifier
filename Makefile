.PHONY: test lint run-api run-mcp

test:
	python -m pytest

lint:
	ruff check .

run-api:
	uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

run-mcp:
	python -m app.mcp.server
