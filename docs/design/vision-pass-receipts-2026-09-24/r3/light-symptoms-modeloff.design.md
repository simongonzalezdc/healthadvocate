judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-symptoms-modeloff.png)

**DESCRIPTION**

- **Layout (top→bottom):** White header bar — sage logo tile + "HealthAdvocate" wordmark left; ochre "1 reminder due soon" pill + two small icon buttons right. Below it a full-width tab strip: "Symptoms" as the active sage pill, nine gray sibling tabs, tiny overflow chevron at far right. Body is warm-paper with one centered white card (~440px on this viewport): icon chip + "Symptom Assessment" title + two-line subtitle; letterspaced all-caps label; a paper-tinted textarea with sample text; a dimmed sage "Analyzing…" button; then three skeleton bars (short pill, full-width, ~55%). Large calm paper field, then a small centered two-line disclaimer footer.
- **Palette:** Warm paper neutral page bg, white surfaces, sage-green used for the active tab, icon chip, and primary button; ochre on the reminder pill only; warm-slate secondary text, ink headings. No coral present — correct, nothing here is danger.
- **Typography:** ~20px bold card title, ~13px subtitle/body, ~11px letterspaced caps label, ~12–13px tabs, ~11px pill and footer. Hierarchy holds, but subtitle/body/tabs all sit in one compressed 12–13px band.
- **Spacing rhythm:** Generous card padding, even section gaps, big empty paper zone before the footer — the "calm" brief is met.
- **Component quality:** Radii and pill shapes are consistent; the loading state is the weak component — it's under-specified (see P1s).

**DEFECTS**

- **P0:** none found.
- **P1 — Field label, above textarea:** copy typo — "WHAT YOU'RE EXPERENCING:" is missing the "I" (EXPERIENCING). On a medical tool this erodes trust exactly where reassurance matters.
- **P1 — Primary button "Analyzing…" (below textarea):** loading state has no spinner, no status text, no cancel/stop, and the dimmed sage reads as *disabled*, not *working*. For sick, overwhelmed users an indefinite mute button reads as broken.
- **P1 — Skeleton group (lower card):** bare gray bars with no status line ("Checking your symptoms…") or ETA, and it duplicates the button's loading signal — two unrelated indicators instead of one coherent progress state.
- **P2 — Tab strip, far right:** the only affordance for hidden tabs is a ~12px low-contrast chevron; "Recorder"/"Library" crowd it. Show a fade/gradient or wider hit area.
- **P2 — Header reminder pill:** ~11px ochre text on pale ochre is borderline contrast, and as the only saturated element up top it out-competes the sage primary action — tension with "one primary action per view."
- **P2 — Textarea, bottom-right corner:** exposed resize grip lets users drag the field out of the grid; lock or hide it for calm.
- **P2 — Textarea value color:** the sample line is dark enough to read as user-entered content rather than placeholder/example — ambiguous empty-vs-filled state on first run.
- **P2 — Main card:** flat single-bezel white card; the committed double-bezel workbench treatment isn't expressed on the system's primary panel.

Otherwise strong system adherence: paper neutral, single sage action, correct absence of coral, restrained motion implied.
