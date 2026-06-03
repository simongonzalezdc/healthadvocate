from healthadvocate.mcp_server import handle_message, handle_tool_call


def test_mcp_prepares_visit_questions():
    result = handle_tool_call(
        "prepare_visit_questions",
        {"concern": "persistent dizziness", "context": "worse in the morning"},
    )

    assert "questions" in result
    assert result["medical_boundary"] == "This is appointment preparation, not medical diagnosis."


def test_mcp_lists_tools():
    response = handle_message({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})

    assert response is not None
    assert any(tool["name"] == "insurance_denial_checklist" for tool in response["result"]["tools"])
