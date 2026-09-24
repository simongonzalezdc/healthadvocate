Can see the image clearly — audit below.

## DESCRIBE

**Layout, top to bottom**
1. Header bar: sage logo chip (heart) + "HealthAdvocate" wordmark left; right cluster = coral-outlined pill "● 1 due soon", square-ish home icon button, square-ish moon (theme) button.
2. Nav strip: 10 text tabs (Symptoms → Library); "Bills" active — sage text on a subtly darker pill.
3. One large rounded panel filling the content column: ochre-brown icon chip ($ glyph), sage tracked-uppercase eyebrow "BILL DECODER", one-line body, tracked-uppercase label "PASTE YOUR BILL TEXT", full-width textarea with muted placeholder, sage pill CTA "Analyze Bill" (dark text).
4. Hairline rule, then centered two-line disclaimer with bolded product name.

**Palette as named hues (dark variant)** — near-black charcoal page, panel one step lighter; sage on logo chip / eyebrow / active tab / CTA; coral appears once (header pill); ochre appears once (icon chip, muddy); warm off-white primary text, warm-gray secondary. Coral and ochre each get exactly one appearance, both peripheral.

**Type scale** — coherent ~6-step ramp: ~22px bold wordmark → 16px nav → ~13px tracked uppercase eyebrow/labels → 18px body/placeholder/button → 16px footer. Nothing oversized or shouty.

**Spacing** — ~100px panel padding, calm vertical rhythm, generous footer whitespace. Strongest on-system quality here.

**Component quality** — CTA pill crisp; textarea is browser-default styled (visible native resize grip); icon buttons uniform; active-tab state is color-only.

## DEFECTS

- **P1 — Nav, item 3:** active "Bills" is *lower*-contrast than inactive tabs (mid-tone sage on dark pill vs bright gray labels). Current page reads quieter than its siblings; state is color-only. Fix: brighter/bolder active state or fill inversion.
- **P1 — Header right pill:** "1 due soon" wears coral = danger, but "soon" is caution-grade; system maps this to ochre. It's also the loudest thing in the chrome, competing with the view's single primary action.
- **P1 — Main panel:** the committed double-bezel workbench is not legible in dark mode — reads as a single hairline ring. The material language that distinguishes panels from the page is lost.
- **P2 — Page/panel backgrounds:** read near-neutral charcoal; warm-paper undertone barely survives (identity carried only by accent hues). Verify bg tokens.
- **P2 — Textarea, bottom-right corner:** native browser resize grip visible; free resize can break the panel. `resize: none` or vertical-only.
- **P2 — Bill Decoder icon chip:** one-off muddy brown, ambiguous against the ochre token; caution-adjacent hue sitting on the view's main tool.
- **P2 — Radius system:** pill CTA (~999px) vs ~12px input vs ~24px panel; no readable ramp.
- **P2 — Textarea:** placeholder duplicates the visible label above it, at borderline muted contrast on the panel.
- **P2 — Footer:** disclaimer centered while the entire view is left-set — alignment one-off.

**No P0s** — nothing broken, illegible, or dishonest. Passes worth keeping: exactly one primary action, calm spacing, disciplined accent counts, clean type ramp.
