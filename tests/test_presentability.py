from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PresentabilityTests(unittest.TestCase):
    def test_requirements_cover_local_runtime_imports(self):
        requirements = (ROOT / "healthadvocate" / "requirements.txt").read_text()

        for package in (
            "fastapi",
            "uvicorn",
            "pydantic",
            "openai",
            "openmed",
            "faker",
            "pysbd",
            "transformers",
            "huggingface-hub",
            "accelerate",
            "tokenizers",
        ):
            self.assertIn(package, requirements)

    def test_dockerfile_installs_same_requirements_file(self):
        dockerfile = (ROOT / "Dockerfile").read_text()

        self.assertIn("COPY healthadvocate/requirements.txt", dockerfile)
        self.assertIn("pip install --no-cache-dir -r /tmp/requirements.txt", dockerfile)
        self.assertIn("openai", (ROOT / "healthadvocate" / "requirements.txt").read_text())

    def test_local_only_security_defaults_are_configurable(self):
        app_py = (ROOT / "healthadvocate" / "app.py").read_text()

        self.assertIn("HEALTHADVOCATE_ALLOW_ORIGINS", app_py)
        self.assertNotIn('allow_origins=["*"]', app_py)
        self.assertIn('"http://127.0.0.1:8080"', app_py)

    def test_frontend_uses_delegated_handlers_for_primary_actions(self):
        html = (ROOT / "healthadvocate" / "static" / "index.html").read_text()
        app_js = (ROOT / "healthadvocate" / "static" / "app.js").read_text()

        self.assertNotIn("onclick=", html)
        for action in (
            "assess-symptoms",
            "decode-document",
            "decode-bill",
            "fight-denial",
            "check-drug",
            "prepare-appointment",
            "translate-discharge",
            "create-second-opinion",
            "scan-community",
            "create-family-profile",
            "create-track",
        ):
            self.assertIn(f'data-action="{action}"', html)
            self.assertIn(f"'{action}'", app_js)
        self.assertIn("const buttonEvent = { currentTarget: btn }", app_js)

    def test_frontend_sanitizes_dynamic_css_classes(self):
        app_js = (ROOT / "healthadvocate" / "static" / "app.js").read_text()

        self.assertIn("urgencyBadgeHtml", app_js)
        self.assertIn("safeTrackStatus", app_js)
        self.assertNotRegex(app_js, re.compile(r'urgency-\\$\\{this\\.escapeHtml\\(data\\.urgency\\)\\}'))
        self.assertNotRegex(app_js, re.compile(r'class="track-status \\$\\{safeStatus\\}"'))

    def test_symptom_glass_renders_needs_human_wrapper_and_unavailable_badge(self):
        app_js = (ROOT / "healthadvocate" / "static" / "app.js").read_text()
        styles = (ROOT / "healthadvocate" / "static" / "styles.css").read_text()

        # Audit D2 round 2: the backend's external urgency "unavailable"
        # (model off, no NER trigger) must render as itself — never
        # laundered to a rubric level, never in high styling.
        self.assertIn("'low', 'medium', 'high', 'unavailable'", app_js)
        self.assertIn(".urgency-unavailable {", styles)
        block = re.search(
            r"\.urgency-unavailable\s*\{[^}]*\}", styles, re.S
        )
        self.assertIsNotNone(block, "urgency-unavailable badge style missing")
        self.assertNotIn(
            "--coral", block.group(0), "unavailable must not wear danger/high styling"
        )

        # The NEEDS_HUMAN wrapper (urgency_decision) must reach the
        # patient: banner + the wrapper reason + the deterministic
        # allowed_next_steps, all escaped.
        self.assertIn("data.urgency_decision", app_js)
        self.assertIn("needs-human-banner", app_js)
        self.assertIn('role="alert"', app_js)
        self.assertIn("this.escapeHtml(decision.reason", app_js)
        self.assertIn("this.escapeHtml(step)", app_js)
        self.assertIn("decision.allowed_next_steps", app_js)
        self.assertIn(".needs-human-banner {", styles)

    def test_view_switches_move_focus_into_the_revealed_content(self):
        app_js = (ROOT / "healthadvocate" / "static" / "app.js").read_text()

        # WCAG 2.1 SC 2.4.3 (Level A): the control that triggers a view switch
        # or the coverage form→panel re-render is hidden with the content it
        # belonged to, which strands keyboard focus on document.body with the
        # new content unannounced. The switch itself must hand focus to the
        # revealed content: first heading, else the container (tabindex=-1).
        # Behavioral proof: tests/browser/focus-order-regression.js.
        self.assertIn("focusInto(container)", app_js)
        self.assertIn("container.querySelector('h1, h2, h3') || container", app_js)
        self.assertIn("target.tabIndex = -1;", app_js)
        self.assertIn("this.focusInto(target);", app_js)
        self.assertIn(
            "this.focusInto(document.getElementById('coverage-panel'));", app_js
        )


    def test_heading_outline_has_no_level_skips_and_tool_views_have_real_titles(self):
        html = (ROOT / "healthadvocate" / "static" / "index.html").read_text()
        styles = (ROOT / "healthadvocate" / "static" / "styles.css").read_text()

        # WCAG 2.1 SC 1.3.1 advisories from the 2026-09-13 machine a11y pass:
        # the home outline skipped h1 -> h3 (entry-card titles sit directly
        # under the hero h1), and every tool view's visual title was a styled
        # span.panel-eyebrow, so screen-reader heading navigation found
        # nothing to orient on outside home and coverage. Tool views now
        # follow the coverage pattern: a real h2 title (the panel-eyebrow
        # class keeps the visual treatment) with the section named through
        # aria-labelledby. Behavioral proof: tests/browser/ax-audit.js.
        self.assertNotIn('<span class="panel-eyebrow">', html)

        headings = re.findall(r"<h([1-6])[^>]*>", html)
        self.assertEqual(headings.count("1"), 1)
        for prev, level in zip(headings, headings[1:]):
            self.assertLessEqual(
                int(level) - int(prev),
                1,
                f"heading outline skips levels h{prev} -> h{level}",
            )

        for view_id, attrs, body in re.findall(
            r'<section id="(view-[\w-]+)"([^>]*)>(.*?)</section>', html, re.S
        ):
            if view_id == "view-home":
                continue  # titled by the page h1
            first = re.search(r'<h([1-6])[^>]*id="([\w-]+)"', body)
            self.assertIsNotNone(first, f"{view_id} has no programmatic heading")
            self.assertEqual(
                first.group(1),
                "2",
                f"{view_id}'s first heading must be its view-title h2",
            )
            self.assertIn(
                f'aria-labelledby="{first.group(2)}"',
                attrs,
                f"{view_id} must be a named region via aria-labelledby to its h2",
            )

        # heading styles follow the promoted tags (entry cards h2, dash cards h3)
        self.assertIn(".entry-card h2 {", styles)
        self.assertIn(".entry-card:first-child h2 {", styles)
        self.assertIn(".dash-card h3 {", styles)
        self.assertNotIn(".entry-card h3 {", styles)
        self.assertNotIn(".dash-card h4 {", styles)

    def test_copy_avoids_compliance_and_certification_overclaims(self):
        combined = "\n".join(
            [
                (ROOT / "README.md").read_text(),
                (ROOT / "healthadvocate" / "static" / "index.html").read_text(),
            ]
        ).lower()

        self.assertNotIn("hipaa compliant", combined)
        self.assertNotIn("wcag 2.1 aa standards", combined)
        self.assertIn("privacy-preserving", combined)
        self.assertIn("accessibility-minded", combined)

    def test_deidentification_failure_does_not_return_raw_text_for_llm(self):
        engine_py = (ROOT / "healthadvocate" / "core" / "engine.py").read_text()

        self.assertIn("DEIDENTIFICATION_FAILED_PLACEHOLDER", engine_py)
        self.assertIn('"_deidentification_failed"', engine_py)
        self.assertNotIn("return text, {}", engine_py)

    def test_every_button_class_has_a_visible_focus_indicator(self):
        styles = (ROOT / "healthadvocate" / "static" / "styles.css").read_text()
        html = (ROOT / "healthadvocate" / "static" / "index.html").read_text()

        for class_name in set(re.findall(r'class="[^"]*?\b(btn-[\w-]+)', html)):
            self.assertIn(
                f".{class_name}:focus-visible",
                styles,
                f".{class_name} buttons render without an author focus indicator",
            )

    def test_theme_colors_meet_wcag_aa_contrast(self):
        styles = (ROOT / "healthadvocate" / "static" / "styles.css").read_text()

        def block(selector):
            match = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", styles, re.S)
            self.assertIsNotNone(match, f"{selector} block missing from styles.css")
            vars_ = {}
            for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", match.group(1)):
                vars_[name] = value.strip()
            return vars_

        def parse_color(value):
            value = value.strip()
            if value.startswith("#"):
                return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5)) + (1.0,)
            m = re.match(r"rgba?\(([^)]+)\)", value)
            parts = [p.strip() for p in m.group(1).split(",")]
            rgb = tuple(float(p) for p in parts[:3])
            alpha = float(parts[3]) if len(parts) > 3 else 1.0
            return rgb + (alpha,)

        def luminance(color):
            def lin(v):
                v /= 255
                return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

            r, g, b, _ = color
            return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

        def contrast(fg, bg):
            l1, l2 = luminance(fg), luminance(bg)
            return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

        def composited(tint_value, over):
            tint = parse_color(tint_value)
            a = tint[3] + over[3] * (1 - tint[3])
            return tuple(
                (tint[i] * tint[3] + over[i] * over[3] * (1 - tint[3])) / a
                for i in range(3)
            ) + (a,)

        light = block(":root")
        dark = block('[data-theme="dark"]')
        white = parse_color("#ffffff")

        surfaces = ("--bg-body", "--bg-surface", "--bg-elevated", "--bg-input")
        for theme in (light, dark):
            for text_var in ("--text-1", "--text-2", "--text-3"):
                for surface_var in surfaces:
                    ratio = contrast(
                        parse_color(theme[text_var]), parse_color(theme[surface_var])
                    )
                    self.assertGreaterEqual(
                        ratio,
                        4.5,
                        f"{text_var} on {surface_var} measures {ratio:.2f}:1"
                        f" (needs 4.5:1)",
                    )
            # accent used as text on its own tint (nav pills, chips, eyebrows)
            for surface_var in surfaces:
                tinted = composited(
                    theme["--accent-light"], parse_color(theme[surface_var])
                )
                ratio = contrast(parse_color(theme["--accent"]), tinted)
                self.assertGreaterEqual(
                    ratio,
                    4.5,
                    f"--accent text on --accent-light over {surface_var}"
                    f" measures {ratio:.2f}:1 (needs 4.5:1)",
                )

        # filled controls: light theme keeps white ink; dark theme flips to
        # bg-body ink because white on the lighter dark accent fails AA
        self.assertGreaterEqual(contrast(white, parse_color(light["--accent"])), 4.5)
        self.assertGreaterEqual(
            contrast(white, parse_color(light["--accent-hover"])), 4.5
        )
        dark_ink = parse_color(dark["--bg-body"])
        self.assertGreaterEqual(contrast(dark_ink, parse_color(dark["--accent"])), 4.5)
        self.assertGreaterEqual(
            contrast(dark_ink, parse_color(dark["--accent-hover"])), 4.5
        )
        self.assertIn('[data-theme="dark"] .btn-primary', styles)
        self.assertIn('[data-theme="dark"] .skip-link', styles)
        self.assertIn('[data-theme="dark"] .logo-icon', styles)

        # skip link carries an author focus indicator that passes 1.4.11 in
        # both themes (ring on the page background, offset clear of the chip)
        self.assertIn(".skip-link:focus-visible", styles)
        self.assertIn("outline: 2px solid var(--text-1)", styles)


if __name__ == "__main__":
    unittest.main()
