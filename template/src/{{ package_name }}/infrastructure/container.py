"""Composition root: wires settings, logging, and use-case registry.

Vanilla container — no external DI framework. Extend by registering
factories (e.g. repositories, sessions) via `register`/`resolve`.
"""

from ..application import CreateUser
from .config.settings import Settings, get_settings
from .logging import configure_logging


class Container:
    """Holds resolved settings and a use-case registry."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.use_cases: dict[str, object] = {}

    def register(self, name: str, instance: object) -> None:
        self.use_cases[name] = instance

    def resolve(self, name: str) -> object:
        return self.use_cases[name]


def build_container(settings: Settings) -> Container:
    """Bootstrap the application composition root."""
    configure_logging(settings.logging)
    container = Container(settings=settings)
    container.register("create_user", CreateUser())
    return container


def get_container() -> Container:
    """Composition root entrypoint used by presentation layers."""
    return build_container(get_settings())
