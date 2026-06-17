---
name: beads-init
description: Initialize or inspect the beads workflow backbone for this repository.
---

Initialize the repository for the beads workflow.

User input: $ARGUMENTS

Steps:
1. Inspect whether `.beads/` already exists.
2. If br is not initialized, initialize it with a sensible prefix derived from the repo name or the user's argument.
3. Confirm `.omp/` backbone files exist; create missing workflow directories or files if asked.
4. Do not edit product code.
5. End with the exact initialized state and the next recommended workflow command.
