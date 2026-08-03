"""Pydantic response models for consistent API contracts."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from app.config import (
    MAX_EXPLANATION_LENGTH,
    MAX_MESSAGE_LENGTH,
    MAX_RECOMMENDATIONS,
    MAX_TOPIC_NAME_LENGTH,
    MIN_RECOMMENDATIONS,
    MIN_TOPIC_NAME_LENGTH,
    NORMALIZED_SCORE_MAX,
    NORMALIZED_SCORE_MIN,
)
from app.core.constants import ClassificationLabel, RecommendationType

TopicName = Annotated[
    str,
    Field(min_length=MIN_TOPIC_NAME_LENGTH, max_length=MAX_TOPIC_NAME_LENGTH),
]
NormalizedScore = Annotated[
    float,
    Field(ge=NORMALIZED_SCORE_MIN, le=NORMALIZED_SCORE_MAX),
]
NonNegativeCount = Annotated[int, Field(ge=0)]


class StrictResponseModel(BaseModel):
    """Base model for consistent response serialization.

    Attributes:
        model_config: Pydantic configuration shared by response models.

    Example:
        >>> StrictResponseModel.model_config["extra"]
        'forbid'
    """

    model_config = ConfigDict(extra="forbid", strict=True)


class ErrorDetail(StrictResponseModel):
    """Represent one validation error detail.

    Attributes:
        field: Field path that failed validation.
        message: Human-readable validation message.

    Example:
        >>> ErrorDetail(field="student_id", message="Must not be empty.").field
        'student_id'
    """

    field: str
    message: str


class ErrorResponse(StrictResponseModel):
    """Represent a standard API error response.

    Attributes:
        success: Always false for error responses.
        error: Safe error summary.
        details: Optional validation details.

    Example:
        >>> ErrorResponse(success=False, error="Validation failed.").success
        False
    """

    success: Literal[False]
    error: str
    details: list[ErrorDetail] = Field(default_factory=list)


class TopicClassification(StrictResponseModel):
    """Represent one topic classification result.

    Attributes:
        topic: Topic name.
        classification: Classification label assigned to the topic.

    Example:
        >>> TopicClassification(topic="Graphs", classification="Weak").classification
        <ClassificationLabel.WEAK: 'Weak'>
    """

    topic: TopicName
    classification: ClassificationLabel


class PracticePlan(StrictResponseModel):
    """Represent a recommended practice workload.

    Attributes:
        easy: Number of easy problems.
        medium: Number of medium problems.
        hard: Number of hard problems.

    Example:
        >>> PracticePlan(easy=3, medium=3, hard=1).medium
        3
    """

    easy: NonNegativeCount
    medium: NonNegativeCount
    hard: NonNegativeCount


class FeatureSummary(StrictResponseModel):
    """Represent aggregate response metrics.

    Attributes:
        overall_accuracy: Average topic accuracy.
        overall_failed_attempts: Total failed attempts.
        average_speed: Qualitative speed summary.

    Example:
        >>> FeatureSummary(
        ...     overall_accuracy=49.25,
        ...     overall_failed_attempts=5,
        ...     average_speed="High",
        ... ).overall_failed_attempts
        5
    """

    overall_accuracy: NormalizedScore
    overall_failed_attempts: NonNegativeCount
    average_speed: str


class RecommendationItem(StrictResponseModel):
    """Represent one recommendation in the API response.

    Attributes:
        topic: Topic name.
        priority: One-based priority rank.
        priority_score: Rounded priority score.
        recommendation_type: Recommendation category.
        action: Student-facing action.
        reason: Explanation referencing actual performance.
        practice_plan: Recommended practice workload.

    Example:
        >>> item = RecommendationItem(
        ...     topic="Graphs",
        ...     priority=1,
        ...     priority_score=82.1,
        ...     recommendation_type="Implementation Practice",
        ...     action="Practice Graph BFS",
        ...     reason="Coding attempts indicate implementation difficulty.",
        ...     practice_plan=PracticePlan(easy=3, medium=3, hard=1),
        ... )
        >>> item.topic
        'Graphs'
    """

    topic: TopicName
    priority: Annotated[
        int,
        Field(ge=MIN_RECOMMENDATIONS, le=MAX_RECOMMENDATIONS),
    ]
    priority_score: NormalizedScore
    recommendation_type: RecommendationType
    action: str
    reason: Annotated[str, Field(max_length=MAX_EXPLANATION_LENGTH)]
    practice_plan: PracticePlan


class RecommendationResponse(StrictResponseModel):
    """Represent a successful recommendation response.

    Attributes:
        success: Always true for successful responses.
        student_id: External student identifier.
        generated_at: ISO-8601 generation timestamp.
        feature_summary: Aggregate response metrics.
        topic_classification: Topic-to-classification mapping.
        recommendations: Ranked recommendation list.
        strengths: Strong or mastered topic names.
        tomorrows_focus_message: Student-facing summary message.

    Example:
        >>> RecommendationResponse(
        ...     success=True,
        ...     student_id="student_001",
        ...     generated_at="2026-08-02T14:30:00Z",
        ...     feature_summary=FeatureSummary(
        ...         overall_accuracy=49.25,
        ...         overall_failed_attempts=5,
        ...         average_speed="High",
        ...     ),
        ...     topic_classification={"Graphs": "Weak"},
        ...     recommendations=[],
        ...     strengths=[],
        ...     tomorrows_focus_message="Focus on Graphs.",
        ... ).success
        True
    """

    success: Literal[True]
    student_id: str
    generated_at: str
    feature_summary: FeatureSummary
    topic_classification: dict[str, ClassificationLabel]
    recommendations: list[RecommendationItem]
    strengths: list[TopicName]
    tomorrows_focus_message: Annotated[str, Field(max_length=MAX_MESSAGE_LENGTH)]
