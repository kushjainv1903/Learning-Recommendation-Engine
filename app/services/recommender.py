"""Recommendation generation service module."""

from dataclasses import dataclass

from app.config import (
    ACTION_TEMPLATES,
    CRITICAL,
    CRITICAL_PRACTICE,
    DEFAULT_RECOMMENDATIONS,
    CRITICAL_FAILURE_LIMIT,
    GOOD_CODING_SUCCESS_THRESHOLD,
    GOOD_FAILURE_LIMIT,
    HIGH_MCQ_THRESHOLD,
    HIGH_SPEED_SCORE_THRESHOLD,
    STRONG_THRESHOLD,
    LOW_CODING_SUCCESS_THRESHOLD,
    LOW_MCQ_THRESHOLD,
    MASTERED,
    MASTERED_PRACTICE,
    MAX_RECOMMENDATIONS,
    MODERATE,
    MODERATE_PRACTICE,
    PRACTICE_FAILURE_LIMIT,
    STRONG,
    STRONG_PRACTICE,
    WEAK,
    WEAK_PRACTICE,
)
from app.core.constants import ClassificationLabel, RecommendationType
from app.models.response_models import PracticePlan
from app.services.feature_extractor import TopicFeatures
from app.services.scorer import ScoredTopic


@dataclass(frozen=True, slots=True)
class RecommendationDraft:
    """Recommendation details before explanation generation.

    Attributes:
        scored_topic: Ranked scored topic used to build the recommendation.
        priority: One-based recommendation priority.
        recommendation_type: Selected recommendation category.
        action: Student-facing action.
        practice_plan: Recommended practice workload.

    Example:
        >>> isinstance(RecommendationDraft, object)
        True
    """

    scored_topic: ScoredTopic
    priority: int
    recommendation_type: RecommendationType
    action: str
    practice_plan: PracticePlan


def generate_recommendations(
    ranked_topics: tuple[ScoredTopic, ...],
) -> tuple[RecommendationDraft, ...]:
    """Generate ranked recommendations from scored topics.

    Args:
        ranked_topics: Deterministically ranked scored topics.

    Returns:
        Tuple of recommendation drafts, each with action, priority, type, and
        practice plan. Explanation text is added by the orchestrator.

    Raises:
        KeyError: If a configured action template is missing.

    Example:
        >>> generate_recommendations(())
        ()
    """
    recommendation_topics = _select_recommendation_topics(ranked_topics)
    return tuple(
        _build_recommendation(scored_topic, priority)
        for priority, scored_topic in enumerate(recommendation_topics, start=1)
    )


def select_recommendation_type(scored_topic: ScoredTopic) -> RecommendationType:
    """Select exactly one recommendation type for a scored topic.

    Args:
        scored_topic: Topic with features, classification, and priority score.

    Returns:
        Recommendation type selected by configured rule order.

    Raises:
        None.

    Example:
        >>> isinstance(select_recommendation_type, object)
        True
    """
    features = scored_topic.features
    if _needs_fundamental_revision(scored_topic):
        return RecommendationType.REVISE_FUNDAMENTALS
    if _has_implementation_gap(features):
        return RecommendationType.IMPLEMENTATION_PRACTICE
    if _has_theory_gap(features):
        return RecommendationType.THEORY_REVISION
    if _needs_structured_practice(scored_topic):
        return RecommendationType.STRUCTURED_PRACTICE
    if _needs_speed_practice(scored_topic):
        return RecommendationType.SPEED_PRACTICE
    if scored_topic.classification is ClassificationLabel.MODERATE:
        return RecommendationType.REINFORCEMENT_PRACTICE
    return RecommendationType.MAINTAIN_STRENGTH


def _select_recommendation_topics(
    ranked_topics: tuple[ScoredTopic, ...],
) -> tuple[ScoredTopic, ...]:
    actionable_topics = tuple(
        scored_topic
        for scored_topic in ranked_topics
        if _is_actionable_recommendation(scored_topic)
    )
    if actionable_topics:
        recommendation_limit = _recommendation_limit(actionable_topics)
        return actionable_topics[:recommendation_limit]

    fallback_topic = _select_strength_fallback(ranked_topics)
    if fallback_topic is None:
        return ()
    return (fallback_topic,)


def _is_actionable_recommendation(scored_topic: ScoredTopic) -> bool:
    if scored_topic.classification is ClassificationLabel.MASTERED:
        return False
    return (
        select_recommendation_type(scored_topic)
        is not RecommendationType.MAINTAIN_STRENGTH
    )


def _recommendation_limit(
    actionable_topics: tuple[ScoredTopic, ...],
) -> int:
    if _all_topics_are_critical(actionable_topics):
        return DEFAULT_RECOMMENDATIONS
    if len(actionable_topics) > MAX_RECOMMENDATIONS:
        return MAX_RECOMMENDATIONS
    return min(DEFAULT_RECOMMENDATIONS, MAX_RECOMMENDATIONS)


def _all_topics_are_critical(scored_topics: tuple[ScoredTopic, ...]) -> bool:
    return all(
        scored_topic.classification is ClassificationLabel.CRITICAL
        for scored_topic in scored_topics
    )


def _select_strength_fallback(
    ranked_topics: tuple[ScoredTopic, ...],
) -> ScoredTopic | None:
    eligible_topics = tuple(
        scored_topic
        for scored_topic in ranked_topics
        if scored_topic.classification
        in {ClassificationLabel.MASTERED, ClassificationLabel.STRONG}
    )
    if not eligible_topics:
        return ranked_topics[0] if ranked_topics else None
    return sorted(
        eligible_topics,
        key=lambda item: (-item.features.accuracy, item.features.topic),
    )[0]


def _build_recommendation(
    scored_topic: ScoredTopic,
    priority: int,
) -> RecommendationDraft:
    recommendation_type = select_recommendation_type(scored_topic)
    return RecommendationDraft(
        scored_topic=scored_topic,
        priority=priority,
        recommendation_type=recommendation_type,
        action=_build_action(recommendation_type, scored_topic.features.topic),
        practice_plan=_build_practice_plan(scored_topic.classification),
    )


def _build_action(recommendation_type: RecommendationType, topic: str) -> str:
    return ACTION_TEMPLATES[recommendation_type.value].format(topic=topic)


def _build_practice_plan(classification: ClassificationLabel) -> PracticePlan:
    practice_by_classification = {
        ClassificationLabel(CRITICAL): CRITICAL_PRACTICE,
        ClassificationLabel(WEAK): WEAK_PRACTICE,
        ClassificationLabel(MODERATE): MODERATE_PRACTICE,
        ClassificationLabel(STRONG): STRONG_PRACTICE,
        ClassificationLabel(MASTERED): MASTERED_PRACTICE,
    }
    return PracticePlan(**practice_by_classification[classification])


def _needs_fundamental_revision(scored_topic: ScoredTopic) -> bool:
    return (
        scored_topic.classification
        in {ClassificationLabel.WEAK, ClassificationLabel.CRITICAL}
        and scored_topic.features.failed_attempts >= PRACTICE_FAILURE_LIMIT
    )


def _has_implementation_gap(features: TopicFeatures) -> bool:
    repeated_high_accuracy_failures = (
        features.accuracy >= STRONG_THRESHOLD
        and features.failed_attempts >= CRITICAL_FAILURE_LIMIT
    )
    measured_implementation_gap = (
        features.mcq_accuracy is not None
        and features.coding_success_rate is not None
        and features.mcq_accuracy >= HIGH_MCQ_THRESHOLD
        and features.coding_success_rate < LOW_CODING_SUCCESS_THRESHOLD
    )
    return repeated_high_accuracy_failures or measured_implementation_gap


def _has_theory_gap(features: TopicFeatures) -> bool:
    return (
        features.mcq_accuracy is not None
        and features.coding_success_rate is not None
        and features.mcq_accuracy < LOW_MCQ_THRESHOLD
        and features.coding_success_rate >= GOOD_CODING_SUCCESS_THRESHOLD
    )


def _needs_structured_practice(scored_topic: ScoredTopic) -> bool:
    return (
        scored_topic.classification
        in {ClassificationLabel.WEAK, ClassificationLabel.CRITICAL}
        and scored_topic.features.failed_attempts <= GOOD_FAILURE_LIMIT
    )


def _needs_speed_practice(scored_topic: ScoredTopic) -> bool:
    return (
        scored_topic.classification is ClassificationLabel.STRONG
        and scored_topic.features.speed_score >= HIGH_SPEED_SCORE_THRESHOLD
    )
