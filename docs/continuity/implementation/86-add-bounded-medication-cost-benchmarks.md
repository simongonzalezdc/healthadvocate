---
source: GitHub mirror simongonzalezdc/healthadvocate issue #86 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/86
title: "Add bounded medication cost benchmarks"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:50Z
updated: 2026-07-22T19:50:17Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Add bounded medication cost benchmarks

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Let a medication target show dated NADAC and DrugCentral reference evidence as acquisition or reference benchmarks, never as a guaranteed cash price, insured price, coupon, or pharmacy quote; GoodRx remains outside the integration boundary.

## Acceptance criteria

- [ ] Every displayed value names its source, effective date, retrieval date, unit, and benchmark meaning.
- [ ] NADAC is always labeled as an acquisition-cost benchmark rather than a patient price.
- [ ] DrugCentral attribution and share-alike obligations are generated from the shipped source registry.
- [ ] No output claims a guaranteed cash, coupon, insured, or pharmacy-specific price.
- [ ] GoodRx and other proprietary price APIs are absent from dependencies and network calls.
- [ ] The adapter can be disabled without breaking the manual cost-comparison workflow.

## Blocked by

- ../decisions/75-define-provider-and-medication-continuity-evidence.md
- 79-gate-every-shipped-artifact-by-open-license-and-provenance.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md
- 83-deliver-the-low-energy-manual-continuity-workflow.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:50:16Z)

## Completion receipt — issue 86

Fixture-backed open adapters landed with claim contracts and tests (`tests/test_evidence_adapters.py`). Full suite green. No real PHI; GoodRx not integrated. Commit local only.

Closing with behavioral evidence for permitted/forbidden claims.
