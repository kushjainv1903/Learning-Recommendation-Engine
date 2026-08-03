"""Shared constants for domain labels and API conventions."""

from enum import StrEnum


class RecommendationType(StrEnum):
    """Supported recommendation type names.

    Example:
        >>> RecommendationType.STRUCTURED_PRACTICE.value
        'Structured Practice'
    """

    REVISE_FUNDAMENTALS = "Revise Fundamentals"
    STRUCTURED_PRACTICE = "Structured Practice"
    IMPLEMENTATION_PRACTICE = "Implementation Practice"
    THEORY_REVISION = "Theory Revision"
    SPEED_PRACTICE = "Speed Practice"
    REINFORCEMENT_PRACTICE = "Reinforcement Practice"
    MAINTAIN_STRENGTH = "Maintain Strength"


class ClassificationLabel(StrEnum):
    """Supported topic classification labels.

    Example:
        >>> ClassificationLabel.CRITICAL.value
        'Critical'
    """

    MASTERED = "Mastered"
    STRONG = "Strong"
    MODERATE = "Moderate"
    WEAK = "Weak"
    CRITICAL = "Critical"


class AttemptResult(StrEnum):
    """Allowed coding attempt result labels.

    Example:
        >>> AttemptResult.INCORRECT.value
        'incorrect'
    """

    CORRECT = "correct"
    INCORRECT = "incorrect"


class SolvingTimeLevel(StrEnum):
    """Supported solving time labels from the API contract.

    Example:
        >>> SolvingTimeLevel.HIGH.value
        'High'
    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "Very High"


class PriorityLevel(StrEnum):
    """Human-readable priority labels for response models.

    Example:
        >>> PriorityLevel.HIGH.value
        'High'
    """

    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    MINIMAL = "Minimal"
