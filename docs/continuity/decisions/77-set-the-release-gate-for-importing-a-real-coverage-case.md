---
source: GitHub mirror simongonzalezdc/healthadvocate issue #77 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/77
title: "Set the release gate for importing a real coverage case"
state_at_import: closed
labels: wayfinder:grilling
opened: 2026-07-22T17:53:49Z
updated: 2026-07-22T19:53:02Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Set the release gate for importing a real coverage case

## Question

What exact evidence and acceptance results must be present before HealthAdvocate may import and retain a real person's coverage, provider, medication, financial, and application data?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:53:01Z)

## Decision: Real-case release gate policy

### Decision
Real-case import stays **disabled** until all of the following are true for the exact shipped build:

1. Receipts exist for HA-E70 through HA-E78 (license, privacy, storage, commitment, UX, evidence, export, domain).
2. Each receipt has evidence_id, build_revision, generated_at, tool/version, pass/fail, artifact checksum/reference, reviewer, stop_rule.
3. No receipt is missing, skipped, waived, stale, flaky, or failed.
4. An **independent verifier** sets `independent_verifier_approved=true` on the exact build.
5. An explicit `real_case_import_override=true` is set after that approval.

Planning approval is not release approval. Default product path keeps `POST /api/coverage/import-real` at HTTP 403.

### Evidence contract
Implemented in `healthadvocate/governance/release_gate.py` and tested in `tests/test_release_gate.py`.

### Residual
Independent human verifier approval has not been granted in this implementation pass; therefore real-case import remains disabled.

Closes fog for issue 77 (policy complete). Issue 90 tracks exact-build proof.
