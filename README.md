# Lab 3: Chatbot vs ReAct Agent (Industry Edition)

Welcome to Phase 3 of the Agentic AI course! This lab focuses on moving from a simple LLM Chatbot to a sophisticated **ReAct Agent** with industry-standard monitoring.

## 🚀 Getting Started

### 1. Setup Environment
Copy the `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2.1 Run Both Versions (Chatbot vs ReAct Agent)

Baseline chatbot (no tools):
```bash
python src/agent/baseline_chatbot.py
```

ReAct n8n agent (tool-using):
```bash
python src/agent/chatbot.py
```

Main entrypoint used by the lab instructions:
```bash
python main.py
```

Provider selection is controlled via `.env`:
```env
DEFAULT_PROVIDER=openai  # openai | google | local
DEFAULT_MODEL=gpt-4o
```

### 3. Directory Structure
- `src/tools/`: Extension point for your custom tools.

### 4. Travel Planner Use Case
The agent can be demoed as a Travel Planner assistant that builds n8n workflows for:
- fetching flight or hotel prices on a schedule
- filtering results with HTTP and Set nodes
- sending itinerary updates by email
- activating the workflow only after validation passes

This use case shows the difference between a plain chatbot answer and a tool-using agent that can actually orchestrate a workflow.

### 5. Core Tools
The lab focuses on these six core tools:
1. list_node_types - discover supported node kinds and parameters
2. validate_spec - validate the intermediate WorkflowSpec
3. compile_spec - compile WorkflowSpec into native n8n JSON
4. create_workflow - create a workflow in n8n
5. activate_workflow - activate the workflow after creation
6. get_workflow - inspect the workflow state and verify deployment

Optional cleanup tooling is also available through delete_workflow.

## 🏠 Running with Local Models (CPU)

If you don't want to use OpenAI or Gemini, you can run open-source models (like Phi-3) directly on your CPU using `llama-cpp-python`.

### 1. Download the Model
Download the **Phi-3-mini-4k-instruct-q4.gguf** (approx 2.2GB) from Hugging Face:
- [Phi-3-mini-4k-instruct-GGUF](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf)
- Direct Download: [phi-3-mini-4k-instruct-q4.gguf](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf)

### 2. Place Model in Project
Create a `models/` folder in the root and move the downloaded `.gguf` file there.

### 3. Update `.env`
Change your `DEFAULT_PROVIDER` and set the path:
```env
DEFAULT_PROVIDER=local
LOCAL_MODEL_PATH=./models/Phi-3-mini-4k-instruct-q4.gguf
```

## 🎯 Lab Objectives

1.  **Baseline Chatbot**: Observe the limitations of a standard LLM when faced with multi-step reasoning.
2.  **ReAct Loop**: Implement the `Thought-Action-Observation` cycle in `src/agent/agent.py`.
3.  **Provider Switching**: Swap between OpenAI and Gemini seamlessly using the `LLMProvider` interface.
4.  **Failure Analysis**: Use the structured logs in `logs/` to identify why the agent fails (hallucinations, parsing errors).
5.  **Grading & Bonus**: Follow the `SCORING.md` file in this repository to maximize your points and explore bonus metrics.

## 🛠️ How to Use This Baseline
The code is designed as a **Production Prototype**. It includes:
- **Telemetry**: Every action is logged in JSON format for later analysis.
- **Robust Provider Pattern**: Easily extendable to any LLM API.
- **Clean Skeletons**: Focus on the logic that matters—the agent's reasoning process.

---

*Happy Coding! Let's build agents that actually work.*
