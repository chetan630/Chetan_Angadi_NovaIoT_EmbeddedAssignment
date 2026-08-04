"""
Sensor Manager
--------------
Abstracts sensor acquisition so the rest of the firmware never talks to
hardware directly. In the physical build this wraps I2C/GPIO/ADC drivers
for the SHT41 (temp/humidity), BH1750 (light), LIS3DH (vibration) and the
reed switch / battery divider. In this software prototype it produces
physically-plausible simulated readings and can inject faults on demand so
the reliability behaviour of the rest of the firmware can be demonstrated.

Responsibilities:
  - Read sensor values periodically
  - Validate incoming sensor data (range checks, staleness)
  - Detect invalid readings / communication failures
  - Retry with backoff and fall back to last-known-good value when a sensor
    is temporarily unavailable
  - Report per-sensor health status to the decision engine / event logger
"""

import random
import time


class SensorFault(Exception):
    """Raised by a simulated sensor read to represent a comms/read failure."""
    pass


class Sensor:
    """Base class for a simulated sensor channel."""

    def __init__(self, name, fault_policy):
        self.name = name
        self.fault_policy = fault_policy
        self.consecutive_failures = 0
        self.last_good_value = None
        self.last_good_timestamp = None
        self.available = True
        self.force_fault = False  # used by the demo to inject failures

    def _raw_read(self):
        raise NotImplementedError

    def read(self):
        """Attempt to read the sensor with retry/backoff. Returns a dict:
        {value, valid, stale, error}"""
        backoff = self.fault_policy["retry_backoff_s"]
        max_failures = self.fault_policy["max_consecutive_failures"]

        for attempt in range(len(backoff) + 1):
            try:
                if self.force_fault:
                    raise SensorFault(f"{self.name}: simulated communication failure")
                value = self._raw_read()
                if not self._in_plausible_range(value):
                    raise SensorFault(f"{self.name}: value out of plausible range ({value})")

                self.consecutive_failures = 0
                self.available = True
                self.last_good_value = value
                self.last_good_timestamp = time.time()
                return {"value": value, "valid": True, "stale": False, "error": None}

            except SensorFault as e:
                self.consecutive_failures += 1
                if attempt < len(backoff):
                    time.sleep(0)  # simulated backoff (no real delay in demo)
                    continue
                # Exhausted retries for this cycle.
                if self.consecutive_failures >= max_failures:
                    self.available = False
                if self.last_good_value is not None:
                    return {
                        "value": self.last_good_value,
                        "valid": False,
                        "stale": True,
                        "error": str(e),
                    }
                return {"value": None, "valid": False, "stale": False, "error": str(e)}

    def _in_plausible_range(self, value):
        return True


class TemperatureHumiditySensor(Sensor):
    """Simulated SHT41 temperature + humidity sensor."""

    def __init__(self, fault_policy, scenario_state):
        super().__init__("SHT41 (Temp/Humidity)", fault_policy)
        self.scenario_state = scenario_state

    def _raw_read(self):
        base_temp, base_rh = self.scenario_state.get("temp_rh_target", (5.0, 50.0))
        temp = round(base_temp + random.uniform(-0.3, 0.3), 2)
        rh = round(base_rh + random.uniform(-2.0, 2.0), 2)
        return {"temperature_c": temp, "humidity_rh": rh}

    def _in_plausible_range(self, value):
        return -40.0 <= value["temperature_c"] <= 85.0 and 0.0 <= value["humidity_rh"] <= 100.0


class DoorSensor(Sensor):
    """Simulated magnetic reed switch (GPIO digital input)."""

    def __init__(self, fault_policy, scenario_state):
        super().__init__("Reed Switch (Door)", fault_policy)
        self.scenario_state = scenario_state

    def _raw_read(self):
        return {"door_open": self.scenario_state.get("door_open", False)}


class BatterySensor(Sensor):
    """Simulated battery voltage via resistive divider + ADC."""

    def __init__(self, fault_policy, scenario_state):
        super().__init__("Battery Voltage (ADC)", fault_policy)
        self.scenario_state = scenario_state

    def _raw_read(self):
        base_v = self.scenario_state.get("battery_v", 12.6)
        return {"voltage_v": round(base_v + random.uniform(-0.05, 0.05), 2)}

    def _in_plausible_range(self, value):
        return 0.0 <= value["voltage_v"] <= 30.0


class SensorManager:
    def __init__(self, config, scenario_state):
        fault_policy = config["sensor_fault_policy"]
        self.scenario_state = scenario_state
        self.sensors = {
            "temp_humidity": TemperatureHumiditySensor(fault_policy, scenario_state),
            "door": DoorSensor(fault_policy, scenario_state),
            "battery": BatterySensor(fault_policy, scenario_state),
        }

    def read_all(self):
        return {key: sensor.read() for key, sensor in self.sensors.items()}

    def inject_fault(self, sensor_key, faulty=True):
        if sensor_key in self.sensors:
            self.sensors[sensor_key].force_fault = faulty

    def health(self):
        return {key: s.available for key, s in self.sensors.items()}
