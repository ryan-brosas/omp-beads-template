# Context Capsule: br-omp-backbone-skill-l3d

## Objective

Hydrate the 5 template memory files under `.omp/memory/project/` with real project identity. These files were written by `/init` with placeholder text (`<project-name>`, `<!-- TODO: fill in -->`, `<option1 | option2>` markers) and have never been updated since template bootstrap. Every agent session loads this placeholder noise — `grep -r '<project-name>' .omp/memory/project/` currently returns 5 matches. The fix replaces all placeholders with concrete content derived from README.md and observable repo state, fixes a broken markdown table in tech-stack.md (3 orphan rows after an attribution paragraph, plus a missing file entry), promotes 5 real architecture decisions from an "Example" section to the actual "Decision Log" (removing the redundancy), and separates project-specific gotchas from template-universal gotchas with a consumer note. After this bead, an agent loading the context can answer "what is this project" within 3 seconds.

The work is a chore (P2, 45-minute estimate). No compiled code changes. No graph dependencies — all 9 beads in the graph are orphans (density 0). The blast radius is exactly 5 markdown files with no cross-file references. Each file is edited independently in sequential waves with per-wave verification gates.

## Key Patterns

- **Memory file frontmatter** — Every memory file uses a YAML-style frontmatter block delimited by `---`. The block contains `purpose:` (a one-line description of the file's role) and `updated:` (a YYYY-MM-DD date). The `purpose` field must not change. The `updated` date must change from `2026-06-17` to `2026-06-18` (today) in all 5 files. Reference: `.omp/memory/project/project.md` lines 1-3 for the canonical frontmatter pattern.
- **Placeholder replacement, not section addition** — The PRD explicitly forbids adding new top-level sections. Edits replace placeholder text with concrete text in-place. The file structure (headings, sections, instruction paragraphs) stays intact. This preserves the files' dual role as both project documentation and template examples for consumers. Reference: `.omp/memory/project/project.md` for the section structure that must survive.
- **README.md as canonical identity source** — The project name "OMP Beads Template" is derived from `README.md` line 1 heading. The goal description incorporates the README's first paragraph ("OMP-native project template with br and bv as the backbone of planning, execution, verification, and review") expanded with concrete deliverables observable in the repo. Do not invent project identity — if uncertain, re-read README.md. Reference: `README.md` lines 1-3.
- **Markdown table structure rules** — Tables use pipe syntax with a header row, separator row (`|---|---|...`), and data rows. Column counts must be consistent across all rows in a table. Multi-word cells are space-padded for readability but padding is not required. An attribution or description paragraph must appear OUTSIDE the table (before or after), not between data rows. The tech-stack.md craft table fix is specifically about this rule — currently it's violated by the attribution paragraph sitting between table row 4 and table row 5. Reference: `.omp/memory/project/conventions.md` "Languages by Purpose" table for a well-formed table example; `.omp/memory/project/tech-stack.md` lines 78-88 for the broken table.
- **Decision log format** — Each decision in the Decision Log is a table row: `| # | Date | Decision | Rationale | Confidence |`. The `#` is sequential starting from 1. Date is `YYYY-MM` (month precision). Decision is one sentence — concrete, not abstract. Rationale includes tradeoffs and rejected alternatives. Confidence is one of High/Medium/Low. The "How to Add a Decision" reference section describes this format in detail. Reference: `.omp/memory/project/decisions.md` "Example" section for the exact 5 decision texts.
- **Gotcha entry format** — Each gotcha is a table row: `| Date | Area | Gotcha | Impact | Mitigation |`. Date is `YYYY-MM` (discovery date). Area is a subsystem name (workflow, bv, br, memory, commands, skills, omp, models, git). Gotcha is specific — what happens, not vague ("bv returns empty" not "bv is broken"). Impact is a concrete consequence. Mitigation is actionable — something the next person can DO. The "How to Add a Gotcha" reference section describes this format. Reference: `.omp/memory/project/gotchas.md` "Template Bootstrap Gotchas" table for the exact 12 entry texts.
- **Idempotency is not a concern** — The memory files are static markdown, not generated code. No automated process regenerates them. Re-running `/init` would write them fresh from templates (with placeholders), so this bead's edits are one-time. The shipping agent must NOT run `/init` during `/ship` because it would overwrite the edits. Reference: `.omp/commands/init.md` Phase 2.5 for the `/init` hydration logic that writes these files.
- **Scope boundary: memory files only** — The blast radius is exactly 5 files under `.omp/memory/project/`: `project.md`, `conventions.md`, `tech-stack.md`, `decisions.md`, `gotchas.md`. No other directory is touched. The shipping agent must not edit `.omp/commands/init.md` (which contains the Python script that originally wrote these files), `.omp/templates/` (which contains the templates the files were instantiated from), `.omp/skills/`, `.omp/AGENTS.md`, `.omp/RULES.md`, `DESIGN.md`, `design/`, `README.md`, or `.gitignore`. Reference: PRD "Out of Scope" section for the full exclusion list.
- **Content preservation is mandatory** — The 5 decisions in decisions.md and all 12 gotchas in gotchas.md must survive the restructure. Decision text, rationale, and confidence are verbatim — the shipping agent copies exact strings, not paraphrases. Gotcha entries are verbatim except for the one meta-gotcha ("Memory templates waste tokens if left as placeholders") whose mitigation text is updated to reference this bead ID (`br-omp-backbone-skill-l3d`). The update changes "Delete placeholder gotchas when real ones exist" to "Fill with real project content immediately. This bead (br-omp-backbone-skill-l3d) addresses the initial hydration. Audit memory files during /close." All other text in that entry (Date, Area, Gotcha, Impact) is verbatim. Reference: `.omp/memory/project/decisions.md` Example section lines and `.omp/memory/project/gotchas.md` Template Bootstrap table lines for the original texts.
- **Verification-first editing discipline** — Before each edit, read the target file to anchor current line numbers (they may differ from the plan's approximate line numbers). After each edit, run the per-task verification checks before moving to the next file. Do not edit from memory — line numbers shift between tasks as text is inserted or removed. Reference: plan.md "Observable Truths" for the pre-edit state of each file; plan.md "File Edit Map" for the approximate line ranges.
- **No new content creation** — This bead fills placeholders and fixes structure. It does not add new gotchas, new decisions, new sections, or new factual claims. The goal text in project.md derives from README.md (canonical). The success criteria are observable properties of this bead's own outcome (zero placeholders, valid markdown, agent comprehension). The current phase reflects actual repo activity (8 beads closed in last 7 days, design system scaffolded, commands and skills refined). Every claim in the edited memory files has a verifiable source in the repo. Reference: PRD "In Scope" list for what this bead does touch; "Out of Scope" for what it explicitly does not.
- **Sequential waves with rollback safety** — Each wave (1 through 5) edits exactly one memory file and verifies it before moving to the next. Wave 6 runs full cross-file verification. If a wave fails verification, the shipping agent can revert that single file's changes without affecting the other 4 files. The files are logically independent — no memory file references another memory file's content. The sequential structure also prevents context window saturation: reading and editing 5 files simultaneously risks holding stale snapshots. Reference: plan.md "Why Sequential Waves" rationale for the design decision.
- **Craft file table alphabetization** — The tech-stack.md craft references table should list files in alphabetical order for consistency. The current order (before fix) is arbitrary: typography, color, anti-ai-slop, animation-discipline, [attribution break], accessibility-baseline, form-validation, typography-hierarchy. The fixed order is alphabetical: accessibility-baseline, animation-discipline, anti-ai-slop, color, form-validation, state-coverage, typography, typography-hierarchy. This makes it easy to check if a file is listed and easy to insert new craft files in the future. Reference: `ls design/craft/` output for the file listing.
- **Blockquote for consumer guidance** — Template-universal gotchas (those that apply to any project cloning the template) need a clear marker that they ship with the template and should be replaced. Use a markdown blockquote (`> `) for this. The blockquote text is: `> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.` This pattern is used nowhere else in the repo and introduces no new markdown syntax that agents can't parse. Reference: The blockquote will appear in `.omp/memory/project/gotchas.md` under the "## Template Bootstrap Gotchas" heading, between the description paragraph and the table.

## Constraints

### MUST

1. MUST replace all `<project-name>` placeholders with "OMP Beads Template" across all 5 files — `grep -r '<project-name>' .omp/memory/project/` must return zero matches after the bead
2. MUST replace all `<!-- TODO: fill in -->` markers in project.md with concrete text — no `<!-- TODO` should remain in project.md
3. MUST fill the Languages by Purpose table in conventions.md with actual values: Backend = N/A, Frontend = N/A, Scripts = Python. Agent instructions and Configuration rows stay as-is (already have real content)
4. MUST fix the craft references table in tech-stack.md: all 8 craft files in one contiguous table (header + separator + 8 data rows) with the attribution paragraph after the table, separated by a blank line. No orphan rows. No attribution between table rows.
5. MUST replace verification command placeholders in tech-stack.md with "N/A" and a brief explanation. The 4 verification commands (typecheck, lint, test, build) and 2 security commands (dependency audit, secrets scan) all become N/A because this is a template repo with no compiled code, no dependencies, and no configured tooling.
6. MUST keep `bv --robot-triage` and `br list --status open --status in_progress --json` commands in tech-stack.md under "Graph state (always available)" — these are always valid regardless of repo type
7. MUST move 5 real decisions from the "Example" section to the "Decision Log" section in decisions.md. Content is verbatim — exact same date, decision text, rationale, and confidence. Only the heading changes.
8. MUST remove the "## Example" section heading and all its content from decisions.md — the content is already migrated to Decision Log, so the Example section is redundant
9. MUST remove the placeholder row (`| 1 | <YYYY-MM> | <what we decided> | <why — tradeoffs, alternatives considered> | <High | Medium | Low> |`) from the Decision Log table in decisions.md
10. MUST separate project-specific gotchas (Active Warnings) from template-universal gotchas (Template Bootstrap Gotchas) in gotchas.md. The "memory templates waste tokens" entry is project-specific — it describes this repo's own maintenance problem. The other 11 entries are template-universal — they apply to any project that clones the template.
11. MUST add a blockquote note in gotchas.md under "Template Bootstrap Gotchas" clarifying that these ship with the template and consumers should replace them: `> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.`
12. MUST preserve all 5 decision texts, rationales, and confidence levels verbatim from the Example section to the Decision Log. Use `git diff` or Python assertion checks to verify verbatim preservation.
13. MUST preserve all 12 gotcha entries (1 in Active Warnings, 11 in Template Bootstrap Gotchas). Only the meta-gotcha's mitigation text may be updated to reference this bead ID. All other gotcha text (Date, Area, Gotcha, Impact) is verbatim.
14. MUST update the `updated:` frontmatter date in all 5 files from `2026-06-17` to `2026-06-18` (today's date)
15. MUST keep each memory file as valid markdown: frontmatter is properly delimited with `---`, headings use `#` and `##` syntax, tables have consistent column counts across header/separator/data rows, no orphan rows without headers, no broken pipe syntax
16. MUST keep the "How to Add a Decision" reference section in decisions.md — its 5-step guide is useful documentation
17. MUST keep the "How to Add a Gotcha" reference section in gotchas.md — its 5-step guide with the "Remove entries once the underlying bug is fixed" note is useful documentation
18. MUST keep instruction/guidance paragraphs that are useful for template consumers: the "Fill in the actual languages..." line after the conventions.md languages table, the "Keep to 3-5 criteria..." line after project.md success criteria, the "Replace placeholders..." line after tech-stack.md verification commands, the intro paragraph after decisions.md header
19. MUST read each target file before editing it — current line numbers may differ from the plan's approximate line numbers. Do not rely on plan line numbers; use the actual file state
20. MUST read `design/craft/state-coverage.md` to derive its purpose description for the craft references table. Do not invent a description — read the file and extract keywords from its heading and introductory text

### SHOULD

1. SHOULD verify each file immediately after editing (per-wave verification gates) before moving to the next wave. This limits blast radius if an edit is wrong — only one file needs reverting
2. SHOULD keep edits minimal — replace only placeholder text, do not reformat unchanged sections. For example, don't re-align table columns that aren't being edited
3. SHOULD record line numbers edited for each file (start and end of each edit block) for the diff scope check in Wave 6
4. SHOULD derive the project goal text from README.md first paragraph rather than inventing it. If the plan's suggested goal text doesn't match the README after re-reading, use the README
5. SHOULD alphabetize the craft references table — the fixed table should list files in alphabetical order: accessibility-baseline, animation-discipline, anti-ai-slop, color, form-validation, state-coverage, typography, typography-hierarchy
6. SHOULD update the meta-gotcha's mitigation text to reference this bead ID (`br-omp-backbone-skill-l3d`) so future maintainers can trace when and how the problem was addressed
7. SHOULD NOT run `/init` during `/ship` — it would regenerate placeholder-filled memory files, undoing this bead's work

### MUST NOT

1. MUST NOT edit `.omp/commands/init.md` — the hydration script that wrote these files. PRD explicitly excludes it
2. MUST NOT edit `.omp/templates/` — the template files that define the placeholder structure
3. MUST NOT edit `.omp/skills/` — any skill definition files
4. MUST NOT edit `.omp/AGENTS.md` — the canonical project context that inlines memory files
5. MUST NOT edit `.omp/RULES.md` — workflow rules
6. MUST NOT edit `DESIGN.md` — the 9-section brand contract
7. MUST NOT edit `design/` — any design system files (tokens.css, primitives.css, base.css, craft/)
8. MUST NOT edit `README.md` — project README (the canonical identity source is read-only)
9. MUST NOT edit `.gitignore` — ignore rules
10. MUST NOT add new top-level sections to any memory file — headings and structure stay as-is
11. MUST NOT change existing decision rationale or confidence values — verbatim copy only
12. MUST NOT add new gotcha entries beyond the 12 that already exist
13. MUST NOT delete any existing gotcha entry — all 12 entries (1 project-specific + 11 template-universal) must survive
14. MUST NOT add new memory files — the 5 existing files are the complete set
15. MUST NOT change the frontmatter `purpose:` field in any file — only `updated:` changes
16. MUST NOT reformat unchanged sections of any file — this creates noisy diffs and increases review burden. If a table column alignment is "wrong" but wasn't part of the edit, leave it
17. MUST NOT run destructive commands (`rm`, `git reset --hard`, `git checkout --`, force push) on memory files
18. MUST NOT create a `.pi/` directory or move files out of `.omp/` — this breaks OMP native discovery
19. MUST NOT modify the Runtime table in tech-stack.md — the `<TypeScript | Python | Go | Rust>` placeholders in the Runtime/Language/Runtime/Package manager rows are intentionally kept as template patterns for consumers
20. MUST NOT modify the Key Dependencies table in tech-stack.md — the `<name> | <what it does> | <version>` placeholder row is intentionally kept

## File Ownership

| Task | Allowed (edit) | Allowed (read) | Forbidden |
|------|---------------|----------------|-----------|
| 1.1 | `.omp/memory/project/project.md` | `README.md`, `.omp/AGENTS.md` | All other files |
| 2.1 | `.omp/memory/project/conventions.md` | — | All other files |
| 3.1 | `.omp/memory/project/tech-stack.md` | `design/craft/state-coverage.md` | All other files |
| 4.1 | `.omp/memory/project/decisions.md` | — | All other files |
| 5.1 | `.omp/memory/project/gotchas.md` | — | All other files |
| 6.1 | — (read-only) | All 5 memory files | All non-memory files |

## File Edit Map

This map shows every edit to every file with approximate line numbers. The shipping agent must read each file before editing — line numbers may differ from these approximations. Use these as a guide for what to look for, not as exact coordinates.

### project.md — Task 1.1 (10 estimated minutes)

Edits: 10 replacements across ~29 lines. Pre-edit size: ~750 bytes. Post-edit size: ~900 bytes.

| # | Approx Line | What | From | To |
|---|-------------|------|------|----|
| 1 | 2 | Frontmatter date | `updated: 2026-06-17` | `updated: 2026-06-18` |
| 2 | 5 | Header | `# Project: <project-name>` | `# Project: OMP Beads Template` |
| 3 | 7-8 | Instruction line | `Replace this with your actual project name.\n\n` | (remove, or keep one blank line) |
| 4 | 11 | Goal | `<One sentence — what are we building and why?>` | `An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating.` |
| 5 | 15 | Criterion 1 | `1. **<Criterion 1>** — <measurable outcome>` | `1. **Zero template placeholders** — No \`<project-name>\` or \`<!-- TODO\` markers in any \`.omp/memory/project/\` file. Verifiable with \`grep\`.` |
| 6 | 16 | Criterion 2 | `2. **<Criterion 2>** — <measurable outcome>` | `2. **Valid markdown throughout** — Every memory file is valid markdown with correctly structured tables. Verifiable by reading each file.` |
| 7 | 17 | Criterion 3 | `3. **<Criterion 3>** — <measurable outcome>` | `3. **Agent comprehension within 3 seconds** — An agent loading this context can answer 'what is this project' immediately from project.md. Qualitative but observable.` |
| 8 | 24 | Status | `- **Status:** <active \| maintenance \| paused>` | `- **Status:** active` |
| 9 | 25 | Milestone | `- **Milestone:** <what we're working toward right now>` | `- **Milestone:** Memory file hydration — project identity hardening` |
| 10 | 26 | Next | `- **Next:** <the next concrete deliverable>` | `- **Next:** Audit command files for consistency with conventions` |

After edit: The "Keep to 3-5 criteria..." instruction paragraph (lines ~18-20) stays. The section headings (`## The Goal`, `## Success Criteria`, `## Current Phase`) stay. The frontmatter stays (with updated date). The "Update this section after every milestone..." instruction paragraph (last paragraph) stays.

### conventions.md — Task 2.1 (10 estimated minutes)

Edits: 5 replacements across ~143 lines. Pre-edit size: ~4.4KB. Post-edit size: ~4.4KB (placeholders replaced with similar-length text).

| # | Approx Line | What | From | To |
|---|-------------|------|------|----|
| 1 | 2 | Frontmatter date | `updated: 2026-06-17` | `updated: 2026-06-18` |
| 2 | 6 | Header | `# Conventions: <project-name>` | `# Conventions: OMP Beads Template` |
| 3 | ~19 | Backend row | `\| Backend \| <TypeScript \| Go \| Rust \| Python> \| <strict? Bun? Deno?> \|` | `\| Backend \| N/A \| Template repo — no backend runtime \|` |
| 4 | ~20 | Frontend row | `\| Frontend \| <TypeScript \| JavaScript> \| <React? Svelte? plain?> \|` | `\| Frontend \| N/A \| Template repo — provides design system assets only \|` |
| 5 | ~21 | Scripts row | `\| Scripts \| <Bash \| Python \| TypeScript> \| <CI, dev tooling, one-offs> \|` | `\| Scripts \| Python \| \`/init\` hydration script \|` |

After edit: Agent instructions row stays (`Markdown | Skills, commands, memory files`). Configuration row stays (`JSON / YAML | settings, manifests`). The "Fill in the actual languages..." instruction paragraph after the table stays. All other sections (`## Naming`, `## Skill Structure`, `## Command Structure`, `## Git`, `## Workflow`, `## Agent Conventions`, `## Honcho Memory`, `## Memory File Maintenance`, `## UI Design`) are untouched.

### tech-stack.md — Task 3.1 (15 estimated minutes)

Edits: 9 replacements across ~88 lines. Pre-edit size: ~2.5KB. Post-edit size: ~2.5KB.

| # | Approx Line | What | From | To |
|---|-------------|------|------|----|
| 1 | 2 | Frontmatter date | `updated: 2026-06-17` | `updated: 2026-06-18` |
| 2 | 6 | Header | `# Tech Stack: <project-name>` | `# Tech Stack: OMP Beads Template` |
| 3 | ~35 | Typecheck cmd | `<tsc --noEmit \| mypy \| cargo check \| go vet>` | `N/A — template repo, no compiled code` |
| 4 | ~38 | Lint cmd | `<eslint \| ruff \| clippy \| golangci-lint>` | `N/A — no linter configured for template files` |
| 5 | ~41 | Test cmd | `<vitest run \| pytest \| cargo test \| go test ./...>` | `N/A — no test framework` |
| 6 | ~44 | Build cmd | `<tsup \| pip install -e . \| cargo build --release \| go build>` | `N/A — no build step` |
| 7 | ~52 | Audit cmd | `<npm audit \| pip-audit \| cargo audit \| govulncheck>` | `N/A — template repo, no runtime dependencies` |
| 8 | ~55 | Secrets cmd | `<gitleaks detect \| trufflehog filesystem .>` | `N/A — no secrets scanning configured` |
| 9 | 78-88 | Craft table block | Broken: 4 rows + attribution mid-table + 3 orphan rows, missing state-coverage.md | Fixed: one contiguous 8-row table + attribution after |

**Craft table edit detail:** Replace the entire "## Craft References" section body (from the description paragraph through the last orphan row) with:

```
Brand-agnostic universal design rules that apply on top of any `DESIGN.md`:

| File | Purpose |
|------|---------|
| `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
| `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |
| `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
| `design/craft/state-coverage.md` | [Derived from file — read design/craft/state-coverage.md for purpose keywords] |
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
```

After edit: The `## Runtime` table, `## Key Dependencies` table, `## Design Assets` table, and `## Constraints` section are untouched. The "Graph state (always available)" commands under verification stay unchanged.

### decisions.md — Task 4.1 (10 estimated minutes)

Edits: 4 structural changes across ~34 lines. Pre-edit size: ~1.3KB. Post-edit size: ~1.3KB.

| # | Approx Line | What | From | To |
|---|-------------|------|------|----|
| 1 | 2 | Frontmatter date | `updated: 2026-06-17` | `updated: 2026-06-18` |
| 2 | 6 | Header | `# Decisions: <project-name>` | `# Decisions: OMP Beads Template` |
| 3 | ~14-16 | Decision Log body | Placeholder row removed; 5 real decision rows inserted from Example section | Decision Log has 5 real rows (verbatim from Example) |
| 4 | ~24-34 | Example section | Entire `## Example` heading, table header, separator, and 5 rows removed | Section gone; content is in Decision Log |

**Decision rows to insert (verbatim):**

```
| 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator. Alternatives (linear, plain markdown) lack the graph query ability. | High |
| 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts and skill knowledge. Scripts add maintenance burden, platform dependencies, and hidden logic. | High |
| 3 | 2026-06 | Bare command names (`/create`, `/plan`) | OMP resolves commands by directory. Prefix would be noise. | High |
| 4 | 2026-06 | `.omp/` as native project root | OMP loads from `.omp/`. Parallel `.pi/` config creates confusion. | High |
| 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages. The beads template stays pure workflow — install providers separately. | High |
```

After edit: The intro paragraph ("Every architecture decision...") stays. The "## How to Add a Decision" section (5 steps) stays verbatim. The "## Example" section is gone. The document ends with the How to Add section.

### gotchas.md — Task 5.1 (10 estimated minutes)

Edits: 5 changes across ~44 lines. Pre-edit size: ~2.2KB. Post-edit size: ~2.3KB.

| # | Approx Line | What | From | To |
|---|-------------|------|------|----|
| 1 | 2 | Frontmatter date | `updated: 2026-06-17` | `updated: 2026-06-18` |
| 2 | 6 | Header | `# Gotchas: <project-name>` | `# Gotchas: OMP Beads Template` |
| 3 | ~13-14 | Active Warnings body | Placeholder row removed; project-specific gotcha inserted | Active Warnings has 1 real entry (memory templates gotcha with updated mitigation) |
| 4 | ~17 | Template Bootstrap note | (none) | Blockquote note inserted after description paragraph, before table |
| 5 | ~29 | Template Bootstrap row | "Memory templates waste tokens" row removed (moved to Active Warnings) | Template Bootstrap has 11 entries (original 12 minus 1 moved) |

**Project-specific gotcha to insert in Active Warnings (with updated mitigation):**

```
| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session — compounds across sessions | Fill with real project content immediately. This bead (br-omp-backbone-skill-l3d) addresses the initial hydration. Audit memory files during /close. |
```

**Blockquote note to insert in Template Bootstrap Gotchas:**

```
> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.
```

After edit: The "How to Add a Gotcha" section (5 steps + "Remove entries once the underlying bug is fixed" note) stays verbatim. The 11 template-universal gotcha entries stay in their original order. The description paragraph for Template Bootstrap Gotchas stays ("These are the gotchas that come with the template itself...") — the blockquote supplements it, doesn't replace it.

## Graph Context

- **Blast radius:** 5 files (0 new, 5 edits, 0 deletes) — all under `.omp/memory/project/`. No files outside this directory are touched.
- **Related beads:** 8 other beads exist in the graph: `br-omp-backbone-skill-1ct`, `-9tl`, `-hfh`, `-iej`, `-kfu`, `-mcu`, `-nvf`, `-qjk`. All 9 beads (including this one) are completely disconnected — no dependency edges exist between any pair. The graph has 9 nodes, 0 edges, and density 0. This bead neither blocks nor is blocked by any other bead.
- **File history:** The 5 target memory files have zero bead history. `bv --robot-file-hotspots --format json` reports `total_files: 0` and `total_bead_links: 0`. No bead has ever edited `.omp/memory/project/*.md` files. They were written once by `/init` during template bootstrap and have been read-only since. This is the first bead to touch them.
- **Hotspots touched:** None — no file in the graph has >3 bead history. The repo has no file-level bead links at all.
- **Graph metrics:**
  - Nodes: 9 | Edges: 0 | Density: 0.0
  - Cycles: 0 (acyclic DAG — trivially, with no edges)
  - Articulation points: 0
  - KCore: 0 for all nodes (no node has any neighbors)
  - PageRank: 0.111 for all nodes (equal in a disconnected graph)
  - Eigenvector: 0.111 for all nodes (equal)
  - Betweenness: 0 for all nodes (no paths to be on)
  - HITS Hubs: 0 for all nodes | Authorities: 0 for all nodes
  - Critical path score: 1 for all nodes (equal)
  - Slack: 0 for all nodes
  - Topological order: all 9 nodes are in arbitrary order (no edges to constrain)
- **Velocity:** 8 beads closed in the last 7 days. 8 beads closed in the last 30 days (all in the past week). Average 0.02 days to close. Estimated velocity: 16 minutes per day.
- **Forecast:** 52 minutes (confidence 0.4). The bead's own estimate is 45 minutes. Forecast factors: chore type ×0.8, dependency depth 1 ×1.10, empty description ×1.00, 1 agent. ETA: 2026-06-21 (low: 2026-06-19, high: 2026-06-22).
- **Planning track:** Single track (`track-A`) with this bead as the only item. No parallelizable work because the graph has no dependency edges to identify parallelism — but the files themselves are independent and could be parallelized. The plan chooses sequential waves for rollback safety, not because the graph constrains it.
- **What this bead unblocks:** Nothing directly in the dependency graph (no edges). Indirectly, it unblocks agent comprehension: every future agent session in this repo will load real project identity in ~300 tokens instead of ~330 tokens of placeholder noise. Over 10 sessions, that saves ~300 tokens. More importantly, agents will understand what this project IS, which is currently impossible from memory files alone.
- **What blocks this bead:** Nothing — no upstream dependencies. The PRD (>600 lines) and plan artifacts exist. The target files are readable and editable. The workflow gate will allow writes because PRD and plan both exist.

## No Graph Surprises

The bv graph is maximally boring for this bead — and that's exactly what we expect. Memory file hydration is a standalone project maintenance chore. It touches files that no bead has ever touched. It depends on no other bead's work, and no other bead depends on its completion. The graph accurately reflects an isolated housekeeping task:

- **0 edges** — no structural coupling to any other bead
- **0 file history** — the memory files are untouched territory
- **0 hotspots** — no risk of destabilizing high-churn files
- **0 cycles** — no risk of dependency deadlock
- **0 articulation points** — removing this bead from the graph changes nothing

This bead could be done first, last, or anywhere in between — the graph doesn't care. The only urgency is the PRD's stated reason: every agent session wastes context on placeholder noise, and the gap widens with every new feature added to the template.

## Handoff Checklist

Before handing off to `/ship`, confirm all of the following:

- [ ] `prd.md` exists in `.beads/artifacts/br-omp-backbone-skill-l3d/` — must be ≥600 lines (currently ~700+ including the PRD JSON mirror)
- [ ] `plan.md` exists — must be ≥600 lines
- [ ] `tasks.md` exists — must be ≥600 lines
- [ ] `context-capsule.md` exists — this file
- [ ] `prd.json` exists — machine-readable requirements mirror (may need generation if missing; currently present at 3696 bytes)
- [ ] br bead status is `in_progress` — claimed at 2026-06-17T16:16:35Z
- [ ] `br dep cycles --json` returns empty (no cycles)
- [ ] `bv --robot-plan --format json` shows this bead as the single actionable item in track-A
- [ ] `git status` shows a clean or known state — no uncommitted changes that would conflict with memory file edits

For the shipping agent reading this capsule:

1. **Start with tasks.md** — it has the detailed ordered checklist with 161+ checkbox items across 6 waves
2. **Reference plan.md "Observable Truths"** (23 statements) for the pre-edit state of each file — confirm each truth before editing the corresponding file
3. **Reference "File Edit Map"** (above) for what changes where with approximate line numbers
4. **Edit files in wave order: 1 → 2 → 3 → 4 → 5**, verifying each file before moving to the next
5. **Wave 6** runs the full cross-file verification suite. The plan.md "Full Verification" section has copypaste-ready Python and bash scripts
6. **Do NOT read the PRD during ship** — the plan and this capsule are self-contained. The PRD is the requirements authority; the plan is the execution authority
7. **If anything is unclear**, re-read the "Constraints" section above — the MUST/SHOULD/MUST NOT lists are the final authority. The "Key Patterns" section explains WHY certain choices were made
8. **If a verification check fails**, fix only the file that failed, re-run just that check, then re-run the full suite
9. **Do not run `/init`** — it would regenerate placeholders and undo this bead's work
10. **After all waves pass**, the bead is ready for `/verify` (record evidence in completion-evidence.json) and `/review`
