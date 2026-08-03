"""Pydantic request models and validation for the recommendation API."""

from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.config import (
    MAX_ACCURACY,
    MAX_ATTEMPTS_PER_PROBLEM,
    MAX_CODING_ATTEMPTS,
    MAX_MCQ_TOPICS,
    MAX_TOPICS,
    MIN_ACCURACY,
    MIN_ATTEMPTS_PER_PROBLEM,
    MIN_MCQ_CORRECT,
    MIN_MCQ_TOTAL,
    MIN_PROBLEM_NAME_LENGTH,
    MIN_TOPICS,
    STUDENT_ID_MAX_LENGTH,
    STUDENT_ID_MIN_LENGTH,
)
from app.core.constants import AttemptResult, SolvingTimeLevel
from app.utils.validators import (
    ensure_topics_have_solving_time,
    normalize_required_text,
    normalize_topic_mapping,
    normalize_topic_name,
    validate_accuracy_mapping_values,
    validate_iso_date_string,
)

AccuracyValue = Annotated[float, Field(ge=MIN_ACCURACY, le=MAX_ACCURACY)]
AttemptsValue = Annotated[
    int, Field(ge=MIN_ATTEMPTS_PER_PROBLEM, le=MAX_ATTEMPTS_PER_PROBLEM)
]
McqCorrectValue = Annotated[int, Field(ge=MIN_MCQ_CORRECT)]
McqTotalValue = Annotated[int, Field(ge=MIN_MCQ_TOTAL)]


class StrictRequestModel(BaseModel):
    """Base model for strict request validation.

    Attributes:
        model_config: Pydantic configuration shared by request models.

    Example:
        >>> StrictRequestModel.model_config["extra"]
        'forbid'
    """

    model_config = ConfigDict(extra="forbid")


class CodingAttempt(StrictRequestModel):
    """Validate a single coding attempt entry.

    Attributes:
        topic: Normalized topic name.
        problem: Non-empty problem name.
        attempts: Number of attempts for the problem.
        result: Attempt result label.

    Example:
        >>> attempt = CodingAttempt(
        ...     topic=" graphs ",
        ...     problem="Graph BFS",
        ...     attempts=2,
        ...     result="incorrect",
        ... )
        >>> attempt.topic
        'Graphs'
    """

    topic: str
    problem: str
    attempts: Annotated[
        int,
        Field(
            strict=True,
            ge=MIN_ATTEMPTS_PER_PROBLEM,
            le=MAX_ATTEMPTS_PER_PROBLEM,
        ),
    ]
    result: AttemptResult

    @field_validator("topic", mode="before")
    @classmethod
    def validate_topic(cls, value: object) -> str:
        """Validate and normalize the coding attempt topic.

        Args:
            value: Raw topic value.

        Returns:
            Normalized topic name.

        Raises:
            ValueError: If topic is invalid.
        """
        return normalize_topic_name(value)

    @field_validator("problem", mode="before")
    @classmethod
    def validate_problem(cls, value: object) -> str:
        """Validate and normalize the problem name.

        Args:
            value: Raw problem value.

        Returns:
            Trimmed problem name.

        Raises:
            ValueError: If problem name is invalid.
        """
        return normalize_required_text(value, "problem", MIN_PROBLEM_NAME_LENGTH)


class MCQResult(StrictRequestModel):
    """Validate MCQ result counts for a topic.

    Attributes:
        correct: Number of correct answers.
        total: Number of attempted MCQs.

    Example:
        >>> MCQResult(correct=8, total=10).correct
        8
    """

    correct: Annotated[int, Field(strict=True, ge=MIN_MCQ_CORRECT)]
    total: Annotated[int, Field(strict=True, ge=MIN_MCQ_TOTAL)]

    @model_validator(mode="after")
    def validate_correct_not_above_total(self) -> "MCQResult":
        """Validate that correct answers do not exceed total answers.

        Returns:
            The validated MCQ result.

        Raises:
            ValueError: If correct answers exceed total answers.
        """
        if self.correct > self.total:
            raise ValueError("correct must be less than or equal to total.")
        return self


class RecommendationRequest(StrictRequestModel):
    """Validate the official recommendation request schema.

    Attributes:
        student_id: External student identifier.
        date: Daily snapshot date in ISO format.
        topic_accuracy: Topic-to-accuracy mapping.
        coding_attempts: Coding attempt entries.
        mcq_results: Topic-to-MCQ-result mapping.
        average_solving_time: Topic-to-solving-time mapping.

    Example:
        >>> request = RecommendationRequest(
        ...     student_id="student_001",
        ...     date="2026-08-02",
        ...     topic_accuracy={" graphs ": 42},
        ...     coding_attempts=[],
        ...     mcq_results={},
        ...     average_solving_time={"Graphs": "High"},
        ... )
        >>> request.topic_accuracy["Graphs"]
        42.0
    """

    student_id: str
    date: date
    topic_accuracy: dict[str, AccuracyValue] = Field(
        min_length=MIN_TOPICS,
        max_length=MAX_TOPICS,
    )
    coding_attempts: list[CodingAttempt] = Field(max_length=MAX_CODING_ATTEMPTS)
    mcq_results: dict[str, MCQResult] = Field(max_length=MAX_MCQ_TOPICS)
    average_solving_time: dict[str, SolvingTimeLevel] = Field(
        min_length=MIN_TOPICS,
        max_length=MAX_TOPICS,
    )

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value: object) -> object:
        """Validate date input before Pydantic parsing.

        Args:
            value: Raw date value.

        Returns:
            Date value accepted by Pydantic.

        Raises:
            ValueError: If date is not valid YYYY-MM-DD input.
        """
        return validate_iso_date_string(value)

    @field_validator("student_id", mode="before")
    @classmethod
    def validate_student_id(cls, value: object) -> str:
        """Validate and normalize student ID.

        Args:
            value: Raw student ID value.

        Returns:
            Trimmed student ID.

        Raises:
            ValueError: If student ID is invalid.
        """
        return normalize_required_text(
            value,
            "student_id",
            STUDENT_ID_MIN_LENGTH,
            STUDENT_ID_MAX_LENGTH,
        )

    @field_validator("topic_accuracy", mode="before")
    @classmethod
    def validate_topic_accuracy_mapping(cls, value: object) -> dict[str, object]:
        """Validate topic accuracy keys and raw numeric values.

        Args:
            value: Raw topic accuracy mapping.

        Returns:
            Normalized topic accuracy mapping.

        Raises:
            ValueError: If mapping, topic keys, or accuracy values are invalid.
        """
        normalized = normalize_topic_mapping(value)
        validate_accuracy_mapping_values(normalized)
        return normalized

    @field_validator("mcq_results", "average_solving_time", mode="before")
    @classmethod
    def validate_topic_mapping(cls, value: object) -> dict[str, object]:
        """Validate and normalize topic-keyed mappings.

        Args:
            value: Raw topic-keyed dictionary.

        Returns:
            Dictionary keyed by normalized topic names.

        Raises:
            ValueError: If mapping or topic keys are invalid.
        """
        return normalize_topic_mapping(value)

    @model_validator(mode="after")
    def validate_required_topic_signals(self) -> "RecommendationRequest":
        """Validate cross-field topic requirements.

        Returns:
            The validated recommendation request.

        Raises:
            ValueError: If a topic is missing required solving-time data.
        """
        ensure_topics_have_solving_time(self.topic_accuracy, self.average_solving_time)
        return self
