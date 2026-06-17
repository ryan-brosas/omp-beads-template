# Conventions

## Naming

- Commands: `/brainstorm`, `/create`, `/plan`, `/ship`, `/verify`, `/review`, `/pr`, `/close`, `/init`
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
- Always `br --json`, always `bv --robot-*`.
- Resolve actor: `ACTOR="${BR_ACTOR:-assistant}"` on all br mutations.

## Artifact layout

- `.beads/artifacts/<bead-id>/prd.md`
- `.beads/artifacts/<bead-id>/prd.json`
- `.beads/artifacts/<bead-id>/decisions.md`
- `.beads/artifacts/<bead-id>/plan.md`
- `.beads/artifacts/<bead-id>/tasks.md`
- `.beads/artifacts/<bead-id>/context-capsule.md`
- `.beads/artifacts/<bead-id>/progress.txt`
- `.beads/artifacts/<bead-id>/completion-evidence.json`
- `.beads/artifacts/<bead-id>/review-report.md`

## Slash command authoring

Executable commands (those that perform git/PR operations) use strict constraints:

- `allowed-tools` frontmatter scopes capabilities to the minimum needed (e.g. `Bash(git:*), Bash(gh pr create:*), Read`).
- `!` backtick syntax injects live state into the prompt: `!`git diff --stat``, `!`br show "$BEAD_ID" --json``.
- Single-turn execution: "do all in one message, no text." No conversation — just the tool calls.
- Descriptive commands (those that guide agent behavior) use the multi-phase recipe pattern without `allowed-tools`.

## Security policy layering

Three levels of security rules, concatenated in order:

1. **Built-in** — this skill's 25-pattern sink catalog (always loaded)
2. **Project** — `.omp/security-policy.md` (committed, team-shared, org-specific rules, max 8KB)
3. **Local** — `.omp/security-policy.local.md` (gitignored, personal overrides)

Rules are loaded: built-in → project → local. Later layers override earlier ones for the same rule.

## Memory file maintenance

- `.omp/memory/project/` files are the project's durable context (equivalent to CLAUDE.md).
- After each session that reveals missing context, capture learnings into the right file:
  - `conventions.md` — code style, naming, workflow rules
  - `decisions.md` — architecture decisions with rationale
  - `gotchas.md` — non-obvious quirks discovered during work
  - `tech-stack.md` — runtime, framework, tooling versions
  - `project.md` — purpose, goals, success criteria
- Audit quality periodically: are commands current? Architecture clear? Gotchas captured?
- Before writing, show proposed diff, get approval, then apply.
