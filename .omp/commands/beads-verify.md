---
name: beads-verify
description: Run targeted verification for the active bead and record the evidence.
---

Verify the active bead.

User input: $ARGUMENTS

Requirements:
- Read the bead plan first.
- Run the smallest set of checks that proves the changed behavior.
- Record commands and results in `.beads/artifacts/<bead-id>/completion-evidence.json` using `.omp/templates/completion-evidence.json` as the shape.
- Separate passed checks, failed checks, and unchecked risks.
- Do not claim completion without evidence.
