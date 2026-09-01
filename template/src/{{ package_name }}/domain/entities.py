"""Domain entities. Pure Python only — no third-party imports allowed."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class User:
    """Sample domain entity. Extend or replace with real aggregates."""

    name: str
    email: str
    id: UUID = field(default_factory=uuid4)
