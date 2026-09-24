# Design System — HealthAdvocate

**Status:** approved (interview re-run per CEO order 2026-09-24; branch `feat/design-system-20260924`)
**Next move:** §0 interview → derived deltas landed in the build → GLM-5.3-Flash judged rounds (receipts under `docs/design/vision-pass-receipts-2026-09-24/`)

`approved` means: every dimension is decided from the product truths in the §0
interview transcript, is buildable, and the build has been brought to the derivation.

## Design direction summary (derived in §0)

> **North star (one line):** "A lamp left on in a dark house" — dark-first warm umber
> rooms, one cream lamp-lit task per screen, vitals-green advocate accent, serif
> letter-voice display, numbered plain-language steps; signature = the lamp (attention
> is light).

- **Reference / anchor:** ACLU Know-Your-Rights card (glanceable numbered advocacy under
  fear) + Starling/Monzo loss flows (calm stepwise hand-holding). What they earn, not
  their layouts.
- **Aesthetic territory:** a lamp left on in a dark house — matte warm dark, cream
  reading light, no glass/gloss, wool-and-paper materials.
- **Personality:** the friend beside you in the waiting room (pole), never the
  institution's counter being polite.
- **Structure and rhythm:** the triage card (one lit card per tool view, state line
  first, numbered findings); home = the night table; steady 24/32 cadence; emergencies
  break rhythm full-width.
- **Signature:** the lamp — light tracks attention; the only glow in the product.
- **Imagery and iconography:** none photographic; one inline line-SVG wayfinding system.

---

## 0. The design-system interview (full transcript, 2026-09-24)

Method note: this is the question-by-question interview required by the
design-system-interview contract, answered against the product truths only. Truths cited
as **T1** free open-source advocacy for people at their most vulnerable (sick,
overwhelmed, fighting insurers) · **T2** local-first, privacy-absolute · **T3**
honest-at-the-glass law (a fallback never looks like an answer; unavailable is neutral;
NEEDS_HUMAN first-class; urgency badges only for real verdicts; the emergency exception
escalates) · **T4** the surfaces: symptom/bill/denial/document/appointment tools + the
call recorder (consent, transcripts) · **T5** mobile/PWA is the primary case (calls
happen on phones) · **T6** catalog/directory/reminders carry machine-derived facts that
must wear provenance. An earlier draft of this section "formalized the founder-built
skin" — voided by CEO order 2026-09-24; every answer below is derived, not inherited.

---

**Q — reference.** Name a real artifact this system learns from, and what it earns HERE.

**A.** Two, one for the voice and one for the mechanics. The **ACLU "Know Your Rights"
card** is the voice reference: a tool carried by a scared person into an encounter with
an institution that outweighs them, designed to be read with shaking hands — plain
words, enormous numbered steps, zero decoration, one glance to the answer. What it
earns for HealthAdvocate (T1, T3): proof that power asymmetry is a *design problem*,
solved with hierarchy and plain language, not reassurance graphics. The mechanical
reference is **Starling/Monzo's fraud-and-loss flows**: banking interfaces that stay
warm and stepwise during a panic ("your money is safe — here is the next step"), showing
that a screen can hold a frightened person's hand without being childish. What it earns
(T1): the calm-next-step cadence for denial appeals and bill fights. We learn the
numbered glance and the calm step; we copy neither layout nor brand.

**Q — personality.** A chosen pole, not a middle.

**A.** The pole is **"the friend who sits beside you in the waiting room."** On one
pole: a person on your side of the desk — warm, low-voiced, unhurried, never surprised,
never performing. On the other: the institution's counter — efficient, coded,
self-protecting. Every middle point reads as the counter being polite. T1 says users are
fighting an institution; the interface must visibly sit on the user's side of the desk.
Explicitly NOT: cheerful SaaS onboarding, clinical neutrality, "empowering" dashboards.

**Q — aesthetic.** One concrete phrase predicting hierarchy and material.

**A.** **"A lamp left on in a dark house."** The moment of use is often 2 a.m., a phone,
a denial letter, a symptom scare (T1, T5). The material: deep warm darkness as the room,
one warm-lit reading field as the task, cream paper light for words, a single green
"still here" accent — the vitals-monitor green that means *alive and being watched
over* (T1). Hierarchy prediction: exactly one lit task per screen; everything the user
is not doing recedes into warm dark; emergencies light the whole room (T3's escalation).
Matte surfaces, soft edges, no glass, no gloss — wool and paper, not chrome.

**Q — type.** Binding evidence, display/body stance, measure risk.

**A.** Binding evidence (T4): the product's artifacts are *letters and records* — appeal
letters, denial letters, discharge summaries, transcripts. Its text is dense medical
plain-language read under stress (T1). Stance: **display = a book serif** (Charter /
Georgia stack) — the voice of a brief written on your behalf, warm and adult, never
techie; **body = the system sans** — maximum operational legibility at 15-16px;
**mono = system mono** for timestamps, money, reference numbers — the receipt voice that
makes "$1,200.00" and "A-2291" feel like evidence. Measure risk: dense medical
explanations at wide measure exhaust a tired reader — hard cap 62ch for reading copy,
68ch absolute; transcripts wrap at ~54ch with speaker labels intact. No third-party
font CDN ever (T2) — serif display is satisfiable from every OS's charter/georgia class.

**Q — color_mode.** Dominant hue, accent job, light/dark commitment — derived from what
hope-against-the-system feels like.

**A.** What it feels like (T1): night, and someone left the light on. **Dark-first** is
therefore the product's home mode (T5: the phone at 2 a.m.); light is the daytime
clinic variant — both shipped, both tuned (never inverted). Dominant hue: **warm
umber-dark rooms** (not cold charcoal, not pure black — the room is warm because
someone is home) with **cream lamp fields** for reading surfaces. Accent jobs, one hue
each (T3/T6 make these laws): **vitals green = the advocate acting** (primary actions,
live states, confirmed facts) — it may glow only while something is live; **amber = the
clock** (deadlines, due-soon, inferred data) — time pressure without panic; **coral =
the alarm** (danger, HIGH, needs-human, recording) — loudest and rarest; **slate = the
record** (extracted facts, information). Neutral-gray reserved for the honest absences:
unavailable, unverified (T3).

**Q — density_shape.** Density, radius range, elevation for stressed users.

**A.** Comfortable density with **big-type scannability** (T1): a tired reader scans
18-22px titles and 15-16px body, never 12px walls. Radius: **12/16/20px** — soft
everyday edges (nothing institutional-sharp), one 24px for the hero workbench; no 32px
blobbiness: this is a tool, not a toy. Elevation = **light, not shadow**: the lit field
is brighter than the room (lamp semantics); borders are warm hairlines; shadows exist
only as the lamp's soft warm spill on the active surface. One glow law (T3 by way of
the glass laws): light tracks attention and liveness, nothing else may glow.

**Q — structure_rhythm.** Composition, motif, sectional cadence for scanability.

**A.** Composition: **the triage card** — every tool view is one lit card in the dark
with a title, one input story, one primary action, and results that arrive beneath as
numbered findings (T4's forms + T3's state-first law). Home is **the night table**: a
short greeting, the one thing due now (reminders, T6), then the three doors. Motif:
**the state line first** — every result opens with its honesty state (needs-human /
unavailable / verdict) before any content (T3). Cadence: card → breathe → card at a
steady 24/32px rhythm; metronomic inside cards (predictability under stress), air
between regions. Emergencies break the rhythm deliberately with a full-width alarm band
(T3).

**Q — signature.** One memorable move — the thing someone screenshots.

**A.** **The lamp.** A dark room; one warm page glowing like a reading lamp, edges soft
with light-spill; a green accent that means "still here." It screenshots as: *someone
left a light on for me and it is on my side.* The honesty lane (mutually exclusive
state species, §6) is the system's law; the lamp is how it feels.

**Q — imagery_iconography.** Source/treatment or absence; one icon system.

**A.** **No photographs, no illustration, no decorative imagery** (T2 seriousness; T1
dignity — clip-art sympathy cheapens a fight for care). One icon system only: inline
line SVG, 1.5-1.75 stroke, round caps, clinical-wayfinding spirit — orientation, not
decoration; sized 16-24px, naked line icons everywhere except the primary action where
they may sit in a soft pill. The product's only "art" is typography, light, and the
state species (T3).

**Q — motion (optional dimension).** Level and character.

**A.** **A calm hand.** 140ms acknowledgement, 200-320ms ease-out entrances; one pulse
in the whole product (the live recording dot, T4); light rises when a card gains
attention, dims when it loses it. Nothing bounces, nothing celebrates (T1: triumph is
not the register — relief is). Reduced-motion: the lamp still lights, nothing moves.

---

**Derived deltas vs. the shipped draft (what the build must change):**
1. **Dark-first default** (was light-default) — the 2 a.m. truth (T1/T5).
2. **Serif display voice** for titles/hero (was all-sans) — the letter/brief evidence (T4).
3. **Accent job sharpened to vitals green** with glow reserved for live/attending states.
4. **Radius tightened to 12/16/20(+24)** (was 10/16/24/32).
5. **Lamp material**: brightness-as-elevation + warm light-spill on the attending card
   (one glow), warm-dark room tones.
6. Numbered-findings cadence in results (rights-card glance, T3 state line first).

---

## 1. Design principles (derived from the product truths)

1. **Honesty at the glass.** A fallback never looks like an answer. "Unavailable" is a
   neutral state, not a muted alarm. NEEDS_HUMAN is a first-class citizen with its own
   banner. Urgency badges exist only for real verdicts. The emergency exception escalates
   loudly — that is the one place loud is correct.
2. **Calm for the overwhelmed.** One task per view, one primary action, generous space,
   quiet color, no motion that celebrates. Density is comfort, not information-hiding.
3. **Privacy you can see.** Local-only is not a footnote; it is a visible, persistent
   indicator wherever data exists (lock mark + "Stays on this device"). Nothing in the UI
   implies a cloud, an account, or a sync.
4. **Readable at the worst moment.** Body text ≥ 15px, measure ≤ 70ch, AA contrast on every
   real pair, visible focus everywhere, reduced-motion honored, plain language.
5. **Warmth without decoration.** Warm paper, sage advocate green, human iconography. No
   gradients, glass, glow, or imagery that decorates rather than informs.
6. **States are designed, not defaulted.** Every reachable data state (empty, loading,
   unavailable, needs-human, emergency, demo) has a designed treatment and honest copy.

---

## 2. Color tokens (→ color-system, theming)

Three layers, one source: primitives (ramps) → semantic roles (what components reference) →
legacy aliases (existing class contracts, kept 1:1 so JS-generated markup never breaks).

Hue jobs — every hue has exactly one job:

| Hue | Job | Light mark | Light ink (text on tint) | Dark mark | Dark ink |
| --- | --- | --- | --- | --- | --- |
| Advocate green | primary action, positive/low urgency, "your advocate acting" | `#446e54` | (accent pair, test-pinned) | `#72a880` | (pair, test-pinned) |
| Warm ochre | caution, medium urgency, watch-items | `#b87848` | `#8f5a32` | `#d09a72` | `#dfa489` |
| Coral | danger, HIGH urgency, needs-human, live recording | `#b85548` | `#96382c` | `#d47a72` | `#eba29a` |
| Slate | information, neutral findings, metadata emphasis | `#55749a` | `#46618a` | `#7a9dbe` | `#9cb9d8` |
| Warm paper | surfaces (light) | `#faf8f5`→`#e5e1da` ramp | — | `#181716`→`#353230` ramp | — |

Ink rule (color-system law): mid-tone hues are **marks** (bars, icons, borders — 3:1 UI
minimum); text on tints uses the darker/lighter **ink** variant (≥4.5:1 measured on tint
composited over every surface it can sit on). The accent green pair is pinned by
`test_theme_colors_meet_wcag_aa_contrast` and does not move.

Semantic tokens (both themes define all of these; components use ONLY these):

```
Surfaces:  --color-bg · --color-surface · --color-surface-2 (elevated) · --color-surface-3 (muted) · --color-input
Text:      --color-text · --color-text-muted · --color-text-subtle
Lines:     --color-border · --color-border-soft
Primary:   --color-primary · --color-primary-hover · --color-primary-tint · --color-primary-tint-strong · --color-on-primary
Status:    --status-danger{,-ink,-tint} · --status-caution{,-ink,-tint} · --status-info{,-ink,-tint}
           · --status-neutral{,-ink,-tint} (the honesty color: gray, dashed border)
Focus:     --color-focus-ring
```

Legacy aliases (kept forever, or until JS stops emitting them): `--bg-body --bg-surface
--bg-elevated --bg-muted --bg-input --accent --accent-hover --accent-light --accent-medium
--warm --warm-light --warm-medium --coral --coral-light --coral-medium --slate
--slate-light --slate-medium --text-1 --text-2 --text-3 --border --border-light` — each now
defined as `var(...)` of a semantic token. **Rule: new CSS never references a legacy alias
or a raw hex; it references semantic tokens.**

Dark theme is tuned, not inverted: near-black warm base (`#181716`, not `#000`), lighter
per-level surfaces, text capped below glare white (`#e8e4de`), status inks re-lightened and
re-measured on dark tint composites (≥4.5:1).

Coverage risk chips (previously raw dark-only hexes) are tokenized: overdue = danger filled,
approaching = caution, unknown = **neutral dashed** (honest absence), stale = info,
conflicted = danger **outline** (same family as overdue, shape differentiates), scheduled =
primary tint.

---

## 3. Type scale (→ web-typography)

Stance (interview-derived): **display = the letter voice** (Charter/Georgia serif — the
product's artifacts are appeal letters, denial letters, discharge summaries; titles read
as a brief written on your behalf), **body = the system sans** (operational legibility),
**mono = the receipt voice** (timestamps, money, reference numbers). Sustained reading is
ragged-right; measure capped at 62ch for reading copy, 68ch absolute, transcripts ~54ch.

```
--font-display: Charter, "Bitstream Charter", Georgia, "Times New Roman", serif
--font-sans: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif
--font-mono: ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace  (timestamps, IDs, timers)
```

| Token | Size / line | Role |
| --- | --- | --- |
| `--step--2` | 12px / 1.5 | fine print, chip text, badge labels (uppercase + tracking) |
| `--step--1` | 13.5px / 1.55 | captions, helper text, result body-secondary |
| `--step-0` | 15px / 1.65 | body (never smaller for reading text) |
| `--step-1` | 17px / 1.5 | card titles, view subtitles |
| `--step-2` | 20px / 1.3 | view titles (panel h2) |
| `--step-3` | 25px / 1.2 | section display |
| `--step-4` | 31px / 1.12 | hero (mobile) |
| `--step-5` | clamp(2rem, 1.35rem + 3vw, 2.875rem) / 1.08 | hero display, `text-wrap: balance` |

Micro-labels (eyebrows, field labels, result-section heads): `--step--2`, weight 600,
uppercase, tracking 0.06–0.2em — the scan layer. Weights: 400/600/700/800 only. Numerals in
stats: weight 800, tracking −0.02em. Paragraphs: `text-wrap: pretty` where supported.

---

## 4. Spacing scale and shape (→ spacing-system)

4px ladder, one vocabulary:

```
--space-1: 4px   attachment (icon↔label, chip↔text)
--space-2: 8px   control (label↔input, inside badges)
--space-3: 12px  task (list items, chip gaps)
--space-4: 16px  group (form fields, card padding floor)
--space-5: 24px  group break (result sections, panel gutters)
--space-6: 32px  region (panel padding, hero→grid)
--space-7: 48px  region break (view tops on mobile)
--space-8: 64px  chapter rhythm (hero padding)
--space-section: clamp(48px, 32px + 4vw, 88px)
```

Relationships: attachment `--space-1/2`, control `--space-2/3`, task `--space-3/4`,
group `--space-4/5`, region `--space-6/7`, chapter `--space-8/section`. Rhythm is
**metronomic-compact inside tool panels** (predictability under stress) and **breathes at
home** (hero, bento). Arbitrary margins are forbidden; any exception gets a comment naming
the observed-hierarchy reason.

Shape: radius ladder `--radius-sm 10 · --radius 16 · --radius-lg 24 · --radius-xl 32 ·
--radius-full 999`. Controls and chips = full pills; cards 16–24; hero panels 32
(double-bezel: outer 32 shell + inner radius−3). Elevation: flat + hairline borders by
default; ONE diffused shadow scale (`--shadow-card/hover/diffused/elevated`), warm-tinted
shadows on light, black-based on dark. No border+heavy-shadow together.

---

## 5. Component inventory + states (→ component-states, empty-states)

Every interactive component ships: default, hover (pointer only), **focus-visible**
(author ring, never removed), active, disabled (+reason text), and where async: busy with
request-ownership. Non-color cues accompany every state color.

| Component | Contract |
| --- | --- |
| **Buttons** | `btn-primary` (green pill, one per view max), `btn-secondary` (slate-tinted outline), `btn-ghost` (quiet inline), `btn-danger` (coral — stop/delete only), `btn-sm` modifier. Busy = disabled + "Analyzing…" label swap. All have `:focus-visible`. |
| **Cards** | `entry-card` (bento, keyboard-focusable role=button), `dash-card`, `profile-card`, `track-item`, `panel`+`panel-inner` (double-bezel workbench). Hover lifts 2–4px; active settles down. |
| **Forms** | `field-label` micro-label; inputs on `--color-input` with 1.5px border; focus = accent border + 4px tint ring; textarea resizable vertical. `form-row` wraps; stacks below 680px. |
| **Banners** | `needs-human-banner` (coral tint + 3px left bar, `role=alert`, leads the DOM); `flag-warning/info/danger` (tint + left bar); emergency escalation = needs-human + urgency-HIGH adjacency (§6). |
| **Badges** | `urgency-high/medium/low` (filled-weight pills, verdict only); `urgency-unavailable` (neutral, bordered, sentence-case — never coral); `track-status`; `risk-chip` set; `entity-chip` set; `demo-badge` (slate outline "DEMO"); privacy chip (lock + "Stays on this device"). |
| **Tables** | `ha-table`: hairline rows, mono numerals, right-aligned money, header micro-label style; wraps in labelled horizontal-scroll region only when truly wide. |
| **Modals** | native `<dialog>` (`ha-dialog`): centered card, backdrop dim, focus moves in, Esc/cancel restores invoker. Used for destructive confirms only. |
| **Toasts** | `ha-toast`, `role=status`, bottom-center pill, auto-dismiss 4s + hover persists; never the only record of an event. |
| **Empty states** | icon (40px, 0.4 opacity) + heading + one next action. First-run teaches; no-results names the filter; never a blank. |
| **Loading** | skeleton lines matching final geometry; shimmer honors reduced-motion. |
| **Transcript (Recorder)** | speaker-turn rows: mono timestamp, speaker label chip, final text solid; **draft/interim text rendered muted+italic** (never indistinguishable from final); `[inaudible]` markers styled as honest gaps, not guesses. |
| **Recording UI** | pulse dot (the only glow in the product), timer (mono), waveform bars (CSS, static under reduced-motion), stop = `btn-danger`. |
| **Skeletons** | `skeleton-line w-*` widths; shimmer 1.8s. |

Disabled never appears without its reason adjacent. Async buttons prevent double-dispatch
(`disabled` during flight; only the owning request settles the region).

---

## 6. The Honesty Lane (signature system)

Four mutually exclusive species. Rendering rules are law; the visual audit fails if any
species can be mistaken for another.

| Species | Visual grammar | Semantics |
| --- | --- | --- |
| **NEEDS_HUMAN** | Coral tint + 3px coral left bar + bold "This needs a human decision." + `role="alert"` + real-human resources block. Leads the result DOM, before any badge. | The system refused to decide. First-class, never styled down. |
| **Unavailable** | Neutral: `--status-neutral` gray ink on elevated surface, **1px dashed border**, sentence case, no hue, no icon that implies alarm: "Model unavailable — no urgency assessment was made." | An absence. Never a rating, never danger-colored, never uppercase. |
| **Urgency verdict** | Filled pills, uppercase, weight 700: LOW green / MEDIUM ochre / HIGH coral. HIGH additionally carries a leading dot (non-color cue). | A real verdict only. No coercion of missing values into a level. |
| **Emergency exception** | Escalation stack: urgency-HIGH badge + needs-human banner + emergency-services line, adjacent and loud. The one place the system shouts — because the entity layer flagged emergency-class terms at high confidence on ANY build. | Safety leg that must not depend on the optional model. |

Adjacent-rule: a result may show at most one of {NEEDS_HUMAN banner, urgency verdict};
unavailable may coexist below a banner (it explains *why*). Demo/synthetic output always
carries the `demo-badge` and never uses verdict or banner styling.

---

## 7. Motion principles (→ micro-motion)

- Purpose only: acknowledgement (press, 120–160ms), insertion (results/transcript turns,
  200ms ease-out), route (view switch, 320ms ease-out custom curve). Nothing moves without
  a reason; nothing celebrates.
- Compositor-safe properties only (`transform`, `opacity`); durations/easings are tokens
  (`--dur-1/2/3`, `--ease-out`).
- **The recording pulse is the only live-state animation** (glow = live, glass-law 18).
  Waveform bars animate only while recording.
- Reduced motion: one project-wide contract — spatial movement removed, content and labels
  intact, shimmer/pulse/waveform static. No-transition is a usable equivalent state, never
  a broken one.
- Scroll-reveal: content starts visible; JS marks only offscreen elements pending after the
  observer attaches (no-JS never hides the hero).

---

## 8. Accessibility rules (→ a11y-pass)

- WCAG 2.2 AA is the bar we test against, claimed as "accessibility-minded" in copy —
  never as certification.
- Visible focus on every interactive element (author `:focus-visible` rings, 2px + offset).
- Every view is a named region (`aria-labelledby` to its real h2); one h1 per page; heading
  outline never skips levels.
- View switches move focus into the revealed content (first heading).
- Contrast: body ≥4.5:1, UI/marks ≥3:1, measured per theme on real surfaces (pinned by
  `test_presentability.py`).
- Statuses announce via `role=status`/`alert` live regions; motion and color never carry
  meaning alone (dot + label, bar + label).
- Keyboard path for everything, including the demo recorder (consent checkbox → start →
  stop → summary). Targets ≥40px. Reflow at 320px and 400% zoom: no horizontal scrolling of
  reading content; wide tables get a labelled scroll region.

---

## 9. Voice & tone

- Plain language at a 8th-grade reading level; medical jargon is decoded, never performed.
- Calm, direct, second person. "We could not reach the server." not "Error 503."
- Honesty in copy: "no urgency assessment was made" — never "low risk"; "this needs a human
  decision" — never "please consult a professional" as a hedge appended to a confident answer.
- Never minimize: no "just", no "simply", no "don't worry". Never celebrate ("Great!").
- Boundaries stated once, plainly, where relevant: software, not a clinician; local-only.

---

## 10. Refusals (what this system will NOT do)

- No third-party font/asset CDNs → system stack (privacy-absolute).
- No glassmorphism/backdrop-blur on content, no gradient bodies, no purple/AI-default palettes.
- No stock photography, illustration, or decorative imagery → one functional SVG icon system.
- No confetti, bounce, autoplaying motion, or celebratory animation → restrained tokens only.
- No unlabeled synthetic data → demo mode is badged and stated.
- No tooltip-only state explanations → states are visible in the layout.
- No second accent competing with green → one primary, four status hues with jobs (§2).
- No disabled-without-reason, no default-only controls, no removed focus rings.

---

## 11. Canonical token block

The living source is `healthadvocate/static/styles.css` (single `:root` block + one
`[data-theme="dark"]` remap; the suite parses these blocks). Shape:

```css
:root {
  /* primitives */  --paper-50…300; --green-600/700; --ochre-500; --coral-500;
                    --ochre-ink-600; --coral-ink-700; --slate-ink-600; …
  /* semantic */    --color-bg/surface/surface-2/surface-3/input; --color-text{-muted,-subtle};
                    --color-border{-soft}; --color-primary{,-hover,-tint,-tint-strong,-on-primary};
                    --status-danger{,-ink,-tint} … --status-neutral{,-ink,-tint}; --color-focus-ring;
  /* type */        --font-sans/mono; --step--2…--step-5;
  /* space */       --space-1…8; --space-section;
  /* shape */       --radius-sm…full;
  /* elevation */   --shadow-card/hover/diffused/elevated;
  /* motion */      --dur-1/2/3; --ease; --ease-out;
  /* legacy aliases (kept for JS class contracts) */ --bg-body…--text-3 → var(semantic)
}
[data-theme="dark"] { /* remaps every semantic token; tuned, not inverted */ }
```

## 12. PWA & mobile-first (CEO amendment, 2026-09-24)

The product ships as an installable PWA; **mobile is the primary case** (medical calls
happen on phones).

- **Mobile-first layout:** one column below 680px; nav is a horizontal scroll rail with
  snap; the Recorder's stop control is a sticky bottom bar inside the thumb arc
  (`env(safe-area-inset-bottom)` honored); nothing interactive under 40px, 44px for primary
  controls, 48px input height; `@media (pointer: coarse)` raises secondary chips to 44px.
- **Installability:** `manifest.webmanifest` (standalone, portrait, theme_color
  `#446e54` on `#faf8f5`, icons 192/512 PNG + maskable + SVG favicon — brand mark only),
  `theme-color` meta per color-scheme, apple-touch-icon, `mobile-web-app-capable`.
- **Offline shell law (health-data):** the service worker (`/sw.js`, scope `/` via
  `Service-Worker-Allowed`) caches **static assets only**; `/api/*` and all non-origin
  traffic are never intercepted and never cached — no patient data in the SW cache, no
  push, no background sync. Offline navigation falls back to the cached app shell; API
  failure offline is an honest failure, never stale data. SW registration is guarded to
  secure contexts (https or localhost).
- **Local notifications:** Notification API via the registered SW only; no push server, no
  network. The UI states the limitation plainly (reminders fire when the app can run
  locally). Spec: docs/PROACTIVE-CATALOG-SPEC.md §5.
- **No third-party origins at all** — fonts, icons, and the manifest are all first-party
  static files (extends the type stance in §0/§3).

## 13. Provenance species (analysis + directory honesty; CEO amendments 2–3, 2026-09-24)

Every machine-derived fact wears its source; the species are mutually exclusive and
inferred data is never styled as confirmed:

| Species | Chip | Grammar | Semantics |
| --- | --- | --- | --- |
| **Extracted** | `prov-extracted` | slate tint, round-dot mark, names its source (call/document/voicemail) | Quoted or read directly from user content — carries its source. |
| **Inferred** | `prov-inferred` | caution tint, square mark, names the pattern | Model-inferred suggestion; review before acting. |
| **Unverified** | `prov-unverified` | neutral dashed, diamond mark + needs-human treatment | Could not be read reliably; excluded from reminders/badges/notifications until a human confirms. |
| **User-confirmed** | `prov-confirmed` | solid green border + ✓ — the only solid species | The person vouched for it; overrides all inference on merge. |

Surfaces: post-call analysis rows (commitments must quote), directory field rows (with
one-tap Confirm), detected deadlines, merge notes ("Merged from N sources: …"). Catalog,
directory, reminders, and their encrypted-storage/merge/analysis contracts are specified in
docs/PROACTIVE-CATALOG-SPEC.md; the recorder runtime in docs/CALL-RECORDER-SPEC.md.

## 14. Build order & audit trail

design-system-interview (this doc) → tokens in `styles.css` → index.html polish (font-CDN
removal, structure) → Call Recorder view + demo → Library + Directory demo views + home
reminders → PWA (manifest/SW/icons/meta) → visual audit loop (screenshots of every view ×
both themes, judged against this spec + the honesty laws, minimum 3 rounds; final shots in
`docs/design/screenshots/`) → suite green → specs
(`docs/CALL-RECORDER-SPEC.md`, `docs/PROACTIVE-CATALOG-SPEC.md`).
