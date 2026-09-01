"""Request/response DTOs passed across application boundaries."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateUserRequest:
    """Input for the CreateUser use case."""

    name: str
    email: str


@dataclass(frozen=True)
class UserResponse:
    """User data exposed to callers."""

    id: UUID
    name: str
    email: str
