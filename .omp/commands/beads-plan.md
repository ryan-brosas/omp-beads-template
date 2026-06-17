---
name: beads-plan
description: Build a scoped plan for the active bead using bv blast-radius and dependency context.
---

Plan the active bead.

User input: $ARGUMENTS

Requirements:
- Confirm the active bead and verify `prd.md` exists.
- Use bv to inspect blast radius, dependencies, hotspots, or blockers.
- Write `.beads/artifacts/<bead-id>/plan.md` using `.omp/templates/plan.md` as the shape.
- Include exact files or subsystems expected to change.
- Include verification steps that prove the intended behavior.
- Do not implement until the plan exists.
