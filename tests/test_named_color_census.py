"""THE NAMED-COLOR CENSUS (felt-law discipline, Resonant-grade).

HealthAdvocate's colors are NAMED for their sources (warm oat, brewed
honey, cocoa ink...) and live in TOKEN BLOCKS only. Component rules must
reference var() — a raw hex in a component rule is an anonymous color,
and anonymous colors are how muddy palettes happen.

Allowed homes for hex literals:
  * token blocks — selectors starting with :root, [data-theme,
    html[data-palette, or the dark-theme token block
  * the ART allowlist — the hand-authored scene/lamp inks, which are
    illustration, not UI state
"""
import re
from pathlib import Path

CSS = Path("healthadvocate/static/styles.css").read_text()

ART_ALLOW = {
    "#ffffff",
    # painterly scene: papers, woods, inks, leaves, light
    "#b3703a", "#7a5c38", "#6b8767", "#54714c", "#8a6a45", "#9c6b4a",
    "#7d8f68", "#b5825a", "#a06a62", "#8f7a99", "#efe2c4", "#e0b06a",
    "#8a5f2e", "#ffdf9e", "#9c6b3f", "#6e4a28", "#f0e4cc", "#f4e9cf",
    "#efe2c4", "#f2c98a", "#e8b877", "#cfa06a", "#ffecdc", "#ffd18a",
    "#ffd9a0", "#5f7d55", "#74956a", "#648358", "#7d9c6d", "#8fae77",
    "#ffdf9e", "#7d9a72",
}


def _token_selector(selector: str) -> bool:
    sel = selector.strip()
    return (sel.startswith(":root") or sel.startswith("[data-theme")
            or sel.startswith("html[data-palette"))


def test_component_rules_use_tokens_not_anonymous_hexes():
    code = re.sub(r'url\("data:image[^"]*"\)', "DATAURI", CSS)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    violations = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", code):
        selector = m.group(1).strip()
        if _token_selector(selector):
            continue
        for hexm in re.finditer(r"#[0-9a-fA-F]{6}\b", m.group(2)):
            hexv = hexm.group(0).lower()
            if hexv not in ART_ALLOW:
                violations.append(f"{hexv} in `{selector[:60]}`")
    assert not violations, (
        "anonymous colors in component rules (felt law: hexes live in token "
        "blocks only — name it, token it, or use the art allowlist):\n"
        + "\n".join(violations[:40])
    )
