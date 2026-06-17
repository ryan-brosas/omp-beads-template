---
name: br
description: Use br as the source of truth for bead state, ownership, and artifact location.
---

# br

## When to use

- You need to inspect, create, claim, update, or close a bead.
- You need the canonical bead id before writing workflow artifacts.
- You need to understand current status before implementation or review.

## When not to use

- You only need code intelligence inside the repository. Use OMP tools first.
- You are guessing bead state from filenames or memory. Inspect br instead.

## Process

1. Inspect before mutation.
   - Prefer `br show <id> --json` for a single bead.
   - Prefer `br list --status open --status in_progress --json` to find active work.
2. Mutate state explicitly.
   - Claim: `br update <id> --claim`
   - Status or metadata updates: `br update ...`
   - Close only after evidence exists.
3. Write artifacts under `.beads/artifacts/<bead-id>/`.
4. Keep one active bead in focus unless the user asks for triage across many beads.
5. After a meaningful state change, sync if your br setup requires it.

## Minimum checks

- Confirm the bead id.
- Confirm current status.
- Confirm the artifact directory matches the bead id.
- Confirm `prd.md` exists before planning.
- Confirm `plan.md` exists before implementation.
