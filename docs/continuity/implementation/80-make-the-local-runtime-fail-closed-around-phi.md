---
source: GitHub mirror simongonzalezdc/healthadvocate issue #80 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/80
title: "Make the local runtime fail closed around PHI"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:36Z
updated: 2026-07-22T19:40:37Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Make the local runtime fail closed around PHI

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Make HealthAdvocate locally usable without exposing PHI: application, container, proxy, and model boundaries default to loopback; ambiguous or remote destinations fail closed; assembled model context is deidentified; and logs and errors do not disclose synthetic canaries.

## Acceptance criteria

- [ ] Default application, container, proxy, and model listeners are reachable only from loopback.
- [ ] An unauthenticated public or reverse-proxy route is absent from the default deployment.
- [ ] Redirects, ambiguous DNS, IPv4 and IPv6 bypass variants, and non-loopback model destinations are rejected.
- [ ] Deidentification runs over fully assembled context and failure prevents every model request.
- [ ] Synthetic identifiers do not appear in logs, errors, screenshots, temporary files, or unauthorized model calls.
- [ ] The deterministic Coverage workflow works when no model runtime is available.

## Blocked by

- ../decisions/72-prove-phi-isolation-across-runtime-and-model-boundaries.md
- 79-gate-every-shipped-artifact-by-open-license-and-provenance.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:40:35Z)

## Completion receipt — issue 80

### Changed modules
- `healthadvocate/privacy/` — endpoint policy, Privacy Boundary, logging redaction, startup bind policy, gated model helper
- `healthadvocate/core/engine.py` — full-context deidentification with status `success|no_pii_found|failed`; fail closed on errors
- `healthadvocate/core/llm_client.py` — loopback-only OpenAI-compatible client; redirects disabled; model optional/default off
- `healthadvocate/core/symptom_assessor.py` — uses gated full-context deidentification path
- `healthadvocate/app.py` — redacting logs + startup bind validation
- `Dockerfile` — bind `127.0.0.1` (was `0.0.0.0`)
- `docker-compose.yaml` — loopback publish only; Traefik/public reverse proxy removed from default
- `tests/test_privacy_boundary.py`

### Tests
```
python3 -m pytest tests/ -q
35 passed
```

### Acceptance criteria mapping
| Criterion | Evidence |
|---|---|
| Default listeners loopback-only | Dockerfile CMD host 127.0.0.1; compose `127.0.0.1:8080:8080`; startup rejects `0.0.0.0` |
| No unauthenticated public reverse-proxy default | compose has no traefik labels/networks |
| Redirects / DNS / IPv4/IPv6 / non-loopback rejected | `test_privacy_boundary.py` LoopbackPolicyTests |
| Full-context deidentification; failure blocks model | DeidentificationBoundaryTests + `structured_model_call` |
| Canaries absent from logs/errors | LoggingRedactionTests |
| Coverage works without model | `manual_workflow_status()` + model default disabled |

### Remaining risks
- Other feature modules still assemble profile after partial scrub in some paths; symptom assessor is migrated to the gated helper; remaining modules should migrate next
- Effective container runtime probe (live non-loopback namespace) not run in this ticket; source/default config + unit policy covered
- Screenshots/temp-file canary scan deferred to release-audit seam (issue 90)

### Proof
- Synthetic canaries only
- No real PHI, no external commitments
- Commit local only (not pushed)

Closing with behavioral evidence for all listed criteria.
