---
source: GitHub mirror simongonzalezdc/healthadvocate issue #78 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/78
title: "Choose the fully open evidence and runtime integration boundary"
state_at_import: closed
labels: wayfinder:research
opened: 2026-07-22T18:27:26Z
updated: 2026-07-22T18:36:38Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Choose the fully open evidence and runtime integration boundary

Part of the Safe Coverage Continuity Track.

## Question

Which medication, provider, price, eligibility, document-processing, storage, and local-inference integrations are genuinely free and open, what claims can each support, and which closed, licensed, hosted, or clinically unsafe alternatives must be excluded?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T18:36:37Z)

Decision: build the open integration layer on a safety/evidence spine with a complete manual-evidence fallback. Approved core sources are RxNorm Current Prescribable Content, DailyMed bulk SPL, openFDA, DrugCentral CC BY-SA 4.0, CMS NADAC, and CMS NPPES; approved support tooling includes Docling, Tesseract, Presidio, SQLCipher, DuckDB, Synthea, and llama.cpp/Ollama with a separately audited OSI-compatible model. PolicyEngine US and CMS Transparency in Coverage remain conditional, late-stage adapters. Each adapter must enforce narrow claim classes: NPPES is identity rather than network/licensing proof; NADAC is an acquisition-cost benchmark rather than a retail price; OCR/redaction remain probabilistic; adverse-event reports do not establish causation; local models cannot diagnose, triage, select doses, or clear interactions. Reject GoodRx, Primary Intelligence/VoxCura, Ada, Solace, OpenEvidence, licensed NeedyMeds data, LM Studio, full RxNorm/RxNav-in-a-Box, and proprietary, noncommercial, hosted-only, partnership-gated, or merely source-available model/API dependencies.
