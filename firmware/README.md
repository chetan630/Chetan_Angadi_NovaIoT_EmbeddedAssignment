# NovaIoT FleetGuard — Firmware Prototype (Option B: Software Simulation)

This is a **software simulation** of the firmware, submitted under the
assignment's Option B (no physical hardware required). It implements the
same module boundaries and control flow described in
[`../docs/Firmware_Architecture.md`](../docs/Firmware_Architecture.md), using
simulated sensor drivers instead of real I2C/GPIO/ADC calls, so the
architecture, decision logic, and reliability behaviour can be verified and
demonstrated without an ESP32-S3 board.

It is **not** the production ESP-IDF/Arduino firmware image — see
`docs/Firmware_Architecture.md` for how each module maps to the real
hardware drivers in the intended production build.

## Requirements

- Python 3.8+ (standard library only — no third-party dependencies)

## Run the demo

```bash
cd firmware
python3 main.py
```

This runs a scripted 9-phase scenario covering every required behaviour:

1. Boot / initialization
2. Normal sensor acquisition and classification
3. Drift into WARNING
4. Excursion into CRITICAL
5. Door-open context event during an excursion
6. Sensor communication fault injection → DEGRADED → last-known-good → FAULT
7. Sensor recovery
8. Low battery event
9. Runtime configuration change
10. Simulated power loss + restart, proving the event log persists on disk

Console output shows, per cycle: device state, environmental condition,
simulated LED colour, simulated buzzer state, and raw sensor values.

## Run the unit tests

```bash
cd firmware
python3 -m unittest tests.test_core -v
```

9 tests cover the decision engine's threshold logic, configuration
validation/merge behaviour, and event log persistence.

## Project layout

```
firmware/
├── main.py                  # scripted demo / entry point
├── src/
│   ├── device.py             # top-level orchestrator (main loop)
│   ├── config_manager.py     # load/validate/persist configuration
│   ├── sensor_manager.py     # simulated sensor drivers + fault injection
│   ├── decision_engine.py    # threshold classification (Normal/Warning/Critical/Fault)
│   ├── event_logger.py       # crash-safe append-only event log
│   ├── alert_manager.py      # LED/buzzer state derivation
│   └── state_machine.py      # BOOT/RUNNING/DEGRADED/FAULT/CONFIG states
├── config/
│   └── device_config.json    # generated on first run (persisted config)
├── data/
│   └── event_log.jsonl       # generated on first run (persisted event log)
└── tests/
    └── test_core.py
```

## Inspecting the event log

Each run appends to `data/event_log.jsonl` (one JSON object per line —
delete the file to start fresh). Example entries:

```json
{"ts": 1735000000.1, "type": "critical_event", "payload": {"temp_humidity": {"condition": "CRITICAL", "temperature_c": 14.07, "humidity_rh": 60.7}}}
{"ts": 1735000000.2, "type": "sensor_failure", "payload": {"sensor": "temp_humidity", "error": "SHT41 (Temp/Humidity): simulated communication failure"}}
{"ts": 1735000000.3, "type": "configuration_change", "payload": {"update": {"thresholds": {"temperature_c": {"warning": [-2.0, 8.5]}}}}}
```
