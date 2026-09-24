judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-symptoms-modeloff.png)

I can see the image. Audit follows.

## What I see

**Layout, top-to-bottom:** Dark app chrome. (1) Header bar: sage rounded-square logo mark + "HealthAdvocate" wordmark left; an ochre-ish pill badge reading "⏱ 1 d1w soon" plus two ghost icon buttons (grid, gear) right. (2) Full-width tab strip in a slightly lighter pill bar: Symptoms (active, sage pill), Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder, Library. (3) One large centered charcoal workbench panel: coral asterisk badge + "SYMPTOM ASSESSMENT" eyebrow + description; caps form label; pre-filled textarea ("mild headache and dizziness…"); sage pill button "Assess Symptoms"; then a results block — a coral-bordered maroon card ("This needs a human decision.", garbled step bullet, divider, "Talk to a real person:" with 988 / SAMHSA / navigator links); slate "URGENCY LEVEL" chip ("Model unavailable — no urgency assessment was made."); "EXPLANATION" paragraph; "POSSIBLE CONDITIONS" with "headache (24%)" and "dizziness (10%)"; "ACTION ITEMS" numbered list; "NAME OVERLAP (INFORMAL)" diagnostic. (4) Footer disclaimer outside the panel.

**Palette as named hues:** Background and panel are cold charcoal/near-black — not warm paper. Sage green correctly carries the active tab and the single primary button. Coral correctly carries the danger card (and, wrongly, the intake-header asterisk badge). Slate correctly carries the info chip. Ochre appears only in the cryptic header badge. Warmth: absent.

**Type:** All-caps tracked eyebrows ~9–10px; body ~11–12px; card heading ~13px; tab labels ~11px. One flat, very small scale; hierarchy carried entirely by caps + gray steps.

**Spacing/quality:** Generous, calm vertical rhythm; panel padding consistent; primary button correctly isolated. The textarea shows a native resize handle; the danger card's inner text runs dim; condition rows have an oversized gap between them.

## Defects

**P0**
1. Danger card body text (y≈280–390): dark-red text on dark-maroon fill, and the italic resource lines dimmer still — at ~11px this is borderline illegible. This card carries 988 and SAMHSA crisis numbers; contrast here is a safety issue, not a style issue.
2. Danger card, first bullet: "Use the Symptoms review using the stripped validation errors." — garbled, meaningless sentence; reads as a leaked error template. Dishonest/broken copy in patient-facing UI.

**P1**
3. Whole screen: cold neutral charcoal contradicts the committed warm-paper system. Even as a sanctioned dark variant, it has no warm tint — it reads as a generic devtools theme, not "warm paper clinic."
4. Dev diagnostics leak into patient UI: ACTION ITEMS items 1–2 ("manual Coverage workflow at local checklists", "loopback-only model runtime") and the entire "NAME OVERLAP (INFORMAL)" section. Sick, overwhelmed users cannot act on any of this.
5. "POSSIBLE CONDITIONS" (y≈517–535): precise percentages (24%, 10%) displayed on the same screen that declares "Model unavailable — no urgency assessment was made." Either provenance is wrong or the numbers look fabricated; label the source or suppress.
6. Global type scale: 9–12px body and eyebrow labels in mid-gray on charcoal, for the stated audience — fails basic readability; eyebrows and tab labels likely sit below 4.5:1.
7. Header badge "1 d1w soon": cryptic, looks like a broken template token ("1 d1w"). Illegible meaning even though glyphs render.
8. Double-bezel workbench treatment is absent — the main panel is a single flat rounded card; the committed panel language isn't visible in this view.

**P2**
9. Textarea: native resize handle visible and height fixed and oversized (~70px) for one line of input — off-system affordance.
10. Coral asterisk badge on the neutral intake header — danger accent misapplied as decoration; coral should stay reserved for danger.
11. Conditions list: ~28px dead gap between "headache" and "dizziness" rows; percentage chips ~9px with no bar or scale to support them.
12. SAMHSA line nesting "(1-800-662-HELP (US))" — double-paren awkward; reformat as "1-800-662-4357 · 1-800-662-HELP (US)".
13. Tab strip: 10 items at ~11px with room to spare — fine at this width, but no overflow plan visible.

**Genuinely good, keep:** honest model-unavailable disclosure (slate chip + plain explanation), coral=danger / slate=info semantics, exactly one sage primary action, calm spacing, clear non-replacement footer.
