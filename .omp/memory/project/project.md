# Project

Purpose: OMP-native project template centered on br for task state and bv for graph-informed planning.

## Goals

- Keep the workflow boring, explicit, and inspectable.
- Make beads the source of truth for active work.
- Make bv the first stop for triage, impact, and review.
- Prefer OMP built-ins over custom glue when they already solve the problem.

## Success criteria

- `.omp/` contains the workflow backbone.
- The beads phases exist as namespaced slash commands.
- br and bv usage is documented as skills.
- Workflow artifacts have stable templates under `.omp/templates`.
- Write protection blocks edits before PRD and plan exist for the active bead.
