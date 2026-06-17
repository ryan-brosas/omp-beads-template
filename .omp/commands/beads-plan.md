---
name: beads-plan
description: Build a scoped plan for the active bead using bv blast-radius and dependency context.
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:

1. `.beads/artifacts/$1/prd.md` exists.
2. `.beads/artifacts/$1/prd.json` exists.
3. PRD has all sections filled (Problem, Scope, Requirements, Approach, Acceptance Criteria) — no placeholders.
4. PRD has no [ ] checkboxes that would indicate incomplete sections.

If PRD missing: STOP. Tell the user: "Run /create first — no PRD found for $1."
If PRD has placeholders: STOP. Tell the user: "PRD incomplete — run /create to fill all sections."
If no bead id provided: STOP. Ask: "Which bead? Provide the bead id."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Plan the active bead.

User input: $ARGUMENTS

## Requirements

1. **Confirm the active bead**: `br show $1 --json`. Verify status is `open` or `in_progress`.
2. **Run bv for graph context**:
   ```bash
   bv --robot-plan --format json
   bv --robot-insights --format json
   ```
   Use `plan.summary.highest_impact` and `plan.tracks[].unblocks` to structure waves.
3. **Write the plan artifacts** under `.beads/artifacts/$1/`:
   - `plan.md` — use `.omp/templates/plan.md` as the shape. Include:
     - Graph Context (blast radius, unblocks, blocked by, critical path, forecast, hotspots)
     - Observable Truths (falsifiable statements — what "done" looks like)
     - Required Artifacts table
     - Wave Structure table (which waves, what's parallel, preconditions, verification gates)
     - Tasks per wave with code outlines (NOT implementation, just the shape)
     - Full Verification section with exact bash commands
   - `tasks.md` — use `.omp/templates/tasks.md` as the shape. YAML metadata (depends_on, parallel, conflicts_with, files, estimated_minutes), checkboxes per step.
   - `context-capsule.md` — use `.omp/templates/context-capsule.md` as the shape. AI handoff: objective, key patterns, constraints, file ownership.
4. **Include exact files or subsystems expected to change.** No "might also need to touch X."
5. **Include verification steps that prove the intended behavior.** Every observable truth must have a corresponding check.
6. **Do not implement until the plan exists.** This phase produces artifacts only.
7. **End with** the bead id, a one-line summary, wave count, and the next command: `/ship $1`.
