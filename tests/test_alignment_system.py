"""G001 — the one measure (alignment system) regression pins.

S+ program (PRD v2.2): every container aligns to --grid-max (920px);
--max-w is RETIRED; the 1000px panel literal is gone; library and
directory rows share --col-label; sibling cards split the measure
equally with gap == --space-5.
"""
import re
from pathlib import Path

CSS = Path("healthadvocate/static/styles.css").read_text()


def test_grid_max_exists_and_max_w_retired():
    assert "--grid-max: 920px" in CSS, "the measure token is missing"
    assert "--max-w:" not in CSS, "--max-w survived; --grid-max must subsume it"
    assert "var(--max-w)" not in CSS


def test_no_1000px_panel_literal():
    assert "max-width: 1000px" not in CSS, (
        "the 1000px panel literal survived; panels align to var(--grid-max)"
    )


def test_col_label_token_present():
    assert "--col-label: 200px" in CSS
    assert CSS.count("var(--col-label)") >= 1, "--col-label declared but never used"


def test_sibling_cards_equal_split():
    m = re.search(r"\.entry-grid\s*\{[^}]*\}", CSS)
    assert m, "entry-grid rule missing"
    block = m.group(0)
    assert "1fr 1fr" in block, "siblings must split the measure equally"
    assert "var(--space-5)" in block, "card gap must equal the shared padding step"
    assert re.search(r"\.entry-card-primary\s*\{[^}]*grid-column:\s*1\s*/\s*-1", CSS), (
        "the featured card must span the full measure"
    )
