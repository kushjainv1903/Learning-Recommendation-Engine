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

