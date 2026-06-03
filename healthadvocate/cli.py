"""HealthAdvocate command-line interface."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from typing import Any


def project_brief() -> dict[str, Any]:
    return {
        "name": "HealthAdvocate",
        "summary": "Local-first patient advocacy app for understanding medical information, preparing questions, decoding bills, and fighting insurance denials.",
        "surfaces": {
            "web": "uvicorn healthadvocate.app:app --host 127.0.0.1 --port 8080",
            "cli": "python -m healthadvocate.cli",
            "mcp": "python -m healthadvocate.mcp_server",
            "skill": "skills/healthadvocate/SKILL.md",
        },
        "guardrail": "Help patients prepare, understand, and advocate. Do not diagnose, prescribe, or replace professional medical care.",
    }


def visit_questions(args: dict[str, Any]) -> dict[str, Any]:
    concern = str(args.get("concern") or "the main concern").strip()
    context = str(args.get("context") or "").strip()
    return {
        "concern": concern,
        "context": context,
        "questions": [
            f"What are the most likely explanations for {concern}, and what would rule them out?",
            "What symptoms or changes should make me seek urgent care?",
            "What tests, referrals, or follow-up steps would change the plan?",
            "What can I do safely at home while waiting for the next appointment?",
            "Can you explain this in plain language and write down the plan?",
        ],
        "prep_notes": [
            "Bring dates, medications, allergies, prior diagnoses, and recent test results.",
            "Write down the top three outcomes you need from the appointment.",
            "Ask how and when results will be communicated.",
        ],
        "medical_boundary": "This is appointment preparation, not medical diagnosis.",
    }


def denial_checklist(args: dict[str, Any]) -> dict[str, Any]:
    denial_reason = str(args.get("denial_reason") or "the stated denial reason").strip()
    return {
        "denial_reason": denial_reason,
        "checklist": [
            "deadline to appeal",
            "claim number and policy/member ID",
            "exact denial language",
            "medical necessity evidence",
            "doctor letter or visit notes",
            "relevant plan language",
            "requested remedy and contact information",
        ],
        "appeal_frame": [
            f"State that you are appealing the denial because of {denial_reason}.",
            "Attach supporting records and name each attachment.",
            "Ask for the clinical criteria used to make the decision.",
            "Request expedited review if delay could harm health.",
        ],
    }


def server_health(args: dict[str, Any]) -> dict[str, Any]:
    url = str(args.get("url") or "http://127.0.0.1:8080").rstrip("/")
    target = f"{url}/api/health"
    try:
        with urllib.request.urlopen(target, timeout=5) as response:
            body = response.read().decode("utf-8")
        return {"url": target, "ok": True, "response": json.loads(body)}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"url": target, "ok": False, "error": str(exc)}


def _print(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="HealthAdvocate CLI for patient-advocacy workflows.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("brief", help="Print the HealthAdvocate project brief.")

    visit = subparsers.add_parser("visit-questions", help="Prepare appointment questions.")
    visit.add_argument("--concern", required=True)
    visit.add_argument("--context", default="")

    denial = subparsers.add_parser("denial-checklist", help="Create an insurance denial appeal checklist.")
    denial.add_argument("--denial-reason", required=True)

    health = subparsers.add_parser("server-health", help="Check a running HealthAdvocate server.")
    health.add_argument("--url", default="http://127.0.0.1:8080")

    args = parser.parse_args()
    if args.command == "brief":
        _print(project_brief())
    elif args.command == "visit-questions":
        _print(visit_questions(vars(args)))
    elif args.command == "denial-checklist":
        _print(denial_checklist(vars(args)))
    elif args.command == "server-health":
        _print(server_health(vars(args)))


if __name__ == "__main__":
    main()
