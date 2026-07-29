# HealthAdvocate

Open-source patient-advocacy web app (FastAPI) that turns confusing medical info into clear questions and next steps, with optional local-LLM support.

**Who it is for:** people navigating bills, insurance denials, discharge notes, and visit prep who want a private tool on their machine.

**What you get:** symptom assessment helpers, denial appeal drafts, bill decoding, visit prep, and drug info tools — **not** a doctor, diagnosis, or guaranteed coverage outcome.

## Quick start

```bash
git clone https://github.com/simongonzalezdc/healthadvocate.git
cd healthadvocate
# Python 3.10+ — create venv, install deps, run FastAPI app per in-tree scripts
pip install -r requirements.txt
# then start the app entrypoint documented in the package (uvicorn / scripts)
```

Default posture: data stays on-device; no accounts/telemetry claims beyond what the code actually enables.

## What it helps with

- Symptom narrative → urgency framing and questions (not diagnosis)
- Insurance denial letter → appeal draft starting point
- Medical bill lines → plain-language explanations and flags to review
- Visit prep talking points and discharge language cleanup

## Docs

- API and module docs in the source tree / in-app routes
- Site pointer: [kyanitelabs.tech](https://kyanitelabs.tech)

## License

MIT / Apache notes per [LICENSE](LICENSE). Not medical advice.
