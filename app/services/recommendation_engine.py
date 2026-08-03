"""Recommendation pipeline orchestration service module."""

from app.config import RESPONSE_TIMESTAMP_SUFFIX, TIME_SCORE
from app.core.constants import ClassificationLabel
from app.models.request_models import RecommendationRequest
from app.models.response_models import (
    FeatureSummary,
    RecommendationItem,
    RecommendationResponse,
)
from app.services.classifier import classify_topics
from app.services.explanation_generator import generate_reason
from app.services.feature_extractor import TopicFeatures, extract_topic_features
from app.services.message_generator import generate_tomorrows_focus_message
from app.services.recommender import RecommendationDraft, generate_recommendations
from app.services.scorer import rank_topics, score_topics


def generate_learning_recommendations(
    request: RecommendationRequest,
) -> RecommendationResponse:
    """Run the recommendation engine pipeline for a validated request.

    Args:
        request: Validated recommendation request.

    Returns:
        Complete recommendation response model.

    Raises:
        KeyError: If an internal pipeline stage is missing required data.

    Example:
        >>> isinstance(generate_learning_recommendations, object)
        True
    """
    features = extract_topic_features(request)
    classifications = classify_topics(features)
    scored_topics = score_topics(features, classifications)
    ranked_topics = rank_topics(scored_topics)
    recommendations = build_recommendation_items(
        generate_recommendations(ranked_topics)
    )
    strengths = identify_strengths(classifications)

    return RecommendationResponse(
        success=True,
        student_id=request.student_id,
        generated_at=f"{request.date.isoformat()}{RESPONSE_TIMESTAMP_SUFFIX}",
        feature_summary=build_feature_summary(features),
        topic_classification=classifications,
        recommendations=list(recommendations),
        strengths=list(strengths),
        tomorrows_focus_message=generate_tomorrows_focus_message(
            recommendations,
            strengths,
            request.date,
        ),
    )


def build_recommendation_items(
    drafts: tuple[RecommendationDraft, ...],
) -> tuple[RecommendationItem, ...]:
    """Attach explanation text to recommendation drafts.

    Args:
        drafts: Recommendation drafts generated from ranked scored topics.

    Returns:
        Complete response recommendation items.

    Raises:
        pydantic.ValidationError: If a generated item violates the response
            model contract.

    Example:
        >>> build_recommendation_items(())
        ()
    """
    return tuple(_build_recommendation_item(draft) for draft in drafts)


def _build_recommendation_item(draft: RecommendationDraft) -> RecommendationItem:
    features = draft.scored_topic.features
    return RecommendationItem(
        topic=features.topic,
        priority=draft.priority,
        priority_score=draft.scored_topic.priority_score,
        recommendation_type=draft.recommendation_type,
        action=draft.action,
        reason=generate_reason(draft.recommendation_type, features),
        practice_plan=draft.practice_plan,
    )


def identify_strengths(
    classifications: dict[str, ClassificationLabel],
) -> tuple[str, ...]:
    """Identify mastered or strong topics for positive reinforcement.

    Args:
        classifications: Mapping of topic name to classification.

    Returns:
        Alphabetically sorted strength topic names.

    Raises:
        None.

    Example:
        >>> identify_strengths({"Arrays": ClassificationLabel.MASTERED})
        ('Arrays',)
    """
    strength_labels = {ClassificationLabel.MASTERED, ClassificationLabel.STRONG}
    return tuple(
        sorted(
            topic
            for topic, classification in classifications.items()
            if classification in strength_labels
        )
    )


def build_feature_summary(features: tuple[TopicFeatures, ...]) -> FeatureSummary:
    """Build aggregate metrics from engineered features.

    Args:
        features: Engineered topic features.

    Returns:
        Feature summary response model.

    Raises:
        ZeroDivisionError: If called without features.

    Example:
        >>> isinstance(build_feature_summary, object)
        True
    """
    overall_accuracy = sum(feature.accuracy for feature in features) / len(features)
    overall_failed_attempts = sum(feature.failed_attempts for feature in features)
    return FeatureSummary(
        overall_accuracy=round(overall_accuracy, 2),
        overall_failed_attempts=overall_failed_attempts,
        average_speed=_average_speed_label(features),
    )


def _average_speed_label(features: tuple[TopicFeatures, ...]) -> str:
    speed_counts = {
        speed_score: sum(feature.speed_score == speed_score for feature in features)
        for speed_score in {feature.speed_score for feature in features}
    }
    selected_score = max(
        speed_counts,
        key=lambda speed_score: (speed_counts[speed_score], speed_score),
    )
    return min(
        TIME_SCORE,
        key=lambda speed_label: (
            abs(TIME_SCORE[speed_label] - selected_score),
            speed_label,
        ),
    )
