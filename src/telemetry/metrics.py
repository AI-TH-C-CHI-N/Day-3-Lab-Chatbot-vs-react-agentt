import json
import time
from pathlib import Path
from typing import Dict, Any, List
from src.telemetry.logger import logger

class PerformanceTracker:
    """
    Tracking industry-standard metrics for LLMs.
    """
    def __init__(self):
        self.session_metrics = []

    def track_request(self, provider: str, model: str, usage: Dict[str, int], latency_ms: int):
        """
        Logs a single request metric to our telemetry.
        """
        total_tokens = usage.get("total_tokens")
        if total_tokens is None:
            total_tokens = usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)

        metric = {
            "provider": provider,
            "model": model,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": total_tokens,
            "latency_ms": latency_ms,
            "cost_estimate": self._calculate_cost(model, usage) # Mock cost calculation
        }
        self.session_metrics.append(metric)
        logger.log_event("LLM_METRIC", metric)

    def _calculate_cost(self, model: str, usage: Dict[str, int]) -> float:
        """
        TODO: Implement real pricing logic.
        For now, returns a dummy constant.
        """
        return (usage.get("total_tokens", 0) / 1000) * 0.01

    def summarize(self) -> Dict[str, Any]:
        """Summarize the current session metrics."""
        count = len(self.session_metrics)
        if count == 0:
            return {
                "request_count": 0,
                "avg_latency_ms": 0.0,
                "total_tokens": 0,
                "total_cost": 0.0,
            }

        total_latency = sum(metric.get("latency_ms", 0) for metric in self.session_metrics)
        total_tokens = sum(metric.get("total_tokens", 0) for metric in self.session_metrics)
        total_cost = sum(metric.get("cost_estimate", 0.0) for metric in self.session_metrics)

        return {
            "request_count": count,
            "avg_latency_ms": total_latency / count,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
        }

    def export_to_json(self, filepath: str) -> Dict[str, Any]:
        """Export the metrics session to a JSON file and return the payload."""
        payload = {
            "summary": self.summarize(),
            "session_metrics": self.session_metrics,
        }

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)

        return payload

# Global tracker instance
tracker = PerformanceTracker()
