"""Topic classification service module."""

from app.config import (
    CRITICAL,
    CRITICAL_FAILURE_LIMIT,
    MASTERED,
    MASTERED_THRESHOLD,
    MODERATE,
    MODERATE_THRESHOLD,
    NO_FAILURES,
    STRONG,
    STRONG_THRESHOLD,
    WEAK,
    WEAK_THRESHOLD,
)
from app.core.constants import ClassificationLabel
from app.services.feature_extractor import TopicFeatures


def classify_topic(features: TopicFeatures) -> ClassificationLabel:
    """Classify one topic from engineered features.

    Args:
        features: Engineered topic features.

    Returns:
        Topic classification label.

    Raises:
        None.

    Example:
        >>> from app.services.feature_extractor import TopicFeatures
        >>> classify_topic(
        ...     TopicFeatures(
        ...         topic="Graphs",
        ...         accuracy=42.0,
        ...         failed_attempts=2,
        ...         mcq_accuracy=None,
        ...         coding_success_rate=None,
        ...         speed_score=70.0,
        ...         concept_score=42.0,
        ...         implementation_score=50.0,
        ...         consistency_score=None,
        ...         learning_priority_score=50.0,
        ...     )
        ... )
        <ClassificationLabel.WEAK: 'Weak'>
    """
    if _is_critical(features):
        return ClassificationLabel(CRITICAL)
    if _is_mastered(features):
        return ClassificationLabel(MASTERED)
    if features.accuracy >= STRONG_THRESHOLD:
        return ClassificationLabel(STRONG)
    if features.accuracy >= MODERATE_THRESHOLD:
        return ClassificationLabel(MODERATE)
    if features.accuracy >= WEAK_THRESHOLD:
        return ClassificationLabel(WEAK)
    return ClassificationLabel(CRITICAL)


def classify_topics(
    features: tuple[TopicFeatures, ...],
) -> dict[str, ClassificationLabel]:
    """Classify all engineered topic features.

    Args:
        features: Engineered topic features.

    Returns:
        Mapping of topic name to classification.

    Raises:
        None.

    Example:
        >>> classify_topics(())
        {}
    """
    return {
        topic_features.topic: classify_topic(topic_features)
        for topic_features in features
    }


def _is_critical(features: TopicFeatures) -> bool:
    return (
        features.accuracy < WEAK_THRESHOLD
        or (
            features.accuracy < STRONG_THRESHOLD
            and features.failed_attempts >= CRITICAL_FAILURE_LIMIT
        )
    )


def _is_mastered(features: TopicFeatures) -> bool:
    return (
        features.accuracy >= MASTERED_THRESHOLD
        and features.failed_attempts == NO_FAILURES
    )
