\# PROJECT STRUCTURE

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document defines the project directory structure, module responsibilities, dependency rules, naming conventions, and implementation boundaries.



Every source file must have a clearly defined responsibility.



No file should perform multiple unrelated tasks.



This document exists to prevent tightly coupled code and ensure long-term maintainability.



\---



\# Project Directory



```

learnpath-ai/

│

├── app/

│   ├── \_\_init\_\_.py

│   ├── main.py

│   ├── config.py

│   │

│   ├── api/

│   │   ├── \_\_init\_\_.py

│   │   └── routes.py

│   │

│   ├── models/

│   │   ├── \_\_init\_\_.py

│   │   ├── request\_models.py

│   │   └── response\_models.py

│   │

│   ├── services/

│   │   ├── \_\_init\_\_.py

│   │   ├── classifier.py

│   │   ├── scorer.py

│   │   ├── recommender.py

│   │   ├── explanation\_generator.py

│   │   ├── message\_generator.py

│   │   └── recommendation\_engine.py

│   │

│   ├── utils/

│   │   ├── \_\_init\_\_.py

│   │   ├── validators.py

│   │   ├── helpers.py

│   │   └── logger.py

│   │

│   └── core/

│       ├── \_\_init\_\_.py

│       ├── constants.py

│       └── exceptions.py

│

├── tests/

│   ├── test\_api.py

│   ├── test\_classifier.py

│   ├── test\_scorer.py

│   ├── test\_recommender.py

│   ├── test\_message\_generator.py

│   └── fixtures/

│       ├── valid\_payload.json

│       ├── invalid\_payload.json

│       └── expected\_output.json

│

├── docs/

│

├── requirements.txt

├── Dockerfile

├── README.md

└── .gitignore

```



\---



\# Module Responsibilities



Every module has ONE responsibility.



Never violate this rule.



\---



\# main.py



Purpose



Application entry point.



Responsibilities



\- Create FastAPI application

\- Register routes

\- Configure middleware

\- Configure logging

\- Configure exception handlers



Must NOT



\- Calculate scores

\- Generate recommendations

\- Validate business logic



\---



\# api/routes.py



Purpose



Expose REST endpoints.



Responsibilities



\- Receive requests

\- Validate request models

\- Call Recommendation Engine

\- Return responses



Must NOT



\- Perform calculations

\- Generate recommendations

\- Build explanations



Business logic belongs inside Services.



\---



\# models/request\_models.py



Purpose



Request validation.



Responsibilities



\- Define Pydantic request models

\- Validate incoming JSON

\- Validate data types

\- Validate required fields



Must NOT



\- Calculate anything



\---



\# models/response\_models.py



Purpose



Standardize API responses.



Responsibilities



\- Success model

\- Error model

\- Recommendation model

\- Topic model



Must NOT



Contain business logic.



\---



\# services/classifier.py



Purpose



Topic classification.



Responsibilities



Determine



Mastered



Strong



Moderate



Weak



Critical



Input



Performance metrics



Output



Topic classifications



Must NOT



Generate recommendations.



\---



\# services/scorer.py



Purpose



Priority score calculation.



Responsibilities



Calculate



Concept Score



Implementation Score



Speed Score



Consistency Score



Learning Priority Score



Must NOT



Generate explanations.



Must NOT



Generate messages.



\---



\# services/recommender.py



Purpose



Recommendation generation.



Responsibilities



Convert scores into



Action



Reason



Practice Plan



Priority



Must NOT



Calculate raw scores.



\---



\# services/explanation\_generator.py



Purpose



Generate human-readable explanations.



Input



Recommendation



Output



Natural language explanation.



Must NOT



Change recommendation priorities.



\---



\# services/message\_generator.py



Purpose



Generate



Tomorrow's Focus



message.



Responsibilities



\- Positive reinforcement

\- Summary

\- Top priorities

\- Motivational closing



Must NOT



Perform calculations.



\---



\# services/recommendation\_engine.py



Purpose



Orchestrator.



Responsibilities



Coordinate



Classifier



↓



Scorer



↓



Recommender



↓



Explanation Generator



↓



Message Generator



This is the ONLY service allowed to call other services.



\---



\# utils/



Purpose



Reusable helper functions.



Examples



Formatting



Date utilities



Common validation helpers



Text utilities



Must NOT



Contain recommendation logic.



\---



\# core/constants.py



Purpose



Global constants.



Examples



Classification names



Recommendation names



Message templates



Never duplicate constants elsewhere.



\---



\# core/exceptions.py



Purpose



Custom exception classes.



Examples



ValidationException



RecommendationException



ConfigurationException



\---



\# Dependency Rules



Allowed



```

Routes



↓



Recommendation Engine



↓



Services



↓



Utilities



↓



Core

```



Not Allowed



```

Utilities



↓



Routes

```



Not Allowed



```

Models



↓



Services

```



Not Allowed



```

Config



↓



Routes

```



Dependencies always point downward.



\---



\# Communication Rules



Services communicate ONLY through return values.



Never modify global state.



Never rely on hidden side effects.



\---



\# Configuration Access



Every configurable value comes from



config.py



Never



Hardcode



Thresholds



Weights



Maximum recommendations



Classification limits



Timeouts



\---



\# File Size Limits



Recommended



Python files



<300 lines



Functions



<40 lines



Methods



<30 lines



Large functions should be split.



\---



\# Function Design



Each function should



Do one thing.



Have one responsibility.



Be independently testable.



Prefer



```

calculate\_speed\_score()



calculate\_accuracy\_score()



calculate\_priority\_score()

```



Instead of



```

calculate\_everything()

```



\---



\# Import Rules



Always



Standard Library



↓



Third-party Libraries



↓



Internal Imports



Separate groups with one blank line.



Example



```python

import logging

from typing import Dict



from fastapi import FastAPI



from app.services.scorer import PriorityScorer

```



\---



\# Naming Conventions



Files



snake\_case



Variables



snake\_case



Functions



snake\_case



Constants



UPPER\_CASE



Classes



PascalCase



Private methods



\_prefix



\---



\# Data Flow



```

Incoming Request



↓



Request Model



↓



Recommendation Engine



↓



Classifier



↓



Scorer



↓



Recommender



↓



Explanation Generator



↓



Message Generator



↓



Response Model



↓



JSON Response

```



Every request must follow this exact flow.



\---



\# Testing Strategy



Each service must be independently testable.



Example



test\_classifier.py



ONLY



Classifier



No API calls.



test\_scorer.py



ONLY



Scorer



No API calls.



API tests



ONLY



Endpoint behaviour.



\---



\# Error Handling



Services



Raise custom exceptions.



Routes



Catch exceptions.



Return JSON.



Never expose stack traces.



\---



\# Logging Strategy



Every service logs



Start



Completion



Warning



Failure



Never



print()



Always use logging module.



\---



\# Future Expansion



The architecture must support adding



Historical trends



Machine Learning



LLMs



Difficulty adaptation



Spaced repetition



without restructuring the project.



\---



\# Prohibited Practices



Do NOT



Create circular imports.



Mix API logic with business logic.



Duplicate constants.



Duplicate scoring logic.



Access configuration directly from multiple places.



Modify global variables.



Use wildcard imports.



Create utility functions that contain business logic.



Use long functions.



Use deeply nested if statements.



Hardcode values.



\---



\# End of Document

