---
name: healthadvocate
description: Use HealthAdvocate for local-first patient advocacy workflows: appointment preparation, medical document questions, insurance denial checklists, bill-review preparation, local FastAPI health checks, and privacy-preserving health-navigation support. Trigger when an agent needs to help a patient prepare or understand next steps without diagnosing.
---

# HealthAdvocate

Use this skill when a task involves HealthAdvocate project work, appointment preparation, denial appeals, medical bill/document navigation, or local patient-advocacy workflows.

## Start Here

- Read `../../README.md` for setup, features, API endpoints, and the medical boundary.
- Use the CLI for local preparation workflows: `python -m healthadvocate.cli`.
- Use the MCP server when an agent host should call tools directly: `python -m healthadvocate.mcp_server`.
- The web app runs with `uvicorn healthadvocate.app:app --host 127.0.0.1 --port 8080`.

## Workflow

1. Identify whether the task is preparation, explanation, appeal support, bill review, or local app debugging.
2. Keep the medical boundary explicit: help the patient ask better questions and understand options; do not diagnose or prescribe.
3. Preserve privacy. Do not ask for names, SSNs, member IDs, or full records unless the user explicitly needs to work with them.
4. For app/API work, prefer local endpoints and the documented FastAPI routes.
5. For urgent symptoms or severe red flags, tell the user to seek emergency or professional care.

## CLI Examples

```bash
python -m healthadvocate.cli brief
python -m healthadvocate.cli visit-questions --concern "persistent dizziness"
python -m healthadvocate.cli denial-checklist --denial-reason "not medically necessary"
python -m healthadvocate.cli server-health --url http://127.0.0.1:8080
```

## MCP Setup

```json
{
  "mcpServers": {
    "healthadvocate": {
      "command": "python",
      "args": ["-m", "healthadvocate.mcp_server"]
    }
  }
}
```

## Guardrails

- Do not diagnose, prescribe, or replace care from a clinician.
- Do not say a medical bill or denial is legally invalid without evidence.
- Treat output as preparation material the patient can bring to a professional.
- Keep local-first privacy promises intact.
