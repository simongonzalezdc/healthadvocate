# HealthAdvocate Coverage Continuity Current State

Updated: 2026-10-28 — **canonical is `git.kyanitelabs.tech/simon/healthadvocate`**; the GitHub
copy is a mirror (frozen as a source of truth on this date) and is no longer the trunk.

## What is already live (tracker)

- Spec: [Local-first Coverage Continuity Track](continuity/spec-local-first-coverage-continuity-track.md)
  — living canon, now versioned in this repo (was GitHub issue #68).
- Wayfinder map: [Safe Coverage Continuity Track](continuity/wayfinder-safe-coverage-continuity-track.md)
  — the standing rules and open questions (was GitHub issue #69).
- Decision records: [continuity/decisions/](continuity/decisions/) — nine closed decisions
  (GitHub #70–#78), bodies **and** the decisive comments imported verbatim.
- Implementation records: [continuity/implementation/](continuity/implementation/) — twelve closed
  acceptance records (GitHub #79–#90).
- Everything above, with provenance and the rules it was imported under:
  [continuity/README.md](continuity/README.md).

## Session handoff

- Closeout: `.omx/handoffs/2026-07-22-open-evidence-continuity-session-closeout.md`
- Next-agent prompt: `.omx/handoffs/2026-07-22-next-agent-prompt.md`

(These paths predate the 2026-09-24 tree and may not exist in this checkout; the continuity
record under `docs/continuity/` is the surviving copy of that work's decisions.)

## Product truths

- Coverage Case aggregate with immutable Evidence Items and append-only Contact Events
- Encrypted local case store + keystore interface; wrong/missing key fails closed
- Commitment Gate blocks pay/submit/message/treatment with zero side effects
- Low-energy Coverage UI + deterministic scripts (no model required)
- Fixture-backed open adapters with narrow claim contracts
- Real-case import **disabled** until independent verifier + full HA-E* receipts

## Open loops (short)

1. Rebase/reconcile any stranded continuity commits onto canonical `master` (do not push blind —
   canonical `master` is push-protected; land through a PR)
2. Independent verifier for the exact build
3. Roll the Privacy Boundary to the remaining LLM modules
4. Stronger a11y/container audit receipts; optional live bulk adapters
5. Track open continuity work in the **canonical** tracker, not the mirror

## Notes

- Superseded framing: until 2026-10-28 this file said "local mirror; GitHub remains canonical"
  and deferred to live `gh issue` state. Both are now wrong: canonical is Forgejo, and the
  continuity issues were imported into this repo because the mirror was the only copy.
- The mirror's issue bodies were the only copy of the spec, map, decisions and acceptance
  records. They were exported verbatim on 2026-10-28 into `docs/continuity/` (see that README for
  the exact provenance and the one disclosed edit: cross-issue links were localised).
- Still accurate from the 2026-09-15 refresh: canonical `master` contained the continuity work in
  the `20fecf0` lineage (`chore(fl4write): adopt`, PR #12).
