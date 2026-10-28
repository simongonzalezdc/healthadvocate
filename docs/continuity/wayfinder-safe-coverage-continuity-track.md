---
source: GitHub mirror simongonzalezdc/healthadvocate issue #69 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/69
title: "Wayfinder: Safe Coverage Continuity Track"
state_at_import: open
labels: wayfinder:map
opened: 2026-07-22T17:53:25Z
updated: 2026-07-22T19:53:04Z
author: simongonzalezdc
comments_imported: 0
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Wayfinder: Safe Coverage Continuity Track

## Destination

Reach an implementation-safe, cognitively accessible Coverage Continuity Track whose product, privacy, evidence, and release decisions are clear enough to manage a private longitudinal insurance case without leaking PHI or creating external commitments.

## Notes

Domain: local-first health administration and coverage continuity.

Standing rules:
- The specification is [Spec: Local-first Coverage Continuity Track](spec-local-first-coverage-continuity-track.md).
- HealthAdvocate prepares, explains, tracks, and drafts; official county, carrier, marketplace, pharmacy, and provider sources remain authoritative.
- No payment, submission, withdrawal, plan selection, cancellation, message, or treatment change without explicit human action outside the first release.
- Do not import a real case until the safety release gate is resolved.
- Refer to issues by linked title, not bare issue number.

## Decisions so far

- [Define the Coverage Case domain and provenance semantics](decisions/70-define-the-coverage-case-domain-and-provenance-semantics.md) — Coverage Case is the aggregate root; Continuity Targets, immutable Evidence Items, append-only Contact Events, explicit Fact Status values, and a draft -> active -> needs-review -> blocked -> closed lifecycle are now the canonical domain model.

- [Validate private case storage and key management](decisions/71-validate-private-case-storage-and-key-management.md) — encrypted local SQLite with a Keychain-backed master key is the right privacy boundary, but migration and recovery need an explicit policy because ThisDeviceOnly-style keychain items do not migrate.

- [Choose the fully open evidence and runtime integration boundary](decisions/78-choose-the-fully-open-evidence-and-runtime-integration-boundary.md) — use a safety/evidence spine and manual fallback; admit only open, self-hostable sources under narrow claim contracts, and reject proprietary or clinically overreaching dependencies.

- [Prove PHI isolation across runtime and model boundaries](decisions/72-prove-phi-isolation-across-runtime-and-model-boundaries.md) — default listeners and model destinations are loopback-only and fail closed; a central Privacy Boundary deidentifies fully assembled model input with explicit success/no_pii_found/failed status; logs omit raw PHI.

- [Design the external Commitment Gate state machine](decisions/73-design-the-external-commitment-gate-state-machine.md) — prohibited payment/submit/withdraw/plan/cancel/message/treatment intents return blocked or review_required with zero side effects; unknown intents default to review_required.

- [Design the low-energy Coverage screen and script workflow](decisions/74-design-the-low-energy-coverage-screen-and-script-workflow.md) — one primary next action, distinct risk states, deterministic county/provider/billing/pharmacy scripts, keyboard and 400% zoom friendly.

- [Define provider and medication continuity evidence](decisions/75-define-provider-and-medication-continuity-evidence.md) — NPPES is identity-only; NADAC is acquisition benchmark; RxNorm CPC identity only; conflicts stay conflicted; no clinical or network overclaims.

- [Define case import, export, redaction, and deletion](decisions/76-define-case-import-export-redaction-and-deletion.md) — private vs redacted export, residual-risk warning, delete app-owned data only, unowned sources reported not deleted, real import disabled until release gate.

- [Set the release gate for importing a real coverage case](decisions/77-set-the-release-gate-for-importing-a-real-coverage-case.md) — real-case import requires full HA-E* receipts, independent verifier approval, and explicit override; default remains disabled.

## Not yet specified

- Whether later releases should support authenticated local-network or tailnet access.
- How the Coverage Track should relate to the existing in-memory Family and Health Tracks features after the private case model is proven.
- Whether a future cloud or multi-user edition is desirable enough to justify a separate compliance architecture.

## Out of scope

- External portal automation, payments, plan selection, cancellation, message sending, diagnosis, prescribing, and treatment changes.
- A public or multi-user PHI deployment in this effort.
- Treating remembered eligibility, provider, formulary, or pricing data as current truth.
