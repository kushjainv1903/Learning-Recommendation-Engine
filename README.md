# LearnPath AI

LearnPath AI is the backend foundation for a stateless FastAPI microservice that will generate explainable personalized learning recommendations. This Phase 1 scaffold intentionally contains no recommendation business logic and no `/recommend` endpoint implementation.

## Phase 1 Scope

- FastAPI application factory and entry point
- Centralized configuration constants
- Startup configuration validation
- Logging setup
- Package and module structure
- Pytest, Black, isort, Ruff, and coverage configuration
- Docker runtime definition

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

