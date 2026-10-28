---
source: GitHub mirror simongonzalezdc/healthadvocate issue #81 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/81
title: "Create and resume an encrypted synthetic Coverage Case"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:38Z
updated: 2026-07-22T19:43:57Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Create and resume an encrypted synthetic Coverage Case

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Let a user create, update, view, restart, and resume a synthetic Coverage Case whose deadlines, Continuity Targets, Evidence Items, Contact Events, Fact Status values, and next action persist in encrypted local storage outside the repository.

## Acceptance criteria

- [ ] A synthetic Coverage Case can be created, updated, read, restarted, and resumed through the public Coverage workflow.
- [ ] Evidence Items remain immutable and Contact Events remain append-only.
- [ ] Every material fact exposes Fact Status, provenance, and observation or retrieval date.
- [ ] Plaintext synthetic canaries are absent from database bytes, journals, temporary files, and backups.
- [ ] A missing or incorrect key fails before case metadata is returned.
- [ ] No real health or coverage data is used in implementation evidence.

## Blocked by

- ../decisions/70-define-the-coverage-case-domain-and-provenance-semantics.md
- ../decisions/71-validate-private-case-storage-and-key-management.md
- 79-gate-every-shipped-artifact-by-open-license-and-provenance.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:43:56Z)

## Completion receipt — issue 81

### Changed modules
- `healthadvocate/coverage/domain.py` — Coverage Case lifecycle, Fact Status, Evidence Items, Contact Events, Continuity Targets
- `healthadvocate/coverage/store.py` — AES-GCM encrypted SQLite payload store (`*.haenc`) outside the repository path by default
- `healthadvocate/coverage/keystore.py` — Keyring + in-memory keystores
- `healthadvocate/coverage/service.py` — public create/get/list/update/resume API
- `healthadvocate/app.py` — `/api/coverage/*` routes
- `healthadvocate/requirements.txt` — cryptography, keyring
- `healthadvocate/governance/data/artifact_registry.json` — license entries for new packages
- `tests/test_coverage_case_store.py`

### Tests
```
python3 -m pytest tests/ -q
42 passed
```

### Acceptance criteria
| Criterion | Evidence |
|---|---|
| Create/update/read/restart/resume synthetic case | store + service tests; `/api/coverage/cases` |
| Evidence immutable; contacts append-only | domain methods raise on mutate/duplicate |
| Material facts expose status, provenance, dates | asserted on stored facts |
| Canaries absent from encrypted file bytes | `test_plaintext_canary_absent_from_encrypted_bytes` |
| Missing/wrong key fails before metadata | dedicated tests |
| No real health data | synthetic-only create; real-case flag rejected |

### Proof
- Synthetic canaries only
- Data directory defaults outside repo (`Application Support` / env override)
- Commit local only

Closing with behavioral evidence.
