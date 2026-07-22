"""HealthAdvocate — FastAPI web application."""

from __future__ import annotations

import sys
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

# Ensure project root is on path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from healthadvocate.core.engine import HealthEngine
from healthadvocate.core import (
    symptom_assessor,
    document_decoder,
    bill_decoder,
    insurance_fighter,
    drug_checker,
    appointment_prep,
    discharge_translator,
    second_opinion,
    community_health,
    family_tracker,
    health_tracks,
)

from healthadvocate.privacy.logging_redaction import install_redacting_log_filter
from healthadvocate.privacy.startup import validate_startup_bind_policy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
install_redacting_log_filter(logger=logger)
install_redacting_log_filter(logger=logging.getLogger())

engine = HealthEngine()

_MAX_INPUT_LENGTH = 50_000  # 50KB max input text


def _cors_origins() -> list[str]:
    """Return allowed browser origins; default stays local-only."""
    raw = os.environ.get("HEALTHADVOCATE_ALLOW_ORIGINS", "")
    if raw.strip():
        return [origin.strip() for origin in raw.split(",") if origin.strip()]
    return [
        "http://127.0.0.1:8080",
        "http://localhost:8080",
    ]


def _validate_length(text: str, field: str = "input") -> None:
    if len(text) > _MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=422,
            detail=f"{field} exceeds maximum length of {_MAX_INPUT_LENGTH} characters.",
        )

# ---------------------------------------------------------------------------
# Lifespan: pre-warm OpenMed models at startup
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app):
    try:
        validate_startup_bind_policy()
    except SystemExit:
        logger.error("startup.bind_rejected code=non_loopback_bind")
        raise
    logger.info("Pre-loading OpenMed models...")
    await run_in_threadpool(engine.preload)
    logger.info("Models loaded. HealthAdvocate ready.")
    yield

app = FastAPI(
    title="HealthAdvocate",
    version="1.0.0",
    description="Patient healthcare advocacy powered by OpenMed medical NLP",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again."},
    )

# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class SymptomRequest(BaseModel):
    symptoms: str
    profile_id: Optional[str] = None

class DocumentRequest(BaseModel):
    text: str
    lang: str = "en"
    profile_id: Optional[str] = None

class BillRequest(BaseModel):
    bill_text: str
    profile_id: Optional[str] = None

class DenialRequest(BaseModel):
    denial_text: str
    patient_info: str = ""
    profile_id: Optional[str] = None

class DrugRequest(BaseModel):
    drug_name: str
    profile_id: Optional[str] = None

class AppointmentRequest(BaseModel):
    symptoms: str
    concern: str = ""
    profile_id: Optional[str] = None

class DischargeRequest(BaseModel):
    text: str
    lang: str = "en"
    profile_id: Optional[str] = None

class SecondOpinionRequest(BaseModel):
    records: str
    lang: str = "en"
    profile_id: Optional[str] = None

class CommunityRequest(BaseModel):
    text: str

class CoverageCaseCreateRequest(BaseModel):
    title: str
    next_action: str = "Review coverage situation and list deadlines"

class CoverageCaseUpdateRequest(BaseModel):
    title: Optional[str] = None
    next_action: Optional[str] = None
    lifecycle: Optional[str] = None
    deadlines: Optional[list[dict[str, str]]] = None

class CoverageEvidenceRequest(BaseModel):
    title: str
    source: str
    summary: str
    claim_class: str = "user_reported"
    checksum: str = ""

class CoverageContactRequest(BaseModel):
    channel: str
    party: str
    summary: str
    outcome: str = ""

class CoverageTargetRequest(BaseModel):
    kind: str
    name: str
    risk_notes: str = ""

class CoverageFactRequest(BaseModel):
    label: str
    value: str
    status: str = "user-reported"
    claim_class: str = "user_reported"
    provenance: str = "user"

class FamilyProfileRequest(BaseModel):
    name: str
    relationship: str = "self"

class FamilyConditionRequest(BaseModel):
    condition: str

class FamilyMedicationRequest(BaseModel):
    medication: str
    dosage: str = ""

class TrackRequest(BaseModel):
    concern: str
    category: str = "general"

class TrackUpdateRequest(BaseModel):
    status: str = ""
    note: str = ""

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "HealthAdvocate", "version": "1.0.0"}

# ---------------------------------------------------------------------------
# Feature endpoints
# ---------------------------------------------------------------------------

@app.post("/api/symptoms/assess")
async def assess_symptoms(request: SymptomRequest):
    _validate_length(request.symptoms, "Symptoms")
    result = await run_in_threadpool(
        symptom_assessor.assess_symptoms, engine, request.symptoms, request.profile_id
    )
    return result

@app.post("/api/documents/decode")
async def decode_document(request: DocumentRequest):
    _validate_length(request.text, "Document text")
    result = await run_in_threadpool(
        document_decoder.decode_document, engine, request.text, request.lang, request.profile_id
    )
    return result

@app.post("/api/bills/decode")
async def decode_bill(request: BillRequest):
    _validate_length(request.bill_text, "Bill text")
    result = await run_in_threadpool(
        bill_decoder.decode_bill, engine, request.bill_text, request.profile_id
    )
    return result

@app.post("/api/insurance/fight")
async def fight_denial(request: DenialRequest):
    _validate_length(request.denial_text, "Denial text")
    result = await run_in_threadpool(
        insurance_fighter.fight_denial, engine, request.denial_text, request.patient_info, request.profile_id
    )
    return result

@app.post("/api/drugs/check")
async def check_drug(request: DrugRequest):
    result = await run_in_threadpool(
        drug_checker.check_drug, engine, request.drug_name, request.profile_id
    )
    return result

@app.post("/api/appointments/prepare")
async def prepare_appointment(request: AppointmentRequest):
    _validate_length(request.symptoms, "Symptoms")
    result = await run_in_threadpool(
        appointment_prep.prepare_appointment, engine, request.symptoms, request.concern, request.profile_id
    )
    return result

@app.post("/api/discharge/translate")
async def translate_discharge(request: DischargeRequest):
    _validate_length(request.text, "Discharge text")
    result = await run_in_threadpool(
        discharge_translator.translate_discharge, engine, request.text, request.lang, request.profile_id
    )
    return result

@app.post("/api/second-opinion/create")
async def create_second_opinion(request: SecondOpinionRequest):
    _validate_length(request.records, "Medical records")
    result = await run_in_threadpool(
        second_opinion.create_brief, engine, request.records, request.lang, request.profile_id
    )
    return result

@app.post("/api/community/scan")
async def scan_community(request: CommunityRequest):
    _validate_length(request.text, "Bulletin text")
    result = await run_in_threadpool(
        community_health.scan_bulletin, engine, request.text
    )
    return result

# ---------------------------------------------------------------------------
# Coverage Continuity endpoints (synthetic cases only)
# ---------------------------------------------------------------------------

@app.get("/api/coverage/status")
async def coverage_status():
    from healthadvocate.coverage import manual_workflow_status
    status = manual_workflow_status()
    return {
        "available": status.available,
        "requires_model": status.requires_model,
        "requires_optional_dataset": status.requires_optional_dataset,
        "mode": status.mode,
        "notes": status.notes,
        "real_case_import_enabled": False,
    }

@app.post("/api/coverage/cases")
async def coverage_create_case(request: CoverageCaseCreateRequest):
    from healthadvocate.coverage import create_synthetic_case
    from healthadvocate.coverage.store import CaseStoreError
    try:
        return create_synthetic_case(request.title, next_action=request.next_action)
    except CaseStoreError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@app.get("/api/coverage/cases")
async def coverage_list_cases():
    from healthadvocate.coverage import list_cases
    return list_cases()

@app.get("/api/coverage/cases/{case_id}")
async def coverage_get_case(case_id: str):
    from healthadvocate.coverage import get_case
    from healthadvocate.coverage.store import CaseStoreError
    try:
        return get_case(case_id)
    except CaseStoreError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.patch("/api/coverage/cases/{case_id}")
async def coverage_update_case(case_id: str, request: CoverageCaseUpdateRequest):
    from healthadvocate.coverage import update_case
    from healthadvocate.coverage.store import CaseStoreError
    try:
        return update_case(
            case_id,
            title=request.title,
            next_action=request.next_action,
            lifecycle=request.lifecycle,
            deadlines=request.deadlines,
        )
    except CaseStoreError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@app.post("/api/coverage/cases/{case_id}/resume")
async def coverage_resume_case(case_id: str):
    from healthadvocate.coverage import resume_case
    from healthadvocate.coverage.store import CaseStoreError
    try:
        return resume_case(case_id)
    except CaseStoreError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/api/coverage/cases/{case_id}/evidence")
async def coverage_add_evidence(case_id: str, request: CoverageEvidenceRequest):
    from healthadvocate.coverage.service import get_default_store
    from healthadvocate.coverage.store import CaseStoreError
    try:
        store = get_default_store()
        case = store.add_evidence(
            case_id,
            title=request.title,
            source=request.source,
            summary=request.summary,
            claim_class=request.claim_class,
            checksum=request.checksum,
        )
        return case.to_dict()
    except CaseStoreError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@app.post("/api/coverage/cases/{case_id}/contacts")
async def coverage_add_contact(case_id: str, request: CoverageContactRequest):
    from healthadvocate.coverage.service import get_default_store
    from healthadvocate.coverage.store import CaseStoreError
    try:
        store = get_default_store()
        case = store.add_contact(
            case_id,
            channel=request.channel,
            party=request.party,
            summary=request.summary,
            outcome=request.outcome,
        )
        return case.to_dict()
    except CaseStoreError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@app.post("/api/coverage/cases/{case_id}/targets")
async def coverage_add_target(case_id: str, request: CoverageTargetRequest):
    from healthadvocate.coverage.service import get_default_store
    from healthadvocate.coverage.store import CaseStoreError
    try:
        store = get_default_store()
        case = store.add_target(
            case_id,
            kind=request.kind,
            name=request.name,
            risk_notes=request.risk_notes,
        )
        return case.to_dict()
    except CaseStoreError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@app.post("/api/coverage/cases/{case_id}/facts")
async def coverage_add_fact(case_id: str, request: CoverageFactRequest):
    from healthadvocate.coverage.service import get_default_store
    from healthadvocate.coverage.store import CaseStoreError
    try:
        store = get_default_store()
        case = store.add_fact(
            case_id,
            label=request.label,
            value=request.value,
            status=request.status,
            claim_class=request.claim_class,
            provenance=request.provenance,
        )
        return case.to_dict()
    except CaseStoreError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

# ---------------------------------------------------------------------------
# Family tracker endpoints
# ---------------------------------------------------------------------------

@app.post("/api/family/profiles")
async def create_family_profile(request: FamilyProfileRequest):
    return family_tracker.create_profile(request.name, request.relationship)

@app.get("/api/family/profiles")
async def list_family_profiles():
    return family_tracker.list_profiles()

@app.get("/api/family/profiles/{profile_id}")
async def get_family_profile(profile_id: str):
    result = family_tracker.get_profile(profile_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.post("/api/family/profiles/{profile_id}/conditions")
async def add_family_condition(profile_id: str, request: FamilyConditionRequest):
    result = family_tracker.add_condition(profile_id, request.condition)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.post("/api/family/profiles/{profile_id}/medications")
async def add_family_medication(profile_id: str, request: FamilyMedicationRequest):
    result = family_tracker.add_medication(profile_id, request.medication, request.dosage)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# ---------------------------------------------------------------------------
# Health tracks endpoints
# ---------------------------------------------------------------------------

@app.post("/api/tracks")
async def create_track(request: TrackRequest):
    return health_tracks.create_track(request.concern, request.category)

@app.get("/api/tracks")
async def list_tracks(status: Optional[str] = None):
    return health_tracks.list_tracks(status)

@app.post("/api/tracks/{track_id}")
async def update_track(track_id: str, request: TrackUpdateRequest):
    result = health_tracks.update_track(track_id, request.status, request.note)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/api/tracks/dashboard")
async def get_dashboard():
    return health_tracks.get_dashboard()

# ---------------------------------------------------------------------------
# Static files and SPA
# ---------------------------------------------------------------------------

_static_dir = Path(__file__).parent / "static"
if _static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

@app.get("/")
async def index():
    return FileResponse(str(_static_dir / "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("healthadvocate.app:app", host="127.0.0.1", port=8080, reload=True)
