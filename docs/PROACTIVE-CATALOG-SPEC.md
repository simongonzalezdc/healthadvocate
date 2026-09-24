# Proactive Catalog & Provider Directory — Spec

**Status:** design spec (Library + Directory + "What's coming up" shipped as demo views with
synthetic data on `feat/design-system-20260924`; storage/analysis backend NOT wired)
**Design system:** docs/DESIGN-SYSTEM.md · **Recorder spec:** docs/CALL-RECORDER-SPEC.md

## 1. Purpose

Every recorded call, transcript, voicemail, and appointment becomes a **first-class,
local-only, encrypted catalog item** that is categorized, cross-referenced, analyzed with
provenance, and surfaced proactively (reminders/deadlines). A self-building **provider
directory** accumulates the people and places in the person's care, so acting on any
reminder is one tap. Nobody types anything unless they are correcting the machine.

## 2. Storage schema (encrypted at rest, local only)

Follows the coverage keystore pattern (docs/ — key held in the OS keychain; no key, no data).

```
catalog_db (SQLCipher or OS-encrypted store; one file, app-private)
  item {
    id uuid pk, kind: call|appointment|voicemail|reminder|document|bill,
    matter_id fk,            -- groups items into one story (e.g. "MRI denial")
    title, created_at, occurred_at,
    audio_ref null,          -- app-private file, random UUID name
    transcript text null,    -- final turns only; interim never persisted as final
    consent_ref null,        -- required for call/appointment kinds (fail-closed)
    analysis_ref null,       -- analysis blob (§4), provenance-labeled
    crypto: blob fields sealed with the keystore key (AES-GCM, per-record nonce)
  }
  matter { id uuid pk, title, status: open|resolved, created_at }
  contact {                                  -- §3 directory record
    id uuid pk, name, klass: doctor|lab|imaging|therapy|pharmacy|facility|insurer,
    fields: [ field {                          -- FIELD-LEVEL provenance
      k: phone|email|address|hours|fax, v,
      prov: user_confirmed|extracted|inferred,
      source_refs: [item_id…],                 -- merge evidence
      confirmed_at null } ],
    merge_key,                                 -- §3.2
    crypto: sealed as above
  }
  reminder {
    id uuid pk, due_at, state: upcoming|due_soon|overdue|done,
    title, context, matter_id fk, contact_id fk null,
    provenance: extracted|inferred,            -- deadlines carry provenance too
    notify_local bool
  }
  item_link { item_id fk, contact_id fk }      -- both-way cross-reference
```

Deletion of an item is transactional across item/audio/analysis/derived reminders;
directory contacts survive with their source_refs pruned (a contact the user confirmed is
theirs, not the call's).

## 3. Directory (self-building)

### 3.1 Field-level provenance (the honesty contract)

- Every field renders its species: `user-confirmed` (solid green check chip — the ONLY
  solid species), `extracted` (slate, names its source: call/document/voicemail),
  `inferred` (caution chip, names the pattern). Inferred data is NEVER styled as confirmed.
- Precedence: `user_confirmed > extracted > inferred`, applied per field on merge. A
  confirmation overrides and freezes the field against later inference (with an "edit"
  path that re-opens it).
- One-tap **Confirm** on any unconfirmed field promotes it (demo implements this).
- tel:/mailto: links fire only on user tap; nothing auto-dials, auto-emails, or opens maps.

### 3.2 Merge-dedupe rules

- Candidates by: normalized phone (E.164 digits), exact/fuzzy name (token-set ratio ≥ 0.9
  with specialty context), address token overlap. Merge never drops a source: the card
  lists `source_refs` ("Merged from 3 sources: Appointment card · Call transcript · Bill
  decode").
- Conflict on same field from two extracted sources → keep the most recent, mark
  `inferred` with both sources listed, surface a "two versions seen" confirm affordance.
- Extraction sources: provider names + numbers from transcripts (post-deid, but the
  directory stores the real contact data — it is user data at rest, encrypted, not model
  input); facility names/addresses from decoded documents and bills; whom-appointments-
  with from the appointments surface; medication → pharmacy links from the drug checker.

### 3.3 Cross-links both ways

- Contact card → its items in the Library timeline (calls, documents, appointments, bills).
- Library entity chips (provider/PII class) → directory entries (demo: via the contact's
  Library link; real impl: `item_link`).
- Reminder/due-soon cards carry the contact's confirmed-or-extracted phone as a one-tap
  Call action.

## 4. Analysis pipeline (typed decisions, provenance-labeled)

```
audio → transcript (local ASR, CALL-RECORDER-SPEC §3)
      → deidentification (existing PII masker; mask map kept LOCAL per item for unmask-on-render)
      → NER (existing entity stack: dates, providers, amounts, medications, denial reasons)
      → typed decisions (HA-JEV DecisionOutcome shape):
           commitment  { quote_span, who, due_hint }        → prov: extracted (must quote)
           deadline    { date|hint, basis: quoted|computed, confidence }
                                                               extracted iff quoted+parsed
           action_item { text }                               inferred (model) unless quoted
      → reminders generated ONLY from extracted|user-confirmed deadlines;
        inferred deadlines surface as UNVERIFIED → NEEDS_HUMAN discipline
```

Rendering law (shipped in the demo): each analysis row carries its provenance chip;
unverified rows additionally render the needs-human treatment ("This needs a human
decision — confirm in writing before relying on it") and are excluded from reminder dates,
badge counts, and notifications until confirmed. Commitments must include the quote.

## 5. Proactive surfacing + local notifications

- Home "What's coming up": reminder cards with states upcoming / due-soon / overdue / done
  (state = left-bar tone + label text + one-tap call/open actions). Header badge counts
  due-soon items only (overdue escalates its own card, not a number).
- **Local notifications only — by law.** Use the Notification API through the registered
  service worker (`registration.showNotification`) or the platform's local scheduler
  (WorkManager/UNNotificationRequest in a wrapper app). NO push server, NO network, NO
  third-party SDKs. Limitation (stated in the UI): reminders fire when the browser/OS
  permits local scheduling — a PWA closed by the user may not wake on iOS; document per
  platform and show the honest "reminders work while the app can run locally" note.
- Notification content is derived locally from the encrypted store; nothing identifying
  leaves the notification surface the OS already trusts.

## 6. Acceptance (when the backend lands)

1. Airplane-mode: catalog search, timeline, directory confirm, reminder state machine —
   zero network.
2. Keychain key absent → catalog store unreadable (gibberish, not plaintext).
3. Deleting an item removes audio + transcript + derived reminders in one transaction.
4. An inferred phone number NEVER renders with the confirmed species; a confirmed field
   survives a re-merge with conflicting extraction.
5. A deadline that cannot be quoted from the transcript cannot produce a reminder date.
