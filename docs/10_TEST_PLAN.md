\# TEST PLAN

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document defines the complete testing strategy for the Learning Recommendation Engine.



The goal is to ensure:



\- Correctness

\- Reliability

\- Deterministic behavior

\- Maintainability



Every business rule defined in the Recommendation Rules document must be validated by automated tests.



\---



\# Testing Philosophy



Testing follows four levels.



```

Unit Tests



↓



Integration Tests



↓



Validation Tests



↓



Golden Test Cases

```



Each level verifies a different aspect of the system.



\---



\# Test Framework



Use



\- pytest

\- FastAPI TestClient



Optional



\- pytest-cov



\---



\# Folder Structure



```

tests/



├── test\_feature\_extractor.py

├── test\_classifier.py

├── test\_scorer.py

├── test\_recommender.py

├── test\_explanation\_generator.py

├── test\_message\_generator.py

├── test\_api.py

├── test\_validation.py

│

└── fixtures/

&#x20;   ├── valid\_payload.json

&#x20;   ├── invalid\_payload.json

&#x20;   ├── perfect\_student.json

&#x20;   ├── weak\_student.json

&#x20;   └── expected\_outputs.json

```



\---



\# Coverage Goals



Business Logic



100%



API Layer



90%



Utilities



80%



Overall Project



85–90%



Coverage should never replace meaningful tests.



\---



\# UNIT TESTS



Every service must be tested independently.



No API calls.



No external dependencies.



\---



\## Feature Extraction Tests



Verify



✓ Accuracy feature



✓ Failed attempt feature



✓ MCQ accuracy



✓ Coding success rate



✓ Speed score



✓ Consistency score



\---



\## Classifier Tests



Test every classification boundary.



| Accuracy | Expected |

|-----------|----------|

|100|Mastered|

|90|Mastered|

|89|Strong|

|75|Strong|

|74|Moderate|

|50|Moderate|

|49|Weak|

|30|Weak|

|29|Critical|

|0|Critical|



\---



\## Scorer Tests



Verify



Priority score increases when



\- accuracy decreases

\- failed attempts increase

\- solving time increases

\- consistency worsens



Ensure



Higher score



↓



Higher priority



\---



\## Recommendation Tests



Verify



Weak



↓



Revision



Critical



↓



Highest Priority



Strong



↓



Maintain Strength



Implementation Gap



↓



Implementation Practice



Theory Gap



↓



Theory Revision



Speed Issue



↓



Speed Practice



\---



\## Explanation Generator Tests



Verify



Generated explanations



\- include topic

\- include reason

\- reference actual metrics

\- remain under configured length



\---



\## Message Generator Tests



Verify



Generated message



contains



✓ greeting



✓ positive observation



✓ top priorities



✓ motivational closing



\---



\# INTEGRATION TESTS



Test complete workflow.



Request



↓



Validation



↓



Feature Extraction



↓



Classification



↓



Scoring



↓



Recommendation



↓



Message



↓



Response



Verify



Entire pipeline works correctly.



\---



\## API Tests



Endpoint



```

POST /recommend

```



Verify



HTTP 200



Correct JSON



Correct schema



Deterministic output



\---



\# VALIDATION TESTS



Invalid inputs must fail.



\---



\## Missing Required Field



Expected



422



\---



\## Accuracy >100



Expected



422



\---



\## Accuracy <0



Expected



422



\---



\## Invalid Solving Time



Expected



422



\---



\## Wrong Data Type



Expected



422



\---



\## Empty Topic Name



Expected



422



\---



\## Negative Attempts



Expected



422



\---



\## Invalid Date



Expected



422



\---



\## Invalid JSON



Expected



400



\---



\## Unsupported Method



Expected



405



\---



\## Unsupported Content Type



Expected



415



\---



\# GOLDEN TEST CASES



Golden tests ensure deterministic behaviour.



Input



↓



Expected Output



must never change unless business rules change.



\---



\## Golden Case 1



Assignment Example



Arrays



90



Sliding Window



35



Graphs



40



DP



30



Expected



Sliding Window



Priority 1



Graphs



Priority 2



DP



Priority 3



\---



\## Golden Case 2



Perfect Student



Expected



Positive reinforcement only.



\---



\## Golden Case 3



Critical Student



All topics weak.



Expected



Top three recommendations only.



\---



\## Golden Case 4



Implementation Gap



High MCQ



Poor Coding



Expected



Implementation Practice



\---



\## Golden Case 5



Theory Gap



Poor MCQ



Good Coding



Expected



Theory Revision



\---



\## Golden Case 6



High Accuracy



High Time



Expected



Speed Practice



\---



\# EDGE CASE TESTS



Test



Empty coding attempts



Empty MCQ



One topic only



Unknown topic



Large payload



Duplicate topics



Floating-point accuracy



Boundary thresholds



Recommendation ties



\---



\# RESPONSE TESTS



Verify



Every successful response contains



✓ success



✓ recommendations



✓ message



✓ generated\_at



Every failure response contains



✓ success



✓ error



\---



\# PERFORMANCE TESTS



Typical payload



Target



<300 ms



Large payload



<1 second



Memory



No significant increase after repeated requests.



\---



\# DETERMINISM TEST



Run the same request



100 times.



Every response



must be identical.



No randomness allowed.



\---



\# LOGGING TESTS



Verify



Validation failure logged



Recommendation generation logged



Unhandled exception logged



Never log



Sensitive information



Entire payload



\---



\# CONFIGURATION TESTS



Verify



Weights sum to 1.0



Thresholds ordered correctly



Recommendation limits valid



Feature flags load correctly



Startup should fail if configuration is invalid.



\---



\# TEST DATA



Maintain reusable fixtures.



Do not duplicate payloads across tests.



Every fixture should have



Expected output



Documented purpose



\---



\# CONTINUOUS TESTING



Run before every commit



```

black .



isort .



pytest



pytest --cov

```



No commit should be made with failing tests.



\---



\# SUCCESS CRITERIA



The project is considered correctly tested when



✓ Every service has unit tests



✓ API integration tests pass



✓ Validation tests pass



✓ Golden tests pass



✓ Edge case tests pass



✓ Deterministic tests pass



✓ Configuration tests pass



✓ Coverage target achieved



\---



\# End of Document

