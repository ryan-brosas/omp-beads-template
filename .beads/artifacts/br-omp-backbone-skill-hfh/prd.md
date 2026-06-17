# PRD: Add OMP backbone skill

## Summary

- Bead: br-omp-backbone-skill-hfh
- Owner: ryan
- Status: in_progress

## Problem

The OMP beads template has skills for individual tools (`br`, `bv`) and a comprehensive OMP reference skill, but lacks a single entry-point skill that explains how **br and bv together form the template backbone**. Agents onboarding into this template must piece together the workflow from multiple skills, commands, and memory files. There is no single skill that:

1. Maps every workflow phase to the correct tool sequence (br → bv → OMP tools → br).
2. Defines the artifact layout, naming conventions, and lifecycle.
3. Provides a phase-by-phase reference card that agents can use as a routing table.
4. Explains when to use br, when to use bv, and when to use OMP built-ins directly.

## Outcome

A new skill `.omp/skills/backbone/SKILL.md` that:

- Is the first skill agents should load when working in this template.
- Explains the br + bv backbone concept clearly and concisely.
- Maps every workflow phase to exact tool commands and expected outputs.
- Defines the complete artifact layout and conventions.
- References, but does not duplicate, the `br`, `bv`, `omp`, `orchestrator`, and `verification-before-completion` skills.
- Serves as a quick-reference routing card for the phase-based workflow.

## Acceptance criteria

- [ ] `.omp/skills/backbone/SKILL.md` exists with valid YAML frontmatter (`name`, `description`).
- [ ] The skill explains the backbone concept: br owns state, bv informs decisions, OMP executes.
- [ ] The skill includes a phase routing table mapping each phase (brainstorm, create, plan, ship, verify, review, pr, close) to the right tools and artifacts.
- [ ] The skill defines the artifact directory layout with expected files per phase.
- [ ] The skill references other skills (`br`, `bv`, `omp`, `orchestrator`, `verification-before-completion`) without duplicating their full content.
- [ ] The skill includes minimum checks (pre-flight) an agent must perform before acting in each phase.
- [ ] The skill loads correctly in OMP (`/extensions` confirms discovery, `skill://backbone/SKILL.md` is readable).
- [ ] The skill does not conflict with existing skills, commands, or agents.

## Constraints

- Must follow the existing SKILL.md format: YAML frontmatter with `name` and `description`, followed by Markdown body.
- Must not duplicate content already covered in the `br`, `bv`, or `omp` skills; reference them instead.
- Must stay under ~150 lines to remain scannable as a quick reference.
- Must use consistent terminology with existing skills and memory files.
- Must be placed at `.omp/skills/backbone/SKILL.md`.

## Risks

- **Low**: Skill may overlap with the `orchestrator` skill. Mitigation: the backbone skill is a reference card; the orchestrator is a routing agent. They serve different purposes (reference vs. active routing).
- **Low**: Skill may become stale if the workflow evolves. Mitigation: keep it concise and reference other skills for details; update it when conventions change.
