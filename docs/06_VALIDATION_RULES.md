\# VALIDATION RULES \& API CONTRACT

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document defines:



\- API request validation

\- Request schema rules

\- Response schema

\- HTTP status codes

\- Validation behavior

\- Error response format

\- API conventions



The objective is to ensure predictable and consistent API behavior.



\---



\# API Overview



Base Endpoint



```

POST /recommend

```



Content Type



```

application/json

```



Character Encoding



```

UTF-8

```



Response Format



```

JSON

```



\---



\# API Principles



The API must be:



\- Stateless

\- RESTful

\- Deterministic

\- Predictable

\- Consistent



Every valid request must return a valid JSON response.



The API must never expose internal implementation details.



\---



\# Request Schema



```json

{

&#x20; "student\_id": "student\_001",

&#x20; "date": "2026-08-02",



&#x20; "topic\_accuracy": {

&#x20;   "Arrays": 90,

&#x20;   "Graphs": 42,

&#x20;   "Dynamic Programming": 35

&#x20; },



&#x20; "coding\_attempts": \[

&#x20;   {

&#x20;     "topic": "Graphs",

&#x20;     "problem": "Graph BFS",

&#x20;     "attempts": 2,

&#x20;     "result": "incorrect"

&#x20;   }

&#x20; ],



&#x20; "mcq\_results": {

&#x20;   "Graphs": {

&#x20;     "correct": 8,

&#x20;     "total": 10

&#x20;   }

&#x20; },



&#x20; "average\_solving\_time": {

&#x20;   "Graphs": "High",

&#x20;   "Arrays": "Low"

&#x20; }

}

```



\---



\# Required Fields



The following fields are mandatory.



| Field | Required |

|--------|----------|

| student\_id | Yes |

| date | Yes |

| topic\_accuracy | Yes |

| coding\_attempts | Yes |

| mcq\_results | Yes |

| average\_solving\_time | Yes |



Requests missing required fields must be rejected.



\---



\# student\_id Rules



Type



```

string

```



Minimum Length



```

1

```



Maximum Length



```

100

```



Must not be empty.



\---



\# date Rules



Format



```

YYYY-MM-DD

```



Example



```

2026-08-02

```



Invalid date formats must fail validation.



\---



\# topic\_accuracy Rules



Type



```

Dictionary

```



Key



Topic Name



Type



```

string

```



Value



Accuracy



Type



```

integer

```



Allowed Range



```

0–100

```



Example



```json

{

&#x20;   "Arrays":90,

&#x20;   "Graphs":45

}

```



\---



\# Topic Name Rules



Must



\- be unique

\- not be empty

\- not contain only whitespace



Maximum length



```

100 characters

```



\---



\# Coding Attempt Schema



Each entry



```json

{

&#x20;   "topic":"Graphs",

&#x20;   "problem":"Graph BFS",

&#x20;   "attempts":2,

&#x20;   "result":"incorrect"

}

```



Required fields



| Field | Type |

|--------|------|

| topic | string |

| problem | string |

| attempts | integer |

| result | string |



\---



\# attempts Rules



Minimum



```

1

```



Maximum



```

100

```



Negative values are invalid.



\---



\# result Rules



Allowed values



```

correct



incorrect

```



Nothing else.



\---



\# MCQ Schema



```json

{

&#x20;   "Graphs":{

&#x20;       "correct":8,

&#x20;       "total":10

&#x20;   }

}

```



Rules



correct



>=0



total



>0



correct



<=total



\---



\# Solving Time Schema



Allowed values



```

Low



Medium



High



Very High

```



Case-sensitive.



Invalid values must fail validation.



\---



\# Empty Collections



Allowed?



| Field | Empty Allowed |

|--------|---------------|

| topic\_accuracy | No |

| coding\_attempts | Yes |

| mcq\_results | Yes |

| average\_solving\_time | No |



\---



\# Duplicate Topics



Duplicate topic names are not allowed.



Validation must fail.



\---



\# Unknown Topics



Unknown topic names



Are allowed.



The recommendation engine should treat them exactly like any other topic.



No predefined topic list is required.



\---



\# Maximum Payload Limits



Maximum Topics



```

100

```



Maximum Coding Attempts



```

500

```



Maximum Request Size



```

1 MB

```



Requests exceeding limits must be rejected.



\---



\# Successful Response



HTTP



```

200 OK

```



Structure



```json

{

&#x20; "success": true,



&#x20; "student\_id": "student\_001",



&#x20; "recommendations": \[



&#x20; ],



&#x20; "tomorrows\_focus\_message": "...",



&#x20; "generated\_at": "2026-08-02T15:30:00Z"

}

```



\---



\# Validation Failure



HTTP



```

422 Unprocessable Entity

```



Structure



```json

{

&#x20;   "success":false,



&#x20;   "error":"Validation failed",



&#x20;   "details":\[



&#x20;   ]

}

```



\---



\# Server Error



HTTP



```

500 Internal Server Error

```



Structure



```json

{

&#x20;   "success":false,



&#x20;   "error":"Unexpected server error"

}

```



Never expose stack traces.



\---



\# Unsupported Method



Example



GET /recommend



Return



```

405 Method Not Allowed

```



\---



\# Unsupported Media Type



If



```

Content-Type



!=



application/json

```



Return



```

415 Unsupported Media Type

```



\---



\# Invalid JSON



Malformed JSON



↓



```

400 Bad Request

```



\---



\# Validation Behavior



Reject



Negative accuracy



Accuracy >100



Empty topic names



Negative attempts



Missing fields



Wrong types



Invalid dates



Invalid solving time



Invalid MCQ values



\---



\# Business Rules



Validation



ONLY checks



Structure



Types



Ranges



Required fields



Business logic



must happen AFTER validation.



Example



Validation



↓



Recommendation Engine



Never mix these two layers.



\---



\# Pydantic Models



Use separate models.



```

RecommendationRequest



CodingAttempt



MCQResult



RecommendationResponse



RecommendationItem



TopicClassification

```



Do not create one giant model.



\---



\# API Versioning



Current



```

v1

```



Future



```

/api/v2/recommend

```



Current implementation



Need not expose version in URL.



Just document it.



\---



\# Time Format



Use



ISO-8601



Example



```

2026-08-02T15:31:40Z

```



\---



\# Numeric Precision



Priority scores



Internal



Float



API



Rounded to



2 decimal places



\---



\# Consistency Rules



Every response



Must contain



```

success

```



Every error



Must contain



```

error

```



Never return plain strings.



Always return JSON.



\---



\# Logging Rules



Log



Incoming requests



Validation failures



Recommendation completion



Unexpected errors



Never log



Entire request payload



Personal information



Internal exceptions



\---



\# Validation Checklist



Before recommendation generation



Verify



✓ JSON valid



✓ Required fields exist



✓ Types correct



✓ Accuracy range valid



✓ Topic names valid



✓ Attempts valid



✓ MCQ values valid



✓ Solving time valid



✓ Payload size acceptable



Only after all checks pass



↓



Run recommendation engine.



\---



\# End of Document

