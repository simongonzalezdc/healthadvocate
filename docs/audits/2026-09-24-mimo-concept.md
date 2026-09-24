<!-- PROVENANCE:
Model: Xiaomi MiMo mimo-v2.6-pro (official Token Plan, token-plan-sgp.xiaomimimo.com/v1) via pushing-dispatch executor xiaomi-mimo.
Lane fix 2026-09-24: wrapper xiaomi-mimo-v26.sh now runs a structured-tool agent loop (bash/read_file/write_file/todowrite, OpenAI tool-calling) instead of the stock single-shot ce_run_openai_compatible completion, which could never terminate agentic MiMo runs with the required 'Status:' token (exit 4 'missing terminal status token').
Worker: w-4271-ha-audit-concept-mimo (11 turns, tokens_in 291835 / tokens_out 16596, state=done exit=0, read-only, worktree left clean).
-->
# HealthAdvocate Concept/Product-Design Red-Team — 2026-09-24

Scope: product questions only (mission, user, scope, maturity, ethics, fail-closed UX, positioning, roadmap, missing concepts). Evidence = file:line or verbatim quotes from this tree. No code judged on quality; no fixes proposed in findings.

---

## A. Mission & user

**A1 — CRITICAL: The product's own policy forbids its target user's actual use.**
README:32 sells "Understand what your symptoms might mean" to people "at your most vulnerable" (README, The Problem). But `docs/THREAT-MODEL.md:22`: "Real PHI typed into free-text surfaces is processed with no gate … Until the real-case era, treat every text box as synthetic-only BY POLICY." The moment a real patient pastes a real denial letter, they are out of policy on the product's core surfaces. This is the synthetic-only/art-piece question answered at the concept level: today HealthAdvocate cannot lawfully (by its own law) receive the problem it exists to solve.

**A2 — HIGH: Install burden selects exactly the wrong user.**
Quick Start requires git clone, pip, LM Studio, and downloading a model (README:122 "Download a medical model like Meditron3-8B"; README:141). The user described in The Problem — sick, overwhelmed, in a coverage gap — will not do this. The user who will (tinkerer, privacy hobbyist) is not the vulnerable patient the mission invokes. The mission's hero and the product's funnel do not overlap.

**A3 — HIGH: Two different customers in one sentence.**
README:7/417: "helps **people navigating healthcare systems and builders of advocacy tools**". The tree ships patient copy ("Fight insurance denials", README:50) next to builder artifacts (`python -m healthadvocate.mcp_server`, `skills/healthadvocate/SKILL.md`, `llms.txt`, GEO/SEO block at README:415+). A patient and an agent-tool builder need different products; the mission statement hedges, and the product inherits the hedge.

**A4 — HIGH: The one load-bearing promise ("data never leaves your machine") is unattested, and it's unclear it's the user's real constraint.**
index.html:7: "your data never leaves your device." vs `docs/THREAT-MODEL.md:19`: "**Assumed, not attested**: a URL check cannot see SSH forwards or proxies behind 127.0.0.1 — the live tunnel pattern … satisfies the letter while sending deidentified text off-machine." Meanwhile the domain's actual patient constraints — cost, deadlines, payer power asymmetry — are barely served (see H2/H3). Local-first privacy is a real niche (consumer LLMs are not HIPAA-covered), but this product undercuts that niche twice: the posture is unverifiable (threat model's own words), and the synthetic-only policy bans the real PHI use case the niche exists for.

---

## B. Scope breadth (focus or graveyard?)

**B1 — HIGH: 12 nav views, 9 generative features, 0 validated — the graveyard is already populated.**
index.html nav: Symptoms, Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Scanner, Family, Tracks, Coverage. Two headline features have no memory at all: README:365 "Family profiles and health tracks live in memory and are lost on server restart" — yet README:74: "Manage health profiles for your whole family … This context flows into every other feature." A Family Health Tracker that forgets your family every restart is a graveyard feature wearing a headline.

**B2 — HIGH: Depth is allocated inversely to risk.**
The deepest machinery in the tree (encrypted case store, keystore, commitment gate, governance ledger, policy receipts) serves Coverage — the low-stakes, deterministic track. The highest-stakes surface, symptom triage, is one prompt ("Assess urgency realistically", `core/symptom_assessor.py:48`) plus substring matching. Insurance gets typed decisions and receipts; your chest pain gets a temperature-0.1 completion.

**B3 — HIGH: "Cross-validation" is a product claim inflating a substring check.**
README:47: "Two AI layers … cross-validate each other to give you a reliable urgency assessment." Reality: `core/cross_validation.py:61-65` — substring matching of NER entity names against LLM field strings; reliability = overlap ratio with 0.7/0.3 cutoffs (`cross_validation.py:86-97`). Both "layers" read the same text; neither independently verifies the other's reasoning. The UI presents it as a trust badge: "Reliability" (`static/app.js:365`). Two clocks reading the same watch is not redundancy.

---

## C. Synthetic-only / pre-user state

**C1 — CRITICAL: Zero evidence for the core proposition; assurance everywhere except where it matters.**
320 test functions across `tests/` verify privacy mechanics, schema round-trips, gate legs, receipt canaries, license provenance — none verify that any output helps a patient (and by policy none can, until "the real-case era"). The measured facts in the tree are about the machinery; the product claim ("helps people navigate healthcare") is entirely unmeasured. Engineering art piece: high internal rigor, zero external contact.

**C2 — HIGH: The governance surface area exceeds the user surface area.**
`governance/` (gate.py, release_gate.py, policy_audit.py, registry.py, inventory.py) + `decisions/` (schemas, receipts, thresholds, runners, AST allowlist pin) exist to make outputs auditable — for an auditor/user base of zero. `docs/HA-JEV…:85`: every NEEDS_HUMAN "carries the numbers plus deterministic allowed_next_steps" — machinery for a compliance regime the pre-user product hasn't earned. The concept has optimized for defensibility before usefulness.

**C3 — HIGH: Three contradictory stories about what the product IS without a model.**
(1) README:147 "That's it. No sign-up, no API keys, no cloud." with a Quick Start that never sets `HEALTHADVOCATE_MODEL_ENABLED` — yet `core/llm_client.py:28-32` disables the model unless that variable (absent from README's configuration table, which lists only `LM_STUDIO_URL`, `MEDICAL_LLM_MODEL`, CORS) is set. (2) README:366: "Without it, feature endpoints return errors." (3) Actual behavior: silent success-shaped fallback (`llm_client.py:190-203`). A user following the docs lands in fallback mode where — per D2 — every symptom reads HIGH. An onboarding path that silently degrades into alarmism is a concept failure, not a docs bug.

---

## D. Health-advocacy ethics

**D1 — CRITICAL: Diagnosis-shaped output, disclaimed by prose.**
`core/llm_client.py:65`: `"possible_conditions": [{"name": "string", "likelihood": "likely or possible or unlikely"}]` — the model labels conditions "likely". README:47 sells "possible conditions". The only guardrail is a system-prompt sentence ("Never diagnose — always recommend seeing a healthcare provider.", `llm_client.py:54`) and one footer disclaimer (`index.html:431`). A patient reads "likely" as a diagnosis. When (not if) an 8B-class local model confidently mislabels a PE as "likely anxiety", the disclaimer is where liability goes to die — guardrail as liability shielding in its purest form.

**D2 — CRITICAL: The shipped default configuration cries "HIGH" at every symptom.**
Model off by default (`llm_client.py:30`) → placeholder output → below-threshold NEEDS_HUMAN (design:222 "model-blocked/unparseable placeholder outputs escalated medium→high") → `external_urgency` returns `CONSERVATIVE_URGENCY` = "high" (`decisions/symptom_triage.py:71,161-177`; pinned in `tests/test_symptom_triage_jev.py`). So "mild headache" in the documented default build yields a `urgency-high` badge (`static/app.js:327`). Fail-closed here fails toward documented domain harm: alarm fatigue, 911/ER overuse, and a user base trained to ignore the badge. A safety valve set to always-open is a stuck-open valve.

**D3 — HIGH: Drug safety computed from model memory, with a fake "verified" stamp.**
`core/drug_checker.py:21-27`: "If the patient's current medications are listed, check for drug-drug interactions" — interactions, `warnings`, `common_side_effects` all come from LLM recall (`drug_checker.py:40-49`). Meanwhile RxNorm/DailyMed/openFDA adapters exist and are wired ONLY into coverage (`app.py:533-543`). And `drug_checker.py:35` returns `ner_verified` — a name-recognition flag the UI/copy reads as verification. The highest-liability clinical surface has the least grounding in the whole product. This is the domain where "wrong-but-confident" (threat model's own phrase, `docs/THREAT-MODEL.md:24`) kills people.

**D4 — HIGH: Misinformation verdicts with zero evidence.**
README:38: "Separate real health advice from misinformation online." Reality: `core/community_health.py:47` — `"credibility": llm_output.get("credibility", "medium")`. An ungrounded local model grades ungrounded claims; no retrieval, no citations, no sources. The product hands a verdict-shaped label to a patient asking "is this true?" — epistemic theater in a domain drowning in misinformation.

**D5 — HIGH: The safety badges don't mean what patients think.**
README:113: "The `pii_scrubbed` flag in every response confirms this happened." vs `core/bill_decoder.py:75`: `"pii_scrubbed": len(pii_map) > 0` — true only when PII was FOUND and masked; if the detector finds nothing (including when it misses real PII), the flag is false or absent, and `docs/THREAT-MODEL.md:20` admits "**Recall is never measured**". A safety confirmation badge whose semantics invert its name is liability shielding sold as safety.

**D6 — MEDIUM: "Suspicious charges" and "your rights" invented without ground truth.**
README:53 "spot suspicious charges … tells you your rights as a patient." Actual input: a price regex (`bill_decoder.py:13`) and a prompt "Flag suspicious charges" (`bill_decoder.py:23`). No price benchmark, no CPT/ICD database, no jurisdiction or plan-type input — yet patient rights and overcharge accusations are state- and plan-dependent. Accusation-shaped output with no evidence base.

**D7 — MEDIUM: "Ready-to-send appeal letter" is an outcome promise on a prep product.**
README:50: "generates a ready-to-send appeal letter you can take straight to your insurer." Real appeals turn on filing deadlines, ERISA vs fully-insured routes, external-review windows, and record citations — none are inputs to `insurance_fighter`. A "ready-to-send" letter that misses the appeal window is worse than no letter, and the product owns none of that clock (see H2).

---

## E. Fail-closed philosophy (usable, or a machine for "ask a human"?)

**E1 — CRITICAL: The machine generates "ask a human" — into a log nobody reads.**
`NEEDS_HUMAN` and `allowed_next_steps` (design:85; `coverage/commitment_gate.py:159`) appear NOWHERE in `static/app.js` or `app.py` (grep: zero hits). The typed-decision layer's entire patient-facing payload — "you need a human, here are the allowed next steps" — is emitted as audit JSON and discarded at the glass. What the patient sees is the escalated HIGH badge (`app.js:327`). The fail-closed philosophy, as a UX concept, is fail-SILENT: the one instruction the product is sure about is the one it never shows.

**E2 — HIGH: NEEDS_HUMAN names no human.**
`decisions/assess.py` FAIL_CLOSED_SENTENCE (pinned equal to the gate's blocked sentence, `commitment_gate.py:134`): "…requires a human decision outside this application." But the product ships no directory of humans: no state DOI, no hospital patient advocate, no CMS navigator, no legal aid, no suicide hotline surfaced on the symptom surface. In this domain "which human, what number, by when" is the entire value of the referral; "outside this application" is a shrug with schema fields.

---

## F. Positioning vs existing patient-advocacy services

**F1 — HIGH: vs human advocates/navigators — the copy promises the advocate, the product delivers the pamphlet.**
Hospital patient advocates, CMS/state marketplace navigators, and insurer case managers can actually call the payer, escalate, and hold deadlines. HealthAdvocate's outputs are worksheets (talking points, scripts, drafts). The brand ("Your Health Deserves an Advocate", hero) promises the function humans provide; the Commitment Gate has by design "no capable outbound adapter" (README, Privacy section). Prep-tool positioning would be honest; advocate positioning invites the comparison it loses.

**F2 — MEDIUM: vs general LLM assistants — the differentiation is cancelled by the product's own gates.**
Against zero-install frontier chat assistants, HA offers privacy + guardrails at the cost of a much weaker model and heavy install (A2). But the defensible niche — "give real PHI to a local model safely" — is precisely what the synthetic-only policy forbids (A1), and the privacy delta is unattested (A4). Against dedicated tools (cost lookups, appeal services, official charity-care help), it has breadth but no ground truth in any single lane (D3/D6/H3).

**F3 — MEDIUM: Trust signaling mismatched to the stakes.**
README end matter cross-links "voice-to-sculpture-game… CyberWitches · grocery-flywheel" and star badges/GEO blocks ("s-plus-geo", README:415) in the same document asking a patient to trust it with denial letters and symptom reports. Domain trust is built on clinical review, validation studies, and institutional accountability — none present.

---

## G. Roadmap believability

**G1 — HIGH: Both promised futures are gated on unscheduled, unnamed human acts — and structurally re-close.**
J3: "OFF by default and **CEO-gated forever**" (design:149). Real-case era: "Real-case import stays disabled until an independent verifier approves the exact build" (README, Coverage Continuity). No named verifier, no date — and "the exact build" means every subsequent commit invalidates the approval, so the real-case era re-closes by construction at any real release cadence. A roadmap of two locked doors with no keyholder is a roadmap to this exact state, forever.

**G2 — MEDIUM: J3 (hosted runner) contradicts the mission at the concept level.**
design:149: "hosted = cloud call = external act". README, Privacy: "No data is sent to a hosted HealthAdvocate service." The escape hatch for the typed-decision layer is the one act the product's identity forbids — on deidentified text whose deidentification recall is, per the threat model, never measured (`docs/THREAT-MODEL.md:20`). Shipping J3 would ship unmeasured PII leakage to a vendor as a feature.

**G3 — MEDIUM: The calibration promise is unreachable under the input policy.**
design:137: thresholds must be "derived from MEASURED confidence distributions on each converted surface" — impossible while real input is banned. The one surface with production thresholds admits it: "the frozen synthetic measurement corpus", confidence "degenerate at 1.0" (`core/insurance_fighter.py` docstring). The HA-JEV concept ("calibration — a model that knows when it doesn't know", design:15) can only ever be calibrated against synthetic text, i.e., never calibrated for the user's problem.

---

## H. Missing concepts a patient would need

**H1 — HIGH: Intake.** Real patients have paper, PDFs, photos, portal messages. Every endpoint is paste-`*_text` (app.py:235-298). No OCR, no PDF, no document store. The first physical act of the journey — "here is my pile of bills" — is unsupported.
**H2 — HIGH: The clock.** Insurance fights are deadline machines (appeal windows, external review, COBRA election, special enrollment). Coverage classifies deadlines (`coverage/workflow.py:25-33`) but there is NO reminder/notification/escalation loop anywhere, and family/tracks state is in-memory (README:365). The highest-cost failure in the domain — missing a deadline — is entirely unowned.
**H3 — HIGH: Money ground truth + financial assistance.** No price benchmarks, no CPT/HCPCS decoding, no 501(r) charity-care/financial-assistance screening — often the single biggest available win on a large bill. What exists is a `$` regex (bill_decoder.py:13).
**H4 — MEDIUM: Jurisdiction/plan-type model.** Rights, appeal routes, and external review depend on state and ERISA status; the product generates "your rights" (README:53) without ever asking.
**H5 — MEDIUM: Human-handoff artifacts.** No named-human directory (E2); no cross-surface case file/timeline/export a professional advocate or attorney could consume (only coverage has export, README endpoints table).
**H6 — LOW: Caregiver reality.** "Family" framing (README:74) with ephemeral single-session profiles (`core/family_tracker.py`, in-memory per README:365); no remote caregiver model, no shared access story.

---

## What I could NOT assess

- **Real-world accuracy/harm rates of any output** — synthetic-only law forbids the real cases that would measure it; nothing in-tree evidences clinical validation.
- **Actual model behavior** — no LM Studio/model run; Meditron3-8B never executed. The audit brief's "27B local model" is not evidenced anywhere in-tree (README recommends Meditron3-8B; `llm_client.py:27` defaults to `"local-model"`).
- **Rendered UI** in a browser (text-only review).
- **Legal/regulatory status** (FDA CDS/SaMD boundaries, state insurance/UDAP law, unauthorized practice) — not legal review.
- **User demand and willingness to install** — pre-user; no users exist to interview.
- **Competitive market facts** — no market research performed; F1/F2 are category-level reasoning, not sourced competitor data.
- **PII recall of the deidentification stack** — explicitly never measured (`docs/THREAT-MODEL.md:20`).

---

## (1) Top-3 existential risks

1. **No lawful product-market contact.** Synthetic-only policy + a self-re-closing real-case gate (A1, G1) mean the target user's real problem can never enter the product. It ossifies as an engineering artifact whose rigor is inversely proportional to its contact with reality.
2. **Harm asymmetry of the assessment surfaces.** Diagnosis-shaped "likely" labels, drug warnings from model memory, and a default config that screams HIGH at everything (D1-D3) — behind trust badges with inverted semantics (D5). One patient harmed by a confident wrong answer or alarm fatigue is an existential liability and a moral failure the receipts ledger does not cover.
3. **The trust promise is unattested.** Unverifiable locality, unmeasured PII recall, "verified"/"confirmed" flags that don't verify (D5, B3, A4). The only real differentiator vs a frontier chatbot is the first thing to be falsified when — not if — real use begins.

## (2) The single highest-leverage change

Open the real-case gate around ONE beachhead user with ONE problem: the person fighting a denial or a coverage gap — the track where the product is already deepest (coverage scripts, commitment gate, deadline classification) and where outputs are deterministic enough to be safe. Name the human verifier, set the date, run real cases end-to-end, and freeze the eight generative surfaces (symptoms, drugs, scanner…) until each has measured evidence. Every downstream concept — calibration honesty (G3), J3 (G2), threshold provenance — is unreachable without real-case contact; one opened gate converts this from an art piece into a product being tested on its mission.

## (3) Verdict

Would I let a family member use this? **No — not today.** Not because the code is careless (the privacy discipline is unusually serious) but because in its documented default configuration it labels every symptom HIGH (D2), its drug and misinformation surfaces have no ground truth yet print verdict-shaped labels (D3/D4), its safety flags don't mean what the README says they mean (D5), and its own policy forbids pasting the real denial letter that would actually help (A1). For a relative with an insurance fight I would point them to a human navigator or hospital advocate first; I might hand them the coverage scripts as a worksheet. The distance between here and "yes" is not more engineering — it is contact with real patients, one named verifier, and one deadline engine.

---

## IMPROVEMENTS

1. **Merge the three "no model" stories into one documented truth** — include `HEALTHADVOCATE_MODEL_ENABLED` and `HEALTHADVOCATE_MODEL_URL` in README's configuration table and reconcile README:366 ("endpoints return errors") with the actual silent-fallback behavior. *Why:* I burned real audit time reconstructing what state the product ships in; a user following the Quick Start lands in fallback mode where every symptom reads HIGH (C3/D2). *Fix:* a "What works without a model" table in README, generated from `unavailable_structured_fallback` behavior.
2. **Render `NEEDS_HUMAN`, its `allowed_next_steps`, and a named-human directory in the UI** (state DOI, CMS navigator, hospital patient advocate, crisis line on the symptom surface). *Why:* the product's core safety concept is invisible at the glass — I had to grep `app.js`/`app.py` to prove the patient never sees "ask a human" (E1/E2). *Fix:* a `decision-banner` partial consuming `urgency_decision`/`allowed_next_steps`, plus a static `resources.json` referral directory.
3. **Put one real case through the product before any J3/calibration/threshold work** — name the independent verifier, date the gate opening, and time-box a pilot with one actual denial letter. *Why:* I could not assess the one thing the product exists to do, and every roadmap item (G1-G3) dead-ends on this gate. *Fix:* a `PILOT-2026-xx` release whose changelog entry is one real-case outcome, pass or fail.

Status: DONE_WITH_CONCERNS
