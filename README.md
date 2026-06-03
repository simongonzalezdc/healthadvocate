<div align="center">

# HealthAdvocate

### Your health deserves an advocate.

Navigate the medical system. Fight insurance denials. Decode bills. Understand your care.

**Free. Private. Runs on your machine.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/simongonzalezdc/healthadvocate?style=social)](https://github.com/simongonzalezdc/healthadvocate)

[Features](#features) · [How It Works](#how-it-works) · [Quick Start](#quick-start) · [API](#api-reference) · [Credits](#credits)

</div>

---

## The Problem

The healthcare system is overwhelming. Medical bills are incomprehensible. Insurance denials feel final. Discharge instructions are written in a language you don't speak. And every step of the way, you're expected to advocate for yourself — often when you're at your most vulnerable.

**HealthAdvocate exists to change that.**

It's a free, open-source tool that sits on your machine and helps you:
- Understand what your symptoms might mean — and how urgent they are
- Decode medical bills and spot suspicious charges
- Fight back when insurance denies your claim — with a drafted appeal letter
- Translate discharge instructions into language you can actually follow
- Prepare for doctor visits with talking points and questions to ask
- Check drug information, side effects, and cheaper alternatives
- Separate real health advice from misinformation online

**Your data stays on your device by default.** No accounts, no cloud service, no tracking, no telemetry. Ever.

---

## Features

### Symptom Assessment
Describe how you feel in your own words. Two AI layers — medical entity recognition and clinical reasoning — cross-validate each other to give you a reliable urgency assessment, possible conditions, and clear next steps. If they disagree on urgency, the system defaults to "high" for your safety.

### Insurance Denial Fighter
Paste your denial letter. HealthAdvocate identifies the denial reason, builds specific appeal arguments, and generates a ready-to-send appeal letter you can take straight to your insurer.

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
  [Local LLM] ── Generates structured clinical assessment (runs on your machine)
      |
      v
  [Cross-Validation] ── Compares NER findings vs LLM reasoning
      |                    Flags disagreements, scores reliability
      v
  Your result
```

**Layer 1 — OpenMed NER**: Extracts medical entities from your text using state-of-the-art transformer models. Identifies diseases, medications, anatomical terms, and personally identifiable information with confidence scores.

**Layer 2 — Local LLM**: Generates a structured assessment — urgency level, action items, red flags, and plain-language explanations. Runs entirely on your machine via LM Studio.

**Cross-validation**: Every result goes through a reliability check. If NER finds a high-urgency entity (like "chest pain" at 90%+ confidence) but the LLM rates urgency as "low", the system overrides to "high". Safety first, always.

**PII protection**: Before any text reaches the LLM, all personal identifiers are stripped. Names become `[first_name] [last_name]`, dates become `[date]`, SSNs become `[ssn]`. The `pii_scrubbed` flag in every response confirms this happened.

---

## Quick Start

### What you need

- **Python 3.10+**
- **[LM Studio](https://lmstudio.ai/)** — free app to run LLMs locally. Download a medical model like [Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3).
- **[OpenMed](https://github.com/maziyarpanahi/openmed)** — medical NLP toolkit (installed automatically)

### Install

```bash
git clone https://github.com/simongonzalezdc/healthadvocate.git
cd healthadvocate
pip install -r healthadvocate/requirements.txt
pip install openmed[hf]
```

### Run

1. Open LM Studio, load a medical model, start the local server (default port 1234)

2. Start HealthAdvocate:

```bash
export LM_STUDIO_URL=http://localhost:1234/v1
uvicorn healthadvocate.app:app --host 127.0.0.1 --port 8080
```

3. Open **http://localhost:8080** in your browser

That's it. No sign-up, no API keys, no cloud.

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
| `LM_STUDIO_URL` | `http://localhost:1234/v1` | Your LM Studio server URL |
| `MEDICAL_LLM_MODEL` | `meditron3-8b` | Model name loaded in LM Studio |
| `HEALTHADVOCATE_ALLOW_ORIGINS` | `http://127.0.0.1:8080,http://localhost:8080` | Comma-separated browser origins allowed by CORS |

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

---

## Privacy & Security

HealthAdvocate is designed as a privacy-preserving local-first health tool:

- **All processing is local by default.** No data is sent to a hosted HealthAdvocate service. The NER models run on your machine via HuggingFace. The LLM runs on your machine via LM Studio.
- **PII is stripped before reasoning.** Every patient-facing module deidentifies your text before it reaches the LLM. Names, dates, SSNs, phone numbers, emails, and addresses are masked using OpenMed's privacy-preserving PII detection.
- **No persistent storage.** Family profiles and health tracks are kept in memory only. When you stop the server, the data is gone. No database, no files, no data to breach.
- **Zero telemetry.** No analytics, no tracking pixels, no error reporting to external services. We wouldn't know how to find your data even if we wanted to.
- **Local network only by default.** The documented run command binds to `127.0.0.1`, and browser CORS defaults to localhost. If you expose the app on a network or public URL, add authentication and a tighter deployment review first.

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
| LLM | [Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3) via [LM Studio](https://lmstudio.ai/) | Clinical reasoning running locally |
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
```

---

## Known Limitations

- **In-memory storage**: Family profiles and health tracks live in memory and are lost on server restart. This is intentional — no persistent data means no data to breach.
- **Requires LM Studio**: You need LM Studio running with a loaded model. Without it, feature endpoints return errors.
- **LLM output quality**: Results depend on the model you choose. Meditron3-8B is a strong medical model, but no LLM is a substitute for a real doctor.

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

## License

This project is licensed under the [Apache License 2.0](LICENSE).

OpenMed is a separate project by Maziyar Panahi, used here as a dependency under its own [Apache 2.0 license](https://github.com/maziyarpanahi/openmed/blob/main/LICENSE).
