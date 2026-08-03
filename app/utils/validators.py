"""Reusable validation helper module."""

import re
from collections.abc import Mapping
from datetime import date
from typing import Any, TypeVar

from app.config import (
    ISO_DATE_PATTERN,
    MAX_ACCURACY,
    MAX_TOPIC_NAME_LENGTH,
    MIN_ACCURACY,
    MIN_TOPIC_NAME_LENGTH,
)

T = TypeVar("T")


def normalize_topic_name(value: Any) -> str:
    """Normalize and validate a topic name.

    Args:
        value: Raw topic name supplied by the request.

    Returns:
        Topic name with surrounding whitespace removed and words title-cased.

    Raises:
        ValueError: If the topic name is not a valid non-empty string.

    Example:
        >>> normalize_topic_name(" graphs ")
        'Graphs'
    """
    if not isinstance(value, str):
        raise ValueError("Topic name must be a string.")

    normalized = " ".join(value.strip().split())
    if len(normalized) < MIN_TOPIC_NAME_LENGTH:
        raise ValueError("Topic name must not be empty.")
    if len(normalized) > MAX_TOPIC_NAME_LENGTH:
        raise ValueError("Topic name must be 100 characters or fewer.")
    return normalized.title()


def normalize_required_text(
    value: Any,
    field_name: str,
    min_length: int,
    max_length: int | None = None,
) -> str:
    """Normalize and validate required string fields.

    Args:
        value: Raw text value supplied by the request.
        field_name: Human-readable field name for validation errors.
        min_length: Minimum allowed length after trimming.
        max_length: Optional maximum allowed length after trimming.

    Returns:
        Trimmed text value.

    Raises:
        ValueError: If the value is not a valid string.

    Example:
        >>> normalize_required_text(" student_001 ", "student_id", 1, 100)
        'student_001'
    """
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")

    normalized = value.strip()
    if len(normalized) < min_length:
        raise ValueError(f"{field_name} must not be empty.")
    if max_length is not None and len(normalized) > max_length:
        raise ValueError(f"{field_name} is too long.")
    return normalized


def normalize_topic_mapping(value: Any) -> dict[str, Any]:
    """Normalize topic-keyed dictionaries and reject duplicate topics.

    Args:
        value: Raw mapping with topic names as keys.

    Returns:
        Dictionary with normalized topic names.

    Raises:
        ValueError: If the value is not a mapping or contains duplicate topics
            after normalization.

    Example:
        >>> normalize_topic_mapping({" graphs ": 42})
        {'Graphs': 42}
    """
    if not isinstance(value, Mapping):
        raise ValueError("Expected a topic mapping.")

    normalized: dict[str, Any] = {}
    for raw_topic, raw_value in value.items():
        topic = normalize_topic_name(raw_topic)
        if topic in normalized:
            raise ValueError("Duplicate topic names are not allowed.")
        normalized[topic] = raw_value
    return normalized


def validate_accuracy_mapping_values(value: Mapping[str, Any]) -> None:
    """Validate raw accuracy values before Pydantic coercion.

    Args:
        value: Normalized topic accuracy mapping.

    Returns:
        None.

    Raises:
        ValueError: If an accuracy value is not numeric or is outside range.

    Example:
        >>> validate_accuracy_mapping_values({"Graphs": 42})
    """
    for topic, accuracy in value.items():
        if isinstance(accuracy, bool) or not isinstance(accuracy, int | float):
            raise ValueError(f"Accuracy for {topic} must be numeric.")
        if not MIN_ACCURACY <= accuracy <= MAX_ACCURACY:
            raise ValueError(f"Accuracy for {topic} must be between 0 and 100.")


def validate_iso_date_string(value: Any) -> Any:
    """Validate API date strings before Pydantic date parsing.

    Args:
        value: Raw date value.

    Returns:
        Original value when valid for Pydantic parsing.

    Raises:
        ValueError: If a string date is not in YYYY-MM-DD format.

    Example:
        >>> validate_iso_date_string("2026-08-02")
        '2026-08-02'
    """
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise ValueError("date must be a YYYY-MM-DD string.")
    if re.fullmatch(ISO_DATE_PATTERN, value) is None:
        raise ValueError("date must use YYYY-MM-DD format.")
    date.fromisoformat(value)
    return value


def ensure_topics_have_solving_time(
    topic_accuracy: Mapping[str, T],
    solving_time: Mapping[str, Any],
) -> None:
    """Validate that every scored topic has solving-time data.

    Args:
        topic_accuracy: Normalized topic accuracy mapping.
        solving_time: Normalized solving time mapping.

    Returns:
        None.

    Raises:
        ValueError: If a topic does not have solving-time data.

    Example:
        >>> ensure_topics_have_solving_time({"Graphs": 42}, {"Graphs": "High"})
    """
    missing_topics = sorted(set(topic_accuracy) - set(solving_time))
    if missing_topics:
        missing = ", ".join(missing_topics)
        raise ValueError(f"Missing solving time for topic(s): {missing}.")
