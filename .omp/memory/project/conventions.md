# Conventions

## Naming

- Commands: `beads-*`
- Skills: short noun names such as `br` and `bv`
- Artifact files: `kebab-case`
- Bead slugs: `kebab-case`

## Workflow

1. Triage with bv before mutating state.
2. Inspect bead state before changing it.
3. Create `prd.md` before `plan.md`.
4. Create `plan.md` before implementation edits.
5. Verify with targeted checks before review or close.
6. Record evidence in the bead artifact directory.

## Agent behavior

- Evidence before claims.
- Read before edit.
- Scope changes to the active bead.
- Prefer OMP built-ins: `task`, `todo`, `read`, `search`, `find`, `lsp`.
- Use subagents for bounded review or reconnaissance, not for blind delegation.

## Artifact layout

- `.beads/artifacts/<bead-id>/prd.md`
- `.beads/artifacts/<bead-id>/plan.md`
- `.beads/artifacts/<bead-id>/completion-evidence.json`
- `.beads/artifacts/<bead-id>/review-report.md`
