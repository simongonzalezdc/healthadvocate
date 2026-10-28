---
source: GitHub mirror simongonzalezdc/healthadvocate issue #70 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/70
title: "Define the Coverage Case domain and provenance semantics"
state_at_import: closed
labels: wayfinder:grilling
opened: 2026-07-22T17:53:28Z
updated: 2026-07-22T18:00:10Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Define the Coverage Case domain and provenance semantics

## Question

What are the exact domain entities, relationships, lifecycle states, Fact Status transitions, and invariants needed for a Coverage Case to distinguish verified evidence from user reports, inference, unknowns, and stale information?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T17:59:49Z)

Decision: Coverage Case is the aggregate root. Continuity Targets are providers or medications. Evidence Items are immutable and dated. Contact Events are append-only. Fact Status values are verified, user-reported, inferred, unknown, and stale. Lifecycle is draft -> active -> needs-review -> blocked -> closed. User-reported facts stay separate from verified evidence and never authorize any payment, submission, plan selection, cancellation, message, or treatment change without a Commitment Gate review.
