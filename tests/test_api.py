"""API foundation tests."""

from fastapi.testclient import TestClient

from app.config import MAX_REQUEST_SIZE_BYTES
from app.main import app

client = TestClient(app)


def api_example_payload() -> dict[str, object]:
    """Build the official API example request payload.

    Returns:
        API example payload.

    Raises:
        None.

    Example:
        >>> api_example_payload()["student_id"]
        'student_001'
    """
    return {
        "student_id": "student_001",
        "date": "2026-08-02",
        "topic_accuracy": {
            "Arrays": 92,
            "Sliding Window": 35,
            "Graphs": 42,
            "Dynamic Programming": 28,
        },
        "coding_attempts": [
            {
                "topic": "Sliding Window",
                "problem": "Longest Substring",
                "attempts": 3,
                "result": "incorrect",
            },
            {
                "topic": "Graphs",
                "problem": "Graph BFS",
                "attempts": 2,
                "result": "incorrect",
            },
        ],
        "mcq_results": {
            "Arrays": {
                "correct": 9,
                "total": 10,
            },
            "Graphs": {
                "correct": 8,
                "total": 10,
            },
        },
        "average_solving_time": {
            "Arrays": "Low",
            "Sliding Window": "High",
            "Graphs": "High",
            "Dynamic Programming": "Medium",
        },
    }


def test_openapi_schema_is_available() -> None:
    """Verify FastAPI documentation schema is available.

    Returns:
        None.

    Raises:
        AssertionError: If OpenAPI schema cannot be loaded.

    Example:
        >>> test_openapi_schema_is_available()
    """
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Learning Recommendation API"


def test_openapi_schema_documents_recommend_endpoint() -> None:
    """Verify OpenAPI includes the recommendation endpoint.

    Returns:
        None.

    Raises:
        AssertionError: If OpenAPI omits the endpoint contract.

    Example:
        >>> test_openapi_schema_documents_recommend_endpoint()
    """
    response = client.get("/openapi.json")

    schema = response.json()

    assert "/recommend" in schema["paths"]
    assert "post" in schema["paths"]["/recommend"]
    assert schema["paths"]["/recommend"]["post"]["summary"] == (
        "Generate learning recommendations"
    )
    assert {"200", "400", "413", "415", "422", "500"} <= set(
        schema["paths"]["/recommend"]["post"]["responses"]
    )


def test_swagger_docs_are_available() -> None:
    """Verify Swagger UI is available.

    Returns:
        None.

    Raises:
        AssertionError: If Swagger UI cannot be loaded.

    Example:
        >>> test_swagger_docs_are_available()
    """
    response = client.get("/docs")

    assert response.status_code == 200
    assert "Swagger UI" in response.text


def test_recommend_accepts_api_example_payload() -> None:
    """Verify POST /recommend accepts the official example request.

    Returns:
        None.

    Raises:
        AssertionError: If the API example request cannot be serialized.

    Example:
        >>> test_recommend_accepts_api_example_payload()
    """
    response = client.post("/recommend", json=api_example_payload())

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["student_id"] == "student_001"
    assert data["generated_at"] == "2026-08-02T00:00:00Z"
    assert data["feature_summary"] == {
        "overall_accuracy": 49.25,
        "overall_failed_attempts": 5,
        "average_speed": "High",
    }
    assert data["topic_classification"]["Arrays"] == "Mastered"
    assert data["topic_classification"]["Graphs"] == "Weak"
    assert data["topic_classification"]["Dynamic Programming"] == "Critical"
    assert data["strengths"] == ["Arrays"]
    assert data["recommendations"]
    for item in data["recommendations"]:
        assert {"topic", "priority", "priority_score", "recommendation_type"} <= set(
            item
        )
        assert {"action", "reason", "practice_plan"} <= set(item)


def test_recommend_validation_error_matches_api_contract() -> None:
    """Verify validation failures use the documented response shape.

    Returns:
        None.

    Raises:
        AssertionError: If validation errors expose raw framework details.

    Example:
        >>> test_recommend_validation_error_matches_api_contract()
    """
    response = client.post(
        "/recommend",
        json={
            "student_id": "",
            "topic_accuracy": {
                "Graphs": 140,
            },
        },
    )

    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["error"] == "Validation failed"
    assert isinstance(data["details"], list)
    assert {"field": "student_id", "message": "student_id must not be empty."} in (
        data["details"]
    )
    assert {
        "field": "topic_accuracy",
        "message": "Accuracy for Graphs must be between 0 and 100.",
    } in data["details"]


def test_recommend_malformed_json_returns_documented_error() -> None:
    """Verify malformed JSON returns the documented 400 response.

    Returns:
        None.

    Raises:
        AssertionError: If malformed JSON is not handled as API contract says.

    Example:
        >>> test_recommend_malformed_json_returns_documented_error()
    """
    response = client.post(
        "/recommend",
        content='{"student_id":',
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "success": False,
        "error": "Invalid JSON payload",
    }


def test_recommend_empty_body_returns_documented_error() -> None:
    """Verify empty JSON request bodies return 400.

    Returns:
        None.

    Raises:
        AssertionError: If empty bodies are not handled as malformed JSON.

    Example:
        >>> test_recommend_empty_body_returns_documented_error()
    """
    response = client.post(
        "/recommend",
        content="",
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "success": False,
        "error": "Invalid JSON payload",
    }


def test_recommend_wrong_method_returns_documented_error() -> None:
    """Verify GET /recommend returns documented 405 JSON.

    Returns:
        None.

    Raises:
        AssertionError: If unsupported methods return non-JSON errors.

    Example:
        >>> test_recommend_wrong_method_returns_documented_error()
    """
    response = client.get("/recommend")

    assert response.status_code == 405
    assert response.json() == {
        "success": False,
        "error": "Method not allowed",
    }


def test_unsupported_media_type_returns_json_error() -> None:
    """Verify body requests reject unsupported media types.

    Returns:
        None.

    Raises:
        AssertionError: If unsupported media types are not rejected.

    Example:
        >>> test_unsupported_media_type_returns_json_error()
    """
    response = client.post(
        "/recommend",
        content="plain text",
        headers={"content-type": "text/plain"},
    )

    assert response.status_code == 415
    assert response.json() == {
        "success": False,
        "error": "Unsupported media type",
    }


def test_missing_content_type_with_body_returns_json_error() -> None:
    """Verify body requests without content type are rejected.

    Returns:
        None.

    Raises:
        AssertionError: If missing content type is accepted.
    """
    response = client.post(
        "/recommend",
        content='{"student_id":"student_001"}',
    )

    assert response.status_code == 415
    assert response.json() == {
        "success": False,
        "error": "Unsupported media type",
    }


def test_payload_larger_than_configured_limit_returns_json_error() -> None:
    """Verify oversized payloads are rejected before routing.

    Returns:
        None.

    Raises:
        AssertionError: If oversized payloads are not rejected.

    Example:
        >>> test_payload_larger_than_configured_limit_returns_json_error()
    """
    content = "x" * (MAX_REQUEST_SIZE_BYTES + 1)

    response = client.post(
        "/recommend",
        content=content,
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 413
    assert response.json() == {
        "success": False,
        "error": "Payload too large",
    }
