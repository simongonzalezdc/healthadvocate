# HealthAdvocate threat model — 2026-09-24

Born from the 2026-09-24 three-lane adversarial audit (Opus architecture
leg: "no document names the adversaries"). This document names them, states
what protects the patient against each today, and states the gap honestly.
It is the seed of the audit's remediation item 7; controls improve, this
list of adversaries does not shrink silently.

## The asset

Patient-entered text (symptoms, bills, denial letters, discharge notes,
coverage cases) — health-identifying by content even when no explicit name
is attached — plus family-profile associations.

## Adversaries and accident classes

| # | Who/what | Today's control | Honest gap |
|---|---|---|---|
| 1 | **The remote model runtime** (where deidentified text actually goes) | Endpoint policy asserts a loopback URL (privacy/endpoint_policy.py); PrivacyBoundary strips PII first | **Assumed, not attested**: a URL check cannot see SSH forwards or proxies behind 127.0.0.1 — the live tunnel pattern (audit finding C1) satisfies the letter while sending deidentified text off-machine. Fix direction: runtime attestation (unix socket or identity-pinned authenticated runtime). |
| 2 | **A PII-detection miss** (the model that fails to spot an identifier) | Mask-by-default deid on every model path; fail-closed placeholder on deid failure; canary tripwires in tests | **Recall is never measured**: a silent NER miss passes identifiers to the deidentified stream. Fix direction: measured-recall gate on pinned model revisions before any model call. |
| 3 | **The local OS / other local users/processes** | Per-user OS account; loopback-only bind; family profiles in memory only (no on-disk profile store) | Nothing authenticates the UI to the OS user; anything running as the same user reads process memory (family associations). |
| 4 | **The patient's own browser / a rebinding website** | Loopback bind; CORS defaults localhost | **No auth on the UI**: DNS rebinding or another local page can reach the API. Real PHI typed into free-text surfaces is processed with no gate (the release gate guards the coverage STORE only — H1/H2). Until the real-case era, treat every text box as synthetic-only BY POLICY; the enforcement gap is tracked, not hidden. |
| 5 | **Model files & supply chain** | Exact openmed pin + transitive lock (CI-installed); pip-audit gate; gitleaks | Model weights load by repo id with integrity check at preload but no hash pin at inference load (audit C3); first-run fetches public checkpoints. |
| 6 | **A malicious or confused model** | Structured-output schemas; guardrail system prompts; NEEDS_HUMAN wrapper on converted surfaces; fallback content is deterministic | Unconverted surfaces trust parsed LLM JSON; fallbacks are success-shaped (audit SOL) — a wrong-but-confident answer is not distinguished from a checked one. |
| 7 | **Family members sharing the machine** | Family profiles in-memory, lost on stop | Anyone at the keyboard mid-session sees/enters profiles; no session lock. |
| 8 | ** ledger tampering** (local audit receipts) | Append-once filenames; sanitized fields (no raw text/canaries) | Receipts are unsigned JSON — a local writer can edit/fabricate (audit M-series). Fix direction: adopt upstream HMAC signing. |

## Non-goals (stated, not implied)

- Not a medical device; no diagnosis — every generative output is advocacy
  prep, unverified by any clinician.
- Not multi-tenant; exactly one patient (the local user) by design.
- No real-case data until the release gate's named-human-verifier act —
  enforced today ONLY on coverage import; the free-text boundary is policy
  (above), pending enforcement work.

## Change rule

Any new model destination, new text surface, or new persistence location
updates this file in the same PR.
