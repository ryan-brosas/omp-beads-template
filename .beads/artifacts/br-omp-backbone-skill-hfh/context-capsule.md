# Context Capsule: br-omp-backbone-skill-hfh

## Objective

Add a foundational OMP skill (`.omp/skills/backbone/SKILL.md`) that serves as the entry-point reference card explaining how br and bv together form the beads workflow backbone.

## Key facts

- **Repo**: omp-template — an OMP-native project template using br/bv for workflow management.
- **Existing skills**: `br` (bead state), `bv` (graph context), `omp` (full OMP reference), `orchestrator` (phase routing agent), `verification-before-completion` (verification discipline).
- **Missing**: No single skill ties br + bv together as a workflow backbone reference.
- **Target file**: `.omp/skills/backbone/SKILL.md` (new, ≤150 lines).
- **Convention**: Skills use YAML frontmatter (`name`, `description`) + Markdown body. Short noun names. Kebab-case artifacts.

## Design decisions

- **D1**: Name `backbone` — matches README phrasing ("backbone of planning, execution, verification, and review").
- **D2**: Reference card, not routing agent — the `orchestrator` already handles active routing.
- **D3**: Reference other skills by name/purpose; do not duplicate their content.
- **D4**: Phase routing table format (Phase, Command, Tools, Artifacts, Pre-flight checks) for scannability.
- **D5**: Full artifact layout included inline — too central to delegate to a reference.

## Current state

- **PRD**: Written (`prd.md`, `prd.json`, `decisions.md`).
- **Plan**: Written (`plan.md`, `tasks.md`).
- **Implementation**: Not started. The skill file `.omp/skills/backbone/SKILL.md` does not yet exist.

## Next agent actions

1. Create `.omp/skills/backbone/` directory.
2. Write `SKILL.md` following the outline in `plan.md` and `tasks.md`.
3. Verify skill loads in OMP (`skill://backbone/SKILL.md` readable, `/extensions` lists it).
4. Confirm no conflicts with existing skills.
5. Record verification evidence in `completion-evidence.json`.

## Files to read before implementing

- `.omp/skills/br/SKILL.md` — br tool conventions
- `.omp/skills/bv/SKILL.md` — bv tool conventions
- `.omp/skills/omp/SKILL.md` — OMP reference (especially the "Template-specific decision rules" section)
- `.omp/skills/orchestrator/SKILL.md` — active routing rules to avoid overlap
- `.omp/AGENTS.md` — project context and workflow expectations
- `.omp/memory/project/conventions.md` — naming and artifact conventions
- `.omp/memory/project/decisions.md` — project-level decisions
