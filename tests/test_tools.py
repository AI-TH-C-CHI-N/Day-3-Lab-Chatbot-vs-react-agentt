import json

from src.n8n.tools import (
    create_n8n_tools,
    tool_activate_workflow,
    tool_compile_spec,
    tool_create_workflow,
    tool_delete_workflow,
    tool_get_workflow,
    tool_list_node_types,
    tool_validate_spec,
)


VALID_SPEC = {
    "name": "Daily Data Fetch and Email",
    "nodes": [
        {"ref": "trigger", "kind": "schedule", "params": {"cron": "0 9 * * *"}},
        {"ref": "fetch_data", "kind": "http", "params": {"url": "https://api.example.com/data", "method": "GET"}},
        {"ref": "send_email", "kind": "email", "params": {"to": "me@x.com", "subject": "Daily Data Report"}},
    ],
    "edges": [
        {"src": "trigger", "dst": "fetch_data"},
        {"src": "fetch_data", "dst": "send_email"},
    ],
}


class FakeClient:
    def __init__(self):
        self.created_workflow = None
        self.activated_workflow_id = None
        self.deleted_workflow_id = None
        self.queried_workflow_id = None

    def create_workflow(self, workflow):
        self.created_workflow = workflow
        return {"id": "abc123", "name": workflow["name"]}

    def activate_workflow(self, workflow_id):
        self.activated_workflow_id = workflow_id
        return {"id": workflow_id, "active": True}

    def get_workflow(self, workflow_id):
        self.queried_workflow_id = workflow_id
        return {
            "id": workflow_id,
            "name": "Daily Data Fetch and Email",
            "active": False,
            "nodes": [1, 2, 3],
            "connections": {"schedule": {"main": [[]]}},
        }

    def delete_workflow(self, workflow_id):
        self.deleted_workflow_id = workflow_id
        return {}


def test_list_node_types_filters_by_query():
    result = tool_list_node_types('{"query": "email"}')

    assert result.startswith("ok | ")
    assert "email" in result


def test_list_node_types_no_match_returns_empty_catalog_message():
    result = tool_list_node_types("zzzz")

    assert result == "ok | (no node types found for query)"


def test_validate_spec_success_and_error():
    assert tool_validate_spec(json.dumps(VALID_SPEC)) == "ok"
    assert tool_validate_spec("not-json") == "error: invalid JSON in validate_spec: Expecting value: line 1 column 1 (char 0)"


def test_compile_spec_success_and_error():
    compiled = tool_compile_spec(json.dumps(VALID_SPEC))

    assert compiled.startswith("ok | ")
    compiled_json = json.loads(compiled.split(" | ", 1)[1])
    assert compiled_json["name"] == VALID_SPEC["name"]
    assert tool_compile_spec("") == "error: compile_spec requires a WorkflowSpec JSON argument"


def test_create_workflow_success_and_error():
    client = FakeClient()

    result = tool_create_workflow(json.dumps(VALID_SPEC), client)

    assert result.startswith("ok | ")
    assert client.created_workflow["name"] == VALID_SPEC["name"]
    assert tool_create_workflow("not-json", client) == "error: invalid JSON in create_workflow: Expecting value: line 1 column 1 (char 0)"


def test_activate_get_and_delete_workflow_success_and_error():
    client = FakeClient()

    activate_result = tool_activate_workflow('"abc123"', client)
    get_result = tool_get_workflow('"abc123"', client)
    delete_result = tool_delete_workflow('"abc123"', client)

    assert activate_result == 'ok | {"id":"abc123","active":true}'
    assert get_result.startswith("ok | ")
    assert delete_result == "ok | deleted abc123"
    assert tool_activate_workflow("", client) == "error: activate_workflow requires a workflow ID argument"
    assert tool_get_workflow("", client) == "error: get_workflow requires a workflow ID argument"
    assert tool_delete_workflow("", client) == "error: delete_workflow requires a workflow ID argument"


def test_create_n8n_tools_dispatcher_unknown_tool():
    tools, execute_tool = create_n8n_tools(FakeClient())

    assert [tool["name"] for tool in tools] == [
        "list_node_types",
        "validate_spec",
        "compile_spec",
        "create_workflow",
        "activate_workflow",
        "get_workflow",
        "delete_workflow",
    ]
    assert execute_tool("missing", "") == "error: tool 'missing' not found"