---
source: GitHub mirror simongonzalezdc/healthadvocate issue #74 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/74
title: "Design the low-energy Coverage screen and script workflow"
state_at_import: closed
labels: wayfinder:prototype
opened: 2026-07-22T17:53:39Z
updated: 2026-07-22T19:46:02Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Design the low-energy Coverage screen and script workflow

## Question

What should the Coverage screen and its county, provider, billing, and pharmacy script flows look and behave like for an anxious user who needs one clear action at a time?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:46:01Z)

## Decision: Low-energy Coverage screen and script workflow

### Decision
Ship one Coverage screen with a single primary next action, progressive disclosure for secondary evidence, plain-language status chips, and deterministic scripts. No model required.

### Screen structure (top → bottom)
1. **Case title + lifecycle chip**
2. **One primary next action** (single prominent button/region; never two equal primaries)
3. **Risk strip**: approaching / overdue / unknown / stale / conflicted — visually and semantically distinct
4. **Continuity targets** (providers, medications) collapsed by default
5. **Evidence + contact history** expandable
6. **Script picker**: County | Provider | Billing | Pharmacy — one script at a time

### Script rules
- Deterministic templates from reviewed facts only
- Unknown fields render as `[unknown]` — never invented
- One question/decision per step in multi-step scripts
- Scripts prepare speech only; Commitment Gate still blocks send/pay

### Accessibility
- Keyboard complete; visible focus; logical order
- Live region for errors/status
- Usable at 400% zoom without required horizontal page scroll
- `prefers-reduced-motion` respected
- Plain-language labels for unknown/stale/conflicted/review required

### Alternatives
- Dense dashboard with many CTAs: rejected (cognitive load)
- Chat-first generative coach: rejected for core path

### Downstream
Issue 83 implements this UI + script generator with a11y checks.

Closes fog for issue 74.
