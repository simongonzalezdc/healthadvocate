<div align="center">

## What it does

**HealthAdvocate is a free, open-source, local-first companion for people facing the
medical system** — everything runs on your device; nothing is sent anywhere.

- **Symptom check** — describe what you feel in your own words; get a plain-language
  read with urgency called out honestly, and next steps you can act on.
- **Appeal-letter generator** — bring a denial and your records; get a complete,
  editable appeal letter drafted locally, every machine-drafted claim labeled and
  traceable to a source. Download it, print it, send it.
- **Share-safe copy** — strip names, dates, phone numbers, and IDs from any document
  before you show it to a new doctor, an insurer, or a forum — with an exact count of
  what was removed.
- **Decoders** — documents, bills, discharge papers, drug labels: medical language
  translated into plain words.
- **Insurance & coverage** — fight denials, track appeals, keep your case file.
- **Library, directory, recorder** — every call, voicemail, and letter catalogued and
  cross-linked; providers fill in as you work.
- **Four warm color themes** (gold · rose · moss · blue) and a dark mode — the reading
  nook, not the clinic. Fully bilingual English/Español.

# HealthAdvocate

> HealthAdvocate is a health advocacy and patient-navigation tooling that helps people navigating healthcare systems and builders of advocacy tools advocate and navigate health workflows with structured support.

**TL;DR:** HealthAdvocate — health advocacy and patient-navigation tooling. Best for people navigating healthcare systems and builders of advocacy tools.

### Your health deserves an advocate.

A free, open-source tool to help people have some hope against the medical system.

Navigate the medical system. Fight insurance denials. Decode bills. Understand your care.

**Free. Private. Local-first. Runs on your machine.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/simongonzalezdc/healthadvocate?style=social)](https://github.com/simongonzalezdc/healthadvocate)

[Features](#features) · [How It Works](#how-it-works) · [Quick Start](#quick-start) · [API](#api-reference) · [Credits](#credits)

</div>

---

## The Problem

The healthcare system is overwhelming. Medical bills are incomprehensible. Insurance denials feel final. Discharge instructions are written in a language you don't speak. And every step of the way, you're expected to advocate for yourself — often when you're at your most vulnerable.

**HealthAdvocate exists to change that.**

It's a free, open-source tool that sits on your machine and helps you:
- Understand what your symptoms might mean — and how urgent they might be
- Decode medical bills and spot suspicious charges
- Fight back when insurance denies your claim — with a drafted appeal letter
- Translate discharge instructions into language you can actually follow
- Prepare for doctor visits with talking points and questions to ask
- Check drug information, side effects, and cheaper alternatives
- Separate real health advice from misinformation online

**Your data stays on your device by default.** No accounts, no cloud service, no tracking, no telemetry. Ever.

---

## Why this exists

The medical system is hard to fight alone, and the people it exhausts most are the ones with the least energy left to fight it. HealthAdvocate is a free tool to help people have some hope against the medical system — free, open source, and local-first, so cost and privacy are never the reason someone goes without support.

**What this is not:** it is not a doctor, not a diagnosis, and not verified medical advice. It prepares, explains, and drafts — you and your clinicians decide. If something feels like an emergency, contact emergency services.

---

## Features

The first nine features have two halves: a **deterministic half** (local entity extraction and preparation that always runs) and a **generative half** (drafts and plain-language explanations) that needs the optional local model. See [What works without a model](#what-works-without-a-model) for the exact split.

### Symptom Assessment
Describe how you feel in your own words. Two layers — local medical entity recognition and an optional local reasoning model — cross-check each other to surface possible conditions and next steps. When both are live and disagree on urgency, the system defaults to the conservative "high" for your safety. Without the model, entity extraction still runs and urgency reads honestly as unavailable rather than guessed.

### Insurance Denial Fighter
Paste your denial letter. HealthAdvocate identifies the denial reason, builds specific appeal arguments, and drafts an appeal letter you can take straight to your insurer.

### Medical Bill Decoder
Paste your bill. It extracts every charge, flags suspicious or duplicate items, explains what each line means, and tells you your rights as a patient.

### Document Decoder
Paste any medical document — lab results, referral letters, visit notes. Every medical term gets explained in plain language. Follow-up actions are laid out clearly.

### Drug Checker
Enter any drug name. Get the drug class, generic alternatives, common side effects, safety warnings, and a list of questions to bring to your doctor.

### Appointment Preparation
Going to the doctor? Describe what you want to discuss. HealthAdvocate generates talking points, questions to ask, and an advocacy script so you walk in prepared.

### Discharge Translator
Discharge instructions are notoriously hard to follow. Paste them and get a clear medication schedule, warning signs to watch for, and follow-up steps — all in plain language.

### Second Opinion Brief
Preparing for a second opinion? Paste your medical records and HealthAdvocate creates a structured, de-identified brief with key questions and records to bring.

### Community Health Scanner
Saw a health claim online? Paste it. HealthAdvocate evaluates credibility, provides scientific context, and tells you whether to act or ignore it.

### Family Health Tracker
Manage health profiles for your whole family — conditions, medications, allergies. This context flows into every other feature, so Drug Checker knows about interactions and Appointment Prep knows your history.

### Coverage Continuity Track
Lose employer coverage? Build a local-first Coverage Case that organizes deadlines, providers, medications, evidence, contacts, and prepared scripts. Encrypted at rest with a key from your OS credential store. The Commitment Gate blocks any payment, submission, plan change, message, or treatment change — the app prepares, you decide. The manual workflow runs without any model or external dataset; open-data adapters (RxNorm, DailyMed, openFDA, NPPES, NADAC, DrugCentral) are optional and each declares exactly what it can and cannot claim. Real-case import stays disabled until an independent verifier approves the exact build.
### Health Tracks

Track ongoing health concerns over time with status updates and notes. See what's active, what's being monitored, and what you've resolved.

---

## How It Works

HealthAdvocate uses a **dual-layer AI architecture** where two independent systems verify each other:

```
  Your input
      |
      v
  [OpenMed NER] ── Extracts diseases, drugs, anatomy, PII with confidence scores
      |
      v
  [PII Deidentification] ── Masks all personal data (names, SSN, dates, addresses)
      |
      v
  [Local LLM] ── Generates structured clinical assessment (optional, off by default)
      |
      v
  [Cross-Validation] ── Compares NER findings vs LLM reasoning
      |                    Flags disagreements, scores reliability
      v
  Your result
```

**Layer 1 — OpenMed NER**: Extracts medical entities from your text using state-of-the-art transformer models. Identifies diseases, medications, anatomical terms, and personally identifiable information with confidence scores. This layer is deterministic and always runs.

**Layer 2 — Local LLM** *(optional, off by default)*: Generates a structured assessment — urgency level, action items, red flags, and plain-language explanations. Runs entirely on your machine via any OpenAI-compatible loopback runtime (LM Studio, Ollama). It only goes live when you set `HEALTHADVOCATE_MODEL_ENABLED=1`.

**Cross-validation**: Every result goes through a reliability check. If NER finds a high-urgency entity (like "chest pain" at 80%+ confidence) but the LLM rates urgency as "low", the system overrides to "high". Safety first, always.

**PII protection**: Before any text reaches the LLM, all personal identifiers are stripped. Names become `[first_name] [last_name]`, dates become `[date]`, SSNs become `[ssn]`. The `pii_scrubbed` flag in every response confirms this happened.

---

## What works without a model

The model runtime is **opt-in and off by default**. With it off, every generative feature answers with the same honest fallback shape (`unavailable_structured_fallback` in `healthadvocate/core/llm_client.py`): a summary that says the optional local model is unavailable, action items pointing at the manual workflows, empty red flags, and a `_model_blocked: true` marker. **Urgency shows an honest "unavailable" state — never a guessed level.** The one exception is deliberate: when the local entity-detection layer flags emergency-class terms (e.g. chest pain) at high confidence, urgency escalates to "high" on ANY build, model or not — the emergency signal never depends on the optional model. On the symptom surface the typed decision layer routes that no-judgment state through a `NEEDS_HUMAN` wrapper, which the UI renders as a "Human decision needed" banner (reason, gate state, next steps, and an emergency-services line) — safety legs that involve a real or unrejected judgment (unparseable model output, deidentification failure, urgency disagreement) still escalate to conservative "high". No endpoint errors out; deterministic preparation keeps working.

| Feature | Deterministic — works with no model | Generative — needs `HEALTHADVOCATE_MODEL_ENABLED=1` |
|---------|-------------------------------------|------------------------------------------------------|
| Symptom Assessment | Condition/drug entity extraction with confidence scores; deidentification | Plain-language assessment, possible conditions, specialist suggestion; urgency assessment |
| Insurance Denial Fighter | Entity extraction from the denial letter; deidentification | Denial-reason classification, appeal arguments, draft appeal letter |
| Medical Bill Decoder | Charge extraction with line items and totals; entity extraction | Suspicious-charge flags, billing-rights explanations, plain-language summary |
| Document Decoder | Medical-term and PII entity extraction (diseases, drugs, anatomy) | Plain-language explanation, term explanations, follow-up actions |
| Drug Checker | Drug-name verification via NER | Drug class, generic availability, side effects, warnings, doctor questions |
| Appointment Prep | Entity extraction from your symptoms and concerns | Talking points, questions to ask, advocacy script |
| Discharge Translator | Medication, condition, and anatomy detection | Plain-language instructions, medication schedule, warning signs |
| Second Opinion Brief | De-identified records output; entity extraction | Structured brief, key questions, records-to-bring list |
| Community Health Scanner | Claim entity extraction | Credibility read, scientific context, recommended action |
| Family Health Tracker | Fully functional — no model involved (profiles live in memory) | — |
| Health Tracks | Fully functional — no model involved (in memory) | — |
| Coverage Continuity Track | Fully functional — manual workflow, encrypted local cases, scripts, Commitment Gate; no model, no external dataset | — |
| CLI (`python -m healthadvocate.cli`) | Fully functional — project brief, visit questions, denial checklists, server health | — |
| MCP server (`python -m healthadvocate.mcp_server`) | Fully functional — preparation tools only | — |

The optional open-data adapters (RxNorm, DailyMed, openFDA, NPPES, NADAC, DrugCentral) are separate from the model runtime: they are off unless invoked and each declares exactly what it can and cannot claim.

---

## Quick Start

### What you need

- **Python 3.11+**
- **[OpenMed](https://github.com/maziyarpanahi/openmed)** — medical NLP toolkit (installed automatically). Runs locally; powers the always-on entity extraction.
- **Optional: an OpenAI-compatible local model runtime** — e.g. [LM Studio](https://lmstudio.ai/) or Ollama, loaded with a model like [Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3). Needed only for the generative half of the features; everything in the deterministic column of [What works without a model](#what-works-without-a-model) runs without it.>>>>>>> 4c38f56 (docs(honesty): README tells one true story — no-model table, real env vars, why-this-exists (Lane C))

### Install

```bash
git clone https://github.com/simongonzalezdc/healthadvocate.git
cd healthadvocate
pip install -r healthadvocate/requirements.txt
pip install openmed[hf]
```

### Run

1. Start HealthAdvocate:

```bash
uvicorn healthadvocate.app:app --host 127.0.0.1 --port 8080
```

2. Open **http://localhost:8080** in your browser. Deterministic features (entity extraction, bill charge extraction, Coverage workflow, CLI, MCP) work immediately — generative features answer with their honest unavailable fallback.

3. Optional — make the generative features live. Start your local runtime with a loaded model, then point HealthAdvocate at it:

```bash
export HEALTHADVOCATE_MODEL_ENABLED=1
export HEALTHADVOCATE_MODEL_URL=http://localhost:1234/v1   # LM Studio; Ollama serves http://127.0.0.1:11434/v1
export MEDICAL_LLM_MODEL=meditron3-8b                       # the name of the model you actually loaded
```

`LM_STUDIO_URL` still works as a deprecated alias for `HEALTHADVOCATE_MODEL_URL`. The model URL must be loopback (`127.0.0.1`/`localhost`) — anything else is rejected fail-closed, and the runtime stays off until you set `HEALTHADVOCATE_MODEL_ENABLED=1`.

That's it. No sign-up, no API keys, no cloud.>>>>>>> 4c38f56 (docs(honesty): README tells one true story — no-model table, real env vars, why-this-exists (Lane C))

### CLI, MCP, and Agent Skill

HealthAdvocate also exposes safety-bounded agent surfaces for local preparation workflows:

```bash
python -m healthadvocate.cli brief
python -m healthadvocate.cli visit-questions --concern "persistent dizziness"
python -m healthadvocate.cli denial-checklist --denial-reason "not medically necessary"
python -m healthadvocate.cli server-health --url http://127.0.0.1:8080
python -m healthadvocate.mcp_server
```

- CLI: `python -m healthadvocate.cli` prepares visit questions, denial checklists, and server health checks.
- MCP: `python -m healthadvocate.mcp_server` starts a stdio MCP server for compatible agent hosts.
- Skill: [`skills/healthadvocate/SKILL.md`](skills/healthadvocate/SKILL.md) tells agents how to help patients prepare without diagnosing or replacing professional care.

Example MCP config:

```json
{
  "mcpServers": {
    "healthadvocate": {
      "command": "python",
      "args": ["-m", "healthadvocate.mcp_server"]
    }
  }
}
```

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HEALTHADVOCATE_MODEL_ENABLED` | `0` (off by default) | Master switch for the generative features. Off: generative surfaces return the honest unavailable fallback. Set `1` to make them live (a valid loopback model URL is still required). |
| `HEALTHADVOCATE_MODEL_URL` | `http://127.0.0.1:11434/v1` | Base URL of the OpenAI-compatible local model runtime. Must be loopback (`127.0.0.1`/`localhost`); non-loopback hosts and HTTP redirects are rejected fail-closed. |
| `LM_STUDIO_URL` | unset | Deprecated alias for `HEALTHADVOCATE_MODEL_URL`, kept for compatibility. |
| `MEDICAL_LLM_MODEL` | `local-model` | Model name sent to the runtime — set it to the model you actually loaded (e.g. `meditron3-8b`). |
| `HEALTHADVOCATE_ALLOW_ORIGINS` | `http://127.0.0.1:8080,http://localhost:8080` | Comma-separated browser origins allowed by CORS |>>>>>>> 4c38f56 (docs(honesty): README tells one true story — no-model table, real env vars, why-this-exists (Lane C))
| `HEALTHADVOCATE_ALLOW_ORIGINS` | `http://127.0.0.1:8080,http://localhost:8080` | Comma-separated browser origins allowed by CORS |
| `HEALTHADVOCATE_BIND_HOST` | `127.0.0.1` | Host the app binds to. Validated at startup: anything that is not a loopback name/address makes the process refuse to start (fail-closed), which is what enforces the loopback-deployment default. |
| `HEALTHADVOCATE_CASE_DIR` | unset → `~/Library/Application Support/HealthAdvocate/cases` | Directory for encrypted Coverage Case storage (key stays in your OS credential store). |
| `HEALTHADVOCATE_CMS_TIC_ENABLED` | `0` (off) | Feature flag for the optional CMS Transparency in Coverage research adapter — disabled until measured resource budgets replace the placeholder limits. |
| `HEALTHADVOCATE_POLICYENGINE_ENABLED` | `0` (off) | Feature flag for the unofficial, local-only PolicyEngine-style eligibility estimate (deterministic stub; no network, no submission). |>>>>>>> ed14a17 (fix(honesty): model-off urgency is an honest 'unavailable', not an alarm; NEEDS_HUMAN wrapper rendered; 2 XSS escapes; docs complete)

---

## API Reference

All endpoints accept and return JSON. Perfect for building integrations, bots, or custom frontends.

### Core Features

```bash
# Symptom check
curl -X POST http://localhost:8080/api/symptoms/assess \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "persistent headache and dizziness for a week"}'

# Decode a medical bill
curl -X POST http://localhost:8080/api/bills/decode \
  -H "Content-Type: application/json" \
  -d '{"bill_text": "ER Visit: EKG $450, Blood Work $125, X-Ray $275"}'

# Fight an insurance denial
curl -X POST http://localhost:8080/api/insurance/fight \
  -H "Content-Type: application/json" \
  -d '{"denial_text": "Your claim for MRI has been denied..."}'

# Check a drug
curl -X POST http://localhost:8080/api/drugs/check \
  -H "Content-Type: application/json" \
  -d '{"drug_name": "metformin"}'
```

### All Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/symptoms/assess` | Symptom analysis with urgency and cross-validation |
| `POST` | `/api/documents/decode` | Medical document translation to plain language |
| `POST` | `/api/bills/decode` | Bill analysis with charge extraction and flagging |
| `POST` | `/api/insurance/fight` | Denial analysis with appeal letter generation |
| `POST` | `/api/drugs/check` | Drug lookup with side effects and alternatives |
| `POST` | `/api/appointments/prepare` | Doctor visit preparation with talking points |
| `POST` | `/api/discharge/translate` | Discharge instruction translation |
| `POST` | `/api/second-opinion/create` | Second opinion brief generation |
| `POST` | `/api/community/scan` | Health bulletin credibility analysis |
| `POST` | `/api/family/profiles` | Create family health profile |
| `GET` | `/api/family/profiles` | List all profiles |
| `POST` | `/api/family/profiles/{id}/conditions` | Add condition to profile |
| `POST` | `/api/family/profiles/{id}/medications` | Add medication to profile |
| `POST` | `/api/tracks` | Start tracking a health concern |
| `GET` | `/api/tracks/dashboard` | Track dashboard overview |
| `GET` | `/api/coverage/status` | Coverage Continuity Track manual workflow availability |
| `GET` | `/api/coverage/cases` | List local Coverage Cases |
| `POST` | `/api/coverage/cases` | Create a synthetic Coverage Case |
| `GET` | `/api/coverage/cases/{id}` | Retrieve a Coverage Case |
| `PATCH` | `/api/coverage/cases/{id}` | Update a Coverage Case title or next action |
| `POST` | `/api/coverage/cases/{id}/resume` | Resume a Coverage Case across restarts |
| `POST` | `/api/coverage/cases/{id}/view` | Build the low-energy Coverage view |
| `POST` | `/api/coverage/cases/{id}/scripts/{kind}` | Deterministic county/provider/billing/pharmacy script |
| `POST` | `/api/coverage/cases/{id}/export` | Private or redacted export of a Coverage Case |
| `POST` | `/api/coverage/cases/{id}/delete` | Delete a Coverage Case and report unowned sources |
| `POST` | `/api/coverage/commitment-gate` | Review-only gate for payment/submit/message/treatment intents |
| `POST` | `/api/coverage/cases/{id}/evidence` | Add immutable Evidence Item (real-case import disabled by default) |
| `POST` | `/api/coverage/cases/{id}/facts` | Add a typed Fact with Fact Status and provenance |
| `POST` | `/api/coverage/cases/{id}/targets` | Add a Continuity Target (provider or medication) |
| `POST` | `/api/coverage/cases/{id}/contacts` | Append a Contact Event |
| `POST` | `/api/coverage/adapters/{rxnorm,dailymed,openfda,nppes,nadac,drugcentral}` | Optional open-data adapter with narrow claim contract |

### Response Format

Every feature endpoint returns a consistent structure:

```json
{
  "explanation": "Plain-language summary written for the patient",
  "urgency": "high",
  "action_items": ["Call your doctor within 24 hours", "..."],
  "red_flags": ["Seek emergency care immediately if..."],
  "pii_scrubbed": true,
  "validation": {
    "confirmed": ["headache", "dizziness"],
    "ner_only": [],
    "llm_only": ["possible migraine"],
    "reliability": "high",
    "urgency_disagreement": false
  }
}
```

Module-specific fields (like `suspicious_charges`, `draft_appeal`, `medication_instructions`) are included alongside these common fields.

When the model runtime is off (the default), generative endpoints do not error — they answer with the honest unavailable fallback described in [What works without a model](#what-works-without-a-model): the unavailable summary, manual-workflow action items, empty red flags, and `_model_blocked: true`. The symptom surface additionally returns `urgency_decision` — the typed decision wrapper — and when it says `NEEDS_HUMAN` (as it does whenever no automated assessment ran), the UI renders a "Human decision needed" banner with the wrapper's reason, gate state, and next steps.

---

## Threat model & honest boundaries

`docs/THREAT-MODEL.md` names the adversaries and accident classes and states
what is controlled versus assumed. Two boundaries stated plainly here:
**the model runtime is opt-in** — the documented quick start runs fully
deterministic/local with generative features in their fallback mode until a
loopback model runtime is configured (see
[What works without a model](#what-works-without-a-model)) — and **every
text box is synthetic-only by policy until the real-case era**: the release
gate (real-case import disabled, independent-verifier pending) is enforced on
the coverage store; free-text surfaces rely on that policy, not yet on
enforcement.

### What works with the model runtime off (the default build)

| Capability | Model off (default) | Model on |
|------------|--------------------|----------|
| Medical NER extraction & confidence scores | Works | Works |
| PII masking before any reasoning | Works | Works |
| Symptom-triage urgency | `unavailable` — no level is fabricated; NER high-urgency findings (e.g. "chest pain" at ≥80% confidence) still escalate to HIGH | Full structured urgency |
| Symptom explanations, action items, red flags | Deterministic fallback copy | Model-authored |
| Other LLM-assisted decoders & prep tools | Deterministic fallback copy | Model-authored |
| Coverage workflows, encrypted case store, Commitment Gate | Works (no model involved) | Works |
| Optional open-data adapters (RxNorm, DailyMed, openFDA, …) | Works (no model involved) | Works |

## Privacy & Security

HealthAdvocate is designed as a privacy-preserving local-first health tool:

- **All processing is local by default.** No data is sent to a hosted HealthAdvocate service. The NER models run on your machine via HuggingFace. The LLM runs on your machine via LM Studio.
- **PII is stripped before reasoning.** Every patient-facing module deidentifies your text before it reaches the LLM. Names, dates, SSNs, phone numbers, emails, and addresses are masked using OpenMed's privacy-preserving PII detection.
- **Private local persistence for Coverage Continuity.** Family profiles and health tracks remain in memory, while synthetic Coverage Continuity cases are stored locally as an encrypted file with a key held by the operating-system credential store. Real-case import remains disabled behind the release gate.
- **Zero telemetry.** No analytics, no tracking pixels, no error reporting to external services. We wouldn't know how to find your data even if we wanted to.
- **Loopback deployment by default.** The documented local command binds to `127.0.0.1`, and the supported Compose profile publishes the container only on `127.0.0.1`. The image's internal server listens on its container interface so Compose port forwarding works; running or publishing the image outside that profile carries no loopback-exposure guarantee and requires a separate deployment review. Browser CORS defaults to localhost.
- **Coverage Cases are encrypted at rest.** Coverage data lives outside the source repository, encrypted with a key held in your OS credential store. Missing or wrong keys fail before any case metadata is returned. Deletion reports any unowned source files it could not remove.
- **Commitment Gate by design.** Pay, submit, withdraw, change plan, cancel, message, and treatment-change intents are review-only. The first release ships no capable outbound adapter for those actions.

---

## Accessibility

The UI uses accessibility-minded patterns because health tools should work for everyone:

- Skip-to-content link as the first focusable element
- `aria-live` regions on all result containers for screen reader announcements
- Screen-reader-only labels on every form input
- `:focus-visible` styles for keyboard navigation
- `prefers-reduced-motion` media query support
- Color choices are selected for readable contrast in light and dark themes
- `role="img"` on all decorative SVGs
- Semantic HTML throughout (`<main>`, `<nav>`, `<header>`, `<footer>`)

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [Pydantic](https://docs.pydantic.dev/) | Fast async Python API with type-safe validation |
| Medical NER | [OpenMed](https://github.com/maziyarpanahi/openmed) | State-of-the-art medical entity extraction, 12+ models |
| LLM | Any OpenAI-compatible loopback runtime (e.g. [LM Studio](https://lmstudio.ai/), Ollama); [Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3) suggested | Clinical reasoning running locally — optional and off by default |
| Frontend | Vanilla HTML/CSS/JS | Zero dependencies, fast load, works everywhere |
| Design | Custom humanistic design system | Light and dark themes, warm and accessible |

---

## Project Structure

```
healthadvocate/
  app.py                  FastAPI app, 17+ endpoints, request validation
  requirements.txt        Python dependencies (fastapi, openai, openmed)
  static/
    index.html            SPA with accessibility-minded markup
    styles.css            Humanistic design system (light + dark themes)
    app.js                Frontend logic with loading states and XSS protection
  core/
    engine.py             OpenMed model management, PII deidentification
    llm_client.py         LM Studio client with multi-strategy JSON parsing
    cross_validation.py   NER vs LLM reliability scoring
    symptom_assessor.py   Symptom assessment with urgency cross-check
    document_decoder.py   Medical document plain-language decoder
    bill_decoder.py       Bill analysis with price extraction and context
    insurance_fighter.py  Denial analysis and appeal letter generator
    drug_checker.py       Drug information with interaction checking
    appointment_prep.py   Doctor visit preparation with advocacy scripts
    discharge_translator.py  Discharge instruction plain-language translator
    second_opinion.py     Second opinion brief with de-identification
    community_health.py   Health bulletin credibility scanner
    family_tracker.py     Family health profile management
    health_tracks.py      Health concern tracking over time
  coverage/                 Local-first Coverage Continuity Track (case, evidence, gate, scripts)
  privacy/                  Loopback-only defaults, gated model, PHI redaction
  governance/               Open license/provenance gate + real-case release gate
  adapters/                 Optional open-data adapters (RxNorm, DailyMed, openFDA, NPPES, NADAC, DrugCentral)
```

---

## Known Limitations

- **In-memory storage**: Family profiles and health tracks live in memory and are lost on server restart. This is intentional — no persistent data means no data to breach.
- **Generative features are opt-in**: without `HEALTHADVOCATE_MODEL_ENABLED=1` and a loopback model runtime, generative surfaces return the honest unavailable fallback — never a raw error, never a guessed answer — while deterministic preparation (entity extraction, bill charge extraction, Coverage workflow, CLI, MCP) keeps working. See [What works without a model](#what-works-without-a-model).
- **LLM output quality**: Results depend on the model you choose and run locally. Meditron3-8B is a reasonable open clinical-reasoning model, but no LLM is a substitute for a real doctor, and nothing here is verified medical advice.>>>>>>> 4c38f56 (docs(honesty): README tells one true story — no-model table, real env vars, why-this-exists (Lane C))

---

## Credits

HealthAdvocate is built on outstanding open-source work:

- **[OpenMed](https://github.com/maziyarpanahi/openmed)** by [Maziyar Panahi](https://github.com/maziyarpanahi) — Apache 2.0 licensed medical NLP toolkit. Powers the NER entity extraction, PII detection, and deidentification layers. [[Paper](https://arxiv.org/abs/2508.01630)]
- **[Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3)** by the EPFL LLM Team — open-weight clinical reasoning model. Powers the structured assessment layer.
- **[LM Studio](https://lmstudio.ai/)** — free local LLM runtime with an OpenAI-compatible API.
- **[FastAPI](https://fastapi.tiangolo.com/)** by [Sebastian Ramirez](https://github.com/tiangolo) — high-performance async Python web framework.
- **[HuggingFace Transformers](https://huggingface.co/docs/transformers)** — the model inference backend behind OpenMed's NER pipelines.

### Citing OpenMed

If you reference this project in academic work, please cite OpenMed:

```bibtex
@misc{panahi2025openmedneropensourcedomainadapted,
      title={OpenMed NER: Open-Source, Domain-Adapted State-of-the-Art Transformers for Biomedical NER Across 12 Public Datasets},
      author={Maziyar Panahi},
      year={2025},
      eprint={2508.01630},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2508.01630},
}
```

---

## Links

- **KyaniteLabs:** [kyanitelabs.tech](https://kyanitelabs.tech)
- **AI / agent navigation:** [llms.txt](llms.txt)
- **Sibling projects:** [Print-OS](https://github.com/simongonzalezdc/Print-OS) · [GameStory-Lab](https://github.com/simongonzalezdc/GameStory-Lab) · [voice-to-sculpture-app](https://github.com/simongonzalezdc/voice-to-scultpure-app) · [CyberWitches](https://github.com/simongonzalezdc/CyberWitches) · [grocery-flywheel](https://github.com/simongonzalezdc/grocery-flywheel)

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

OpenMed is a separate project by Maziyar Panahi, used here as a dependency under its own [Apache 2.0 license](https://github.com/maziyarpanahi/openmed/blob/main/LICENSE).

<!-- s-plus-geo:start -->

## What is HealthAdvocate?

**HealthAdvocate** is a **health advocacy and patient-navigation tooling** that helps **people navigating healthcare systems and builders of advocacy tools** **advocate and navigate health workflows with structured support**.

| | |
| --- | --- |
| **Product** | HealthAdvocate |
| **Category** | health advocacy and patient-navigation tooling |
| **Best for** | people navigating healthcare systems and builders of advocacy tools |
| **Not** | a medical device or clinical diagnosis product |
| **Price** | Free, open source (Apache-2.0); runs local-first on your machine |
| **Source** | [GitHub](https://github.com/simongonzalezdc/healthadvocate) · [Forgejo](https://git.kyanitelabs.tech/simon/healthadvocate) |
| **Keywords** | health advocate, patient navigation tool |

## Who it's for

- Primary: people navigating healthcare systems and builders of advocacy tools
- Use when you need to advocate and navigate health workflows with structured support
- Skip if you need a medical device or clinical diagnosis product

## FAQ

### What is HealthAdvocate?

HealthAdvocate is a health advocacy and patient-navigation tooling. It helps people navigating healthcare systems and builders of advocacy tools advocate and navigate health workflows with structured support.

### Who should use HealthAdvocate?

people navigating healthcare systems and builders of advocacy tools.

### How is HealthAdvocate different?

Advocacy/navigation tooling — not a clinic or diagnostic device.

### Is HealthAdvocate production software?

Treat the README status and release tags as source of truth for maturity. Validate against your own requirements before production use.

## Status

- Maintained as of 2026 on the default branch
- Prefer release tags when pinning dependencies
- Report issues on the canonical remote listed above

## Agent surface

- Coding agents: read this README first, then repo docs/`AGENTS.md` if present
- Prefer machine-readable briefs (`llms.txt`) when the repo ships one
- MCP or skill entrypoints are documented in-repo when applicable

## Contributing

Issues and PRs welcome on the canonical remote. Keep public docs free of secrets and machine-local paths.

## License

See [LICENSE](LICENSE) in this repository (or package metadata if license is package-only).

<!-- s-plus-geo:end -->
