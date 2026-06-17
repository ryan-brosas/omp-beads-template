# OMP beads template

This repository uses br and bv as the backbone of planning, execution, verification, and review.

@memory/project/project.md
@memory/project/conventions.md
@memory/project/tech-stack.md
@memory/project/decisions.md
@memory/project/gotchas.md

## Preferred workflow

Use the namespaced slash commands to avoid collisions with OMP built-ins:

- `/beads-init`
- `/beads-brainstorm`
- `/beads-create`
- `/beads-plan`
- `/beads-ship`
- `/beads-verify`
- `/beads-review`
- `/beads-pr`
- `/beads-close`

## Process rules

- br owns task state.
- bv informs every phase before action.
- Do not edit implementation files until the active bead has both `prd.md` and `plan.md`.
- Write artifacts under `.beads/artifacts/<bead-id>/`.
- Keep one bead active per session unless the user explicitly asks for portfolio triage.
- Claims need evidence: commands run, files changed, acceptance criteria checked.
- Use OMP built-ins for execution: `task` for subagents, `todo` for tracking, `read/search/find/lsp` for discovery.

## Workflow expectations by phase

1. Brainstorm: understand repo state and candidate work with bv; no implementation edits.
2. Create: create or select a bead, then write `prd.md`.
3. Plan: write `plan.md` with blast radius, risks, and verification.
4. Ship: implement only the active bead.
5. Verify: run targeted checks and record results in `completion-evidence.json`.
6. Review: inspect the diff and risks, then write `review-report.md`.
7. PR/Close: summarize change, suggested follow-ups, and only close once evidence exists.

## Escape hatch

Set `OMP_SKIP_BEADS_WORKFLOW=1` only for emergencies or template bootstrap work.
