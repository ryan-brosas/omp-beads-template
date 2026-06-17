---
name: init
description: Initialize or inspect the beads workflow backbone for this repository.
---

## Prerequisites (CHECK FIRST)

None. This command bootstraps the workflow itself.

Initialize the repository for the beads workflow.

User input: $ARGUMENTS

## Steps

1. **Check if `.beads/` already exists.** If `br where` succeeds, the workspace is initialized — report current state and skip to step 5.
2. **Initialize br**: `br init`. Uses a sensible prefix derived from the repo name or `$ARGUMENTS`.
3. **Confirm `.omp/` backbone exists.** Check that `.omp/commands/`, `.omp/skills/`, `.omp/templates/`, `.omp/agents/`, `.omp/extensions/` directories are present.
4. **Seed missing template files.** If any of these are missing, copy from `.omp/templates/`:
   - `.beads/artifacts/` (directory with `.gitkeep`)
5. **Do not edit product code.**
6. **End with the exact initialized state** and the next recommended workflow command (`/brainstorm`).

## Output

Report: workspace path, br version, bead prefix, existing bead count (open/closed), and recommended next command.
