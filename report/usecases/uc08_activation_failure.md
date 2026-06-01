# UC08 - Activation Failure

| Field | Value |
| :--- | :--- |
| Input | Lúc 9 sáng hàng ngày, gọi GET https://api.example.com/data và gửi email cho me@x.com. |
| Path | create_workflow succeeds -> activate_workflow fails -> get_workflow confirms inactive state |
| Expected Result | The agent reports the activation problem instead of pretending the workflow is live. |
| Insight | The runtime n8n config can still fail even when the spec compiles correctly. |
