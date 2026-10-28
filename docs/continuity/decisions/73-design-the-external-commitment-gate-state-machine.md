---
source: GitHub mirror simongonzalezdc/healthadvocate issue #73 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/73
title: "Design the external Commitment Gate state machine"
state_at_import: closed
labels: wayfinder:prototype
opened: 2026-07-22T17:53:37Z
updated: 2026-07-22T19:44:41Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Design the external Commitment Gate state machine

## Question

What user-visible state machine should classify and block payments, submissions, withdrawals, plan changes, cancellations, messages, and treatment changes while still allowing safe preparation and review?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:44:40Z)

## Decision: Commitment Gate state machine

### Decision

All external, financial, coverage, communication, and clinical-consequence intents pass through a Commitment Gate that never executes side effects. The gate classifies intents and returns a user-visible state. There is no outbound adapter for prohibited actions in this track.

### States
| State | Meaning | Side effects |
|---|---|---|
| `allowed` | Safe local preparation only | Local save/view/script generation only |
| `review_required` | Human must review outside the app before acting | Zero outbound calls |
| `blocked` | Explicitly prohibited for this product surface | Zero outbound calls |
| `not_applicable` | Intent does not apply to current case context | Zero outbound calls |

There is **no** `executed` or `submitted` state in the first release.

### Intent classification
**Prohibited → `blocked` or `review_required` (never auto-executed):**
- payment / charge / purchase
- application submission
- application withdrawal
- plan selection / plan change
- cancellation of coverage
- outbound message/email/SMS to insurer, county, provider, or pharmacy
- prescribe / change dose / start or stop medication
- treatment change authorization

Default for any unknown or ambiguous intent: **`review_required`** (never `allowed`).

**Allowed without gate friction:**
- create/update/view/resume local Coverage Case
- attach manual evidence
- append Contact Events (local notes only)
- generate deterministic scripts (county, provider, billing, pharmacy)
- export/redact/delete local case data per policy
- unofficial eligibility *estimate* display when feature-flagged (still no submit)

### User-visible behavior
- API returns `{ "gate_state", "intent", "reason", "allowed_next_steps", "side_effects": [] }`
- UI shows a clear “Review required” / “Blocked” panel; primary action never implies the system will pay, submit, or message
- Recorded outbound call count remains zero for every prohibited intent

### Alternatives considered
- Silent no-op without user notice: rejected (false confidence)
- Auto-open mailto/payment deep links: rejected for first release
- Allow with confirmation checkbox only: rejected; still no execution path

### Failure behavior
- Unknown intent → `review_required`
- Attempted execution path → hard error; no network

### Downstream constraints
- Issue 82 implements this table with zero-side-effect tests
- Scripts may prepare language but cannot send
- Real-case release still requires issue 90

Closes fog for issue 73.
