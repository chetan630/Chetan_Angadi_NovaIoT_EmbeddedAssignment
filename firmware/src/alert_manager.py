"""
Alert Manager
-------------
Drives local indication (RGB LED + active buzzer) based on the current
device condition. In hardware this writes to GPIO pins (see
hardware/Pin_Mapping.md); here it prints the equivalent physical state so
the behaviour is observable in the console demo / serial-output equivalent.
"""

from .decision_engine import Condition

_LED_COLOR = {
    Condition.NORMAL: "GREEN",
    Condition.WARNING: "AMBER",
    Condition.CRITICAL: "RED",
    Condition.FAULT: "RED (blinking)",
}


class AlertManager:
    def __init__(self, config):
        self.buzzer_enabled = config["alerts"]["buzzer_enabled"]
        self.led_enabled = config["alerts"]["led_enabled"]
        self.last_condition = None

    def update(self, condition: Condition):
        led = _LED_COLOR[condition] if self.led_enabled else "OFF"
        buzzer_on = self.buzzer_enabled and condition in (Condition.CRITICAL, Condition.FAULT)

        changed = condition != self.last_condition
        self.last_condition = condition

        return {
            "led": led,
            "buzzer": "ON" if buzzer_on else "OFF",
            "changed": changed,
        }
