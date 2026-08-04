# Demonstration Video — Script / Shot List

**Required:** 5-10 minute video, filename `Chetan_Angadi_Demo.mp4`, covering:
solution overview, design decisions, working prototype, challenges
encountered. This file is a script to record from — **recording and
uploading the video is a step only you can do**; Claude cannot produce
video/audio.

## Suggested structure (~8 minutes)

**1. Solution overview (~1.5 min)**
- State the problem: FleetGuard needs visibility into refrigerated
  container conditions; today there's no local monitoring, no historical
  data, no alerting.
- State the solution in one sentence: an ESP32-S3-based edge device that
  monitors temperature/humidity (+ optional door/battery/light/vibration),
  classifies conditions locally, alerts locally, and logs history — with
  architecture ready for future cloud connectivity.
- Show the repo structure (`README.md` project structure section) as a
  map of what you'll walk through.

**2. Design decisions (~3 min)**
- Screen-share `docs/Hardware_Design.md` and the Mermaid block diagram at
  the top — explain why ESP32-S3 + SHT41 (dual-core/Wi-Fi readiness,
  factory-calibrated accuracy).
- Screen-share `docs/System_Architecture.md` — walk through the 6 layers
  and why they're separated.
- Screen-share `docs/Firmware_Architecture.md` — explain the
  worst-case-wins classification strategy and the device state machine
  (BOOT/RUNNING/DEGRADED/FAULT/CONFIG), and why device state is kept
  separate from environmental condition.
- Mention the reliability strategy: retry/backoff, last-known-good
  fallback, crash-safe event logging (fsync).

**3. Working prototype (~3 min)**
- Open a terminal, `cd firmware`, run `python3 main.py`.
- Narrate each phase as it prints: normal → warning → critical → door
  event → sensor fault injection → DEGRADED state → recovery → low
  battery → config update → simulated power loss/restart showing the
  event log survives.
- Run `python3 -m unittest tests.test_core -v` and show all 9 tests
  passing.
- Briefly open `firmware/data/event_log.jsonl` to show the persisted
  event history.

**4. Challenges encountered (~1 min)**
- Be honest here — good options to mention:
  - No physical ESP32-S3 hardware was available in time, so Task 4 was
    completed as Option B (software simulation) with module boundaries
    designed to map directly onto real ESP-IDF drivers later.
  - Designing a threshold strategy that avoids alert chattering at a
    boundary (why the two-band Normal/Warning/Critical model was chosen
    over a single cutoff).
  - Balancing storage endurance vs. capacity for the local event log
    (why SPI flash + MicroSD hybrid, not just one).
  - (If true for you) Deciding how much of the production security model
    (secure boot, device identity) to design for vs. implement given the
    assignment's time window — see the Engineering Report's Risks &
    Limitations section.

**5. Close (~0.5 min)**
- Point to the Engineering Decision Report and AI Usage Report for full
  written detail on trade-offs and AI-assisted workflow.

## Recording tips

- Record your terminal output at a large enough font size to read on
  camera/screen-share.
- If you re-run `python3 main.py`, delete `firmware/data/event_log.jsonl`
  and `firmware/config/device_config.json` first so the "Phase 9 restart"
  section shows a clean before/after event count, or explicitly narrate
  that you're reusing an existing log to show persistence across runs.
