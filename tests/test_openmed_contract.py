"""Contract tests pinning the openmed surface HealthAdvocate consumes.

Version-agnostic by construction: every assertion holds at the vendored 1.4.0
AND at the pinned 2.5.0 (Stage 2 bump). A failure here is a bump tripwire,
not a discovery session. This file is the prose-to-code conversion of the
API-compatibility assessment in docs/OPENMED-UPSTREAM-LEVERAGE-2026-09-17.md
§3 (CEO order 2026-09-22; PROSE-TO-CODE-PROGRAM-2026-09-16).

Verification method (both legs must pass):
- vendored leg:  .venv/bin/python -m pytest tests/test_openmed_contract.py -q
                 (repo-root cwd resolves the vendored openmed)
- pinned leg:    pre-import openmed from site-packages, then run pytest
                 (simulates the post-Stage-2 resolution)
"""

from __future__ import annotations

import inspect
from datetime import datetime
from types import SimpleNamespace

import openmed
from openmed import ModelLoader, OpenMedConfig
from openmed.core.pii import DeidentificationResult, reidentify

from healthadvocate.core.engine import _extract_entities

# The three fixed registry model names HealthEngine.preload() resolves
# (healthadvocate/core/engine.py).
ENGINE_REGISTRY_KEYS = (
    "disease_detection_superclinical",
    "pharma_detection_superclinical",
    "anatomy_detection_electramed",
)


class TestImportSurface:
    """engine.py imports exactly these symbols at module import time."""

    def test_top_level_symbols(self):
        for name in (
            "ModelLoader",
            "OpenMedConfig",
            "analyze_text",
            "extract_pii",
            "deidentify",
        ):
            assert hasattr(openmed, name), name
        for name in ("analyze_text", "extract_pii", "deidentify"):
            assert callable(getattr(openmed, name)), name

    def test_core_pii_symbols(self):
        assert inspect.isclass(DeidentificationResult)
        assert callable(reidentify)

    def test_model_loader_and_config_are_classes(self):
        assert inspect.isclass(ModelLoader)
        assert inspect.isclass(OpenMedConfig)


class TestSignatureContract:
    """HealthEngine calls these exact keywords; the params must keep existing."""

    def test_analyze_text_params(self):
        params = inspect.signature(openmed.analyze_text).parameters
        for p in (
            "text",
            "model_name",
            "loader",
            "output_format",
            "confidence_threshold",
            "group_entities",
        ):
            assert p in params, p

    def test_deidentify_params(self):
        params = inspect.signature(openmed.deidentify).parameters
        for p in ("text", "method", "keep_mapping", "loader", "lang"):
            assert p in params, p

    def test_deidentify_default_pii_model_is_concrete(self):
        default = inspect.signature(openmed.deidentify).parameters["model_name"].default
        assert isinstance(default, str) and default, (
            "default PII model must stay a concrete model id, not None/empty"
        )

    def test_reidentify_signature(self):
        params = list(inspect.signature(reidentify).parameters)
        assert params == ["deidentified_text", "mapping"], params

    def test_deidentification_result_fields(self):
        result = DeidentificationResult(
            original_text="Patient called",
            deidentified_text="[NAME] called",
            pii_entities=[],
            method="mask",
            timestamp=datetime.now(),
            mapping={"[NAME]": "Patient"},
        )
        assert result.deidentified_text == "[NAME] called"
        assert result.mapping == {"[NAME]": "Patient"}
        assert isinstance(result.to_dict(), dict)


class TestReidentifyRoundTrip:
    """keep_mapping=True outputs must stay reversible without any model."""

    def test_simple_round_trip(self):
        mapping = {"[NAME]": "Ada Lovelace", "[PHONE]": "555-0100"}
        text = "[NAME] can be reached at [PHONE]."
        assert reidentify(text, mapping) == "Ada Lovelace can be reached at 555-0100."

    def test_repeated_placeholder_restores(self):
        # 1.4.0 carries our offset-safe local patch; 2.5.0 is occurrence-aware.
        # Both must restore repeated identical placeholders.
        assert reidentify("[NAME] met [NAME]", {"[NAME]": "Ada"}) == "Ada met Ada"

    def test_placeholder_scheme_bracketed_uppercase(self):
        # The mask scheme (bracketed UPPERCASE labels) is load-bearing for HA
        # UI copy and the a11y announcements; assert the documented example.
        mapping = {"[DATE]": "2026-09-22"}
        assert reidentify("Visit on [DATE]", mapping) == "Visit on 2026-09-22"


class TestModelRegistryKeys:
    def test_engine_preload_model_names_resolve(self):
        for key in ENGINE_REGISTRY_KEYS:
            info = openmed.get_model_info(key)
            assert info, key

    def test_default_en_pii_model_present(self):
        default = openmed.get_default_pii_model("en")
        assert isinstance(default, str) and default
        assert default.startswith("OpenMed/"), default


class TestHaAdapterExtractEntities:
    """_extract_entities is the duck-typed boundary HA built over openmed
    results (PredictionResult objects, dicts, or raw lists)."""

    def test_object_with_entities_attr(self):
        raw = SimpleNamespace(
            entities=[
                SimpleNamespace(
                    text="influenza", label="Disease", confidence=0.9, start=0, end=10
                )
            ]
        )
        out = _extract_entities(raw, "condition")
        assert len(out) == 1
        assert out[0].text == "influenza"
        assert out[0].label == "Disease"
        assert out[0].category == "condition"

    def test_dict_with_entities(self):
        raw = {"entities": [{"text": "aspirin", "label": "Drug", "confidence": 0.8, "start": 0, "end": 7}]}
        out = _extract_entities(raw, "medication")
        assert len(out) == 1 and out[0].text == "aspirin"

    def test_dict_with_predictions_fallback(self):
        raw = {"predictions": [{"word": "heart", "entity_group": "Anatomy", "score": 0.7, "start": 0, "end": 5}]}
        out = _extract_entities(raw, "anatomy")
        assert len(out) == 1
        assert out[0].text == "heart"
        assert out[0].label == "Anatomy"

    def test_raw_list(self):
        raw = [SimpleNamespace(text=" fever ", label="Disease", confidence=0.5, start=0, end=6)]
        out = _extract_entities(raw, "symptom")
        assert len(out) == 1 and out[0].text.strip() == "fever"

    def test_empty_and_unknown_shapes_return_empty(self):
        assert _extract_entities(None, "x") == []
        assert _extract_entities(42, "x") == []
        assert _extract_entities({}, "x") == []
