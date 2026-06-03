# HealthAdvocate

**Free, local-first health toolkit that decodes medical bills, fights insurance denials, and translates clinical jargon into plain language — for patients who need an advocate on their own machine.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## What it is

HealthAdvocate is a self-hosted FastAPI web app with 17+ health-focused endpoints — symptom assessment, medical bill decoding, insurance denial appeal drafting, drug checking, discharge translation, appointment preparation, and more. It runs entirely on your machine using a dual-layer AI architecture: OpenMed NER extracts medical entities and PII, then a local LLM (via LM Studio) generates structured clinical assessments. The two layers cross-validate each other, and disagreements on urgency default to "high" for safety. No data leaves your device; family profiles and health tracks are in-memory only.

## Install / Quick start

**Prerequisites:** Python 3.10+, [LM Studio](https://lmstudio.ai/) with a medical model loaded (e.g. [Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3)).

```bash
git clone https://github.com/simongonzalezdc/healthadvocate.git
cd healthadvocate
pip install -r healthadvocate/requirements.txt
pip install openmed[hf]
```

Then start LM Studio's local server on port 1234 and run:

```bash
export LM_STUDIO_URL=http://localhost:1234/v1
uvicorn healthadvocate.app:app --host 127.0.0.1 --port 8080
```

Open **http://localhost:8080** in your browser. No sign-up, no API keys, no cloud.

## Usage

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
```

Every endpoint returns a consistent JSON response with `explanation`, `urgency`, `action_items`, `red_flags`, and a `validation` object showing NER vs. LLM agreement.

## Why / How it works

The healthcare system is overwhelming — bills are incomprehensible, insurance denials feel final, and discharge instructions are written in a language patients don't speak. HealthAdvocate's key design decision is a **dual-layer cross-validation architecture**: OpenMed's transformer-based NER extracts diseases, drugs, anatomy, and PII with confidence scores, then a local LLM generates a structured clinical assessment. If the two layers disagree on urgency (e.g. NER flags "chest pain" at 90%+ confidence but the LLM rates low), the system overrides to "high". PII is stripped before any text reaches the LLM — names become `[first_name] [last_name]`, SSNs become `[ssn]` — and the `pii_scrubbed` flag in every response confirms deidentification happened.

### Core features

| Feature | What it does |
|---------|-------------|
| Symptom Assessment | Describes urgency, possible conditions, and next steps with cross-validated safety |
| Insurance Denial Fighter | Identifies denial reason, builds appeal arguments, generates ready-to-send letter |
| Medical Bill Decoder | Extracts charges, flags suspicious/duplicate items, explains patient rights |
| Document Decoder | Translates lab results, referral letters, and visit notes to plain language |
| Drug Checker | Drug class, generic alternatives, side effects, safety warnings |
| Appointment Prep | Talking points, questions to ask, advocacy script for doctor visits |
| Discharge Translator | Medication schedule, warning signs, and follow-up steps in plain language |
| Second Opinion Brief | Structured, de-identified brief with key questions |
| Community Health Scanner | Evaluates credibility of health claims found online |
| Family Health Tracker | Manages conditions, medications, and allergies for the whole family |
| Health Tracks | Tracks ongoing health concerns with status updates over time |

### Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LM_STUDIO_URL` | `http://localhost:1234/v1` | LM Studio server URL |
| `MEDICAL_LLM_MODEL` | `meditron3-8b` | Model loaded in LM Studio |
| `HEALTHADVOCATE_ALLOW_ORIGINS` | `http://127.0.0.1:8080,http://localhost:8080` | CORS browser origins |

### Tech stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Pydantic |
| Medical NER | [OpenMed](https://github.com/maziyarpanahi/openmed) (HuggingFace Transformers) |
| LLM | [Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3) via [LM Studio](https://lmstudio.ai/) |
| Frontend | Vanilla HTML/CSS/JS with accessible design system (light + dark themes) |

> **Best-fit searches:** local health advocate app, medical bill decoder open source, insurance denial appeal generator, symptom checker local LLM, patient advocacy tool, private health assistant, offline medical NLP

## Links

- [AI/agent navigation (llms.txt)](llms.txt)
- [Changelog](CHANGELOG.md)
- [Credits & OpenMed citation](#credits)

## Credits

HealthAdvocate is built on outstanding open-source work:

- **[OpenMed](https://github.com/maziyarpanahi/openmed)** by [Maziyar Panahi](https://github.com/maziyarpanahi) — Apache 2.0 medical NLP toolkit powering NER, PII detection, and deidentification. [[Paper](https://arxiv.org/abs/2508.01630)]
- **[Meditron3-8B](https://huggingface.co/epfl-llm/meditron-3)** — open-weight clinical reasoning model by the EPFL LLM Team
- **[LM Studio](https://lmstudio.ai/)** — free local LLM runtime with OpenAI-compatible API
- **[FastAPI](https://fastapi.tiangolo.com/)** — high-performance async Python web framework

### Citing OpenMed

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

## License

[Apache License 2.0](LICENSE). OpenMed is a separate project used under its own [Apache 2.0 license](https://github.com/maziyarpanahi/openmed/blob/main/LICENSE).
