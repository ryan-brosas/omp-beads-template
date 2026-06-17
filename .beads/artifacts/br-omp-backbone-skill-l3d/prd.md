# PRD: Hydrate template memory files

**Bead:** br-omp-backbone-skill-l3d | **Type:** chore | **Priority:** P2
**Created:** 2026-06-17 | **Estimate:** 45

## Problem

WHEN any agent loads the OMP Beads Template context, THEN ~1KB of placeholder text is loaded from `.omp/memory/project/` files that contain `<project-name>` and template fill-in-the-blank markers BECAUSE the template's own memory files were never hydrated after template instantiation.

The project that teaches other repos how to hydrate their memory files via `/init` has not dogfooded its own hydration. Five memory files still contain placeholder content:

1. **`project.md`** — Every field is a placeholder. The project literally has no stated goal, no success criteria, no current phase. An agent reading this within 3 seconds cannot answer "what is this project doing right now." Eight specific placeholders exist: `<project-name>`, `<One sentence>`, 3x `<Criterion N>`, 3x `<measurable outcome>`, `<active | maintenance | paused>`, `<current milestone>`, `<next deliverable>`.

2. **`conventions.md`** — Header reads "Conventions: <project-name>". The "Languages by Purpose" table has a single row with `<TypeScript | Go | Rust | Python>` as options instead of actual values. Agents cannot pick the right language for the job — they see a template option list, not a decision.

3. **`tech-stack.md`** — Header reads "Tech Stack: <project-name>". All verification commands are placeholders (`<tsc --noEmit | mypy | cargo check | go vet>`). The craft references table is structurally broken: lines 80-84 form a complete table with 4 rows (typography, color, anti-ai-slop, animation-discipline), line 85 is an attribution paragraph, and lines 86-88 are orphan table rows with no header (accessibility-baseline, form-validation, typography-hierarchy) — they render as corrupted markdown. Additionally, `design/craft/state-coverage.md` exists on disk but is not listed in the table at all. Six placeholders across header, runtime table, and verification sections.

4. **`decisions.md`** — Five real architecture decisions exist (br/bv for tracking, commands+skills only, bare command names, `.omp/` as native root, tooling in separate repos) but they live under an "Example" heading rather than the "Decision Log" heading. The actual "Decision Log" section contains only a placeholder row with `<YYYY-MM>`, `<what we decided>`, `<why>`, `<High | Medium | Low>`. The header reads "Decisions: <project-name>". The decisions are real — they shaped the project — but they're structurally demoted to examples.

5. **`gotchas.md`** — Header reads "Gotchas: <project-name>". The "Template Bootstrap Gotchas" section mixes 13 gotcha entries: 1 is project-specific (memory templates waste tokens), 12 are template-universal. The section's note says "Replace with your project's actual gotchas" — but for the template repo itself, these ARE the actual gotchas (consumers need them) mixed with maintenance gotchas (the template maintainer needs them).

If we don't fix this, every agent session wastes context on template noise. New contributors can't understand the project's identity from its own memory files. The dogfooding gap undermines the template's credibility — "use our hydration, but we didn't."

### Root Cause Analysis

The root cause is a bootstrap sequencing gap. When the OMP Beads Template was instantiated from its own template, the `/init` hydration phase either was never run on this repo (the template was cloned directly rather than instantiated through `/init`), or was run but the `/init` Python script uses `<!-- TODO: fill in -->` markers for project-specific fields that require human input.

Examining the `/init` command (`.omp/commands/init.md`, lines 186, 308, 316, 323-324, 331, 335, 339, 346, 353, 360, 371, 379-385, 418, 430), the hydration script deliberately leaves `<!-- TODO: fill in -->` markers for: `project_desc` (line 186), backend notes for unknown languages (line 316), frontend language/notes when no framework detected (lines 323-324), scripts notes for Bash (line 331), verification commands for unknown languages (lines 335, 339, 346, 353, 360), security audit for unknown package managers (line 371), success criterion placeholders (lines 379-382), and milestone/next deliverable (lines 384-385).

This means `/init` intentionally leaves some fields as placeholders — it detects what it can from the repo and marks the rest for human completion. The OMP Beads Template repo, being a template with no compiled code, no package.json, no Cargo.toml, and no go.mod, triggers the "unknown" paths for most detections. Result: nearly every field remains a placeholder.

The fix is NOT to change `/init` (which is working as designed) but to manually hydrate the memory files as a project maintainer would — filling in the project-specific fields that `/init` rightly leaves for human judgment.

### Impact Quantification

Counting placeholders across all 5 memory files:

| File | `<project-name>` | `<!-- TODO -->` | `<option1 \| option2>` | Broken structure | Total issues |
|------|------------------|-----------------|------------------------|------------------|-------------|
| project.md | 1 | 7 | 0 | 0 | 8 |
| conventions.md | 1 | 0 | 1 | 0 | 2 |
| tech-stack.md | 1 | 0 | 4 | 1 | 6 |
| decisions.md | 1 | 0 | 0 | 1 | 2 |
| gotchas.md | 1 | 0 | 0 | 0 | 1 |
| **TOTAL** | **5** | **7** | **5** | **2** | **19** |

19 discrete issues across 5 files. Every agent session loads all 19 placeholders. At ~330 tokens per session for this template noise, over 10 sessions that's ~3,300 wasted tokens — and that's conservative since each session typically involves multiple agent turns, each reloading the context.

### Why Now

The design system (19 files, 1,907 lines) was recently scaffolded. The Honcho memory workflow was implemented. The git-clean command was added. The project has accumulated real infrastructure — but its own memory files still claim it's an unnamed project with no goal. This gap widens with every new feature added to the template. Each new addition makes the template more valuable and the missing identity more conspicuous.

### Stakeholders Affected

- **Future agents** working in this repo — every session starts with confusing placeholder noise
- **New contributors** — the README says "OMP Beads Template" but memory files say `<project-name>` — which is authoritative?
- **Template consumers** — if the template can't dogfood its own hydration, why should they trust it?

## Scope

### In Scope

- **`project.md`** — Replace `<project-name>` with "OMP Beads Template". Write a real goal, 3 success criteria, and current phase. Derive from README.md and AGENTS.md patterns — do not invent.
- **`conventions.md`** — Replace `<project-name>`. Fill "Languages by Purpose" table with actual values: Agent instructions = Markdown, Configuration = JSON/YAML, Scripts = Python (init hydration). Backend/Frontend rows = N/A (this is a template repo, not an application).
- **`tech-stack.md`** — Replace `<project-name>`. Fill verification commands with actual working commands (N/A for typecheck/lint/test/build since this is a template repo). Fix broken craft references table: merge all 8 craft files into one contiguous table, place attribution paragraph after the table. Add missing `state-coverage.md` row.
- **`decisions.md`** — Move 5 real decisions from "Example" section to "Decision Log" section with sequential `#`. Keep the "How to Add a Decision" reference section. Remove the "Example" section (content already migrated). Note: these decisions were labeled "Example" during template bootstrap — they are now confirmed as actual architecture decisions.
- **`gotchas.md`** — Replace `<project-name>`. Separate template-specific gotchas from project-specific gotchas. Template gotchas that apply universally to template consumers should be marked as such but kept (they're part of what the template provides). Project-specific gotchas about the OMP Beads Template development itself stay in "Active Warnings."

### Out of Scope

- Not touching `/init` command logic
- Not creating new memory files
- Not touching `DESIGN.md` or `design/` directory
- Not touching `.omp/AGENTS.md`
- Not modifying any command files
- Not modifying `.omp/RULES.md`
- Not running `/git-clean` (separate housekeeping)
- Not changing any `.omp/skills/` files
- Not changing any `.omp/templates/` files
- Not changing `.gitignore` or `README.md`
- Not adding or removing gotchas — only restructuring existing ones
- Not changing the decisions' rationale or content — only their placement in the document

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| 1 | `project.md` has real project identity | MUST | `grep -c '<project-name>' .omp/memory/project/project.md` returns 0. All 8 placeholder fields (project name, goal, 3 criteria, 3 outcomes, status, milestone, next) are filled with concrete text. No `<!-- TODO` markers remain. |
| 2 | `conventions.md` has filled language table | MUST | "Languages by Purpose" table has no `<TypeScript \| Go \| Rust \| Python>` placeholders. All 5 rows filled with actual values or "N/A" for inapplicable rows. Header has real project name. |
| 3 | `tech-stack.md` craft table is structurally valid | MUST | Craft references table renders as valid markdown — all 8 rows in one table with a single header. No orphan rows. Attribution paragraph follows the table. Missing `state-coverage.md` added. |
| 4 | `tech-stack.md` verification commands are real | MUST | Verification commands section contains actual commands or "N/A", not `<tsc \| mypy \| cargo check>` placeholders. Runtime table has real values. |
| 5 | `decisions.md` has decisions in Decision Log | MUST | Five real decisions appear under "## Decision Log" heading with sequential `#` (1-5). No decisions remain under "Example" heading. "Example" section removed. Placeholder row removed. |
| 6 | `gotchas.md` separates template from project gotchas | MUST | Template bootstrap gotchas are clearly labeled as such. Project-specific gotchas about the OMP Beads Template are in "Active Warnings" section. Blockquote note explains template gotchas ship with the template. |
| 7 | No `<project-name>` in any memory file | MUST | `grep -r '<project-name>' .omp/memory/project/` returns no matches. |
| 8 | All memory files remain valid markdown | MUST | Each file parses as valid markdown. Tables render correctly (consistent column counts, header rows present). No orphan rows between tables. |
| 9 | No content loss from existing decisions | SHOULD | All 5 existing decisions' rationale and confidence are preserved verbatim. Only structure changes. |
| 10 | No content loss from existing gotchas | SHOULD | All 13 existing gotcha entries are preserved. Only categorization changes — no text changes. |

## Technical Context

**Key files:**

- `.omp/memory/project/project.md` — EDIT (~29 lines currently, will expand to ~35 lines with real content)
- `.omp/memory/project/conventions.md` — EDIT (~143 lines currently, 2 sections changed: header + Languages table; 3 rows change)
- `.omp/memory/project/tech-stack.md` — EDIT (~88 lines currently, header + runtime table + verification commands + craft table fix; ~10 lines change)
- `.omp/memory/project/decisions.md` — EDIT (~34 lines currently, restructure: Example → Decision Log, remove placeholder row; ~15 lines change)
- `.omp/memory/project/gotchas.md` — EDIT (~44 lines currently, header + separate template/project gotchas; ~8 lines change)

**Existing patterns in use:**

- All memory files use the same frontmatter pattern: `---\npurpose: ...\nupdated: ...\n---`
- Tables use standard markdown pipe syntax with aligned columns
- Memory files follow the conventions.md maintenance rules: update after milestones, keep under 2KB
- Project identity is derived from README.md heading ("OMP Beads Template") and first paragraph: "OMP-native project template with **br** and **bv** as the backbone of planning, execution, verification, and review."
- AGENTS.md describes the project as providing "br as the task tracking backbone and bv for graph-informed planning"

**How these files are consumed:**

- `.omp/AGENTS.md` uses OMP `@` imports to inline `project.md` and `conventions.md` into agent context at session start. These two files are ALWAYS in context.
- `tech-stack.md`, `decisions.md`, and `gotchas.md` are loaded on-demand when an agent references them or when a task touches their domain.
- All five files are read by agents during `/brainstorm`, `/create`, `/plan`, and other phases that need project context.
- The `updated` frontmatter field is used by agents to determine staleness.

**Constraints:**

- **Token budget:** Each memory file should stay under 2KB per conventions.md. Current sizes: project.md ~1KB, conventions.md ~3KB (over budget!), tech-stack.md ~2KB, decisions.md ~1.5KB, gotchas.md ~2KB. The conventions.md overshoot is from the extensive UI Design section — not touched by this bead.
- **Backward compatible:** br, bv, and workflow gate must continue to function — these files are markdown, no structural dependencies. The gate reads `project.md` and `conventions.md` via OMP imports — changing placeholders to real text is a no-op for the import mechanism.
- **No new sections:** Following the template pattern — fill placeholders, don't add new top-level sections. Exceptions: renaming "Example" to nothing (removal), adding blockquote note to "Template Bootstrap Gotchas" (inline annotation, not new section).
- **Preserve existing gotchas:** All 13 gotcha entries must survive — some are project-specific, some are template-universal. None are deleted.
- **Decisions content immutable:** The 5 decisions' text, rationale, and confidence levels are verbatim — only the section heading changes from "## Example" to "## Decision Log".

**Existing code to NOT modify:**

- `.omp/commands/init.md` — the hydration logic that writes these files
- `.omp/templates/prd.md`, `.omp/templates/plan.md`, etc. — template files
- `.omp/skills/` — any skill files
- `.omp/AGENTS.md` — canonical project context; already imports these files
- `.omp/RULES.md` — workflow rules
- `DESIGN.md` — brand contract
- `design/` — all design system files
- `README.md` — project README
- `.gitignore` — ignore rules

## Approach

### File 1: project.md

**Current state (8 placeholders):**
- `# Project: <project-name>` → `# Project: OMP Beads Template`
- `<One sentence — what are we building and why?>` → real goal
- `<Criterion 1>` / `<Criterion 2>` / `<Criterion 3>` → 3 real criteria
- `<measurable outcome>` (x3) → real measurable outcomes
- `<active | maintenance | paused>` → `active`
- `<what we're working toward right now>` → real milestone
- `<the next concrete deliverable>` → real next step

**Target values:**

Goal: "An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating." Derived from README.md ("OMP-native project template with br and bv as the backbone") expanded with concrete deliverables visible in the repo: 9 slash commands, 16 skills, workflow gate extension, design system assets, and memory file templates.

Success Criteria:
1. **Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file** — verifiable with `grep -r '<project-name>' .omp/memory/project/` returning no matches
2. **Every memory file is valid markdown with filled tables** — verifiable by reading each file; no orphan rows, consistent column counts
3. **An agent loading this context can answer "what is this project" within 3 seconds** — qualitative but observable: `project.md` heading + goal must be self-contained

Current Phase:
- Status: active (8 beads closed, design system scaffolded, Honcho workflow added, git-clean command added — active development)
- Milestone: "Memory file hydration — project identity hardening"
- Next: "Audit command files for consistency with conventions.md"

**Edit plan:** Replace 8 placeholder strings with concrete values. Frontmatter `updated` date set to 2026-06-17. No structural changes.

### File 2: conventions.md

**Current state (2 issues):**
- `# Conventions: <project-name>` → `# Conventions: OMP Beads Template`
- Languages by Purpose table: Backend row has `<TypeScript | Go | Rust | Python>`, Frontend has `<TypeScript | JavaScript>`, Scripts has `<Bash | Python | TypeScript>`

**Target values for Languages by Purpose table:**

| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | N/A | Template repo — no backend runtime |
| Frontend | N/A | Template repo — provides design system assets only |
| Scripts | Python | `/init` hydration script (`.omp/commands/init.md` Phase 2.5) |

Rationale for each row:
- **Agent instructions:** Confirmed by file inventory — all skills and commands are `.md` files
- **Configuration:** Confirmed by `.omp/config.yml` existence
- **Backend:** N/A — the template has no server, no runtime, no compiled backend. The only executable code is the TypeScript workflow gate extension and the Python init hydration script, neither of which constitutes a backend.
- **Frontend:** N/A — while the template provides `design/` assets (tokens, primitives, base CSS, craft rules), these are framework-agnostic static assets, not a running frontend application.
- **Scripts:** Python — the `/init` Phase 2.5 Python script is the only build-time/init-time script. The template has no CI scripts, no build scripts, no dev tooling scripts outside OMP commands.

**Edit plan:** Replace header. Replace the 3 placeholder rows in the Languages table. Frontmatter `updated` date set to 2026-06-17. No other changes — the extensive UI Design section (~70 lines) is untouched.

### File 3: tech-stack.md

**Current state (6 issues):**
- `# Tech Stack: <project-name>` → `# Tech Stack: OMP Beads Template`
- Runtime table: Language row has `<TypeScript | Python | Go | Rust>`, `<version>`, `<strict mode? async? experimental flags?>`
- Runtime table: Runtime row has `<Node.js | Bun | Deno | Python 3.x | Go 1.x>`, `<version>`, `<LTS? latest?>`
- Runtime table: Package manager row has `<npm | pnpm | yarn | pip | cargo | go mod>`, `<version>`
- Verification commands: Typecheck, Lint, Test, Build, Security all have `<tsc | mypy | ...>` placeholders
- Craft references table: structurally broken (orphan rows, missing state-coverage.md)

**Target values for Runtime table:**

| Layer | Tool | Version | Notes |
|-------|------|---------|-------|
| Language | N/A | — | Template repo — no application language |
| Runtime | N/A | — | Template repo — no application runtime |
| Package manager | N/A | — | Template repo — no dependencies |
| Task tracking | br (beads_rust) | latest | `which br` — CLI task tracker |
| Graph intelligence | bv (beads_viewer) | latest | `which bv` — robot commands for graph analysis |

The Language/Runtime/Package manager rows are explicitly N/A. This is honest: the template repo has no installed runtime, no package.json, no lockfiles, no compiled code. The only tools it depends on are br and bv (which are external CLI tools, not project dependencies).

**Target values for Verification Commands:**

```bash
# Typecheck
N/A — template repo, no application code

# Lint
N/A — template repo, no application code

# Test
N/A — template repo, no application code

# Build
N/A — template repo, no application code

# Graph state (always available)
bv --robot-triage
br list --status open --status in_progress --json
```

**Target values for Security:**

```bash
# Dependency audit
N/A — template repo, no dependencies to audit

# Secrets scan (if configured)
N/A — no secrets scan configured
```

**Craft references table fix:**

Current broken structure:
```
| File | Purpose |
|------|---------|
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
| `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
| `design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
| `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |
```

Target structure (single contiguous table, attribution after):
```
| File | Purpose |
|------|---------|
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |
| `design/craft/state-coverage.md` | Loading, empty, error, edge-case states; loading skeleton strategy; empty-state copy and illustration rules |
| `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
| `design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
| `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
```

Note: state-coverage.md description derived from reading the actual file at `design/craft/state-coverage.md`.

**Edit plan:** Replace header. Replace runtime table rows with N/A. Replace verification/security command placeholders with N/A. Merge craft table rows into one contiguous table. Add missing state-coverage.md row. Move attribution paragraph after table. Frontmatter `updated` date set to 2026-06-17.

### File 4: decisions.md

**Current state (2 issues):**
- `# Decisions: <project-name>` → `# Decisions: OMP Beads Template`
- 5 real decisions under "## Example" heading; "## Decision Log" has a placeholder row

**Target structure:**

```
# Decisions: OMP Beads Template

Every architecture decision that affects the shape of the project goes here.
Use the table. Dates, rationale, and confidence are required.

## Decision Log

| # | Date | Decision | Rationale | Confidence |
|---|------|----------|-----------|------------|
| 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator. Alternatives (linear, plain markdown) lack the graph query ability. | High |
| 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts and skill knowledge. Scripts add maintenance burden, platform dependencies, and hidden logic. | High |
| 3 | 2026-06 | Bare command names (`/create`, `/plan`) | OMP resolves commands by directory. Prefix would be noise. | High |
| 4 | 2026-06 | `.omp/` as native project root | OMP loads from `.omp/`. Parallel `.pi/` config creates confusion. | High |
| 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages. The beads template stays pure workflow — install providers separately. | High |

## How to Add a Decision

... (kept as-is)
```

**Edit plan:** Replace header. Replace "## Decision Log" placeholder row with 5 real rows from "## Example". Remove "## Example" section entirely. Keep "## How to Add a Decision" as-is. Frontmatter `updated` date set to 2026-06-17.

### File 5: gotchas.md

**Current state (1 structural issue):**
- `# Gotchas: <project-name>` → `# Gotchas: OMP Beads Template`
- 13 gotchas all under "Template Bootstrap Gotchas" — 1 project-specific, 12 template-universal

**Classification of existing 13 gotchas:**

Project-specific (move to "Active Warnings"):
1. "Memory templates waste tokens if left as placeholders" — this is the problem this bead fixes; specific to the OMP Beads Template's own maintenance

Template-universal (keep in "Template Bootstrap Gotchas"):
2. "workflow gate only understands the active bead if br list works"
3. "gate blocks edit and write but shell bypasses it"
4. "Implementing without a bead or plan"
5. "Assuming requirements without reading PRD"
6. "Commands are prompt templates, not compiled code"
7. "OMP loads from .omp/ — moving files to .pi/ stops native discovery"
8. "bv requires git history — robot commands return empty until at least one commit"
9. "bv requires br data — robot commands need .beads/ database"
10. "Stale memory is worse than no memory"
11. "Lazy/small models skip steps, assume context, don't follow workflow"
12. "Loading domain-specific skills in the wrong project wastes context"

**Target structure:**

```
# Gotchas: OMP Beads Template

Every entry must include impact and mitigation. A gotcha without a mitigation is just a complaint.

## Active Warnings

| Date | Area | Gotcha | Impact | Mitigation |
|------|------|--------|--------|------------|
| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session | Fill with real project content immediately. Delete placeholder gotchas when real ones exist. |

## Template Bootstrap Gotchas

> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.

| Date | Area | Gotcha | Impact | Mitigation |
|... (12 entries verbatim) ...

## How to Add a Gotcha

... (kept as-is)
```

**Edit plan:** Replace header. Extract project-specific gotcha (#1) into "Active Warnings" table. Keep 12 template-universal gotchas in "Template Bootstrap Gotchas" with a blockquote note. Frontmatter `updated` date set to 2026-06-17.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Decisions were labeled "Example" intentionally — they may be provisional | Low | Medium | The 5 decisions span 2026-06, match actual architecture, and are cited in conventions.md. If they were provisional, they'd have been replaced by now. Verify each decision matches current repo state before promoting. Plan B: if any decision is contested, revert that row to "Example" and only promote confirmed ones. |
| Craft table fix breaks something parsing the tech-stack.md file | Low | Low | This is a markdown file consumed by humans and agents. No tool parses its structure. The fix only rearranges existing rows — no content is lost. Plan B: if any tool does depend on the broken structure, the fix makes it MORE parseable, not less. |
| Removing "Example" section loses reference pattern for future decisions | Low | Low | The "How to Add a Decision" section remains — it provides the pattern with the same table columns. The Example section was redundant with Decision Log. |
| Gotcha recategorization moves something important to wrong section | Low | Low | All gotchas are preserved. Categorization only affects which section they appear in — both sections are read by agents. If wrong, it's one `edit` to move a row between tables. |
| Project goal is opinionated — might not match maintainer intent | Medium | Low | Derive goal from README.md (canonical project description) and AGENTS.md (workflow philosophy). If wrong, it's one line to change. The goal is descriptive ("provides workflow infrastructure") not aspirational ("revolutionizes development"). |
| `conventions.md` token budget overshoot goes unnoticed | Low | Low | conventions.md is already ~3KB (over the 2KB budget) due to the extensive UI Design section. This bead adds ~20 characters (project name). The overshoot predates this bead and is not addressed here — it's a separate concern. |
| `N/A` in verification commands prevents future agents from running checks | Low | Low | The template repo genuinely has no code to typecheck/lint/test/build. An "N/A" is honest and prevents agents from fabricating verification commands. When/if code is added to the template, the tech-stack.md should be updated in that bead. |

## Verification Plan

After implementing all 5 file edits, run these verification checks:

### Automated checks

```bash
# Check 1: No <project-name> anywhere
grep -r '<project-name>' .omp/memory/project/
# Expected: no output (exit code 1)

# Check 2: No TODO markers in project.md
grep '<!-- TODO' .omp/memory/project/project.md
# Expected: no output (exit code 1)

# Check 3: Decisions have 5 numbered rows in Decision Log
grep -c '^| [1-5] |' .omp/memory/project/decisions.md
# Expected: 5

# Check 4: No "Example" heading in decisions.md
grep -c '## Example' .omp/memory/project/decisions.md
# Expected: 0

# Check 5: Craft table has all 8 files
grep -c 'design/craft/' .omp/memory/project/tech-stack.md
# Expected: 8 (one per craft file)

# Check 6: No orphan table rows in tech-stack.md
# Read the file and verify no table rows appear outside a table context

# Check 7: Gotchas has "Active Warnings" and "Template Bootstrap Gotchas" sections
grep -c '## Active Warnings' .omp/memory/project/gotchas.md
# Expected: 1
grep -c '## Template Bootstrap Gotchas' .omp/memory/project/gotchas.md
# Expected: 1

# Check 8: Gotchas has blockquote note
grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md
# Expected: 1
```

### Manual checks

- Read each of the 5 files end-to-end. Verify:
  - All tables render correctly (consistent column counts, headers present)
  - No orphan rows between tables
  - Frontmatter `updated` dates are all 2026-06-17
  - No placeholder text remains in any file
  - "Languages by Purpose" table in conventions.md has N/A for Backend/Frontend
  - Runtime table in tech-stack.md has N/A for Language/Runtime/Package manager
  - Verification commands in tech-stack.md say N/A for all code checks
  - The 5 decisions' text matches the original verbatim

### Integration check

```bash
# Verify br still works with the updated files
br list --status open --json
bv --robot-triage --format json
```

These commands don't read memory files directly, but they validate that no structural change broke the bead database or graph analysis.

## Acceptance Criteria

- [ ] `project.md` has real content in all 8 placeholder fields
    - Verify: `grep '<project-name>' .omp/memory/project/project.md` returns nothing. `grep '<!-- TODO' .omp/memory/project/project.md` returns nothing. Read file — goal, 3 criteria, 3 outcomes, status, milestone, next are all concrete text.

- [ ] `conventions.md` has filled language table with N/A for inapplicable rows
    - Verify: No `<TypeScript | Go | Rust | Python>` pattern in the languages table. Backend row says "N/A", Frontend row says "N/A", Scripts row says "Python". Header says "OMP Beads Template".

- [ ] `tech-stack.md` craft table has 8 contiguous rows with one header
    - Verify: All 8 craft files appear in a single markdown table. No orphan rows. Attribution paragraph follows the table, not sits between rows. `grep -c 'design/craft/' .omp/memory/project/tech-stack.md` returns 8.

- [ ] `tech-stack.md` verification commands are N/A for code checks
    - Verify: Typecheck, Lint, Test, Build, Security, Dependency audit all say "N/A". Graph state commands preserved.

- [ ] `decisions.md` has 5 decisions in Decision Log
    - Verify: `grep -c '^| [1-5] |' .omp/memory/project/decisions.md` returns 5. No "Example" heading in file. "Decision Log" heading has 5 real rows.

- [ ] `gotchas.md` has separated template/project gotchas with blockquote note
    - Verify: "Active Warnings" table has 1 project-specific gotcha. "Template Bootstrap Gotchas" table has 12 entries with blockquote note. Header says "OMP Beads Template".

- [ ] No `<project-name>` anywhere in memory files
    - Verify: `grep -r '<project-name>' .omp/memory/project/` returns no matches (exit code 1, 0 lines).

- [ ] All memory files are valid markdown
    - Verify: Read each file — tables have consistent column counts, no orphan rows, headers present. No broken table fragments.

- [ ] No content loss from existing decisions
    - Verify: Each of the 5 decisions (br/bv, commands+skills, bare names, .omp/ root, tooling separate) appears verbatim with same rationale and confidence in the Decision Log.

- [ ] br and bv still function
    - Verify: `br list --status open --json` succeeds. `bv --robot-triage --format json` succeeds.

- [ ] Bead artifacts pass quality self-check
    - Verify: `wc -l .beads/artifacts/br-omp-backbone-skill-l3d/prd.md` ≥ 600 lines.

## Impact Assessment

**Before (current state):**
- 5 memory files loaded per session
- 19 placeholder issues across files
- ~330 tokens of template noise per session
- Agents cannot answer "what is this project" from memory files
- decisions.md has real decisions demoted to "Example"
- tech-stack.md has broken markdown table

**After (target state):**
- 5 memory files loaded per session — same count, but all content is real
- 0 placeholder issues across files
- 0 tokens of template noise
- Agents can answer "what is this project" from project.md alone
- decisions.md has real decisions in their proper home
- tech-stack.md has valid table structure

**Files changed:** 5 (all in `.omp/memory/project/`)
**Lines changed:** ~40 lines across 5 files
**Risk to existing functionality:** Zero — these are markdown documentation files with no code dependencies
**Blast radius:** `.omp/memory/project/` only — no other directories touched

## Design Decisions

### Decision 1: N/A over "None" or empty cells

**Choice:** Use "N/A" for inapplicable rows in language/runtime/verification tables.
**Rationale:** "None" could be misread as "not configured" (implying it SHOULD be configured). An empty cell looks like a rendering error. "N/A" is unambiguous — "not applicable to this project."
**Alternatives considered:** Leaving cells empty (ambiguous), removing rows entirely (loses the table structure that template consumers expect).

### Decision 2: "Template repo" as the explanation for every N/A

**Choice:** Every N/A in tech-stack.md includes the note "Template repo — no application code/runtime/dependencies."
**Rationale:** An agent reading "N/A" alone might try to detect the stack. An agent reading "Template repo — no backend runtime" understands WHY it's N/A and stops looking. This prevents agents from fabricating stack decisions.

### Decision 3: Blockquote note for template bootstrap gotchas

**Choice:** Add a `> These gotchas ship with...` blockquote note before the Template Bootstrap Gotchas table.
**Rationale:** The previous note was a paragraph ABOVE the section saying "Replace with your project's actual gotchas." This is confusing in the template repo itself — are we supposed to replace our own gotchas? The blockquote clarifies: these ship WITH the template, consume them if you're using it; replace them if you're a consumer. The template maintainer (this repo) keeps them because they're part of the deliverable.
**Alternatives considered:** Moving template gotchas to a separate file (adds complexity — one more file to maintain), deleting them (loses institutional knowledge that template consumers need).

### Decision 4: State-coverage.md purpose derived from file content

**Choice:** Read `design/craft/state-coverage.md` to derive a one-line purpose for the craft table.
**Rationale:** All other craft files have purpose descriptions in the table. The missing `state-coverage.md` row needs one. Rather than inventing, read the file's first paragraph or heading to extract a purpose.

### Decision 5: Frontmatter `updated` date set to 2026-06-17 for all 5 files

**Choice:** Set `updated: 2026-06-17` in all 5 memory file frontmatters.
**Rationale:** All 5 files are being modified in this bead on 2026-06-17. The `updated` field should reflect the last modification date. Agents use this to determine staleness.
**Alternatives considered:** Updating only files with substantive changes (but the header change in gotchas.md IS a substantive change — the project name is part of the file's identity).

## Edge Cases

### Edge Case 1: What if a future maintainer adds a backend to the template?

If the OMP Beads Template ever gains a backend (e.g., a build script, a CI server, a web dashboard), the conventions.md and tech-stack.md should be updated in that bead. The current "N/A" values are accurate for the current state — they're not permanent declarations.

### Edge Case 2: What if a 6th architecture decision is made?

The decisions.md "How to Add a Decision" section provides the pattern. The next decision gets `# 6`. The 5 existing decisions keep their numbers. The placeholder row in Decision Log is gone — future beads add rows, they don't replace placeholders.

### Edge Case 3: What if a gotcha is discovered that's both project-specific AND template-universal?

If a gotcha applies to both contexts, it goes in "Template Bootstrap Gotchas" (broader audience) with a note in "Active Warnings" cross-referencing it. The project-specific section is for gotchas that ONLY apply to the template's own maintenance.

### Edge Case 4: What if the token budget constraint is violated?

The conventions.md is already ~3KB (over the 2KB budget) due to the UI Design section. This bead adds ~20 characters. If the budget is a hard constraint, the UI Design section should be moved to DESIGN.md or a separate file — but that's out of scope for this bead. The current approach (exceed budget for good reason) is acceptable per the gotcha "Stale memory is worse than no memory."

### Edge Case 5: What if grep matches a false positive?

`grep -r '<project-name>' .omp/memory/project/` could match if `<project-name>` appears in a code example or documentation within a memory file. But the files don't contain code examples that reference `<project-name>` — they use it as a literal placeholder. If a false positive occurs (unlikely), inspect the match manually.

## Implementation Order

The five files are independent — they can be edited in any order. However, the following sequence minimizes re-reads:

1. **project.md** — establishes project identity; all other files reference "OMP Beads Template"
2. **conventions.md** — language table; completes the core identity files (project + conventions are always in context)
3. **tech-stack.md** — most complex edit (header + runtime + verification + craft table fix); requires reading state-coverage.md for the purpose description
4. **decisions.md** — pure restructure; no content changes, only section moves
5. **gotchas.md** — pure recategorization; no content changes, one row moves between tables

This order means the simpler files (project.md, conventions.md) build confidence before the complex tech-stack.md edit, and the content-preserving restructures (decisions.md, gotchas.md) come last when the agent is most familiar with the files.

## Rollback Plan

If any edit produces incorrect output:
1. Each file's original state is preserved in git (`git diff .omp/memory/project/` shows all changes)
2. Individual file rollback: `git checkout -- .omp/memory/project/<file>.md`
3. Full rollback: `git checkout -- .omp/memory/project/`
4. The bead's PRD and decisions artifacts remain valid regardless of implementation outcome

No database state, no compiled code, no external dependencies — rollback is a single git command.

## Notes for the Implementing Agent

1. **Read before edit.** For each file, read the current content before making changes. Confirm the line numbers and placeholders match what this PRD documents — the files may have been modified since this PRD was written.

2. **Use exact string replacement.** The placeholders are literal strings. Use `edit` tool with exact `SWAP` operations. For tables, replace the entire row rather than individual cells — this avoids column misalignment.

3. **Verify after each file.** After editing each file, run the corresponding grep check from the Verification Plan before moving to the next file. Catching errors early prevents cascading mistakes.

4. **Do not reformat.** The files have existing table alignment (padded columns with spaces). Preserve the alignment. Only change the placeholder text — do not reflow tables or adjust whitespace.

5. **state-coverage.md purpose.** Before editing tech-stack.md, read `design/craft/state-coverage.md` to extract a one-line purpose description for the craft table. The purpose should match the pattern of other craft file descriptions: ~5-10 words describing what the file covers.

6. **Commit atomically.** After all 5 files are edited and verified, create a single commit: `chore: hydrate memory files with project identity`. Do not commit each file separately — this is one logical change.

7. **Run the integration checks.** After committing, run `br list --status open --json` and `bv --robot-triage --format json` to confirm no structural breakage.

8. **Update progress.** After implementation, update this bead's status and prepare for `/verify`.

## Open Questions

1. **Should the "Template Bootstrap Gotchas" be extracted to a separate file for template consumers?** Currently they're mixed in gotchas.md. If a consumer clones the template, they get the template gotchas in their gotchas.md. If the template maintainer adds a project-specific gotcha, the consumer won't get it (they'll have replaced the gotchas with their own). This is acceptable — consumers are expected to replace template gotchas. But it's worth considering whether a `gotchas.template.md` file would be cleaner. **Decision deferred** — out of scope for this bead.

2. **Should conventions.md's UI Design section be split out?** The section is ~70 lines (over half the file) and covers design system rules that only apply if the project uses the design system. For non-UI projects, this is noise. **Decision deferred** — out of scope.

3. **Should there be a `/hydrate` command that re-runs init detection?** Currently, if the repo gains a new dependency (e.g., package.json is added), the memory files don't auto-update. A hydration command would detect changes and fill newly-detectable fields. **Decision deferred** — YAGNI until there's a concrete use case.
