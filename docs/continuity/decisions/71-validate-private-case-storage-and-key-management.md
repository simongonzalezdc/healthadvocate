---
source: GitHub mirror simongonzalezdc/healthadvocate issue #71 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/71
title: "Validate private case storage and key management"
state_at_import: closed
labels: wayfinder:research
opened: 2026-07-22T17:53:31Z
updated: 2026-07-22T18:03:57Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Validate private case storage and key management

## Question

Does encrypted local SQLite with an operating-system credential-store key provide the right privacy, recovery, backup, migration, and deletion boundary for Coverage Cases, and what exact failure behavior must be required?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T18:03:49Z)

Resolved in [private-case-storage-key-management.md](https://github.com/simongonzalezdc/healthadvocate/blob/fa9bc78/research/private-case-storage-key-management.md). Recommendation: use encrypted local SQLite for Coverage Cases and store only the unlock key in macOS Keychain. This is the right privacy boundary for a local-first single-user case, but the product must fail closed on missing or wrong key, and it must add an explicit recovery/export path because ThisDeviceOnly-style keychain items do not migrate. Current repo state is still stateless for this surface: family_tracker is in-memory only, and engine handles de-identification without persistence.
