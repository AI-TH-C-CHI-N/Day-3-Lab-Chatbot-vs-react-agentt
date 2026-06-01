# UC02 - Multi-Step Workflow

| Field | Value |
| :--- | :--- |
| Input | Check the available node types and then create a workflow for a daily email reminder. |
| Path | User -> ReAct Agent -> list_node_types -> validate_spec -> compile_spec -> create_workflow |
| Expected Result | The agent decomposes the task, calls tools in sequence, and returns the workflow result. |
| Insight | This is the clearest example of why ReAct beats a plain chatbot on operational tasks. |
