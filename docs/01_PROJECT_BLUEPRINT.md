# AI-Powered Personalised Learning Recommendation Engine
## Complete Project Blueprint — TechLearn Placement Prep Platform

Prepared as a pre-build planning document, adapted from the "6 Documents You Need Before Writing Any Code" framework. Since this is a backend AI microservice (no UI of its own), Documents 3 & 4 have been replaced with **System Architecture** and **Recommendation Engine Logic Design** — the two documents that actually determine whether this feels like a smart tutor or a glorified if-else script.

---

## Table of Contents
1. PRD — Product Requirements Document
2. TRD — Technical Requirements Document
3. System Architecture & Data Flow
4. Recommendation Engine Logic Design (the core differentiator)
5. Backend Schema — Request/Response & Internal Models
6. Implementation Plan — 36-Hour Build Sequence
7. Testing & Validation Plan
8. README / Documentation Plan
9. MERN Integration Guide
10. Demo Recording Script
11. Assumptions Log

---

## 01 — PRD: Product Requirements Document

| Field | Detail |
|---|---|
| **Service Name** | LearnPath AI — Personalised Learning Recommendation Engine |
| **Tagline** | "Turn today's mistakes into tomorrow's plan." |
| **Problem** | Students on placement-prep platforms grind through MCQs and coding problems but rarely get a synthesized, explainable picture of *what* to fix next and *why*. Generic "practice more" advice doesn't change behavior. |
| **Who feels it** | Students preparing for tech placements (coding + CS fundamentals + aptitude), who have limited time and need prioritized, not exhaustive, guidance. |
| **Core Value Proposition** | Not just a score dashboard — an explainable recommendation layer that reads accuracy + attempts + solving time together (not in isolation) and produces a short, human-readable action plan, the way a mentor would. |
| **Target User (persona)** | A 3rd/4th-year engineering student, prepping 1–2 hrs/day for placements, doing daily DSA + MCQ sets on TechLearn. They don't want more data — they want to be told what to do next in plain English. |
| **Must-Have Features** | 1. Accept structured daily performance data (topic accuracy, coding submissions, MCQ results, solving time)<br>2. Classify topics into Strength / Moderate / Weak<br>3. Generate ranked, explainable recommendations (not a flat list)<br>4. Generate a natural-language "Tomorrow's Focus" message<br>5. Expose everything via REST API, stateless, JSON in/out |
| **Nice-to-Have (v2)** | Trend tracking across multiple days (is Graphs improving or stuck?); difficulty-adaptive question suggestions; integration with an LLM for richer explanations; spaced-repetition scheduling for weak topics |
| **Out of Scope (v1)** | User authentication, persistent storage/database, frontend UI, actual question bank/content, notification delivery (email/push) |
| **User Stories** | As a student, I want to see my weak topics ranked by severity, so I know what to fix first.<br>As a student, I want a short reason for each recommendation, so I trust it isn't random.<br>As a backend engineer, I want a single stateless endpoint, so I can call it after each day's data is aggregated in MongoDB. |
| **Success Metrics** | API responds < 300ms for typical payload; recommendations are directionally correct on 100% of hand-crafted test cases (e.g. the example in the task); output is directly renderable in a React card with zero frontend logic needed. |

---

## 02 — TRD: Technical Requirements Document

| Field | Detail |
|---|---|
| **Language** | Python 3.11+ |
| **API Framework** | FastAPI (auto OpenAPI docs at `/docs`, async-ready, Pydantic-native) |
| **Data Handling** | Pandas/NumPy — used for the scoring/weighting math, not strictly required but shows engineering maturity |
| **ML (optional layer)** | Scikit-learn **not required for v1 correctness** — this task rewards a well-designed **rule-based + weighted-scoring engine** that is explainable. A black-box ML classifier would actually hurt the "explain why" requirement. (See Recommendation Logic doc for the honest reasoning on this choice — you'll want this in your README as a deliberate design decision, not a shortcut.) |
| **Validation** | Pydantic v2 models for strict request/response typing |
| **Server** | Uvicorn (ASGI) |
| **Testing** | Pytest + FastAPI TestClient |
| **Docs** | FastAPI auto-generated Swagger/ReDoc + a hand-written README |
| **Packaging** | `requirements.txt` + optional Dockerfile for portability into the MERN stack's infra |
| **Folder Structure** | See below |
| **Env Variables** | None required for v1 (stateless, no DB, no external API keys) — keep it that way; it's a selling point for the assessor (zero infra dependency to run it) |
| **Hard Constraints** | Must be stateless (no DB) per task scope; must return valid JSON always, even on partial/missing input; must not crash on malformed payloads — return structured validation errors instead |

**Proposed folder structure:**
```
learnpath-ai/
├── app/
│   ├── main.py                 # FastAPI app, route registration
│   ├── models/
│   │   ├── request_models.py   # Pydantic input schemas
│   │   └── response_models.py  # Pydantic output schemas
│   ├── services/
│   │   ├── classifier.py       # Strength/Weak/Moderate classification
│   │   ├── scorer.py           # Weighted priority scoring
│   │   ├── recommender.py      # Recommendation generation + reasoning
│   │   └── message_generator.py# Natural language "Tomorrow's Focus" builder
│   ├── config.py                # Thresholds, weights (centralized, tunable)
│   └── utils/
│       └── validators.py
├── tests/
│   ├── test_api.py
│   ├── test_classifier.py
│   ├── test_scorer.py
│   └── fixtures/
│       └── sample_payloads.json
├── requirements.txt
├── Dockerfile
├── README.md
└── demo/
    └── sample_requests.http
```

---

## 03 — System Architecture & Data Flow

*(This replaces "App Flow" from the standard framework, since there's no UI to navigate — instead we map how a single request flows through the engine.)*

**Request lifecycle:**

```
MERN Backend (Node/Express)
   │  aggregates the student's daily activity from MongoDB
   ▼
POST /recommend  (JSON payload: topic accuracies, coding attempts, MCQ results, solving time)
   │
   ▼
[FastAPI] Pydantic validation layer
   │  rejects malformed input with 422 + structured error, never a silent failure
   ▼
[Classifier Service]
   │  buckets each topic → Strength / Moderate / Weak
   │  using accuracy thresholds + submission failure signal
   ▼
[Scorer Service]
   │  computes a composite "priority score" per weak/moderate topic
   │  factors: accuracy gap, failed attempts, solving time, topic exam-weight
   ▼
[Recommender Service]
   │  ranks topics by priority score
   │  generates 3–5 concrete action items (revise / practice / solve N problems)
   │  attaches a plain-English "why" to each, referencing the actual numbers
   ▼
[Message Generator]
   │  assembles the ranked items into a "Tomorrow's Focus" narrative block
   ▼
JSON Response → back to Node/Express → stored in MongoDB / rendered in React
```

**Key architectural decision:** the engine is **fully stateless per request** — it takes one day's snapshot and returns recommendations for that snapshot. Historical trend tracking (v2) would live in Mongo on the Node side and just get passed in as additional context fields later; the Python service doesn't need to own history. This keeps the service simple, horizontally scalable, and trivially easy for your MERN team to call from any route.

---

## 04 — Recommendation Engine Logic Design (the core differentiator)

This is the document that separates a mediocre submission from a standout one. Assessors reviewing this task will see dozens of submissions that just do `if accuracy < 50: recommend`. Here's how we make this genuinely good.

### 4.1 Inputs considered per topic
Not just accuracy — a **composite signal**:
- **Accuracy %** — the baseline
- **Failed submission count** — repeated wrong attempts on the *same* topic signal a conceptual gap, not a slip
- **Solving time** — high time + low accuracy = struggling with fundamentals; high time + high accuracy = slow but correct (different intervention: speed drills, not concept revision)
- **MCQ vs Coding mismatch** — if MCQ accuracy is high but coding accuracy is low on the same topic, that's a "understands theory, can't implement" signal — a distinct, specific recommendation type

### 4.2 Classification logic
```
Strength   : accuracy >= 75%  AND failed_attempts <= 1
Moderate   : 50% <= accuracy < 75%  OR (accuracy >= 75% AND failed_attempts > 1)
Weak       : accuracy < 50%  OR failed_attempts >= 2 on that topic
```
Thresholds live in `config.py`, not hardcoded — so they're tunable without touching logic (good engineering practice to call out in your README).

### 4.3 Priority scoring (why Sliding Window beats Graphs beats DP in the example)
```
priority_score = (100 - accuracy) * 0.5
               + (failed_attempts * 10) * 0.3
               + (time_penalty) * 0.2
```
Where `time_penalty` is a normalized 0–100 value derived from solving time relative to expected time for that difficulty. Highest score = highest priority in "Tomorrow's Focus."

Using the task's own example:
- Sliding Window: 35% accuracy, 3 failed attempts, high time → **highest priority**
- Graphs: 40% accuracy, 2 failed attempts (BFS) → **second**
- Dynamic Programming: 30% accuracy, but 0 recorded attempts (never seriously tried) → flagged differently: *"foundational gap, not a performance gap"* — recommend **structured practice** (3 medium problems) rather than "revise fundamentals," since revision implies they tried and failed, but here they haven't engaged yet

This distinction — *engaged-but-struggling* vs *not-yet-engaged* — is exactly the kind of nuance that makes output feel intelligent instead of templated.

### 4.4 Recommendation type templates
Each weak/moderate topic maps to one of these **action types**, chosen by which signal dominates:

| Signal pattern | Action type | Example phrasing |
|---|---|---|
| Low accuracy + high failed attempts | "Revise fundamentals" | *Revise Sliding Window fundamentals — 3 failed attempts suggest a pattern-recognition gap, not a careless error.* |
| Low accuracy + few/no attempts | "Structured practice" | *Solve 3 Medium-level DP questions — you haven't engaged deeply with this topic yet.* |
| Moderate accuracy + high solving time | "Speed drilling" | *Time yourself on Arrays problems — you're accurate but slow, which will cost you in timed rounds.* |
| Good MCQ, poor coding on same topic | "Implementation gap" | *Practice implementing Graph BFS in code — your MCQ score shows you understand the theory, the gap is translation to code.* |

This mapping is what makes the "why" behind every recommendation feel earned rather than boilerplate.

### 4.5 Message Generator
Takes the ranked, typed recommendation list and assembles it into the exact "Tomorrow's Focus" format shown in the task brief — a short header + 3–5 bullet actions, each with a one-line reason, plus one motivational closing line.

### 4.6 Why rule-based over ML for v1
Worth stating explicitly in your README: with a single day of data per student and no historical dataset to train on, a black-box classifier would need synthetic/fake training data — undermining trust exactly where explainability matters most. A transparent, tunable scoring system is the *correct* engineering choice here, not a shortcut. (v2 note: once historical multi-day data exists, a lightweight model — e.g. gradient boosting on engineered features — could refine the priority weights, with the rule engine kept as a fallback/explainer layer.)

---

## 05 — Backend Schema: Request/Response Models

### Request — `POST /recommend`
```json
{
  "student_id": "stu_1234",
  "date": "2026-08-02",
  "topic_accuracy": {
    "Arrays": 90,
    "Sliding Window": 35,
    "Graphs": 40,
    "Dynamic Programming": 30
  },
  "coding_attempts": [
    {"topic": "Sliding Window", "problem": "Longest Substring", "result": "incorrect", "attempts": 3},
    {"topic": "Graphs", "problem": "Graph BFS", "result": "incorrect", "attempts": 2}
  ],
  "mcq_results": {
    "Sliding Window": {"correct": 4, "total": 10},
    "Graphs": {"correct": 8, "total": 10}
  },
  "average_solving_time_minutes": {
    "Arrays": 12,
    "Sliding Window": 28,
    "Graphs": 25,
    "Dynamic Programming": 20
  }
}
```

### Response
```json
{
  "student_id": "stu_1234",
  "date": "2026-08-02",
  "topic_classification": {
    "Arrays": "Strength",
    "Sliding Window": "Weak",
    "Graphs": "Weak",
    "Dynamic Programming": "Weak"
  },
  "recommendations": [
    {
      "topic": "Sliding Window",
      "priority": 1,
      "action_type": "revise_fundamentals",
      "action": "Revise Sliding Window fundamentals",
      "reason": "35% accuracy with 3 failed submissions on the same problem type indicates a conceptual gap, not a careless mistake."
    },
    {
      "topic": "Graphs",
      "priority": 2,
      "action_type": "implementation_gap",
      "action": "Practice implementing Graph BFS in code",
      "reason": "80% MCQ accuracy but repeated coding failures — you understand the theory, the gap is in implementation."
    },
    {
      "topic": "Dynamic Programming",
      "priority": 3,
      "action_type": "structured_practice",
      "action": "Solve 3 Medium-level Dynamic Programming questions",
      "reason": "Low accuracy with no recorded attempts yet — this is an unexplored area, not a struggling one."
    }
  ],
  "tomorrows_focus_message": "Tomorrow's Focus:\n1. Revise Sliding Window fundamentals — repeated failed attempts point to a pattern-recognition gap.\n2. Practice Graph Traversal problems in code — your theory is solid, translation to code needs work.\n3. Solve 3 Medium-level DP questions — time to start building intuition here.\n\nYou're strong in Arrays — keep that consistency going while you close these three gaps."
}
```

All fields typed via Pydantic — invalid/missing fields return a `422` with a clear field-level error, never a silent 500.

---

## 06 — Implementation Plan (36-Hour Build Sequence)

| Phase | Time budget | Goal | Done criteria |
|---|---|---|---|
| **1. Setup** | 1 hr | Repo, venv, FastAPI skeleton, folder structure, `requirements.txt` | `uvicorn app.main:app` runs, `/docs` loads |
| **2. Schema** | 2 hrs | Pydantic request/response models, validation edge cases | Malformed payload returns clean 422, not a crash |
| **3. Classifier + Scorer** | 4 hrs | Implement thresholds, priority scoring math, config-driven weights | Unit tests pass on the task's own example input |
| **4. Recommender + Message Generator** | 4 hrs | Action-type mapping, reason-string generation, "Tomorrow's Focus" assembly | Output matches expected structure/tone from task brief |
| **5. API wiring + error handling** | 2 hrs | Connect services into `/recommend`, handle empty/partial data gracefully | No 500s on partial input (e.g. missing MCQ data for a topic) |
| **6. Testing** | 3 hrs | Pytest suite: unit tests per service + integration test on full endpoint | >90% of core logic covered, all pass |
| **7. Docs** | 3 hrs | README (approach, API docs, MERN integration, assumptions), inline docstrings | README is self-sufficient — no need to read code to understand the service |
| **8. Dockerize (optional polish)** | 2 hrs | Dockerfile, run instructions | `docker run` serves the API identically to local |
| **9. Demo recording** | 2 hrs | Script, record, edit lightly | 3–5 min, shows Swagger UI + a live example call + explanation of the "why" logic |
| **Buffer** | ~4 hrs | Bug fixes, polish, edge cases | — |

Total: ~27 hrs of work inside the 36-hr window, leaving slack for the unexpected.

---

## 07 — Testing & Validation Plan

- **Unit tests** per service (classifier, scorer, recommender) with hand-crafted inputs, including the exact example from the task brief as a golden test case.
- **Edge cases to explicitly test:** a student with all-strength topics (empty recommendation list, positive message), a student with zero coding attempts recorded, missing MCQ data for a topic, duplicate topic names with different casing.
- **API-level integration test** via FastAPI's `TestClient` hitting `/recommend` end-to-end.
- **Manual Swagger UI walkthrough** before recording the demo, to catch anything automated tests miss.

---

## 08 — README / Documentation Plan

Your README should cover, in this order:
1. **One-paragraph overview** — what the service does and why rule-based scoring was chosen over ML for v1
2. **Quickstart** — clone, install, run, hit `/docs`
3. **API documentation** — endpoint, request/response schema, example curl call
4. **Recommendation logic explained** — a condensed version of Document 04 above, so a reviewer understands the reasoning without reading source
5. **MERN integration guide** — see Document 09 below, paste in directly
6. **Assumptions** — see Document 11 below
7. **Possible v2 extensions** — trend tracking, LLM-enhanced explanations, spaced repetition

---

## 09 — MERN Integration Guide

Since the Python service is stateless and REST-based, integration is a thin proxy call from Express:

```javascript
// Node/Express side — after aggregating today's activity from MongoDB
const axios = require('axios');

app.post('/api/students/:id/daily-recommendation', async (req, res) => {
  const performanceData = await buildPerformancePayload(req.params.id); // your Mongo aggregation
  const { data } = await axios.post('http://learnpath-ai:8000/recommend', performanceData);
  await Recommendation.create({ studentId: req.params.id, ...data }); // persist in Mongo
  res.json(data);
});
```

- The Python service owns **zero** persistence or auth — Express remains the source of truth for student identity and history.
- Recommended deployment: containerize the FastAPI service and run it as an internal microservice alongside the Node app (same VPC/network), called only server-to-server — never exposed directly to the React frontend.
- React just renders whatever JSON Express forwards — no frontend logic needed to interpret the recommendation structure.

---

## 10 — Demo Recording Script (3–5 min)

1. **0:00–0:30** — One-line problem statement: "Students get scores, not direction. This service turns raw performance data into an explainable action plan."
2. **0:30–1:30** — Show Swagger UI (`/docs`), walk through the request schema.
3. **1:30–3:00** — Fire the task's example payload, walk through the response: classification → priority scoring → the "why" behind each recommendation, specifically calling out the Sliding Window vs Dynamic Programming distinction (struggling vs unexplored) as the "smart" part.
4. **3:00–4:00** — Briefly show the test suite passing, and the config file showing tunable thresholds (engineering maturity signal).
5. **4:00–4:30** — Close with the MERN integration snippet and a one-line note on the ML-vs-rules design decision.

---

## 11 — Assumptions Log

- No authentication/authorization is implemented in this service — assumed to sit behind the existing MERN auth layer.
- No persistent storage — each request is a self-contained daily snapshot; history/trends are a Node/Mongo responsibility in v2.
- Topic names are assumed to arrive pre-normalized from the frontend/DB (no fuzzy topic-name matching in v1).
- Solving-time "expected baseline per difficulty" is approximated with reasonable defaults in `config.py`, documented as tunable rather than empirically derived (since no historical dataset was provided).
- English-only output for v1.

---

### Next step
This is the full blueprint — nothing built yet. When you're ready, say the word and I'll start with **Phase 1 (Setup)** and work through the implementation plan phase by phase, showing you code and test results as we go.
