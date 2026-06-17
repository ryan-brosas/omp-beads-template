# Decisions: Add OMP backbone skill

## D1: Skill name

- **Decision**: Name the skill directory `backbone` and the skill itself `backbone`.
- **Rationale**: The README explicitly calls br and bv "the backbone of planning, execution, verification, and review." The name is descriptive, short (noun form, matching convention), and signals entry-point importance.
- **Alternatives considered**:
  - `workflow`: too generic; already used by the orchestrator concept.
  - `br-bv`: too tool-focused; doesn't capture the template-level concept.
  - `template`: conflicts with the broader template concept.

## D2: Skill scope

- **Decision**: The backbone skill is a reference card, not an active routing agent.
- **Rationale**: The `orchestrator` skill already handles active routing. The backbone skill should serve as a static reference that agents load first to understand the workflow shape. This avoids competing routing logic.
- **Alternatives considered**:
  - Merge into orchestrator: would make orchestrator too long and conflate reference with routing.
  - Make it the only entry-point skill: would break the modular design of the existing skills.

## D3: Content strategy

- **Decision**: Reference other skills by name and purpose; do not duplicate their content.
- **Rationale**: Duplication creates maintenance burden and inconsistency. The backbone skill should be the map; the other skills are the detailed terrain guides.
- **Alternatives considered**:
  - Inline all workflow documentation: would make the skill too long (>300 lines) and brittle.

## D4: Phase routing table format

- **Decision**: Use a concise table with columns: Phase, Command, Tools, Artifacts, Pre-flight checks.
- **Rationale**: A table is scannable, matches the reference-card intent, and fits in <150 lines.
- **Alternatives considered**:
  - Narrative prose: harder to scan quickly.
  - Per-phase subsections: too verbose for a reference card.

## D5: Artifact layout inclusion

- **Decision**: Include the full artifact directory layout in the skill.
- **Rationale**: The artifact layout is the physical manifestation of the backbone. Agents need to know where files go without reading conventions separately. This is central enough to include rather than reference.
- **Alternatives considered**:
  - Reference conventions.md: adds an indirection for a core fact.
