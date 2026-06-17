---
name: ship
description: Implement the active bead only after PRD and plan exist.
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:

1. `.beads/artifacts/$1/plan.md` exists.
2. `.beads/artifacts/$1/tasks.md` exists.
3. `.beads/artifacts/$1/context-capsule.md` exists.

If plan missing: STOP. Tell the user: "Run /plan first — no plan found for $1."
If tasks missing: STOP. Tell the user: "Run /plan first — no tasks found for $1."
If no bead id provided: STOP. Ask: "Which bead? Provide the bead id."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Ship the active bead.

User input: $ARGUMENTS

## Requirements

1. **Confirm the active bead**: `br show $1 --json`.
2. **Claim it**: `br update --actor "$ACTOR" $1 --claim`.
3. **Read the plan and tasks** before editing:
   - `plan.md` for wave structure and verification gates
   - `tasks.md` for task order, dependencies, and per-task verification
   - `context-capsule.md` for constraints and file ownership
4. **Implement per the wave structure.** Complete each wave's verification gate before starting the next. Parallel tasks within a wave can run concurrently.
5. **Keep changes limited to the current bead.** If you discover unrelated work, create a new bead — don't scope-creep.
6. **Update `progress.txt`** as tasks complete. Mark done tasks with `[x]`.
7. **If the plan changes materially**, update `plan.md` and note the change in `progress.txt`.
8. **Run the plan's verification commands** as each wave completes.
9. **End with**: what changed (files + line counts), what remains risky, which verification commands passed/failed, and the next command: `/verify $1`.
