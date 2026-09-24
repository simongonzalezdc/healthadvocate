CRITICAL

**C1. "Loopback-only" does not mean "local". The default model URL is an SSH tunnel to another host.**
- `endpoint_policy.py:108` accepts any loopback host by its label alone. `default_model_base_url()` returns `http://127.0.0.1:11434/v1` (lines 125–127), and `docker-compose.yaml:10` sets the same.
- On this machine, `lsof` shows the listener on `127.0.0.1:11434` is `ssh` (pid 69897).
- `~/Library/LaunchAgents/com.kyanite.ha-crack-tunnel.plist` runs `/usr/bin/ssh -N ... -L <ip>:11434:<ip>:8908 nucbox` with `KeepAlive`.
- `tools/champion_playground.py:5` says it outright: "127.0.0.1:11434 -> nucbox Qwen3.8-27B via the self-healing launchd tunnel".
- So in live runs, de-identified patient text goes over the network to a second machine. The README's claim of local-only inference is false in practice. No code can detect this: the policy checks the URL string, not where the socket actually ends up.
- I could not check nucbox's logging, retention, or who else can reach its port 8908.

**C2. The lockfile is empty.**
- `requirements.lock.txt` has 8 lines, all comments, and zero package pins. The same is true on `origin/master`.
- Commit `aefccb8` says "66 exact pins frozen … hash-exact transitive lock". `git show` shows it added only those 8 comment lines. The claimed reproducible build and hash-exact lock do not exist.
- What actually gets installed:
  - CI installs from `healthadvocate/requirements.txt`, which uses `>=` ranges for everything except openmed (`ci.yml:60`).
  - pip-audit runs against that same range file (`ci.yml:74`).
  - The Dockerfile installs an unpinned `torch` from a separate index, uses the ranges file, and uses `python:3.14-slim` although the product targets 3.13.
  - `.renovaterc.json` has `"automerge": true, "platformAutomerge": true`, so an openmed bump — the de-identifier itself — auto-merges if the contract tests pass.
  - Those contract tests (`tests/test_openmed_contract.py`) only check function signatures and round-trips. They do not measure recall.

**C3. The whole privacy guarantee rests on openmed's NER recall, which has never been measured, and a miss sends raw text with the status reported as success.**
- `boundary.py:133–136`: an empty mapping becomes `NO_PII_FOUND`, and `allows_model_call` is true for that status (lines 42–46). Any PII the model misses goes verbatim to the model.
- The only backstop is canaries. In production they are empty: `structured_model_call` passes `canaries=None` (`gated_model.py:25`), which becomes `canaries=canaries or []` (`engine.py:399`).
- No test runs the real de-identifier against realistic PHI. The only real-openmed tests are the signature and round-trip checks above.
- Model weights load through `ModelLoader()` (`engine.py:97–100`). I found no revision pin, `local_files_only` or offline flag (grep for `revision|HF_HUB|OFFLINE` in `healthadvocate/` returned nothing). A swapped or updated model file silently changes what counts as PII. That unpinned-revision point is my inference; I did not inspect openmed's loader defaults.

### HIGH

**H1. DNS rebinding exposes the family and coverage data.**
- `app.py:96–101` adds only CORS. There is no `TrustedHostMiddleware`, no Host-header check and no authentication on any endpoint (`app.py:227–632`).
- A malicious site that rebinds its domain to `127.0.0.1:8080` becomes same-origin and can read `GET /api/family/profiles`, `GET /api/coverage/cases/{id}` (decrypted cases), and `POST .../export`.
- Binding to loopback does not defend against browser-borne attacks.

**H2. The real-case release gate is decorative: nothing stops real PHI from being entered today.**
- `/api/coverage/import-real` is a hardcoded 403 (`app.py:388–398`), and `coverage_status` hardcodes `"real_case_import_enabled": False` (`app.py:320`).
- `release_gate.py` writes a JSON bundle that no runtime path reads. Its evidence is caller-supplied booleans (`independent_verifier_approved`, `verified_evidence`, lines 106–109 and 142–158) with no identity or signature for the verifier. `extra_receipts` are appended without checks (line 167–168).
- Meanwhile every free-text endpoint (symptoms, bills, denials, documents, discharge, family profiles) accepts real PHI. The gate controls a label, not the data flow. The "real-case era" has effectively already started for anyone who pastes a real bill.

**H3. The decision receipts are forgeable and not bound to any input.**
- `IdentificationReceipt` is a plain pydantic model (`receipt.py:56–64`) with no input digest, nonce, signature, or question/run binding.
- `assess` only re-validates its shape (`assess.py:407`). Anyone can construct `IdentificationReceipt(model_used="x", deidentification_status=NO_PII_FOUND)`; the docstring admits "Direct construction carries caller text verbatim" (`receipt.py:18–19`).
- A receipt from one call can gate a different call.
- The receipt's "identification" is clinical NER classes (disease, drug, anatomy), not PII coverage. So the rule "identification before assessment" says nothing about whether the text was actually de-identified.
- The status itself is taken from the model-output dict (`symptom_assessor.py:73–75`, `llm_output.get("deidentification_status")`). Today that is safe only because `gated_model.py:62` overwrites the field after the model returns. That is fragile, not structural.

**H4. Threshold honesty: the symptom-triage "confidence" is a hardcoded 1.0 on a raw LLM pick, and the ANSWERED reason text claims a measured, calibrated threshold.**
- `symptom_triage.py:139` sets `confidence=0.0 if placeholder else 1.0`.
- `_REASONS["answered"]` = "Calibrated confidence met the measured threshold" (`assess.py:140–142`), but this surface uses the policy tier.
- If the model omits `urgency`, the default is `"medium"` (`symptom_triage.py:131`) at confidence 1.0, so it comes back ANSWERED medium.
- If the model says `"low"` for red-flag symptoms, it comes back ANSWERED low unless NER cross-validation happens to flag a disagreement.
- The gate checks whether the model's output is valid JSON, not whether it is correct. The NEEDS_HUMAN path is complete for malformed output, not for a confident wrong answer.

**H5. The model is untrusted input but is treated as an oracle, and port squatting makes that an attack.**
- If the tunnel or runtime is down, any local process (any user on the machine) can bind `127.0.0.1:11434`. It then receives the de-identified text and returns chosen JSON, for example urgency "low" or a fabricated `draft_appeal`.
- The loopback policy authenticates nothing (no TLS pinning or token; `api_key="local"`, `llm_client.py:160`).
- The same applies to a hosts-file change: `localhost` is accepted by name without resolution (`endpoint_policy.py:37`).

### MEDIUM

**M1. The "PII scrubbed" indicator is always true.** `deidentify_for_llm` always adds `_deidentification_status` to the mapping (`engine.py:215`), so `bill_decoder.py:77`'s `"pii_scrubbed": len(pii_map) > 0` is always True, even when de-identification failed or found nothing. The same `deidentify_for_llm` + `pii_map` pattern appears in `document_decoder.py:20`, `community_health.py:20` and `appointment_prep.py:20`. Also `engine.privacy_boundary()` (lines 408–412) can never report `NO_PII_FOUND` for the same reason.

**M2. Supplying canaries silently drops the defaults.** `assess.py:417` uses `tuple(canaries) or DEFAULT_CANARIES`, and `redact_text` uses `canaries or DEFAULT_CANARIES` (`logging_redaction.py:48`). Both contradict "supplied canaries plus the module's defensive defaults" (`receipt.py:16–17`, `assess.py:367–369`). Canaries are also synthetic-only by nature (`logging_redaction.py:10–15`), so they protect nothing once data is real.

**M3. The audit "ledger" has no tamper evidence, and the brief's word "signed" is false.**
- `policy_audit.py` writes plain JSON files. There is no HMAC, signature or hash chain. Grep for `sign|hmac|tamper` in HA code found nothing; openmed 2.5.0 offers HMAC audit keys, but HA does not adopt them per the upstream changelog doc (line 47).
- Anyone with write access can delete, fabricate or edit receipts. Only an unparseable file is re-healed (lines 190–197).
- `run_input_digest` is an unsalted, truncated SHA-256 of the assembled PII-bearing text (`engine.py:245–251`). For low-entropy PHI (a short name plus date of birth, an SSN) it works as a confirmation oracle, which contradicts "never reversible to text".
- The default location is derived from the package path (`default_project_root()` = `parents[2]`), which is odd inside site-packages or a container.

**M4. The Docker image binds 0.0.0.0** (Dockerfile `CMD ... --host 0.0.0.0`). Safety depends entirely on the compose file's `127.0.0.1` publish. The README concedes "no loopback-exposure guarantee" outside that profile (`README.md:286`).

**M5. Raw NER entity text goes into prompts.** `bill_decoder.py:24` builds `entity_desc` from NER on the raw `bill_text` and puts it in the prompt next to `safe_text`. Protection then depends on the second de-identification pass in `structured_model_call`. If the first pass failed (placeholder), clinical terms still flow. Low identifying risk, but it breaks "de-identify first".

### LOW

- **L1.** `llm_client.chat()` (line 170) is an exported, ungated model primitive with no de-identification. It is unused today and is a trap for the next feature.
- **L2.** The hosted-jev stub is genuinely inert (`runners.py:82–85`). Its safety depends on review discipline, not a technical control: a future edit to `get_runner` or `hosted_jev_call` flips it.
- **L3.** `threshold_applied` and the answer are attached even on NEEDS_HUMAN legs (by design), but no consumer is audited for acting on them.

## Threat-model gaps

No document names the adversaries. My reading of the code:
- **Local OS users and processes:** unaddressed (H5).
- **The patient's own browser and websites:** unaddressed (H1).
- **Model files and supply chain:** unaddressed (C2, C3).
- **The remote model host:** unacknowledged (C1).
- **Family members sharing the machine:** unauthenticated UI; family profiles are held unencrypted in process memory (`family_tracker.py:9`).
- **A malicious or confused model:** not modelled (H4, H5).

## What I could not assess

- openmed's real recall on PHI.
- nucbox runtime logging and exposure.
- Whether openmed's loader pins model revisions or downloads at first run (network egress).
- The frontend JS.
- Live CI results.
- The keystore and encrypted-store crypto in depth.
- The Compose publish at runtime.

## Summary

**(1) Top-3 existential risks**
1. De-identified patient text leaves the machine over the tunnel (C1).
2. PII passes through on any NER miss, with no measurement and an unpinned model and dependencies (C2 + C3).
3. Real PHI can be entered today with no release gate in the path, served unauthenticated to any rebinding website (H1 + H2).

**(2) Highest-leverage change:** make the model destination and the de-identifier something the system can attest to at runtime, rather than something it assumes. That means refusing forwarded endpoints (for example, requiring a unix socket or an authenticated, identity-pinned runtime), and gating every model call on a measured-recall de-identifier pinned by hash. Together this closes C1, C3 and H5.

**(3) Verdict:** No, I would not let a family member use this with real data. The code-level fail-closed discipline is unusually careful. But the guarantees that actually protect a patient — data stays on this machine, identifiers are removed, nothing real enters until verified, the build is reproducible — are either untrue in current live runs (tunnel, empty lock) or never measured (NER recall). The gate that is supposed to hold the line guards a single endpoint while every other text box accepts PHI. Synthetic-only demo use is fine; real use needs C1–C3 and H1–H2 closed first.

## IMPROVEMENTS
1. **Claim-vs-artifact check on commits.** Why: commit `aefccb8` claims 66 hash pins and the file holds 0 pins, and a four-gate CI did not catch it. Fix: a CI step that fails if `requirements.lock.txt` has fewer than N `==` lines or no `--hash`, and switch CI to install from the lock.
2. **Audit briefs should name the live topology.** Why: the brief called 127.0.0.1:11434 loopback-only; that it is a tunnel to nucbox only surfaced from launchd. Fix: dispatch briefs for privacy audits include `lsof -iTCP -sTCP:LISTEN` output for the ports involved.
3. **Brief placeholder.** Why: "PRIVACY {{TASK}} SAFETY" is an unrendered template variable in this brief. Fix: have the dispatch renderer fail when a `{{...}}` placeholder survives.
