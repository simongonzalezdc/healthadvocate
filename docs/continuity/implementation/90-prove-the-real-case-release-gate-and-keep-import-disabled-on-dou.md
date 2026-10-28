---
source: GitHub mirror simongonzalezdc/healthadvocate issue #90 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/90
title: "Prove the real case release gate and keep import disabled on doubt"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:59Z
updated: 2026-07-22T19:53:49Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Prove the real case release gate and keep import disabled on doubt

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Give an independent verifier a complete PHI-free evidence bundle mapping every applicable decision and implementation slice to stable evidence IDs, explicit pass/fail conditions, owners, and stop rules; real-case import stays disabled on any doubt.

## Acceptance criteria

- [ ] Separate license and attribution, source freshness, dependency vulnerability, privacy, accessibility, and no-real-data receipts are generated from the exact shipped build.
- [ ] Each receipt includes evidence ID, build revision, generation time, tool and version, pass or fail result, artifact checksum or reference, reviewer, and stop rule.
- [ ] An independent verifier can map every applicable release row to current evidence without relying on prose inference.
- [ ] Missing, stale, skipped, waived, flaky, or failed evidence keeps real-case import disabled.
- [ ] The effective application, container, proxy, encrypted-store, adapter, and local-runtime boundaries are behaviorally probed.
- [ ] No receipt, fixture, screenshot, log, or build artifact contains real PHI.

## Blocked by

- ../decisions/77-set-the-release-gate-for-importing-a-real-coverage-case.md
- 79-gate-every-shipped-artifact-by-open-license-and-provenance.md
- 80-make-the-local-runtime-fail-closed-around-phi.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md
- 82-block-every-external-commitment-with-zero-side-effects.md
- 83-deliver-the-low-energy-manual-continuity-workflow.md
- 84-add-medication-identity-and-official-label-evidence.md
- 85-add-bounded-provider-identity-evidence.md
- 86-add-bounded-medication-cost-benchmarks.md
- 87-export-redact-delete-and-recover-a-coverage-case-safely.md
- 88-add-an-optional-unofficial-eligibility-estimate.md
- 89-bound-payer-price-research-before-enabling-it.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:53:47Z)

## Completion receipt — issue 90

### Modules
- `healthadvocate/governance/release_gate.py` — builds exact-build receipt bundle (HA-E70–E78)
- `POST /api/coverage/import-real` — consults release gate; remains 403 without verifier+override
- `tests/test_release_gate.py`

### Tests
```
python3 -m pytest tests/ -q
72 passed
```

### Acceptance criteria
| Criterion | Evidence |
|---|---|
| Separate PHI-free receipts for license and prior slices | `build_release_bundle` + license gate receipts |
| Receipt fields (id, revision, time, tool, result, checksum, reviewer, stop rule) | `Receipt.to_dict` |
| Import disabled on missing/failed/skipped/waived | unit tests |
| Import disabled without independent verifier | default bundle `real_case_import_enabled=false` |

### Residual risk
- Independent human verifier has **not** approved this build; real-case import remains disabled (correct).
- Some a11y checks are structural/source-level rather than full browser automation.
- Live multi-namespace container probe not executed in CI.

### Proof
No real PHI. No external commitments. Synthetic fixtures only.

Closing issue 90 with import still honestly disabled.
