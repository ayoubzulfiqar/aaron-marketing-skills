#!/usr/bin/env python3
"""Regression tests for typed system-catalog architecture invariants."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts" / "check-architecture.py"
    spec = importlib.util.spec_from_file_location("check_architecture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CatalogLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        with (ROOT / "references" / "system-catalog.json").open(encoding="utf-8") as handle:
            cls.catalog = json.load(handle)

    def failures_for(self, catalog):
        failures = []
        paths = self.module.expected_skill_paths(catalog, failures)
        self.module.check_catalog_shape(catalog, paths, failures)
        return failures

    def test_current_layer_declarations_match_membership(self):
        self.assertEqual([], self.failures_for(copy.deepcopy(self.catalog)))

    def test_discipline_layer_declaration_cannot_contradict_membership(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["disciplines"]["narrative"]["layer"] = "L2"
        failures = self.failures_for(catalog)
        self.assertTrue(
            any("narrative declares layer 'L2' but layer membership is 'L1'" in item for item in failures),
            failures,
        )

    def test_protocol_layer_declaration_cannot_contradict_membership(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["protocol"]["layer"] = "L3"
        failures = self.failures_for(catalog)
        self.assertTrue(
            any("protocol declares layer 'L3' but layer membership is 'L4'" in item for item in failures),
            failures,
        )

    def test_bare_root_runtime_commands_are_detected(self):
        self.assertIsNotNone(
            self.module.BARE_ROOT_RUNTIME_COMMAND.search(
                "Run python3 scripts/rubric-score.py score run.json"
            )
        )
        self.assertIsNone(
            self.module.BARE_ROOT_RUNTIME_COMMAND.search(
                'python3 "$AARON_SKILLS_ROOT/scripts/rubric-score.py" score run.json'
            )
        )


if __name__ == "__main__":
    unittest.main()
