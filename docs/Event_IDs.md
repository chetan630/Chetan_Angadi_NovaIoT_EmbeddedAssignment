# Event ID Catalog

Every event the firmware can log is assigned a stable, numbered Event ID
in addition to its human-readable type string. Event IDs give a
version-independent way to reference an event in logs, support tickets,
and the Engineering Report — "EV003" means the same thing across
firmware builds even if the free-text type string or payload shape
changes.

Implemented in [`firmware/src/event_logger.py`](../firmware/src/event_logger.py)
as `EVENT_CATALOG`. Every call to `EventLogger.log()` stamps the event
with its `event_id` automatically based on the event type string passed
in.

## Catalog

| Event ID | Event Type (`type` field) | Description | Trigger |
|----------|---------------------------|--------------|---------|
| EV001 | `boot` | Boot | Device power-on or restart (config loaded, sensors initialized) |
| EV002 | `warning_event` | Warning | A monitored parameter enters the Warning band |
| EV003 | `critical_event` | Critical | A monitored parameter exceeds the Critical threshold |
| EV004 | `door_open` | Door Open | Reed switch reports the container door has opened |
| EV005 | `door_closed` | Door Closed | Reed switch reports the container door has closed |
| EV006 | `fault_event` | Fault | Required sensor data missing/stale beyond retry policy |
| EV007 | `sensor_failure` | Sensor Failure | A sensor read attempt failed after retries were exhausted |
| EV008 | `sensor_recovered` | Sensor Recovered | A previously failed sensor has produced a valid reading again |
| EV009 | `state_transition` | State Transition | The device state machine changed state (see `docs/Firmware_Architecture.md`) |
| EV010 | `configuration_change` | Configuration Change | A validated configuration update was applied |
| EV000 | *(any unrecognized type)* | Unknown Event | Fallback ID for a type string not in the catalog — logged rather than dropped, so an unrecognized event from a newer firmware build is never silently lost |

## Example log entries

```json
{"ts": 1735000000.10, "event_id": "EV001", "type": "boot", "payload": {"note": "device boot"}}
{"ts": 1735000000.25, "event_id": "EV003", "type": "critical_event", "payload": {"temp_humidity": {"condition": "CRITICAL", "temperature_c": 14.07, "humidity_rh": 60.7}}}
{"ts": 1735000000.30, "event_id": "EV004", "type": "door_open", "payload": {}}
{"ts": 1735000000.45, "event_id": "EV007", "type": "sensor_failure", "payload": {"sensor": "temp_humidity", "error": "SHT41 (Temp/Humidity): simulated communication failure"}}
{"ts": 1735000000.60, "event_id": "EV008", "type": "sensor_recovered", "payload": {"sensor": "temp_humidity"}}
{"ts": 1735000000.75, "event_id": "EV010", "type": "configuration_change", "payload": {"update": {"thresholds": {"temperature_c": {"warning": [-2.0, 8.5]}}}}}
```
