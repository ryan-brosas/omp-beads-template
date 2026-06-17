# Decisions: br-omp-backbone-skill-l3d

## Decision Log

| # | Decision | Rationale | Confidence |
|---|----------|-----------|------------|
| 1 | Use N/A over "None" or empty cells for inapplicable rows | "None" could be misread as "not configured"; empty cells look like rendering errors. "N/A" is unambiguous. | High |
| 2 | Include "Template repo" explanation with every N/A | Agents reading "N/A" alone might try to detect the stack. An explanation prevents agents from fabricating stack decisions. | High |
| 3 | Add blockquote note before Template Bootstrap Gotchas | The previous "replace with your own" paragraph was confusing in the template repo itself. A blockquote clarifies these ship WITH the template. | High |
| 4 | Derive state-coverage.md purpose from reading the file | Rather than inventing a description, read the actual file to match the pattern of other craft file descriptions. | High |
| 5 | Set updated: 2026-06-17 in all 5 memory file frontmatters | All files are modified in this bead. The updated field should reflect actual modification date for staleness detection. | High |

## Rejected Alternatives

| # | Alternative | Why Rejected | Risk if Re-introduced |
|---|-------------|--------------|----------------------|
| 1 | Change `/init` to auto-detect template repos and skip TODO markers | This is a /init logic change — out of scope. `/init` is working as designed (leaves project-specific fields for human input). Making it special-case template repos adds complexity for a one-time need. | Low — if done cleanly, could prevent this situation for future template repos. But YAGNI. |
| 2 | Move template bootstrap gotchas to a separate `gotchas.template.md` file | Adds file count (6 instead of 5). Template consumers would need to manually copy or merge. The current approach (mix them in gotchas.md with a note) is simpler but slightly messier for the template maintainer. | Low — cleaner separation, but adds maintenance surface. |
| 3 | Leave decisions in "Example" section and just rename it to "Decision Log" | The "Example" heading implies provisional content. Renaming the section while keeping the content is effectively what we're doing, but the "Example" label needs to go — it's not an example, it's a decision. | Low — would still surface the decisions, just with a confusing label. |
| 4 | Remove template bootstrap gotchas entirely (they're for consumers) | Loses institutional knowledge. Template consumers NEED these gotchas. The template maintainer also benefits from them (they document the template's design constraints). | Medium — consumers would lose important warnings about workflow gate, bv requirements, etc. |

## Assumptions

| # | Assumption | Validation | Invalidation Impact |
|---|------------|------------|---------------------|
| 1 | The 5 decisions in decisions.md's "Example" section are real architecture decisions, not provisional placeholders | Each decision matches the actual repo state: br + bv are the backbone, commands + skills only (no scripts), bare command names, .omp/ as root, tooling in separate repos. All predate this bead and are cited in conventions.md. | If any decision is contested, it should be moved back to a separate section or re-evaluated. The others remain promoted. |
| 2 | The OMP Beads Template will remain a template repo with no compiled code | Current file inventory: no package.json, no Cargo.toml, no go.mod, no pyproject.toml. All files are markdown, CSS, or TypeScript (workflow gate extension). | If a backend is added, tech-stack.md and conventions.md language table must be updated. The N/A values become stale. |
| 3 | Memory files are consumed by agents only, not by automated tooling | No tool parses the markdown structure of these files. The workflow gate reads br state, not memory files. The OMP import mechanism inlines them as text. | If a tool starts parsing these files structurally (e.g., extracting table data), the table structure changes could break it. Unlikely — these are human/agent documentation. |
| 4 | The 13 gotchas are all still relevant | Every gotcha was reviewed during exploration — all 13 describe real constraints or pitfalls in the current workflow. None are obsolete. | If any gotcha becomes obsolete (e.g., a bv bug is fixed), it should be removed in its own bead. |
| 5 | The project goal derived from README.md is accurate | README.md line 3: "OMP-native project template with br and bv as the backbone of planning, execution, verification, and review." The derived goal expands this with concrete deliverables visible in the repo. | If the maintainer disagrees with the goal wording, it's one line to change. The structure (project.md having a goal at all) is the primary win. |
