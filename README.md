# Learning Recommendation Engine

A modular recommendation engine built with **FastAPI** that delivers personalized learning suggestions based on user preferences, skills, and learning objectives.

This project focuses on building a production-ready backend architecture for recommendation systems, emphasizing clean software design, maintainability, testing, and scalability. The current implementation establishes the service foundation, API structure, configuration management, validation, logging, and development tooling, providing a solid base for future recommendation algorithms.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pytest](https://img.shields.io/badge/Tested_with-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Ruff](https://img.shields.io/badge/Lint-Ruff-D7FF64?style=for-the-badge)
![Black](https://img.shields.io/badge/Code_Style-Black-000000?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</p>

## ⚡ Key Features

| Category | Feature & Description |
| :--- | :--- |
| **Core** | **🚀 FastAPI Backend** — Modular, scalable architecture following clean code principles. |
| **Config** | **⚙️ Centralized Settings** — Environment-based validation powered by Pydantic. |
| **Quality** | **🧪 Testing & Tooling** — Pytest suite, Ruff, Black, and `isort` integration. |
| **Ops** | **🐳 Dockerized** — Containerized setup for seamless deployment & local dev. |
| **Docs** | **📚 Auto Documentation** — Interactive Swagger UI & ReDoc endpoints. |
## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI is available at:

```text
http://localhost:8000/docs
```

## 📁 Project Structure

```text
Learning-Recommendation-Engine/
├── app/
│   ├── api/                      # API routes and endpoint definitions
│   ├── core/                     # Application configuration and shared utilities
│   ├── models/                   # Pydantic request and response models
│   ├── services/                 # Business logic and recommendation services
│   ├── utils/                    # Helper functions and reusable utilities
│   ├── __init__.py
│   ├── config.py                 # Core configuration handling
│   └── main.py                   # FastAPI application entry point
├── demo/
│   └── sample_requests.http      # Sample HTTP requests for testing endpoints
├── docs/                         # Project documentation
├── tests/                        # Unit and integration tests
│   ├── fixtures/                 # Test fixtures and shared data
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_classifier.py
│   ├── test_config.py
│   ├── test_edge_cases_integration.py
│   ├── test_explanation_generator.py
│   ├── test_feature_extractor.py
│   ├── test_message_generator.py
│   ├── test_recommendation_engine.py
│   ├── test_recommender.py
│   ├── test_scorer.py
│   └── test_validation.py
├── .gitignore
├── COPYRIGHT.md
├── Dockerfile                    # Docker image configuration
├── pyproject.toml                # Project metadata and tooling configuration
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```
## Development Commands

```bash
black .
isort .
ruff check .
pytest
```

## Architectural Boundary

Phase 1 creates the foundation only. Request schemas, validation rules, feature extraction, classification, scoring, recommendation generation, explanation generation, message generation, and the `/recommend` endpoint are reserved for later phases.

