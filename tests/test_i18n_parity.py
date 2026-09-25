"""G002 deliverable — en/es key-set parity, both directions, zero missing.

The plan is explicit: the parity checker did NOT exist on this branch (it was
D118's unlanded work); this story builds its own. Structure check only —
completeness (a string missing from BOTH files) is covered by the data-i18n
presence assertions in the browser batteries, not here.
"""
import re
from pathlib import Path


def catalog_keys(path):
    txt = Path(path).read_text()
    return set(re.findall(r"^\s*'([a-z0-9_.]+)':", txt, re.M))


def test_en_es_key_parity_both_directions():
    en = catalog_keys("healthadvocate/static/i18n/en.js")
    es = catalog_keys("healthadvocate/static/i18n/es.js")
    missing_es = sorted(en - es)
    missing_en = sorted(es - en)
    assert not missing_es, f"keys missing from es.js: {missing_es}"
    assert not missing_en, f"keys missing from en.js: {missing_en}"


def test_every_data_i18n_binding_has_catalog_keys():
    html = Path("healthadvocate/static/index.html").read_text()
    used = set(re.findall(r'data-i18n(?:-placeholder|-aria)?="([a-z0-9_.]+)"', html))
    en = catalog_keys("healthadvocate/static/i18n/en.js")
    missing = sorted(used - en)
    assert not missing, f"data-i18n bindings without en.js keys: {missing}"
