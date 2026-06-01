# UC07 - Metrics Export

| Field | Value |
| :--- | :--- |
| Input | Capture request metrics after a test session. |
| Path | track_request -> summarize -> export_to_json(filepath) |
| Expected Result | The metrics module writes a JSON file with summary statistics and session records. |
| Insight | This makes latency, tokens, and cost easy to report in the final deliverable. |
