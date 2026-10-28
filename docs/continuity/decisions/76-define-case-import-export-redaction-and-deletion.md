---
source: GitHub mirror simongonzalezdc/healthadvocate issue #76 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/76
title: "Define case import, export, redaction, and deletion"
state_at_import: closed
labels: wayfinder:grilling
opened: 2026-07-22T17:53:46Z
updated: 2026-07-22T19:50:55Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Define case import, export, redaction, and deletion

## Question

What should private import, private export, redacted export, backup, retention, and deletion do across structured case data, evidence files, derived scripts, logs, and source documents the application does not own?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:50:54Z)

## Decision: Case import, export, redaction, and deletion

### Decision
- **Private export**: full application-owned case JSON + evidence copies the app stored; review before write; path outside repo default.
- **Redacted export**: strips direct identifiers (names, member IDs, phones, emails, SSNs, street addresses) via deterministic redaction rules; shows residual-risk warning that automated redaction is not a guarantee.
- **Deletion**: removes application-owned DB rows, derived scripts, app-copied evidence files, and optionally the key; reports unowned source file paths without deleting them.
- **Import of real cases**: disabled until issue 90/77 gate passes.
- **Key rotation**: re-encrypt store with new key; old key invalidated.
- **Recovery**: encrypted export + key recovery material; wrong key fails closed.

Closes fog for issue 76.
