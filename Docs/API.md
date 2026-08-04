# 🎯 Learning Recommendation Engine API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

The **Learning Recommendation Engine** is an intelligent RESTful API built with **FastAPI**. It analyzes a student's daily practice metrics—including topic-wise accuracy, failed coding attempts, MCQ scores, and solving times—to automatically classify performance, prioritize weak areas, and generate actionable, tailored study plans.

---

## 🚀 Quick Start

### Base URLs

* **Local Base URL:** `http://127.0.0.1:8000`
* **Swagger UI Documentation:** `http://127.0.0.1:8000/docs`
* **ReDoc Alternative:** `http://127.0.0.1:8000/redoc`

---

## ⚙️ How It Works (Pipeline Workflow)

Every request sent to the engine goes through an automated 8-stage analysis pipeline:
```mermaid
graph TD
    Req[Request] --> S1[1. Validate]
    S1 --> S2[2. Normalize]
    S2 --> S3[3. Feature Engineering]
    S3 --> S4[4. Topic Classifier]
    S4 --> S5[5. Priority Scoring]
    S5 --> S6[6. Action Items]
    S6 --> S7[7. Practice Plan]
    S7 --> S8[8. Output]
    S8 --> Resp[Response]

    %% Styling
    style Req fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px
    style Resp fill:#efebe9,stroke:#7d6608,stroke-width:2px
    style S1 fill:#e8f8f5,stroke:#117a65,stroke-width:2px
    style S2 fill:#e8f8f5,stroke:#117a65,stroke-width:2px
    style S3 fill:#e8f8f5,stroke:#117a65,stroke-width:2px
    style S4 fill:#e8f8f5,stroke:#117a65,stroke-width:2px
    style S5 fill:#e8f8f5,stroke:#117a65,stroke-width:2px
    style S6 fill:#e8f8f5,stroke:#117a65,stroke-width:2px
    style S7 fill:#e8f8f5,stroke:#117a65,stroke-width:2px
    style S8 fill:#e8f8f5,stroke:#117a65,stroke-width:2px
```
---

## 📡 Endpoints

### `POST /recommend`

Generates personalized learning recommendations and daily practice targets based on performance payload.

#### 🛠️ Headers
| Key | Value |
| :--- | :--- |
| `Content-Type` | `application/json` |

---

### 📥 Request Body Schema

```json
{
  "student_id": "123456789",
  "date": "2026-08-03",
  "topic_accuracy": {
    "Arrays": 90,
    "Sliding Window": 35,
    "Graphs": 40,
    "Dynamic Programming": 30
  },
  "coding_attempts": [
    {
      "topic": "Sliding Window",
      "problem": "Maximum Sum Subarray",
      "attempts": 3,
      "result": "incorrect"
    },
    {
      "topic": "Graphs",
      "problem": "BFS Traversal",
      "attempts": 2,
      "result": "incorrect"
    }
  ],
  "mcq_results": {
    "Arrays": {
      "correct": 9,
      "total": 10
    },
    "Graphs": {
      "correct": 4,
      "total": 10
    },
    "Dynamic Programming": {
      "correct": 3,
      "total": 10
    }
  },
  "average_solving_time": {
    "Arrays": "Low",
    "Sliding Window": "High",
    "Graphs": "High",
    "Dynamic Programming": "High"
  }
}
```
📤 Response Schema

```JSON
{
  "success": true,
  "student_id": "123456789",
  "generated_at": "2026-08-03T00:00:00Z",
  "feature_summary": {
    "overall_accuracy": 48.75,
    "overall_failed_attempts": 5,
    "average_speed": "High"
  },
  "topic_classification": {
    "Arrays": "Mastered",
    "Dynamic Programming": "Weak",
    "Graphs": "Weak",
    "Sliding Window": "Critical"
  },
  "recommendations": [
    {
      "topic": "Sliding Window",
      "priority": 1,
      "priority_score": 62,
      "recommendation_type": "Revise Fundamentals",
      "action": "Revise Sliding Window fundamentals",
      "reason": "Sliding Window accuracy is 35% with 3 failed coding attempts, indicating a conceptual gap.",
      "practice_plan": {
        "easy": 5,
        "medium": 3,
        "hard": 1
      }
    }
  ],
  "strengths": [
    "Arrays"
  ],
  "tomorrows_focus_message": "Tomorrow's Focus: Great work on Arrays today. Focus on: Revise Sliding Window fundamentals; Revise Graphs fundamentals; Solve structured Dynamic Programming practice problems. Consistency beats intensity."
}
```
---

### 💻 Example Usage ('cURL' POST request)
```Bash
curl -X 'POST' \
  'http://127.0.0.1:8000/recommend' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "student_id": "23FE10CAI00398",
  "date": "2026-08-03",
  "topic_accuracy": {
    "Arrays": 90,
    "Sliding Window": 35
  },
  "coding_attempts": [],
  "mcq_results": {},
  "average_solving_time": {}
}'
```
---

### 🚨 Status Codes & Error Handling

Incoming payloads are strictly validated using Pydantic models (validating ID formats, accuracy ranges 0–100, topic schema, and enum values).

| Status Code | Description | Reason / Action |
| :--- | :--- | :--- |
| **200 OK** | Success | Recommendations successfully processed |
| **400 Bad Request** | JSON Parse Error | Malformed payload syntax |
| **413 Payload Too Large** | Size Exceeded | Request size exceeds maximum allowed threshold |
| **415 Unsupported Type** | Header Error | Missing or incorrect `Content-Type` header |
| **422 Unprocessable** | Schema Validation | Data type mismatches, out-of-range numerical values |
| **500 Internal Error** | Engine Failure | Server-side execution exception |
