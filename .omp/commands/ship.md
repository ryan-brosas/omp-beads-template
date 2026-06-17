---
description: "Implement. Graph-informed — checks file history, impact, and related work before coding."
argument-hint: "<bead-id>"
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:
1. `.beads/artifacts/$ARGUMENTS/plan.md` exists
2. `.beads/artifacts/$ARGUMENTS/tasks.md` exists
3. `.beads/artifacts/$ARGUMENTS/context-capsule.md` exists

If plan missing: STOP. Tell the user: "Run /plan first — no plan found for $ARGUMENTS."
If tasks missing: STOP. Tell the user: "Run /plan first — no tasks found for $ARGUMENTS."
Do NOT proceed. Do NOT "helpfully" skip ahead.

You are implementing bead $ARGUMENTS. Check the graph before coding.

## Phase 1: Graph Check

```bash
bv --robot-triage --format json              # Have priorities shifted?
bv --robot-alerts --format json              # Any new blockers or stale issues?
br show "$ARGUMENTS" --json                    # Bead details
br dep tree "$ARGUMENTS" --json                # Dependencies
```

If priorities shifted or new blockers appeared, report before proceeding.

## Phase 2: File Context

Before editing any file, check its history:

```bash
bv --robot-file-beads <file> --format json   # What tasks touched this file?
bv --robot-file-relations <file> --format json # What files co-change with this?
```

**Token efficiency:** For tasks touching >5 files, check only the 3 most critical files (by blast radius) plus any hotspots (`bv --robot-file-hotspots`). Use `--format toon` for large result sets.

This prevents:
- Reverting someone else's work
- Missing files that should co-change
- Breaking changes that depend on patterns in the file

## Phase 3: Claim

```bash
ACTOR="${BR_ACTOR:-assistant}"
br update --actor "$ACTOR" "$ARGUMENTS" --status in_progress --claim --json
```

## Phase 4: Implement

Follow the plan in `.beads/artifacts/$ARGUMENTS/plan.md`.

For each task:
1. Read context capsule (`.beads/artifacts/$ARGUMENTS/context-capsule.md`)
2. Check file history (Phase 2)
3. Implement the change
4. Update `.beads/artifacts/$ARGUMENTS/progress.txt` — mark task done
5. Run the wave's verification gate before starting next wave

## Phase 5: Verify

```bash
br lint "$ARGUMENTS" --json                    # Lint changed files
br dep cycles --json                         # Must still be empty
```

Run project-specific verification (tests, build, typecheck) before proceeding.

## Phase 6: Report

```
Bead: $ARGUMENTS | Status: IMPLEMENTED
Files changed: <N> (<+additions> <-deletions>)
Verification gates passed: <N>/<N>
Next: /verify $ARGUMENTS
```

## Guardrails

- Always check file history before editing (robot-file-beads)
- Always check co-changing files (robot-file-relations)
- If graph check reveals priority shift, ask before proceeding
- Keep edits scoped to the bead
- For discovered work >2 min, ask before creating a bead
