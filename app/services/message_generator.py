"""Tomorrow's Focus message generation service module."""

from datetime import date

from app.config import MAX_FOCUS_TOPICS, MAX_MESSAGE_LENGTH, MOTIVATIONAL_MESSAGES
from app.models.response_models import RecommendationItem


def generate_tomorrows_focus_message(
    recommendations: tuple[RecommendationItem, ...],
    strengths: tuple[str, ...],
    request_date: date,
) -> str:
    """Generate a deterministic Tomorrow's Focus message.

    Args:
        recommendations: Ranked recommendation items.
        strengths: Strength or mastered topics.
        request_date: Request date used for deterministic closing selection.

    Returns:
        Student-facing focus message.

    Raises:
        None.

    Example:
        >>> generate_tomorrows_focus_message((), ("Arrays",), date(2026, 8, 2))
        'Tomorrow\\'s Focus: Great work on Arrays today. Keep building consistency.'
    """
    message_parts = [
        "Tomorrow's Focus:",
        _build_positive_observation(strengths),
        _build_priority_summary(recommendations),
        _select_motivational_closing(request_date),
    ]
    message = " ".join(part for part in message_parts if part)
    return message[:MAX_MESSAGE_LENGTH]


def _build_positive_observation(strengths: tuple[str, ...]) -> str:
    if strengths:
        return f"Great work on {strengths[0]} today."
    return "You have a clear set of improvement areas for tomorrow."


def _build_priority_summary(recommendations: tuple[RecommendationItem, ...]) -> str:
    focus_items = recommendations[:MAX_FOCUS_TOPICS]
    if not focus_items:
        return ""
    actions = "; ".join(item.action for item in focus_items)
    return f"Focus on: {actions}."


def _select_motivational_closing(request_date: date) -> str:
    index = request_date.day % len(MOTIVATIONAL_MESSAGES)
    return MOTIVATIONAL_MESSAGES[index]
