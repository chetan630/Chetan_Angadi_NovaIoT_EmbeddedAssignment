# NovaIoT FleetGuard — Cold-Chain Container Monitoring Device

**Candidate:** Chetan Angadi
**Assignment:** NovaIoT Embedded Systems Assignment (FleetGuard)

## 1. Project Overview

FleetGuard needs a compact IoT edge device that can be installed inside
refrigerated transport containers to continuously monitor environmental
conditions, alert locally on abnormal conditions, retain a local event
history, and be architecturally ready for future cloud connectivity —
deployable across a fleet that scales from 10 to 10,000+ units.

This repository contains the engineering-grade solution design and a
working proof-of-concept requested by the assignment brief: it is **not**
a fully functioning physical prototype.

**What's implemented:**

- A production-oriented **hardware architecture** built around the
  ESP32-S3-WROOM-1, an SHT41 temperature/humidity sensor, and a set of
  optional sensors (door status, battery voltage, ambient light,
  vibration) — see [`docs/Hardware_Design.md`](docs/Hardware_Design.md).
- A modular **firmware architecture** covering data acquisition,
  condition classification, event logging, alerting, configuration
  management, and reliability behaviour — see
  [`docs/Firmware_Architecture.md`](docs/Firmware_Architecture.md).
- A **software-simulated proof-of-concept** (Task 4, Option B) that runs
  the full pipeline — sensor acquisition, classification, event
  generation, alerting, fault injection, config updates, and a power-loss
  restart test — without requiring physical hardware. See
  [`firmware/README.md`](firmware/README.md).
- Supporting **diagrams**, an **Engineering Decision Report**, and an
  **AI Usage Report** (see Project Structure below).

## 2. Hardware Platform

The prototype architecture is built around the **ESP32-S3-WROOM-1**
microcontroller.

Reasons for selection:

- Dual-core architecture
- Built-in Wi-Fi/BLE
- FreeRTOS support
- Low-cost production platform
- Suitable for future cloud connectivity

### Selected Hardware

- ESP32-S3-WROOM-1
- Sensirion SHT41-AD1B Temperature & Humidity Sensor
- (Optional sensors: BH1750 ambient light, LIS3DH vibration, reed switch
  door status, battery voltage divider — see
  [`docs/Hardware_Design.md`](docs/Hardware_Design.md) for full
  justification of every component)

**Design Philosophy**

This project is presented as a production-oriented architecture for a
cold-chain monitoring system. The proof-of-concept firmware runs as a
software simulation (see Section 4 below), while certain hardware
selections (e.g., industrial-grade storage and sensors) represent the
intended production design rather than the minimum prototype.

## 3. Setup Instructions

### Prerequisites

- Python 3.8 or later (standard library only — no external packages
  required for the firmware simulation)
- Git (to clone the repository)
- A `.drawio`-compatible viewer ([app.diagrams.net](https://app.diagrams.net))
  if you want to open the diagram source files, or a Markdown viewer that
  renders Mermaid (GitHub does this natively) to view the embedded
  diagrams in `docs/`.

### Clone / extract

```bash
git clone <repository-url>
cd Chetan_Angadi_NovaIoT_EmbeddedAssignment
# or, if working from the ZIP archive: unzip and cd into the folder
```

No build step, package installation, or toolchain is required to run the
proof-of-concept — it uses only the Python standard library.

## 4. Build / Run Instructions

The prototype is a **software simulation** (Task 4, Option B), so there is
no firmware image to flash. Run the scripted demo directly:

```bash
cd firmware
python3 main.py
```

Run the unit tests:

```bash
cd firmware
python3 -m unittest tests.test_core -v
```

See [`firmware/README.md`](firmware/README.md) for a full description of
what the demo scenario exercises and how to read the generated event log.

## 5. Assumptions

- **Target cargo type**: chilled goods with a nominal safe range of
  2-8°C and 30-70% RH (not deep-frozen -18°C cargo); thresholds are
  configurable, so this is a starting default rather than a hard
  constraint.
- **Deployment environment**: 12V/24V vehicle electrical systems (trucks,
  refrigerated vans), not mains-powered.
- **Connectivity**: the device operates fully offline at the edge;
  cloud/MQTT connectivity is architected for but intentionally not
  implemented, per the assignment ("Cloud implementation is not
  mandatory. Architectural readiness is expected").
  Non-goal for this submission — see the AI Usage Report and Engineering
  Report for reasoning.
- **Single-tenant device identity**: each device is assumed to have a
  unique identity for future fleet management, but device provisioning
  and authentication are out of scope for this MVP.
- **Option B (simulation) satisfies Task 4** as explicitly permitted by
  the assignment brief, given no physical ESP32-S3 hardware was available
  in this environment.

## 6. Limitations

- The firmware prototype is a **Python simulation**, not compiled
  ESP-IDF/Arduino C/C++ firmware. Module boundaries and logic map 1:1 to
  the intended production firmware (see
  [`docs/Firmware_Architecture.md`](docs/Firmware_Architecture.md)), but
  timing, memory footprint, and real I2C/SPI/GPIO behaviour are not
  validated on physical hardware.
- No physical hardware validation (no board bring-up, no schematic
  capture, no PCB layout) — architecture and BOM are documented, not
  fabricated.
- Cloud connectivity, OTA firmware updates, and remote fleet management
  are architected for but not implemented.
- Security (firmware signing, secure boot, TLS to cloud) is discussed at
  the design level in the Engineering Report but not implemented in the
  simulation.
- The event logger uses a local JSON-lines file with fsync-based
  durability, which models the intended SPI-flash/MicroSD hybrid storage
  behaviour but is not the actual flash/SD driver code.
- Sensor simulation uses plausible synthetic values and injected faults;
  it does not model every real-world SHT41/BH1750/LIS3DH failure mode.

## 7. Project Structure

```
Chetan_Angadi_NovaIoT_EmbeddedAssignment/
├── README.md                      # this file
├── docs/
│   ├── System_Architecture.md      # Task 1
│   ├── Hardware_Design.md          # Task 2
│   └── Firmware_Architecture.md    # Task 3
├── diagrams/
│   ├── System_Architecture.drawio
│   ├── Hardware_Block_Diagram.drawio
│   └── Data_Flow.drawio
├── firmware/                       # Task 4 (Option B: software simulation)
│   ├── main.py
│   ├── src/
│   ├── config/
│   ├── data/
│   ├── tests/
│   └── README.md
├── hardware/
│   ├── BOM.md
│   ├── Pin_Mapping.md
│   └── Hardware_Block_Diagram.png
├── reports/
│   ├── Chetan_Angadi_EngineeringReport.pdf   # Task 5
│   └── AI_Usage_Report.md                    # Task 6
├── demo/
│   └── Demo_Script.md              # talking points / shot list for the recorded video
└── assets/
```

## 8. Documentation Index

| Task | Document |
|---|---|
| Task 1 — System Architecture | [`docs/System_Architecture.md`](docs/System_Architecture.md) |
| Task 2 — Hardware Design | [`docs/Hardware_Design.md`](docs/Hardware_Design.md), [`hardware/BOM.md`](hardware/BOM.md), [`hardware/Pin_Mapping.md`](hardware/Pin_Mapping.md) |
| Task 3 — Firmware Design | [`docs/Firmware_Architecture.md`](docs/Firmware_Architecture.md) |
| Task 4 — Working Prototype | [`firmware/`](firmware/) (run instructions in [`firmware/README.md`](firmware/README.md)) |
| Task 5 — Engineering Decision Report | [`reports/Chetan_Angadi_EngineeringReport.pdf`](reports/) |
| Task 6 — AI Usage Report | [`reports/AI_Usage_Report.md`](reports/AI_Usage_Report.md) |
| Demonstration Video | [`demo/Demo_Script.md`](demo/Demo_Script.md) (script for the video — recording/upload is the candidate's own step) |
