"""Dark theme must win the variables it owns.

Regression pin (2026-09-24): a later bare `:root { --bg-body: ... }`
overwrote [data-theme="dark"]'s body ink — equal specificity, file order
wins — and darkmode rendered a light-paper page under dark chrome.
"""
import re
from pathlib import Path

CSS = Path("healthadvocate/static/styles.css").read_text()


def test_no_bare_root_body_override_after_dark_block():
    dark = CSS.find('[data-theme="dark"] {')
    assert dark != -1, "dark theme block missing"
    for m in re.finditer(r":root\s*(?:,[^{]*)?\{[^}]*--bg-body\s*:", CSS):
        assert m.start() < dark, (
            "a bare :root block sets --bg-body AFTER the dark block and will "
            "overwrite it (equal specificity, file order wins) — scope it "
            "with :not([data-theme=\"dark\"]) or move it before the dark block"
        )
