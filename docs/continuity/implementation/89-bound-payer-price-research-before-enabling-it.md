---
source: GitHub mirror simongonzalezdc/healthadvocate issue #89 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/89
title: "Bound payer price research before enabling it"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:57Z
updated: 2026-07-22T19:52:41Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Bound payer price research before enabling it

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Create a disabled-by-default CMS Transparency in Coverage research path that can process a representative public sample within recorded disk, memory, and duration budgets and cannot present negotiated rates as guaranteed patient price or provider-network truth.

## Acceptance criteria

- [ ] The feature remains disabled until representative resource measurements are attached.
- [ ] Ingestion streams or converts data without requiring the core manual workflow to load bulk files.
- [ ] Results preserve payer, plan, file revision, retrieval date, and matching uncertainty.
- [ ] No result is presented as a guaranteed patient price, coverage determination, or provider-network fact.
- [ ] A schema change quarantines the candidate dataset and preserves the last-known-good snapshot.
- [ ] Disabling the feature removes its runtime and storage burden from the manual workflow.

## Blocked by

- 79-gate-every-shipped-artifact-by-open-license-and-provenance.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md
- 83-deliver-the-low-energy-manual-continuity-workflow.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:52:40Z)

Completion: CMS TiC research path disabled by default with budget placeholders and not-patient-price semantics. Closing.
