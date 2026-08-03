\# CODING STANDARDS

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document defines the coding standards, software engineering principles,

and best practices that must be followed throughout the project.



The goal is to produce a codebase that is:



\- Readable

\- Maintainable

\- Testable

\- Modular

\- Extensible

\- Production-ready



\---



\# General Principles



Every line of code should prioritize



\- Clarity

\- Simplicity

\- Maintainability



Never write clever code when simple code is sufficient.



Readable code is preferred over shorter code.



\---



\# Python Version



Required



```

Python 3.11+

```



Do not use deprecated language features.



\---



\# Style Guide



Follow



PEP 8



throughout the project.



Use



Black



for automatic formatting.



Recommended line length



```

88 characters

```



\---



\# Type Hints



All public functions must include type hints.



Good



```python

def calculate\_priority(

&#x20;   accuracy: float,

&#x20;   failed\_attempts: int

) -> float:

```



Bad



```python

def calculate\_priority(a, b):

```



\---



\# Docstrings



Every public module



Every public class



Every public function



must include docstrings.



Use Google style.



Example



```python

def classify\_topic(topic: str, accuracy: float) -> str:

&#x20;   """

&#x20;   Classify a topic based on student performance.



&#x20;   Args:

&#x20;       topic:

&#x20;           Topic name.



&#x20;       accuracy:

&#x20;           Topic accuracy percentage.



&#x20;   Returns:

&#x20;       Classification label.

&#x20;   """

```



\---



\# Naming Conventions



Variables



```

snake\_case

```



Functions



```

snake\_case

```



Classes



```

PascalCase

```



Constants



```

UPPER\_CASE

```



Private helpers



```

\_prefix

```



\---



\# Function Design



Each function should



\- Perform one task

\- Have one responsibility

\- Be independently testable



Recommended



```

<40 lines

```



Avoid



Large multi-purpose functions.



\---



\# Class Design



Classes should encapsulate



One responsibility.



Avoid



God classes.



If a class exceeds



```

300 lines

```



consider splitting it.



\---



\# SOLID Principles



Apply



Single Responsibility Principle



Open/Closed Principle



Liskov Substitution Principle



Interface Segregation Principle



Dependency Inversion Principle



Only where appropriate.



Avoid unnecessary abstraction.



\---



\# DRY Principle



Don't Repeat Yourself.



Never duplicate



\- validation

\- scoring

\- constants

\- recommendation logic



Shared logic belongs in reusable functions.



\---



\# KISS Principle



Keep It Simple, Stupid.



Prefer



```python

if accuracy < threshold:

```



over unnecessarily complex abstractions.



\---



\# YAGNI Principle



You Aren't Gonna Need It.



Do not implement features that are outside the project scope.



Examples



Do NOT build



\- Authentication

\- Database

\- Machine Learning

\- User accounts

\- Analytics dashboard



unless explicitly required.



\---



\# Imports



Import order



1\.



Standard Library



2\.



Third-party Libraries



3\.



Internal Imports



Example



```python

import logging

from typing import List



from fastapi import FastAPI



from app.services.scorer import PriorityScorer

```



Never use



```python

from module import \*

```



\---



\# Constants



Never hardcode



```

75



90



0.45



5

```



All constants belong in



```

config.py

```



\---



\# Logging



Use



Python logging



Never



print()



Example



```python

logger.info("Generating recommendations")

```



Log



✓ API start



✓ API completion



✓ Validation failures



✓ Errors



Do not log



\- Entire payload

\- Sensitive information



\---



\# Exception Handling



Raise



Specific exceptions.



Good



```python

raise ValidationException(...)

```



Bad



```python

raise Exception(...)

```



Never suppress exceptions silently.



\---



\# Business Logic



Business logic belongs ONLY inside



```

services/

```



Never inside



```

routes.py



main.py



models.py

```



\---



\# API Layer



Routes should



\- Receive request

\- Validate request

\- Call service

\- Return response



Nothing else.



\---



\# Configuration



Every configurable value



must come from



```

config.py

```



Never



```python

if accuracy >= 75:

```



Instead



```python

if accuracy >= STRONG\_THRESHOLD:

```



\---



\# Comments



Write comments only when



WHY



needs explanation.



Do NOT comment obvious code.



Bad



```python

\# increment counter



counter += 1

```



Good



```python

\# Apply heavier penalty because repeated failures

\# indicate conceptual misunderstanding.

```



\---



\# Error Messages



Error messages should be



Clear



Actionable



Professional



Never expose



Stack traces



File paths



Internal implementation



\---



\# Validation



Validate



Early.



Fail Fast.



Never continue processing invalid data.



\---



\# Return Values



Functions should return



Predictable types.



Avoid



Mixed return types.



Bad



```python

return "error"

```



sometimes



```python

return {}

```



Good



Always return



Recommendation



or



Raise Exception



\---



\# Mutable Defaults



Never use



```python

def func(items=\[]):

```



Use



```python

def func(items=None):

```



\---



\# File Responsibilities



Each file



One purpose.



Avoid



Mixing



Validation



Scoring



Recommendation



Formatting



in one file.



\---



\# Performance



Avoid unnecessary loops.



Prefer



O(n)



where possible.



Do not prematurely optimize.



Correctness first.



\---



\# Testing



Every service



must have



unit tests.



Every endpoint



must have



integration tests.



Tests should be



Independent



Repeatable



Deterministic



\---



\# Deterministic Behaviour



The same input



must always produce



the same output.



Never use



```

random



uuid



datetime.now()

```



inside recommendation logic.



\---



\# Dependency Rules



Allowed



```

API



↓



Services



↓



Utilities



↓



Core

```



Never reverse dependencies.



\---



\# Circular Imports



Never create circular imports.



Refactor shared logic instead.



\---



\# JSON Responses



Every API response



must be valid JSON.



Never return



Plain text



HTML



XML



\---



\# Formatting



Before committing



Run



```

black .

```



Then



```

isort .

```



Then



```

pytest

```



Only commit



passing code.



\---



\# Git Commit Messages



Use



```

feat:



fix:



refactor:



docs:



test:



style:

```



Examples



```

feat: implement recommendation scoring



fix: validate duplicate topics



test: add scorer unit tests



docs: update README

```



\---



\# Code Review Checklist



Before marking any task complete



Verify



✓ Type hints



✓ Docstrings



✓ No hardcoded constants



✓ No duplicate logic



✓ PEP8



✓ Logging added



✓ Exceptions handled



✓ Unit tests written



✓ Integration tests pass



✓ No unused imports



✓ Black formatting



✓ Meaningful variable names



✓ Business logic separated



✓ Configuration centralized



\---



\# Anti-Patterns



Never



Use global mutable state.



Use wildcard imports.



Use nested functions unnecessarily.



Create extremely long functions.



Mix API and business logic.



Hardcode thresholds.



Ignore validation.



Duplicate recommendation logic.



Catch every exception with



```

except:

```



Use print()



Return inconsistent types.



\---



\# Definition of Good Code



Good code is



Easy to read.



Easy to modify.



Easy to test.



Easy to debug.



Easy to extend.



If another engineer can understand a module in less than five minutes,

the module is considered well designed.



\---



\# End of Document

