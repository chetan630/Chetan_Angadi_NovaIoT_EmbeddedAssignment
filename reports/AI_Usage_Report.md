# AI Usage Report

**Assignment:** NovaIoT FleetGuard Embedded Systems Assignment
**Candidate:** Chetan Angadi

Per the assignment's AI Usage Policy, this report documents how AI tools
were used to complete this submission, honestly and specifically.

## Tool Used

**ChatGpt**, **Claude**, **Gemini**, **Replit**.

## Purpose

* AI tools were used to support research and comparison of sensor and module options by providing specifications, performance trade-offs, and design considerations. These outputs were evaluated and used to support final hardware selection decisions.
* AI tools were used during system design exploration to generate and compare alternative architecture approaches. The final system architecture was selected based on engineering judgment and project requirements.
* AI tools were used as an engineering assistant to accelerate development of remaining deliverables, while all outputs were reviewed, corrected where necessary, and validated before inclusion in the final submission.
* AI assistance was used in developing the firmware proof-of-concept by suggesting implementation structures and logic flow, which were then adapted and implemented based on design requirements.
* AI assistance was used in creating firmware architecture documentation by helping organize system components and data flow, which were refined to match the actual system design.
* AI assistance was used to generate initial diagram source files for architecture diagrams, which were then manually reviewed, corrected, and aligned with the final design.
* AI tools were used to improve clarity, consistency, and readability of technical documentation across the project, while ensuring technical accuracy was preserved.
* AI tools were used to help identify potential edge cases, risks, and limitations, which were then critically evaluated and incorporated into the final engineering analysis where appropriate.

## How It Was Used — Workflow

1. The candidate provided the assignment brief (PDF) and the current
   state of the GitHub repository, and asked Claude to analyze what was
   already done against the brief before doing anything else.
2. Claude inventoried the repository, identified which required
   deliverables existed, which were empty placeholder files (e.g.
   `Firmware_Architecture.md` and the three `.drawio` files were 0 bytes),
   and which were entirely missing (no `firmware/`, `reports/`, or
   `demo/` directories existed).
3. Rather than assume scope, Claude asked the candidate three direct
   questions before writing anything: (a) whether the working prototype
   should be Option A (physical hardware) or Option B (simulation), (b)
   what to prioritize in this session, and (c) how to fill the empty
   diagram files. The candidate chose Option B (software simulation),
   asked for everything to be completed in order, and asked for both
   Mermaid-in-Markdown and draw.io XML diagram sources.
4. Claude then built the firmware simulation (config manager, sensor
   manager with fault injection, decision engine, event logger, alert
   manager, state machine, orchestrator, a 9-phase scripted demo, and a
   9-test unit test suite), ran it, and used the failing config-merge
   test case it surfaced to fix a real bug (a shallow dict merge that
   silently dropped a sibling threshold field during a nested
   configuration update) before treating the module as done.
5. Claude generated the diagram sources (System Architecture, Hardware
   Block Diagram, Data Flow) as both draw.io XML (via a small helper
   script, validated as well-formed XML) and Mermaid diagrams embedded
   directly in the relevant Markdown docs.
6. Claude wrote `docs/Firmware_Architecture.md`, rewrote `README.md` to
   include the required project overview / setup / build / assumptions /
   limitations sections, and generated the Engineering Decision Report as
   a PDF using `reportlab` (verified at 5 pages, within the 10-page
   limit) and this AI Usage Report as Markdown.

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
