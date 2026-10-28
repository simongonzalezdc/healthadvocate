---
source: GitHub mirror simongonzalezdc/healthadvocate issue #88 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/88
title: "Add an optional unofficial eligibility estimate"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:55Z
updated: 2026-07-22T19:52:39Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Add an optional unofficial eligibility estimate

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Add a feature-flagged PolicyEngine US workflow that calculates an explicitly unofficial estimate from reviewed synthetic inputs and shows the rule version, assumptions, missing facts, uncertainty, and official verification action without submitting anything.

## Acceptance criteria

- [ ] The feature is disabled by default and the manual workflow does not depend on it.
- [ ] Every estimate displays engine and rule version, input assumptions, missing inputs, and calculation date.
- [ ] The result is labeled unofficial and cannot claim approval, denial, current eligibility, or an enrollment deadline.
- [ ] An official verification action is shown beside the estimate.
- [ ] No application, message, selection, or payment is submitted.
- [ ] Tests pin rule fixtures and use only synthetic household and income inputs.

## Blocked by

- 79-gate-every-shipped-artifact-by-open-license-and-provenance.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md
- 83-deliver-the-low-energy-manual-continuity-workflow.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:52:37Z)

Completion: optional unofficial eligibility estimate stub, disabled by default, tests green. Manual workflow independent. Closing.
