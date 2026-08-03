"""Unit tests for recommendation engine orchestration."""

from app.core.constants import ClassificationLabel, RecommendationType
from app.models.request_models import RecommendationRequest
from app.services.feature_extractor import extract_topic_features
from app.services.recommendation_engine import (
    build_feature_summary,
    generate_learning_recommendations,
    identify_strengths,
)


def make_request() -> RecommendationRequest:
    """Create a validated request for orchestration tests.

    Returns:
        Validated recommendation request.

    Raises:
        pydantic.ValidationError: If fixture data violates request rules.

    Example:
        >>> make_request().student_id
        'student_001'
    """
    return RecommendationRequest.model_validate(
        {
            "student_id": "student_001",
            "date": "2026-08-02",
            "topic_accuracy": {
                "Arrays": 92,
                "Sliding Window": 35,
                "Graphs": 42,
                "Dynamic Programming": 28,
            },
            "coding_attempts": [
                {
                    "topic": "Sliding Window",
                    "problem": "Longest Substring",
                    "attempts": 3,
                    "result": "incorrect",
                },
                {
                    "topic": "Graphs",
                    "problem": "Graph BFS",
                    "attempts": 2,
                    "result": "incorrect",
                },
            ],
            "mcq_results": {
                "Arrays": {
                    "correct": 9,
                    "total": 10,
                },
                "Graphs": {
                    "correct": 8,
                    "total": 10,
                },
            },
            "average_solving_time": {
                "Arrays": "Low",
                "Sliding Window": "High",
                "Graphs": "High",
                "Dynamic Programming": "Medium",
            },
        }
    )


def test_generate_learning_recommendations_returns_response_contract() -> None:
    """Verify the orchestrator produces the expected response structure.

    Returns:
        None.

    Raises:
        AssertionError: If the pipeline response contract changes.
    """
    response = generate_learning_recommendations(make_request())

    assert response.success is True
    assert response.student_id == "student_001"
    assert response.generated_at == "2026-08-02T00:00:00Z"
    assert response.topic_classification["Arrays"] is ClassificationLabel.MASTERED
    assert response.topic_classification["Sliding Window"] is (
        ClassificationLabel.CRITICAL
    )
    assert response.strengths == ["Arrays"]
    assert response.recommendations
    for recommendation in response.recommendations:
        assert recommendation.action
        assert recommendation.priority > 0
        assert recommendation.reason
        assert recommendation.practice_plan


def test_generate_learning_recommendations_is_deterministic() -> None:
    """Verify identical input produces identical output.

    Returns:
        None.

    Raises:
        AssertionError: If orchestration becomes non-deterministic.
    """
    first = generate_learning_recommendations(make_request())
    second = generate_learning_recommendations(make_request())

    assert first == second


def test_orchestrator_uses_engineered_priority_for_ordering() -> None:
    """Verify recommendations are ordered by engineered priority score.

    Returns:
        None.

    Raises:
        AssertionError: If recommendation order stops using scored features.
    """
    response = generate_learning_recommendations(make_request())

    assert response.recommendations[0].topic == "Sliding Window"
    assert response.recommendations[0].recommendation_type is (
        RecommendationType.REVISE_FUNDAMENTALS
    )


def test_identify_strengths_returns_sorted_strength_topics() -> None:
    """Verify positive reinforcement topics are deterministic.

    Returns:
        None.

    Raises:
        AssertionError: If strength ordering changes.
    """
    strengths = identify_strengths(
        {
            "Graphs": ClassificationLabel.STRONG,
            "Arrays": ClassificationLabel.MASTERED,
            "DP": ClassificationLabel.WEAK,
        }
    )

    assert strengths == ("Arrays", "Graphs")


def test_build_feature_summary_aggregates_engineered_features() -> None:
    """Verify feature summary is built from engineered feature objects.

    Returns:
        None.

    Raises:
        AssertionError: If summary aggregation changes.
    """
    summary = build_feature_summary(extract_topic_features(make_request()))

    assert summary.overall_accuracy == 49.25
    assert summary.overall_failed_attempts == 5
    assert summary.average_speed == "High"
