# PRD: Add Phase Auto-Commit Guidance

## Problem
The template currently requires explicit sync and commit discipline, but `/create`, `/ship`, and `/review` do not clearly require a scoped commit at phase completion. This leaves workflow artifacts and implementation changes vulnerable to being left uncommitted between phases.

## Outcome
Update the command workflows so `/create`, `/ship`, and `/review` each finish by creating a scoped git commit for the phase's artifacts or changes.

## Acceptance Criteria
1. `/create` includes an end-of-phase auto-commit step for bead artifacts and `.beads/` sync state.
2. `/ship` includes an end-of-phase auto-commit step for implementation changes and `.beads/` sync state.
3. `/review` includes an end-of-phase auto-commit step for review artifacts and `.beads/` sync state.
4. Each step runs `br sync --flush-only` before staging `.beads/`.
5. Guidance preserves scoped commits: stage only files changed by that phase.

## Non-Goals
- Do not auto-push from these phase commands.
- Do not change `/pr` or `/close` behavior.
- Do not add scripts or runtime automation outside command instructions.
