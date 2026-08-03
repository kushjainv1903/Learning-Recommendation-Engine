"""Custom exceptions for application and service boundaries."""

from typing import Any


class LearnPathException(Exception):
    """Base exception for LearnPath AI errors.

    Args:
        message: Safe error message for logs or API responses.
        details: Optional structured error metadata.

    Attributes:
        message: Safe error message.
        details: Structured error metadata.

    Example:
        >>> exc = LearnPathException("Validation failed.", [{"field": "date"}])
        >>> exc.message
        'Validation failed.'
    """

    def __init__(self, message: str, details: list[dict[str, Any]] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or []


class ConfigurationException(LearnPathException):
    """Raised when application configuration is invalid."""


class ValidationException(LearnPathException):
    """Raised when validated input fails domain-level validation."""


class RecommendationException(LearnPathException):
    """Raised when recommendation pipeline execution fails."""
