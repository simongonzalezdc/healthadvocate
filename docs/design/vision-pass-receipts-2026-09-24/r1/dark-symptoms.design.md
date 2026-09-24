judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-symptoms.png)

Image is visible — proceeding with the audit.

## Describe

**Layout, top to bottom:** Fixed dark app header — sage rounded-square logo mark + white "HealthAdvocate" wordmark left; ochre outlined "⚠ 1 due soon" pill plus two circular icon buttons (bell, moon) right. Below it, a full-width nav strip of ~10 text tabs, "Symptoms" active in a sage pill outline. Main area: one large elevated dark card, top-aligned — coral icon chip, "SYMPTOM ASSESSMENT" small-caps overline, two-line gray description, "WHAT ARE YOU EXPERIENCING?" small-caps label, a large bordered textarea with a gray placeholder, then a sage pill button "Assess Symptoms" (the only primary action). A hairline divider, then a centered two-line gray disclaimer. Bottom ~30% of the viewport is empty background.

**Palette as named hues:** No warm paper anywhere — background is warm near-black charcoal, cards one step lighter. Sage appears (logo, active tab, primary button) and reads correctly. Coral appears as the decorative icon chip. Ochre on the due-soon badge is correct. All body text is slate/dim gray. The system's light "paper" ground is entirely absent.

**Typography:** Compressed scale — two letter-spaced small-caps overlines (~10px equivalent), one ~13px body line, bold wordmark, dim footer. No display-size heading anywhere; the page's only title is a tiny overline.

**Spacing rhythm:** Card padding and internal gaps are generous and consistent; the void under the footer destroys the calm rhythm.

**Component quality:** Button, badge, and tabs are clean and well-shaped. Textarea is a bare thin-border box. Icon buttons are faint.

## Defects

1. **P0 — Global palette.** Committed system is "warm paper neutrals"; this renders as charcoal-on-black with zero paper. Entire off-system ground. If this is a sanctioned dark mode, it has no defined dark tokens (paper/slate roles are unanchored) — either way it fails the system as shipped.
2. **P1 — Coral misuse, card header.** Coral = danger in the system, but the coral pencil chip fronts a routine assessment entry point. In a medical tool this falsely signals alarm on the screen sick users land on first. Swap to sage or slate.
3. **P1 — Placeholder contrast, main textarea.** Gray placeholder on dark card is near the legibility floor for the core input, for the exact audience (sick, overwhelmed) least able to squint. Also the only "content" the empty state offers — raise contrast a full step.
4. **P1 — Vertical balance, below footer.** Footer sits ~70% down; the remaining ~30% is dead charcoal. Reads unfinished and wastes the calm-spacing value. Center the card vertically or anchor the footer to the viewport bottom.
5. **P1 — Type hierarchy, card header.** "Symptom Assessment" exists only as a 10px overline; no heading weight on the page. The view has no anchor for scanning. Give the card a real title and demote the overline to eyebrow.
6. **P2 — Double bezel missing, main card.** System specifies double-bezel workbench panels; this is a single flat bordered surface.
7. **P2 — Inactive nav + header icon buttons.** Tab labels and the bell/moon glyphs are uniformly dim — icons sit close to invisible against the strip. Lift inactive states one step; keep hierarchy via weight, not near-invisibility.
8. **P2 — Disclaimer legibility, footer.** Safety-critical text ("Always consult a qualified healthcare provider…") is the smallest, dimmest text on the page. Fine as quiet, but it should clear AA at this size.

**What works:** one primary action, sage reserved for it, ochre used correctly for the due-soon caution, disciplined single-card layout. The bones are right; the ground color and the coral chip are the two things I'd block ship on.
