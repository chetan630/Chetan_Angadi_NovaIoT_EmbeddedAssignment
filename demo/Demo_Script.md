# Demonstration Video — Script

**1. Working prototype**
- Open a terminal, `cd firmware`, run `python3 main.py`.
- Narrate each phase as it prints: normal → warning → critical → door
  event → sensor fault injection → DEGRADED state → recovery → low
  battery → config update → simulated power loss/restart showing the
  event log survives.
- Run `python3 -m unittest tests.test_core -v` and show all 9 tests
  passing.
- Briefly open `firmware/data/event_log.jsonl` to show the persisted
  event history.

## tips

- If you re-run `python3 main.py`, delete `firmware/data/event_log.jsonl`
  and `firmware/config/device_config.json` first so the "Phase 9 restart"
  section shows a clean before/after event count, or explicitly narrate
  that you're reusing an existing log to show persistence across runs.
