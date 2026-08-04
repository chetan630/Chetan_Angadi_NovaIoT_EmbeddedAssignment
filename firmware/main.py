#!/usr/bin/env python3
"""
NovaIoT FleetGuard - Firmware Prototype
=========================================================================
Runs a scripted demo scenario through the full firmware pipeline:

    sensor acquisition -> condition classification -> event generation
    -> local alerting -> event logging -> configuration change
    -> sensor fault injection -> device restart / log persistence

This is a proof-of-concept demonstrating the firmware architecture
described in docs/Firmware_Architecture.md. It is not the production
ESP-IDF/Arduino firmware image; it models the same modules and control
flow so the design can be verified without physical hardware.

Run:
    python3 main.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from src.device import Device  # noqa: E402

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "device_config.json")
LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "event_log.jsonl")


def banner(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def print_cycle(result):
    print(
        f"[cycle {result['cycle']:02d}] "
        f"state={result['device_state']:<9} condition={result['condition']:<8} "
        f"LED={result['alert']['led']:<15} buzzer={result['alert']['buzzer']}"
    )
    for key, d in result["details"].items():
        print(f"           {key}: {d}")


def run_scenario():
    scenario_state = {"temp_rh_target": (5.0, 50.0), "door_open": False, "battery_v": 12.6}

    banner("BOOT: initializing device (config load, sensor init, state machine)")
    device = Device(CONFIG_PATH, LOG_PATH, scenario_state)

    banner("PHASE 1: Normal operating conditions")
    for _ in range(3):
        print_cycle(device.run_cycle())
        time.sleep(0.2)

    banner("PHASE 2: Temperature drifting into WARNING band")
    scenario_state["temp_rh_target"] = (9.2, 55.0)
    for _ in range(2):
        print_cycle(device.run_cycle())
        time.sleep(0.2)

    banner("PHASE 3: Temperature exceeds safe threshold -> CRITICAL")
    scenario_state["temp_rh_target"] = (14.0, 60.0)
    for _ in range(2):
        print_cycle(device.run_cycle())
        time.sleep(0.2)

    banner("PHASE 4: Door opened during critical excursion (context event)")
    scenario_state["door_open"] = True
    print_cycle(device.run_cycle())
    scenario_state["door_open"] = False

    banner("PHASE 5: Sensor communication failure (fault injection)")
    device.sensors.inject_fault("temp_humidity", True)
    for _ in range(3):
        print_cycle(device.run_cycle())
        time.sleep(0.2)
    print("  -> device degraded to last-known-good value, then FAULT after retries exhausted")

    banner("PHASE 6: Sensor recovers")
    scenario_state["temp_rh_target"] = (5.0, 50.0)
    device.sensors.inject_fault("temp_humidity", False)
    for _ in range(2):
        print_cycle(device.run_cycle())
        time.sleep(0.2)

    banner("PHASE 7: Low battery voltage")
    scenario_state["battery_v"] = 10.2
    print_cycle(device.run_cycle())
    scenario_state["battery_v"] = 12.6

    banner("PHASE 8: Remote configuration change (tighten warning band)")
    ok = device.apply_config_update({"thresholds": {"temperature_c": {"warning": [-2.0, 8.5]}}})
    print(f"  configuration update applied: {ok}")
    print_cycle(device.run_cycle())

    banner("PHASE 9: Simulated power loss + restart (event log persistence check)")
    del device
    events_before = open(LOG_PATH).read().count("\n")
    device2 = Device(CONFIG_PATH, LOG_PATH, scenario_state)
    events_after = open(LOG_PATH).read().count("\n")
    print(f"  events on disk before restart: {events_before}")
    print(f"  events on disk after restart:  {events_after}  (history preserved + power_restart logged)")
    print_cycle(device2.run_cycle())

    banner("EVENT LOG (most recent 10 entries)")
    for e in device2.logger.tail(10):
        print(f"  {e['type']:<22} {e['payload']}")

    banner(f"DONE. Full event log written to: {LOG_PATH}")


if __name__ == "__main__":
    run_scenario()
