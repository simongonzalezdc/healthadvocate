judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-directory-live.png)

I can see the image. Audit follows.

## DESCRIBE

**Layout, top to bottom:** Compact top bar (sage shield-check logo + "HealthAdvocate" left; "reminder due soon" outlined pill + two icon-only round buttons right). Global nav strip of ~11 items, "Directory" active in a sage pill, one more item clipped at the right edge. Then one large near-full-width panel: "Directory" header (small person-icon tile left, 3-line lede, small pill button top-right whose label wraps to two lines), full-width search field, chip filter row ("All" active in sage + 6 outlined chips), a legend sentence with three inline provenance pills, then 4 provider cards (Dr. Maya Patel, Riverside Imaging, Aetna member services, Corner Pharmacy), each: icon tile + name + dim right-aligned type meta, dim "Merged from N sources" line, 2–3 field rows (micro-caps label · value · provenance pill · dim "Confirm" action), footer row with outlined "Call" pill + "Items in Library". Centered dim legal disclaimer at page bottom.

**Palette:** Background is warm near-black brown, not paper — panel/card fills step up in warm taupe-brown. Text is warm cream; secondary text warm gray. Sage-green appears on logo, active nav pill, "All" chip, and "YOU CONFIRMED ✓" pills. Ochre on "INFERRED" pills. Slate-gray-blue on "BILL DECODE / VOICEMAIL / DOCUMENT / CALL" pills. **No coral anywhere** (acceptable — no danger state on this view). Hue family is warm and disciplined, but this is a dark theme, not the committed warm-paper surface.

**Typography:** One humanist sans throughout. Scale is compressed: page title only marginally larger than card names; provenance pills and field labels are micro-caps at what looks like 9–10px equivalent — at the legibility floor. Numbers not tabular-differentiated.

**Spacing rhythm:** Genuinely good — generous, even card padding, consistent gaps between cards and sections, calm panel margins. This is the strongest dimension.

**Component quality:** Pills, chips, and cards are geometrically consistent (uniform radii, hairline borders). All actions are outlined/text — there is no filled sage primary anywhere. Hairline borders nearly vanish against the dark fills.

## DEFECTS

**P0**
1. **Nav overflow clip** — top nav, right edge (x≈550–570): last nav item is cut mid-glyph by the panel edge. Broken global chrome, on every page.
2. **Button label wraps** — Directory header, top-right pill (x≈470–500, y≈120–140): uppercase tracked label stacked on two lines ("SHOW / DATA"). Broken button rendering; also ambiguous affordance (export? raw view?).

**P1**
3. **Theme contradicts committed system** — entire view: dark warm charcoal where the system commits to warm-paper light neutrals. Either an undocumented dark variant (then codify warm-dark tokens) or drift. Warmth is preserved, so this is a system violation, not a palette accident.
4. **Systemic AA contrast failures on secondary text** — card "Merged from N sources…" lines, right-aligned type metas ("DOCTOR · ORTHOPEDICS" etc.), per-field "Confirm" actions, and footer disclaimer are dim warm-gray on dark brown, visibly under 4.5:1. For the stated audience (sick, overwhelmed), "Confirm" being the least visible element on every row is a usability problem.
5. **Sage accent dilution / no primary action** — sage is simultaneously active-nav, "All" chip, and "YOU CONFIRMED" success pills. Success state and action accent share one hue, and the view ends with zero distinct primary actions. Violates "one primary action per view" semantics.
6. **Silent truncation in address** — Dr. Maya Patel card, ADDRESS row: "410 Center St, Big C, Portland OR" reads as a mid-word cut with no ellipsis. In a trust-critical record, data that looks clipped is dishonest display; verify value vs. truncation.

**P2**
7. **Weak title hierarchy** — "Directory" (y≈112) barely outranks card names; the 3-line lede outweighs the title.
8. **Inconsistent badge grammar** — legend pills carry leading bullets ("• FROM A CALL") while card pills don't; compounds mix middle-dot ("INFERRED·PATTERN") and space ("BILL DECODE"); ✓ suffix only on confirmed. Pick one system.
9. **Semantic mislabel** — Riverside card, HOURS row: "INFERRED·VOICEMAIL" conflates inference method with source channel; reads wrong next to "VOICEMAIL" as a PHONE provenance.
10. **Legend wraps mid-enumeration** — legend sentence (y≈240–256) breaks between "INFERRED" and "YOU CONFIRMED ✓", producing the run-on "INFERRED YOU CONFIRMED". Keep the three pills on one line or restructure.
11. **Ambiguous icon-only buttons** — top bar right (x≈480–515): bell and crescent glyphs, no labels; at this size undecipherable.
12. **"Reminder due soon" hue uncommitted** — top bar pill reads neutral-warm; if it's a due-soon caution it should be ochre per system.
13. **Double bezel not expressed** — main panel reads as a single hairline bezel; the second bezel is only implied by inner cards. Verify against the workbench-panel spec.
14. **Legend vs card pill mismatch** — "FROM A CALL" pill in the legend reads warmer/greener than the slate "CALL" pill on Aetna's PHONE row; same concept should map to one token.
15. **Active nav placement** — "Directory" sits at the far end of an already-overflowing nav scroller; the active destination is the first thing clipped on narrow viewports.

Not assessable from a still: motion restraint. Not defects: 555 numbers / `.example` domain (demo data).
