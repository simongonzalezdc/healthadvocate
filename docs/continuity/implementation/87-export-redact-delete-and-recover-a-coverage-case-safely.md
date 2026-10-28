---
source: GitHub mirror simongonzalezdc/healthadvocate issue #87 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/87
title: "Export redact delete and recover a Coverage Case safely"
state_at_import: closed
labels: ready-for-agent
opened: 2026-07-22T19:19:52Z
updated: 2026-07-22T19:52:04Z
author: simongonzalezdc
comments_imported: 1
edits: issue links that point at other imported issues are rewritten to the local file; no prose changed
---

# Export redact delete and recover a Coverage Case safely

## Parent

../spec-local-first-coverage-continuity-track.md

## What to build

Let a user create private and redacted exports, see residual-risk warnings, delete application-owned case data and derived artifacts, distinguish unowned source files, rotate keys, and exercise the approved recovery path.

## Acceptance criteria

- [ ] Private and redacted exports are distinct user-visible operations with review before artifact creation.
- [ ] Redacted export removes seeded direct identifiers and displays that automated redaction is not a guarantee.
- [ ] Deletion removes application-owned case data and derived artifacts and reports unowned external source files.
- [ ] Key rotation preserves data and invalidates the old key.
- [ ] The approved recovery path is testable without exposing plaintext or silently replacing a lost key.
- [ ] Export, deletion, and recovery requests remain subject to the applicable review and Commitment Gate rules.

## Blocked by

- ../decisions/76-define-case-import-export-redaction-and-deletion.md
- 80-make-the-local-runtime-fail-closed-around-phi.md
- 81-create-and-resume-an-encrypted-synthetic-coverage-case.md
- 82-block-every-external-commitment-with-zero-side-effects.md

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:52:03Z)

## Completion receipt — issue 87

Modules: `lifecycle_ops.py`, export/delete/import-real API routes, tests.
Suite: 63 passed. Real import returns 403. Synthetic only.

Closing.
