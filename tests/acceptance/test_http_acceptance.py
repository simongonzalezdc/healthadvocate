"""Clean-room HTTP acceptance gate (audit remediation 4, 2026-09-24).

Mandate: HA-ADVERSARIAL-AUDIT-2026-09-24 — both engine legs (Opus
architecture + GPT-6 SOL engineering) converged on one prescription:
"install from the hash lock, boot the documented runtime, wait for
TRUTHFUL readiness, and drive every named feature through HTTP in BOTH
model-success and model-failure modes. Make it mandatory in CI."

This module is that gate. Unlike the source-level suite (SOL top risk 2:
"tests pin source-level behavior, not HTTP behavior"), every check here
is a real ASGI round trip through fastapi.testclient against the
documented FastAPI app (healthadvocate.app:app), in two modes:

- MODEL-FAILURE MODE: HEALTHADVOCATE_MODEL_ENABLED unset (the documented
  quick start; SOL top risk 1: "official setup silently disables the
  model"). Every generative surface must return 200 with the DESIGNED
  deterministic fallback, and the fallback must be MACHINE-DISTINGUISHABLE
  from a real answer (SOL: "fallback outputs are success-shaped") — we
  assert the ``structured_output._model_blocked`` marker, not just any
  200. A side test proves ZERO outbound model traffic occurs even though
  a reachable loopback model endpoint exists in-process.

- MODEL-SUCCESS MODE: an in-process OpenAI-compatible fake
  (http.server, 127.0.0.1, ephemeral port — genuinely loopback, so the
  endpoint policy accepts it) serves canned chat completions; the app is
  pointed at it via LM_STUDIO_URL + HEALTHADVOCATE_MODEL_ENABLED=1 +
  MEDICAL_LLM_MODEL=fake-model. The canned JSON must flow through to the
  HTTP response (parsed, not echoed raw), and the deidentified prompt —
  never the raw synthetic name — is what reaches the model host.

Marker coverage (machine-distinguishable fallback), pinned 2026-09-24:

| Surface                        | Marker                                        |
|--------------------------------|-----------------------------------------------|
| POST /api/symptoms/assess      | structured_output._model_blocked/_block_reason|
| POST /api/documents/decode     | same                                          |
| POST /api/bills/decode         | same                                          |
| POST /api/insurance/fight      | same                                          |
| POST /api/drugs/check          | same                                          |
| POST /api/appointments/prepare | same                                          |
| POST /api/discharge/translate  | same                                          |
| POST /api/second-opinion/create| same                                          |
| POST /api/community/scan       | same                                          |
| POST /api/coverage/commitment-gate | n/a — model-independent by design          |
| coverage case lifecycle        | n/a — manual workflow, requires_model=False   |
| family / tracks / adapters     | n/a — no generative leg                       |

Every generative surface carries the marker NESTED in
``structured_output``; no top-level marker field exists. Synthetic
inputs only (CANARY_* constants where text flows). No new dependencies;
no network beyond the in-process loopback fake.
"""

from __future__ import annotations

import importlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from fastapi.testclient import TestClient

# Synthetic input constants (repo canaries; never real PHI).
CANARY_PATIENT = "CANARY_PATIENT_ALPHA_9f3c"
CANARY_MEMBER = "CANARY_MEMBER_SYNTH_42"
SYNTH_NAME = "John Smith"  # PII-shaped synthetic; must be masked before any model hop

# The canned model answer. Its summary is the machine-checkable proof that
# the fake completion was parsed and flowed through to the HTTP surface.
FAKE_SUMMARY = "FAKE-MODEL ACCEPTANCE MARKER 7c1f synthetic model-shaped answer"
FAKE_ACTION_ITEM = "fake-model fixture action item"
_CANNED_CONTENT = json.dumps(
    {
        "summary": FAKE_SUMMARY,
        "urgency": "low",
        "action_items": [FAKE_ACTION_ITEM],
        "red_flags": [],
        "possible_conditions": [
            {"name": "fixture condition", "likelihood": "possible"}
        ],
        "recommended_specialist": None,
    }
)

FAKE_MODEL_NAME = "fake-model"

# The nine generative POST surfaces, each driven with synthetic text.
GENERATIVE_SURFACES = {
    "symptoms": ("/api/symptoms/assess", {"symptoms": f"mild headache and dizziness reported by {CANARY_PATIENT}"}),
    "documents": ("/api/documents/decode", {"text": f"Discharge summary for {CANARY_PATIENT}: follow up in 2 weeks."}),
    "bills": ("/api/bills/decode", {"bill_text": f"Hospital stay total $1,200.00 for {CANARY_MEMBER}."}),
    "insurance": ("/api/insurance/fight", {"denial_text": "Claim denied as not medically necessary.", "patient_info": ""}),
    "drugs": ("/api/drugs/check", {"drug_name": "metformin"}),
    "appointments": ("/api/appointments/prepare", {"symptoms": "persistent knee pain", "concern": "mobility"}),
    "discharge": ("/api/discharge/translate", {"text": "Take amoxicillin 500mg twice daily for 7 days."}),
    "second_opinion": ("/api/second-opinion/create", {"records": f"Records for {CANARY_PATIENT}: stable chronic condition."}),
    "community": ("/api/community/scan", {"text": "Local bulletin claims a miracle supplement cures fatigue."}),
}


# ---------------------------------------------------------------------------
# In-process OpenAI-compatible fake (loopback only)
# ---------------------------------------------------------------------------

class _FakeCompatHandler(BaseHTTPRequestHandler):
    """Serves canned /v1/chat/completions + /v1/models; records every body."""

    server_version = "FakeOpenAI/1"

    def log_message(self, *args):  # silence per-request stderr noise
        pass

    def _respond_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802 (http.server naming)
        if self.path.rstrip("/") == "/v1/models":
            self._respond_json(
                {
                    "object": "list",
                    "data": [
                        {
                            "id": FAKE_MODEL_NAME,
                            "object": "model",
                            "created": 1700000000,
                            "owned_by": "acceptance-fixture",
                        }
                    ],
                }
            )
        else:
            self._respond_json({"error": {"message": "not found"}}, status=404)

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw.decode("utf-8")) if raw else {}
        except json.JSONDecodeError:
            body = {"_unparseable": True}
        self.server.record_request(self.path, body)
        if self.path.rstrip("/") == "/v1/chat/completions":
            self._respond_json(
                {
                    "id": "chatcmpl-acceptance-fixture",
                    "object": "chat.completion",
                    "created": 1700000000,
                    "model": body.get("model", FAKE_MODEL_NAME),
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": _CANNED_CONTENT,
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 1,
                        "completion_tokens": 1,
                        "total_tokens": 2,
                    },
                }
            )
        else:
            self._respond_json({"error": {"message": "not found"}}, status=404)


class _RecordingHTTPServer(ThreadingHTTPServer):
    """ThreadingHTTPServer that records every request body it serves."""

    daemon_threads = True

    def __init__(self, address):
        super().__init__(address, _FakeCompatHandler)
        self._lock = threading.Lock()
        self._requests: list[dict] = []

    def record_request(self, path: str, body: dict) -> None:
        with self._lock:
            self._requests.append({"path": path, "body": body})

    def chat_requests(self) -> list[dict]:
        with self._lock:
            return [r for r in self._requests if "chat/completions" in r["path"]]

    def reset_requests(self) -> None:
        with self._lock:
            self._requests.clear()


class FakeModelServer:
    """Threaded loopback server on an ephemeral 127.0.0.1 port."""

    def __init__(self) -> None:
        self._httpd = _RecordingHTTPServer(("127.0.0.1", 0))
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def shutdown(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=5)

    @property
    def base_url(self) -> str:
        host, port = self._httpd.server_address[:2]
        return f"http://{host}:{port}/v1"

    def chat_requests(self) -> list[dict]:
        return self._httpd.chat_requests()

    def reset(self) -> None:
        self._httpd.reset_requests()


# ---------------------------------------------------------------------------
# Session plumbing: one documented app + fake; per-test mode application
# ---------------------------------------------------------------------------

_ENV_KEYS = (
    "HEALTHADVOCATE_MODEL_ENABLED",
    "HEALTHADVOCATE_MODEL_URL",
    "LM_STUDIO_URL",
    "MEDICAL_LLM_MODEL",
)


def _drop_default_store() -> None:
    """Close and forget the cached coverage store WITHOUT rebuilding it.

    service.get_default_store(reset=True) also eagerly re-constructs the
    store, which would bind the NEXT mode's env too early (and, on
    teardown, run against the just-restored real keystore). We only ever
    need the lazy drop: the next route call rebuilds under the mode's
    HEALTHADVOCATE_CASE_DIR + patched keystore.
    """
    from healthadvocate.coverage import service as coverage_service

    if coverage_service._DEFAULT_STORE is not None:
        try:
            coverage_service._DEFAULT_STORE.close()
        except Exception:
            pass
    coverage_service._DEFAULT_STORE = None


def _apply_mode(mode: str, fake: FakeModelServer, case_dir: str) -> None:
    """Switch llm_client between failure/success mode.

    healthadvocate.core.llm_client reads its env at import time, so the
    module is reloaded with the mode's env applied. importlib.reload
    re-executes into the SAME module dict, so every by-name reference
    held elsewhere (privacy.gated_model.chat_structured, ...) keeps
    working and observes the new values.
    """
    import os

    if mode == "failure":
        # The documented quick start: the model flag is simply unset.
        for key in _ENV_KEYS:
            os.environ.pop(key, None)
    else:
        os.environ["HEALTHADVOCATE_MODEL_ENABLED"] = "1"
        os.environ["LM_STUDIO_URL"] = fake.base_url
        os.environ["MEDICAL_LLM_MODEL"] = FAKE_MODEL_NAME
    os.environ["HEALTHADVOCATE_CASE_DIR"] = case_dir

    from healthadvocate.core import llm_client

    importlib.reload(llm_client)

    # Fresh per-mode coverage store (enc-at-rest cases must not leak
    # across modes; each mode gets its own HEALTHADVOCATE_CASE_DIR).
    _drop_default_store()


@pytest.fixture(scope="session")
def acceptance_env():
    """Isolate process-global state for the whole acceptance session.

    - Patches the coverage service keystore seam to InMemoryKeyStore (the
      documented test injection point) so the gate never writes a real
      key into the host OS credential store — and runs on hosts with no
      keyring backend (CI container).
    - Snapshot/restore the model env keys so the suite state afterwards
      is exactly what it was before.
    """
    import os

    from healthadvocate.coverage import service as coverage_service
    from healthadvocate.coverage.keystore import InMemoryKeyStore

    original_keystore_cls = coverage_service.KeyringKeyStore
    original_env = {key: os.environ.get(key) for key in _ENV_KEYS}
    original_case_dir = os.environ.get("HEALTHADVOCATE_CASE_DIR")

    def _inmemory_keystore_factory(*_args, **_kwargs):
        return InMemoryKeyStore()

    coverage_service.KeyringKeyStore = _inmemory_keystore_factory

    yield

    # Drop the store BEFORE restoring the keystore class (no eager rebuild
    # against the real keyring; the store file lives under the session tmp).
    _drop_default_store()
    coverage_service.KeyringKeyStore = original_keystore_cls
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    if original_case_dir is None:
        os.environ.pop("HEALTHADVOCATE_CASE_DIR", None)
    else:
        os.environ["HEALTHADVOCATE_CASE_DIR"] = original_case_dir
    from healthadvocate.core import llm_client

    importlib.reload(llm_client)


@pytest.fixture(scope="session")
def fake_model_server(acceptance_env):
    server = FakeModelServer()
    server.start()
    yield server
    server.shutdown()


@pytest.fixture(scope="session")
def documented_app(acceptance_env, tmp_path_factory):
    """Boot the documented runtime once (lifespan included)."""
    from healthadvocate.app import app

    with TestClient(app) as client:  # entering runs the startup lifespan
        yield client


@pytest.fixture(scope="session")
def _modes(documented_app, fake_model_server, tmp_path_factory):
    return {
        "client": documented_app,
        "fake": fake_model_server,
        "case_dirs": {
            "failure": str(tmp_path_factory.mktemp("ha-accept-cases-failure")),
            "success": str(tmp_path_factory.mktemp("ha-accept-cases-success")),
        },
    }


class _ModeClient:
    """TestClient for one mode, plus a chat_requests() view of the fake.

    Thin proxy: HTTP verbs go to the real ASGI client; chat_requests()
    exposes what the in-process fake model server actually received.
    """

    def __init__(self, client: TestClient, fake: FakeModelServer) -> None:
        self._client = client
        self._fake = fake

    def __getattr__(self, name):
        return getattr(self._client, name)

    def chat_requests(self) -> list[dict]:
        return self._fake.chat_requests()


@pytest.fixture()
def failure_client(_modes):
    """Every generative surface in the documented default (model off)."""
    _modes["fake"].reset()
    _apply_mode("failure", _modes["fake"], _modes["case_dirs"]["failure"])
    return _ModeClient(_modes["client"], _modes["fake"])


@pytest.fixture()
def success_client(_modes):
    """Model on, pointed at the in-process loopback fake."""
    _modes["fake"].reset()
    _apply_mode("success", _modes["fake"], _modes["case_dirs"]["success"])
    return _ModeClient(_modes["client"], _modes["fake"])


# ---------------------------------------------------------------------------
# Shared assertion helpers
# ---------------------------------------------------------------------------

def _assert_fallback_shape(payload: dict) -> None:
    """The designed deterministic fallback, machine-distinguishable.

    SOL's finding: fallbacks are success-shaped. The contract pinned
    here: the nested structured_output must carry ``_model_blocked`` True
    plus a non-empty ``_block_reason`` (PrivacyBoundaryError when the
    model flag is off; deidentification_failed if the privacy leg could
    not run — both are the designed fail-closed legs).
    """
    assert isinstance(payload, dict), payload
    nested = payload.get("structured_output")
    assert isinstance(nested, dict), f"no structured_output marker block: {payload}"
    assert nested.get("_model_blocked") is True, nested
    reason = nested.get("_block_reason")
    assert isinstance(reason, str) and reason, nested


def _assert_model_shaped(payload: dict) -> None:
    """The canned fake completion, parsed and flowed through."""
    assert isinstance(payload, dict), payload
    nested = payload.get("structured_output")
    assert isinstance(nested, dict), payload
    assert not nested.get("_model_blocked"), nested
    assert nested.get("summary") == FAKE_SUMMARY, nested
    assert nested.get("action_items") == [FAKE_ACTION_ITEM], nested


# ---------------------------------------------------------------------------
# MODEL-FAILURE MODE — the documented default must fail closed, visibly
# ---------------------------------------------------------------------------

class TestModelFailureMode:
    @pytest.mark.parametrize("surface", sorted(GENERATIVE_SURFACES))
    def test_generative_surface_returns_designed_fallback(self, failure_client, surface):
        path, body = GENERATIVE_SURFACES[surface]
        response = failure_client.post(path, json=body)
        assert response.status_code == 200, response.text
        _assert_fallback_shape(response.json())

    def test_zero_outbound_model_traffic_while_endpoint_reachable(self, failure_client):
        """Fail-closed means fail SILENT to the wire: a reachable loopback
        model endpoint exists in-process, and the disabled runtime must
        never send it a single request (audit: guarantees enforced, not
        assumed)."""
        for path, body in GENERATIVE_SURFACES.values():
            assert failure_client.post(path, json=body).status_code == 200
        assert failure_client.chat_requests() == []

    def test_health_report(self, failure_client):
        response = failure_client.get("/api/health")
        assert response.status_code == 200
        payload = response.json()
        # TODO(audit HA-ADVERSARIAL-AUDIT-2026-09-24, SOL "readiness stays
        # green through model failure"): /api/health reports a constant
        # {"status": "ok"} with no model-readiness field at all — it cannot
        # overclaim model readiness, but it also cannot inform: it stays
        # green while every generative surface degrades to fallbacks.
        # Current behavior pinned as-is here; product fix out of scope for
        # this tests+CI-only PR.
        assert payload["status"] == "ok"
        assert payload["service"] == "HealthAdvocate"
        assert {"status", "service", "version"} <= set(payload)

    def test_index_served(self, failure_client):
        response = failure_client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_coverage_status_truthful_manual_workflow(self, failure_client):
        response = failure_client.get("/api/coverage/status")
        assert response.status_code == 200
        payload = response.json()
        assert payload["available"] is True
        assert payload["requires_model"] is False
        assert payload["real_case_import_enabled"] is False

    def test_commitment_gate_blocks_prohibited_and_allows_local(self, failure_client):
        blocked = failure_client.post("/api/coverage/commitment-gate", json={"intent": "pay"})
        assert blocked.status_code == 200
        payload = blocked.json()
        assert payload["gate_state"] == "blocked"
        assert payload["intent"] == "payment"
        assert payload["executed"] is False
        assert payload["side_effects"] == []

        allowed = failure_client.post(
            "/api/coverage/commitment-gate", json={"intent": "save"}
        )
        assert allowed.status_code == 200
        assert allowed.json()["gate_state"] == "allowed"

    def test_real_case_import_refused_over_http(self, failure_client):
        response = failure_client.post("/api/coverage/import-real")
        assert response.status_code == 403
        assert "disabled" in response.json()["detail"].lower()

    def test_coverage_case_lifecycle_over_http(self, failure_client):
        client = failure_client
        created = client.post(
            "/api/coverage/cases",
            json={"title": f"Acceptance case {CANARY_MEMBER}", "next_action": "List deadlines"},
        )
        assert created.status_code == 200, created.text
        case = created.json()
        case_id = case["case_id"]
        assert case["synthetic"] is True

        listed = client.get("/api/coverage/cases")
        assert listed.status_code == 200
        assert any(c["case_id"] == case_id for c in listed.json())

        patched = client.patch(
            f"/api/coverage/cases/{case_id}",
            json={
                "lifecycle": "active",
                "next_action": "Collect denial letter",
                "deadlines": [{"label": "appeal", "due": "2026-10-01"}],
            },
        )
        assert patched.status_code == 200, patched.text
        assert patched.json()["lifecycle"] == "active"

        for path, body in (
            (f"/api/coverage/cases/{case_id}/evidence",
             {"title": "Denial letter", "source": "user", "summary": f"Notice for {CANARY_MEMBER}"}),
            (f"/api/coverage/cases/{case_id}/contacts",
             {"channel": "phone", "party": "Insurer line", "summary": "Asked for reconsideration form"}),
            (f"/api/coverage/cases/{case_id}/targets",
             {"kind": "provider", "name": "Fixture Clinic", "risk_notes": ""}),
            (f"/api/coverage/cases/{case_id}/facts",
             {"label": "member_id", "value": CANARY_MEMBER, "provenance": "synthetic"}),
        ):
            step = client.post(path, json=body)
            assert step.status_code == 200, step.text

        view = client.get(f"/api/coverage/cases/{case_id}/view")
        assert view.status_code == 200
        assert view.json()["case_id"] == case_id
        assert view.json()["ui"]["requires_model"] is False

        script = client.get(f"/api/coverage/cases/{case_id}/scripts/county")
        assert script.status_code == 200
        assert script.json()["kind"] == "county"

        export = client.post(
            f"/api/coverage/cases/{case_id}/export",
            json={"mode": "redacted", "reviewed": False},
        )
        assert export.status_code == 200
        assert export.json()["written"] is False  # review gate respected over HTTP

        resumed = client.post(f"/api/coverage/cases/{case_id}/resume")
        assert resumed.status_code == 200
        assert resumed.json()["resumed"] is True

        deleted = client.post(
            f"/api/coverage/cases/{case_id}/delete", json={"unowned_source_paths": []}
        )
        assert deleted.status_code == 200
        assert client.get(f"/api/coverage/cases/{case_id}").status_code == 404

    def test_family_profiles_over_http(self, failure_client):
        client = failure_client
        created = client.post(
            "/api/family/profiles",
            json={"name": CANARY_MEMBER, "relationship": "parent"},
        )
        assert created.status_code == 200, created.text
        profile_id = created.json()["id"]

        listed = client.get("/api/family/profiles")
        assert listed.status_code == 200
        assert any(p["id"] == profile_id for p in listed.json())

        cond = client.post(
            f"/api/family/profiles/{profile_id}/conditions",
            json={"condition": "hypertension"},
        )
        assert cond.status_code == 200

        med = client.post(
            f"/api/family/profiles/{profile_id}/medications",
            json={"medication": "amlodipine", "dosage": "5mg"},
        )
        assert med.status_code == 200

    def test_health_tracks_over_http(self, failure_client):
        client = failure_client
        created = client.post("/api/tracks", json={"concern": "morning walks", "category": "activity"})
        assert created.status_code == 200, created.text
        track_id = created.json()["id"]

        updated = client.post(f"/api/tracks/{track_id}", json={"status": "done", "note": "30 min"})
        assert updated.status_code == 200

        dash = client.get("/api/tracks/dashboard")
        assert dash.status_code == 200

    def test_offline_adapters_deterministic_shapes(self, failure_client):
        rx = failure_client.post("/api/coverage/adapters/rxnorm", json={"name": "metformin"})
        assert rx.status_code == 200
        assert rx.json()["claim_class"] == "official_source"
        assert "forbidden_claims" in rx.json()

        verdict = failure_client.post(
            "/api/coverage/adapters/clinical-verdict", json={"kind": "efficacy"}
        )
        assert verdict.status_code == 200
        assert verdict.json()["allowed"] is False
        assert verdict.json()["kind"] == "efficacy"


# ---------------------------------------------------------------------------
# MODEL-SUCCESS MODE — the canned completion must actually flow through
# ---------------------------------------------------------------------------

class TestModelSuccessMode:
    @pytest.mark.parametrize("surface", sorted(GENERATIVE_SURFACES))
    def test_generative_surface_returns_model_shaped_answer(self, success_client, surface):
        path, body = GENERATIVE_SURFACES[surface]
        response = success_client.post(path, json=body)
        assert response.status_code == 200, response.text
        _assert_model_shaped(response.json())

    def test_fake_model_actually_drove_the_surfaces(self, success_client):
        """The gate proves delivery, not just absence of failure: the fake
        server must have received chat requests naming fake-model."""
        for path, body in GENERATIVE_SURFACES.values():
            assert success_client.post(path, json=body).status_code == 200
        requests = success_client.chat_requests()
        assert requests, "no chat completions reached the fake model server"
        assert all(r["body"].get("model") == FAKE_MODEL_NAME for r in requests)

    def test_summary_projects_to_top_level_explanation(self, success_client):
        response = success_client.post(
            "/api/symptoms/assess", json={"symptoms": "mild headache"}
        )
        assert response.status_code == 200
        assert response.json()["explanation"] == FAKE_SUMMARY

    def test_deidentification_precedes_model_hop(self, success_client):
        """Audit C-series at acceptance level: PII-shaped synthetic input
        must be masked BEFORE any text reaches the model destination —
        the raw name must never appear in any request the fake received."""
        response = success_client.post(
            "/api/symptoms/assess",
            json={"symptoms": f"John Smith reports mild headache since Monday"},
        )
        assert response.status_code == 200
        outbound = [json.dumps(r) for r in success_client.chat_requests()]
        assert outbound, "expected at least one model request"
        for blob in outbound:
            assert SYNTH_NAME not in blob, "raw synthetic name reached the model host"

    def test_health_report_unchanged_by_model_presence(self, success_client):
        response = success_client.get("/api/health")
        assert response.status_code == 200
        # Same pinned shape as failure mode — see the TODO there (audit:
        # readiness truth). The payload must not silently change shape
        # between modes.
        assert response.json()["status"] == "ok"

    def test_coverage_status_still_requires_no_model(self, success_client):
        """Truthfulness anchor: a present model runtime must not flip the
        manual workflow into claiming a model dependency."""
        payload = success_client.get("/api/coverage/status").json()
        assert payload["requires_model"] is False
        assert payload["available"] is True

    def test_commitment_gate_does_not_loosen_with_model(self, success_client):
        blocked = success_client.post("/api/coverage/commitment-gate", json={"intent": "pay"})
        assert blocked.status_code == 200
        assert blocked.json()["gate_state"] == "blocked"
        assert blocked.json()["executed"] is False

    def test_coverage_case_lifecycle_over_http(self, success_client):
        client = success_client
        created = client.post(
            "/api/coverage/cases",
            json={"title": f"Acceptance success-mode case {CANARY_MEMBER}"},
        )
        assert created.status_code == 200, created.text
        case_id = created.json()["case_id"]

        # Legal transition chain: draft -> active -> needs-review (the
        # store enforces the lifecycle graph; illegal jumps 400).
        patched = client.patch(
            f"/api/coverage/cases/{case_id}", json={"lifecycle": "active"}
        )
        assert patched.status_code == 200
        assert patched.json()["lifecycle"] == "active"
        reviewed = client.patch(
            f"/api/coverage/cases/{case_id}", json={"lifecycle": "needs-review"}
        )
        assert reviewed.status_code == 200, reviewed.text
        assert reviewed.json()["lifecycle"] == "needs-review"

        illegal = client.patch(
            f"/api/coverage/cases/{case_id}", json={"lifecycle": "draft"}
        )
        assert illegal.status_code == 400  # transition graph enforced over HTTP

        evidence = client.post(
            f"/api/coverage/cases/{case_id}/evidence",
            json={"title": "EOB", "source": "user", "summary": "synthetic EOB text"},
        )
        assert evidence.status_code == 200

        view = client.get(f"/api/coverage/cases/{case_id}/view")
        assert view.status_code == 200

        deleted = client.post(
            f"/api/coverage/cases/{case_id}/delete", json={"unowned_source_paths": []}
        )
        assert deleted.status_code == 200
