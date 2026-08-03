\# CODEX INSTRUCTIONS

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document is the primary implementation guide for Codex.



Together with the Project Blueprint, it defines the complete architecture, implementation rules, coding standards, and constraints for this project.



The Project Blueprint (01\_PROJECT\_BLUEPRINT.md) is the product specification.



This document defines HOW the software must be implemented.



Whenever there is uncertainty, THIS document and the Project Blueprint are the only sources of truth.



Never invent features that are not defined.



\---



\# Project Goal



Build a production-quality backend microservice that analyzes a student's daily learning performance and generates explainable learning recommendations.



The service must expose a REST API using FastAPI.



Input:



\- Topic accuracy

\- Coding attempts

\- MCQ performance

\- Solving time



Output:



\- Topic classifications

\- Ranked recommendations

\- Human-readable explanations

\- End-of-day learning message



The service must remain completely stateless.



\---



\# High Level Architecture



```

&#x20;               Student Performance



&#x20;                        │



&#x20;                        ▼



&#x20;             FastAPI Request Validation



&#x20;                        │



&#x20;                        ▼



&#x20;             Feature Extraction Layer



&#x20;                        │



&#x20;                        ▼



&#x20;             Topic Classification Engine



&#x20;                        │



&#x20;                        ▼



&#x20;            Priority Scoring Engine



&#x20;                        │



&#x20;                        ▼



&#x20;           Recommendation Generator



&#x20;                        │



&#x20;                        ▼



&#x20;          Explanation Generator



&#x20;                        │



&#x20;                        ▼



&#x20;         Tomorrow's Focus Generator



&#x20;                        │



&#x20;                        ▼



&#x20;               JSON API Response

```



Every stage must remain independent.



\---



\# Source of Truth



The following documents must be followed in order.



1\. Project Blueprint

2\. Codex Instructions

3\. Recommendation Rules

4\. Config Specification

5\. Validation Rules



If multiple documents conflict, use the document with the lower number.



Never make assumptions outside these documents.



\---



\# Development Principles



The implementation must prioritize:



\- readability

\- maintainability

\- modularity

\- explainability

\- extensibility

\- simplicity



Avoid unnecessary complexity.



The recommendation engine should be understandable by another engineer without requiring comments explaining complicated logic.



\---



\# Architecture Principles



Follow these principles throughout the project.



\## Single Responsibility Principle



Each module performs one responsibility.



Example



classifier.py



ONLY classifies topics.



No scoring.



No recommendation generation.



No formatting.



\---



scorer.py



ONLY calculates scores.



No message generation.



No API logic.



\---



message\_generator.py



ONLY converts recommendation objects into natural language.



\---



main.py



ONLY exposes endpoints.



Business logic must never exist inside route handlers.



\---



\# Dependency Direction



Allowed



```

API



↓



Services



↓



Utilities



↓



Configuration

```



Not allowed



```

Utilities



↓



API



or



Configuration



↓



Services

```



Configuration should never depend on application code.



\---



\# Stateless Design



This application must remain stateless.



Do NOT implement



\- database

\- authentication

\- login

\- session

\- cache

\- user storage



Every request is completely independent.



\---



\# Configuration Rules



All configurable values belong inside config.py.



Never hardcode



accuracy thresholds



weights



priority levels



time thresholds



recommendation limits



magic numbers



Every configurable value must exist exactly once.



\---



\# Code Quality Requirements



Python Version



3.11+



Use



Type Hints



throughout the project.



Use



PEP8



naming conventions.



Maximum function length



40 lines



Maximum file length



Prefer below 300 lines.



Maximum nesting depth



3



Avoid long if/else chains.



Prefer helper functions.



\---



\# Naming Conventions



Variables



snake\_case



Functions



snake\_case



Classes



PascalCase



Constants



UPPER\_CASE



Enums



PascalCase



Models



PascalCase



\---



\# Documentation Rules



Every public function must include



Purpose



Parameters



Returns



Raises



Example



Example



```python

def calculate\_priority(...):

&#x20;   """

&#x20;   Calculate recommendation priority score.



&#x20;   Args:

&#x20;       ...



&#x20;   Returns:

&#x20;       ...



&#x20;   Raises:

&#x20;       ...



&#x20;   """

```



\---



\# Logging



Never use



print()



Use Python logging.



Levels



DEBUG



INFO



WARNING



ERROR



CRITICAL



Important events



API request received



validation failed



recommendations generated



unexpected exception



Never log



student personal data



future passwords



tokens



API keys



\---



\# Error Handling



Never crash the application.



Always return structured JSON.



Example



```

{

&#x20;   "success":false,

&#x20;   "error":"Validation failed"

}

```



Never expose stack traces.



Never expose internal exceptions.



\---



\# Validation



Every incoming request must pass Pydantic validation.



Reject



negative accuracy



accuracy >100



empty topic names



duplicate required fields



incorrect data types



missing required fields



\---



\# Recommendation Engine Rules



The recommendation engine must be completely deterministic.



The same input must always generate the same output.



No randomness.



No timestamps inside recommendations.



No probabilistic behavior.



\---



\# Recommendation Ordering



Recommendations must always be sorted by



Highest Priority Score



↓



Highest Failed Attempts



↓



Lowest Accuracy



↓



Alphabetical Topic Name



This guarantees deterministic output.



\---



\# Explanation Generation



Every recommendation must explain



WHY



the recommendation exists.



Bad



"Practice Graphs."



Good



"Graphs accuracy is 42% with two incorrect coding submissions, indicating difficulty applying traversal concepts."



Never generate recommendations without explanations.



\---



\# Performance Requirements



Average response time



<300ms



Typical payload



Memory usage



Minimal



Avoid unnecessary DataFrame creation.



Prefer built-in Python when Pandas provides no benefit.



\---



\# Testing Requirements



Every business logic module must have unit tests.



Every endpoint must have integration tests.



Target coverage



90%



Minimum



80%



All tests must pass before implementation is considered complete.



\---



\# API Design Rules



REST only.



JSON only.



UTF-8.



No XML.



No HTML.



All responses should use consistent structure.



\---



\# Folder Responsibilities



API



Receives requests



↓



Models



Validate data



↓



Services



Business logic



↓



Utilities



Shared helpers



↓



Config



Constants



Never violate this dependency chain.



\---



\# Future Compatibility



The architecture must allow replacing



Rule Engine



↓



Machine Learning Model



↓



LLM



without changing the API contract.



Recommendation generation must remain isolated from transport logic.



\---



\# Security



Even though authentication is out of scope,



follow secure coding practices.



Validate every request.



Never trust input.



Never execute user input.



Never use eval().



Never build dynamic imports.



\---



\# Git Practices



Small commits.



Meaningful commit messages.



Examples



feat: implement recommendation scoring



fix: validate duplicate topics



test: add API integration tests



docs: update README



\---



\# Build Order



The project must be implemented in the following order.



Phase 1



Project setup



↓



Phase 2



Folder structure



↓



Phase 3



Configuration



↓



Phase 4



Models



↓



Phase 5



Validation



↓



Phase 6



Classification Engine



↓



Phase 7



Priority Scoring



↓



Phase 8



Recommendation Generator



↓



Phase 9



Message Generator



↓



Phase 10



REST API



↓



Phase 11



Testing



↓



Phase 12



Documentation



Do not skip phases.



\---



\# Things Codex Must Never Do



Do not invent features.



Do not add databases.



Do not add authentication.



Do not introduce machine learning.



Do not hardcode thresholds.



Do not write business logic inside API routes.



Do not duplicate code.



Do not ignore validation.



Do not leave TODO placeholders.



Do not leave unused imports.



Do not generate dead code.



Do not suppress exceptions silently.



\---



\# Definition of Success



The implementation is complete only if



✓ FastAPI application runs



✓ Swagger UI works



✓ Request validation works



✓ Classification works



✓ Priority scoring works



✓ Recommendations are deterministic



✓ Every recommendation includes an explanation



✓ Tomorrow's Focus message is generated



✓ Unit tests pass



✓ Integration tests pass



✓ README is complete



✓ Code follows PEP8



✓ The service can be integrated into a MERN backend without modification



\---



End of Document

