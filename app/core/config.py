"""Configuração centralizada, carregada de ambiente e do arquivo .env."""

from functools import lru_cache

from pydantic import Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Valores de infraestrutura e limites operacionais da aplicação."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4.1-mini"
    classifier_batch_size: int = Field(default=20, ge=1, le=100)
    max_concurrent_batches: int = Field(default=5, ge=1, le=20)
    classifier_timeout_seconds: float = Field(default=45, gt=0, le=300)
    classifier_max_retries: int = Field(default=2, ge=0, le=5)
    classifier_retry_base_seconds: float = Field(default=1, gt=0, le=30)
    max_items_per_request: int = Field(default=100, ge=1, le=1000)
    mcp_server_host: str = "127.0.0.1"
    mcp_server_port: int = Field(default=8001, ge=1, le=65535)
    mcp_server_url: HttpUrl = HttpUrl("http://localhost:8001/mcp")
    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Retorna a configuração como singleton para facilitar DI e testes."""

    return Settings()
