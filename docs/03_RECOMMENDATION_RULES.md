\# RECOMMENDATION RULES

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document defines the complete decision-making logic for the recommendation engine.



It specifies:



\- Topic classification

\- Priority scoring

\- Recommendation generation

\- Explanation generation

\- Recommendation ranking

\- Message generation



This document is the source of truth for all recommendation-related logic.



No recommendation should be generated outside these rules.



\---



\# Design Philosophy



The recommendation engine must behave like an experienced mentor.



It should not simply react to low scores.



Instead, it should identify WHY a student is struggling and recommend the most appropriate next action.



Every recommendation must be:



\- Explainable

\- Deterministic

\- Actionable

\- Prioritized



\---



\# Performance Signals



The engine evaluates multiple signals together.



No recommendation should rely on a single metric.



Signals include:



\- Topic Accuracy

\- Coding Attempts

\- Failed Coding Attempts

\- MCQ Performance

\- Average Solving Time



Each signal contributes differently.



\---



\# Learning Indicators



The recommendation engine derives five internal indicators.



These indicators are NOT exposed through the API.



\---



\## 1. Concept Mastery Score



Represents conceptual understanding.



Primary input:



\- Topic Accuracy



Classification



90–100



Excellent



75–89



Strong



50–74



Moderate



30–49



Weak



0–29



Critical



\---



\## 2. Implementation Score



Measures coding ability.



Derived from



\- Failed submissions

\- Coding attempts



Classification



0 failed attempts



Excellent



1 failed attempt



Good



2 failed attempts



Needs Practice



3 or more



Poor



\---



\## 3. Speed Score



Determines solving efficiency.



Input:



Average Solving Time



Classification



Low



Excellent



Medium



Acceptable



High



Needs Speed Improvement



Very High



Critical



\---



\## 4. Consistency Score



Measures agreement between MCQ understanding and Coding ability.



Examples



High MCQ

High Coding



↓



Consistent



\----------------



High MCQ

Low Coding



↓



Implementation Gap



\----------------



Low MCQ

High Coding



↓



Theory Gap



\----------------



Low MCQ

Low Coding



↓



Fundamental Gap



\---



\## 5. Learning Priority Score



Final score used for ranking.



Higher score means higher recommendation priority.



Formula



Priority Score



=



Accuracy Component



\+



Attempt Component



\+



Speed Component



\+



Consistency Component



Configuration values must come from config.py.



Never hardcode weights.



\---



\# Topic Classification



Each topic belongs to exactly one category.



\---



\## Mastered



Conditions



Accuracy ≥ 90



Failed Attempts = 0



Recommendation



No recommendation required.



\---



\## Strong



Conditions



Accuracy



75–89



Failed Attempts ≤1



Recommendation



Optional revision.



\---



\## Moderate



Conditions



Accuracy



50–74



Recommendation



Practice recommended.



\---



\## Weak



Conditions



Accuracy



30–49



Recommendation



Revision required.



\---



\## Critical



Conditions



Accuracy <30



OR



Repeated failures ≥3



Recommendation



Highest priority.



\---



\# Recommendation Categories



The engine selects exactly one recommendation type.



\---



\## Revise Fundamentals



Conditions



Weak accuracy



\+



Repeated failures



Example



Sliding Window



Accuracy



35%



Attempts



3 incorrect



Recommendation



Revise Sliding Window fundamentals.



\---



\## Structured Practice



Conditions



Low accuracy



Few coding attempts



Recommendation



Solve Easy and Medium problems.



\---



\## Speed Practice



Conditions



High accuracy



High solving time



Recommendation



Timed practice.



\---



\## Implementation Practice



Conditions



High MCQ



Low Coding



Recommendation



Practice implementation.



Example



Graph BFS



Theory understood



Coding weak



\---



\## Theory Revision



Conditions



Low MCQ



Good Coding



Recommendation



Review concepts.



\---



\## Reinforcement Practice



Conditions



Moderate performance



Recommendation



Solve additional practice questions.



\---



\## Maintain Strength



Conditions



Mastered topics



Recommendation



Light revision only.



\---



\# Recommendation Templates



Each recommendation follows a standard format.



Template



Action



Reason



Suggested Practice



Priority



Example



Action



Revise Sliding Window Fundamentals



Reason



Repeated failed submissions indicate conceptual misunderstanding.



Suggested Practice



Read notes



↓



Solve 5 Easy



↓



Solve 3 Medium



Priority



High



\---



\# Practice Recommendation Matrix



Critical



↓



Revise Concepts



↓



5 Easy



↓



3 Medium



↓



1 Hard



\--------------



Weak



↓



Revision



↓



3 Easy



↓



3 Medium



\--------------



Moderate



↓



Practice



↓



2 Easy



↓



3 Medium



\--------------



Strong



↓



Timed Practice



↓



2 Medium



\--------------



Mastered



↓



Revision Only



↓



1 Challenge Question



\---



\# Explanation Templates



The explanation generator must always reference actual performance.



Never use generic explanations.



\---



Template 1



Low Accuracy



"{topic} accuracy is only {accuracy}% indicating weak conceptual understanding."



\---



Template 2



Repeated Failures



"You made {attempts} incorrect coding submissions, suggesting repeated implementation difficulties."



\---



Template 3



High Solving Time



"Problems are being solved correctly but significantly slower than expected."



\---



Template 4



Implementation Gap



"Your MCQ performance is strong while coding performance is weak, indicating difficulty translating concepts into code."



\---



Template 5



Theory Gap



"Implementation is acceptable, but theory-based questions reveal conceptual gaps."



\---



Template 6



Strong Performance



"You consistently perform well in this topic. Continue periodic revision to maintain proficiency."



\---



\# Recommendation Ranking



Recommendations are sorted by



1\.



Highest Priority Score



↓



2\.



Classification Severity



Critical



↓



Weak



↓



Moderate



↓



Strong



↓



Mastered



↓



3\.



Highest Failed Attempts



↓



4\.



Lowest Accuracy



↓



5\.



Alphabetical Topic Name



Sorting must always be deterministic.



\---



\# Duplicate Recommendations



Never generate multiple recommendations for the same topic.



Merge signals.



Generate one recommendation.



\---



\# Maximum Recommendations



Default



3



Maximum



5



Minimum



1



If all topics are strong,



return



1 positive recommendation.



\---



\# Positive Reinforcement



The engine must identify strengths.



Never produce only negative feedback.



Include at least one positive observation.



Example



"Arrays is one of your strongest topics. Maintain this consistency."



\---



\# Tomorrow's Focus Message



Structure



Greeting



↓



Positive Observation



↓



Top Three Priorities



↓



Motivational Closing



Example



Tomorrow's Focus



Great work on Arrays today.



Your strongest improvement opportunity is Sliding Window.



Revise Sliding Window fundamentals.



Practice Graph Traversal implementation.



Solve three Medium Dynamic Programming problems.



Keep building consistency and tomorrow's session will be even stronger.



\---



\# Recommendation Limits



Do NOT recommend



More than five topics.



Topics already mastered.



Duplicate practice.



Impossible workloads.



Recommendations exceeding one study session.



\---



\# Future Compatibility



The recommendation engine should be replaceable.



Future versions may include



Machine Learning



LLMs



Historical learning trends



Spaced repetition



Difficulty adaptation



The API contract must remain unchanged.



\---



\# Recommendation Principles



Always



Explain why.



Prioritize intelligently.



Recommend achievable actions.



Reward strengths.



Be encouraging.



Stay deterministic.



Never



Recommend randomly.



Recommend impossible workloads.



Ignore failed submissions.



Ignore solving time.



Ignore MCQ performance.



Generate duplicate recommendations.



Return unexplained recommendations.



\---



\# End of Document

