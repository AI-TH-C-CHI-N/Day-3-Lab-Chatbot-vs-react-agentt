# UC03 - Parse Error Recovery

| Field | Value |
| :--- | :--- |
| Input | A prompt that makes the model answer with an invalid Action line. |
| Path | User -> ReAct Agent -> Parse Action fails -> Error Observation -> LLM retry |
| Expected Result | The agent appends a parse error observation and asks the model to recover. |
| Insight | The parser is intentionally strict so invalid tool calls do not silently propagate. |
