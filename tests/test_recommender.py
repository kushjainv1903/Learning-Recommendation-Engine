"""Unit tests for recommendation generation."""

from app.core.constants import ClassificationLabel, RecommendationType
from app.services.feature_extractor import TopicFeatures
from app.services.recommender import (
    generate_recommendations,
    select_recommendation_type,
)
from app.services.scorer import ScoredTopic


def make_scored_topic(
    topic: str = "Graphs",
    classification: ClassificationLabel = ClassificationLabel.WEAK,
    accuracy: float = 42.0,
    failed_attempts: int = 2,
    mcq_accuracy: float | None = None,
    coding_success_rate: float | None = None,
    speed_score: float = 70.0,
    priority_score: float = 80.0,
) -> ScoredTopic:
    """Create a scored topic for recommender tests.

    Args:
        topic: Topic name.
        classification: Topic classification.
        accuracy: Topic accuracy.
        failed_attempts: Failed coding attempts.
        mcq_accuracy: Optional MCQ accuracy.
        coding_success_rate: Optional coding success rate.
        speed_score: Numeric solving-time score.
        priority_score: Learning priority score.

    Returns:
        Scored topic.

    Raises:
        ValueError: If feature values are invalid.
    """
    return ScoredTopic(
        features=TopicFeatures(
            topic=topic,
            accuracy=accuracy,
            failed_attempts=failed_attempts,
            mcq_accuracy=mcq_accuracy,
            coding_success_rate=coding_success_rate,
            speed_score=speed_score,
            concept_score=accuracy,
            implementation_score=None,
            consistency_score=None,
            learning_priority_score=priority_score,
        ),
        classification=classification,
        priority_score=priority_score,
    )


def test_revise_fundamentals_wins_for_weak_repeated_failures() -> None:
    """Verify repeated weak failures select fundamentals revision.

    Returns:
        None.

    Raises:
        AssertionError: If conflict ordering changes.
    """
    scored_topic = make_scored_topic(failed_attempts=2)

    assert select_recommendation_type(scored_topic) is (
        RecommendationType.REVISE_FUNDAMENTALS
    )


def test_implementation_gap_selects_implementation_practice() -> None:
    """Verify high MCQ and low coding selects implementation practice.

    Returns:
        None.

    Raises:
        AssertionError: If implementation gap detection changes.
    """
    scored_topic = make_scored_topic(
        failed_attempts=1,
        mcq_accuracy=90.0,
        coding_success_rate=20.0,
    )

    assert select_recommendation_type(scored_topic) is (
        RecommendationType.IMPLEMENTATION_PRACTICE
    )


def test_theory_gap_selects_theory_revision() -> None:
    """Verify low MCQ and good coding selects theory revision.

    Returns:
        None.

    Raises:
        AssertionError: If theory gap detection changes.
    """
    scored_topic = make_scored_topic(
        failed_attempts=1,
        mcq_accuracy=40.0,
        coding_success_rate=90.0,
    )

    assert (
        select_recommendation_type(scored_topic) is RecommendationType.THEORY_REVISION
    )


def test_structured_practice_selected_for_low_accuracy_few_attempts() -> None:
    """Verify low accuracy with few failures selects structured practice.

    Returns:
        None.

    Raises:
        AssertionError: If structured practice rules change.
    """
    scored_topic = make_scored_topic(failed_attempts=0)

    assert select_recommendation_type(scored_topic) is (
        RecommendationType.STRUCTURED_PRACTICE
    )


def test_speed_practice_selected_for_strong_high_time_topic() -> None:
    """Verify strong slow topics select speed practice.

    Returns:
        None.

    Raises:
        AssertionError: If speed-practice rules change.
    """
    scored_topic = make_scored_topic(
        classification=ClassificationLabel.STRONG,
        accuracy=82.0,
        failed_attempts=0,
        speed_score=70.0,
    )

    assert select_recommendation_type(scored_topic) is RecommendationType.SPEED_PRACTICE


def test_generate_recommendations_includes_required_fields() -> None:
    """Verify generated recommendations include action, priority, reason, plan.

    Returns:
        None.

    Raises:
        AssertionError: If required recommendation fields are absent.
    """
    recommendations = generate_recommendations((make_scored_topic(),))

    assert recommendations[0].action
    assert recommendations[0].priority == 1
    assert recommendations[0].reason
    assert recommendations[0].practice_plan.easy == 3
    assert recommendations[0].practice_plan.medium == 3


def test_generate_recommendations_returns_strength_fallback() -> None:
    """Verify all-strong inputs return one positive recommendation.

    Returns:
        None.

    Raises:
        AssertionError: If positive fallback disappears.
    """
    strong_topic = make_scored_topic(
        classification=ClassificationLabel.STRONG,
        accuracy=88.0,
        failed_attempts=0,
        speed_score=30.0,
    )

    recommendations = generate_recommendations((strong_topic,))

    assert len(recommendations) == 1
    assert (
        recommendations[0].recommendation_type is RecommendationType.MAINTAIN_STRENGTH
    )
