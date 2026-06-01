"""
baseline_chatbot.py — plain chatbot baseline (no tools, no ReAct loop).

Purpose:
- Provide the required "Chatbot" baseline for Lab 3.
- Answer user questions directly with a single LLM call per turn.

Run:
    python src/agent/baseline_chatbot.py
"""

import os
import sys
from typing import Dict, List

from dotenv import load_dotenv

# Make `src` importable when running this file directly from src/agent.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.provider_factory import build_llm_from_env


def run_baseline_chat() -> None:
    try:
        llm = build_llm_from_env()
    except Exception as e:
        print(f"No usable LLM provider found: {e}")
        sys.exit(1)

    print("=== Baseline Chatbot (No Tools) ===")
    print("Type your message. Commands: 'clear' to reset memory, 'quit' to exit.\n")

    history: List[Dict[str, str]] = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Bye!")
            break

        if user_input.lower() in {"clear", "reset"}:
            history = []
            print("(conversation memory cleared)\n")
            continue

        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})
        transcript = "\n".join([f"{m['role']}: {m['content']}" for m in history])

        system_prompt = (
            "You are a helpful assistant. Answer clearly and concisely. "
            "Do not claim to have called external tools or APIs."
        )

        result = llm.generate(transcript, system_prompt=system_prompt)
        answer = result.get("content", "") if isinstance(result, dict) else str(result)
        history.append({"role": "assistant", "content": answer})

        print(f"Bot: {answer}\n")


def main() -> None:
    load_dotenv()
    run_baseline_chat()


if __name__ == "__main__":
    main()
