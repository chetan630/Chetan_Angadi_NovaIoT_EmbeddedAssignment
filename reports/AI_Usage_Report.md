# AI Usage Report

**Assignment:** NovaIoT FleetGuard Embedded Systems Assignment
**Candidate:** Chetan Angadi

Per the assignment's AI Usage Policy, this report documents how AI tools
were used to complete this submission, honestly and specifically.

## Tool Used

**ChatGpt**, **Claude**, **Gemini**, **Replit**,**Google AI**.

## Purpose

* AI tools were used to support research and comparison of sensor and module options by providing specifications, performance trade-offs, and design considerations. These outputs were evaluated and used to support final hardware selection decisions.
* AI tools were used during system design exploration to generate and compare alternative architecture approaches. The final system architecture was selected based on engineering judgment and project requirements.
* AI tools were used as an engineering assistant to accelerate development of remaining deliverables, while all outputs were reviewed, corrected where necessary, and validated before inclusion in the final submission.
* AI assistance was used in developing the firmware proof-of-concept by suggesting implementation structures and logic flow, which were then adapted and implemented based on design requirements.
* AI assistance was used in creating firmware architecture documentation by helping organize system components and data flow, which were refined to match the actual system design.
* AI assistance was used to generate initial diagram source files for architecture diagrams, which were then manually reviewed, corrected, and aligned with the final design.
* AI tools were used to improve clarity, consistency, and readability of technical documentation across the project, while ensuring technical accuracy was preserved.
* AI tools were used to help identify potential edge cases, risks, and limitations, which were then critically evaluated and incorporated into the final engineering analysis where appropriate.

## Generated Outputs Used

- All firmware simulation source code (`firmware/src/*.py`,
  `firmware/main.py`, `firmware/tests/test_core.py`) — used as-is after
  being run and verified (9/9 unit tests passing, full 9-phase demo
  scenario producing expected state transitions and log entries).
- All three `.drawio` diagram files and their Mermaid equivalents
  embedded in `docs/System_Architecture.md`, `docs/Hardware_Design.md`,
  and `docs/Firmware_Architecture.md` — used as-is, validated as
  well-formed XML.
- `docs/Firmware_Architecture.md`, the rewritten `README.md`, and the
  Engineering Decision Report PDF — used as drafted, since they
  synthesize decisions already made and documented elsewhere in the
  repository (hardware/architecture docs) rather than inventing new
  engineering claims.

## Generated Outputs Rejected / Corrected

- The first version of `ConfigManager.update()` used a one-level-deep
  dictionary merge. When exercised by the demo scenario (a nested
  threshold update) and by a unit test written specifically to check
  this behaviour, it silently dropped a sibling field it wasn't supposed
  to touch. This was caught by actually running the code rather than
  trusting it, and was rewritten as a recursive deep merge before being
  accepted.
- No other generated code or content was rejected outright, but all
  generated engineering content (hardware rationale, trade-off framing,
  risk list) was scoped deliberately to summarize and extend decisions
  already present in the pre-existing `docs/Hardware_Design.md` and
  `docs/System_Architecture.md` rather than introduce new, unreviewed
  hardware or architecture claims.

## Independent Engineering Decisions (Candidate's Own Judgment)

- The original hardware selection, hardware design rationale, system
  architecture layering, BOM, and pin mapping (present in the repository
  before this session) were the candidate's own prior work and were not
  regenerated.
- The choice of **Option B (software simulation)** for Task 4, over
  Option A (physical hardware), was made explicitly by the candidate when
  asked, based on hardware availability and time constraints — not
  assumed by the AI.
- The decision to request **both** Mermaid and draw.io diagram formats,
  and to prioritize completing every remaining task in a single session,
  were explicit candidate choices made when Claude asked rather than
  assumed them.
- Final review and acceptance of all AI-generated content — including
  verifying the firmware actually runs, the tests actually pass, and the
  report stays within the page limit — remains the candidate's
  responsibility and was performed as part of this workflow.
