"""Unit tests for topic classification."""

import pytest

from app.core.constants import ClassificationLabel
from app.services.classifier import classify_topic, classify_topics
from app.services.feature_extractor import TopicFeatures


def make_features(accuracy: float, failed_attempts: int = 0) -> TopicFeatures:
    """Create topic features for classifier tests.

    Args:
        accuracy: Topic accuracy.
        failed_attempts: Failed coding attempts.

    Returns:
        Engineered topic features.

    Raises:
        ValueError: If feature values are outside valid ranges.
    """
    return TopicFeatures(
        topic="Graphs",
        accuracy=accuracy,
        failed_attempts=failed_attempts,
        mcq_accuracy=None,
        coding_success_rate=None,
        speed_score=30.0,
        concept_score=accuracy,
        implementation_score=None,
        consistency_score=None,
        learning_priority_score=10.0,
    )


@pytest.mark.parametrize(
    ("accuracy", "expected"),
    [
        (100.0, ClassificationLabel.MASTERED),
        (90.0, ClassificationLabel.MASTERED),
        (89.0, ClassificationLabel.STRONG),
        (75.0, ClassificationLabel.STRONG),
        (74.0, ClassificationLabel.MODERATE),
        (50.0, ClassificationLabel.MODERATE),
        (49.0, ClassificationLabel.WEAK),
        (30.0, ClassificationLabel.WEAK),
        (29.0, ClassificationLabel.CRITICAL),
        (0.0, ClassificationLabel.CRITICAL),
    ],
)
def test_classify_topic_uses_configured_accuracy_boundaries(
    accuracy: float,
    expected: ClassificationLabel,
) -> None:
    """Verify classification boundaries from configuration.

    Args:
        accuracy: Topic accuracy.
        expected: Expected classification.

    Returns:
        None.

    Raises:
        AssertionError: If classification rules change.
    """
    assert classify_topic(make_features(accuracy)) is expected


def test_repeated_failures_make_non_strong_topic_critical() -> None:
    """Verify critical failure threshold overrides non-strong accuracy.

    Returns:
        None.

    Raises:
        AssertionError: If repeated failures do not produce Critical.
    """
    assert classify_topic(make_features(74.0, failed_attempts=3)) is (
        ClassificationLabel.CRITICAL
    )


def test_high_accuracy_repeated_failures_remain_strong() -> None:
    """Verify high accuracy with repeated failures follows edge-case rules.

    Returns:
        None.

    Raises:
        AssertionError: If high-accuracy repeated failures become Critical.
    """
    assert classify_topic(make_features(88.0, failed_attempts=3)) is (
        ClassificationLabel.STRONG
    )


def test_mastered_requires_no_failed_attempts() -> None:
    """Verify mastered topics require zero failures.

    Returns:
        None.

    Raises:
        AssertionError: If failed attempts still classify as Mastered.
    """
    assert classify_topic(make_features(95.0, failed_attempts=1)) is (
        ClassificationLabel.STRONG
    )


def test_classify_topics_returns_topic_mapping() -> None:
    """Verify batch classification returns a topic mapping.

    Returns:
        None.

    Raises:
        AssertionError: If topic mapping is incorrect.
    """
    features = (make_features(42.0),)

    assert classify_topics(features) == {"Graphs": ClassificationLabel.WEAK}
