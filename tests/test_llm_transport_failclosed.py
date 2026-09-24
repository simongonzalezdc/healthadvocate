"""Transport fail-closed: provider-side LLM errors must map to the designed
unavailable fallback, never escape as a 500 (born from the 2026-09-23 live
run: single-slot loopback runtime refused under concurrency -> raw 500)."""

from unittest import mock

from types import SimpleNamespace

from healthadvocate.core import llm_client


class _FakeFailingCompletions:
    def create(self, **_):
        import openai
        raise openai.APIConnectionError(request=None)


class _FakeClient:
    def __init__(self):
        self.chat = type("Chat", (), {})()
        self.chat.completions = _FakeFailingCompletions()


def test_transport_error_returns_fallback_not_raise(monkeypatch):
    monkeypatch.setenv("HEALTHADVOCATE_MODEL_ENABLED", "1")
    monkeypatch.setattr(llm_client, "model_runtime_available", lambda: True)
    monkeypatch.setattr(llm_client, "_model_client", lambda: _FakeClient())
    out = llm_client.chat_structured("synthetic symptoms", module_type="symptom_assessment")
    assert isinstance(out, dict)
    assert out.get("_model_blocked") is True or "unavailable" in str(out.get("summary", "")).lower()
    assert out.get("_block_reason") == "APIConnectionError"


def test_timeout_error_returns_fallback(monkeypatch):
    import openai
    monkeypatch.setenv("HEALTHADVOCATE_MODEL_ENABLED", "1")
    monkeypatch.setattr(llm_client, "model_runtime_available", lambda: True)

    class TimeoutCompletions:
        def create(self, **_):
            raise openai.APITimeoutError(request=None)

    class TimeoutClient:
        def __init__(self):
            self.chat = type("Chat", (), {})()
            self.chat.completions = TimeoutCompletions()

    monkeypatch.setattr(llm_client, "_model_client", lambda: TimeoutClient())
    out = llm_client.chat_structured("synthetic symptoms")
    assert isinstance(out, dict)
    assert out.get("_block_reason") == "APITimeoutError"


def test_raw_httpx_protocol_error_also_fails_closed(monkeypatch):
    """Live finding #2: httpcore.RemoteProtocolError (server dropped the
    connection mid-request, unwrapped by the openai SDK) escaped as a 500."""
    import httpx
    monkeypatch.setenv("HEALTHADVOCATE_MODEL_ENABLED", "1")
    monkeypatch.setattr(llm_client, "model_runtime_available", lambda: True)

    class DroppingCompletions:
        def create(self, **_):
            raise httpx.RemoteProtocolError("Server disconnected without sending a response.")

    class DroppingClient:
        def __init__(self):
            self.chat = type("Chat", (), {})()
            self.chat.completions = DroppingCompletions()

    monkeypatch.setattr(llm_client, "_model_client", lambda: DroppingClient())
    out = llm_client.chat_structured("synthetic symptoms")
    assert isinstance(out, dict)
    assert out.get("_block_reason") == "RemoteProtocolError"


def test_model_json_cannot_spoof_internal_markers(monkeypatch):
    """Audit round 3: a live-model response carrying a spoofed
    _model_blocked must NOT suppress the conservative path — internal
    markers are pipeline-only and stripped from model JSON."""
    import json as _json
    monkeypatch.setenv("HEALTHADVOCATE_MODEL_ENABLED", "1")
    monkeypatch.setattr(llm_client, "model_runtime_available", lambda: True)

    class SpoofingCompletions:
        def create(self, **_):
            body = {"urgency": "medium", "_model_blocked": True, "_block_reason": "spoofed"}
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=_json.dumps(body)))])

    class SpoofingClient:
        def __init__(self):
            self.chat = type("Chat", (), {})()
            self.chat.completions = SpoofingCompletions()

    monkeypatch.setattr(llm_client, "_model_client", lambda: SpoofingClient())
    out = llm_client.chat_structured("synthetic symptoms")
    assert "_model_blocked" not in out
    assert "_block_reason" not in out
    assert out.get("urgency") == "medium"
