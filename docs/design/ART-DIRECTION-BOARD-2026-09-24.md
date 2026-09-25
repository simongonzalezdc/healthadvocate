# Art direction board — HealthAdvocate (2026-09-24, r5)

CEO verdict this board answers: "everything reads like 5 years old, this needs
life, texture, humanity, DESIGN ART DIRECTION."

## Stance (one line)

For an overwhelmed, sick person at 2am, the screen must feel like **a
caseworker's night desk where someone has been working on your case** —
lamplight over paper, a ledger of what's coming, stamps that mean something,
and a human hand in the margins. Desired response: *"someone is here; someone
has already started fighting for me."* Copy alone cannot say that; only
evidence-of-work imagery can.

## The visual job (not adjectives)

| Element | Job | Implementation |
|---|---|---|
| Lamplight | orient + trust: the page is a lit place, not a void | warm radial that breathes (8s), lights the hero display from upper-left via gradient text |
| Paper | explain: this product is paperwork-fighting | visible grain + fiber flecks, deckled top edge on the lit card, ruled ledger lines behind reminder rows |
| Stamps | controlled emotional cue: statuses are ACTED ON | rubber-stamp treatment (distressed double border, slight rotation, ink color per status) |
| Margin notes | humanity: a person, not a system | handwriting font (local macOS/iOS stacks only — no downloads, local-first law) on one annotation per view, never body copy |
| Micro-motion | life | staggered reveal of ledger rows, stamp thump (1.12→1 settle) on reveal, warm hover lift; all off under prefers-reduced-motion |

## Asset contract

- **Source**: every asset self-authored inline SVG / CSS in this repo. No
  stock, no external hosts, no font downloads.
- **Rights**: ours (authored in-repo); no attribution required.
- **Alt strategy**: decorative SVGs carry `aria-hidden`; semantic content
  stays real text (stamps are styled text, not images of text).
- **Narrow crop**: annotations hide under 640px (margin metaphor needs
  margin); stamps keep ≤3° rotation and pass contrast at 13px mono.
- **Reject criterion**: if a texture/stamp makes a status harder to read or
  the paper makes body copy contrast fail — the texture goes, the words stay.

## Treatment chosen

Primary: **editorial paper-artifact system** (lamplight + paper + stamps +
margin notes), drawn, not photographed. Fallback: the existing icon system
(retains meaning if a layer is disabled).

## Ship check

- [x] Treatment explains what copy cannot (evidence of a human at work)
- [x] Every asset: source=self-drawn, rights=ours, alt decisions recorded
- [x] Narrow composition reviewed (annotations gate at 640px)
- [x] No placeholder/imagined assets — all layers are code in this diff

## Addendum — golden hour (2026-09-24 evening)

The desk now sits at golden hour: cream paper lit by a marigold lamp whose
cone actually falls on the work; emerald ink for everything the product says;
the night shift (dark theme) is a green-black room with a lit lamp — spring
emerald accents, no murk. The lamp grew a visible cone and pool and moved to
inhabit the hero's right half (the trio's dead-zone finding). Handwritten
notes are pen ink (warm ochre), not pencil gray. Tape stays on the featured
card only. Focus is the caseworker's pen: a warm underline beneath the words,
never a box.

## Ship addendum (2026-09-25, PR #51)
The S+ program build landed at honest blind-audit 8 (3 pre-registered two-judge rounds;
the >=9 bar never met; thresholds never moved — receipts in docs/design/audit-2026-09-25/).
Landed with it: one-measure alignment, the friend + custom warm icons, warmth fragments
in every view, radiogroup swatches, AA across all themes, mobile affordances. The nook
kept its stamps, handwriting, tea, and lamp — the over-polish warning held.
