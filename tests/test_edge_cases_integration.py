"""Integration coverage for documented edge cases."""

from copy import deepcopy

from fastapi.testclient import TestClient

import app.api.routes as routes
from app.main import app

client = TestClient(app)
error_client = TestClient(app, raise_server_exceptions=False)


def base_payload() -> dict[str, object]:
    """Build a minimal mutable valid payload."""
    return {
        "student_id": "student_001",
        "date": "2026-08-02",
        "topic_accuracy": {"Graphs": 42},
        "coding_attempts": [],
        "mcq_results": {},
        "average_solving_time": {"Graphs": "High"},
    }


def test_empty_optional_signals_still_generate_recommendation() -> None:
    """Case 2 and 3: empty coding attempts and MCQ results are allowed."""
    response = client.post("/recommend", json=base_payload())

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["recommendations"]
    assert data["recommendations"][0]["recommendation_type"] == "Structured Practice"


def test_high_accuracy_with_repeated_failures_gets_implementation_practice() -> None:
    """Case 19: repeated failures outweigh otherwise strong accuracy."""
    payload = base_payload()
    payload["topic_accuracy"] = {"Graphs": 88}
    payload["coding_attempts"] = [
        {
            "topic": "Graphs",
            "problem": "Graph BFS",
            "attempts": 4,
            "result": "incorrect",
        }
    ]
    payload["average_solving_time"] = {"Graphs": "Medium"}

    response = client.post("/recommend", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["topic_classification"]["Graphs"] == "Strong"
    assert data["recommendations"][0]["recommendation_type"] == (
        "Implementation Practice"
    )


def test_more_than_five_weak_topics_returns_top_five_only() -> None:
    """Case 26: weak-topic overload is capped at five recommendations."""
    payload = base_payload()
    topics = {f"Topic {index}": 35 + index for index in range(6)}
    payload["topic_accuracy"] = topics
    payload["average_solving_time"] = {topic: "High" for topic in topics}

    response = client.post("/recommend", json=payload)

    assert response.status_code == 200
    recommendations = response.json()["recommendations"]
    assert len(recommendations) == 5
    assert len({item["topic"] for item in recommendations}) == 5


def test_all_critical_topics_return_top_three_only() -> None:
    """Case 7: all-critical payloads keep the stricter top-three cap."""
    payload = base_payload()
    topics = {f"Topic {index}": index for index in range(6)}
    payload["topic_accuracy"] = topics
    payload["average_solving_time"] = {topic: "Very High" for topic in topics}

    response = client.post("/recommend", json=payload)

    assert response.status_code == 200
    recommendations = response.json()["recommendations"]
    assert len(recommendations) == 3
    assert all(
        response.json()["topic_classification"][item["topic"]] == "Critical"
        for item in recommendations
    )


def test_unexpected_exception_returns_safe_json(monkeypatch) -> None:
    """Case 38: unexpected errors are logged and masked."""

    def raise_unexpected_error(request):
        raise RuntimeError("internal details")

    monkeypatch.setattr(routes, "generate_learning_recommendations", raise_unexpected_error)

    response = error_client.post("/recommend", json=deepcopy(base_payload()))

    assert response.status_code == 500
    assert response.json() == {
        "success": False,
        "error": "Unexpected server error.",
    }
