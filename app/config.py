"""Centralized configuration for the LearnPath AI service."""

from app.core.exceptions import ConfigurationException

MASTERED_THRESHOLD = 90
STRONG_THRESHOLD = 75
MODERATE_THRESHOLD = 50
WEAK_THRESHOLD = 30
MIN_ACCURACY = 0
MAX_ACCURACY = 100
NORMALIZED_SCORE_MIN = 0
NORMALIZED_SCORE_MAX = 100
PERCENTAGE_MULTIPLIER = 100
IMPLEMENTATION_FAILURE_PENALTY = 25
PRIORITY_SCORE_PRECISION = 2
STUDENT_ID_MIN_LENGTH = 1
STUDENT_ID_MAX_LENGTH = 100
MIN_TOPIC_NAME_LENGTH = 1
MAX_TOPIC_NAME_LENGTH = 100
MIN_PROBLEM_NAME_LENGTH = 1

NO_FAILURES = 0
GOOD_FAILURE_LIMIT = 1
PRACTICE_FAILURE_LIMIT = 2
CRITICAL_FAILURE_LIMIT = 3
MIN_ATTEMPTS_PER_PROBLEM = 1
MAX_ATTEMPTS_PER_PROBLEM = 100

TIME_SCORE = {
    "Low": 10,
    "Medium": 30,
    "High": 70,
    "Very High": 100,
}

ACCURACY_WEIGHT = 0.45
FAILED_ATTEMPT_WEIGHT = 0.25
SOLVING_TIME_WEIGHT = 0.20
CONSISTENCY_WEIGHT = 0.10

DEFAULT_RECOMMENDATIONS = 3
MIN_RECOMMENDATIONS = 1
MAX_RECOMMENDATIONS = 5

MASTERED_PRACTICE = {"easy": 0, "medium": 1, "hard": 1}
STRONG_PRACTICE = {"easy": 0, "medium": 2, "hard": 1}
MODERATE_PRACTICE = {"easy": 2, "medium": 3, "hard": 0}
WEAK_PRACTICE = {"easy": 3, "medium": 3, "hard": 1}
CRITICAL_PRACTICE = {"easy": 5, "medium": 3, "hard": 1}

MASTERED = "Mastered"
STRONG = "Strong"
MODERATE = "Moderate"
WEAK = "Weak"
CRITICAL = "Critical"

CRITICAL_PRIORITY = 5
HIGH_PRIORITY = 4
MEDIUM_PRIORITY = 3
LOW_PRIORITY = 2
MINIMAL_PRIORITY = 1
CLASSIFICATION_SEVERITY = {
    CRITICAL: CRITICAL_PRIORITY,
    WEAK: HIGH_PRIORITY,
    MODERATE: MEDIUM_PRIORITY,
    STRONG: LOW_PRIORITY,
    MASTERED: MINIMAL_PRIORITY,
}

HIGH_MCQ_THRESHOLD = STRONG_THRESHOLD
LOW_MCQ_THRESHOLD = MODERATE_THRESHOLD
GOOD_CODING_SUCCESS_THRESHOLD = STRONG_THRESHOLD
LOW_CODING_SUCCESS_THRESHOLD = MODERATE_THRESHOLD
HIGH_SPEED_SCORE_THRESHOLD = TIME_SCORE["High"]

RECOMMENDATION_CONFLICT_ORDER = [
    "Revise Fundamentals",
    "Implementation Practice",
    "Theory Revision",
    "Structured Practice",
    "Speed Practice",
    "Reinforcement Practice",
    "Maintain Strength",
]

ACTION_TEMPLATES = {
    "Revise Fundamentals": "Revise {topic} fundamentals",
    "Structured Practice": "Solve structured {topic} practice problems",
    "Implementation Practice": "Practice {topic} implementation",
    "Theory Revision": "Review {topic} concepts",
    "Speed Practice": "Complete timed {topic} practice",
    "Reinforcement Practice": "Reinforce {topic} with focused practice",
    "Maintain Strength": "Maintain strength in {topic}",
}

RESPONSE_TIMESTAMP_SUFFIX = "T00:00:00Z"

ENABLE_POSITIVE_REINFORCEMENT = True
MAX_EXPLANATION_LENGTH = 180
MAX_FOCUS_TOPICS = 3
MAX_MESSAGE_LENGTH = 600

MOTIVATIONAL_MESSAGES = [
    "Keep building consistency.",
    "Small improvements every day lead to big results.",
    "Stay focused and trust the process.",
    "Consistency beats intensity.",
    "You're improving one topic at a time.",
]

API_TITLE = "Learning Recommendation API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "AI-powered personalized learning recommendation engine."

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

MAX_TOPICS = 100
MIN_TOPICS = 1
MAX_CODING_ATTEMPTS = 500
MAX_MCQ_TOPICS = 100
MAX_REQUEST_SIZE_BYTES = 1_048_576
MIN_MCQ_CORRECT = 0
MIN_MCQ_TOTAL = 1
ISO_DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"

SUCCESS_MESSAGE = "Recommendations generated successfully"
VALIDATION_ERROR = "Validation failed"
UNKNOWN_ERROR = "Unexpected server error"
INVALID_JSON_ERROR = "Invalid JSON payload"
METHOD_NOT_ALLOWED_ERROR = "Method not allowed"
UNSUPPORTED_MEDIA_TYPE_ERROR = "Unsupported media type"
PAYLOAD_TOO_LARGE_ERROR = "Payload too large"
JSON_CONTENT_TYPES = frozenset({"application/json", "application/json; charset=utf-8"})
BODY_HTTP_METHODS = frozenset({"POST", "PUT", "PATCH"})

SORT_ORDER = [
    "priority",
    "classification",
    "failed_attempts",
    "accuracy",
    "topic",
]

ENABLE_SPEED_ANALYSIS = True
ENABLE_CONSISTENCY_ANALYSIS = True
ENABLE_MCQ_ANALYSIS = True
ENABLE_CODING_ANALYSIS = True
ENABLE_HISTORY_ANALYSIS = False
ENABLE_SPACED_REPETITION = False
ENABLE_MACHINE_LEARNING = False
ENABLE_LLM_EXPLANATIONS = False


def validate_config() -> None:
    """Validate application configuration at startup.

    Returns:
        None.

    Raises:
        ConfigurationException: If configuration values are inconsistent.

    Example:
        >>> validate_config()
    """
    _validate_accuracy_thresholds()
    _validate_priority_weights()
    _validate_recommendation_limits()
    _validate_payload_limits()
    _validate_feature_config()
    _validate_message_templates()
    _validate_classification_labels()


def _validate_accuracy_thresholds() -> None:
    if not MAX_ACCURACY > MASTERED_THRESHOLD > STRONG_THRESHOLD:
        raise ConfigurationException("Accuracy thresholds are not ordered.")
    if not STRONG_THRESHOLD > MODERATE_THRESHOLD > WEAK_THRESHOLD > MIN_ACCURACY:
        raise ConfigurationException("Accuracy thresholds are not ordered.")


def _validate_priority_weights() -> None:
    weights_total = (
        ACCURACY_WEIGHT
        + FAILED_ATTEMPT_WEIGHT
        + SOLVING_TIME_WEIGHT
        + CONSISTENCY_WEIGHT
    )
    if round(weights_total, 2) != 1.0:
        raise ConfigurationException("Priority weights must sum to 1.0.")


def _validate_recommendation_limits() -> None:
    if not MIN_RECOMMENDATIONS <= DEFAULT_RECOMMENDATIONS <= MAX_RECOMMENDATIONS:
        raise ConfigurationException("Recommendation limits are invalid.")


def _validate_payload_limits() -> None:
    if MIN_TOPICS < 1 or MAX_TOPICS < MIN_TOPICS:
        raise ConfigurationException("Topic limits are invalid.")
    if MAX_CODING_ATTEMPTS < 0 or MAX_MCQ_TOPICS < 0:
        raise ConfigurationException("Payload collection limits are invalid.")
    if MAX_REQUEST_SIZE_BYTES <= 0:
        raise ConfigurationException("Maximum request size is invalid.")


def _validate_feature_config() -> None:
    if NORMALIZED_SCORE_MIN != MIN_ACCURACY:
        raise ConfigurationException("Normalized score minimum is invalid.")
    if NORMALIZED_SCORE_MAX != MAX_ACCURACY:
        raise ConfigurationException("Normalized score maximum is invalid.")
    if IMPLEMENTATION_FAILURE_PENALTY <= NORMALIZED_SCORE_MIN:
        raise ConfigurationException("Implementation failure penalty is invalid.")
    if HIGH_SPEED_SCORE_THRESHOLD not in TIME_SCORE.values():
        raise ConfigurationException("High speed threshold is invalid.")
    if not ACTION_TEMPLATES:
        raise ConfigurationException("Action templates cannot be empty.")


def _validate_message_templates() -> None:
    if not MOTIVATIONAL_MESSAGES:
        raise ConfigurationException("Motivational messages cannot be empty.")


def _validate_classification_labels() -> None:
    labels = [MASTERED, STRONG, MODERATE, WEAK, CRITICAL]
    if len(labels) != len(set(labels)):
        raise ConfigurationException("Classification labels must be unique.")
