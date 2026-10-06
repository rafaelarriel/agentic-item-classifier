"""Agente LangChain com tool calling MCP e resposta validada por Pydantic."""

import json
from typing import Protocol

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.mcp.client import LangChainMCPToolProvider
from app.prompts.item_classifier_prompt import SYSTEM_PROMPT
from app.schemas.classifier import AgentBatchOutput, ItemInput


class ItemClassifier(Protocol):
    """Contrato que torna o serviço independente do provedor de classificação."""

    async def classify(self, items: list[ItemInput]) -> AgentBatchOutput:
        """Classifica um batch e devolve somente ids e ids de categoria."""


class LangChainItemClassifierAgent:
    """Cria por chamada um agente com as tools MCP atuais e structured output."""

    def __init__(self, settings: Settings, tool_provider: LangChainMCPToolProvider) -> None:
        self._settings = settings
        self._tool_provider = tool_provider

    async def classify(self, items: list[ItemInput]) -> AgentBatchOutput:
        """Executa o ciclo agente -> tool calls MCP -> resposta estruturada."""

        api_key = self._settings.openai_api_key
        if api_key is None or not api_key.get_secret_value():
            raise ValueError("OPENAI_API_KEY não está configurada")

        model = ChatOpenAI(
            model=self._settings.openai_model,
            api_key=api_key.get_secret_value(),
            temperature=0,
            timeout=self._settings.classifier_timeout_seconds,
        )
        tools = await self._tool_provider.get_tools()
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            response_format=AgentBatchOutput,
        )
        # JSON separa dados de instruções e reduz o risco de a descrição virar prompt.
        input_payload = json.dumps(
            {"items": [item.model_dump() for item in items]}, ensure_ascii=False
        )
        result = await agent.ainvoke({"messages": [{"role": "user", "content": input_payload}]})
        output = result["structured_response"]
        return AgentBatchOutput.model_validate(output)
