"""Unit tests for the feature engineering layer."""

import pytest

from app.models.request_models import CodingAttempt, MCQResult, RecommendationRequest
from app.services.feature_extractor import (
    TopicFeatures,
    calculate_coding_success_rate,
    calculate_concept_score,
    calculate_consistency_score,
    calculate_failed_attempts,
    calculate_implementation_score,
    calculate_learning_priority_score,
    calculate_mcq_accuracy,
    calculate_speed_score,
    clamp_score,
    extract_topic_features,
    filter_attempts_for_topic,
    optional_gap,
)


def make_attempt(topic: str, attempts: int, result: str) -> CodingAttempt:
    """Create a validated coding attempt for feature tests.

    Args:
        topic: Topic name.
        attempts: Attempt count.
        result: Attempt result label.

    Returns:
        Validated coding attempt.

    Raises:
        pydantic.ValidationError: If test input violates request rules.

    Example:
        >>> make_attempt("Graphs", 2, "incorrect").topic
        'Graphs'
    """
    return CodingAttempt(
        topic=topic,
        problem=f"{topic} Practice",
        attempts=attempts,
        result=result,
    )


def make_request() -> RecommendationRequest:
    """Create a validated request for feature extraction tests.

    Returns:
        Validated recommendation request.

    Raises:
        pydantic.ValidationError: If the fixture violates request rules.

    Example:
        >>> make_request().student_id
        'student_001'
    """
    return RecommendationRequest.model_validate(
        {
            "student_id": "student_001",
            "date": "2026-08-02",
            "topic_accuracy": {
                " graphs ": 42,
                "Arrays": 92,
                "Dynamic Programming": 30,
            },
            "coding_attempts": [
                {
                    "topic": "Graphs",
                    "problem": "Graph BFS",
                    "attempts": 2,
                    "result": "incorrect",
                },
                {
                    "topic": "Graphs",
                    "problem": "Graph DFS",
                    "attempts": 1,
                    "result": "correct",
                },
                {
                    "topic": "Arrays",
                    "problem": "Two Sum",
                    "attempts": 1,
                    "result": "correct",
                },
            ],
            "mcq_results": {
                "Graphs": {
                    "correct": 8,
                    "total": 10,
                }
            },
            "average_solving_time": {
                "Graphs": "High",
                "Arrays": "Low",
                "Dynamic Programming": "Medium",
            },
        }
    )


def test_extract_topic_features_returns_one_feature_per_topic() -> None:
    """Verify extraction creates deterministic topic feature objects.

    Returns:
        None.

    Raises:
        AssertionError: If features are missing, duplicated, or unsorted.
    """
    features = extract_topic_features(make_request())

    assert isinstance(features[0], TopicFeatures)
    assert [feature.topic for feature in features] == [
        "Arrays",
        "Dynamic Programming",
        "Graphs",
    ]


def test_topic_features_rejects_out_of_range_scores() -> None:
    """Verify engineered features cannot carry invalid normalized scores.

    Returns:
        None.

    Raises:
        AssertionError: If invalid feature ranges are accepted.
    """
    with pytest.raises(ValueError):
        TopicFeatures(
            topic="Graphs",
            accuracy=101.0,
            failed_attempts=0,
            mcq_accuracy=None,
            coding_success_rate=None,
            speed_score=70.0,
            concept_score=42.0,
            implementation_score=None,
            consistency_score=None,
            learning_priority_score=20.0,
        )


def test_topic_features_rejects_negative_failed_attempts() -> None:
    """Verify failed-attempt counts cannot be negative.

    Returns:
        None.

    Raises:
        AssertionError: If negative failed attempts are accepted.
    """
    with pytest.raises(ValueError):
        TopicFeatures(
            topic="Graphs",
            accuracy=42.0,
            failed_attempts=-1,
            mcq_accuracy=None,
            coding_success_rate=None,
            speed_score=70.0,
            concept_score=42.0,
            implementation_score=None,
            consistency_score=None,
            learning_priority_score=20.0,
        )


def test_extract_topic_features_computes_graph_features() -> None:
    """Verify full feature extraction for a topic with every signal.

    Returns:
        None.

    Raises:
        AssertionError: If any computed feature differs from the documented
            formula.
    """
    features = {
        feature.topic: feature for feature in extract_topic_features(make_request())
    }

    graphs = features["Graphs"]

    assert graphs.accuracy == 42.0
    assert graphs.failed_attempts == 2
    assert graphs.mcq_accuracy == 80.0
    assert graphs.coding_success_rate == pytest.approx(33.3333333333)
    assert graphs.speed_score == 70.0
    assert graphs.concept_score == 42.0
    assert graphs.implementation_score == 50.0
    assert graphs.consistency_score == pytest.approx(53.3333333333)
    assert graphs.learning_priority_score == 57.27


def test_extract_topic_features_preserves_missing_optional_signals() -> None:
    """Verify missing MCQ and coding signals remain None.

    Returns:
        None.

    Raises:
        AssertionError: If optional missing signals are fabricated.
    """
    features = {
        feature.topic: feature for feature in extract_topic_features(make_request())
    }

    dynamic_programming = features["Dynamic Programming"]

    assert dynamic_programming.mcq_accuracy is None
    assert dynamic_programming.coding_success_rate is None
    assert dynamic_programming.implementation_score is None
    assert dynamic_programming.consistency_score is None
    assert dynamic_programming.learning_priority_score == 37.5


def test_filter_attempts_for_topic_returns_only_matching_attempts() -> None:
    """Verify topic-specific attempt filtering.

    Returns:
        None.

    Raises:
        AssertionError: If attempts for other topics are included.
    """
    attempts = [
        make_attempt("Graphs", 2, "incorrect"),
        make_attempt("Arrays", 1, "correct"),
    ]

    filtered = filter_attempts_for_topic(attempts, "Graphs")

    assert len(filtered) == 1
    assert filtered[0].topic == "Graphs"


def test_calculate_concept_score_uses_accuracy() -> None:
    """Verify concept score formula.

    Returns:
        None.

    Raises:
        AssertionError: If concept score does not equal accuracy.
    """
    assert calculate_concept_score(42.5) == 42.5


@pytest.mark.parametrize(
    ("failed_attempts", "expected_score"),
    [
        (0, 100.0),
        (1, 75.0),
        (2, 50.0),
        (3, 25.0),
        (4, 0.0),
        (5, 0.0),
    ],
)
def test_calculate_implementation_score_uses_failed_attempt_penalty(
    failed_attempts: int,
    expected_score: float,
) -> None:
    """Verify implementation score formula and clamp behavior.

    Args:
        failed_attempts: Number of incorrect attempts to model.
        expected_score: Expected implementation score.

    Returns:
        None.

    Raises:
        AssertionError: If implementation score formula changes.
    """
    if failed_attempts == 0:
        attempts = [make_attempt("Graphs", 1, "correct")]
    else:
        attempts = [make_attempt("Graphs", failed_attempts, "incorrect")]

    assert calculate_implementation_score(tuple(attempts)) == expected_score


def test_calculate_implementation_score_returns_none_without_attempts() -> None:
    """Verify missing coding attempts remain unavailable.

    Returns:
        None.

    Raises:
        AssertionError: If missing implementation data is fabricated.
    """
    assert calculate_implementation_score(()) is None


def test_calculate_failed_attempts_sums_incorrect_attempt_quantities() -> None:
    """Verify failed-attempt calculation.

    Returns:
        None.

    Raises:
        AssertionError: If correct attempts are counted as failures.
    """
    attempts = (
        make_attempt("Graphs", 2, "incorrect"),
        make_attempt("Graphs", 1, "correct"),
        make_attempt("Graphs", 3, "incorrect"),
    )

    assert calculate_failed_attempts(attempts) == 5


def test_calculate_mcq_accuracy_uses_correct_over_total() -> None:
    """Verify MCQ accuracy formula.

    Returns:
        None.

    Raises:
        AssertionError: If MCQ accuracy formula changes.
    """
    assert calculate_mcq_accuracy(MCQResult(correct=8, total=10)) == 80.0


def test_calculate_mcq_accuracy_returns_none_when_missing() -> None:
    """Verify missing MCQ data remains unavailable.

    Returns:
        None.

    Raises:
        AssertionError: If missing MCQ data is fabricated.
    """
    assert calculate_mcq_accuracy(None) is None


def test_calculate_coding_success_rate_uses_correct_over_total_attempts() -> None:
    """Verify coding success rate formula.

    Returns:
        None.

    Raises:
        AssertionError: If coding success rate formula changes.
    """
    attempts = (
        make_attempt("Graphs", 3, "correct"),
        make_attempt("Graphs", 1, "incorrect"),
    )

    assert calculate_coding_success_rate(attempts) == 75.0


def test_calculate_coding_success_rate_returns_none_without_attempts() -> None:
    """Verify missing coding success remains unavailable.

    Returns:
        None.

    Raises:
        AssertionError: If missing coding success data is fabricated.
    """
    assert calculate_coding_success_rate(()) is None


@pytest.mark.parametrize(
    ("solving_time", "expected_score"),
    [
        ("Low", 10.0),
        ("Medium", 30.0),
        ("High", 70.0),
        ("Very High", 100.0),
    ],
)
def test_calculate_speed_score_uses_configured_time_scores(
    solving_time: str,
    expected_score: float,
) -> None:
    """Verify speed score mapping.

    Args:
        solving_time: Qualitative solving-time label.
        expected_score: Expected configured numeric score.

    Returns:
        None.

    Raises:
        AssertionError: If configured speed mapping is not used.
    """
    assert calculate_speed_score(solving_time) == expected_score


def test_calculate_speed_score_rejects_unknown_time_level() -> None:
    """Verify invalid solving-time labels fail fast.

    Returns:
        None.

    Raises:
        AssertionError: If unknown time levels are accepted.
    """
    with pytest.raises(KeyError):
        calculate_speed_score("Fast")


def test_calculate_consistency_score_uses_absolute_gap() -> None:
    """Verify consistency score formula.

    Returns:
        None.

    Raises:
        AssertionError: If consistency score formula changes.
    """
    assert calculate_consistency_score(90.0, 85.0) == 95.0
    assert calculate_consistency_score(90.0, 30.0) == 40.0


@pytest.mark.parametrize(
    ("mcq_accuracy", "coding_success_rate"),
    [
        (None, 80.0),
        (80.0, None),
        (None, None),
    ],
)
def test_calculate_consistency_score_returns_none_when_signal_missing(
    mcq_accuracy: float | None,
    coding_success_rate: float | None,
) -> None:
    """Verify missing consistency inputs remain unavailable.

    Args:
        mcq_accuracy: Optional MCQ accuracy.
        coding_success_rate: Optional coding success rate.

    Returns:
        None.

    Raises:
        AssertionError: If missing consistency data is fabricated.
    """
    assert calculate_consistency_score(mcq_accuracy, coding_success_rate) is None


def test_calculate_learning_priority_score_uses_weighted_formula() -> None:
    """Verify learning priority formula with all components present.

    Returns:
        None.

    Raises:
        AssertionError: If priority formula changes.
    """
    score = calculate_learning_priority_score(
        concept_score=40.0,
        implementation_score=50.0,
        speed_score=70.0,
        consistency_score=20.0,
    )

    assert score == 61.5


def test_calculate_learning_priority_score_ignores_missing_optional_components() -> (
    None
):
    """Verify unavailable optional components add no priority penalty.

    Returns:
        None.

    Raises:
        AssertionError: If missing data is penalized or fabricated.
    """
    score = calculate_learning_priority_score(
        concept_score=30.0,
        implementation_score=None,
        speed_score=30.0,
        consistency_score=None,
    )

    assert score == 37.5


def test_optional_gap_uses_zero_for_missing_scores() -> None:
    """Verify optional score gaps preserve missing data.

    Returns:
        None.

    Raises:
        AssertionError: If missing optional scores are penalized.
    """
    assert optional_gap(None) == 0.0
    assert optional_gap(75.0) == 25.0


@pytest.mark.parametrize(
    ("raw_score", "expected_score"),
    [
        (-10.0, 0.0),
        (42.0, 42.0),
        (125.0, 100.0),
    ],
)
def test_clamp_score_limits_values_to_normalized_range(
    raw_score: float,
    expected_score: float,
) -> None:
    """Verify score clamping.

    Args:
        raw_score: Unbounded raw score.
        expected_score: Expected normalized score.

    Returns:
        None.

    Raises:
        AssertionError: If clamping behavior changes.
    """
    assert clamp_score(raw_score) == expected_score
