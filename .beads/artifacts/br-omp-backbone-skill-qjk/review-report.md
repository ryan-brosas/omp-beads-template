# Review Report

## Summary
Added scoped auto-commit completion steps to `/create`, `/ship`, and `/review` command workflows.

## Changed Artifacts
- `.omp/commands/create.md` — commits PRD artifacts and bead sync state after create verification.
- `.omp/commands/ship.md` — commits implementation files and bead sync/progress state after ship verification.
- `.omp/commands/review.md` — commits review report and bead sync state after review report generation.

## Risks Checked
- Unrelated staging: each command explicitly says not to stage unrelated user changes.
- br sync ordering: each auto-commit section runs `br sync --flush-only` before staging `.beads/`.
- Scope creep: no auto-push or runtime hooks were added.

## Verdict
Pass. Command guidance satisfies the requested phase auto-commit behavior.
