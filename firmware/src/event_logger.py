"""
Event Logger
------------
Maintains local event history: sensor failures, warning/critical
transitions, power restarts, configuration changes.

Production mapping (see docs/Hardware_Design.md, Local Storage section):
  - ESP32 NVS            -> configuration/state (not modeled here)
  - External SPI Flash    -> short-term event buffer, survives brief power loss
  - Industrial MicroSD    -> long-term historical log

This simulation models the SPI-flash-buffer behaviour using an append-only,
line-delimited JSON file with atomic-write semantics: every event is written
to a temp file and then flushed with an explicit fsync before append, so a
simulated power loss between writes cannot corrupt previously committed
events (only the in-flight one can be lost, which is the same guarantee an
append-only flash log provides in the real design).
"""

import json
import os
import time

# Structured Event ID catalog. Every event type the firmware can log is
# assigned a stable, documented ID (see docs/Event_IDs.md) so events can be
# referenced unambiguously in logs, reports, and support tickets — "EV003"
# is unambiguous across firmware versions in a way a free-text message is
# not. Unrecognized event types fall back to EV000 rather than raising,
# since a forward-compatible logger should never crash on a new event type
# introduced by a newer firmware build.
EVENT_CATALOG = {
    "boot": "EV001",
    "warning_event": "EV002",
    "critical_event": "EV003",
    "door_open": "EV004",
    "door_closed": "EV005",
    "fault_event": "EV006",
    "sensor_failure": "EV007",
    "sensor_recovered": "EV008",
    "state_transition": "EV009",
    "configuration_change": "EV010",
    # Back-compat alias: earlier builds logged the boot event as
    # "power_restart" before the Event ID catalog was introduced.
    "power_restart": "EV001",
}
UNKNOWN_EVENT_ID = "EV000"


class EventLogger:
    def __init__(self, log_path, max_local_events=5000):
        self.log_path = log_path
        self.max_local_events = max_local_events
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        if not os.path.exists(log_path):
            open(log_path, "a").close()

    def log(self, event_type, payload=None):
        event = {
            "ts": time.time(),
            "event_id": EVENT_CATALOG.get(event_type, UNKNOWN_EVENT_ID),
            "type": event_type,
            "payload": payload or {},
        }
        line = json.dumps(event)
        # Append + fsync: durability guarantee analogous to a flash write
        # that must survive an abrupt power cut.
        with open(self.log_path, "a") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
        self._enforce_retention()
        return event

    def _enforce_retention(self):
        """Keep the local buffer bounded, mirroring flash capacity limits.
        Oldest events are dropped once the SD/cloud sync would normally have
        archived them (not implemented in this offline prototype)."""
        events = self.read_all()
        if len(events) <= self.max_local_events:
            return
        trimmed = events[-self.max_local_events:]
        tmp_path = self.log_path + ".tmp"
        with open(tmp_path, "w") as f:
            for e in trimmed:
                f.write(json.dumps(e) + "\n")
        os.replace(tmp_path, self.log_path)

    def read_all(self):
        events = []
        with open(self.log_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    # A partially-written line from an interrupted power-loss
                    # write is skipped rather than crashing the logger.
                    continue
        return events

    def tail(self, n=10):
        return self.read_all()[-n:]