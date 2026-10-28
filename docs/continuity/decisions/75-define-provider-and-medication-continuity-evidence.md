---
source: GitHub mirror simongonzalezdc/healthadvocate issue #75 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/75
title: "Define provider and medication continuity evidence"
state_at_import: closed
labels: wayfinder:grilling
opened: 2026-07-22T17:53:43Z
updated: 2026-07-22T19:48:56Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Define provider and medication continuity evidence

## Question

What evidence, freshness, conflict, risk, and verification rules must a Continuity Target use so provider participation and medication coverage are never overclaimed?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:48:54Z)

## Decision: Provider and medication continuity evidence

### Decision
Continuity Targets carry separate claim classes. Evidence may upgrade only the claims it is permitted to make. Conflicts stay `conflicted` until qualifying evidence resolves them.

### Medication rules
- RxNorm CPC: identity/codes only — never safety, dose, interaction, coverage
- DailyMed / openFDA: dated label/recall/shortage evidence only — no individualized advice or causation
- DrugCentral: attributed structured facts with share-alike notice — not clinical clearance
- NADAC: acquisition-cost benchmark only — never patient cash/insured/coupon price
- User pharmacy quotes: separate fact class with observed date; never merged into NADAC

### Provider rules
- NPPES: identity + taxonomy only
- Never from NPPES: network participation, licensure status, availability, quality, appointment access
- Network status requires direct plan/provider/user contact evidence

### Freshness / conflict
- Each fact has freshness policy and observed/retrieved dates
- Conflicting active evidence → `conflicted` + verification task
- Stale sources remain visible with `stale` status; last-known-good preserved on failed updates

### Forbidden
- Diagnosis, interaction clearance, dose selection, treatment change
- Presenting NADAC as checkout price
- Presenting NPPES match as in-network

Closes fog for issue 75.
