"""Feature extraction service for normalized learning signals."""

from dataclasses import dataclass

from app.config import (
    ACCURACY_WEIGHT,
    CONSISTENCY_WEIGHT,
    FAILED_ATTEMPT_WEIGHT,
    IMPLEMENTATION_FAILURE_PENALTY,
    NORMALIZED_SCORE_MAX,
    NORMALIZED_SCORE_MIN,
    PERCENTAGE_MULTIPLIER,
    PRIORITY_SCORE_PRECISION,
    SOLVING_TIME_WEIGHT,
    TIME_SCORE,
)
from app.core.constants import AttemptResult
from app.models.request_models import CodingAttempt, MCQResult, RecommendationRequest


@dataclass(frozen=True, slots=True)
class TopicFeatures:
    """Normalized feature values for one topic.

    Attributes:
        topic: Normalized topic name.
        accuracy: Raw topic accuracy validated into the 0-100 range.
        failed_attempts: Count of incorrect coding attempts for the topic.
        mcq_accuracy: MCQ accuracy percentage, or None when MCQ data is absent.
        coding_success_rate: Coding success percentage, or None when attempts are
            absent.
        speed_score: Numeric solving-time score from configuration.
        concept_score: Concept score using the formula `Concept Score = Accuracy`.
        implementation_score: Implementation score using the formula
            `100 - (Failed Attempts * 25)`, clamped to 0-100, or None when no
            coding attempts exist for the topic.
        consistency_score: Consistency score using the formula
            `100 - abs(MCQ Accuracy - Coding Success Rate)`, or None when either
            signal is unavailable.
        learning_priority_score: Weighted score using the configured priority
            formula.

    Example:
        >>> TopicFeatures(
        ...     topic="Graphs",
        ...     accuracy=42.0,
        ...     failed_attempts=2,
        ...     mcq_accuracy=80.0,
        ...     coding_success_rate=0.0,
        ...     speed_score=70.0,
        ...     concept_score=42.0,
        ...     implementation_score=50.0,
        ...     consistency_score=20.0,
        ...     learning_priority_score=60.1,
        ... ).topic
        'Graphs'
    """

    topic: str
    accuracy: float
    failed_attempts: int
    mcq_accuracy: float | None
    coding_success_rate: float | None
    speed_score: float
    concept_score: float
    implementation_score: float | None
    consistency_score: float | None
    learning_priority_score: float

    def __post_init__(self) -> None:
        """Validate normalized feature ranges after object creation.

        Returns:
            None.

        Raises:
            ValueError: If any feature violates the normalized score range.

        Example:
            >>> TopicFeatures(
            ...     topic="Graphs",
            ...     accuracy=42.0,
            ...     failed_attempts=2,
            ...     mcq_accuracy=80.0,
            ...     coding_success_rate=0.0,
            ...     speed_score=70.0,
            ...     concept_score=42.0,
            ...     implementation_score=50.0,
            ...     consistency_score=20.0,
            ...     learning_priority_score=60.1,
            ... ).topic
            'Graphs'
        """
        _validate_non_negative_count("failed_attempts", self.failed_attempts)
        _validate_required_score("accuracy", self.accuracy)
        _validate_required_score("speed_score", self.speed_score)
        _validate_required_score("concept_score", self.concept_score)
        _validate_required_score(
            "learning_priority_score",
            self.learning_priority_score,
        )
        _validate_optional_score("mcq_accuracy", self.mcq_accuracy)
        _validate_optional_score("coding_success_rate", self.coding_success_rate)
        _validate_optional_score("implementation_score", self.implementation_score)
        _validate_optional_score("consistency_score", self.consistency_score)


def extract_topic_features(request: RecommendationRequest) -> tuple[TopicFeatures, ...]:
    """Extract normalized feature objects from a validated request.

    Formula notes:
        Each topic from `topic_accuracy` produces exactly one `TopicFeatures`
        object. Topics are sorted alphabetically so extraction is deterministic
        without assigning recommendation priority.

    Args:
        request: Validated recommendation request.

    Returns:
        Tuple of normalized topic feature objects.

    Raises:
        KeyError: If solving-time data is missing for a topic. Request
            validation should prevent this.

    Example:
        >>> request = RecommendationRequest(
        ...     student_id="student_001",
        ...     date="2026-08-02",
        ...     topic_accuracy={"Graphs": 42},
        ...     coding_attempts=[],
        ...     mcq_results={},
        ...     average_solving_time={"Graphs": "High"},
        ... )
        >>> extract_topic_features(request)[0].topic
        'Graphs'
    """
    return tuple(
        build_topic_features(
            topic=topic,
            accuracy=accuracy,
            coding_attempts=request.coding_attempts,
            mcq_result=request.mcq_results.get(topic),
            solving_time=request.average_solving_time[topic].value,
        )
        for topic, accuracy in sorted(request.topic_accuracy.items())
    )


def build_topic_features(
    topic: str,
    accuracy: float,
    coding_attempts: list[CodingAttempt],
    mcq_result: MCQResult | None,
    solving_time: str,
) -> TopicFeatures:
    """Build a normalized feature object for one topic.

    Formula notes:
        This function composes the individual feature formulas without
        classification, recommendation generation, or API behavior.

    Args:
        topic: Normalized topic name.
        accuracy: Validated topic accuracy.
        coding_attempts: Validated coding attempts for all topics.
        mcq_result: Optional MCQ result for this topic.
        solving_time: Qualitative solving-time label.

    Returns:
        Normalized feature object for the topic.

    Raises:
        KeyError: If solving time is not configured.

    Example:
        >>> from app.models.request_models import CodingAttempt
        >>> attempts = [
        ...     CodingAttempt(
        ...         topic="Graphs",
        ...         problem="Graph BFS",
        ...         attempts=2,
        ...         result="incorrect",
        ...     )
        ... ]
        >>> build_topic_features("Graphs", 42.0, attempts, None, "High").speed_score
        70.0
    """
    topic_attempts = filter_attempts_for_topic(coding_attempts, topic)
    failed_attempts = calculate_failed_attempts(topic_attempts)
    mcq_accuracy = calculate_mcq_accuracy(mcq_result)
    coding_success_rate = calculate_coding_success_rate(topic_attempts)
    concept_score = calculate_concept_score(accuracy)
    implementation_score = calculate_implementation_score(topic_attempts)
    speed_score = calculate_speed_score(solving_time)
    consistency_score = calculate_consistency_score(mcq_accuracy, coding_success_rate)
    learning_priority_score = calculate_learning_priority_score(
        concept_score=concept_score,
        implementation_score=implementation_score,
        speed_score=speed_score,
        consistency_score=consistency_score,
    )

    return TopicFeatures(
        topic=topic,
        accuracy=accuracy,
        failed_attempts=failed_attempts,
        mcq_accuracy=mcq_accuracy,
        coding_success_rate=coding_success_rate,
        speed_score=speed_score,
        concept_score=concept_score,
        implementation_score=implementation_score,
        consistency_score=consistency_score,
        learning_priority_score=learning_priority_score,
    )


def filter_attempts_for_topic(
    coding_attempts: list[CodingAttempt], topic: str
) -> tuple[CodingAttempt, ...]:
    """Return coding attempts that belong to a topic.

    Args:
        coding_attempts: Validated coding attempts for all topics.
        topic: Topic name to match.

    Returns:
        Tuple of attempts for the topic.

    Raises:
        None.

    Example:
        >>> filter_attempts_for_topic([], "Graphs")
        ()
    """
    return tuple(attempt for attempt in coding_attempts if attempt.topic == topic)


def calculate_concept_score(accuracy: float) -> float:
    """Calculate the concept score.

    Formula:
        `Concept Score = Accuracy`.

    Args:
        accuracy: Validated topic accuracy in the 0-100 range.

    Returns:
        Accuracy clamped to the normalized 0-100 score range.

    Raises:
        None.

    Example:
        >>> calculate_concept_score(42.0)
        42.0
    """
    return clamp_score(accuracy)


def calculate_implementation_score(
    topic_attempts: tuple[CodingAttempt, ...],
) -> float | None:
    """Calculate implementation score from failed attempts.

    Formula:
        `Implementation Score = 100 - (Failed Attempts * 25)`, clamped to
        `0-100`. If no coding attempts exist for the topic, return None.

    Args:
        topic_attempts: Coding attempts for one topic.

    Returns:
        Normalized implementation score, or None when attempts are absent.

    Raises:
        None.

    Example:
        >>> calculate_implementation_score(())
        >>> # returns None
    """
    if not topic_attempts:
        return None

    failed_attempts = calculate_failed_attempts(topic_attempts)
    raw_score = NORMALIZED_SCORE_MAX - (
        failed_attempts * IMPLEMENTATION_FAILURE_PENALTY
    )
    return clamp_score(raw_score)


def calculate_failed_attempts(topic_attempts: tuple[CodingAttempt, ...]) -> int:
    """Calculate failed coding attempts for a topic.

    Formula:
        `Failed Attempts = sum(attempts where result == incorrect)`.

    Args:
        topic_attempts: Coding attempts for one topic.

    Returns:
        Total incorrect attempts.

    Raises:
        None.

    Example:
        >>> calculate_failed_attempts(())
        0
    """
    return sum(
        attempt.attempts
        for attempt in topic_attempts
        if attempt.result is AttemptResult.INCORRECT
    )


def calculate_mcq_accuracy(mcq_result: MCQResult | None) -> float | None:
    """Calculate MCQ accuracy.

    Formula:
        `MCQ Accuracy = (correct / total) * 100`. If MCQ data is absent,
        return None.

    Args:
        mcq_result: Optional validated MCQ result.

    Returns:
        Normalized MCQ accuracy percentage, or None.

    Raises:
        None.

    Example:
        >>> from app.models.request_models import MCQResult
        >>> calculate_mcq_accuracy(MCQResult(correct=8, total=10))
        80.0
    """
    if mcq_result is None:
        return None
    return clamp_score((mcq_result.correct / mcq_result.total) * PERCENTAGE_MULTIPLIER)


def calculate_coding_success_rate(
    topic_attempts: tuple[CodingAttempt, ...],
) -> float | None:
    """Calculate coding success rate.

    Formula:
        `Coding Success Rate = Correct Attempts / Total Attempts * 100`. The
        validated `attempts` count is used as the attempt quantity for each row.
        If no coding attempts exist for the topic, return None.

    Args:
        topic_attempts: Coding attempts for one topic.

    Returns:
        Normalized coding success percentage, or None.

    Raises:
        None.

    Example:
        >>> calculate_coding_success_rate(())
        >>> # returns None
    """
    if not topic_attempts:
        return None

    total_attempts = sum(attempt.attempts for attempt in topic_attempts)
    correct_attempts = sum(
        attempt.attempts
        for attempt in topic_attempts
        if attempt.result is AttemptResult.CORRECT
    )
    return clamp_score((correct_attempts / total_attempts) * PERCENTAGE_MULTIPLIER)


def calculate_speed_score(solving_time: str) -> float:
    """Calculate speed score from qualitative solving time.

    Formula:
        `Speed Score = TIME_SCORE[solving_time]`, where `TIME_SCORE` comes from
        `config.py`.

    Args:
        solving_time: Qualitative solving-time label.

    Returns:
        Configured numeric speed score.

    Raises:
        KeyError: If solving time is not configured.

    Example:
        >>> calculate_speed_score("High")
        70.0
    """
    return float(TIME_SCORE[solving_time])


def calculate_consistency_score(
    mcq_accuracy: float | None,
    coding_success_rate: float | None,
) -> float | None:
    """Calculate consistency between theory and coding performance.

    Formula:
        `Consistency Score = 100 - abs(MCQ Accuracy - Coding Success Rate)`. If
        either source signal is unavailable, return None.

    Args:
        mcq_accuracy: Optional MCQ accuracy percentage.
        coding_success_rate: Optional coding success percentage.

    Returns:
        Normalized consistency score, or None.

    Raises:
        None.

    Example:
        >>> calculate_consistency_score(90.0, 85.0)
        95.0
    """
    if mcq_accuracy is None or coding_success_rate is None:
        return None

    raw_score = NORMALIZED_SCORE_MAX - abs(mcq_accuracy - coding_success_rate)
    return clamp_score(raw_score)


def calculate_learning_priority_score(
    concept_score: float,
    implementation_score: float | None,
    speed_score: float,
    consistency_score: float | None,
) -> float:
    """Calculate learning priority score.

    Formula:
        `Priority = Accuracy Weight * (100 - Concept Score)
        + Failure Weight * (100 - Implementation Score)
        + Speed Weight * Speed Score
        + Consistency Weight * (100 - Consistency Score)`.

        If `implementation_score` or `consistency_score` is unavailable, that
        optional component contributes zero penalty. This preserves missing data
        as missing rather than fabricating a downstream signal.

    Args:
        concept_score: Normalized concept score.
        implementation_score: Optional normalized implementation score.
        speed_score: Normalized speed score.
        consistency_score: Optional normalized consistency score.

    Returns:
        Rounded normalized learning priority score.

    Raises:
        None.

    Example:
        >>> calculate_learning_priority_score(40.0, 50.0, 70.0, 20.0)
        62.5
    """
    accuracy_component = ACCURACY_WEIGHT * (NORMALIZED_SCORE_MAX - concept_score)
    failure_component = FAILED_ATTEMPT_WEIGHT * optional_gap(implementation_score)
    speed_component = SOLVING_TIME_WEIGHT * speed_score
    consistency_component = CONSISTENCY_WEIGHT * optional_gap(consistency_score)

    score = (
        accuracy_component + failure_component + speed_component + consistency_component
    )
    return round(clamp_score(score), PRIORITY_SCORE_PRECISION)


def optional_gap(score: float | None) -> float:
    """Calculate missing-safe distance from the maximum score.

    Formula:
        `Optional Gap = 100 - score` when score exists, otherwise `0`.

    Args:
        score: Optional normalized score.

    Returns:
        Gap from maximum score or zero when the signal is unavailable.

    Raises:
        None.

    Example:
        >>> optional_gap(75.0)
        25.0
    """
    if score is None:
        return float(NORMALIZED_SCORE_MIN)
    return NORMALIZED_SCORE_MAX - score


def clamp_score(score: float) -> float:
    """Clamp a numeric feature into the normalized score range.

    Formula:
        `Clamp Score = min(100, max(0, score))`.

    Args:
        score: Raw numeric score.

    Returns:
        Score constrained to the normalized 0-100 range.

    Raises:
        None.

    Example:
        >>> clamp_score(125.0)
        100.0
    """
    return float(min(NORMALIZED_SCORE_MAX, max(NORMALIZED_SCORE_MIN, score)))


def _validate_non_negative_count(field_name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{field_name} must not be negative.")


def _validate_required_score(field_name: str, value: float) -> None:
    if not NORMALIZED_SCORE_MIN <= value <= NORMALIZED_SCORE_MAX:
        raise ValueError(f"{field_name} must be between 0 and 100.")


def _validate_optional_score(field_name: str, value: float | None) -> None:
    if value is not None:
        _validate_required_score(field_name, value)
