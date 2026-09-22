# OpenMed upstream leverage assessment — 2026-09-17

Owner: PM-HEALTHADVOCATE (session 2). Commissioned by the Head of Product on a CEO
directive: "HealthAdvocate is built on top of OpenMed, I believe. OpenMed has
continued dev. I want to see what we can leverage from the latest upstream into
HealthAdvocate."

Status: ASSESSMENT ONLY. No upgrade was executed. The matrix and the staged path
below ARE the deliverable. Nothing left the workspace (health-data class law);
upstream was fetched read-only into `_reference/openmed-upstream/` (local-only
ignore via `.git/info/exclude`; never committed, never pushed).

---

## 1. Verified relationship (evidence, not belief)

**The CEO's belief is correct.** HealthAdvocate vendors the OpenMed medical-NLP
toolkit and builds its entire clinical/privacy engine on it.

| Fact | Evidence (live-verified 2026-09-17) |
|---|---|
| Vendored location | `/Users/simongonzalezdecruz/workspaces/HealthAdvocate/openmed/` — 66 `.py` files, 1.7 MB, tracked in git |
| Vendoring event | Single commit `bcf9990` (2026-05-12 16:47 PT, "Add openmed library dependency and full Docker setup with torch CPU"), 68 files / 18,099 insertions; `git log --oneline -- openmed/` shows exactly ONE commit — never touched since |
| Fork point | Upstream tag **v1.4.0** (2026-05-04). Content match: `diff -rq` of our vendored tree vs `git archive v1.4.0 openmed` differs in exactly 3 files (see §2); all other differences are `__pycache__` noise |
| True upstream | `https://github.com/maziyarpanahi/openmed` (README credits + arXiv 2508.01630, "OpenMed NER", Maziyar Panahi). Verified by content match against the tag, not just the name |
| Upstream today | **v2.5.0 (2026-09-14)** — 3,600 commits after our fork point; package grew to 898 `.py` files / 22 MB |
| Runtime truth | The VENDORED copy wins at runtime: `healthadvocate/core/engine.py:21-24` inserts the project root at `sys.path[0]` "so the bundled/development OpenMed copy is importable" — it shadows the pip-installed package |
| Known drift | `healthadvocate/requirements.txt` pins `openmed[hf]>=1.5.2` (its deps get installed; its CODE is shadowed). So HA ships v1.4.0 behavior regardless of the floor. Vendored `__about__.py` says `1.4.0` |
| License | Apache-2.0 at v1.4.0 AND at 2.5.0 HEAD (both LICENSE files verified) — **no license change, no Counsel flag required**. Upstream also ships a `NOTICE` (must be copied along if we keep vendoring) |

**What HA built on top** (the layers that make HA more than a OpenMed demo —
from session-1 live receipts, desk §1):
- `healthadvocate/governance/` — fail-closed release gate, license receipts
  (HA-E78), real-case-import stays disabled, independent-verifier approval flow.
- `healthadvocate/privacy/boundary.py` — PrivacyBoundary with canaries,
  deidentify-failure placeholder, fail-closed status codes, model-destination
  gating.
- `healthadvocate/core/` feature modules (community_health, insurance_fighter,
  appointment_prep, bill_decoder, discharge_translator, document_decoder…) all
  route through `HealthEngine.deidentify_for_llm()`.
- `healthadvocate/cli.py`, `healthadvocate/mcp_server.py`, `healthadvocate/coverage/`,
  FastAPI app with a11y-hardened views; 85-test synthetic suite; CI gates
  (gitleaks → pytest → compileall → pip-audit, PR #20).
- The ONLY import surface HA consumes from openmed: `ModelLoader`,
  `OpenMedConfig`, `analyze_text(...)`, `extract_pii(text, lang, loader)`,
  `deidentify(text, method, loader, keep_mapping)` → `.deidentified_text` /
  `.mapping`, plus three fixed registry model names
  (`disease_detection_superclinical`, `pharma_detection_superclinical`,
  `anatomy_detection_electramed`) and the per-language default PII model
  (`en` → `OpenMed/OpenMed-PII-SuperClinical-Small-44M-v1`).

**The `/Users/simongonzalezdecruz/workspaces/OpenMed` husk** (identified, not
worked in): PNGs only (`frontend-*.png`, `taste-*.png`, `home-*.png`, all
2026-05-12) plus `.omc`/`.omx`/`.playwright-mcp` agent-tool caches. It is the
same-day visual exploration/taste workspace for the OpenMed-based frontend that
became HealthAdvocate (the vendoring commit lands that same afternoon). No code,
no git. Candidate for archival by whoever owns workspace hygiene; out of this
lane's authority.

## 2. Our three local patches inside the vendored tree (the real divergence)

`diff -rq vendored vs upstream-v1.4.0` = exactly 3 files (committed as part of
`bcf9990` itself):

1. `openmed/__init__.py` — pure maintainability refactor: `analyze_text()`
   decomposed into 5 private helpers; public signature unchanged. No behavior
   delta.
2. `openmed/core/config.py` — (a) `threading.Lock` around global config
   get/set (HA is a threaded FastAPI server); (b) `_load_toml` now uses
   `tomllib`/`tomli` with the naive line-parser kept as fallback.
3. `openmed/core/pii.py` — (a) `to_dict()` exposes `mapping`; (b) `reidentify()`
   rewritten offset-safe (reverse-order replacement) — fixes upstream's buggy
   sequential `str.replace()` for repeated/overlapping placeholders.

Upstream absorption status at 2.5.0 (verified in the reference clone):
- Patch 3 is **superseded**: upstream 1.6.0+ emits unique placeholders
  (`[NAME]`, `[NAME_2]`) and 2.5.0's `reidentify()` is occurrence-aware with
  ordinal mapping keys — a more complete fix of the same bug class.
- Patch 2a is **NOT absorbed**: 2.5.0 `get_config`/`set_config` are still
  unlocked — our lock remains a needed carry-over (and an upstream-contribution
  candidate).
- Patch 2b/1 are moot at 2.5.0 (code restructured beyond recognition).

Everything else HA-side lives OUTSIDE the vendored dir — a rebase's blast radius
is the 3-file patch set plus the engine coupling contract above.

## 3. What changed upstream since our fork (v1.4.0 → v2.5.0, 3,600 commits)

Headline: upstream went from a Python/Apple-Silicon NER+PII toolkit to a
cross-platform (Python/Swift/Android/JS/browser) clinical-privacy platform with
policy-aware de-identification, signed audit evidence, FHIR/OMOP interop,
multimodal redaction, and its own CI/security gates. **The documented v1 Python
root entry points we use are preserved** — upstream's static API gates record
additions-only from 1.9.1 through 2.5.0 (zero removals/narrowed signatures), and
2.0.0's Compatibility section explicitly preserves `OpenMedConfig`,
`analyze_text`, `deidentify`, `extract_pii`. Verified concretely at 2.5.0:
`AnalyzeResult` is a `Mapping` with `.entities` of `EntityPrediction
(text, label, confidence, start, end)` — HA's duck-typed
`_extract_entities()` works unchanged; `DeidentificationResult` still exposes
`.deidentified_text` and `.mapping`; `requires-python >= 3.10` (HA venv is
3.13).

## 4. Leverage matrix

Class legend: SEC=security-fix (adopt fast), BUG=bug-fix (adopt),
FEAT=feature (evaluate vs roadmap + governance), BRK=breaking change
(migration cost), CONF=conflicts-with-HA-layers. Decision: ADOPT / ADAPT /
SKIP (+one-line reason). "On-bump" = arrives automatically with the vendor
bump; the reason column says what it buys or costs HA.

| # | Version | Change (upstream changelog) | Class | Decision | Reason |
|---|---|---|---|---|---|
| 1 | 1.5.2 | privacy-filter dispatcher RCE hardening: `trust_remote_code=True` was enabled for ANY repo-id containing "privacy-filter" (attacker-controlled `model_name` on OpenMed's own `/pii/*` endpoints → HF remote-code execution); default flipped to False + first-party allowlist + `OPENMED_TRUSTED_REMOTE_CODE_MODELS` override | SEC | **ADOPT (on-bump)** | Vendored 1.4.0 still carries the unsafe default (`openmed/torch/privacy_filter.py:61`). HA exposure TODAY is LOW: HA never passes user-controlled `model_name`; request input reaches openmed only as `text`+`lang` (`lang` → `DEFAULT_PII_MODELS.get(lang)` → None for unknown langs, fails closed); the `en` default PII model is a first-party SuperClinical checkpoint through the standard loader, not the privacy-filter path; deployment is loopback-only. Still adopt: the unsafe default is a latent hazard and the fix is free with the bump |
| 2 | 1.4.1 | `ModelLoader` local-path resolution + `local_files_only=True` for local model dirs (offline/air-gapped inference); `model_id` alias | BUG | **ADOPT (on-bump)** | Aligns exactly with HA's local-first, offline-evidence posture (`HF_HUB_OFFLINE=1` runs) |
| 3 | 1.5.0–2.1.0 | PII language packs: ar/ja/tr/ko/ro/ru/vi + 34-code catalog, checksum-valid ID validators, script-correct surrogates | FEAT | **ADAPT (on-demand)** | Zero runtime cost until a `lang` is requested; per-language rollout is a roadmap call for the Head of Product, not a code fork |
| 4 | 1.6.0 | policy-aware de-identification runtime: ten-stage pipeline, 6 bundled policy profiles (hipaa_safe_harbor…strict_no_leak), signed/reproducible audit reports | FEAT | **ADAPT (Stage 3)** | Strong alignment with HA's fail-closed governance DNA; audit evidence could feed HA's receipt ledger (HA-E78 class). Selective adoption: default profile ≈ current behavior, add profile+audit as explicit opts |
| 5 | 1.6.0 | `keep_mapping=True` now emits unique placeholders (`[NAME]`, `[NAME_2]`) for repeated entities | BRK | **ADAPT (tests)** | Supersedes our local `reidentify` patch with a better design, but deidentified OUTPUT strings change for repeated entities — synthetic suite + any UI copy asserting single placeholder style must be updated and re-heard (a11y) |
| 6 | 1.6.0 | shift_dates canonical-label fix, Feb-29 shifting, reversible `remove` mappings, repeated-entity round-trip fixes | BUG | **ADOPT (on-bump)** | Directly hardens the deidentify↔reidentify path HA's privacy boundary depends on |
| 7 | 1.7.0 | clinical term protection default ON in PII extraction (suppresses PERSON/LOCATION matches that are protected clinical vocabulary) | FEAT/BRK | **ADAPT (deliberate)** | Fewer false PII redactions on symptom text = better UX; but changes redaction behavior → gate with dedicated synthetic tests + canary pass-through check before accepting |
| 8 | 1.7.0 | `analyze_text(output_format="dict")` returns frozen `AnalyzeResult` (Mapping; `to_dict()` keeps legacy shape) | BRK | **ADOPT (verified low-cost)** | HA's `_extract_entities` already duck-types `.entities` (verified at 2.5.0: fields text/label/confidence/start/end present) — add a contract test, no code change expected |
| 9 | 1.8.1 | attention `auto` no longer forces SDPA onto unsupported architectures (DebertaV2 et al.); eager fallback | BUG | **ADOPT (on-bump)** | Correctness for HA's superclinical/electramed model families on Mac/CPU |
| 10 | 1.5.5/1.8.0 | batch PII/deid via `BatchProcessor`, model warm pools, `/models/unload`, loader cache release | FEAT | **ADAPT (Stage 3)** | RAM-constrained Mac wins for the dev loop (unload models after AX/a11y batteries) |
| 11 | 1.8.0 | no-raw-PHI logging, offline-mode socket blocking, privacy-gateway redaction before external calls | FEAT | **ADAPT (Stage 3)** | Defense-in-depth underneath HA's own PrivacyBoundary; matches org no-telemetry law |
| 12 | 1.9.x | ONNX cross-runtime contract (`OnnxModel` CPU), model-size/RAM estimation CLI, ARM latency budgets | FEAT | **EVALUATE (later)** | Possible memory/latency win vs torch on the Mac tier, but requires model-export qualification — roadmap call, not this pass |
| 13 | 1.6→2.5 | FHIR R4/R5 + OMOP CDM exporters, US Core conformance, terminology grounding | FEAT | **SKIP (now), PARK** | No interoperability roadmap item today; real lever if a "share with clinician" flow is ever chartered |
| 14 | 1.7→2.5 | multimodal redaction (PDF/DICOM/image OCR, EML, notebooks) | FEAT | **SKIP** | HA is text-first; huge optional-dependency surface conflicts with the minimal local-first posture |
| 15 | 2.0.0 | upstream MCP server (`openmed-mcp`, 30+ tools, protected resources, OAuth-style boundaries) | FEAT | **SKIP (keep HA's)** | HA already runs its own deliberately-scoped MCP (4 tools, fail-closed); swapping would widen the trusted surface for no current user need. Borrow patterns only |
| 16 | 2.0.0 | telemetry-off-by-default enforcement; `DEVICE` canonical label added (closed-enum consumers must update) | BRK/FEAT | **ADOPT (no-op)** | HA passes labels through (no enum of canonical labels) — verified non-issue; telemetry-off aligns with org law |
| 17 | 2.3.0 | strict input validation, rooted public error taxonomy, JSON fail-closed loading, bounded parsers everywhere | BUG/FEAT | **ADOPT (on-bump)** | More fail-closed behavior under HA's fail-closed layers — same direction of travel |
| 18 | 2.5.0 | clinical-preserving preview privacy processing; local privacy budget ledger; HMAC audit-key rotation; minimum-necessary field selector | FEAT | **EVALUATE (Stage 3+)** | Genuinely useful to HA's future real-case governance pack; adopt when the real-case path unfreezes (currently fail-closed by design) |
| 19 | 2.5.0 | Material-for-MkDocs CVE-2026-73295 fix (docs build dep) | SEC | **SKIP (N/A)** | HA doesn't build upstream docs; HA's own pip-audit gate governs HA's tree |
| 20 | 2.3.0 | known NLTK CVE-2026-81726 in OPTIONAL integration trees (agent/LlamaIndex/QuickUMLS/scrubadub) | SEC | **NOTE** | HA installs none of those extras; keep out of HA's dependency closure |
| 21 | all | dependency/setuptools security bumps, SBOM/Sigstore/SLSA release evidence | SEC | **ADOPT (on-bump)** | Keeps our PR-#20 pip-audit gate quiet; upstream ships signed evidence we can cite in receipts |
| 22 | — | upstream config get/set STILL unlocked at 2.5.0 | CONF | **CARRY our patch 2a** | Re-apply the threading.Lock as a 6-line patch on top of the pinned package (or propose upstream); HA's threaded server wants it |
| 23 | — | vendoring vs pinning: package is now 898 files / 22 MB (vs our 66 / 1.7 MB) | CONF | **DECIDE (Stage 0)** | Re-vendoring 22 MB re-creates today's drift on a monthly-release upstream; recommended path is PyPI pin + drop the vendored dir (see §5) |
| 24 | — | `engine.py` sys.path insert makes the vendored copy shadow the pip pin (`>=1.5.2` floor never actually ran) | CONF | **FIX (Stage 0/2)** | The floor was set at 1.5.2 (the security release) yet the runtime never used it — exactly the drift class this assessment exists to close |

## 5. Staged upgrade path (assessment; execution is a future session)

Pivot decision first (Stage 0): **stop vendoring; pin the PyPI package.**
Rationale: (a) content-verified API compatibility makes the swap low-risk;
(b) 22 MB / 898 files in-repo on a monthly-release upstream guarantees repeat
drift; (c) `requirements.txt` already names `openmed[hf]` — the pin becomes the
single source of truth and the PR-#20 CI gates (pip-audit especially) become
the upgrade safety net; (d) license is unchanged Apache-2.0 with NOTICE shipped
in the package. If an air-gap requirement ever lands (real-case era), revisit
with an sdist vendor + hash pin.

- **Stage 0 — hygiene PR (pre-req)**: land Q1 changelog repair; remove the
  `engine.py` sys.path insert (lines 21-24) in the same PR so the pip copy
  resolves; align `requirements.txt` to an exact pin so reality and manifest
  agree before the jump. AMENDED at execution (2026-09-22): the pin is
  `openmed[hf]==1.5.2`, not ==1.4.0 — the PR-#20 pip-audit gate correctly
  refuses 1.4.0 (PYSEC-2026-2852, fixed in 1.5.2). Runtime at this stage is
  still the vendored 1.4.0+patches via repo-root cwd; the pin governs the
  pip copy and CI; Stage 2 unifies both at 2.5.0. Re-run the 85-test suite + governance receipt at this
  intermediate state.
- **Stage 1 — contract-test PR (make the bump red/green, not discovery)**: add
  adapter tests pinning the coupling contract at 1.4.0: `analyze_text` result
  shape; `deidentify(keep_mapping=True)` → mapping round-trip; placeholder
  scheme; PrivacyBoundary canary pass-through; the three model registry keys.
  These tests are version-agnostic and become the bump's tripwire.
- **Stage 2 — vendor bump PR (`chore/openmed-2.5.0-bump`)**: branch from
  canonical master → set `openmed[hf]==2.5.0` (exact pin, not `>=`, so CI is
  reproducible) → delete the vendored `openmed/` dir → re-apply the 6-line
  config thread-lock patch as a site-level shim if still wanted (preferred:
  wrap `OpenMedConfig` access in `HealthEngine` under our own lock, zero
  upstream patch) → full gate battery: 85-test synthetic suite + subtests,
  `compileall`, governance license receipt + fail-closed release-bundle probe,
  `make a11y-ax` (3 journeys), CLI + MCP live probes (session-1 commands),
  Forgejo CI all four gates green (gitleaks → venv/deps → pytest → pip-audit).
  Expected code changes: none in `engine.py` beyond the sys.path removal;
  test updates only where placeholder uniqueness (`[NAME_2]`) or clinical-term
  protection changes asserted output. Rollback = revert one PR (stateless
  library swap, no data migration).
- **Stage 3 — selective feature adoption (separate small PRs, each with
  tests)**: policy-profile deid + signed audit receipts wired into the
  governance ledger; no-raw-PHI logging alignment; model unload for the dev
  loop; placeholder-scheme copy updates re-checked by the a11y batteries.
- **Stage 4 — watch**: quarterly upstream sync review (upstream ships
  ~monthly; 2.5.0 was 2026-09-14); extend desk queue Q5 (pip-audit freshness)
  to cover the openmed chain; revisit FEAT rows 12/13/18 at the real-case
  governance milestone.

Guardrails that hold throughout: synthetic-only inputs; fail-closed posture
unchanged (import disabled, verifier pending); no cloud calls; nothing leaves
the workspace; CI gates stay green at every merge.

## 6. Fork-point receipts (how this was verified)

- `git log --oneline -- openmed/` → exactly `bcf9990` (2026-05-12).
- `git diff bcf9990 d8818c5 --stat -- openmed/` → 0 lines (vendored tree
  unchanged from fork to current canonical master).
- `git archive v1.4.0 openmed | tar -x` + `diff -rq` vs vendored → 3 differing
  files (`__init__.py`, `core/config.py`, `core/pii.py`), rest `__pycache__`.
- Upstream clone at `_reference/openmed-upstream/`, HEAD `b161a18f`
  ("Add clinical note routing and extraction profiles (#3245)"), `__about__.py`
  → 2.5.0; `git rev-list --count v1.4.0..HEAD` → 3600.
- License: `head LICENSE` at HEAD and `git show v1.4.0:LICENSE | head` → both
  Apache-2.0; `pyproject.toml` → `license = { text = "Apache-2.0" }`.
- 2.5.0 API spot-checks: `openmed/__init__.py` lazy-export table contains
  `ModelLoader`, `OpenMedConfig`, `deidentify`, `extract_pii`, `analyze_text`;
  `openmed/core/results.py` `AnalyzeResult(Mapping)` with `.entities`;
  `openmed/processing/outputs.py` `EntityPrediction(text, label, confidence,
  start, end)`; `openmed/core/pii.py` `DeidentificationResult` keeps
  `.deidentified_text`/`.mapping`; occurrence-aware `reidentify()` at
  `pii.py:3652`.
- Vendored 1.5.2-exposure check: `openmed/torch/privacy_filter.py:61`
  `trust_remote_code: bool = True`; HA request surface passes only
  `text`/`lang`/`profile_id` (`app.py` request models); `lang` resolves via
  `DEFAULT_PII_MODELS.get(lang)` (`model_registry.py:1033`) — no user path to
  `model_name`; `en` default model is `OpenMed/OpenMed-PII-SuperClinical-Small-44M-v1`
  (`pii_i18n.py:43`), a first-party checkpoint via the standard loader.

Reference clone retention: `_reference/` is local-only-ignored; keep for the
Stage-0/1/2 sessions, then refresh with `git fetch --tags` at execution time.
