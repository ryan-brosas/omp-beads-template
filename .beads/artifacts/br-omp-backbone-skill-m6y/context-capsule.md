# Context Capsule: br-omp-backbone-skill-m6y

## Objective

Post-review cleanup of 5 accumulated quality issues surfaced by the Codex automated reviewer on PR #2 and the vui bead review cycle. The repository's memory files have drifted: conventions.md is 75% over its documented 4KB size target due to duplicated UI design rules, project.md contains a self-matching grep that creates false positives in success criteria verification, tech-stack.md has non-executable shell commands (`N/A — ...` in bash blocks), AGENTS.md is missing 4 of 9 template files from its canonical tree diagram, and project.md's Current Phase references a stale milestone (bead 1da) instead of the current state. All changes are doc-only — no runtime behavior, no code, no database. The bead is an orphan (0 graph edges, 0 dependents) so there are no ordering constraints.

## Key Patterns

- **Memory file maintenance happens on `/close`** — conventions.md § Memory File Maintenance documents when each file should be updated, but the process relies on agent vigilance rather than automated checks. This bead is a manual sweep of accumulated rot.
- **Design rules live in skills, not Tier 1 memory** — `.omp/skills/design-system/SKILL.md` is the on-demand entry point for UI generation rules. `.omp/memory/project/conventions.md` should point there, not duplicate its content. The design system contains 5 craft files (animation-discipline.md, anti-ai-slop.md, color.md, typography.md, DESIGN.md) that provide full-depth rules — conventions.md needs only a pointer.
- **Success criteria must be self-consistent** — A success criterion that fails when you run the prescribed verification command is worse than no criterion at all. The `--exclude=project.md` fix makes the grep self-aware.
- **`true  #` is the canonical shell no-op** — Preferred over `:` because it's explicit about intent. Both exit 0 and accept arguments silently, but `true` is more recognizable to non-shell experts and tooling.
- **Tree diagrams are canonical maps** — Agents use the AGENTS.md tree as their mental model of the repository. Missing entries mean agents don't know those files exist, leading to skipped steps (e.g., `/verify` reads completion-evidence.json but the tree doesn't show it).

## Constraints

1. **Do NOT modify design system content** — DESIgn.md, tokens.css, primitives.css, base.css, and all craft/*.md files are authoritative. This bead only relocates conventions.md rules into SKILL.md.
2. **Do NOT change conventions.md structure beyond the UI Design section** — The rest of the file (naming, workflow, agent conventions, honcho memory, memory file maintenance, per-phase quick ref, memory protocol, honcho operating protocol, skills map, philosophy, guardrails) is stable and not in scope.
3. **Do NOT add new templates or remove existing ones** — The 9 template files in `.omp/templates/` are correct. The fix is documentation only: listing them in the tree.
4. **Do NOT modify any `.omp/commands/*.md` files** — Their content is stable from the vui bead and not in scope for this cleanup bead.
5. **Do NOT retroactively fix Codex findings on closed bead artifacts** — Historical bead artifacts (1da, nvf, vui) remain as they are. Only living memory/configuration files are in scope.
6. **Keep the 3-line pointer in conventions.md exactly that** — No temptation to re-add any UI rule to conventions.md. The pointer is the contract: "load design-system/SKILL.md."
7. **Use `true  #` not `:` for no-ops** — Consistency matters. All 6 replacements use the same pattern.
8. **All changes in one atomic commit** — Single conventional commit `fix: ... (br-omp-backbone-skill-m6y)`. No partial states.

## File Ownership

| Task | Allowed | Forbidden |
|------|---------|-----------|
| 1.1 | `.omp/memory/project/conventions.md` | All other files |
| 1.2 | `.omp/memory/project/project.md` | All other files |
| 1.3 | `.omp/memory/project/tech-stack.md` | All other files |
| 2.1 | `.omp/skills/design-system/SKILL.md` | `.omp/skills/design-system/DESIGN.md`, `craft/*.md`, CSS files |
| 2.2 | `.omp/AGENTS.md` | All other files |
| 3.1 | Git staging area only | No new edits |
| 3.2 | `.beads/artifacts/br-omp-backbone-skill-m6y/completion-evidence.json` | No edits to source files |
| 3.3 | Bead graph (via `br sync`) | No file writes |

## Graph Context

- **Blast radius:** 5 files (3 memory files, 1 AGENTS.md, 1 design-system SKILL.md) — all doc/config. No code, no runtime, no database.
- **Related beads:** 0 edges — this bead is an orphan. No dependencies, no dependents.
- **File history:** Files have moderate bead history:
  - `conventions.md` — modified by 1da (initial creation), vui (density gate sync, design system migration). Now being trimmed.
  - `project.md` — modified by 1da (initial creation), vui (current phase updates). Now being fixed/updated.
  - `tech-stack.md` — modified by 1da (initial creation), vui (design assets table removed). Now getting shell-safe no-ops.
  - `AGENTS.md` — modified by 1da (initial creation), nvf (init.md hydration fixes), vui (design system migration). Tree diagram being completed.
  - `design-system/SKILL.md` — created by vui bead. Now absorbing Tier 1 craft rules.
- **Hotspots touched:** None — all files have ≤3 bead history. No file meets the >3 threshold.
- **Graph metrics:** 12 nodes (11 closed + this bead), 0 edges, density 0. All orphans, uniform PageRank 0.083. Velocity: 11 closed in 7 days.
- **Critical path:** No — 0 downstream dependents. This bead blocks nothing.
