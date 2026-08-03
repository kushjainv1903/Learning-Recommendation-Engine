"""Unit tests for Tomorrow's Focus message generation."""

from datetime import date

from app.core.constants import RecommendationType
from app.models.response_models import PracticePlan, RecommendationItem
from app.services.message_generator import generate_tomorrows_focus_message


def make_recommendation(topic: str, action: str) -> RecommendationItem:
    """Create a recommendation item for message tests.

    Args:
        topic: Topic name.
        action: Recommendation action.

    Returns:
        Recommendation item.

    Raises:
        pydantic.ValidationError: If the fixture violates response schema.
    """
    return RecommendationItem(
        topic=topic,
        priority=1,
        priority_score=80.0,
        recommendation_type=RecommendationType.REINFORCEMENT_PRACTICE,
        action=action,
        reason=f"{topic} needs practice based on today's metrics.",
        practice_plan=PracticePlan(easy=2, medium=3, hard=0),
    )


def test_generate_message_includes_positive_observation_and_actions() -> None:
    """Verify Tomorrow's Focus message structure.

    Returns:
        None.

    Raises:
        AssertionError: If required message parts are missing.
    """
    recommendations = (
        make_recommendation("Graphs", "Practice Graphs"),
        make_recommendation("DP", "Practice DP"),
    )

    message = generate_tomorrows_focus_message(
        recommendations,
        ("Arrays",),
        date(2026, 8, 2),
    )

    assert message.startswith("Tomorrow's Focus:")
    assert "Great work on Arrays today." in message
    assert "Practice Graphs" in message
    assert "Practice DP" in message


def test_generate_message_is_deterministic_for_same_date() -> None:
    """Verify motivational closing selection is deterministic.

    Returns:
        None.

    Raises:
        AssertionError: If message generation becomes random.
    """
    recommendations = (make_recommendation("Graphs", "Practice Graphs"),)

    first = generate_tomorrows_focus_message(
        recommendations,
        (),
        date(2026, 8, 2),
    )
    second = generate_tomorrows_focus_message(
        recommendations,
        (),
        date(2026, 8, 2),
    )

    assert first == second
