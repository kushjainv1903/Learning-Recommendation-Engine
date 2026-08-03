\# EDGE CASES \& SYSTEM BEHAVIOR

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document defines how the recommendation engine behaves under unusual,

unexpected, or boundary conditions.



The objective is to guarantee deterministic and predictable behaviour.



Every edge case must produce a valid response.



The application must never crash because of user input.



\---



\# Design Principles



The engine should always



✓ Return valid JSON



✓ Remain deterministic



✓ Never crash



✓ Never generate duplicate recommendations



✓ Never expose internal errors



✓ Produce meaningful output whenever possible



\---



\# Edge Case Categories



The following categories are covered



1\. Empty Data

2\. Invalid Values

3\. Boundary Values

4\. Duplicate Data

5\. Missing Data

6\. Contradictory Data

7\. Large Payloads

8\. Exceptional Performance

9\. Recommendation Conflicts



\---



\# CASE 1



\## Empty topic\_accuracy



Example



```json

{

&#x20;   "topic\_accuracy": {}

}

```



Behavior



Reject request.



Reason



The recommendation engine cannot operate without topic performance.



Response



HTTP



422



\---



\# CASE 2



\## Empty coding\_attempts



Example



```json

{

&#x20;   "coding\_attempts":\[]

}

```



Behavior



Allowed.



Recommendations are generated using



\- Topic Accuracy

\- MCQ Results

\- Solving Time



Coding score defaults to neutral.



\---



\# CASE 3



\## Empty MCQ Results



Behavior



Allowed.



Use



Accuracy



Coding Attempts



Time



Only.



Consistency analysis is skipped.



\---



\# CASE 4



\## Empty Solving Time



Behavior



Reject request.



Reason



Speed analysis is a required signal.



HTTP



422



\---



\# CASE 5



\## One Topic Only



Example



```json

{

&#x20;   "topic\_accuracy":{

&#x20;       "Arrays":45

&#x20;   }

}

```



Behavior



Generate recommendation normally.



No minimum topic count beyond one.



\---



\# CASE 6



\## All Topics Mastered



Example



Arrays



95



Graphs



94



DP



91



Behavior



No weak-topic recommendations.



Return



Positive reinforcement.



Challenge practice.



Advanced questions.



Example



"Excellent work today. Continue solving advanced problems to maintain your level."



\---



\# CASE 7



\## All Topics Critical



Behavior



Prioritize



Top 3 only.



Do NOT recommend every topic.



Reason



Recommendation overload reduces usefulness.



\---



\# CASE 8



\## Accuracy Exactly on Threshold



Threshold



75



Accuracy



75



Behavior



Belongs to



Strong



Thresholds are inclusive.



\---



\# CASE 9



\## Accuracy = 0



Behavior



Critical



Highest recommendation priority.



\---



\# CASE 10



\## Accuracy = 100



Behavior



Mastered



No revision required.



\---



\# CASE 11



\## Negative Accuracy



Behavior



Validation Error



Reject request.



\---



\# CASE 12



\## Accuracy >100



Behavior



Validation Error



Reject request.



\---



\# CASE 13



\## Negative Coding Attempts



Behavior



Validation Error



\---



\# CASE 14



\## Very Large Attempt Count



Example



attempts



500



Behavior



Reject request.



Reason



Unrealistic input.



\---



\# CASE 15



\## Duplicate Topic Names



Behavior



Validation Error



Never merge duplicates automatically.



Reason



Client should send clean data.



\---



\# CASE 16



\## Unknown Topic



Example



Binary Lifting



Behavior



Treat as a valid topic.



No predefined topic catalogue exists.



\---



\# CASE 17



\## Topic Name with Leading Spaces



Example



"   Graphs"



Behavior



Trim whitespace during validation.



\---



\# CASE 18



\## Topic Name with Mixed Case



Example



graphs



Graphs



GRAPHS



Behavior



Normalize



Title Case



before processing.



\---



\# CASE 19



\## High Accuracy



High Failed Attempts



Example



Accuracy



88



Attempts



4



Behavior



Classification



Strong



Recommendation



Implementation Practice



Reason



Repeated failures outweigh good accuracy.



\---



\# CASE 20



\## Low Accuracy



Zero Attempts



Behavior



Recommend



Structured Practice



Reason



Student has not attempted enough coding.



\---



\# CASE 21



\## High MCQ



Low Coding



Behavior



Implementation Gap



Recommendation



Practice Coding



\---



\# CASE 22



\## Low MCQ



High Coding



Behavior



Theory Gap



Recommendation



Concept Revision



\---



\# CASE 23



\## High Accuracy



High Solving Time



Behavior



Speed Practice



Do NOT recommend concept revision.



\---



\# CASE 24



\## Low Accuracy



Low Solving Time



Behavior



Conceptual misunderstanding.



Prioritize revision.



\---



\# CASE 25



\## Identical Priority Scores



Behavior



Sort by



Classification



↓



Failed Attempts



↓



Accuracy



↓



Alphabetical



Always deterministic.



\---



\# CASE 26



\## More Than Five Weak Topics



Behavior



Return only



Top Five.



Never overwhelm students.



\---



\# CASE 27



\## More Than 100 Topics



Behavior



Reject request.



Payload exceeds supported limit.



\---



\# CASE 28



\## Payload Larger Than 1 MB



Behavior



Reject request.



HTTP



413



Payload Too Large



\---



\# CASE 29



\## Unsupported Solving Time



Example



"Fast"



Behavior



Validation Error



\---



\# CASE 30



\## Missing student\_id



Behavior



Validation Error



Required field.



\---



\# CASE 31



\## Missing Date



Behavior



Validation Error



\---



\# CASE 32



\## Future Date



Behavior



Allowed.



Recommendation engine is date-independent.



\---



\# CASE 33



\## Old Historical Date



Behavior



Allowed.



The service is stateless.



\---



\# CASE 34



\## Empty String Topic Name



Behavior



Validation Error



\---



\# CASE 35



\## Null Topic Name



Behavior



Validation Error



\---



\# CASE 36



\## Recommendation Tie



Behavior



Always use deterministic ordering.



Never randomize.



\---



\# CASE 37



\## No Recommendations Generated



Possible



All topics mastered.



Behavior



Generate



Maintenance recommendation.



Positive reinforcement.



\---



\# CASE 38



\## Unexpected Exception



Behavior



Return



HTTP



500



JSON



```json

{

&#x20;   "success":false,

&#x20;   "error":"Unexpected server error."

}

```



Log internally.



Never expose traceback.



\---



\# CASE 39



\## Floating Point Accuracy



Example



89.6



Behavior



Accept.



Round internally if required.



Maintain precision.



\---



\# CASE 40



\## Empty Request Body



Behavior



HTTP



400



Bad Request



\---



\# Positive Reinforcement Rules



Every response must contain



At least one encouraging observation.



Examples



"You are performing consistently in Arrays."



"Excellent progress in Graphs."



"Your coding accuracy has remained strong."



Never produce purely negative feedback.



\---



\# Recommendation Limits



Maximum



5



Default



3



Minimum



1



Always return at least one recommendation.



\---



\# Recommendation Conflicts



If multiple recommendation types apply



Priority Order



1\.



Revise Fundamentals



2\.



Implementation Practice



3\.



Theory Revision



4\.



Structured Practice



5\.



Speed Practice



6\.



Maintain Strength



Only one recommendation per topic.



\---



\# Deterministic Rules



The same input



must



always produce



\- identical recommendations

\- identical priorities

\- identical explanations

\- identical message



No randomness.



No timestamps inside recommendations.



No probabilistic logic.



\---



\# Error Recovery



Whenever possible



Reject only the invalid request.



Do not silently modify user data.



Do not guess missing values.



Do not fabricate recommendations.



\---



\# Future Compatibility



Additional edge cases may be added for



\- Historical learning

\- Personalized schedules

\- Adaptive difficulty

\- Multi-day analysis

\- AI-generated explanations



The existing behavior must remain backward compatible.



\---



\# End of Document

