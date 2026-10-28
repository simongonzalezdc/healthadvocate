---
source: GitHub mirror simongonzalezdc/healthadvocate issue #79 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/79
title: "Gate every shipped artifact by open license and provenance"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:34Z
updated: 2026-07-22T19:34:50Z
author: simongonzalezdc
comments_imported: 2
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Gate every shipped artifact by open license and provenance

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Make the exact shipped build self-auditing: application packages, model runtimes, model artifacts, and datasets are inventoried separately, attribution is generated, and an unknown or incompatible artifact fails the build.

## Acceptance criteria

- [ ] The shipped build produces four separate inventories with source, version, license, provenance, checksum policy, and approval result.
- [ ] Approval of a runtime does not approve model weights, tokenizers, templates, conversions, quantizations, or datasets.
- [ ] Unknown, proprietary, paid-only, hosted-only, noncommercial, or incompatible artifacts fail the build.
- [ ] The manual Coverage workflow remains usable without a model or optional dataset.
- [ ] Tests use synthetic fixtures and generated receipts contain no real PHI.

## Blocked by

None — can start immediately.

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:30:10Z)

## Claimed

Starting implementation of the open license/provenance gate (issue 79).

Scope:
- Four separate artifact inventories (packages, model runtimes, model artifacts, datasets)
- Machine-readable allowlist with fail-closed approval
- Attribution generation and synthetic-fixture tests
- No real PHI, no external commitments, no model/dataset hard dependency for core path

Working branch: master (local only; no push).

### Comment 2 — simongonzalezdc (2026-07-22T19:34:49Z)

## Completion receipt — issue 79

### Changed modules
- `healthadvocate/governance/` — registry, inventory builders, fail-closed gate, attribution + receipt writers, CLI (`python -m healthadvocate.governance`)
- `healthadvocate/governance/data/artifact_registry.json` — audited packages, model runtimes, model artifacts, datasets; denylist for GoodRx/LM Studio/etc. (issue 78)
- `healthadvocate/coverage/__init__.py` — public manual-workflow status (no model/dataset hard dependency)
- `tests/test_license_provenance_gate.py` — behavior tests
- `.github/workflows/ci.yml` — license gate step
- `.gitignore` — ignore generated `build/` receipts

### Tests (exact)
```
python3 -m pytest tests/ -v
18 passed
```

Narrow gate CLI:
```
python3 -m healthadvocate.governance --project-root . --out build/receipts/license
result=pass evidence_id=HA-E78
```

### Acceptance criteria mapping
| Criterion | Evidence |
|---|---|
| Four separate inventories with source/version/license/provenance/checksum/approval | `inventory-*.json` under `build/receipts/license`; tests assert all four kinds |
| Runtime approval does not approve model artifacts/datasets | `cross_inventory_rules` false in gate report; no shipped model artifacts approved |
| Unknown/proprietary/paid-only/hosted-only/noncommercial/incompatible fail | unit tests + unregistered requirement fails build |
| Manual Coverage workflow usable without model or optional dataset | `manual_workflow_status()` + inventory required flags all false |
| Synthetic fixtures; receipts contain no real PHI | canary scan on all receipts; `contains_real_phi: false` |

### License/source evidence
- Core packages inventoried from `requirements.txt` + app MIT license file
- Optional adapters (RxNorm CPC, DailyMed, openFDA, DrugCentral, NADAC, NPPES) listed as `not_shipped`
- Explicit denylist: GoodRx, LM Studio (catalog evidence only; does not fail gate)
- Commit: `611f523` (local only; not pushed)

### Remaining risks
- Versions are requirement pins (`>=x`), not lockfile hashes; strengthen when a lockfile is introduced
- Model runtimes (llama.cpp/Ollama) are approved as candidates but not pinned/shipped yet
- README still says Apache-2.0 while `LICENSE` is MIT — pre-existing inconsistency, not fixed in this ticket
- Branch is behind `origin/master` by 7 commits; local commit not rebased/pushed

### Proof: no real PHI / external commitment
- Registry and receipts are package metadata only
- No payments, submissions, messages, plan changes, or real-case import
- Synthetic canaries only in tests

Closing as all criteria have behavioral evidence.
