import copy
from decimal import Decimal
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("rubric_score", ROOT / "scripts" / "rubric-score.py")
score = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(score)
CATALOG = json.loads((ROOT / "references" / "framework-catalog.json").read_text())


def evidence(kind="measured", confidence="high"):
    return {
        "type": kind,
        "source": "own export fixture",
        "observed_at": "2026-07-10",
        "confidence": confidence,
    }


def complete_run(framework="ROAS", profile="direct-response", context=None, state="pass"):
    spec = CATALOG["frameworks"][framework]
    if context is None:
        context = {key: "fixture" for key in spec.get("required_context", [])}
        context.update(spec["profiles"][profile].get("context_equals", {}))
        if framework == "C3":
            context["assessment_time"] = "actual"
    items = []
    for ids in score.expected_items(spec, profile).values():
        items.extend({"id": item_id, "state": state, "evidence": evidence()} for item_id in ids)
    return {
        "framework": framework,
        "profile": profile,
        "target": "fixture-target",
        "observed_at": "2026-07-10",
        "context": context,
        "items": items,
    }


def set_item_state(run, item_id, state, reason="fixture inapplicability"):
    item = next(candidate for candidate in run["items"] if candidate["id"] == item_id)
    item.clear()
    item.update({"id": item_id, "state": state})
    if state == "na":
        item["reason"] = reason
    else:
        item["evidence"] = evidence()


def set_dimension_points(run, item_ids, points):
    """Assign pass/partial/fail states that sum to an exact item-point total."""
    passes, remainder = divmod(points, 10)
    partials = 1 if remainder == 5 else 0
    states = (["pass"] * passes + ["partial"] * partials
              + ["fail"] * (len(item_ids) - passes - partials))
    for item_id, state in zip(item_ids, states):
        set_item_state(run, item_id, state)


def set_summary_score(result, value):
    """Keep a synthetic scorer result internally state-machine consistent."""
    result["raw_overall_score"] = value
    result["final_overall_score"] = value
    result["veto_count"] = 0
    result["cap_applied"] = False
    if value >= 75:
        result.update({"status": "DONE", "verdict": "SHIP"})
    else:
        result.update({"status": "DONE_WITH_CONCERNS", "verdict": "FIX"})
    return result


class CatalogTests(unittest.TestCase):
    def test_catalog_is_valid(self):
        self.assertEqual(score.validate_catalog(CATALOG), [])

    def test_c3_rollup_schema_declares_discriminated_properties_at_top_level(self):
        schema = json.loads((ROOT / "references" / "c3-rollup.schema.json").read_text())
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["properties"]), {"scopes", "components"})
        self.assertEqual(
            {tuple(branch["required"]) for branch in schema["oneOf"]},
            {("scopes",), ("components",)},
        )
        scored = schema["$defs"]["scoredResult"]
        self.assertEqual(scored["properties"]["catalog_version"], {"const": "17.0.0"})
        self.assertTrue({
            "status", "verdict", "evidence_coverage", "score_confidence",
            "veto_count", "cap_applied", "raw_overall_score", "final_overall_score",
        }.issubset(scored["required"]))
        self.assertEqual(set(scored["properties"]["verdict"]["enum"]), {"SHIP", "FIX"})

    def test_catalog_contains_eight_frameworks(self):
        self.assertEqual(len(CATALOG["frameworks"]), 8)

    def test_malformed_catalog_fails_closed_without_crashing(self):
        catalog = copy.deepcopy(CATALOG)
        catalog["frameworks"]["ROAS"]["profiles"]["direct-response"]["dimensions"]["R"] = "invalid"
        errors = score.validate_catalog(catalog)
        self.assertTrue(errors)
        self.assertTrue(any("weights do not sum to 1" in error for error in errors))

        for label, mutate in (
            ("catalog_version", lambda value: value.pop("catalog_version")),
            ("external_validity", lambda value: value["semantics"].pop("external_validity")),
            ("confidence factor", lambda value: value["semantics"]["confidence_factors"].__setitem__("high", "1")),
        ):
            with self.subTest(label=label):
                malformed = copy.deepcopy(CATALOG)
                mutate(malformed)
                self.assertTrue(score.validate_catalog(malformed))
                with self.assertRaises(score.RubricError):
                    score.score_run(complete_run(), malformed)


class RubricScoreTests(unittest.TestCase):
    def test_complete_roas_run_scores_and_ships(self):
        result = score.score_run(complete_run(), CATALOG)
        self.assertEqual(result["score_state"], "SCORED")
        self.assertEqual(result["final_overall_score"], 100)
        self.assertEqual(result["verdict"], "SHIP")
        self.assertEqual(result["evidence_coverage"], 100)

    def test_missing_item_is_unknown_and_prevents_total(self):
        run = complete_run()
        run["items"].pop()
        result = score.score_run(run, CATALOG)
        self.assertEqual(result["score_state"], "NOT_SCORED")
        self.assertEqual(result["verdict"], "UNDECIDED")
        self.assertNotIn("raw_overall_score", result)
        self.assertLess(result["evidence_coverage"], 100)

    def test_exact_dimension_math_is_preserved_until_the_final_floor(self):
        core = complete_run("CORE-EEAT", "product-review")
        for item_id in ("O03", "E01", "Exp01", "A07", "T04"):
            set_item_state(core, item_id, "na")
        core_points = {
            "C": 0, "O": 25, "R": 100, "E": 80,
            "Exp": 80, "Ept": 100, "A": 60, "T": 80,
        }
        for dimension, points in core_points.items():
            ids = [item["id"] for item in core["items"]
                   if item["id"] in score.expected_items(
                       CATALOG["frameworks"]["CORE-EEAT"], "product-review"
                   )[dimension] and item["state"] != "na"]
            set_dimension_points(core, ids, points)
        self.assertEqual(score.score_run(core, CATALOG)["raw_overall_score"], 75)

        cite = complete_run("CITE", "default")
        for item_id in ("C05", "E09"):
            set_item_state(cite, item_id, "na")
        cite_points = {"C": 70, "I": 75, "T": 100, "E": 35}
        expected_cite = score.expected_items(CATALOG["frameworks"]["CITE"], "default")
        for dimension, points in cite_points.items():
            ids = [item_id for item_id in expected_cite[dimension]
                   if next(item for item in cite["items"] if item["id"] == item_id)["state"] != "na"]
            set_dimension_points(cite, ids, points)
        self.assertEqual(score.score_run(cite, CATALOG)["raw_overall_score"], 75)

        c3 = complete_run("C3", "ace-awareness")
        c3_points = {"ACE.A": 35, "ACE.C": 15, "ACE.E": 35}
        expected_c3 = score.expected_items(CATALOG["frameworks"]["C3"], "ace-awareness")
        for dimension, points in c3_points.items():
            ids = list(expected_c3[dimension])
            if dimension == "ACE.C":
                ids = ["ACE.C1", "ACE.C2", "ACE.C3", "ACE.C4"]
            set_dimension_points(c3, ids, points)
        self.assertEqual(score.score_run(c3, CATALOG)["raw_overall_score"], 75)

    def test_na_requires_catalog_permission_and_reason(self):
        run = complete_run("SEND", "newsletter")
        e2 = next(item for item in run["items"] if item["id"] == "E2")
        e2.clear()
        e2.update({"id": "E2", "state": "na", "reason": "opens are not used"})
        self.assertEqual(score.score_run(run, CATALOG)["score_state"], "SCORED")
        required = next(item for item in run["items"] if item["id"] == "E1")
        required.clear()
        required.update({"id": "E1", "state": "na", "reason": "not available"})
        with self.assertRaisesRegex(score.RubricError, "cannot be N/A"):
            score.score_run(run, CATALOG)

    def test_single_veto_caps_at_59(self):
        run = complete_run()
        item = next(item for item in run["items"] if item["id"] == "R1")
        item["state"] = "fail"
        result = score.score_run(run, CATALOG)
        self.assertEqual(result["veto_count"], 1)
        self.assertEqual(result["verdict"], "FIX")
        self.assertEqual(result["final_overall_score"], 59)

    def test_multi_veto_blocks_without_execution_failure(self):
        run = complete_run()
        for item in run["items"]:
            if item["id"] in {"R1", "R2"}:
                item["state"] = "fail"
        result = score.score_run(run, CATALOG)
        self.assertEqual(result["status"], "DONE")
        self.assertEqual(result["verdict"], "BLOCK")
        self.assertNotIn("final_overall_score", result)

    def test_incomplete_multi_veto_still_has_completed_block_status(self):
        run = complete_run()
        for item in run["items"]:
            if item["id"] in {"R1", "R2"}:
                item["state"] = "fail"
        run["items"].pop()
        result = score.score_run(run, CATALOG)
        self.assertEqual(result["score_state"], "NOT_SCORED")
        self.assertEqual((result["status"], result["verdict"]), ("DONE", "BLOCK"))

    def test_required_framework_context_is_enforced(self):
        run = complete_run("CITE", "default")
        del run["context"]["peer_cohort"]
        with self.assertRaisesRegex(score.RubricError, "peer_cohort"):
            score.score_run(run, CATALOG)

    def test_ramp_profiles_do_not_mix_time_horizons(self):
        preflight = complete_run("RAMP", "preflight")
        ids = {item["id"] for item in preflight["items"]}
        self.assertIn("P1", ids)
        self.assertNotIn("P2", ids)
        self.assertIn("M1", ids)
        self.assertNotIn("M2", ids)
        outcome = complete_run("RAMP", "outcome")
        outcome_ids = {item["id"] for item in outcome["items"]}
        self.assertNotIn("P1", outcome_ids)
        self.assertIn("P10", outcome_ids)

    def test_echo_asset_gate_contains_only_asset_relevant_controls(self):
        run = complete_run("ECHO", "asset-gate")
        ids = {item["id"] for item in run["items"]}
        self.assertEqual(len(ids), 14)
        self.assertTrue({"E1", "C1", "C10", "H1", "H2", "O1"}.issubset(ids))
        self.assertNotIn("E2", ids)
        self.assertNotIn("H3", ids)
        self.assertEqual(score.score_run(run, CATALOG)["score_state"], "SCORED")

    def test_all_na_weighted_dimension_never_crashes_or_renormalizes(self):
        catalog = copy.deepcopy(CATALOG)
        catalog["frameworks"]["ECHO"]["item_policies"]["O1"].update({
            "applicability": "conditional", "condition": "fixture-only condition",
        })
        run = complete_run("ECHO", "asset-gate")
        o1 = next(item for item in run["items"] if item["id"] == "O1")
        o1.clear()
        o1.update({"id": "O1", "state": "na", "reason": "fixture"})
        result = score.score_run(run, catalog)
        self.assertEqual(result["score_state"], "NOT_SCORED")
        self.assertEqual(result["dimension_coverage"]["O"], 0)

    def test_c3_rollup_rejects_forecast_actual_mixing(self):
        scopes = []
        for profile in ("ace-awareness", "art-awareness", "roi-awareness"):
            run = complete_run("C3", profile, context={
                "scope": profile.split("-", 1)[0],
                "goal": "awareness",
                "assessment_time": "actual",
                "rollup_id": "campaign-1",
            })
            scopes.append(score.score_run(run, CATALOG))
        rollup = score.c3_rollup({"scopes": scopes})
        self.assertEqual(rollup["cvi"], 100)
        mixed = copy.deepcopy(scopes)
        mixed[-1]["context"]["assessment_time"] = "forecast"
        with self.assertRaisesRegex(score.RubricError, "cannot mix"):
            score.c3_rollup({"scopes": mixed})

    def test_profile_context_must_match(self):
        run = complete_run("SEND", "newsletter")
        run["context"]["program_type"] = "promotional"
        with self.assertRaisesRegex(score.RubricError, "must be 'newsletter'"):
            score.score_run(run, CATALOG)

    def test_unknown_fields_and_ambiguous_unknown_fail_closed(self):
        run = complete_run()
        run["surprise"] = True
        with self.assertRaisesRegex(score.RubricError, "unknown audit run fields"):
            score.score_run(run, CATALOG)

        run = complete_run()
        run["items"][0]["extra"] = "ignored-before-v17"
        with self.assertRaisesRegex(score.RubricError, "unknown fields"):
            score.score_run(run, CATALOG)

        run = complete_run()
        item = run["items"][0]
        item["state"] = "unknown"
        with self.assertRaisesRegex(score.RubricError, "Unknown requires a gap reason"):
            score.score_run(run, CATALOG)

    def test_c3_forecast_requires_actual_only_items_to_be_na(self):
        run = complete_run("C3", "roi-awareness")
        run["context"]["assessment_time"] = "forecast"
        actual_only = {"ROI.R1", "ROI.R2", "ROI.I1", "ROI.I2", "ROI.I3"}
        for item in run["items"]:
            if item["id"] in actual_only:
                item_id = item["id"]
                item.clear()
                item.update({"id": item_id, "state": "na", "reason": "forecast read"})
        self.assertEqual(score.score_run(run, CATALOG)["score_state"], "SCORED")

    def test_c3_roi_attribution_failure_emits_results_unverified_flag(self):
        run = complete_run("C3", "roi-conversion")
        next(item for item in run["items"] if item["id"] == "ROI.I3")["state"] = "fail"
        result = score.score_run(run, CATALOG)
        self.assertEqual(result["flags"], [{"id": "ROI.I3", "flag": "results-unverified"}])

    def test_c3_rollup_requires_same_goal_and_rollup_identity(self):
        scopes = []
        for profile in ("ace-awareness", "art-awareness", "roi-awareness"):
            scopes.append(score.score_run(complete_run("C3", profile), CATALOG))
        wrong_goal = copy.deepcopy(scopes)
        wrong_goal[1]["profile"] = "art-engagement"
        wrong_goal[1]["context"]["goal"] = "engagement"
        with self.assertRaisesRegex(score.RubricError, "share one goal"):
            score.c3_rollup({"scopes": wrong_goal})
        wrong_campaign = copy.deepcopy(scopes)
        wrong_campaign[2]["context"]["rollup_id"] = "campaign-2"
        with self.assertRaisesRegex(score.RubricError, "share one rollup_id"):
            score.c3_rollup({"scopes": wrong_campaign})

    def test_c3_components_aggregate_ace_by_budget_and_art_equally(self):
        def result(profile, value, target):
            scored = score.score_run(complete_run("C3", profile), CATALOG)
            scored["target"] = target
            return set_summary_score(scored, value)

        payload = {"components": {
            "ace": [
                {"result": result("ace-awareness", 60, "creator-a"), "weight": 1},
                {"result": result("ace-awareness", 100, "creator-b"), "weight": 3},
            ],
            "art": [
                {"result": result("art-awareness", 80, "asset-a")},
                {"result": result("art-awareness", 100, "asset-b")},
            ],
            "roi": [{"result": result("roi-awareness", 70, "campaign-1")}],
        }}
        rolled = score.c3_rollup(payload)
        self.assertEqual(rolled["scope_scores"], {"ace": 90, "art": 90, "roi": 70})
        self.assertEqual(rolled["component_counts"], {"ace": 2, "art": 2, "roi": 1})
        self.assertEqual(rolled["cvi"], 82)

        missing_weight = copy.deepcopy(payload)
        del missing_weight["components"]["ace"][0]["weight"]
        with self.assertRaisesRegex(score.RubricError, "require a positive budget weight"):
            score.c3_rollup(missing_weight)

    def test_c3_component_averages_remain_exact_until_cvi_floor(self):
        def result(profile, value, target):
            scored = score.score_run(complete_run("C3", profile), CATALOG)
            scored["target"] = target
            return set_summary_score(scored, value)

        payload = {"components": {
            "ace": [
                {"result": result("ace-awareness", 50, "creator-a"), "weight": 1},
                {"result": result("ace-awareness", 50, "creator-b"), "weight": 1},
            ],
            "art": [
                {"result": result("art-awareness", 69, "asset-a")},
                {"result": result("art-awareness", 100, "asset-b")},
            ],
            "roi": [{"result": result("roi-awareness", 100, "campaign-1")}],
        }}
        rolled = score.c3_rollup(payload)
        self.assertEqual(rolled["scope_scores"], {"ace": 50, "art": 84.5, "roi": 100})
        self.assertEqual(rolled["cvi"], 75)

    def test_c3_context_identity_is_typed_before_scoring_and_rollup(self):
        malformed_run = complete_run("C3", "ace-awareness")
        malformed_run["context"]["rollup_id"] = ["campaign-1"]
        with self.assertRaisesRegex(score.RubricError, "rollup_id must be a non-empty string"):
            score.score_run(malformed_run, CATALOG)

        scopes = [
            score.score_run(complete_run("C3", profile), CATALOG)
            for profile in ("ace-awareness", "art-awareness", "roi-awareness")
        ]
        malformed_rollup = copy.deepcopy(scopes)
        malformed_rollup[0]["context"]["rollup_id"] = ["campaign-1"]
        with self.assertRaisesRegex(score.RubricError, "rollup_id must be a non-empty string"):
            score.c3_rollup({"scopes": malformed_rollup})

    def test_c3_weight_runtime_matches_numeric_schema(self):
        def result(profile, target):
            scored = score.score_run(complete_run("C3", profile), CATALOG)
            scored["target"] = target
            return scored

        payload = {"components": {
            "ace": [
                {"result": result("ace-awareness", "creator-a"), "weight": "1"},
                {"result": result("ace-awareness", "creator-b"), "weight": 1},
            ],
            "art": [{"result": result("art-awareness", "asset-a")}],
            "roi": [{"result": result("roi-awareness", "campaign-1")}],
        }}
        with self.assertRaisesRegex(score.RubricError, "positive finite number"):
            score.c3_rollup(payload)

        boolean_weight = copy.deepcopy(payload)
        boolean_weight["components"]["ace"][0]["weight"] = True
        with self.assertRaisesRegex(score.RubricError, "positive finite number"):
            score.c3_rollup(boolean_weight)

    def test_json_decimal_weights_remain_exact_across_cvi_boundary(self):
        def result(profile, value, target):
            scored = score.score_run(complete_run("C3", profile), CATALOG)
            scored["target"] = target
            return set_summary_score(scored, value)

        payload = {"components": {
            "ace": [
                {"result": result("ace-awareness", 0, "creator-a"), "weight": 0},
                {"result": result("ace-awareness", 100, "creator-b"), "weight": 0},
            ],
            "art": [{"result": result("art-awareness", 100, "asset-a")}],
            "roi": [{"result": result("roi-awareness", 100, "campaign-1")}],
        }}
        encoded = json.dumps(payload, separators=(",", ":"))
        encoded = encoded.replace('"weight":0}', '"weight":0.271000000000000001}', 1)
        encoded = encoded.replace('"weight":0}', '"weight":0.728999999999999999}', 1)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            parsed = score.load_json(handle.name)
        rolled = score.c3_rollup(parsed)
        self.assertEqual(str(parsed["components"]["ace"][0]["weight"]), "0.271000000000000001")
        round_tripped = json.loads(
            score.exact_json_dumps({"weight": parsed["components"]["ace"][0]["weight"]}),
            parse_float=Decimal,
        )
        self.assertEqual(round_tripped["weight"], Decimal("0.271000000000000001"))
        self.assertEqual(rolled["scope_scores"]["ace"], 72.9)
        self.assertEqual(rolled["cvi"], 89)

    def test_c3_rollup_rejects_blocked_or_internally_inconsistent_results(self):
        scopes = [
            score.score_run(complete_run("C3", profile), CATALOG)
            for profile in ("ace-awareness", "art-awareness", "roi-awareness")
        ]
        blocked = copy.deepcopy(scopes)
        blocked[0].update({
            "status": "DONE", "verdict": "BLOCK", "veto_count": 2,
            "cap_applied": False, "final_overall_score": 100,
        })
        with self.assertRaisesRegex(score.RubricError, "blocked|SHIP or FIX"):
            score.c3_rollup({"scopes": blocked})

        mismatched = copy.deepcopy(scopes)
        mismatched[0]["final_overall_score"] = 0
        with self.assertRaisesRegex(score.RubricError, "final == raw"):
            score.c3_rollup({"scopes": mismatched})

    def test_c3_rollup_binds_components_to_the_active_catalog(self):
        scopes = [
            score.score_run(complete_run("C3", profile), CATALOG)
            for profile in ("ace-awareness", "art-awareness", "roi-awareness")
        ]
        for version in ("16.0.0", "999.0.0"):
            with self.subTest(version=version):
                forged = copy.deepcopy(scopes)
                for component in forged:
                    component["catalog_version"] = version
                with self.assertRaisesRegex(score.RubricError, "does not match active catalog"):
                    score.c3_rollup({"scopes": forged})

    def test_json_valid_malicious_types_raise_rubric_errors(self):
        mutations = (
            ("framework", lambda run: run.__setitem__("framework", [])),
            ("profile", lambda run: run.__setitem__("profile", {})),
            ("item id", lambda run: run["items"][0].__setitem__("id", [])),
            ("item state", lambda run: run["items"][0].__setitem__("state", {})),
            ("evidence type", lambda run: run["items"][0]["evidence"].__setitem__("type", [])),
            ("evidence confidence", lambda run: run["items"][0]["evidence"].__setitem__("confidence", {})),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                run = complete_run()
                mutate(run)
                with self.assertRaises(score.RubricError):
                    score.score_run(run, CATALOG)

    def test_non_finite_json_constants_fail_before_scoring(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as handle:
            handle.write('{"weight": NaN}')
            handle.flush()
            with self.assertRaisesRegex(score.RubricError, "non-finite JSON constant"):
                score.load_json(handle.name)

    def test_input_file_and_profile_item_counts_are_bounded(self):
        with tempfile.NamedTemporaryFile("wb") as handle:
            handle.write(b" " * (score.MAX_INPUT_BYTES + 1))
            handle.flush()
            with self.assertRaisesRegex(score.RubricError, "byte limit"):
                score.load_json(handle.name)
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/rubric-score.py"), "score", handle.name],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)

        with tempfile.NamedTemporaryFile("wb") as handle:
            handle.write(b"\xff")
            handle.flush()
            with self.assertRaisesRegex(score.RubricError, "utf-8"):
                score.load_json(handle.name)

        run = complete_run()
        run["items"].append(copy.deepcopy(run["items"][0]))
        with self.assertRaisesRegex(score.RubricError, "item maximum"):
            score.score_run(run, CATALOG)

        schema = json.loads((ROOT / "references/audit-run.schema.json").read_text())
        self.assertEqual(schema["properties"]["items"]["maxItems"], 80)

    def test_extreme_numbers_and_deep_context_fail_without_runtime_tracebacks(self):
        huge = complete_run()
        huge["context"]["business_constraint"] = 10 ** 10000
        with self.assertRaisesRegex(score.RubricError, "finite JSON"):
            score.score_run(huge, CATALOG)

        deep = {}
        cursor = deep
        for _ in range(score.MAX_JSON_DEPTH + 2):
            cursor["nested"] = {}
            cursor = cursor["nested"]
        nested = complete_run()
        nested["context"]["business_constraint"] = deep
        with self.assertRaisesRegex(score.RubricError, "finite JSON"):
            score.score_run(nested, CATALOG)

        raw_deep = '{"nested":' * 1100 + "null" + "}" * 1100
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as handle:
            handle.write(raw_deep)
            handle.flush()
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/rubric-score.py"), "score", handle.name],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)

    def test_catalog_canonicalization_is_linear_and_depth_bounded(self):
        nested = "leaf"
        for _ in range(20):
            nested = {"nested": nested}
        encoded = score.canonical_json_value(nested)
        self.assertIsInstance(encoded, tuple)
        self.assertLess(len(repr(encoded)), 5000)

        too_deep = "leaf"
        for _ in range(score.MAX_JSON_DEPTH + 2):
            too_deep = {"nested": too_deep}
        catalog = copy.deepcopy(CATALOG)
        catalog["frameworks"]["CORE-EEAT"]["profiles"]["product-review"][
            "context_equals"
        ]["content_type"] = too_deep
        errors = score.validate_catalog(catalog)
        self.assertTrue(any("bounded finite JSON" in error for error in errors), errors)

    def test_evidence_date_cannot_be_in_the_future_of_the_run(self):
        run = complete_run()
        run["items"][0]["evidence"]["observed_at"] = "2026-07-11"
        with self.assertRaisesRegex(score.RubricError, "after the audit"):
            score.score_run(run, CATALOG)


if __name__ == "__main__":
    unittest.main()
