---
description: "Wave-sequence into implementation plan. Graph-informed — uses bv for tracks, impact, forecasting, and capacity."
argument-hint: "<bead-id>"
---

Before doing ANYTHING, verify:
1. `.beads/artifacts/$ARGUMENTS/prd.md` exists
2. `.beads/artifacts/$ARGUMENTS/prd.json` exists
3. PRD has all sections filled (Problem, Scope, Requirements, Approach, Success Criteria) — no placeholders

If PRD missing: STOP. Tell the user: "Run /create first — no PRD found for $ARGUMENTS."
If PRD has placeholders: STOP. Tell the user: "PRD incomplete — run /create to fill all sections."
Do NOT proceed. Do NOT "helpfully" skip ahead.

You are planning implementation for bead $ARGUMENTS. Use the graph to inform sequencing.

## Phase 1: Graph Context

```bash
bv --robot-plan --format json                # Execution tracks — parallel-safe waves
bv --robot-insights --format json            # Graph metrics — PageRank, critical path
bv --robot-file-hotspots --format json       # Riskiest files — touch with care
bv --robot-forecast "$ARGUMENTS" --format json # ETA prediction
br show "$ARGUMENTS" --json                    # Bead details
br dep tree "$ARGUMENTS" --json                # Full dependency tree
```

From the graph:
- What tracks exist — group work into parallel waves
- What's the blast radius — which files will change
- What's the ETA — is this realistic for one session?
- What files are hotspots — touch with extra care

## Phase 2: Decompose

Break the work into tasks. For each task:
- What it does (1-2 sentences)
- Files it touches (check `bv --robot-file-hotspots` for hot files)
- Dependencies (what must finish first)
- Can it run in parallel? (check `bv --robot-plan` tracks)
- Estimated minutes

## Phase 3: Wave-Sequence

Organize tasks into waves:

```
Wave 1 (parallel): tasks with no dependencies
Wave 2 (parallel): tasks that depend only on Wave 1
Wave N: tasks that depend on Wave N-1
```

Within a wave, tasks that touch different files can run in parallel.

## Phase 4: Write Artifacts

**plan.md** — Use `.omp/templates/plan.md` as the shape:
- Graph Context: blast radius (N files, M new/O edits/P deletes), unblocks, blocked by, critical path, forecast, hotspots
- Observable Truths: falsifiable statements — what "done" looks like
- Required Artifacts table: what files, what they provide, path, status
- Wave Structure table: wave #, tasks, parallel?, preconditions, verification gate
- Tasks per wave with code outlines (NOT implementation, just the shape)
- Full Verification section with exact bash commands

**tasks.md** — Use `.omp/templates/tasks.md` as the shape:
- YAML metadata per task: depends_on, parallel, conflicts_with, files, estimated_minutes
- Concrete checkboxes per task step
- Verification check per task

**context-capsule.md** — Use `.omp/templates/context-capsule.md` as the shape:
- Objective (one paragraph)
- Key patterns with file references
- Constraints (MUST/SHOULD lists)
- File ownership table
- Graph context summary

## Phase 5: Verify

```bash
br lint "$ARGUMENTS" --json
bv --robot-suggest --format json
br dep cycles --json                         # Must be empty
ls .beads/artifacts/"$ARGUMENTS"/plan.md .beads/artifacts/"$ARGUMENTS"/tasks.md .beads/artifacts/"$ARGUMENTS"/context-capsule.md
br sync --flush-only
```

## Phase 6: Report

```
Plan: $ARGUMENTS
Waves: <N> | Tasks: <N> total, <N> parallel
Blast radius: <N files> (<M new, O edits, P deletes)
Forecast: <N minutes>
Verification gates: <N>
Next: /ship $ARGUMENTS
```
