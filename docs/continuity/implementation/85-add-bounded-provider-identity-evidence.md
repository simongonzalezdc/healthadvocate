---
source: GitHub mirror simongonzalezdc/healthadvocate issue #85 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/85
title: "Add bounded provider identity evidence"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:48Z
updated: 2026-07-22T19:50:14Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Add bounded provider identity evidence

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Let a provider Continuity Target be matched to dated NPPES identity evidence while network participation, licensure, availability, quality, and appointment access remain explicitly unknown until separately verified.

## Acceptance criteria

- [ ] Provider identity evidence records source revision, retrieval date, and match rationale.
- [ ] A match never upgrades network participation, licensure, availability, quality, or appointment access.
- [ ] Ambiguous or conflicting matches remain unresolved and create a verification task.
- [ ] Schema-change and stale-data behavior fails safely and preserves the last-known-good snapshot.
- [ ] The adapter can be disabled without breaking the manual provider continuity workflow.
- [ ] Tests use only synthetic provider identities.

## Blocked by

- ../decisions/75-define-provider-and-medication-continuity-evidence.md
- 79-gate-every-shipped-artifact-by-open-license-and-provenance.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md
- 83-deliver-the-low-energy-manual-continuity-workflow.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:50:13Z)

## Completion receipt — issue 85

Fixture-backed open adapters landed with claim contracts and tests (`tests/test_evidence_adapters.py`). Full suite green. No real PHI; GoodRx not integrated. Commit local only.

Closing with behavioral evidence for permitted/forbidden claims.
