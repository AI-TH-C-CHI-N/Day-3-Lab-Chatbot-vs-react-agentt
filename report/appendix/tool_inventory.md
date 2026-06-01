# Tool Inventory

| Tool Name | Input Format | Use Case |
| :--- | :--- | :--- |
| `list_node_types` | string / optional JSON query | Discover supported node kinds and parameters. |
| `validate_spec` | WorkflowSpec JSON | Validate the workflow before compilation or deployment. |
| `compile_spec` | WorkflowSpec JSON | Convert the logical spec into native n8n JSON. |
| `create_workflow` | WorkflowSpec JSON | Validate, compile, and create the workflow in n8n. |
| `activate_workflow` | workflow id string | Activate the workflow after creation. |
| `get_workflow` | workflow id string | Inspect the workflow and confirm its state. |
| `delete_workflow` | workflow id string | Cleanup or rollback after a failed run. |
