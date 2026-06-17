# Plan: Add Phase Auto-Commit Guidance

## Scope
Update `.omp/commands/create.md`, `.omp/commands/ship.md`, and `.omp/commands/review.md` to require scoped commits at phase completion.

## Blast Radius
- Command instruction markdown only.
- No shell scripts, hooks, or runtime extension changes.

## Steps
1. Read the three command files and identify the final checkpoint/exit sections.
2. Add an auto-commit requirement to each phase:
   - `/create`: PRD/planning artifacts plus `.beads/`.
   - `/ship`: implementation changes plus `.beads/`.
   - `/review`: review report/evidence artifacts plus `.beads/`.
3. Ensure each command calls `br sync --flush-only` before staging `.beads/`.
4. Verify command files contain the new auto-commit sections and scoped staging language.

## Risks
- Over-staging unrelated user changes. Mitigation: require scoped `git add` only for phase-touched files.
- Premature commit before verification/review artifacts exist. Mitigation: place steps at phase completion only.

## Verification
Targeted search for "Auto-Commit" in create/ship/review and for `br sync --flush-only` in each updated section.
