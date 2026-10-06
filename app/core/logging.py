"""Logging pequeno, estruturado em JSON e sem dados sensíveis."""

import logging


def configure_logging(level: str) -> None:
    """Configura um formato consistente para API e servidor MCP."""

    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
