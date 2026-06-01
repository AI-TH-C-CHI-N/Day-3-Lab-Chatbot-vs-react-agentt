# UC05 - Max Steps Exhaustion

| Field | Value |
| :--- | :--- |
| Input | A complex prompt that keeps producing partial thoughts but never reaches a valid final answer. |
| Path | User -> ReAct Agent -> Several Thought/Action/Observation cycles -> Max steps reached |
| Expected Result | The agent returns a fallback message that it could not finish within the step budget. |
| Insight | The max-step limit is a practical safety boundary for production use. |
