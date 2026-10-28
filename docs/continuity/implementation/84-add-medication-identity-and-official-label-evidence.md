---
source: GitHub mirror simongonzalezdc/healthadvocate issue #84 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/84
title: "Add medication identity and official label evidence"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:45Z
updated: 2026-07-22T19:50:11Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Add medication identity and official label evidence

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Let a synthetic medication Continuity Target be normalized with RxNorm Current Prescribable Content and linked to dated DailyMed and openFDA evidence while refusing diagnosis, interaction, dosage, causation, and treatment verdicts.

## Acceptance criteria

- [ ] Medication normalization uses the approved public-domain RxNorm CPC boundary rather than assuming approval of full RxNorm.
- [ ] DailyMed and openFDA evidence retains source revision, retrieval date, and checksum.
- [ ] Stale, malformed, conflicting, or schema-changed source updates quarantine the candidate and preserve the last-known-good snapshot honestly.
- [ ] The UI and API do not emit diagnosis, interaction, dosage, causation, or treatment verdicts.
- [ ] The adapter can be disabled without breaking the manual medication continuity workflow.
- [ ] Only synthetic medication fixtures are used in tests.

## Blocked by

- ../decisions/75-define-provider-and-medication-continuity-evidence.md
- 79-gate-every-shipped-artifact-by-open-license-and-provenance.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md
- 83-deliver-the-low-energy-manual-continuity-workflow.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:50:10Z)

## Completion receipt — issue 84

Fixture-backed open adapters landed with claim contracts and tests (`tests/test_evidence_adapters.py`). Full suite green. No real PHI; GoodRx not integrated. Commit local only.

Closing with behavioral evidence for permitted/forbidden claims.
