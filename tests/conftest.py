"""Fakes reutilizáveis, sem rede ou chamadas reais à OpenAI."""

from app.schemas.classifier import AgentBatchOutput, Category, ItemInput


class FakeCatalogClient:
    def __init__(
        self, categories: list[Category] | None = None, error: Exception | None = None
    ) -> None:
        self.categories = categories or [
            Category(id="electronics", name="Eletrônicos"),
            Category(id="food", name="Alimentos"),
            Category(id="other", name="Outros"),
        ]
        self.error = error

    async def list_categories(self) -> list[Category]:
        if self.error:
            raise self.error
        return self.categories


class FakeAgent:
    def __init__(
        self, output: AgentBatchOutput | None = None, error: Exception | None = None
    ) -> None:
        self.output = output
        self.error = error
        self.calls: list[list[ItemInput]] = []

    async def classify(self, items: list[ItemInput]) -> AgentBatchOutput:
        self.calls.append(items)
        if self.error:
            raise self.error
        assert self.output is not None
        return self.output
