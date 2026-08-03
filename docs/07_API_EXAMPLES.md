\# API EXAMPLES

\## AI-Powered Personalized Learning Recommendation Engine



Version: 1.0



\---



\# Purpose



This document defines the official API examples for the Recommendation Engine.



It serves as:



\- API documentation

\- Integration reference

\- Testing reference

\- Frontend development guide

\- MERN integration guide



All examples in this document are considered valid API contracts.



\---



\# Endpoint



```

POST /recommend

```



Content Type



```

application/json

```



\---



\# Complete Request Example



```json

{

&#x20; "student\_id": "student\_001",

&#x20; "date": "2026-08-02",



&#x20; "topic\_accuracy": {

&#x20;   "Arrays": 92,

&#x20;   "Sliding Window": 35,

&#x20;   "Graphs": 42,

&#x20;   "Dynamic Programming": 28

&#x20; },



&#x20; "coding\_attempts": \[

&#x20;   {

&#x20;     "topic": "Sliding Window",

&#x20;     "problem": "Longest Substring",

&#x20;     "attempts": 3,

&#x20;     "result": "incorrect"

&#x20;   },

&#x20;   {

&#x20;     "topic": "Graphs",

&#x20;     "problem": "Graph BFS",

&#x20;     "attempts": 2,

&#x20;     "result": "incorrect"

&#x20;   }

&#x20; ],



&#x20; "mcq\_results": {

&#x20;   "Arrays": {

&#x20;     "correct": 9,

&#x20;     "total": 10

&#x20;   },

&#x20;   "Graphs": {

&#x20;     "correct": 8,

&#x20;     "total": 10

&#x20;   }

&#x20; },



&#x20; "average\_solving\_time": {

&#x20;   "Arrays": "Low",

&#x20;   "Sliding Window": "High",

&#x20;   "Graphs": "High",

&#x20;   "Dynamic Programming": "Medium"

&#x20; }

}

```



\---



\# Successful Response



```json

{

&#x20; "success": true,



&#x20; "student\_id": "student\_001",



&#x20; "generated\_at": "2026-08-02T14:30:00Z",



&#x20; "feature\_summary": {



&#x20;   "overall\_accuracy": 49.25,



&#x20;   "overall\_failed\_attempts": 5,



&#x20;   "average\_speed": "High"



&#x20; },



&#x20; "topic\_classification": {



&#x20;   "Arrays": "Mastered",



&#x20;   "Sliding Window": "Weak",



&#x20;   "Graphs": "Weak",



&#x20;   "Dynamic Programming": "Critical"



&#x20; },



&#x20; "recommendations": \[



&#x20;   {



&#x20;     "topic": "Sliding Window",



&#x20;     "priority": 1,



&#x20;     "priority\_score": 91.75,



&#x20;     "recommendation\_type": "Revise Fundamentals",



&#x20;     "action": "Revise Sliding Window fundamentals",



&#x20;     "reason": "35% accuracy with repeated failed submissions indicates conceptual misunderstanding.",



&#x20;     "practice\_plan": {



&#x20;       "easy": 5,



&#x20;       "medium": 3,



&#x20;       "hard": 1



&#x20;     }



&#x20;   },



&#x20;   {



&#x20;     "topic": "Graphs",



&#x20;     "priority": 2,



&#x20;     "priority\_score": 82.10,



&#x20;     "recommendation\_type": "Implementation Practice",



&#x20;     "action": "Practice Graph BFS implementation",



&#x20;     "reason": "Theory understanding is good, but coding attempts indicate implementation difficulty.",



&#x20;     "practice\_plan": {



&#x20;       "easy": 3,



&#x20;       "medium": 3,



&#x20;       "hard": 1



&#x20;     }



&#x20;   }



&#x20; ],



&#x20; "strengths": \[



&#x20;   "Arrays"



&#x20; ],



&#x20; "tomorrows\_focus\_message": "Great work on Arrays today. Focus on Sliding Window fundamentals, Graph implementation, and Dynamic Programming practice to strengthen your weak areas."

}

```



\---



\# Example 2



Perfect Student



Request



```json

{

&#x20; "student\_id":"student\_002",



&#x20; "date":"2026-08-02",



&#x20; "topic\_accuracy":{



&#x20;   "Arrays":95,



&#x20;   "Graphs":90,



&#x20;   "DP":91



&#x20; },



&#x20; "coding\_attempts":\[],



&#x20; "mcq\_results":{},



&#x20; "average\_solving\_time":{



&#x20;   "Arrays":"Low",



&#x20;   "Graphs":"Low",



&#x20;   "DP":"Low"



&#x20; }

}

```



Response



```json

{

&#x20; "success":true,



&#x20; "recommendations":\[



&#x20;   {



&#x20;     "recommendation\_type":"Maintain Strength",



&#x20;     "action":"Attempt one challenging problem from your strongest topic."



&#x20;   }



&#x20; ],



&#x20; "strengths":\[



&#x20;   "Arrays",



&#x20;   "Graphs",



&#x20;   "DP"



&#x20; ]

}

```



\---



\# Example 3



Validation Error



Request



```json

{

&#x20;   "student\_id":"",



&#x20;   "topic\_accuracy":{



&#x20;       "Graphs":140



&#x20;   }

}

```



Response



HTTP



422



```json

{

&#x20;   "success":false,



&#x20;   "error":"Validation failed",



&#x20;   "details":\[



&#x20;       {



&#x20;           "field":"student\_id",



&#x20;           "message":"Must not be empty"



&#x20;       },



&#x20;       {



&#x20;           "field":"topic\_accuracy.Graphs",



&#x20;           "message":"Accuracy must be between 0 and 100"



&#x20;       }



&#x20;   ]

}

```



\---



\# Example 4



Malformed JSON



Response



HTTP



400



```json

{

&#x20;   "success":false,



&#x20;   "error":"Invalid JSON payload"

}

```



\---



\# Example 5



Wrong HTTP Method



GET



/recommend



Response



HTTP



405



```json

{

&#x20;   "success":false,



&#x20;   "error":"Method not allowed"

}

```



\---



\# Example 6



Unsupported Content Type



Content-Type



text/plain



Response



HTTP



415



```json

{

&#x20;   "success":false,



&#x20;   "error":"Unsupported media type"

}

```



\---



\# Response Object Definitions



\## Feature Summary



```json

{

&#x20; "overall\_accuracy":49.25,

&#x20; "overall\_failed\_attempts":5,

&#x20; "average\_speed":"High"

}

```



\---



\## Recommendation Object



```json

{

&#x20; "topic":"Graphs",



&#x20; "priority":2,



&#x20; "priority\_score":82.15,



&#x20; "recommendation\_type":"Implementation Practice",



&#x20; "action":"Practice Graph BFS",



&#x20; "reason":"Repeated failed submissions indicate implementation issues.",



&#x20; "practice\_plan":{



&#x20;     "easy":3,



&#x20;     "medium":3,



&#x20;     "hard":1



&#x20; }

}

```



\---



\## Practice Plan



```json

{

&#x20;   "easy":3,



&#x20;   "medium":3,



&#x20;   "hard":1

}

```



\---



\## Topic Classification



```json

{

&#x20;   "Arrays":"Mastered",



&#x20;   "Graphs":"Weak",



&#x20;   "DP":"Critical"

}

```



\---



\# Standard HTTP Status Codes



| Code | Meaning |

|------|----------|

|200|Success|

|400|Malformed JSON|

|405|Wrong Method|

|415|Wrong Content Type|

|422|Validation Failed|

|500|Unexpected Server Error|



\---



\# API Design Rules



The API must always



✓ Return JSON



✓ Return success field



✓ Return deterministic output



✓ Return recommendations in priority order



✓ Include explanations



✓ Include positive reinforcement



\---



\# MERN Integration Example



Node.js



```javascript

const response = await axios.post(

&#x20;   "http://localhost:8000/recommend",

&#x20;   performanceData

);



console.log(response.data.recommendations);

```



React



```javascript

const recommendations = response.data.recommendations;



recommendations.map(item => (

&#x20;   <RecommendationCard

&#x20;       topic={item.topic}

&#x20;       action={item.action}

&#x20;       reason={item.reason}

&#x20;   />

));

```



\---



\# Future Compatibility



Future API versions may include



Historical trends



Difficulty adaptation



LLM-generated explanations



Weekly recommendations



None of these changes should break Version 1 clients.



\---



\# End of Document

