"""
Decision Engine
---------------
Classifies validated sensor data into an operating condition:

    NORMAL   - all parameters within acceptable range
    WARNING  - a parameter is approaching an unsafe level
    CRITICAL - a parameter has exceeded a safe threshold
    FAULT    - required sensor data is missing/stale beyond policy

Threshold strategy
-------------------
Two-band thresholds per parameter (normal band nested inside a warning band)
are used rather than a single cutoff. This avoids alert "chattering" right
at a boundary and gives operators lead time between WARNING and CRITICAL,
which matters for perishable cold-chain goods where a few minutes of
lead time can prevent product loss. Values outside the warning band are
CRITICAL. The worst condition across all monitored parameters determines
the overall device state (worst-case wins).
"""

from enum import Enum


class Condition(Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    FAULT = "FAULT"

# Ordering used to pick the "worst" condition across parameters.
_SEVERITY = {Condition.NORMAL: 0, Condition.WARNING: 1, Condition.CRITICAL: 2, Condition.FAULT: 3}


def _classify_value(value, bands):
    normal_lo, normal_hi = bands["normal"]
    warn_lo, warn_hi = bands["warning"]
    if normal_lo <= value <= normal_hi:
        return Condition.NORMAL
    if warn_lo <= value <= warn_hi:
        return Condition.WARNING
    return Condition.CRITICAL


class DecisionEngine:
    def __init__(self, config):
        self.thresholds = config["thresholds"]

    def evaluate(self, sensor_readings):
        """
        sensor_readings: output of SensorManager.read_all()
        Returns: (overall_condition: Condition, details: dict)
        """
        details = {}
        worst = Condition.NORMAL

        th_reading = sensor_readings["temp_humidity"]
        if not th_reading["valid"] and th_reading["value"] is None:
            details["temp_humidity"] = {"condition": Condition.FAULT.value, "reason": th_reading["error"]}
            worst = self._worse(worst, Condition.FAULT)
        else:
            temp_c = th_reading["value"]["temperature_c"]
            rh = th_reading["value"]["humidity_rh"]
            temp_cond = _classify_value(temp_c, self.thresholds["temperature_c"])
            rh_cond = _classify_value(rh, self.thresholds["humidity_rh"])

            # Stale readings (last-known-good used after sensor comms failure)
            # are never allowed to read as better than WARNING, since we can
            # no longer vouch for their accuracy.
            if th_reading.get("stale"):
                temp_cond = self._worse(temp_cond, Condition.WARNING)
                rh_cond = self._worse(rh_cond, Condition.WARNING)

            param_worst = self._worse(temp_cond, rh_cond)
            details["temp_humidity"] = {
                "condition": param_worst.value,
                "temperature_c": temp_c,
                "humidity_rh": rh,
                "stale": th_reading.get("stale", False),
            }
            worst = self._worse(worst, param_worst)

        battery_reading = sensor_readings.get("battery")
        if battery_reading and battery_reading["value"] is not None:
            v = battery_reading["value"]["voltage_v"]
            if v < 10.5:
                batt_cond = Condition.CRITICAL
            elif v < 11.5:
                batt_cond = Condition.WARNING
            else:
                batt_cond = Condition.NORMAL
            details["battery"] = {"condition": batt_cond.value, "voltage_v": v}
            worst = self._worse(worst, batt_cond)

        door_reading = sensor_readings.get("door")
        if door_reading and door_reading["value"] is not None:
            details["door"] = {"door_open": door_reading["value"]["door_open"]}

        return worst, details

    @staticmethod
    def _worse(a, b):
        return a if _SEVERITY[a] >= _SEVERITY[b] else b
