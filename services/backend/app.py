"""
Backend API server for the Chatbot vs ReAct Agent lab.

This service serves the static frontend and exposes simple JSON endpoints for:
- `POST /api/chat` for chatbot or ReAct agent responses
- `POST /api/metrics` for session telemetry
- `GET /api/health` for readiness checks

The implementation reuses the project's real runtime code under `src/` so the
services folder no longer behaves like a copied travel-planner demo.
"""

from __future__ import annotations

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

load_dotenv()

from src.agent.chatbot import build_agent
from src.core.provider_factory import build_llm_from_env
from src.telemetry.logger import logger
from src.telemetry.metrics import tracker


FE_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

_BOOT_ERROR = None
_CHAT_LLM = None
_AGENT = None


def _bootstrap_runtime() -> None:
    global _BOOT_ERROR, _CHAT_LLM, _AGENT

    if _BOOT_ERROR is not None or _CHAT_LLM is not None or _AGENT is not None:
        return

    try:
        _CHAT_LLM = build_llm_from_env()
    except Exception as exc:
        _BOOT_ERROR = f"LLM initialization failed: {exc}"

    try:
        _AGENT = build_agent()
    except Exception as exc:
        if _BOOT_ERROR:
            _BOOT_ERROR = f"{_BOOT_ERROR}; agent bootstrap failed: {exc}"
        else:
            _BOOT_ERROR = f"Agent bootstrap failed: {exc}"


def _runtime_status() -> dict:
    _bootstrap_runtime()
    return {
        "ready": _CHAT_LLM is not None or _AGENT is not None,
        "provider": getattr(_CHAT_LLM, "model_name", None),
        "agent_ready": _AGENT is not None,
        "error": _BOOT_ERROR,
    }


class LabHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves static files and JSON endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FE_DIR, **kwargs)

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/chat":
            self._handle_chat()
        elif parsed.path == "/api/metrics":
            self._handle_metrics()
        else:
            self.send_error(404, "Not found")

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/health":
            self._json_response(_runtime_status())
            return

        super().do_GET()

    def _handle_chat(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            payload = self.rfile.read(content_length)
            data = json.loads(payload.decode("utf-8"))
        except (json.JSONDecodeError, ValueError) as exc:
            self._json_response({"error": f"Invalid JSON: {exc}"}, status=400)
            return

        message = data.get("message", "").strip()
        mode = data.get("mode", "agent").strip().lower()

        if not message:
            self._json_response({"error": "Empty message"}, status=400)
            return

        _bootstrap_runtime()
        if _BOOT_ERROR and _CHAT_LLM is None and _AGENT is None:
            self._json_response({"error": _BOOT_ERROR}, status=503)
            return

        logger.log_event("API_REQUEST", {"message": message, "mode": mode})

        try:
            if mode == "chatbot":
                result = self._run_chatbot(message)
            else:
                result = self._run_agent(message)

            self._json_response(result)
        except Exception as exc:
            logger.log_event("API_ERROR", {"error": str(exc)})
            self._json_response({"error": str(exc)}, status=500)

    def _run_chatbot(self, message: str) -> dict:
        import time

        if _CHAT_LLM is None:
            raise RuntimeError(_BOOT_ERROR or "Chatbot provider is unavailable")

        system_prompt = (
            "Bạn là một trợ lý cho lab Chatbot vs ReAct Agent. "
            "Trả lời ngắn gọn, rõ ràng, bằng tiếng Việt. "
            "Nếu người dùng hỏi về workflow n8n hoặc agent, hãy giải thích phù hợp với ngữ cảnh của dự án."
        )

        start = time.time()
        llm_result = _CHAT_LLM.generate(message, system_prompt=system_prompt)
        latency_ms = int((time.time() - start) * 1000)
        reply = llm_result.get("content", "")

        usage = llm_result.get("usage", {}) if isinstance(llm_result, dict) else {}
        tracker.track_request(
            provider=llm_result.get("provider", "chatbot") if isinstance(llm_result, dict) else "chatbot",
            model=getattr(_CHAT_LLM, "model_name", "unknown"),
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            latency_ms=latency_ms,
        )

        logger.log_event(
            "CHATBOT_RESPONSE",
            {
                "latency_ms": latency_ms,
                "tokens": usage.get("total_tokens", 0),
                "answer_preview": reply[:100],
            },
        )

        return {
            "reply": reply,
            "steps": 1,
            "status": "success",
            "traces": [],
            "mode": "chatbot",
        }

    def _run_agent(self, message: str) -> dict:
        if _AGENT is None:
            raise RuntimeError(_BOOT_ERROR or "Agent runtime is unavailable")

        answer = _AGENT.run(message)

        logger.log_event(
            "API_RESPONSE",
            {
                "status": "success",
                "answer_preview": answer[:100],
            },
        )

        return {
            "reply": answer,
            "steps": len(_AGENT.history),
            "status": "success",
            "traces": [],
            "mode": "agent",
        }

    def _handle_metrics(self):
        self._json_response(tracker.summarize() | {"requests": tracker.session_metrics})

    def _json_response(self, data: dict, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        pass


def main():
    port = int(os.getenv("PORT", "8000"))
    _bootstrap_runtime()

    server = HTTPServer(("0.0.0.0", port), LabHandler)
    print(f"\n🚀 Chatbot vs ReAct Agent server running at http://localhost:{port}")
    print(f"   Frontend:  http://localhost:{port}/index.html")
    print(f"   Chat:      http://localhost:{port}/chat.html")
    print(f"   API:       POST http://localhost:{port}/api/chat")
    print(f"   Health:    GET  http://localhost:{port}/api/health")
    if _BOOT_ERROR:
        print(f"   Warning:   {_BOOT_ERROR}")
    print("\n   Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
