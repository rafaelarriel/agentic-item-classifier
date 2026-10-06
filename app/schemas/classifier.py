"""Schemas de entrada, saída e comunicação interna da classificação."""

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ItemInput(BaseModel):
    """Produto recebido pela API; seu identificador é opaco para o classificador."""

    id: str = Field(min_length=1, max_length=128)
    description: str = Field(min_length=1, max_length=2_000)

    @field_validator("id", "description")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        """Impede valores visualmente preenchidos, mas semanticamente vazios."""

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("não pode ser vazio ou conter apenas espaços")
        return cleaned


class BatchClassifierRequest(BaseModel):
    """Request da rota de classificação em lote."""

    items: list[ItemInput] = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def ids_must_be_unique(self) -> "BatchClassifierRequest":
        """Evita ambiguidade ao consolidar batches concorrentes."""

        ids = [item.id for item in self.items]
        if len(ids) != len(set(ids)):
            raise ValueError("ids dos itens devem ser únicos no mesmo request")
        return self


class Category(BaseModel):
    """Categoria publicada pelo catálogo MCP."""

    id: str = Field(min_length=1, max_length=64, pattern=r"^[a-z0-9_-]+$")
    name: str = Field(min_length=1, max_length=100)


class ClassifiedItem(BaseModel):
    """Resultado público de um único produto."""

    id: str
    category: Category


class BatchClassifierResponse(BaseModel):
    """Resposta consolidada, preservando a ordem da entrada."""

    items: list[ClassifiedItem]


class AgentClassification(BaseModel):
    """Saída mínima que o agente deve produzir por produto."""

    id: str
    category_id: str


class AgentBatchOutput(BaseModel):
    """Structured output exigido do agente LangChain."""

    model_config = ConfigDict(extra="forbid")

    items: list[AgentClassification]
