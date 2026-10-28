---
source: GitHub mirror simongonzalezdc/healthadvocate issue #82 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/82
title: "Block every external commitment with zero side effects"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:40Z
updated: 2026-07-22T19:45:16Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Block every external commitment with zero side effects

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Make payment, submission, withdrawal, plan selection, cancellation, messaging, and treatment-change intents return a clear review-required result in both API and UI without producing any outbound call or external state change.

## Acceptance criteria

- [ ] Every prohibited intent maps to an explicit Commitment Gate state.
- [ ] Blocked and review-required results are understandable in the API and critical UI flow.
- [ ] Recorded outbound calls remain zero for every prohibited intent.
- [ ] Unknown or ambiguous intents fail closed instead of being coerced into an allowed action.
- [ ] Model output cannot satisfy, bypass, or mutate the Commitment Gate.

## Blocked by

- ../decisions/73-design-the-external-commitment-gate-state-machine.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:45:15Z)

## Completion receipt — issue 82

### Modules
- `healthadvocate/coverage/commitment_gate.py`
- `POST /api/coverage/commitment-gate`
- `tests/test_commitment_gate.py`

### Tests
```
python3 -m pytest tests/ -q
48 passed
```

### Acceptance criteria
| Criterion | Evidence |
|---|---|
| Every prohibited intent maps to explicit gate state | unit table in tests |
| Blocked/review results understandable in API | response shape test + endpoint |
| Zero outbound for prohibited intents | OutboundRecorder stays at 0; execute never called |
| Unknown intent → review_required | dedicated test |

### Proof
No real PHI; no payments/messages/submissions performed.

Closing.
