"""
Device
------
Top-level orchestrator: wires config, sensors, decision engine, event
logger, alert manager, and the device state machine together, and runs the
periodic sampling loop. This is the simulation's equivalent of firmware
main.c / app_main().
"""

from .config_manager import ConfigManager
from .sensor_manager import SensorManager
from .decision_engine import DecisionEngine, Condition
from .event_logger import EventLogger
from .alert_manager import AlertManager
from .state_machine import StateMachine, DeviceState


class Device:
    def __init__(self, config_path, log_path, scenario_state):
        self.config_mgr = ConfigManager(config_path)
        config = self.config_mgr.get()

        self.logger = EventLogger(log_path, config["storage"]["max_local_events"])
        self.state_machine = StateMachine(self.logger)
        self.sensors = SensorManager(config, scenario_state)
        self.decision_engine = DecisionEngine(config)
        self.alerts = AlertManager(config)

        self.cycle_count = 0
        self.logger.log("power_restart", {"note": "device boot"})
        self.state_machine.transition(DeviceState.RUNNING, "initialization complete")

    def run_cycle(self):
        """Executes one full sample -> classify -> log -> alert cycle."""
        self.cycle_count += 1
        readings = self.sensors.read_all()
        health = self.sensors.health()

        condition, details = self.decision_engine.evaluate(readings)

        # Device-level state reflects sensor health, independent of the
        # environmental condition being reported.
        if not all(health.values()):
            self.state_machine.transition(DeviceState.DEGRADED, "one or more sensors unavailable")
        elif self.state_machine.state != DeviceState.RUNNING:
            self.state_machine.transition(DeviceState.RUNNING, "all sensors healthy")

        for sensor_key, reading in readings.items():
            if reading.get("error"):
                self.logger.log("sensor_failure", {"sensor": sensor_key, "error": reading["error"]})

        if condition in (Condition.WARNING, Condition.CRITICAL, Condition.FAULT):
            self.logger.log(f"{condition.value.lower()}_event", details)

        alert_state = self.alerts.update(condition)

        return {
            "cycle": self.cycle_count,
            "condition": condition.value,
            "details": details,
            "device_state": self.state_machine.state.value,
            "alert": alert_state,
            "sensor_health": health,
        }

    def apply_config_update(self, partial_update):
        self.state_machine.transition(DeviceState.CONFIG, "applying configuration update")
        ok = self.config_mgr.update(partial_update)
        if ok:
            self.logger.log("configuration_change", {"update": partial_update})
            self.decision_engine = DecisionEngine(self.config_mgr.get())
            self.alerts = AlertManager(self.config_mgr.get())
        self.state_machine.transition(DeviceState.RUNNING, "configuration update finished")
        return ok
