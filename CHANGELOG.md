# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CLI surfaces for appointment prep, denial checklists, and server health
  (`python -m healthadvocate.cli`).
- MCP server surface (`python -m healthadvocate.mcp_server`) with uplifted tool
  descriptions and cache hints.
- `llms.txt` machine-readable project summary for AI tooling and GEO discovery.
- Lightweight CI workflow (test + compile gates on pull requests and `master`).
- Renovate dependency automation configuration.

### Changed
- **OpenMed vendoring retired** — the repo-root `openmed/` fork (upstream
  v1.4.0 + 3 local patches, 67 files) is deleted; the runtime is the
  PyPI-pinned package (`openmed[hf]==2.5.0`, exact pin; Renovate offers
  bumps). The `engine.py` sys.path insert that let the vendored copy shadow
  the pip pin is removed. Version-agnostic contract tests
  (`tests/test_openmed_contract.py`) gate the surface HA consumes.
  Rationale + full upstream update list:
  `docs/OPENMED-UPSTREAM-LEVERAGE-2026-09-17.md`,
  `docs/OPENMED-UPSTREAM-CHANGELOG-2026-09-22.md`. Our offset-safe
  `reidentify` patch is superseded upstream (occurrence-aware); the config
  thread-lock patch is dropped (HA never touches OpenMed global config).
- Public repo hygiene hardening; tracked agent session state removed.
- Docker Python base image tag updated to `3.14`.
- README restored to full pre-wave2b content with S+ SEO/GEO public-face pass and
  sibling-repo cross-links.
- `.gitignore` completed (was missing its trailing entry).
- README documents the live Coverage Continuity Track (Features entry,
  project-structure lines for `coverage/`, `privacy/`, `governance/`,
  `adapters/`, the 16 `/api/coverage/*` endpoints in the All Endpoints
  table, and the encrypted-case + Commitment-Gate privacy bullets).

### Fixed
- Incomplete `.gitignore` entry that left local artifacts unignored.

### Dependencies
- `fastapi`, `uvicorn`, `pydantic`, `openai`, `openmed`, `faker`, `pysbd`,
  `transformers`, `huggingface-hub`, `accelerate`, and `tokenizers` pinned to
  current minor releases; `actions/checkout` and `actions/setup-python` bumped.

---

## 2026-05-20 — Initial changelog

### Added
- Initial changelog file so release and repository health tooling have a
  canonical change log.