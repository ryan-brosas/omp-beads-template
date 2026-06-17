---
name: beads-create
description: Turn a selected request into a bead plus a concrete PRD artifact.
---

## Prerequisites (CHECK FIRST)

Before doing ANYTHING, verify:

1. User provided input ($ARGUMENTS) describing what to build.
2. You have run `/brainstorm` or the user has explicitly chosen a work item.

If no input: STOP. Ask the user: "What are we building? Provide a short description or run /brainstorm first."
If the idea is still fuzzy: STOP. Tell the user: "Run /brainstorm first to narrow the scope."
Do NOT proceed. Do NOT "helpfully" skip ahead.

Create or select a bead for this work, then write its PRD.

User input: $ARGUMENTS

## Requirements

1. **Inspect existing beads first** to avoid duplicates.
   - `br list --status open --status in_progress --json`
   - `br search "$ARGUMENTS" --json`
2. **Create a new bead** only when no suitable bead exists:
   ```bash
   ACTOR="${BR_ACTOR:-assistant}"
   br create --actor "$ACTOR" "$ARGUMENTS" -p 2 -t feature --json
   ```
   Adjust `-p` (0-4) and `-t` (task|bug|feature|epic|question|docs) based on scope.
3. **Identify the target bead id explicitly.** If reusing an existing bead, state it.
4. **Write the PRD artifacts** under `.beads/artifacts/<bead-id>/`:
   - `prd.md` — use `.omp/templates/prd.md` as the shape. Fill every section. No placeholders.
   - `prd.json` — use `.omp/templates/prd.json` as the shape. Machine-readable requirements + success criteria.
   - `decisions.md` — use `.omp/templates/decisions.md` as the shape. Decision log, rejected alternatives, assumptions.
5. **Do not implement code yet.** This phase produces artifacts only.
6. **End with the bead id**, a one-line summary, and the next command: `/plan <bead-id>`.
