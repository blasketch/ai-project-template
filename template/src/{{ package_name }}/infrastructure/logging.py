"""Structlog-over-stdlib logging: dev console renderer, prod JSON.

A redaction processor scrubs configured secret patterns from every event.
"""

import logging
import re
import sys

import structlog
from structlog.stdlib import ProcessorFormatter
from structlog.types import EventDict, WrappedLogger

from ..domain import ConfigError
from .config.settings import LoggingSettings


def _redact(patterns: list[str]):
    """Build a processor that replaces matches of each pattern with ***."""
    compiled = [re.compile(p, re.IGNORECASE) for p in patterns]

    def processor(
        logger: WrappedLogger, method: str, event_dict: EventDict
    ) -> EventDict:
        for key, value in event_dict.items():
            if isinstance(value, str):
                for pattern in compiled:
                    value = pattern.sub("***", value)
                event_dict[key] = value
        return event_dict

    return processor


def _renderer(json_format: bool):
    if json_format:
        return structlog.processors.JSONRenderer()
    return structlog.dev.ConsoleRenderer()


def _numeric_level(level: str) -> int:
    match = logging.getLevelNamesMapping().get(level.upper())
    if match is None:
        msg = f"Unknown log level: {level}"
        raise ConfigError(msg)
    return match


def configure_logging(config: LoggingSettings) -> None:
    """Configure stdlib + structlog from the settings section."""
    level = _numeric_level(config.level)
    renderer = _renderer(config.json_format)
    redactor = _redact(config.redaction_patterns)

    shared = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        redactor,
    ]

    formatter = ProcessorFormatter(
        foreign_pre_chain=shared,
        processors=[
            ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)

    structlog.configure(
        processors=[
            *shared,
            ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=False,
    )
