# OMP beads template

This repository uses br and bv as the backbone of planning, execution, verification, and review.

@memory/project/project.md
@memory/project/conventions.md
@memory/project/tech-stack.md
@memory/project/decisions.md
@memory/project/gotchas.md

## Workflow Enforcement

The workflow-gate extension (`.omp/extensions/workflow-gate.ts`) enforces the workflow. It blocks `edit`/`write` tools until required artifacts exist.

**You MUST follow the workflow:**
1. `/create` → `/plan` → `/ship` → `/verify` → `/review` → `/pr` → (human merges) → `/close`
2. `/brainstorm` when you need new ideas — it's the entry point, not a required phase
3. Each command checks its prerequisites. If it says "run X first," do it.
4. The human always gets the last call — agent proposes, human decides

**What gets blocked:**
| Tool | Condition | Error |
|------|-----------|-------|
| edit | No PRD for active bead | "Run /create first" |
| edit | No plan for active bead | "Run /plan first" |
| write | Same as edit | Same |

**What always passes:**
- Reading files (read tool, read-only bash)
- Writing to `.beads/` and `.omp/` (workflow files)
- Running `br`, `bv`, `git status`, `git diff`

**Bypass:** `OMP_SKIP_BEADS_WORKFLOW=1` (emergencies only).

## Preferred workflow

Use the slash commands directly — no `beads-` prefix needed in OMP:

- `/brainstorm` — generate ideas (entry point, run when you need new work)
- `/create` → `/plan` → `/ship` → `/verify` → `/review` → `/pr` — core loop
- (human merges) → `/close` — human gets the last call

(A `/init` command bootstraps the workspace.)

## Process rules

- br owns task state.
- bv informs every phase before action.
- Do not edit implementation files until the active bead has both `prd.md` and `plan.md`.
- Write artifacts under `.beads/artifacts/<bead-id>/`.
- Keep one bead active per session unless the user explicitly asks for portfolio triage.
- Claims need evidence: commands run, files changed, acceptance criteria checked.
- Use OMP built-ins for execution: `task` for subagents, `todo` for tracking, `read/search/find/lsp` for discovery.

## Workflow expectations by phase

1. **Brainstorm**: understand repo state and candidate work with bv; no implementation edits.
2. **Create**: create or select a bead, then write `prd.md`, `prd.json`, `decisions.md`.
3. **Plan**: write `plan.md`, `tasks.md`, `context-capsule.md` with blast radius, risks, and verification.
4. **Ship**: implement only the active bead per the plan's wave structure.
5. **Verify**: run targeted checks and record results in `completion-evidence.json`.
6. **Review**: inspect the diff and risks, then write `review-report.md`.
7. **PR/Close**: summarize change, suggested follow-ups, and only close once evidence exists.

## Escape hatch

Set `OMP_SKIP_BEADS_WORKFLOW=1` only for emergencies or template bootstrap work.
