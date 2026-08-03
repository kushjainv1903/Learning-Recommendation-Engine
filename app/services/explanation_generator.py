"""Explanation generation service module."""

from app.config import HIGH_SPEED_SCORE_THRESHOLD, MAX_EXPLANATION_LENGTH
from app.core.constants import RecommendationType
from app.services.feature_extractor import TopicFeatures


def generate_reason(
    recommendation_type: RecommendationType,
    features: TopicFeatures,
) -> str:
    """Generate a metric-grounded recommendation reason.

    Args:
        recommendation_type: Selected recommendation category.
        features: Engineered topic features.

    Returns:
        Human-readable reason referencing actual performance metrics.

    Raises:
        None.

    Example:
        >>> isinstance(generate_reason, object)
        True
    """
    reason_generators = {
        RecommendationType.REVISE_FUNDAMENTALS: _revise_fundamentals_reason,
        RecommendationType.STRUCTURED_PRACTICE: _structured_practice_reason,
        RecommendationType.IMPLEMENTATION_PRACTICE: _implementation_practice_reason,
        RecommendationType.THEORY_REVISION: _theory_revision_reason,
        RecommendationType.SPEED_PRACTICE: _speed_practice_reason,
        RecommendationType.REINFORCEMENT_PRACTICE: _reinforcement_practice_reason,
        RecommendationType.MAINTAIN_STRENGTH: _maintain_strength_reason,
    }
    reason = reason_generators[recommendation_type](features)
    return reason[:MAX_EXPLANATION_LENGTH]


def _revise_fundamentals_reason(features: TopicFeatures) -> str:
    return (
        f"{features.topic} accuracy is {features.accuracy:g}% with "
        f"{features.failed_attempts} failed coding attempts, indicating a "
        "conceptual gap."
    )


def _structured_practice_reason(features: TopicFeatures) -> str:
    return (
        f"{features.topic} accuracy is {features.accuracy:g}% with limited "
        "coding evidence, so structured practice should build engagement."
    )


def _implementation_practice_reason(features: TopicFeatures) -> str:
    return (
        f"{features.topic} MCQ accuracy is {_format_optional(features.mcq_accuracy)} "
        f"while coding success is {_format_optional(features.coding_success_rate)}, "
        "showing an implementation gap."
    )


def _theory_revision_reason(features: TopicFeatures) -> str:
    return (
        f"{features.topic} MCQ accuracy is {_format_optional(features.mcq_accuracy)} "
        f"while coding success is {_format_optional(features.coding_success_rate)}, "
        "showing a theory gap."
    )


def _speed_practice_reason(features: TopicFeatures) -> str:
    return (
        f"{features.topic} accuracy is {features.accuracy:g}% but speed score is "
        f"{features.speed_score:g}, meeting the high-time threshold "
        f"of {HIGH_SPEED_SCORE_THRESHOLD}."
    )


def _reinforcement_practice_reason(features: TopicFeatures) -> str:
    return (
        f"{features.topic} accuracy is {features.accuracy:g}%, which is not weak "
        "but still needs reinforcement."
    )


def _maintain_strength_reason(features: TopicFeatures) -> str:
    return (
        f"{features.topic} accuracy is {features.accuracy:g}% with "
        f"{features.failed_attempts} failed attempts, showing strong performance."
    )


def _format_optional(value: float | None) -> str:
    if value is None:
        return "unavailable"
    return f"{value:g}%"
