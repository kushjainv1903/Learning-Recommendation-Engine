"""Unit tests for strict request validation."""

from copy import deepcopy
from datetime import date

import pytest
from pydantic import ValidationError

from app.config import MAX_TOPICS
from app.core.constants import AttemptResult, SolvingTimeLevel
from app.models.request_models import RecommendationRequest


def valid_payload() -> dict[str, object]:
    """Build a valid request payload for validation tests.

    Returns:
        Mutable request payload dictionary.

    Raises:
        None.

    Example:
        >>> payload = valid_payload()
        >>> payload["student_id"]
        'student_001'
    """
    return {
        "student_id": "student_001",
        "date": "2026-08-02",
        "topic_accuracy": {
            "Arrays": 92,
            "Sliding Window": 35.5,
            "Graphs": 42,
        },
        "coding_attempts": [
            {
                "topic": "Sliding Window",
                "problem": "Longest Substring",
                "attempts": 3,
                "result": "incorrect",
            }
        ],
        "mcq_results": {
            "Graphs": {
                "correct": 8,
                "total": 10,
            }
        },
        "average_solving_time": {
            "Arrays": "Low",
            "Sliding Window": "High",
            "Graphs": "High",
        },
    }


def assert_invalid(payload: dict[str, object]) -> None:
    """Assert that a payload fails request validation.

    Args:
        payload: Request payload expected to fail validation.

    Returns:
        None.

    Raises:
        AssertionError: If validation succeeds.

    Example:
        >>> bad_payload = valid_payload()
        >>> bad_payload["student_id"] = ""
        >>> assert_invalid(bad_payload)
    """
    with pytest.raises(ValidationError):
        RecommendationRequest.model_validate(payload)


def test_valid_request_accepts_contract_payload() -> None:
    """Validate the official request shape.

    Returns:
        None.

    Raises:
        AssertionError: If valid input is rejected.
    """
    request = RecommendationRequest.model_validate(valid_payload())

    assert request.student_id == "student_001"
    assert request.date == date(2026, 8, 2)
    assert request.topic_accuracy["Sliding Window"] == 35.5
    assert request.coding_attempts[0].result is AttemptResult.INCORRECT
    assert request.average_solving_time["Graphs"] is SolvingTimeLevel.HIGH


def test_topic_names_are_trimmed_and_title_cased() -> None:
    """Validate topic normalization for mappings and nested attempts.

    Returns:
        None.

    Raises:
        AssertionError: If topic names are not normalized.
    """
    payload = valid_payload()
    payload["topic_accuracy"] = {" graphs ": 42}
    payload["coding_attempts"] = [
        {
            "topic": " graphs ",
            "problem": " Graph BFS ",
            "attempts": 2,
            "result": "incorrect",
        }
    ]
    payload["mcq_results"] = {" graphs ": {"correct": 8, "total": 10}}
    payload["average_solving_time"] = {" graphs ": "High"}

    request = RecommendationRequest.model_validate(payload)

    assert list(request.topic_accuracy) == ["Graphs"]
    assert request.coding_attempts[0].topic == "Graphs"
    assert request.coding_attempts[0].problem == "Graph BFS"


def test_empty_optional_collections_are_allowed() -> None:
    """Validate empty coding attempts and MCQ results.

    Returns:
        None.

    Raises:
        AssertionError: If allowed empty collections are rejected.
    """
    payload = valid_payload()
    payload["coding_attempts"] = []
    payload["mcq_results"] = {}

    request = RecommendationRequest.model_validate(payload)

    assert request.coding_attempts == []
    assert request.mcq_results == {}


@pytest.mark.parametrize(
    "field",
    [
        "student_id",
        "date",
        "topic_accuracy",
        "coding_attempts",
        "mcq_results",
        "average_solving_time",
    ],
)
def test_required_fields_are_enforced(field: str) -> None:
    """Validate all required top-level fields.

    Args:
        field: Required field to remove.

    Returns:
        None.

    Raises:
        AssertionError: If missing required fields are accepted.
    """
    payload = valid_payload()
    del payload[field]

    assert_invalid(payload)


@pytest.mark.parametrize("student_id", ["", "   ", "x" * 101, 123])
def test_student_id_rules_are_enforced(student_id: object) -> None:
    """Validate student ID type and length rules.

    Args:
        student_id: Invalid student ID value.

    Returns:
        None.

    Raises:
        AssertionError: If invalid student IDs are accepted.
    """
    payload = valid_payload()
    payload["student_id"] = student_id

    assert_invalid(payload)


@pytest.mark.parametrize("date_value", ["2026/08/02", "02-08-2026", "2026-13-02", 123])
def test_date_must_be_iso_calendar_date(date_value: object) -> None:
    """Validate strict YYYY-MM-DD date input.

    Args:
        date_value: Invalid date value.

    Returns:
        None.

    Raises:
        AssertionError: If invalid dates are accepted.
    """
    payload = valid_payload()
    payload["date"] = date_value

    assert_invalid(payload)


@pytest.mark.parametrize("accuracy", [-1, 101, "42", True])
def test_accuracy_values_are_strict_and_bounded(accuracy: object) -> None:
    """Validate topic accuracy type and range rules.

    Args:
        accuracy: Invalid accuracy value.

    Returns:
        None.

    Raises:
        AssertionError: If invalid accuracy is accepted.
    """
    payload = valid_payload()
    payload["topic_accuracy"] = {"Graphs": accuracy}
    payload["average_solving_time"] = {"Graphs": "High"}

    assert_invalid(payload)


def test_empty_topic_accuracy_is_rejected() -> None:
    """Validate that at least one topic accuracy is required.

    Returns:
        None.

    Raises:
        AssertionError: If empty topic accuracy is accepted.
    """
    payload = valid_payload()
    payload["topic_accuracy"] = {}

    assert_invalid(payload)


def test_empty_solving_time_is_rejected() -> None:
    """Validate that solving time is required.

    Returns:
        None.

    Raises:
        AssertionError: If empty solving time is accepted.
    """
    payload = valid_payload()
    payload["average_solving_time"] = {}

    assert_invalid(payload)


def test_missing_solving_time_for_scored_topic_is_rejected() -> None:
    """Validate every scored topic has solving-time data.

    Returns:
        None.

    Raises:
        AssertionError: If missing solving-time data is accepted.
    """
    payload = valid_payload()
    payload["average_solving_time"] = {"Arrays": "Low"}

    assert_invalid(payload)


@pytest.mark.parametrize("topic", ["", "   ", None])
def test_invalid_topic_names_are_rejected(topic: object) -> None:
    """Validate topic-name rules.

    Args:
        topic: Invalid topic key.

    Returns:
        None.

    Raises:
        AssertionError: If invalid topic names are accepted.
    """
    payload = valid_payload()
    payload["topic_accuracy"] = {topic: 42}
    payload["average_solving_time"] = {"Graphs": "High"}

    assert_invalid(payload)


def test_duplicate_normalized_topic_names_are_rejected() -> None:
    """Validate duplicate topics after normalization fail validation.

    Returns:
        None.

    Raises:
        AssertionError: If duplicate normalized topics are accepted.
    """
    payload = valid_payload()
    payload["topic_accuracy"] = {"graphs": 42, " Graphs ": 45}

    assert_invalid(payload)


def test_more_than_max_topics_is_rejected() -> None:
    """Validate maximum topic count.

    Returns:
        None.

    Raises:
        AssertionError: If oversized topic collections are accepted.
    """
    payload = valid_payload()
    topic_accuracy = {f"Topic {index}": 50 for index in range(MAX_TOPICS + 1)}
    solving_time = {topic: "Medium" for topic in topic_accuracy}
    payload["topic_accuracy"] = topic_accuracy
    payload["average_solving_time"] = solving_time

    assert_invalid(payload)


@pytest.mark.parametrize("attempts", [0, 101, "2", True])
def test_coding_attempt_count_rules_are_enforced(attempts: object) -> None:
    """Validate coding attempt count rules.

    Args:
        attempts: Invalid attempt count.

    Returns:
        None.

    Raises:
        AssertionError: If invalid attempt counts are accepted.
    """
    payload = valid_payload()
    attempt = deepcopy(payload["coding_attempts"][0])
    attempt["attempts"] = attempts
    payload["coding_attempts"] = [attempt]

    assert_invalid(payload)


@pytest.mark.parametrize("result", ["wrong", "Correct", 1])
def test_coding_result_rules_are_enforced(result: object) -> None:
    """Validate coding result enum rules.

    Args:
        result: Invalid result label.

    Returns:
        None.

    Raises:
        AssertionError: If invalid result labels are accepted.
    """
    payload = valid_payload()
    attempt = deepcopy(payload["coding_attempts"][0])
    attempt["result"] = result
    payload["coding_attempts"] = [attempt]

    assert_invalid(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("topic", ""),
        ("topic", "   "),
        ("problem", ""),
        ("problem", "   "),
    ],
)
def test_coding_attempt_text_fields_are_required(field: str, value: str) -> None:
    """Validate required coding-attempt text fields.

    Args:
        field: Attempt field to replace.
        value: Invalid text value.

    Returns:
        None.

    Raises:
        AssertionError: If blank text fields are accepted.
    """
    payload = valid_payload()
    attempt = deepcopy(payload["coding_attempts"][0])
    attempt[field] = value
    payload["coding_attempts"] = [attempt]

    assert_invalid(payload)


def test_extra_fields_are_rejected() -> None:
    """Validate strict model field handling.

    Returns:
        None.

    Raises:
        AssertionError: If unknown fields are accepted.
    """
    payload = valid_payload()
    payload["unexpected"] = "value"

    assert_invalid(payload)


@pytest.mark.parametrize(
    "mcq_result",
    [
        {"correct": -1, "total": 10},
        {"correct": 11, "total": 10},
        {"correct": 1, "total": 0},
        {"correct": "8", "total": 10},
        {"correct": 8, "total": "10"},
    ],
)
def test_mcq_result_rules_are_enforced(mcq_result: dict[str, object]) -> None:
    """Validate MCQ count rules.

    Args:
        mcq_result: Invalid MCQ result mapping.

    Returns:
        None.

    Raises:
        AssertionError: If invalid MCQ results are accepted.
    """
    payload = valid_payload()
    payload["mcq_results"] = {"Graphs": mcq_result}

    assert_invalid(payload)


@pytest.mark.parametrize("solving_time", ["Fast", "low", 10])
def test_solving_time_values_are_case_sensitive(solving_time: object) -> None:
    """Validate solving-time enum rules.

    Args:
        solving_time: Invalid solving-time value.

    Returns:
        None.

    Raises:
        AssertionError: If invalid solving-time values are accepted.
    """
    payload = valid_payload()
    payload["topic_accuracy"] = {"Graphs": 42}
    payload["average_solving_time"] = {"Graphs": solving_time}

    assert_invalid(payload)
