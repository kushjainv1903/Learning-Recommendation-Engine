"""Priority scoring and deterministic ranking service module."""

from dataclasses import dataclass

from app.config import CLASSIFICATION_SEVERITY
from app.core.constants import ClassificationLabel
from app.services.feature_extractor import TopicFeatures


@dataclass(frozen=True, slots=True)
class ScoredTopic:
    """Topic features decorated with classification and priority score.

    Attributes:
        features: Engineered topic features.
        classification: Topic classification.
        priority_score: Learning priority score from feature engineering.

    Example:
        >>> isinstance(ScoredTopic, object)
        True
    """

    features: TopicFeatures
    classification: ClassificationLabel
    priority_score: float


def score_topics(
    features: tuple[TopicFeatures, ...],
    classifications: dict[str, ClassificationLabel],
) -> tuple[ScoredTopic, ...]:
    """Attach priority scores and classifications to topic features.

    Args:
        features: Engineered topic features.
        classifications: Mapping of topic name to classification.

    Returns:
        Tuple of scored topics.

    Raises:
        KeyError: If a feature has no matching classification.

    Example:
        >>> score_topics((), {})
        ()
    """
    return tuple(
        ScoredTopic(
            features=topic_features,
            classification=classifications[topic_features.topic],
            priority_score=topic_features.learning_priority_score,
        )
        for topic_features in features
    )


def rank_topics(scored_topics: tuple[ScoredTopic, ...]) -> tuple[ScoredTopic, ...]:
    """Sort topics by deterministic recommendation ranking rules.

    Sorting order:
        Highest priority score, highest classification severity, highest failed
        attempts, lowest accuracy, then alphabetical topic name.

    Args:
        scored_topics: Topics with scores and classifications.

    Returns:
        Deterministically sorted scored topics.

    Raises:
        None.

    Example:
        >>> rank_topics(())
        ()
    """
    return tuple(sorted(scored_topics, key=_ranking_key))


def assign_priority_ranks(
    scored_topics: tuple[ScoredTopic, ...],
) -> dict[str, int]:
    """Assign one-based priority ranks after deterministic sorting.

    Args:
        scored_topics: Ranked scored topics.

    Returns:
        Mapping of topic name to one-based priority rank.

    Raises:
        None.

    Example:
        >>> assign_priority_ranks(())
        {}
    """
    return {
        scored_topic.features.topic: index
        for index, scored_topic in enumerate(scored_topics, start=1)
    }


def _ranking_key(scored_topic: ScoredTopic) -> tuple[float, int, int, float, str]:
    classification_severity = CLASSIFICATION_SEVERITY[scored_topic.classification.value]
    return (
        -scored_topic.priority_score,
        -classification_severity,
        -scored_topic.features.failed_attempts,
        scored_topic.features.accuracy,
        scored_topic.features.topic,
    )
