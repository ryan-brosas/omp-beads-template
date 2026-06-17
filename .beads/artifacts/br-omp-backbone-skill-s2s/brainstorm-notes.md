# Brainstorm Notes: br-omp-backbone-skill-s2s

Generated: 2026-06-17 | Agent: makora1

## Summary

Audit of omp-template after all 13 prior beads closed. Found multiple quality/documentation issues.

## Findings

### 1. Missing Design Assets (12 files)

Referenced in `.omp/memory/project/tech-stack.md` (Design Assets table + Craft References table) and `.omp/memory/project/conventions.md` (line 101), but none exist on disk:

| File | Referenced In | Purpose |
|------|--------------|---------|
| `.omp/skills/design-system/DESIGN.md` | conventions.md:101, tech-stack.md:69 | 9-section brand contract |
| `.omp/design/tokens.css` | tech-stack.md:70 | CSS custom properties |
| `.omp/design/base.css` | tech-stack.md:71 | Minimal reset + body defaults |
| `.omp/design/primitives.css` | tech-stack.md:72 | Base element styles |
| `.omp/design/craft/typography.md` | tech-stack.md:78 | Type scale reference |
| `.omp/design/craft/color.md` | tech-stack.md:79 | Palette structure |
| `.omp/design/craft/anti-ai-slop.md` | tech-stack.md:80 | Seven cardinal sins |
| `.omp/design/craft/animation-discipline.md` | tech-stack.md:81 | Motion rules |
| `.omp/design/craft/state-coverage.md` | tech-stack.md:82 | Loading/empty/error states |
| `.omp/design/craft/accessibility-baseline.md` | tech-stack.md:83 | WCAG 2.2 AA |
| `.omp/design/craft/form-validation.md` | tech-stack.md:84 | Input state machine |
| `.omp/design/craft/typography-hierarchy.md` | tech-stack.md:85 | Hierarchy rules |

### 2. Empty Headers in conventions.md

- Line 112: `### CSS Ownership` — no content, immediately followed by another header
- Line 118: `### Craft Rules` — no content, immediately followed by another header

### 3. Stale project.md

- Line 23: Milestone still says "Command–convention consistency audit (br-omp-backbone-skill-1da)" — that bead is closed
- Line 24: Next says "Workflow verification" — never executed

### 4. Missing design-system Skill Directory

- `conventions.md:101` references `.omp/skills/design-system/DESIGN.md`
- No `.omp/skills/design-system/` directory exists at all
- Note: tech-stack.md also references design files under `.omp/design/` which doesn't exist

## Decision Required

These design files were adapted from "Open Design's craft/ directory (Apache 2.0) and refero_skill (MIT)" per tech-stack.md:87. The key question for /create:

- **Option A**: Create the missing design files as empty stubs that downstream projects fill in (consistent with template philosophy)
- **Option B**: Remove all stale references — this template doesn't need design assets because it's a workflow template, not a UI template
- **Option C**: Create the design-system skill with DESING.md as the brand contract, remove .omp/design/ references (those belong in downstream projects, not in the template), fix empty headers

Recommendation: Option C — the design-system skill is referenced by the orchestrator and is part of the template's skill library. The .omp/design/ files are downstream concerns. Empty headers should be either filled or removed.

## Notes for /create

- conventions.md "UI Design" section seems out of place for a workflow template — this is template cruft from a prior project
- tech-stack.md "Design Assets" and "Craft References" tables are downstream concerns, not template infrastructure
- The design-system SKILL.md should document the brand contract format that downstream projects fill in
