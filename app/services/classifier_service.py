"""Caso de uso de classificação: batches, concorrência, retry e consolidação."""

import asyncio
import logging
import time
from collections.abc import Iterable, Sequence

from app.agents.item_classifier_agent import ItemClassifier
from app.core.config import Settings
from app.core.exceptions import (
    ClassificationUnavailableError,
    InvalidAgentResponseError,
)
from app.mcp.client import CategoryCatalogClient
from app.schemas.classifier import (
    AgentBatchOutput,
    BatchClassifierResponse,
    Category,
    ClassifiedItem,
    ItemInput,
)

logger = logging.getLogger(__name__)


def split_into_batches(items: Sequence[ItemInput], batch_size: int) -> list[list[ItemInput]]:
    """Divide preservando ordem; função pura para teste e leitura simples."""

    return [list(items[index : index + batch_size]) for index in range(0, len(items), batch_size)]


class ClassifierService:
    """Orquestra a classificação sem conhecer HTTP ou detalhes de LangChain."""

    def __init__(
        self,
        agent: ItemClassifier,
        catalog_client: CategoryCatalogClient,
        settings: Settings,
    ) -> None:
        self._agent = agent
        self._catalog_client = catalog_client
        self._settings = settings

    async def classify(self, items: list[ItemInput]) -> BatchClassifierResponse:
        """Classifica todos os itens ou falha a requisição inteira de modo explícito."""

        started_at = time.perf_counter()
        catalog = await self._catalog_client.list_categories()
        batches = split_into_batches(items, self._settings.classifier_batch_size)
        logger.info("classification_started items=%d batches=%d", len(items), len(batches))
        semaphore = asyncio.Semaphore(self._settings.max_concurrent_batches)

        async def bounded_classify(batch: list[ItemInput]) -> list[ClassifiedItem]:
            async with semaphore:
                output = await self._classify_with_retry(batch)
                return self._validate_and_map(output, batch, catalog)

        try:
            results = await asyncio.gather(*(bounded_classify(batch) for batch in batches))
        except Exception as exc:
            logger.exception("classification_failed items=%d", len(items))
            if isinstance(exc, (ClassificationUnavailableError, InvalidAgentResponseError)):
                raise
            raise ClassificationUnavailableError("A classificação não pôde ser concluída") from exc

        classified_by_id = {item.id: item for batch in results for item in batch}
        ordered_items = [classified_by_id[item.id] for item in items]
        elapsed = time.perf_counter() - started_at
        logger.info(
            "classification_completed items=%d batches=%d duration_seconds=%.3f",
            len(items),
            len(batches),
            elapsed,
        )
        return BatchClassifierResponse(items=ordered_items)

    async def _classify_with_retry(self, batch: list[ItemInput]) -> AgentBatchOutput:
        """Tenta falhas transitórias com backoff exponencial limitado."""

        max_attempts = self._settings.classifier_max_retries + 1
        for attempt in range(1, max_attempts + 1):
            try:
                return await asyncio.wait_for(
                    self._agent.classify(batch),
                    timeout=self._settings.classifier_timeout_seconds,
                )
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                if attempt == max_attempts:
                    raise ClassificationUnavailableError(
                        f"Batch falhou após {max_attempts} tentativa(s)"
                    ) from exc
                delay = self._settings.classifier_retry_base_seconds * (2 ** (attempt - 1))
                logger.warning(
                    "classification_retry batch_size=%d attempt=%d delay_seconds=%.2f error=%s",
                    len(batch),
                    attempt,
                    delay,
                    type(exc).__name__,
                )
                await asyncio.sleep(delay)
        raise AssertionError("fluxo de retry deveria sempre retornar ou lançar")

    @staticmethod
    def _validate_and_map(
        output: AgentBatchOutput,
        source_items: Iterable[ItemInput],
        catalog: Sequence[Category],
    ) -> list[ClassifiedItem]:
        """Garante ids preservados, cobertura completa e categorias publicadas pelo MCP."""

        requested_ids = [item.id for item in source_items]
        received_ids = [item.id for item in output.items]
        if len(received_ids) != len(requested_ids) or set(received_ids) != set(requested_ids):
            raise InvalidAgentResponseError(
                "O agente deve devolver cada id recebido exatamente uma vez"
            )

        categories_by_id = {category.id: category for category in catalog}
        invalid_categories = [
            item.category_id for item in output.items if item.category_id not in categories_by_id
        ]
        if invalid_categories:
            raise InvalidAgentResponseError(
                "O agente retornou uma categoria inexistente no catálogo MCP"
            )

        classified_by_id = {
            item.id: ClassifiedItem(id=item.id, category=categories_by_id[item.category_id])
            for item in output.items
        }
        return [classified_by_id[item_id] for item_id in requested_ids]
