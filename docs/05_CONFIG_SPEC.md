\# CONFIGURATION SPECIFICATION

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document defines every configurable parameter used throughout the recommendation engine.



The objective is to eliminate hardcoded values ("magic numbers") from the codebase.



All configurable values must exist exactly once.



Business logic must NEVER hardcode:



\- Thresholds

\- Weights

\- Recommendation limits

\- Classification ranges

\- Message templates

\- Time thresholds



Every value defined here should be loaded from `app/config.py`.



\---



\# Configuration Philosophy



The recommendation engine must be completely configurable.



Changing recommendation behaviour should require updating configuration values only.



Business logic should remain unchanged.



\---



\# Accuracy Thresholds



These values determine topic classification.



```python

MASTERED\_THRESHOLD = 90



STRONG\_THRESHOLD = 75



MODERATE\_THRESHOLD = 50



WEAK\_THRESHOLD = 30



MIN\_ACCURACY = 0



MAX\_ACCURACY = 100

```



Meaning



| Accuracy | Classification |

|-----------|----------------|

| 90–100 | Mastered |

| 75–89 | Strong |

| 50–74 | Moderate |

| 30–49 | Weak |

| 0–29 | Critical |



Never hardcode these values.



\---



\# Failed Attempt Thresholds



```python

NO\_FAILURES = 0



GOOD\_FAILURE\_LIMIT = 1



PRACTICE\_FAILURE\_LIMIT = 2



CRITICAL\_FAILURE\_LIMIT = 3

```



Interpretation



| Failed Attempts | Meaning |

|-----------------|----------|

| 0 | Excellent |

| 1 | Good |

| 2 | Needs Practice |

| 3+ | Critical |



\---



\# Solving Time Levels



The API receives



Low



Medium



High



Very High



Internally these map to scores.



```python

TIME\_SCORE = {



&#x20;   "Low": 10,



&#x20;   "Medium": 30,



&#x20;   "High": 70,



&#x20;   "Very High": 100



}

```



Future versions may replace this with actual minutes.



\---



\# Learning Priority Weights



Priority Score is a weighted combination of multiple indicators.



Default



```python

ACCURACY\_WEIGHT = 0.45



FAILED\_ATTEMPT\_WEIGHT = 0.25



SOLVING\_TIME\_WEIGHT = 0.20



CONSISTENCY\_WEIGHT = 0.10

```



Requirements



Weights



Must sum to



1.0



Validation should verify this during application startup.



\---



\# Recommendation Limits



```python

DEFAULT\_RECOMMENDATIONS = 3



MIN\_RECOMMENDATIONS = 1



MAX\_RECOMMENDATIONS = 5

```



Rules



Never recommend



More than five topics.



Never return zero recommendations.



\---



\# Practice Plan Configuration



Mastered



```python

MASTERED\_PRACTICE = {



&#x20;   "easy": 0,



&#x20;   "medium": 1,



&#x20;   "hard": 1



}

```



Strong



```python

STRONG\_PRACTICE = {



&#x20;   "easy": 0,



&#x20;   "medium": 2,



&#x20;   "hard": 1



}

```



Moderate



```python

MODERATE\_PRACTICE = {



&#x20;   "easy": 2,



&#x20;   "medium": 3,



&#x20;   "hard": 0



}

```



Weak



```python

WEAK\_PRACTICE = {



&#x20;   "easy": 3,



&#x20;   "medium": 3,



&#x20;   "hard": 1



}

```



Critical



```python

CRITICAL\_PRACTICE = {



&#x20;   "easy": 5,



&#x20;   "medium": 3,



&#x20;   "hard": 1



}

```



These values may change later without changing recommendation logic.



\---



\# Classification Labels



Always use these exact values.



```python

MASTERED = "Mastered"



STRONG = "Strong"



MODERATE = "Moderate"



WEAK = "Weak"



CRITICAL = "Critical"

```



Never generate alternative spellings.



\---



\# Recommendation Types



```python

REVISE\_FUNDAMENTALS



STRUCTURED\_PRACTICE



IMPLEMENTATION\_PRACTICE



THEORY\_REVISION



SPEED\_PRACTICE



REINFORCEMENT\_PRACTICE



MAINTAIN\_STRENGTH

```



These should be implemented as Enum values.



\---



\# Priority Levels



```python

CRITICAL\_PRIORITY = 5



HIGH\_PRIORITY = 4



MEDIUM\_PRIORITY = 3



LOW\_PRIORITY = 2



MINIMAL\_PRIORITY = 1

```



These values are internal.



The API should expose human-readable priorities if required.



\---



\# Positive Reinforcement Rules



Every response must include



Minimum



One positive observation.



Configuration



```python

ENABLE\_POSITIVE\_REINFORCEMENT = True

```



\---



\# Explanation Configuration



Maximum explanation length



```python

MAX\_EXPLANATION\_LENGTH = 180

```



Target



One sentence.



Never exceed two sentences.



\---



\# Tomorrow's Focus Configuration



Maximum Topics



```python

MAX\_FOCUS\_TOPICS = 3

```



Message Length



```python

MAX\_MESSAGE\_LENGTH = 600

```



Closing sentence



Selected from



```python

MOTIVATIONAL\_MESSAGES = \[



&#x20;   "Keep building consistency.",



&#x20;   "Small improvements every day lead to big results.",



&#x20;   "Stay focused and trust the process.",



&#x20;   "Consistency beats intensity.",



&#x20;   "You're improving one topic at a time."



]

```



Messages should rotate deterministically.



Never choose randomly.



Example



Use



```

day\_of\_month % len(messages)

```



instead of random.



\---



\# API Configuration



```python

API\_TITLE = "Learning Recommendation API"



API\_VERSION = "1.0.0"



API\_DESCRIPTION = "AI-powered personalized learning recommendation engine."

```



\---



\# Logging Configuration



```python

LOG\_LEVEL = "INFO"



LOG\_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

```



Production



INFO



Development



DEBUG



\---



\# Validation Limits



Maximum topics



```python

MAX\_TOPICS = 100

```



Minimum topics



```python

MIN\_TOPICS = 1

```



Maximum coding attempts



```python

MAX\_CODING\_ATTEMPTS = 500

```



Maximum MCQ entries



```python

MAX\_MCQ\_TOPICS = 100

```



These limits prevent unreasonable payload sizes.



\---



\# Response Configuration



```python

SUCCESS\_MESSAGE = "Recommendations generated successfully."



VALIDATION\_ERROR = "Validation failed."



UNKNOWN\_ERROR = "Unexpected server error."

```



Never expose raw exception messages.



\---



\# Sorting Configuration



Primary



Priority Score



Secondary



Classification



Third



Failed Attempts



Fourth



Accuracy



Fifth



Alphabetical



Store this order as



```python

SORT\_ORDER = \[



&#x20;   "priority",



&#x20;   "classification",



&#x20;   "failed\_attempts",



&#x20;   "accuracy",



&#x20;   "topic"



]

```



\---



\# Feature Toggles



Future-proofing.



```python

ENABLE\_SPEED\_ANALYSIS = True



ENABLE\_CONSISTENCY\_ANALYSIS = True



ENABLE\_MCQ\_ANALYSIS = True



ENABLE\_CODING\_ANALYSIS = True



ENABLE\_HISTORY\_ANALYSIS = False



ENABLE\_SPACED\_REPETITION = False



ENABLE\_MACHINE\_LEARNING = False



ENABLE\_LLM\_EXPLANATIONS = False

```



Future versions can enable these without changing architecture.



\---



\# Environment Configuration



The current project requires no environment variables.



Future versions may include



```python

API\_HOST



API\_PORT



LOG\_LEVEL



DATABASE\_URL



OPENAI\_API\_KEY

```



None of these are required for Version 1.



\---



\# Configuration Validation



At application startup



Validate



✓ Accuracy thresholds are ordered correctly



✓ Weights sum to 1.0



✓ Recommendation limits are valid



✓ Message templates are not empty



✓ Labels are unique



If validation fails



Application startup should fail with a clear configuration error.



\---



\# Configuration Principles



Always



Centralize configuration.



Document every value.



Use constants.



Validate configuration.



Never



Hardcode thresholds.



Duplicate values.



Scatter constants across files.



Modify configuration inside business logic.



\---



\# End of Document

