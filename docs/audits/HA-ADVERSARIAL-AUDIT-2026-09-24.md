# HealthAdvocate — three-lane adversarial audit — 2026-09-24

Mandate (CEO, one-time): MECE adversarial audit of the entire concept —
project, design, functional features, everything — via pushing-dispatch on
three named lanes: Xiaomi MiMo v2.6 PRO (official Token Plan), Opus 5.5-class
(inside kilo-cli), GPT-6 SOL (codex primary, high effort).

## Lane receipt

| Leg | Executor | Model | Outcome |
|---|---|---|---|
| Concept & product design | xiaomi-mimo (matrix override: re-enabled, pro tier) | mimo-v2.6-pro | **DONE (lane FIXED same-day).** Original defect: the stock wrapper is single-shot; agentic MiMo answers briefs with tool calls, so the required terminal Status token never appears (v2.5-pro failed identically — the "worked historically" belief was false). Fix: xiaomi-mimo-v26.sh now runs a structured-tool agent loop (bash/read/write/todowrite, budgets, final-message-only Status grep). Verified: smoke DONE + the full concept audit ran (w-4271, 11 turns, 291k tokens, worktree clean). Durable upstream fix (opt-in tool loop in ce_run_openai_compatible) noted to Platform. Report: `2026-09-24-mimo-concept.md`. |
| Architecture, privacy & safety | kilo-opus-55 (temp matrix lane) | kilo/~anthropic/claude-opus-latest | **DONE** — 114-line report, 21 file:line citations (full text: `2026-09-24-opus-architecture.md`). |
| Functional features & engineering | codex-sol-high | GPT-6 SOL | **DONE** — 122-line report (full text: `2026-09-24-gpt6sol-engineering.md`), 132k tokens of work. |

All three MECE partitions are now covered: concept/product (MiMo),
architecture/privacy (Opus), features/engineering (SOL). All three verdicts
CONVERGE: not for real-patient use today; synthetic-demo use only; the gap is
contact with reality, not code rigor.

## Convergent findings (both engines, independently — the strongest class)

1. **"Would not let a family member use this with real data today."** Both
   verdicts, independently, with the same shape: excellent code-level
   fail-closed discipline; the guarantees that actually protect a patient are
   either untrue in live runs, unmeasured, or unenforced on real surfaces.
   Both permit synthetic-demo use only.
2. **The transitive lock shipped EMPTY (verified, fixed same-session).**
   Commit aefccb8's header-write self-truncated the file to 0 pins while
   claiming 66; four-gate CI caught nothing. Both auditors prescribed the
   same cure. FIXED: PR #34 (clean-room regen, 67 pins verified in-file
   pre-commit) + new CI Gate 1.5 (fail < 60 pins). Install-CI-from-lock
   queued.
3. **Guarantees are assumed, not attested.** SOL: "green evidence conceals
   broken delivery" (mock/source-level tests; readiness that stays green
   through model failure). Opus: the model destination and de-identifier are
   trusted, not proven — with my own live tunnel as the exhibit (C1 below).

## Opus architecture leg — the load-bearing findings

- **C1 (CRITICAL): de-identified patient text leaves the machine.** The live
  loopback endpoint is an SSH tunnel to the nucbox (launchd
  com.kyanite.ha-crack-tunnel); the endpoint policy checks the URL host, not
  the destination. VERIFIED TRUE — this is my own session's setup.
  Prescribed: attest the destination at runtime (unix socket /
  identity-pinned authenticated runtime), refuse forwards.
- **C2/C3: PII passes through on any NER miss — and recall is never
  measured**; model revisions and dependency integrity unpinned at load.
  Prescribed: gate every model call on a measured-recall de-identifier
  pinned by hash.
- **H1/H2: real PHI can be entered TODAY** — the release gate guards the
  coverage store only; every free-text surface (symptoms/bills/documents)
  accepts real PHI, served by an unauthenticated UI (browser rebind
  exposure). VERIFIED TRUE in code (gate exists only on coverage import).
- **M-series:** audit receipts are unsigned plain JSON (no HMAC — upstream
  ships it, HA didn't adopt); run_input_digest = unsalted truncated SHA-256
  of PHI-bearing text (confirmation oracle for low-entropy identifiers);
  Docker binds 0.0.0.0 (compose-only protection); bill_decoder puts raw NER
  entity text in prompts; llm_client.chat() is an ungated exported primitive.
- **Threat-model gaps:** no document names the adversaries (local OS users,
  the browser, model files/supply chain, the remote model host, family
  members sharing the machine, a malicious model).

## GPT-6 SOL engineering leg — the load-bearing findings

- **Top risk 1: the first-run product is functionally hollow** — official
  setup silently disables the model; nearly every promised answer path
  degrades to fallbacks; quick-start promises turnkey it doesn't deliver.
- **Top risk 2: green conceals broken** — route/Docker/model-setup/UI flows
  can fail while the aggregate count stays green; tests pin source-level
  behavior, not HTTP/browser behavior; fallback outputs are success-shaped.
- **Top risk 3: overstated inference** — substring-overlap "validation",
  unsourced LLM generation presented with medical-adjacent confidence.
- **Highest-leverage change (both legs converge on variants of this):** one
  clean-room, model-fixture-backed acceptance gate — install from the hash
  lock, boot the documented runtime, wait for TRUTHFUL readiness, drive every
  named feature through HTTP AND browser in model-success and model-failure
  modes; mandatory in CI. (Our a11y/ax harness is the seed of exactly this —
  it must grow from 3 journeys to all surfaces.)

## Verified-vs-claimed reconciliation (PM, this session)

| Claim | Verdict |
|---|---|
| Lock empty on master | VERIFIED (8 lines at d76c0d4) → FIXED PR #34 |
| Free-text surfaces ungated vs real PHI | VERIFIED (gate only on coverage import) |
| Tunnel violates local-only posture | VERIFIED (my own launchd agent; also self-reported §9.13) |
| NER recall unmeasured; receipts unsigned; family profiles unencrypted in memory | ENGINE-CLAIMED, plausible on code read — queued for verification |

## MiMo concept leg — the load-bearing findings (the third convergence)

- **A1/CRITICAL: the product's own policy forbids its target user's use** —
  synthetic-only-by-policy on every text box vs a mission sold to patients
  "at their most vulnerable." The real denial letter cannot lawfully enter.
- **D2/CRITICAL: the documented default build screams HIGH at every symptom**
  (model off -> placeholder -> NEEDS_HUMAN -> conservative escalation to
  HIGH): alarm fatigue by design. (PM-verified chain; the escalation rule is
  mine from J2-c.)
- **D1/D3/D4: verdict-shaped output without ground truth** — "likely"
  condition labels disclaimed by prose; drug interactions from model memory
  with an `ner_verified` stamp the UI reads as verification; misinformation
  "credibility" grades with no retrieval. Highest liability, least grounding.
- **D5: `pii_scrubbed` semantics inverted** — true only when PII was FOUND;
  a detector miss shows the absence of the badge (or false) — the README
  sells it as confirmation.
- **E1: the fail-closed payload is invisible at the glass** — NEEDS_HUMAN and
  allowed_next_steps appear NOWHERE in the UI; the patient sees only the
  HIGH badge. E2: it names no human (no navigator/advocate/crisis directory).
- **B3: "cross-validation" is a substring check presented as a Reliability
  badge.** A2: install burden selects tinkerers, not the vulnerable patient.
- **G1: both roadmap doors re-close by construction** (verifier must approve
  "the exact build"; J3 is CEO-gated forever) — a roadmap to this exact state.
- **Highest-leverage (all three engines, stated three ways): open ONE real
  beachhead** — the denial/coverage fight, where the product is deepest and
  outputs deterministic — with ONE named verifier and a date. This is
  exactly the staged Pack A decision.

## Remediation ledger (ranked; owner PM unless noted)

DONE same-session: lock regenerated + CI lock-sanity gate (PR #34).
1. C1: runtime-attested model destination (refuse forwarded endpoints; unix
   socket or identity-pinned runtime).
2. H1/H2: free-text PHI decision (gate the text surfaces OR document the
   boundary honestly) + UI auth for non-loopback.
3. Measured NER-recall gate before any model call (pin model by hash).
4. Clean-room acceptance gate in CI (SOL's #1; grows a11y-ax).
5. HMAC-sign the audit receipts (upstream mechanism exists).
6. Install CI from the lock; kill or gate llm_client.chat().
7. Threat-model doc naming adversaries (Opus's list is the seed).
8. ~~MiMo lane defect~~ DONE (agent-loop wrapper; upstream note to Platform).
9. NEW (concept leg): distinguish model-UNAVAILABLE from model-answered-low
   in triage escalation (D2 — default build must not scream HIGH).
10. NEW: render NEEDS_HUMAN + allowed_next_steps + a named-human resource
    directory in the UI (E1/E2 — MiMo's #2 improvement).
11. NEW: "What works without a model" README table incl.
    HEALTHADVOCATE_MODEL_ENABLED (C3 — MiMo's #1 improvement).
12. NEW: fix pii_scrubbed semantics / rename to pii_found_and_masked (D5).
13. ~~Real-case beachhead pilot~~ STRUCK BY CEO RULING 2026-09-24: "this is
    a free open source tool." HealthAdvocate is positioned as free OSS for
    self-hosters — the org does not open a real-case era, does not name a
    verifier, runs no pilot. The release gate remains what it already is: a
    fail-closed control the SHIPPER of the tool carries (anyone deploying it
    seriously performs their own verifier act). Pack A card closed — not
    parked; the org-side ask no longer exists. Several concept-leg findings
    re-contextualize under this ruling: A2/A3/F1 (install burden, two
    customers, advocate-vs-pamphlet positioning) describe a consumer funnel
    the product does not claim; D1-D5/E1 ethics-and-honesty findings STAND —
    a free OSS tool that labels model recall "verified" still harms whoever
    self-hosts it.

Full engine reports: docs/audits/2026-09-24-opus-architecture.md ·
docs/audits/2026-09-24-gpt6sol-engineering.md
