"""Licence pins (2026-10-28): the repo states one licence, and ships it.

Grounding for every pin here:

- ``LICENSE`` is the Apache License, Version 2.0 text as published at
  https://www.apache.org/licenses/LICENSE-2.0.txt. The fingerprint is taken over
  the *words*, so a reflow passes and an edit of the legal text fails.
- ``README.md`` claimed Apache-2.0 in three places (badge, "licensed under", the
  S+ product table) while the root ``LICENSE`` was MIT — from 2026-07 at the
  latest until 2026-10-28. The governance gate only inventories *dependencies*
  (``healthadvocate/governance/``), so nothing in CI asserted the repo's own
  licence. These pins close that hole.
- ``NOTICE`` is where Apache-2.0 §4(d) attribution lives, because the licence
  text itself carries no copyright line to fill in.
- ``Dockerfile`` hands an image to whoever builds it, and an image is a copy of
  the software: §4(a) requires the licence text and §4(d) the notices, so both
  are copied into the image and pinned here.
"""

import hashlib
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

LICENSE = (ROOT / "LICENSE").read_text(encoding="utf-8")
NOTICE = (ROOT / "NOTICE").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
DOCKERFILE = (ROOT / "Dockerfile").read_text(encoding="utf-8")

# sha256 over " ".join(line.split()) per line, joined by newlines and stripped:
# any change of wording in LICENSE changes this, a whitespace-only reflow does not.
LICENSE_WORDS_SHA256 = "c0ce83e35fe5d08830446c0921d094bc561566f09debe1946fa9ad89106eea8d"


def _word_fingerprint(text: str) -> str:
    normalized = "\n".join(" ".join(line.split()) for line in text.splitlines()).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def copy_lines() -> list[str]:
    """Every ``COPY`` instruction in the Dockerfile, whitespace-normalised."""
    return [
        " ".join(line.split())
        for line in DOCKERFILE.splitlines()
        if line.strip().upper().startswith("COPY")
    ]


class LicenseFileTests(unittest.TestCase):
    """The licence file is the Apache-2.0 text, unmodified."""

    def test_license_file_is_the_apache_2_0_text(self):
        # The title is centre-padded in the published text, hence lstrip().
        self.assertTrue(LICENSE.lstrip().startswith("Apache License"), LICENSE[:40])
        for marker in (
            "Version 2.0, January 2004",
            "http://www.apache.org/licenses/",
            "3. Grant of Patent License.",
            "4. Redistribution.",
            "6. Trademarks.",
            "END OF TERMS AND CONDITIONS",
            "APPENDIX: How to apply the Apache License to your work.",
        ):
            self.assertIn(marker, LICENSE, f"LICENSE lost the {marker!r} marker")

    def test_license_wording_is_unchanged(self):
        self.assertEqual(
            _word_fingerprint(LICENSE),
            LICENSE_WORDS_SHA256,
            "LICENSE text changed; if that was deliberate, update LICENSE_WORDS_SHA256 "
            "in the same commit and say why",
        )

    def test_license_file_is_not_the_mit_text(self):
        self.assertNotIn("Permission is hereby granted, free of charge", LICENSE)
        self.assertFalse(LICENSE.startswith("MIT License"))


class ReadmeClaimTests(unittest.TestCase):
    """What the README promises the reader must be what LICENSE delivers."""

    def test_readme_claims_the_apache_licence_the_file_carries(self):
        self.assertIn("apache license, version 2.0", README.lower())
        self.assertIsNone(
            re.search(r"\bMIT\b", README),
            "README still names MIT; the repo is Apache-2.0",
        )

    def test_readme_has_exactly_one_license_section(self):
        headings = re.findall(r"(?m)^##\s+Licen[cs]e\s*$", README)
        self.assertEqual(
            len(headings), 1, f"README carries {len(headings)} '## License' headings"
        )

    def test_licence_badge_matches_the_licence(self):
        badges = [line for line in README.splitlines() if "img.shields.io/badge/License-" in line]
        self.assertEqual(len(badges), 1, "expected exactly one licence badge")
        self.assertIn("Apache_2.0", badges[0])
        self.assertNotIn("MIT", badges[0])

    def test_readme_points_at_the_notice(self):
        self.assertIn("](NOTICE)", README)


class NoticeTests(unittest.TestCase):
    """Apache-2.0 §4(d): the notices exist and travel with a distributed image."""

    def test_notice_names_the_project_and_the_holder(self):
        self.assertIn("HealthAdvocate", NOTICE)
        self.assertIn("Copyright 2026 Simon Gonzalez De Cruz", NOTICE)

    def test_notice_does_not_promise_vendored_third_party_source(self):
        # The repo vendors nothing today; the NOTICE says so. If someone starts
        # vendoring, this line has to change with it.
        self.assertIn("No third-party source code is vendored", NOTICE)

    def test_image_carries_the_licence_and_the_notice(self):
        copies = copy_lines()
        for name in ("LICENSE", "NOTICE"):
            self.assertTrue(
                any(name in line for line in copies),
                f"Dockerfile has no COPY for {name}; a distributed image would "
                f"break §4(a)/§4(d). COPY lines seen: {copies}",
            )


if __name__ == "__main__":
    unittest.main()
