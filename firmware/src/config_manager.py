"""
Config Manager
--------------
Loads, validates, and persists device operational configuration.

Production equivalent: values are stored in ESP32 NVS (Non-Volatile Storage).
Here they are persisted as JSON on disk to keep the simulation portable and
runnable without hardware.

Responsibilities:
  - Load configuration on boot (fall back to safe defaults if corrupt/missing)
  - Validate any incoming configuration change before applying it
  - Apply configuration changes at runtime (simulating a remote config push)
  - Emit a "Configuration change" event through the event logger
"""

import json
import os
from copy import deepcopy

DEFAULT_CONFIG = {
    "sampling_interval_s": 5,
    "thresholds": {
        "temperature_c": {"normal": [2.0, 8.0], "warning": [-2.0, 10.0]},
        "humidity_rh": {"normal": [30.0, 70.0], "warning": [20.0, 85.0]},
    },
    "alerts": {
        "buzzer_enabled": True,
        "led_enabled": True,
        "critical_repeat_s": 10,
    },
    "sensor_fault_policy": {
        "max_consecutive_failures": 3,
        "retry_backoff_s": [1, 2, 4],
    },
    "storage": {
        "buffer_flush_interval_s": 15,
        "max_local_events": 5000,
    },
}


class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = deepcopy(DEFAULT_CONFIG)
        self._load()

    def _load(self):
        """Load config from disk. Falls back to defaults on any failure,
        mirroring the reliability requirement that the device must always
        boot into a known-good state even if stored config is corrupt."""
        if not os.path.exists(self.config_path):
            self._save()
            return
        try:
            with open(self.config_path, "r") as f:
                loaded = json.load(f)
            if self._validate(loaded):
                self.config = loaded
            else:
                raise ValueError("Config failed validation")
        except (json.JSONDecodeError, ValueError, OSError):
            # Corrupt or invalid config -> revert to safe defaults, keep running.
            self.config = deepcopy(DEFAULT_CONFIG)
            self._save()

    def _validate(self, cfg):
        try:
            assert cfg["sampling_interval_s"] > 0
            t = cfg["thresholds"]["temperature_c"]
            h = cfg["thresholds"]["humidity_rh"]
            assert t["normal"][0] < t["normal"][1]
            assert h["normal"][0] < h["normal"][1]
            return True
        except (KeyError, AssertionError, TypeError, IndexError):
            return False

    def _save(self):
        tmp_path = self.config_path + ".tmp"
        with open(tmp_path, "w") as f:
            json.dump(self.config, f, indent=2)
        os.replace(tmp_path, self.config_path)  # atomic on POSIX

    def get(self):
        return deepcopy(self.config)

    @staticmethod
    def _deep_merge(base, override):
        """Recursively merge override into base, returning a new dict.
        Only replaces the specific leaf keys present in override, so a
        partial update (e.g. just the warning band) never silently drops
        sibling keys (e.g. the normal band) at any nesting depth."""
        merged = deepcopy(base)
        for key, value in override.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = ConfigManager._deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    def update(self, partial_update):
        """Apply a runtime configuration change (simulating a remote/config
        push). Returns True on success. Rejects invalid updates and leaves
        the previous configuration untouched."""
        candidate = self._deep_merge(self.config, partial_update)

        if not self._validate(candidate):
            return False

        self.config = candidate
        self._save()
        return True
