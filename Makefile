# HealthAdvocate developer targets.
# CI (Forgejo/GitHub workflow) runs the python suite; these targets drive the
# local loopback-browser batteries that need node+playwright (not in CI).

PY ?= .venv/bin/python
PORT_A ?= 8080
PORT_B ?= 8081
NODE_PATH ?= /opt/homebrew/lib/node_modules
PLAYWRIGHT_BROWSERS_PATH ?= /Users/simongonzalezdecruz/workspaces/.cache/playwright
CASES_DIR ?= /tmp/ha-ax-coverage-cases

# Clean-room HTTP acceptance gate (audit 2026-09-24 remediation 4).
# Boots the documented runtime through fastapi.testclient and drives every
# named route in BOTH model-failure (default env) and model-success (an
# in-process loopback OpenAI-compatible fake server) modes. Mirrors CI
# Gate 2.5. Loopback only; synthetic data only; no new dependencies.
.PHONY: acceptance
acceptance:
	$(PY) -m pytest tests/acceptance/ -q

# Machine announcement-equivalent AX audit (screen-reader-half a11y gate).
# Boots both loopback servers from this checkout, runs
# tests/browser/ax-audit.js, tears everything down. Exit 0 = all journeys
# PASS (advisories allowed). Result JSON: /tmp/ha-ax-audit-result.json
# (override with AX_OUT). Loopback only; synthetic data only.
.PHONY: a11y-ax
a11y-ax:
	@set -e; \
	trap 'rc=$$?; kill $$SRV_A $$SRV_B 2>/dev/null || true; sleep 1; kill -9 $$SRV_A $$SRV_B 2>/dev/null || true; \
	      rm -rf $(CASES_DIR); \
	      lsof -iTCP:$(PORT_A) -sTCP:LISTEN || true; lsof -iTCP:$(PORT_B) -sTCP:LISTEN || true; \
	      exit $$rc' EXIT; \
	rm -rf $(CASES_DIR); \
	HEALTHADVOCATE_MODEL_ENABLED=0 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
	  $(PY) -m uvicorn healthadvocate.app:app --host 127.0.0.1 --port $(PORT_A) \
	  >/tmp/ha-ax-server-a.log 2>&1 & \
	  SRV_A=$$!; \
	HA_CASES_DIR=$(CASES_DIR) $(PY) tests/browser/serve-coverage.py $(PORT_B) \
	  >/tmp/ha-ax-server-b.log 2>&1 & \
	  SRV_B=$$!; \
	for i in $$(seq 1 40); do \
	  curl -sf http://127.0.0.1:$(PORT_A)/api/health >/dev/null && \
	  curl -sf http://127.0.0.1:$(PORT_B)/api/health >/dev/null && break; \
	  sleep 1; \
	done; \
	curl -sf http://127.0.0.1:$(PORT_A)/api/health >/dev/null || { echo 'server A failed to start (log: /tmp/ha-ax-server-a.log)'; exit 1; }; \
	curl -sf http://127.0.0.1:$(PORT_B)/api/health >/dev/null || { echo 'server B failed to start (log: /tmp/ha-ax-server-b.log)'; exit 1; }; \
	AX_BASE=$${AX_BASE:-http://127.0.0.1:$(PORT_A)} AX_COV=$${AX_COV:-http://127.0.0.1:$(PORT_B)} AX_OUT=$${AX_OUT:-/tmp/ha-ax-audit-result.json} \
	NODE_PATH=$(NODE_PATH) PLAYWRIGHT_BROWSERS_PATH=$${PLAYWRIGHT_BROWSERS_PATH:-$(PLAYWRIGHT_BROWSERS_PATH)} node tests/browser/ax-audit.js
