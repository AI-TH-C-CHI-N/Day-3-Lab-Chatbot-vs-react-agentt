# Ablation Studies

| Case | Chatbot Result | Agent v1 Result | Agent v2 Result | Winner |
| :--- | :--- | :--- | :--- | :--- |
| Simple question | Correct direct answer | Correct direct answer | Correct direct answer | Draw |
| Multi-step workflow | Descriptive only | Tool-using but less stable | Tool-using with validation + guardrails | Agent v2 |
| Activation failure | Cannot execute | Repeats activation attempt | Detects failure and stops with diagnosis | Agent v2 |

Summary:
- The chatbot is fine for short answers.
- The agent wins once a task needs tools and validation.
- Guardrails matter as much as the model.
