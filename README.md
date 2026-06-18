<div align="center">

# HealthAdvocate

### Your health deserves an advocate.

**AI-powered health advocacy tool** that helps you navigate the medical system, fight insurance denials, decode medical bills, and understand your care — all from your own machine.

Built with **Python**, **FastAPI**, and **OpenMed** medical NLP.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/simongonzalezdc/healthadvocate?style=social)](https://github.com/simongonzalezdc/healthadvocate)

[Features](#features) · [Quick Start](#quick-start) · [API](#api-reference) · [FAQ](#faq) · [Contributing](#contributing)

</div>

---

## What Is This?

HealthAdvocate is a **free, open-source medical bill decoder and insurance denial fighter** that runs entirely on your local machine. It combines medical entity recognition (NER) with clinical reasoning to help you understand symptoms, decode medical documents, fight insurance denials, and prepare for doctor visits.

**Your data never leaves your device.** No accounts, no cloud service, no tracking, no telemetry. Ever.

### Who It's For

- Patients overwhelmed by medical bills, insurance letters, or discharge instructions
- Caregivers managing health information for family members
- Anyone who wants to understand their healthcare better — without a medical degree

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
Paste discharge instructions and get a clear medication schedule, warning signs to watch for, and follow-up steps — all in plain language.

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
      │
      ▼
  ┌─────────────────────────────────────────┐
  │  OpenMed NER                            │
  │  Extracts diseases, drugs, anatomy, PII │
  │  with confidence scores                 │
  └─────────────────┬───────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────────┐
  │  PII Deidentification                   │
  │  Masks names, SSN, dates, addresses     │
  └─────────────────┬───────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────────┐
  │  Local LLM (via LM Studio)             │
  │  Generates structured clinical          │
  │  assessment on your machine             │
  └─────────────────┬───────────────────────┘
                    │
                    ▼
  ┌─────────────────────────────────────────┐
  │  Cross-Validation                       │
  │  Compares NER findings vs LLM reasoning │
  │  Flags disagreements, scores reliability│
  └─────────────────┬───────────────────────┘
                    │
                    ▼
              Your result
```

**Layer 1 — OpenMed NER**: Extracts medical entities using state-of-the-art transformer models. Identifies diseases, medications, anatomical terms, and PII with confidence scores.

**Layer 2 — Local LLM**: Generates a structured assessment — urgency level, action items, red flags, and plain-language explanations. Runs entirely on your machine via LM Studio.

**Cross-validation**: If NER finds a high-urgency entity (like "chest pain" at 90%+ confidence) but the LLM rates urgency as "low", the system overrides to "high". Safety first, always.

**PII protection**: Before any text reaches the LLM, all personal identifiers are stripped. The `pii_scrubbed` flag in every response confirms this happened.

---

## Installation

### Prerequisites

- **Python 3.10+**
- **[LM Studio](https://lmstudio.ai/)** — free app to run LLMs locally
- **A medical model** loaded in LM Studio (e.g., [Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3))

### Install from Source

```bash
git clone https://github.com/simongonzalezdc/healthadvocate.git
cd healthadvocate
pip install -r healthadvocate/requirements.txt
pip install openmed[hf]
```

### Install with Docker

```bash
git clone https://github.com/simongonzalezdc/healthadvocate.git
cd healthadvocate
docker-compose up --build
```

This starts the FastAPI server on port 8080. You still need LM Studio running locally with a medical model loaded.

---

## Quick Start

### 1. Start LM Studio

Open LM Studio, download a medical model (e.g., Meditron3-8B), and start the local server. Default port is `1234`.

### 2. Start HealthAdvocate

```bash
export LM_STUDIO_URL=http://localhost:1234/v1
uvicorn healthadvocate.app:app --host 127.0.0.1 --port 8080
```

### 3. Open the App

Navigate to **http://localhost:8080** in your browser.

That's it. No sign-up, no API keys, no cloud.

---

## Usage

### Web Interface

Open **http://localhost:8080** after starting the server. The interface provides access to all features — symptom assessment, bill decoding, insurance denial appeals, and more.

### Command-Line Interface (CLI)

HealthAdvocate includes a CLI for common preparation tasks:

```bash
# Generate a brief for a doctor visit
python -m healthadvocate.cli brief

# Prepare visit questions for a specific concern
python -m healthadvocate.cli visit-questions --concern "persistent dizziness"

# Create a denial checklist
python -m healthadvocate.cli denial-checklist --denial-reason "not medically necessary"

# Check server health
python -m healthadvocate.cli server-health --url http://127.0.0.1:8080
```

### MCP Server

HealthAdvocate exposes a Model Context Protocol (MCP) server for integration with compatible AI agent hosts:

```bash
python -m healthadvocate.mcp_server
```

Example MCP configuration for agent hosts:

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

### Agent Skill

The file [`skills/healthadvocate/SKILL.md`](skills/healthadvocate/SKILL.md) defines a skill that teaches AI agents how to help patients prepare for medical interactions — without diagnosing or replacing professional care.

### API

All endpoints accept and return JSON. See the [API Reference](#api-reference) below.

---

## API Reference

### Base URL

```
http://localhost:8080/api
```

### Symptom Assessment

```bash
curl -X POST http://localhost:8080/api/symptoms/assess \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "persistent headache and dizziness for a week"}'
```

### Medical Bill Decoder

```bash
curl -X POST http://localhost:8080/api/bills/decode \
  -H "Content-Type: application/json" \
  -d '{"bill": "your medical bill text here"}'
```

### Insurance Denial Appeal

```bash
curl -X POST http://localhost:8080/api/denials/appeal \
  -H "Content-Type: application/json" \
  -d '{"denial_letter": "your denial letter text here"}'
```

### Document Decoder

```bash
curl -X POST http://localhost:8080/api/documents/decode \
  -H "Content-Type: application/json" \
  -d '{"document": "your medical document text here"}'
```

### Drug Checker

```bash
curl -X POST http://localhost:8080/api/drugs/check \
  -H "Content-Type: application/json" \
  -d '{"drug_name": "metformin"}'
```

### Appointment Preparation

```bash
curl -X POST http://localhost:8080/api/appointments/prepare \
  -H "Content-Type: application/json" \
  -d '{"concern": "persistent dizziness", "symptoms": "lightheadedness when standing"}'
```

### Response Format

All responses include a `pii_scrubbed` boolean flag confirming that personal identifiers were removed before processing.

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LM_STUDIO_URL` | `http://localhost:1234/v1` | Your LM Studio server URL |
| `MEDICAL_LLM_MODEL` | `meditron3-8b` | Model name loaded in LM Studio |
| `HEALTHADVOCATE_ALLOW_ORIGINS` | `http://127.0.0.1:8080,http://localhost:8080` | Comma-separated browser origins allowed by CORS |

---

## FAQ

### Does HealthAdvocate replace my doctor?

**No.** HealthAdvocate is a preparation and education tool. It helps you understand medical information, prepare for appointments, and navigate the healthcare system. It does not diagnose conditions, prescribe treatments, or replace professional medical advice. Always consult a healthcare provider for medical decisions.

### Is my health data private?

**Yes.** HealthAdvocate runs entirely on your local machine. Your data never leaves your device. There is no cloud service, no accounts, no tracking, and no telemetry. All personal identifiers (names, SSNs, dates, addresses) are scrubbed before any processing occurs.

### What hardware do I need?

HealthAdvocate itself is lightweight. The main requirement is a machine capable of running a local LLM via [LM Studio](https://lmstudio.ai/). Most modern laptops with 8GB+ RAM can run smaller medical models. For best results with larger models like Meditron3-8B, 16GB+ RAM and a GPU with 8GB+ VRAM are recommended.

### Can I use a different LLM backend?

Yes. HealthAdvocate connects to any OpenAI-compatible API endpoint. Set `LM_STUDIO_URL` to point to your preferred backend. Compatible options include LM Studio, Ollama (with OpenAI compatibility mode), and other local inference servers.

### What medical models work best?

[