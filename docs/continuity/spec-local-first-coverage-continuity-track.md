---
source: GitHub mirror simongonzalezdc/healthadvocate issue #68 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/68
title: "Spec: Local-first Coverage Continuity Track"
state_at_import: open
labels: ready-for-agent
opened: 2026-07-22T17:53:22Z
updated: 2026-07-22T19:18:07Z
author: simongonzalezdc
comments_imported: 0
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Spec: Local-first Coverage Continuity Track

## Problem Statement

A person losing employer health coverage must coordinate eligibility, deadlines, documents, county calls, providers, prescriptions, bills, and fallback options while under financial and emotional pressure. HealthAdvocate can explain documents and organize health information, but its current runtime and model boundaries are not strong enough for a real longitudinal coverage case, and its existing medical-assistance surfaces can imply more clinical certainty than the underlying evidence supports.

The user needs one calm, private place that identifies the next safe action, protects provider and medication continuity, distinguishes verified facts from uncertain claims, uses only fully free and open components in the core path, and prevents any payment, submission, plan selection, cancellation, message, or treatment change without explicit human review.

## Solution

Build a local-first Coverage Continuity Track around an encrypted Coverage Case. It will organize deadlines, Continuity Targets, Evidence Items, Contact Events, Prepared Scripts, and external-verification tasks. It will show one primary next action, label every material fact by Fact Status, provenance, and freshness, and enforce a Commitment Gate before anything with an external, financial, coverage, communication, or clinical consequence.

The first usable path is a manual evidence workflow. Narrow open-data adapters may later normalize official evidence, but each adapter has explicit permitted and forbidden claims. The product remains an evidence-and-continuity assistant, not an AI doctor, eligibility authority, provider-network directory, live pharmacy quote, or autonomous insurance agent.

The shipped core uses only auditable free/open software and appropriately licensed public/open data. Proprietary, paid-only, hosted-only, noncommercial, or source-available-but-not-open dependencies are excluded from the core path.

## User Stories

1. As a person losing employer coverage, I want one Coverage Case, so that I do not reconstruct my situation across emails, portals, and notes.
2. As an overwhelmed user, I want one clearly ranked next action, so that I can make progress without processing the whole case at once.
3. As an anxious user, I want short scripts written in plain language, so that I can complete difficult calls.
4. As a user with cognitive accessibility needs, I want one question or decision at a time, so that the interface does not increase my stress.
5. As a keyboard user, I want the critical workflow to work without a mouse, so that I can complete it with my preferred input method.
6. As a low-vision user, I want the critical workflow to remain usable at 400% zoom, so that information and actions remain available.
7. As an applicant, I want application and case identifiers stored privately, so that I can retrieve them without exposing them in source control or logs.
8. As an applicant, I want submission dates, offices, workers, and confirmation details recorded, so that follow-up is accurate.
9. As an applicant, I want document-request deadlines highlighted, so that I do not lose eligibility through an avoidable missed deadline.
10. As a former employee, I want COBRA dates and status separated from assumptions, so that an unverified portal state is not presented as coverage.
11. As a marketplace shopper, I want special-enrollment dates tied to dated evidence, so that the system does not guess a deadline.
12. As a Medi-Cal applicant, I want pending, approved, denied, and needs-information states represented clearly, so that I know what follow-up is appropriate.
13. As a patient, I want each current provider listed as a Continuity Target, so that no essential relationship is forgotten.
14. As a patient, I want each provider's identity, network status, availability, and licensure represented as separate claims, so that one kind of evidence is not mistaken for another.
15. As a patient, I want visit cadence and next-appointment risk recorded, so that continuity work is prioritized by urgency.
16. As a patient, I want cash, hardship, delayed-billing, and payment-plan information recorded without authorizing it, so that I can compare bridge options safely.
17. As a patient using maintenance medication, I want each medication represented as a Continuity Target, so that refill risk is visible.
18. As a patient, I want prescriber, pharmacy, refill date, formulary evidence, and authorization restrictions recorded, so that coverage problems do not remain hidden.
19. As a patient, I want medication identity normalized without changing my treatment, so that evidence from different sources can be compared safely.
20. As a patient, I want official label, recall, and safety evidence dated and sourced, so that I can take questions to a clinician or pharmacist.
21. As a patient, I want the product to refuse diagnosis, interaction, dosage, causation, and treatment verdicts, so that administrative help is not mistaken for medical care.
22. As a patient, I want price benchmarks clearly separated from pharmacy cash quotes and insured prices, so that I understand what a number can and cannot tell me.
23. As a user, I want screenshots, PDFs, emails, notices, and call notes represented as Evidence Items, so that important claims can be traced.
24. As a user, I want each Evidence Item to show its source, observation date, retrieval date, and checksum where applicable, so that stale or changed evidence is visible.
25. As a user, I want each material fact labeled verified, user-reported, inferred, unknown, stale, or conflicted, so that confidence is never implied.
26. As a user, I want conflicting evidence preserved instead of silently overwritten, so that I can resolve it with the authoritative source.
27. As a caller, I want a deterministic county-interview script generated from reviewed facts, so that I do not have to improvise.
28. As a patient, I want a deterministic provider-continuity script, so that I can ask the right network and continuity questions.
29. As a patient, I want a deterministic billing and cash-price script, so that I can request options without agreeing to a charge.
30. As a patient, I want a deterministic pharmacy and refill-bridge script, so that I can address medication risk without changing treatment.
31. As a user, I want unknown values left blank or marked unknown, so that the system never invents an answer.
32. As a user, I want any payment action blocked by a Commitment Gate, so that the system cannot spend money.
33. As a user, I want submissions, withdrawals, selections, cancellations, and messages blocked by a Commitment Gate, so that preparation cannot become an unintended external action.
34. As a patient, I want treatment and medication changes blocked by a Commitment Gate, so that the tool cannot alter care.
35. As a privacy-conscious user, I want the application, container, proxy, and model endpoints restricted to loopback by default, so that sensitive information stays on my machine.
36. As a privacy-conscious user, I want ambiguous, redirected, or non-loopback model destinations rejected, so that configuration tricks cannot silently move my data.
37. As a privacy-conscious user, I want the fully assembled model input deidentified, so that profile and evidence context cannot bypass the privacy boundary.
38. As a privacy-conscious user, I want deidentification failures to stop model processing, so that failure cannot be mistaken for successful scrubbing.
39. As a privacy-conscious user, I want the core workflow to function without any model, so that evidence and continuity do not depend on generative AI.
40. As a user, I want case data encrypted outside the source repository, so that development and Git operations cannot publish it accidentally.
41. As a user, I want private and redacted export modes, so that I control which identifiers leave the case store.
42. As a user, I want redaction limitations stated plainly, so that automated redaction is not presented as a guarantee.
43. As a user, I want a clear deletion operation, so that I can remove the local case and application-owned derived artifacts.
44. As a user, I want unowned source files identified during deletion, so that the product does not falsely claim to delete data it does not control.
45. As a returning user, I want the case to survive application restarts, so that multi-week coverage work is durable.
46. As a user, I want a Contact Event timeline with names, reference numbers, promises, and next steps, so that follow-up is accountable.
47. As a user, I want overdue and approaching risks separated, so that I can focus on what can still be saved.
48. As a user, I want official-source links and verification actions beside estimates, so that unofficial assistance leads back to authoritative decisions.
49. As a user, I want provider identity evidence clearly labeled as identity-only, so that it is not mistaken for network participation or licensure.
50. As a user, I want acquisition-cost benchmarks clearly labeled, so that they are not mistaken for my retail price.
51. As a user, I want optional eligibility estimates to show rule version, assumptions, and missing facts, so that they are not mistaken for official eligibility.
52. As a maintainer, I want each evidence adapter to declare permitted and forbidden claims, so that data access does not become product overclaiming.
53. As a maintainer, I want failed data updates quarantined while the last-known-good snapshot remains available and marked stale, so that upstream drift fails safely.
54. As a maintainer, I want application packages, model runtimes, model artifacts, and datasets inventoried separately, so that approval of one cannot approve another.
55. As a maintainer, I want every shipped artifact to have license, provenance, version, and attribution evidence, so that the open-source-only boundary is enforceable.
56. As a maintainer, I want an unknown or incompatible artifact to fail the build, so that proprietary dependencies cannot enter through convenience.
57. As a maintainer, I want external adapters replaceable with fakes, so that tests never contact insurers, providers, pharmacies, or government systems.
58. As a maintainer, I want logs, errors, screenshots, fixtures, and build artifacts free of real PHI, so that diagnostics do not create another disclosure path.
59. As a reviewer, I want each release decision mapped to a stable evidence receipt, explicit pass/fail condition, owner, and stop rule, so that release approval is auditable.
60. As a reviewer, I want real-case import disabled whenever evidence is absent, stale, skipped, waived, flaky, or failed, so that uncertainty fails closed.
61. As a maintainer, I want current HealthAdvocate routes covered by regression behavior, so that the Coverage Track is additive and any deprecation is explicit.
62. As a maintainer, I want one audited open local runtime tested through the same model contract, so that runtime portability is proven without approving any model weights implicitly.

## Implementation Decisions

- Use the canonical domain terms Coverage Case, Continuity Target, Evidence Item, Contact Event, Fact Status, Risk Date, Prepared Script, Source Registry, and Commitment Gate.
- Treat Coverage Case as the aggregate root. It owns case lifecycle, next action, risk dates, continuity targets, evidence references, contact history, prepared scripts, and verification tasks.
- Use the resolved case lifecycle and provenance invariants from the Wayfinder decision map. Evidence Items are immutable; Contact Events are append-only; corrections create new evidence or events rather than rewriting history.
- Every material claim carries a typed claim class, Fact Status, source/provenance, observation or retrieval date, and freshness policy.
- Official county, carrier, marketplace, pharmacy, clinician, and provider sources remain authoritative. The application organizes evidence and prepares verification; it does not adjudicate eligibility, coverage, network participation, formulary status, licensure, diagnosis, or treatment.
- Persist cases in encrypted local SQLite outside the repository with a key stored in the operating-system credential store. Missing or incorrect keys fail before case metadata is returned.
- Keep the default application, container, proxy, and model boundaries on loopback. Non-loopback deployment is not part of this specification and must not be enabled by an accidental configuration change.
- Validate resolved model destinations, redirects, IPv4/IPv6 forms, and DNS ambiguity. Failure prevents a model call.
- Deidentify the fully assembled model input, not only the user's primary text. Distinguish success, no-PII-found, and failure; failure blocks processing.
- The manual Coverage workflow functions without a model. Use deterministic templates for county, provider, billing, pharmacy, and Commitment Gate scripts.
- A local model may assist with retrieval-linked summarization or simplification after the privacy gate, but it cannot create Evidence Items, upgrade Fact Status, authorize a commitment, or issue a clinical verdict.
- Use one primary Coverage screen with one primary next action and clear sections for deadlines, providers, medications, evidence, contacts, and prepared scripts.
- Add review-only Commitment Gate behavior for payment, submission, withdrawal, plan selection, cancellation, messaging, and treatment-change intents. The first release contains no capable outbound adapter for those actions.
- Maintain a Source Registry and four independent shipped-artifact inventories: application/runtime packages, model runtimes, model artifacts, and datasets. Approval never transfers between inventories.
- Require an auditable acceptable license, provenance, version pin, source, checksum policy, permitted claims, forbidden claims, and attribution for each shipped component or dataset.
- Admit RxNorm Current Prescribable Content for public-domain medication normalization; do not treat approval as approval of full RxNorm or a complete RxNav distribution.
- Admit DailyMed bulk SPL for official label evidence and openFDA for dated public regulatory evidence. Adverse-event reports are not proof of causation.
- Admit DrugCentral under its attribution/share-alike terms for reference evidence.
- Admit CMS NADAC only as an acquisition-cost benchmark, never a retail or insured patient price.
- Admit CMS NPPES only as provider identity data, never as proof of licensure, network participation, availability, or quality.
- Permit PolicyEngine US only behind an optional feature flag as an unofficial estimate that displays rule version, assumptions, missing inputs, and official verification action.
- Keep CMS Transparency in Coverage analysis disabled until representative public samples have measured storage, compute, and duration budgets. Negotiated rates do not establish guaranteed patient price or provider network status.
- Use open document extraction/redaction components only as assistive tools. OCR and automated redaction are probabilistic and require review before sharing.
- Reject GoodRx, Primary Intelligence/VoxCura, hosted medical-reasoning products, paid/closed provider-price APIs, LM Studio as a required core dependency, and proprietary/noncommercial/source-available model artifacts.
- Permit an audited llama.cpp or Ollama runtime through a replaceable local model contract. Select and approve model artifacts separately.
- Preserve existing product routes or deprecate them explicitly with migration and regression evidence. Remove or rewrite claims that present generative medical output as independently verified or safe to share.
- Keep real-case import disabled until an independent verifier approves all applicable release receipts. Planning approval does not authorize implementation or real-data use.

## Testing Decisions

- Use one primary behavior seam: exercise the public Coverage API and critical browser workflow with a temporary encrypted store, synthetic cases, a fake model, fake source adapters, and a recorded outbound boundary.
- Use one release-audit seam for facts the public workflow cannot prove: inspect and probe the effective shipped runtime, listener/proxy configuration, encrypted artifacts, license inventories, attribution, logs, and generated reports.
- Prefer external behavior over tests bound to private classes, SQL text, prompt wording, or frontend implementation details.
- Through the primary seam, verify case creation, updates, restart persistence, risk ordering, Fact Status transitions, conflicts, provenance, continuity targets, deterministic scripts, review states, exports, redaction warnings, deletion, and recovery behavior.
- Verify that unknown facts remain unknown and model drafts cannot create evidence, upgrade status, or satisfy a Commitment Gate.
- Verify that every prohibited commitment produces a blocked/review result and zero external side effects.
- Verify default loopback behavior for the application, container, proxy, and model runtime by starting the effective deployment and probing it from loopback and a non-loopback test namespace.
- Verify rejection of redirects, ambiguous DNS, IPv4/IPv6 variants, and non-loopback model destinations.
- Seed synthetic canary identifiers through user text, profile context, evidence metadata, exception paths, and model responses; confirm none appear in logs, errors, screenshots, exports, temporary files, build artifacts, or unauthorized model requests.
- Verify that encrypted storage contains no plaintext canaries in database bytes, journals, temporary files, backups, or crash artifacts.
- Verify missing/wrong-key failure, key rotation, recovery, private export, redacted export, deletion, and unowned-source reporting.
- Run adapter contract tests against pinned normal, stale, malformed, missing, duplicate, conflicting, and schema-changed fixtures. A failed update must quarantine the candidate and preserve the last-known-good snapshot with honest freshness.
- Verify each adapter's forbidden claims: NPPES cannot verify network or licensure; NADAC cannot state patient price; openFDA cannot state causation; eligibility estimates cannot state official eligibility.
- Verify that each optional adapter can be disabled without breaking the manual Coverage workflow.
- Verify keyboard navigation, focus order, error announcement, one-primary-action hierarchy, reduced motion, and 400% zoom for the critical Coverage flow.
- Generate separate license/attribution, source-freshness, dependency-vulnerability, and no-real-data receipts. Each receipt records evidence ID, build revision, generation time, tool/version, pass/fail result, checksum or artifact reference, reviewer, and stop rule without real PHI.
- Test one audited pinned open local runtime through the same replaceable model contract. Runtime approval must not approve the model artifact loaded into it.
- Keep all tests synthetic and network-denied unless a narrowly scoped public-fixture update job is being run. No test may load the user's real coverage or medical information.
- Use the existing presentation and route tests as regression prior art, but replace source-text assertions with behavior-level proof where the new seams allow it.

## Out of Scope

- Submitting or withdrawing BenefitsCal, Medi-Cal, Covered California, COBRA, or other applications.
- Selecting, accepting, changing, or canceling a health plan.
- Paying premiums, medical bills, prescription costs, or self-pay charges.
- Sending emails, portal messages, appeals, forms, or provider communications.
- Diagnosing, prescribing, changing medication, calculating dose, deciding interactions, or recommending treatment changes.
- Claiming current eligibility, coverage, formulary status, provider network participation, licensure, availability, patient price, or adverse-event causation without qualifying authoritative evidence.
- Scraping authenticated insurer, government, provider, pharmacy, or discount-card portals.
- Integrating GoodRx, Primary Intelligence, hosted medical-reasoning tools, or any proprietary, paid-only, noncommercial, or hosted-only core dependency.
- A public, cloud, multi-user, local-network, or tailnet PHI deployment.
- Treating OCR, automated redaction, local-model output, or public datasets as independent clinical verification.
- Importing a real case before the independent release gate passes.

## Further Notes

The feature exists to reduce cognitive load and protect provider and medication continuity, not to maximize automation. The no-payment, no-commitment, no-treatment-change posture is a product requirement.

Eligibility rules, deadlines, provider participation, drug formularies, datasets, model licenses, and prices change. Store source dates and versions; never encode remembered values as timeless product truth.

The strongest safe fallback is a manual-evidence-only release. Open adapters are optional enhancements and must never become prerequisites for the basic continuity workflow.

The canonical decision map remains [Wayfinder: Safe Coverage Continuity Track](wayfinder-safe-coverage-continuity-track.md). All implementation tickets must honor its unresolved decisions and the independent real-case release gate.
