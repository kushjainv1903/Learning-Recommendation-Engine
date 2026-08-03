"""Unit tests for priority scoring and ranking."""

from app.core.constants import ClassificationLabel
from app.services.feature_extractor import TopicFeatures
from app.services.scorer import assign_priority_ranks, rank_topics, score_topics


def make_features(
    topic: str,
    accuracy: float,
    failed_attempts: int,
    priority_score: float,
) -> TopicFeatures:
    """Create feature objects for scorer tests.

    Args:
        topic: Topic name.
        accuracy: Topic accuracy.
        failed_attempts: Failed coding attempt count.
        priority_score: Learning priority score.

    Returns:
        Engineered topic features.

    Raises:
        ValueError: If feature values are outside valid ranges.
    """
    return TopicFeatures(
        topic=topic,
        accuracy=accuracy,
        failed_attempts=failed_attempts,
        mcq_accuracy=None,
        coding_success_rate=None,
        speed_score=30.0,
        concept_score=accuracy,
        implementation_score=None,
        consistency_score=None,
        learning_priority_score=priority_score,
    )


def test_score_topics_attaches_classification_and_priority_score() -> None:
    """Verify scorer decorates engineered features.

    Returns:
        None.

    Raises:
        AssertionError: If score attachment changes.
    """
    features = (make_features("Graphs", 42.0, 2, 81.5),)

    scored = score_topics(features, {"Graphs": ClassificationLabel.WEAK})

    assert scored[0].classification is ClassificationLabel.WEAK
    assert scored[0].priority_score == 81.5


def test_rank_topics_uses_deterministic_tie_breakers() -> None:
    """Verify priority ranking order.

    Returns:
        None.

    Raises:
        AssertionError: If sorting rules change.
    """
    features = (
        make_features("Beta", 50.0, 1, 80.0),
        make_features("Alpha", 50.0, 1, 80.0),
        make_features("Critical", 60.0, 1, 80.0),
        make_features("Attempts", 50.0, 2, 80.0),
        make_features("Lowest Accuracy", 40.0, 1, 80.0),
        make_features("Top Score", 60.0, 0, 90.0),
    )
    classifications = {
        "Beta": ClassificationLabel.WEAK,
        "Alpha": ClassificationLabel.WEAK,
        "Critical": ClassificationLabel.CRITICAL,
        "Attempts": ClassificationLabel.WEAK,
        "Lowest Accuracy": ClassificationLabel.WEAK,
        "Top Score": ClassificationLabel.MODERATE,
    }

    ranked = rank_topics(score_topics(features, classifications))

    assert [topic.features.topic for topic in ranked] == [
        "Top Score",
        "Critical",
        "Attempts",
        "Lowest Accuracy",
        "Alpha",
        "Beta",
    ]


def test_assign_priority_ranks_is_one_based() -> None:
    """Verify priority ranks start at one.

    Returns:
        None.

    Raises:
        AssertionError: If priority rank assignment changes.
    """
    features = (
        make_features("Graphs", 42.0, 2, 80.0),
        make_features("Arrays", 92.0, 0, 10.0),
    )
    scored = score_topics(
        features,
        {
            "Graphs": ClassificationLabel.WEAK,
            "Arrays": ClassificationLabel.MASTERED,
        },
    )

    ranks = assign_priority_ranks(rank_topics(scored))

    assert ranks == {"Graphs": 1, "Arrays": 2}
