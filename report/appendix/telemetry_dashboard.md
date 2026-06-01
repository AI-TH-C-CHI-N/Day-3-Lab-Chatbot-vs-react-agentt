# Telemetry Dashboard

- **Average Latency (P50)**: ~4310 ms per agent step
- **Max Latency (P99)**: ~9840 ms per agent step
- **Average Tokens per Task**: not yet persisted in the main trace; use `PerformanceTracker.summarize()` for the next benchmark pass.
- **Total Cost of Test Suite**: not yet persisted in the main trace; use `export_to_json()` to capture it.

Observed runtime summary:
- Total steps: 11
- `create_workflow`: success twice
- `activate_workflow`: failed twice with `Bad request: Could not find property option`
- `get_workflow`: success once and confirmed the workflow was still inactive
