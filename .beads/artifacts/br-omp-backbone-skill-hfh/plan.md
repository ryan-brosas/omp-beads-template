# Plan: Add OMP backbone skill

## Scope

Create a single new skill file at `.omp/skills/backbone/SKILL.md` that serves as the entry-point reference card for the beads workflow backbone.

## Blast radius

- Files: `.omp/skills/backbone/SKILL.md` (new file)
- Systems: OMP skill discovery (`.omp/skills/` directory); no changes to existing skills, commands, agents, or templates.

## Steps

1. **Create the skill directory**: `mkdir -p .omp/skills/backbone/`
2. **Write SKILL.md** with the following structure:
   - YAML frontmatter: `name: backbone`, `description: The br + bv workflow backbone reference card.`
   - **Backbone concept** section: explains that br owns bead state, bv informs decisions with graph context, and OMP executes the work.
   - **Phase routing table**: concise table mapping brainstorm → create → plan → ship → verify → review → pr → close to commands, tools, artifacts, and pre-flight checks.
   - **Artifact layout** section: the canonical directory/file structure under `.beads/artifacts/<bead-id>/`.
   - **Tool decision rules** section (abridged from omp skill): when to use br vs bv vs OMP built-ins.
   - **Related skills** section: brief references to `br`, `bv`, `omp`, `orchestrator`, `verification-before-completion` with their purposes.
   - **Minimum checks** section: pre-flight checklist before any phase.
3. **Verify skill loads**: Confirm `skill://backbone/SKILL.md` is readable and `/extensions` lists the skill.
4. **Verify no conflicts**: Confirm the new skill does not shadow or break existing skills.

## Risks and mitigations

- **Risk**: Skill overlaps with orchestrator, confusing agents about which to load.
  - **Mitigation**: The backbone skill's description clearly positions it as a reference card, not a routing agent. The orchestrator skill keeps its routing role.
- **Risk**: Skill grows too long (>150 lines) during writing, defeating the reference-card purpose.
  - **Mitigation**: Aggressively reference other skills instead of inlining; trim any prose that doesn't serve quick lookup.

## Verification

- **Command**: `omp -p '/extensions' | grep backbone`
- **Expected result**: `backbone` appears in the skill listing with its description.
- **Command**: Read `skill://backbone/SKILL.md` via OMP read tool.
- **Expected result**: Full skill content is returned; YAML frontmatter parses cleanly.
- **Command**: `wc -l .omp/skills/backbone/SKILL.md`
- **Expected result**: ≤150 lines.
