"""
Device State Machine
---------------------
Top-level operating states for the device, independent of the per-sample
condition (Normal/Warning/Critical) computed by the decision engine.

    BOOT       -> device initializing (config load, sensor init)
    RUNNING    -> normal periodic sampling loop
    DEGRADED   -> operating with one or more sensors unavailable
                  (falls back to last-known-good data / reduced confidence)
    FAULT      -> unrecoverable condition requiring intervention
    CONFIG     -> transient state while applying a validated config update

Transitions are deliberately conservative: the device always prefers to
keep sampling and alerting in a reduced-confidence mode (DEGRADED) rather
than stopping entirely, since silence is worse than a degraded reading for
a monitoring device.
"""

from enum import Enum


class DeviceState(Enum):
    BOOT = "BOOT"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    FAULT = "FAULT"
    CONFIG = "CONFIG"


class StateMachine:
    def __init__(self, logger):
        self.state = DeviceState.BOOT
        self.logger = logger

    def transition(self, new_state: DeviceState, reason=""):
        if new_state == self.state:
            return
        old_state = self.state
        self.state = new_state
        self.logger.log(
            "state_transition",
            {"from": old_state.value, "to": new_state.value, "reason": reason},
        )
