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

        self.assertIn("safeUrgency", app_js)
        self.assertIn("safeTrackStatus", app_js)
        self.assertNotRegex(app_js, re.compile(r'urgency-\\$\\{this\\.escapeHtml\\(data\\.urgency\\)\\}'))
        self.assertNotRegex(app_js, re.compile(r'class="track-status \\$\\{safeStatus\\}"'))

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


if __name__ == "__main__":
    unittest.main()
