import json

from src.telemetry.metrics import PerformanceTracker


def test_summarize_reports_average_latency_tokens_and_cost(tmp_path):
    tracker = PerformanceTracker()
    tracker.session_metrics = [
        {"latency_ms": 100, "total_tokens": 10, "cost_estimate": 0.1},
        {"latency_ms": 300, "total_tokens": 30, "cost_estimate": 0.3},
    ]

    summary = tracker.summarize()

    assert summary == {
        "request_count": 2,
        "avg_latency_ms": 200.0,
        "total_tokens": 40,
        "total_cost": 0.4,
    }

    exported = tracker.export_to_json(tmp_path / "metrics.json")
    saved = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))

    assert exported == saved
    assert saved["summary"]["total_cost"] == 0.4