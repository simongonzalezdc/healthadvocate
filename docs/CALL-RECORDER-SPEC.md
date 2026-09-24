# Call Recorder — Backend & Runtime Spec

**Status:** design spec (view + demo states shipped on `feat/design-system-20260924`; backend NOT wired — the shipped view runs a clearly-badged synthetic demo)
**Design system:** docs/DESIGN-SYSTEM.md (tokens, Honesty Lane, motion)
**Companion spec:** docs/PROACTIVE-CATALOG-SPEC.md (catalog, directory, analysis pipeline, reminders, encrypted storage)

## 1. Purpose

Record medical phone calls and in-person appointments, transcribe them **on the same
device**, and turn the transcript into an honest summary with commitments, deadlines, and
action items — feeding the existing decoder / appointment-prep flows. The person using
HealthAdvocate is often sick, overwhelmed, and outmatched on the phone; the recorder exists
so they never have to rely on memory in those moments.

**Laws this feature inherits:**
- Local-first, privacy-absolute: audio + transcript never leave the device. No telemetry, no
  crash dumps carrying audio, no third-party ASR, ever.
- Honest-at-the-glass: interim/draft transcript text is visually distinct from final text;
  `[inaudible]` is an honest gap, never a guess; analysis is provenance-labeled; unverified
  deadlines render through the NEEDS_HUMAN discipline and are never styled as certain.
- Consent is a first-class state, not a checkbox buried in settings.

## 2. Surfaces and states (all shipped as demo states in the view)

| State | Entry | Contract |
| --- | --- | --- |
| **First run / consent** | default | Law note (plain language, non-legal-advice), one acknowledgment checkbox gating the start button. Button stays disabled + explains itself until acknowledged. |
| **Recording** | consent given | Pulse dot (the product's only glow), mono timer, waveform, live transcript, persistent privacy chip, sticky stop bar (mobile-first: phone calls happen on phones). |
| **Live transcript** | during recording | Speaker turns with mono timestamps; interim text muted+italic, final solid; `[inaudible]` turns styled as gaps; autoscroll; `aria-live=polite`. |
| **Stopped → summary** | stop | Summary + provenance-labeled analysis (see PROACTIVE-CATALOG-SPEC §4); recording lands in the Library catalog; toast confirms local save. |
| **Demo mode** | always (until backend lands) | `demo-badge` on the panel; start button reads "Start demo recording"; toast states no microphone is used; synthetic script; delete uses the confirm dialog and says nothing is really stored. |

## 3. Recording pipeline (backend, to build)

1. **Capture.** Platform audio APIs: Android `MediaRecorder` (via a wrapper app or
   WebView bridge), iOS `AVAudioEngine`/CallKit constraints, desktop browser
   `MediaRecorder` (loopback microphone only — browser tab capture of calls is NOT
   possible for phone calls; document honestly per platform).
   - Format: Opus in WebM/OGG (browser), AAC/FLAC (native). Write stream to a
     device-scoped app directory; filename = random UUID, never caller metadata.
2. **Consent record.** Store a structured consent event (timestamp, scope: call/appointment,
   acknowledgment text version) beside the recording. No consent record → recorder refuses
   to start (fail-closed).
3. **Local ASR.** Requirements: fully offline model, no network. Options (evaluate in this
   order):
   - **whisper.cpp** (GGML tiny/base/small quantized) — best accuracy/portability trade;
     runs CPU on phones (tiny.en ~75MB, base ~150MB); incremental/segmented decoding for
     live-ish transcript.
   - **Vosk** small models (~50MB) — true streaming, weaker accuracy, permissive license.
   - **Android SpeechRecognizer** with `EXTRA_PREFER_OFFLINE` — free but device-dependent
     availability; treat as fallback with an honest capability probe (never silently
     degrade to cloud — check `onDevice` flags; if only cloud exists, feature reports
     unavailable).
   - Model download is an explicit user action (one-time), from the project's release
     artifacts, verified by checksum; no auto-update without consent.
4. **Speaker turns.** Diarization is hard on-device; ship V1 as single-channel with
   energy-based turn segmentation + manual "who said this" correction in the transcript
   view. V2: local diarization (e.g. pyannote-derived quantized) only if it stays offline.
5. **Post-call analysis.** Handled by the typed-decision pipeline in PROACTIVE-CATALOG-SPEC
   §4 (deid → NER → typed decisions with provenance). The recorder itself never invents
   structure.

## 4. Consent law notes (UI copy is intentionally plain; this is not legal advice)

- **US federal:** one-party consent suffices for federal wiretap (18 U.S.C. § 2511) — but
  state call-recording law governs most phone calls.
- **All-party states** (e.g. CA, FL, PA, WA, and others): everyone on the call must consent.
  Recording without it can be a crime and makes the recording inadmissible.
- **Healthcare settings:** providers may prohibit recording in offices; a patient may still
  have rights to the information (request records instead when refused).
- **Voicemail:** leaving a message is generally treated as consent to recording by the
  system that takes it — one-party rules then apply to your copy.
- The UI must: state that HealthAdvocate cannot advise on the law; link the
  state-by-state reference from the Help view (offline copy bundled); require the explicit
  acknowledgment before the first recording on each new contact context (session-level, not
  a one-time EULA).

## 5. Privacy boundary integration

- Audio files live in the app's private storage; the existing privacy boundary
  (`healthadvocate/privacy/`) gains a `media` asset class: same redaction-on-ingest rule as
  text — the transcript is deidentified before any analysis, and raw audio is never passed
  to the LLM client (model input is transcript text only, post-deid).
- The commitment gate (coverage/DIR intents) treats "share recording" and "email transcript"
  as prohibited outbound intents unless the user performs the export gesture themselves.
- Deletion must be real deletion: removing a catalog item removes audio + transcript +
  derived analysis in one transaction, and the confirm dialog says so.

## 6. Acceptance (when the backend lands)

1. Airplane-mode end-to-end: record → transcript → summary → reminder, zero network.
2. No consent record → recorder cannot start (UI + storage both refuse).
3. Interim-vs-final and inaudible markers survive the analysis pipeline.
4. Kill the app mid-recording: partial audio + transcript recover; consent record intact.
5. Suite green; demo badge removed only when a real capture path exists per platform.
