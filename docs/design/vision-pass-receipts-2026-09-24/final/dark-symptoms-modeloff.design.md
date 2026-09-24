judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/dark-symptoms-modeloff.png)

I can see the image (dark-mode "Symptom Assessment" view, model-off state). Audit below.

## DESCRIPTION

**Layout, top→bottom:** Fixed dark app bar (sage logo badge + "HealthAdvocate" wordmark left; ochre "1 reminder due soon" pill + two circular icon buttons right). Below it a two-row tab nav: row 1 = Symptoms (active sage-tinted pill), Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder; row 2 = Library, Directory, Scanner, Family, Tracks, Coverage, Help (dimmer). Then one centered workbench panel (~72% of canvas width, visible outer bezel + inset content) containing: panel header (small sage icon square + "Symptom Assessment" title + subtitle), uppercase micro-label "WHAT ARE YOU EXPERIENCING?", a ~2-line textarea prefilled "mild headache and dizziness for two days", sage pill button "Assess Symptoms", then a large coral/danger panel (left coral border rule: "This needs a human decision," escalation bullets, divider, "Talk to a real person:" with 988 + SAMHSA numbers and a "Find help near you" link). Below, five numbered micro-caption sections: 1 URGENCY LEVEL (neutral chip "Model unavailable — no urgency assessment was made."), 2 EXPLANATION (honest model-off paragraph), 3 NAME MATCHES — NOT A DIAGNOSIS (headache / dizziness rows with similarity parentheticals), 4 ACTION ITEMS (2 numbered items), 5 NAME OVERLAP (INFORMAL) ("Name overlap: low"). Centered two-line micro disclaimer footer.

**Palette (as named hues):** Background warm near-black charcoal, panel one step lighter — warmth is preserved, so this reads as a sanctioned dark variant of "warm paper." Sage = primary button, active tab, logo/panel icons (correct). Coral = the escalation panel (correct, danger). Ochre = reminder pill (correct, caution). Slate = effectively absent — the info chip reads as un-tinted gray. Text is warm off-white, but secondary tiers drop opacity steeply down the page.

**Type scale:** Wordmark ~14 bold; panel title ~18–20 semibold; body 12–13; section captions 9–10 uppercase tracked; match parentheticals ~10. Three usable tiers, but everything under 11px is fragile at these opacities.

**Spacing rhythm:** Calm and generous between page blocks and between the five sections (~40px); coral panel internal leading is noticeably tighter than the rest. Column grid holds inside the panel (content inset aligns button, label, coral panel).

**Component quality:** Pills/chips/buttons share consistent radii; double bezel on the main panel reads correctly; danger panel's left-border pattern is right. Quality drops in the result sections (opacity, micro type).

## DEFECTS

**P0**
- **§4 ACTION ITEMS (panel, mid-lower):** header and both numbered items render at very low opacity (~30% white on charcoal) — core guidance is effectively illegible. Same failure on the §3 intro line ("These are dictionary name matches…") and the "(…% string similarity)" parentheticals. Sick, overwhelmed users are the stated audience; this fails any contrast floor.
- **Coral escalation panel, line 2 + bullet 1:** garbled safety copy — "…so this is not a rule result. **Band next steps:**" and "Go directly **as help**" are not English; looks like a template/string-format bug on the single most safety-critical surface. Fix copy, then legal-review this panel.
- **§3 intro line, second half:** appears to read "…— an urgency assessment **was made** after…", directly contradicting §1/§2 ("no urgency assessment was made"). If the "no" is genuinely missing, that's a dishonest claim in a medical context; it's currently unreadable anyway (see above). Verify and fix both.

**P1**
- **Progressive dimming §3→§5:** section headers "3 NAME MATCHES…", "4 ACTION ITEMS", "5 NAME OVERLAP…" are each dimmer than 1 and 2. Same-level content must share one text token; a fade down the page reads as broken rendering, not hierarchy.
- **Panel subtitle vs. state:** subtitle still promises "we'll identify possible conditions, **assess urgency**…" while the view's whole point is that no urgency assessment was made. Overpromise/dishonest in the model-off state — swap to state-aware copy.
- **16 tabs, two rows, no grouping (header):** two unexplained tiers (row 2 dimmer but unlabeled, no divider) is IA overload for the target user. Group or demote row 2 behind "More."
- **Two competing primary signals:** the large saturated coral block sits immediately under the sage CTA, so the view reads as an error page while the sage button still invites "assess." In model-off state, promote the human-escalation path and quiet/disable the CTA.
- **§3 match meta:** "headache — **verse match**, 56% string similarity" — "verse" is a broken token (likely "exact"), and if the word appears verbatim in the input, "56% similarity" is wrong data. Verify labels and values; dizziness's "fuzzy match, 40%" looks fine by comparison.

**P2**
- **Right-edge grid (top of screen):** header controls end ~x517, nav row 1 ends ~x504, panel ends ~x530; left edges differ too (panel ~x90 vs nav/logo ~x97). Three right edges on one screen — commit to one column grid.
- **"Model unavailable…" chip (§1):** neutral gray; per system semantics it should carry the slate=info tint.
- **Textarea (~2 lines):** too small for the core input of the view — a sick user will write more; grow to 4+ rows.
- **Coral panel density:** ~12px/1.3 coral-on-maroon is borderline contrast and tighter than the page rhythm; 13px/1.5 minimum.
- **Top-right icon buttons:** ~22px targets, below 24px minimum; reminder pill is borderline too.
- **Footer disclaimer:** ~10px, low emphasis — for a medical disclaimer give it a step more size/contrast.
- **Logo mark (top-left):** circular sage badge + inset rounded-square reads muddy at 24px; simplify to one shape.
- **Dark variant provenance:** warmth is preserved, but confirm this charcoal set is a sanctioned "warm paper" dark token pair — if not, the whole view is off-system.
