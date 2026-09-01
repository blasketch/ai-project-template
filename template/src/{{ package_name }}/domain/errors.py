"""Domain error hierarchy shared by every layer."""

from __future__ import annotations


class DomainError(Exception):
    """Base error for domain violations."""


class NotFoundError(DomainError):
    """Raised when an entity lookup fails."""


class ValidationError(DomainError):
    """Raised when a domain invariant is violated."""


class ConflictError(DomainError):
    """Raised when an operation conflicts with existing state."""


class ConfigError(DomainError):
    """Raised when configuration cannot be resolved at boot."""
