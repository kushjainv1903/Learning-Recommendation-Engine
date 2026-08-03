"""Unit tests for explanation generation."""

from app.core.constants import RecommendationType
from app.services.explanation_generator import generate_reason
from app.services.feature_extractor import TopicFeatures


def make_features() -> TopicFeatures:
    """Create feature object for explanation tests.

    Returns:
        Engineered topic features.

    Raises:
        ValueError: If feature values are invalid.
    """
    return TopicFeatures(
        topic="Graphs",
        accuracy=42.0,
        failed_attempts=2,
        mcq_accuracy=80.0,
        coding_success_rate=25.0,
        speed_score=70.0,
        concept_score=42.0,
        implementation_score=50.0,
        consistency_score=45.0,
        learning_priority_score=82.1,
    )


def test_generate_reason_references_actual_metrics() -> None:
    """Verify explanations include topic and measured values.

    Returns:
        None.

    Raises:
        AssertionError: If explanations become generic.
    """
    reason = generate_reason(RecommendationType.REVISE_FUNDAMENTALS, make_features())

    assert "Graphs" in reason
    assert "42%" in reason
    assert "2 failed" in reason


def test_generate_reason_for_implementation_gap_mentions_both_signals() -> None:
    """Verify implementation-gap reasons include MCQ and coding metrics.

    Returns:
        None.

    Raises:
        AssertionError: If implementation explanations lose metrics.
    """
    reason = generate_reason(
        RecommendationType.IMPLEMENTATION_PRACTICE, make_features()
    )

    assert "80%" in reason
    assert "25%" in reason
    assert "implementation gap" in reason
