"""Coverage-journey loopback server with the repo's own InMemoryKeyStore test
double (the same injection the unit tests use) — the macOS keychain denies a
sandboxed server process. Serves tests/browser/focus-order-regression.js.

Synthetic data only. Cases land in a throwaway /tmp dir; the encryption key
lives in process memory only, so a persisted store cannot be re-opened by the
next run — delete the case dir between runs.

Run:  .venv/bin/python tests/browser/serve-coverage.py [port]   (default 8081)
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("HEALTHADVOCATE_MODEL_ENABLED", "0")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from healthadvocate.coverage import service as cov_service
from healthadvocate.coverage.keystore import InMemoryKeyStore

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
cases_dir = Path(os.environ.get("HA_CASES_DIR", f"/tmp/ha-focus-regression-{port}/cases"))
cases_dir.mkdir(parents=True, exist_ok=True)
cov_service.get_default_store(data_dir=cases_dir, keystore=InMemoryKeyStore())

import uvicorn

from healthadvocate.app import app

uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
