
tally · current session
61%
≈4.3 sonnet msgs
resets in 4h 32m
weekly · all models
5% · Thu 17:30


















Readme · MD
<div align="center">
# 🎯 LearnPath AI — Learning Recommendation Engine
 
**An explainable, rule-driven FastAPI service that turns raw student practice data into personalized, prioritized study plans.**
 
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Pytest](https://img.shields.io/badge/Tested_with-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Ruff](https://img.shields.io/badge/Lint-Ruff-D7FF64?style=for-the-badge)](https://docs.astral.sh/ruff/)
[![Black](https://img.shields.io/badge/Code_Style-Black-000000?style=for-the-badge)](https://black.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
 
[Quick Start](#-quick-start) • [How It Works](#-how-it-works) • [API](#-api-reference) • [Architecture](#-architecture) • [Testing](#-testing) • [Docs](#-documentation)
 
</div>
---
 
## 📖 Overview
 
**LearnPath AI** analyzes a student's daily practice signals — topic-wise accuracy, failed coding attempts, MCQ performance, and solving speed — and turns them into a transparent, rule-based diagnosis of *where the student stands* and *what they should do next*.
 
Every topic is classified into a mastery tier, every recommendation carries a human-readable reason, and every response ships with a ready-to-use daily practice plan. No black-box scoring — every number the API returns can be traced back to a documented rule.
 
**Why it's useful:**
 
- 🧠 **Explainable, not a black box** — every recommendation states *why* (e.g. *"Sliding Window accuracy is 35% with 3 failed attempts, indicating a conceptual gap"*).
- 🎯 **Prioritized, not just listed** — weak topics are ranked by a weighted priority score, so students know what to fix first.
- 🧩 **Deterministic & stateless** — same input always produces the same output; no hidden session state between requests.
- 🛡️ **Strictly validated** — every payload is checked by Pydantic before it ever touches business logic.
---
 
## ⚡ Key Features
 
| Category | Feature |
| :--- | :--- |
| **Core Engine** | 8-stage analysis pipeline: validate → normalize → feature engineering → classify → score → recommend → plan → respond |
| **Classification** | 5-tier topic mastery model — `Mastered` · `Strong` · `Moderate` · `Weak` · `Critical` |
| **Scoring** | Weighted priority score from accuracy, failed attempts, solving speed, and consistency |
| **Recommendations** | Topic-specific actions, plain-language reasons, and tiered practice plans (easy / medium / hard) |
| **API** | Single, well-documented `POST /recommend` contract with strict status-code semantics |
| **Validation** | Pydantic v2 models enforce ID formats, 0–100 accuracy ranges, and payload size limits |
| **Quality** | Pytest suite, `ruff` linting, `black` formatting, `isort` import ordering |
| **Ops** | Dockerized for one-command local runs and deployment |
| **Docs** | Auto-generated Swagger UI & ReDoc, plus hand-written architecture references in `Docs/` |
 
---
 
## 🚀 Quick Start
 
### Prerequisites
 
- Python **3.11+**
- Git
- pip
### Setup
 
```bash
# 1. Clone the repository
git clone https://github.com/kushjainv1903/Learning-Recommendation-Engine.git
cd Learning-Recommendation-Engine
 
# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
 
# 3. Install dependencies
pip install -r requirements.txt
 
# 4. Run the server
uvicorn app.main:app --reload
```
 
The API is now live at `http://127.0.0.1:8000`, with interactive docs at `/docs` (Swagger UI) and `/redoc` (ReDoc).
 
### Or run it with Docker
 
```bash
docker build -t learnpath-ai .
docker run -p 8000:8000 learnpath-ai
```
 
📘 Full setup, troubleshooting, and platform-specific notes live in **[Docs/Installation.md](Docs/Installation.md)**.
 
---
 
## 🧠 How It Works
 
Every request flows through an 8-stage pipeline before a response is returned:
 
<div align="center">
<img src="Docs/diagrams/API workflow.png" alt="8-stage recommendation pipeline" width="360">
</div>
| Stage | Responsibility |
| :---: | :--- |
| 1. **Validate** | Reject malformed or out-of-range payloads before any processing begins |
| 2. **Normalize** | Standardize raw input into a consistent internal shape |
| 3. **Feature Engineering** | Derive per-topic accuracy, failure counts, and speed signals |
| 4. **Topic Classifier** | Assign each topic a mastery tier using threshold rules |
| 5. **Priority Scoring** | Compute a weighted urgency score per weak topic |
| 6. **Action Items** | Generate the specific action and human-readable reason per topic |
| 7. **Practice Plan** | Build an easy/medium/hard problem-count plan for each focus area |
| 8. **Output** | Assemble the final, contract-compliant JSON response |
 
### Topic classification tiers
 
| Tier | Meaning |
| :--- | :--- |
| 🟢 **Mastered** | Consistently high accuracy — no intervention needed |
| 🔵 **Strong** | Solid grasp with minor room to sharpen |
| 🟡 **Moderate** | Inconsistent performance — light reinforcement recommended |
| 🟠 **Weak** | Clear conceptual gaps — targeted practice required |
| 🔴 **Critical** | Low accuracy combined with repeated failed attempts — top priority |
 
### Priority score weighting
 
The priority score behind each recommendation blends four signals:
 
| Signal | Weight |
| :--- | :---: |
| Topic accuracy | 45% |
| Failed coding attempts | 25% |
| Average solving time | 20% |
| Practice consistency | 10% |
 
---
 
## 📡 API Reference
 
### `POST /recommend`
 
Generates personalized recommendations and a daily practice plan from a student's performance snapshot.
 
**Headers**
 
| Key | Value |
| :--- | :--- |
| `Content-Type` | `application/json` |
 
**Example request**
 
```bash
curl -X POST 'http://127.0.0.1:8000/recommend' \
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
 
**Example response**
 
```json
{
  "success": true,
  "student_id": "23FE10CAI00398",
  "generated_at": "2026-08-03T00:00:00Z",
  "feature_summary": {
    "overall_accuracy": 48.75,
    "overall_failed_attempts": 5,
    "average_speed": "High"
  },
  "topic_classification": {
    "Arrays": "Mastered",
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
      "practice_plan": { "easy": 5, "medium": 3, "hard": 1 }
    }
  ],
  "strengths": ["Arrays"],
  "tomorrows_focus_message": "Tomorrow's Focus: Great work on Arrays today. Focus on: Revise Sliding Window fundamentals. Consistency beats intensity."
}
```
 
**Status codes**
 
| Code | Meaning |
| :---: | :--- |
| `200` | Success — recommendations generated |
| `400` | Malformed JSON |
| `413` | Payload exceeds the maximum allowed size |
| `415` | Missing or incorrect `Content-Type` header |
| `422` | Schema validation failed (type mismatch, out-of-range value, etc.) |
| `500` | Unexpected server-side error |
 
📘 Full request/response schemas and field-level rules: **[Docs/API.md](Docs/API.md)**
 
---
 
## 🏛️ Architecture
 
The service follows a strictly layered architecture — each layer has one job, and no layer reaches past its boundary.
 
<div align="center">
<img src="Docs/diagrams/Architecture.png" alt="System architecture" width="380">
</div>
| Layer | Location | Responsibility |
| :--- | :--- | :--- |
| **API Layer** | [`app/api/`](app/api/routes.py) | Request ingestion, routing, response serialization |
| **Validation Layer** | [`app/models/`](app/models/) | Pydantic schemas, type safety, early rejection |
| **Feature Engineering** | [`app/services/feature_extractor.py`](app/services/feature_extractor.py) | Accuracy/attempt/speed metric extraction |
| **Classification** | [`app/services/classifier.py`](app/services/classifier.py) | Topic mastery tier assignment |
| **Scoring** | [`app/services/scorer.py`](app/services/scorer.py) | Weighted priority score calculation |
| **Recommendation Engine** | [`app/services/recommendation_engine.py`](app/services/recommendation_engine.py) | Orchestrates the full pipeline end to end |
| **Explanation & Messaging** | [`app/services/explanation_generator.py`](app/services/explanation_generator.py), [`app/services/message_generator.py`](app/services/message_generator.py) | Human-readable reasons and the "Tomorrow's Focus" message |
| **Response Layer** | [`app/models/response_models.py`](app/models/response_models.py) | Final API contract enforcement |
 
<details>
<summary><strong>More diagrams</strong> — recommendation pipeline & request lifecycle</summary>
<br>
<div align="center">
<img src="Docs/diagrams/recommendation pipeline.png" alt="Recommendation pipeline" width="500"><br><br>
<img src="Docs/diagrams/request lifecycle.png" alt="Request lifecycle" width="700">
</div>
</details>
📘 Full architectural breakdown: **[Docs/Architecture.md](Docs/Architecture.md)**
 
---
 
## 📁 Project Structure
 
<div align="center">
<img src="Docs/diagrams/Project Structure.png" alt="Project structure" width="700">
</div>
```text
Learning-Recommendation-Engine/
├── app/
│   ├── api/                       # Routing & endpoint definitions
│   │   └── routes.py
│   ├── core/                      # Shared constants & exception types
│   │   ├── constants.py
│   │   └── exceptions.py
│   ├── models/                    # Pydantic request/response contracts
│   │   ├── request_models.py
│   │   └── response_models.py
│   ├── services/                  # Business logic
│   │   ├── feature_extractor.py
│   │   ├── classifier.py
│   │   ├── scorer.py
│   │   ├── recommender.py
│   │   ├── recommendation_engine.py
│   │   ├── explanation_generator.py
│   │   └── message_generator.py
│   ├── utils/
│   │   └── logger.py
│   ├── config.py                  # Thresholds, weights, centralized settings
│   └── main.py                    # FastAPI app entry point
├── demo/
│   └── sample_requests.http       # Ready-to-run sample HTTP requests
├── Docs/
│   ├── API.md
│   ├── Architecture.md
│   ├── Installation.md
│   ├── diagrams/                  # Mermaid-exported architecture diagrams
│   └── Screenshots/                # UI & terminal walkthrough screenshots
├── tests/
│   ├── fixtures/                  # Shared test payloads
│   └── test_*.py                  # Unit, integration & edge-case suites
├── Dockerfile
├── pyproject.toml                 # black / isort / ruff / pytest config
├── requirements.txt
└── LICENSE
```
 
---
 
## 🧪 Testing
 
The project is backed by a comprehensive Pytest suite covering unit, integration, edge-case, and API-contract testing.
 
```bash
# Run the full suite
pytest
 
# With coverage
pytest --cov=app
 
# Lint & format check
ruff check .
black --check .
isort --check .
```
 
---
 
## 🖼️ Gallery
 
<div align="center">
<img src="Docs/Screenshots/local-host-dashboard.png" alt="Swagger UI dashboard" width="420">
<img src="Docs/Screenshots/sample input.png" alt="Sample request input" width="420"><br><br>
<img src="Docs/Screenshots/response-URL-generated.png" alt="Generated response" width="420">
<img src="Docs/Screenshots/server-terminal-success.png" alt="Server terminal output" width="420">
</div>
---
 
## 📚 Documentation
 
| Doc | Description |
| :--- | :--- |
| [Docs/Installation.md](Docs/Installation.md) | Full setup, environment, and troubleshooting guide |
| [Docs/API.md](Docs/API.md) | Complete request/response schema and error reference |
| [Docs/Architecture.md](Docs/Architecture.md) | Layer-by-layer architectural breakdown |
 
---
 
## 🤝 Contributing
 
Contributions, issues, and feature requests are welcome.
 
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Run `black .`, `isort .`, and `ruff check .` before committing
4. Make sure `pytest` passes locally
5. Open a pull request with a clear description of the change
---
 
## 📄 License
 
Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.



 
</div>
