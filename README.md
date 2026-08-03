# Learning Recommendation Engine

A modular recommendation engine built with **FastAPI** that delivers personalized learning suggestions based on user preferences, skills, and learning objectives.

This project focuses on building a production-ready backend architecture for recommendation systems, emphasizing clean software design, maintainability, testing, and scalability. The current implementation establishes the service foundation, API structure, configuration management, validation, logging, and development tooling, providing a solid base for future recommendation algorithms.

> **Project Status:** Backend infrastructure and project foundation are complete. Recommendation logic and ranking algorithms will be introduced in upcoming phases.

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

## Project Structure

```text
app/
  api/
  core/
  models/
  services/
  utils/
tests/
  fixtures/
docs/
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

