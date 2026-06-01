# UC04 - Repeated Tool Error Guardrail

| Field | Value |
| :--- | :--- |
| Input | A request that repeatedly triggers the same invalid tool argument or unsupported tool call. |
| Path | User -> ReAct Agent -> Tool error -> Same tool error again -> Early stop |
| Expected Result | The agent stops early with a message explaining that the same error repeated. |
| Insight | This prevents infinite loops and avoids wasting tokens on unrecoverable states. |
