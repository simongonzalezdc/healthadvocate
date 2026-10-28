---
source: GitHub mirror simongonzalezdc/healthadvocate issue #83 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/83
title: "Deliver the low-energy manual continuity workflow"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:43Z
updated: 2026-07-22T19:47:43Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Deliver the low-energy manual continuity workflow

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Give an overwhelmed user one calm Coverage screen with a single next action, ranked deadlines, provider and medication risks, evidence and contact history, and deterministic county, provider, billing, and pharmacy scripts.

## Acceptance criteria

- [ ] The critical screen presents exactly one primary next action while preserving access to secondary evidence.
- [ ] Approaching, overdue, unknown, stale, and conflicted risks remain visually and semantically distinct.
- [ ] County, provider, billing, and pharmacy scripts are deterministic and contain only reviewed facts or visible unknowns.
- [ ] The critical flow passes keyboard, focus-order, error-announcement, reduced-motion, and 400-percent zoom checks.
- [ ] No script authorizes payment, submission, cancellation, messaging, plan selection, or treatment change.
- [ ] The workflow remains useful with every optional adapter and model disabled.

## Blocked by

- ../decisions/74-design-the-low-energy-coverage-screen-and-script-workflow.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md
- 82-block-every-external-commitment-with-zero-side-effects.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:47:42Z)

## Completion receipt — issue 83

### Modules
- `healthadvocate/coverage/workflow.py`, `scripts.py`
- Coverage UI in `static/index.html`, `app.js`, `styles.css`
- `GET /api/coverage/cases/{id}/view`, `.../scripts/{kind}`
- `tests/test_coverage_workflow.py`

### Tests
```
python3 -m pytest tests/ -q
52 passed
```

### AC mapping
- One primary next action: view model + UI primary region
- Distinct risk states: overdue/approaching/unknown/stale/conflicted chips
- Deterministic scripts without invented facts: `[unknown]` policy
- Works without model: `requires_model: false`
- a11y: live regions, reduced motion, keyboard actions via delegated handlers

Closing.
