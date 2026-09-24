# Design System — HealthAdvocate

**Status:** approved (mission-delegated: 2026-09-24 design-system build, branch `feat/design-system-20260924`)
**Next move:** implement `styles.css` token re-architecture → Call Recorder view → 3-round visual audit (all done in this branch; see §12)

`approved` here means: every dimension below is decided from the mission's non-negotiable
product truths plus the shipped code, and is buildable without further confirmation. Where a
choice is an assumption rather than a brief-decided fact, the decision map says so.

---

## 0. The interview (decision snapshot)

Run against the product truths (free open-source advocacy tool; users at their most
vulnerable; local-first privacy-absolute; honest-at-the-glass law) and the shipped
surface (`healthadvocate/static/`: 13 views, warm light/dark themes, founder-built
"Humanistic Medical Advocacy UI").

**What I see:** the strongest signal in the brief is that honesty outranks beauty — the
design must never let a fallback look like an answer. The shipped product already carries a
coherent, brief-supported direction (warm sage green on warm paper, soft structuralism,
bento home) with AA-proven core pairs.
**My recommendation:** formalize and deepen that direction into a token system — "a warm
paper clinic" — rather than replace it. Replacement would be slop-by-preference.
**Why it fits:** vulnerable, overwhelmed people need calm and warmth, not clinical cold and
not startup gloss; the founder-built palette already encodes that correctly.
**Choose:** Fork A formalize (committed) / Fork B re-skin cool-clinical (rejected —
contradicts the advocate-warmth truth and discards AA-proven pairs).

### Decision map (nine dimensions)

| Dimension | Evidence | Decision | Consequence |
| --- | --- | --- | --- |
| `reference` | Shipped styles.css header ("Humanistic Medical Advocacy UI / Soft Structuralism / Asymmetric Bento"); product truths | **committed:** the product's own founder direction, formalized; calm-health restraint (Apple Health/Oura register), never agency-splash | Keep hue families and structure; add the missing token/motion/state layers |
| `personality` | "Used by people at their most vulnerable" | **committed:** calm advocate pole — warm, steady, unhurried; confidence through clarity, not tech gloss | Spacious density, one primary action per view, no celebratory motion |
| `aesthetic` | Derived | **committed:** "A warm paper clinic" — soft structuralism, matte surfaces, hairline borders, diffused ambient shadows; hero on warm paper, tools in double-bezel workbenches | No glass blur on content, no gradients as decoration, no pure-white glare |
| `type` | Local-first privacy-absolute truth vs. shipped Google Fonts CDN; web-typography skill ("a fast system stack is deliberate for operational UI") | **committed:** drop the third-party font CDN entirely; deliberate system stack, personality from scale/weight/tracking; mono role for timestamps/IDs | Zero third-party requests, offline-perfect rendering, no font-flash; `-webkit-font-smoothing` kept |
| `color_mode` | Shipped toggle + AA-proven pairs (test_theme_colors_meet_wcag_aa_contrast) | **committed:** light default + tuned dark (not inverted); dominant warm paper neutrals; green = advocate/primary action; warm ochre = caution; coral = danger/high/needs-human; slate = information | Contrast pairs are pinned by tests; dark theme re-tunes inks per surface |
| `density_shape` | Overwhelmed-audience truth | **committed:** comfortable density; radius ladder 10/16/24/32px; elevation = flat + borders + one diffused shadow scale | Controls never below 40px hit height; cards breathe (24–32px padding) |
| `structure_rhythm` | Shipped home (bento) + tool panels | **committed:** home = hero + asymmetric bento (first card spans) + quiet stat strip; every tool = ONE workbench panel (double-bezel), one primary action; section cadence chapter(view) → region(panel) → group(result-section) | Coverage view folds into the same panel grammar; nav stays a horizontal scroll rail |
| `signature` | Honest-at-the-glass law | **committed:** **the Honesty Lane** — the state-band grammar where NEEDS_HUMAN, unavailable, and urgency verdicts are mutually exclusive visual species and can never impersonate each other (§6) | This is the memorable move: honesty rendered as a system, not a disclaimer |
| `imagery_iconography` | Privacy + seriousness; art-direction skill | **committed:** one inline-SVG icon system (1.5 stroke, round caps, functional only); NO photography, illustration, or decorative imagery anywhere | Icons orient; states carry a non-color cue (shape/pattern) alongside color |

Motion level (optional dimension): **restrained** — acknowledgement 120–160ms, entrances
200–320ms ease-out, one live-state animation in the whole product (the recording pulse;
glow/pulse = live state only).

### Assumptions awaiting confirmation (not blocking; documented, reversible)

- System-font stance over a self-hosted brand webfont. If a brand face is later desired, it
  must be self-hosted (bundled) — never a third-party CDN. Owner: product seat.
- "Recorder" as the nav label (noun cadence of the existing rail). View title is "Call
  Recorder". Owner: product seat.

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

Stance: operational UI for stressed readers — a deliberate system stack (privacy decision,
§0 `type`), personality from scale/weight/tracking rather than the face. Sustained reading
is ragged-right, 45–70ch measure, unitless line-heights.

```
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
