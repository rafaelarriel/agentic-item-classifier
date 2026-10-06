"""Exceções de negócio mapeadas pela camada HTTP."""


class ClassifierError(Exception):
    """Falha esperada durante o fluxo de classificação."""


class CatalogUnavailableError(ClassifierError):
    """O catálogo MCP não pôde ser consultado."""


class ClassificationUnavailableError(ClassifierError):
    """LLM ou agente não concluiu a classificação após as tentativas."""


class InvalidAgentResponseError(ClassifierError):
    """Saída estruturada não satisfaz as invariantes do domínio."""
