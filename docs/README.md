\# 🎯 AI-Powered Personalized Learning Recommendation Engine



> Turn today's learning performance into tomorrow's personalized study plan.



\---



\# Overview



This project is a backend AI-powered recommendation service developed for the \*\*TechLearn Placement Preparation Platform\*\*.



The service analyzes a student's daily learning performance—including topic accuracy, coding submissions, MCQ results, and solving time—and generates personalized learning recommendations with clear explanations.



The application is built as a \*\*stateless FastAPI microservice\*\*, making it easy to integrate into any MERN (MongoDB, Express, React, Node.js) application.



\---



\# Problem Statement



Students preparing for technical placements often receive only raw scores after completing coding and MCQ practice.



Raw scores answer:



> "How did I perform?"



They do \*\*not\*\* answer:



\- What should I study tomorrow?

\- Which topic needs immediate attention?

\- Why is this topic important?

\- Am I struggling conceptually or only in implementation?



This recommendation engine bridges that gap by converting performance metrics into an explainable action plan.



\---



\# Solution



The recommendation engine evaluates multiple performance indicators together instead of relying on accuracy alone.



It considers:



\- Topic-wise Accuracy

\- Coding Attempts

\- Failed Coding Submissions

\- MCQ Performance

\- Average Solving Time



These signals are transformed into engineered features that drive personalized recommendations.



\---



\# Architecture



```

Student Performance



&#x20;       │



&#x20;       ▼



FastAPI Request



&#x20;       │



&#x20;       ▼



Validation Layer



&#x20;       │



&#x20;       ▼



Feature Extraction



&#x20;       │



&#x20;       ▼



Topic Classification



&#x20;       │



&#x20;       ▼



Priority Scoring



&#x20;       │



&#x20;       ▼



Recommendation Generator



&#x20;       │



&#x20;       ▼



Explanation Generator



&#x20;       │



&#x20;       ▼



Tomorrow's Focus Message



&#x20;       │



&#x20;       ▼



JSON Response

```



\---



\# Recommendation Logic



Unlike simple rule-based systems that only check accuracy, this engine evaluates multiple learning signals simultaneously.



\### Signals Used



\- Topic Accuracy

\- Failed Coding Attempts

\- MCQ Performance

\- Coding Success Rate

\- Average Solving Time



These are converted into derived features:



\- Concept Score

\- Implementation Score

\- Speed Score

\- Consistency Score

\- Learning Priority Score



The recommendation engine then ranks topics and generates explainable recommendations.



\---



\# Features



\## Topic Classification



Topics are classified as:



\- Mastered

\- Strong

\- Moderate

\- Weak

\- Critical



\---



\## Priority Ranking



Recommendations are ranked using a weighted priority score.



Topics with the highest learning priority appear first.



\---



\## Explainable Recommendations



Every recommendation includes a human-readable explanation.



Example:



> Revise Sliding Window fundamentals because repeated incorrect submissions indicate a conceptual misunderstanding rather than isolated mistakes.



\---



\## Personalized Study Plan



The engine generates an end-of-day message such as:



```

Tomorrow's Focus



• Revise Sliding Window Fundamentals



• Practice Graph Traversal Problems



• Solve 3 Medium Dynamic Programming Questions



Great work on Arrays today.

Keep building consistency.

```



\---



\# Technology Stack



| Component | Technology |

|------------|------------|

| Language | Python 3.11+ |

| API Framework | FastAPI |

| Validation | Pydantic |

| Data Processing | NumPy (optional) |

| Testing | Pytest |

| Documentation | Swagger/OpenAPI |

| Server | Uvicorn |



\---



\# Project Structure



```

learnpath-ai/



app/



├── api/



├── models/



├── services/



├── utils/



├── config.py



├── main.py



tests/



docs/



README.md

```



\---



\# API



\## Endpoint



```

POST /recommend

```



\---



\## Request Example



```json

{

&#x20; "student\_id":"student\_001",



&#x20; "topic\_accuracy":{

&#x20;     "Arrays":90,

&#x20;     "Graphs":42,

&#x20;     "Dynamic Programming":35

&#x20; },



&#x20; "coding\_attempts":\[



&#x20; ],



&#x20; "mcq\_results":{



&#x20; },



&#x20; "average\_solving\_time":{

&#x20;     "Graphs":"High"

&#x20; }

}

```



\---



\## Response Example



```json

{

&#x20; "success": true,



&#x20; "recommendations":\[



&#x20; ],



&#x20; "tomorrows\_focus\_message":"..."

}

```



\---



\# Running the Project



\## Clone Repository



```bash

git clone <repository-url>



cd learnpath-ai

```



\---



\## Create Virtual Environment



Windows



```bash

python -m venv .venv



.venv\\Scripts\\activate

```



Linux / macOS



```bash

python3 -m venv .venv



source .venv/bin/activate

```



\---



\## Install Dependencies



```bash

pip install -r requirements.txt

```



\---



\## Run Server



```bash

uvicorn app.main:app --reload

```



\---



\## Open Swagger Documentation



```

http://localhost:8000/docs

```



\---



\# Testing



Run all tests



```bash

pytest

```



Coverage



```bash

pytest --cov

```



\---



\# MERN Integration



The FastAPI service is designed to operate as an independent recommendation microservice.



Typical flow:



```

React



↓



Express



↓



MongoDB



↓



FastAPI Recommendation Engine



↓



JSON Recommendations



↓



React UI

```



Express collects student performance from MongoDB and forwards it to the FastAPI service.



The recommendation engine remains completely stateless.



\---



\# Design Decisions



\## Why FastAPI?



\- Automatic request validation

\- OpenAPI documentation

\- High performance

\- Clean architecture



\---



\## Why Rule-Based Instead of Machine Learning?



The assignment provides no historical training dataset.



The evaluator also requires every recommendation to include a human-readable explanation.



A transparent scoring engine is therefore a better engineering choice than an untrained machine learning model.



The architecture remains extensible for future ML integration.



\---



\# Assumptions



\- Student data is aggregated externally.

\- Authentication is handled by the parent MERN application.

\- No database is required.

\- Recommendations are generated independently for each request.

\- Topic names are provided consistently.



\---



\# Future Improvements



Potential enhancements include:



\- Multi-day learning trends

\- Spaced repetition scheduling

\- Adaptive difficulty recommendations

\- Historical performance analytics

\- LLM-generated personalized feedback

\- Learning velocity prediction



\---



\# API Documentation



FastAPI automatically generates interactive documentation.



Swagger UI



```

http://localhost:8000/docs

```



ReDoc



```

http://localhost:8000/redoc

```



\---



\# Repository Contents



```

docs/



Project documentation



app/



FastAPI source code



tests/



Automated test suite



README.md



Project overview

```



\---



\# Author



\*\*Kush Jain\*\*



B.Tech Computer Science (AI \& ML)



\---



\# License



This project was developed as part of a technical assessment for TechLearn.

