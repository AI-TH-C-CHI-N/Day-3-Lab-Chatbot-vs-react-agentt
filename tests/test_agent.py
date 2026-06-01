from src.agent.agent import ReActAgent


class ScriptedLLM:
    def __init__(self, outputs):
        self.outputs = outputs
        self.calls = 0
        self.model_name = "scripted"

    def generate(self, prompt, system_prompt=None):
        index = min(self.calls, len(self.outputs) - 1)
        self.calls += 1
        return {
            "content": self.outputs[index],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
            "latency_ms": 1,
            "provider": "scripted",
        }


def test_agent_returns_final_answer_when_model_stops():
    llm = ScriptedLLM([
        "Thought: simple greeting is enough.\nFinal Answer: Hello there.",
    ])
    agent = ReActAgent(llm, tools=[], max_steps=3)

    result = agent.run("Say hello")

    assert result == "Hello there."
    assert agent.history[-1]["assistant"] == "Hello there."


def test_agent_stops_at_max_steps_when_no_final_answer():
    llm = ScriptedLLM([
        "Thought: I should use the tool.\nAction: echo(\"step-1\")",
        "Thought: I still do not have enough.\nAction: echo(\"step-2\")",
    ])
    agent = ReActAgent(
        llm,
        tools=[{"name": "echo", "description": "Echo the input", "func": lambda args: f"ok | {args}"}],
        max_steps=2,
    )

    result = agent.run("Try to answer")

    assert result == "I could not reach a final answer within the step budget."
    assert llm.calls == 2