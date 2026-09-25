"""G003 — the contrast matrix: 5 named pairs x (base + 4 palettes) x (light + dark).

Parses the token blocks from styles.css (the same literals the browser
computes), composites tints over surfaces, and measures WCAG 2.x ratios.
Body-size pairs need 4.5:1; the display heading (28px+ bold) qualifies as
large text at 3:1 but is held to 4.5 anyway where achievable.
"""
import re
from pathlib import Path

CSS = Path("healthadvocate/static/styles.css").read_text()


def parse_block(block):
    return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", block))


def token_maps():
    """(palette, theme) -> merged token map. Palette '' = base."""
    maps = {}
    light = parse_block(re.search(r":root\s*\{(.*?)\}", CSS, re.S).group(1))
    dark = parse_block(re.search(r'\[data-theme="dark"\]\s*\{(.*?)\}', CSS, re.S).group(1))
    for pal in ("", "plush", "moss", "blue"):
        sel = f'html[data-palette="{pal}"]' if pal else None
        pl = pd = {}
        if pal:
            m = re.search(re.escape(sel) + r":root\s*\{(.*?)\}", CSS, re.S)
            if m: pl = parse_block(m.group(1))
            m = re.search(re.escape(sel) + r'\[data-theme="dark"\]\s*\{(.*?)\}', CSS, re.S)
            if m: pd = parse_block(m.group(1))
        maps[(pal, "light")] = {**light, **pl}
        maps[(pal, "dark")] = {**light, **dark, **pd}
    return maps


def hexv(tok, key, default=None):
    v = tok.get(key, default or "")
    m = re.search(r"#([0-9a-fA-F]{6})", v)
    return "#" + m.group(1) if m else None


def lum(hexc):
    r, g, b = (int(hexc.lstrip("#")[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def tint_over(tok, tint_key, base_key):
    """composite rgba(var-like tints) written against the same rgb triple"""
    m = re.search(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", tok.get(tint_key, ""))
    if not m:
        return hexv(tok, base_key)
    r, g, b, a = (float(x) for x in m.groups())
    bh = hexv(tok, base_key)
    br, bg_, bb = (int(bh.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (round(r * a + br * (1 - a)), round(g * a + bg_ * (1 - a)), round(b * a + bb * (1 - a)))


PAIRS = [
    # (label, fg token, bg resolver, min)
    ("headline", "--text-1", lambda t: hexv(t, "--bg-body"), 4.5),
    ("body", "--text-2", lambda t: hexv(t, "--bg-body"), 4.5),
    ("secondary-cta", "--accent", lambda t: tint_over(t, "--accent-light", "--bg-body"), 4.5),
    ("placeholder", "--text-3", lambda t: hexv(t, "--bg-input"), 4.5),
    ("nav-secondary", "--text-2", lambda t: hexv(t, "--bg-surface"), 4.5),
    ("chip", "--text-1", lambda t: hexv(t, "--bg-muted"), 4.5),
]


def test_contrast_matrix_all_themes_both_modes():
    failures = []
    for (pal, theme), tok in token_maps().items():
        for label, fg_key, bg_fn, minimum in PAIRS:
            fg = hexv(tok, fg_key)
            bg = bg_fn(tok)
            if not fg or not bg:
                failures.append(f"{pal or 'base'}/{theme}/{label}: token unresolved")
                continue
            r = ratio(fg, bg)
            if r < minimum:
                failures.append(f"{pal or 'base'}/{theme}/{label}: {r:.2f}:1 < {minimum} ({fg} on {bg})")
    assert not failures, "contrast matrix failures:\n" + "\n".join(failures)


def test_coral_hover_is_not_cyclic():
    m = re.search(r"--coral-hover\s*:\s*([^;]+);", CSS)
    assert m and "var(--coral-hover)" not in m.group(1), "cyclic custom property"
