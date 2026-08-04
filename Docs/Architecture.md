# 🏛️ System Architecture

## 📌 Overview

The **Learning Recommendation Engine** follows a clean, layered architecture designed to strictly separate API handling, core business logic, feature engineering, recommendation generation, and data models. 

Each layer adheres to the **Single Responsibility Principle (SRP)**, ensuring the project remains modular, highly testable, and effortless to scale.

---

## 🗺️ Architectural Diagrams

For detailed visual workflows and component breakdowns, refer to:

* 📊 [System Architecture](diagrams/Architecture.png)
* 🔄 [Recommendation Workflow](diagrams/recommendation%20pipeline.png)
* ⚡ [Request Lifecycle](diagrams/request%20lifecycle.png)
* 📁 [Project Structure](diagrams/Project%20Structure.png)

---

## 🧱 System Layers & Structure

| Layer | Primary Location | Key Role |
| :--- | :--- | :--- |
| **API Layer** | [`app/api/`](../app/api/) | Ingestion, response formatting, & HTTP handling |
| **Validation Layer** | [`app/models/`](../app/utils/validators.py) | Data schemas, typing, & payload validation |
| **Feature Engineering Layer** | [`app/services/feature_engineering.py`](../app/services/feature_extractor.py) | Metric extraction & performance signal calculations |
| **Classification Layer** | [`app/services/classifier.py`](../app/services/classifier.py) | Topic mastery evaluation & grouping |
| **Recommendation Engine** | [`app/services/recommendation_engine.py`](../app/services/recommendation_engine.py) | Core logic, priority sorting, & practice plans |
| **Response Layer** | [`app/api/`](../app/models/) | Payload formatting & API contract enforcement |

---

## 🔍 Detailed Layer Breakdown

### 🌐 API Layer
📍 **Location:** [`app/api/`](../app/api/routes.py)

#### Responsibilities
* **Request Ingestion:** Receives raw HTTP requests from clients.
* **Schema Validation:** Ensures incoming data matches required endpoint formats.
* **Response Serialization:** Returns structured JSON outputs with standard status codes.
* **Exception Handling:** Catches and standardizes API errors gracefully.

> [!NOTE]  
> **Architectural Boundary:** This layer is strictly decoupled and contains **zero** recommendation logic.

---

### 🛡️ Validation Layer
📍 **Location:** [`app/models/`](../app/utils/)

#### Responsibilities
* **Payload Verification:** Validates incoming request payloads against Pydantic models.
* **Type Safety:** Enforces strict data types across all payload attributes.
* **Early Rejection:** Intercepts and rejects malformed requests before processing.
* **Error Reporting:** Generates structured, actionable validation error models.

---

### ⚙️ Feature Engineering Layer
📍 **Location:** [`app/services/feature_extractor.py`](../app/services/feature_extractor.py)

#### Responsibilities
* **Accuracy Metrics:** Calculates topic-level and overall user accuracy scores.
* **Attempt Tracking:** Computes failed coding attempts and friction points.
* **Practice Analysis:** Aggregates user practice history and engagement stats.
* **Derived Features:** Produces structured feature vectors required for classification.

---

### 🏷️ Classification Layer
📍 **Location:** [`app/services/classifier.py`](../app/services/classifier.py)

#### Responsibilities
Categorizes every learning topic into distinct mastery tiers using predefined business rules:

* 🟢 **Mastered**
* 🔵 **Strong**
* 🟡 **Weak**
* 🔴 **Critical**

> [!TIP]
> Topic classification outputs directly feed into the Recommendation Engine to target areas needing immediate focus.

---

### 🧠 Recommendation Engine *(Core Logic)*
📍 **Location:** [`app/services/recommendation_engine.py`](../app/services/recommendation_engine.py)

#### Responsibilities
* **Topic Prioritization:** Sorts and isolates weak/critical topic areas.
* **Personalized Recommendations:** Generates targeted practice suggestions.
* **Actionable Plans:** Constructs daily practice schedules for the user.
* **Focus Messaging:** Generates dynamic *"Tomorrow's Focus"* messaging.

---

### 📤 Request - Response Layer
📍 **Location:** [`app/models/`](../app/models/)

#### Responsibilities
* **JSON Formatting:** Constructs the final outbound HTTP payload.
* **Contract Maintenance:** Guarantees consistent field names and API interface contracts.
* **Structure Consistency:** Ensures standard payload responses across all endpoints.

---

## 🧪 Testing Strategy

The system relies on automated pytest suites to verify stability:

* **Unit Tests:** Independent verification of core services and classification rules.
* **Integration Tests:** End-to-end data processing validation across layers.
* **Edge Case Tests:** Handling of incomplete, zero-activity, or malformed data profiles.
* **API Tests:** Endpoint validation using FastAPI's test client.
