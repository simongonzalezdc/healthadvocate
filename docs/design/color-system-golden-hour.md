# Color system — golden-hour tokens, measured evidence (2026-09-24)

Hue jobs: emerald ink = the product's voice (actions, brand, health);
marigold = the lamp (warmth, caution, the human hand); coral = danger only;
slate = information only. Neutral temperature: warm cream in light (paper),
green-black in dark (night desk). Chroma policy: accents mid-L high-C; canvas
low-C; chroma tapers at extremes (both canvases ≤ #faf6ec/#0f1712 chroma).

## Measured rendered pairs (WCAG 2.x; AA body ≥ 4.5, large/UI ≥ 3.0)

| Pair | Ratio | Req | Verdict |
| --- | --- | --- | --- |
| light text-1 #1f2620 / body #faf6ec | 14.35 | 4.5 | PASS |
| light text-1 / surface #fffdf7 | 15.22 | 4.5 | PASS |
| light text-2 #5c6055 / body | 5.97 | 4.5 | PASS |
| light text-3 #61645a / body | 5.59 | 4.5 | PASS |
| white / accent #106b3f (primary btn) | 6.57 | 4.5 | PASS |
| white / accent-hover #0c5732 | 8.66 | 4.5 | PASS |
| light text-1 / elevated #f5efdf | 13.49 | 4.5 | PASS |
| ochre-ink #a35414 / warm-tint over cream | 4.94 | 4.5 | PASS |
| coral-ink #b02f1f / coral-tint | 5.77 | 4.5 | PASS |
| slate-ink #35567e / slate-tint | 6.71 | 4.5 | PASS |
| accent / body (links, UI) | 6.09 | 3.0 | PASS |
| warm #c96b1a / body (large marks) | 3.47 | 3.0 | PASS |
| coral #d8402f / body | 4.15 | 3.0 | PASS |
| dark text-1 #f1ecdd / body #0f1712 | 15.44 | 4.5 | PASS |
| dark text-1 / surface #18231c | 13.72 | 4.5 | PASS |
| dark text-2 #c3bfaf / body | 9.89 | 4.5 | PASS |
| dark text-3 #a09c8a / body | 6.61 | 4.5 | PASS |
| body-ink / dark accent #4ecf8d (btn text) | 9.23 | 4.5 | PASS |
| dark text-1 / elevated #131d16 | 14.64 | 4.5 | PASS |
| dark ochre-ink #f4b866 / warm-tint | 9.03 | 4.5 | PASS |
| dark coral-ink #f79b8b / coral-tint | 8.04 | 4.5 | PASS |
| dark slate-ink #a5c8ea / slate-tint | 9.27 | 4.5 | PASS |
| dark accent / body | 9.23 | 3.0 | PASS |
| dark warm #f0a24f / body | 8.67 | 3.0 | PASS |

Non-color cues: statuses carry icon + label + stamp shape (never color alone).
Gamut: all values sRGB-safe; P3 display shifts hue slightly warmer in Safari —
hierarchy preserved (WebKit capture lane verifies).
Interaction states: hover/active derive by L nudge (accent-hover #0c5732
light / #63dba0 dark), not opacity.
