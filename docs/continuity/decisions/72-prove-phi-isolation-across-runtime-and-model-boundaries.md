---
source: GitHub mirror simongonzalezdc/healthadvocate issue #72 (exported 2026-10-28 by pm-healthadvocate)
source_url: https://github.com/simongonzalezdc/healthadvocate/issues/72
title: "Prove PHI isolation across runtime and model boundaries"
state_at_import: closed
labels: wayfinder:research
opened: 2026-07-22T17:53:34Z
updated: 2026-07-22T19:35:38Z
author: simongonzalezdc
comments_imported: 1
edits: none — body is verbatim
---

# Prove PHI isolation across runtime and model boundaries

## Question

What enforceable runtime, authentication, deidentification, logging, and remote-model controls are required to prove that PHI cannot silently leave the local trusted boundary?

## Comments (verbatim from the source thread)

### Comment 1 — simongonzalezdc (2026-07-22T19:35:37Z)

## Decision: PHI isolation across runtime and model boundaries

### Decision

Enforce a single local trusted boundary with fail-closed controls. PHI-bearing computation stays on the machine. Any model use is optional, local-only, and subordinate to a central Privacy Boundary.

### Runtime and binding
1. Default application, container, and model listeners bind to loopback only (`127.0.0.1` / `::1`). Binding to `0.0.0.0`, non-loopback interfaces, or advertising an unauthenticated public/reverse-proxy route is not a default profile.
2. An authenticated non-loopback deployment profile is out of scope for this track and must fail startup if selected without explicit auth configuration (none ships in the default path).
3. Default Docker/Compose must not enable Traefik or any unauthenticated public path.

### Model destination policy
1. Model endpoints must be OpenAI-compatible local runtimes only (llama.cpp or Ollama once audited). LM Studio is excluded from the core path (issue 78).
2. Allowed destinations: loopback hostnames/IPs only (`localhost`, `127.0.0.0/8`, `::1`, IPv4-mapped loopback).
3. Rejected: remote hosts, public IPs, link-local non-loopback, DNS names that resolve to any non-loopback address, resolution failure, credentialed URLs that hide a remote host, fragments/userinfo tricks, and HTTP redirects.
4. HTTP clients used for model calls must disable redirects. Ambiguous or mixed IPv4/IPv6 results fail closed if any address is non-loopback.

### Deidentification
1. One Privacy Boundary assembles the complete model input (user text, Family Profile context, evidence metadata, notes, error strings intended for the model) before any model call.
2. Deidentification status is explicit: `success` | `no_pii_found` | `failed`. The boolean `pii_scrubbed` is not authoritative.
3. `failed` produces zero model requests and a non-sensitive error. Missing tools or exceptions are failures, never pass-through of raw text.
4. Deterministic Coverage workflows must work with no model runtime available.

### Logging and artifacts
1. Structured logs carry event codes, correlation IDs, adapter/status values, and timing only.
2. Logs, exceptions, screenshots, temporary files, and CI artifacts must not contain configured synthetic canaries or raw request bodies.
3. No analytics, tracking pixels, remote fonts, telemetry, or crash uploaders in the real-case-capable build.

### Alternatives considered
- Trust env vars and LM Studio defaults: rejected (remote leakage risk).
- Allow LAN/tailnet without auth for convenience: rejected for this track.
- Scrub only the user field and append profile later: rejected (profile bypass).

### Failure behavior
- Bad bind/proxy/model destination → refuse start or refuse request.
- Deidentification failure → no model call, safe error.
- Canary escape in tests → suite fail; blocks real-case release (issue 77/90).

### Downstream constraints
- Issue 80 must implement these controls with behavioral tests.
- Later adapters and optional models cannot weaken this boundary.
- Real-case import remains disabled until issue 90 and HA-E72 evidence pass.

Closes the fog for issue 72.
