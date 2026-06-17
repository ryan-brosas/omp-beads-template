---
name: beads-create
description: Turn a selected request into a bead plus a concrete PRD artifact.
---

Create or select a bead for this work, then write its PRD.

User input: $ARGUMENTS

Requirements:
- Inspect existing beads first to avoid duplicates.
- Create a new bead only when no suitable bead exists.
- Identify the target bead id explicitly.
- Write `.beads/artifacts/<bead-id>/prd.md` using `.omp/templates/prd.md` as the shape.
- Capture problem, outcome, acceptance criteria, constraints, and risks.
- Do not implement code yet.
