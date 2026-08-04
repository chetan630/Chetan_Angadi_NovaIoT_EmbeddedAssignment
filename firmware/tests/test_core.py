"""
Minimal unit tests for the core firmware logic. Run with:
    python3 -m pytest firmware/tests -q
or, if pytest is unavailable:
    python3 firmware/tests/test_core.py
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.decision_engine import DecisionEngine, Condition
from src.config_manager import DEFAULT_CONFIG, ConfigManager
from src.event_logger import EventLogger


class TestDecisionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine(DEFAULT_CONFIG)

    def _reading(self, temp, rh, valid=True, stale=False):
        return {
            "temp_humidity": {"value": {"temperature_c": temp, "humidity_rh": rh}, "valid": valid, "stale": stale, "error": None},
            "battery": {"value": {"voltage_v": 12.6}, "valid": True, "stale": False, "error": None},
            "door": {"value": {"door_open": False}, "valid": True, "stale": False, "error": None},
        }

    def test_normal(self):
        cond, _ = self.engine.evaluate(self._reading(5.0, 50.0))
        self.assertEqual(cond, Condition.NORMAL)

    def test_warning(self):
        cond, _ = self.engine.evaluate(self._reading(9.0, 50.0))
        self.assertEqual(cond, Condition.WARNING)

    def test_critical(self):
        cond, _ = self.engine.evaluate(self._reading(20.0, 50.0))
        self.assertEqual(cond, Condition.CRITICAL)

    def test_fault_on_missing_data(self):
        reading = self._reading(0, 0)
        reading["temp_humidity"] = {"value": None, "valid": False, "stale": False, "error": "no comms"}
        cond, _ = self.engine.evaluate(reading)
        self.assertEqual(cond, Condition.FAULT)

    def test_stale_never_reads_better_than_warning(self):
        cond, _ = self.engine.evaluate(self._reading(5.0, 50.0, valid=False, stale=True))
        self.assertEqual(cond, Condition.WARNING)


class TestConfigManager(unittest.TestCase):
    def test_nested_partial_update_preserves_siblings(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "config.json")
            mgr = ConfigManager(path)
            ok = mgr.update({"thresholds": {"temperature_c": {"warning": [-3.0, 9.0]}}})
            self.assertTrue(ok)
            cfg = mgr.get()
            self.assertEqual(cfg["thresholds"]["temperature_c"]["warning"], [-3.0, 9.0])
            # sibling "normal" band must survive the partial update
            self.assertEqual(cfg["thresholds"]["temperature_c"]["normal"], [2.0, 8.0])

    def test_invalid_update_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "config.json")
            mgr = ConfigManager(path)
            ok = mgr.update({"sampling_interval_s": -5})
            self.assertFalse(ok)
            self.assertEqual(mgr.get()["sampling_interval_s"], 5)

    def test_corrupt_config_falls_back_to_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "config.json")
            with open(path, "w") as f:
                f.write("{not valid json")
            mgr = ConfigManager(path)
            self.assertEqual(mgr.get()["sampling_interval_s"], DEFAULT_CONFIG["sampling_interval_s"])


class TestEventLogger(unittest.TestCase):
    def test_events_persist_across_instances(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "log.jsonl")
            logger1 = EventLogger(path)
            logger1.log("power_restart", {"note": "boot 1"})
            logger2 = EventLogger(path)
            logger2.log("power_restart", {"note": "boot 2"})
            events = logger2.read_all()
            self.assertEqual(len(events), 2)
            self.assertEqual(events[0]["payload"]["note"], "boot 1")


if __name__ == "__main__":
    unittest.main()
