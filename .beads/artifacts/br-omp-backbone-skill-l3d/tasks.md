# Tasks: br-omp-backbone-skill-l3d

## Task Metadata

| Task | Complexity | Risk | Parallel Safe? | Rollback Cost | Files Touched |
|------|-----------|------|----------------|---------------|---------------|
| 1.1 project.md | Low | Low | Yes | Trivial (`git checkout`) | 1 |
| 1.2 conventions.md | Low | Low | Yes | Trivial (`git checkout`) | 1 |
| 1.3 tech-stack.md | Medium | Low | Yes | Trivial (`git checkout`) | 2 (edit + read) |
| 1.4 decisions.md | Low | Low | Yes | Trivial (`git checkout`) | 1 |
| 1.5 gotchas.md | Low | Low | Yes | Trivial (`git checkout`) | 1 |
| 2.1 verification | Low | Low | No | N/A (read-only) | 5 (read) |
| 3.1 commit | Low | Low | No | Trivial (`git reset`) | 6 (5 edit + .beads) |

## Pre-Flight Checklist

Before starting ANY task, confirm:

- [ ] `.beads/artifacts/br-omp-backbone-skill-l3d/prd.md` exists and has ≥600 lines
- [ ] `.beads/artifacts/br-omp-backbone-skill-l3d/plan.md` exists and has ≥600 lines
- [ ] Bead `br-omp-backbone-skill-l3d` is open: `br show br-omp-backbone-skill-l3d --json` shows status "open"
- [ ] No uncommitted changes in `.omp/memory/project/`: `git diff .omp/memory/project/` is empty for files not yet edited (other files may have pre-existing changes)
- [ ] Working directory is at repo root: `pwd` shows `/home/ryan/repos/omp-template`

## Common Edit Operations Reference

### Reading a file before editing

```
read .omp/memory/project/<file>.md
```

Always read the file first to confirm current content matches the documented state. If the file has been modified since the PRD was written, adapt the edit to the current state — only replace placeholders that still exist, skip already-filled ones.

### Replacing a single placeholder string

Use the `edit` tool with `SWAP` to replace the exact placeholder string with the target value. Always match the exact string — including angle brackets `<>`, pipes `|`, and whitespace. For table cells, replace the entire cell content, not just the placeholder tokens.

Example:
```
SWAP 6.=6:
+ # Project: OMP Beads Template
```

This replaces line 6 (which contains `# Project: <project-name>`) with the new line.

### Verifying a replacement

After each replacement:
```bash
grep "OLD_STRING" .omp/memory/project/<file>.md    # Should return nothing (exit 1)
grep "NEW_STRING" .omp/memory/project/<file>.md    # Should return at least 1 match
```

### Rolling back a single file

```bash
git checkout -- .omp/memory/project/<file>.md
```

### Checking file state before editing

```bash
# See what placeholders exist
grep -n '<project-name>\|<Criterion\|<measurable\|TODO\|<active \|' .omp/memory/project/project.md

# See the current language table
grep -A5 'Languages by Purpose' .omp/memory/project/conventions.md

# See the current craft table
grep -n 'design/craft/' .omp/memory/project/tech-stack.md

# See the current decision sections
grep -n 'Decision Log\|Example\|How to Add' .omp/memory/project/decisions.md

# See the current gotcha sections
grep -n 'Active Warnings\|Template Bootstrap\|How to Add' .omp/memory/project/gotchas.md
```

## Task Execution Order Rationale

Although all 5 Wave 1 tasks are parallel-safe (different files, no shared state), the recommended sequential order is:

1. **project.md first** — establishes the project identity ("OMP Beads Template") that other files reference. Also the simplest edit — 11 literal string replacements. Builds confidence.
2. **conventions.md second** — completes the core identity pair (project + conventions are always loaded in agent context by OMP imports). 7 replacements in the language table.
3. **tech-stack.md third** — most complex edit: header fix, runtime table fix, verification command fix, AND structural craft table fix. Do this when you're familiar with the edit patterns from tasks 1 and 2.
4. **decisions.md fourth** — pure restructure with content preservation. Lower cognitive load after the complex edit. Only 3 operations: replace header, promote decisions, delete Example section.
5. **gotchas.md fifth** — pure recategorization. Fastest and simplest. 5 operations: replace header, fill active warning, remove from template, add blockquote, update frontmatter.

## 1. Wave 1: File Edits (all parallel)

All five tasks in this wave edit different files with no inter-dependencies. They can execute in any order, including simultaneously if using parallel agents.

### 1.1 Edit project.md — fill project identity

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/project.md"]
estimated_minutes: 5
risk: Low
rollback: "git checkout -- .omp/memory/project/project.md"
pre_checks:
  - "grep '<project-name>' .omp/memory/project/project.md  # Should match (placeholder exists)"
  - "grep '<!-- TODO' .omp/memory/project/project.md       # Should match 7 times"
post_checks:
  - "grep '<project-name>' .omp/memory/project/project.md  # Should return nothing"
  - "grep '<!-- TODO' .omp/memory/project/project.md       # Should return nothing"
  - "grep 'OMP Beads Template' .omp/memory/project/project.md  # Should match once"
```

**What this task does:** Replace all 11 placeholder strings in project.md with real content describing the OMP Beads Template.

**Why this order:** First task — establishes the project identity that all other files reference. Also the simplest edit (literal string replacements) — good for building momentum.

**Before:**
```
# Project: <project-name>
## The Goal
<One sentence — what are we building and why?>
## Success Criteria
1. **<Criterion 1>** — <measurable outcome>
2. **<Criterion 2>** — <measurable outcome>
3. **<Criterion 3>** — <measurable outcome>
## Current Phase
- **Status:** <active | maintenance | paused>
- **Milestone:** <what we're working toward right now>
- **Next:** <the next concrete deliverable>
```

**After:**
```
# Project: OMP Beads Template
## The Goal
An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating.
## Success Criteria
1. **Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file** — `grep -r '<project-name>' .omp/memory/project/` returns no matches
2. **Every memory file is valid markdown with filled tables** — Read each file — tables have consistent columns, no orphan rows
3. **An agent loading this context can answer what this project is within 3 seconds** — `project.md` heading + goal is self-contained and understandable
## Current Phase
- **Status:** active
- **Milestone:** Memory file hydration — project identity hardening
- **Next:** Audit command files for consistency with conventions.md
```

**Steps:**

- [ ] Read `.omp/memory/project/project.md` — confirm all 11 placeholders exist as documented above
- [ ] Replace `# Project: <project-name>` → `# Project: OMP Beads Template`
- [ ] Replace `<One sentence — what are we building and why?>` → full goal text (see After section above)
- [ ] Replace `<Criterion 1>` → "Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file"
- [ ] Replace `<Criterion 2>` → "Every memory file is valid markdown with filled tables"
- [ ] Replace `<Criterion 3>` → "An agent loading this context can answer what this project is within 3 seconds"
- [ ] Replace first `<measurable outcome>` → "`grep -r '<project-name>' .omp/memory/project/` returns no matches"
- [ ] Replace second `<measurable outcome>` → "Read each file — tables have consistent columns, no orphan rows"
- [ ] Replace third `<measurable outcome>` → "`project.md` heading + goal is self-contained and understandable"
- [ ] Replace `<active | maintenance | paused>` → `active`
- [ ] Replace `<what we're working toward right now>` → "Memory file hydration — project identity hardening"
- [ ] Replace `<the next concrete deliverable>` → "Audit command files for consistency with conventions.md"
- [ ] Update frontmatter `updated:` date to `2026-06-17`
- [ ] Verify: `grep '<project-name>' .omp/memory/project/project.md` returns no output (exit code 1)
- [ ] Verify: `grep '<!-- TODO' .omp/memory/project/project.md` returns no output (exit code 1)
- [ ] Verify: `grep -c 'OMP Beads Template' .omp/memory/project/project.md` returns 1
- [ ] Verify: `grep -c 'br/bv-powered workflow infrastructure' .omp/memory/project/project.md` returns 1
- [ ] Verify: `grep -c 'Memory file hydration' .omp/memory/project/project.md` returns 1
- [ ] Verify: Read file end-to-end — confirm all 11 placeholders have been replaced, all fields have real content

**Error handling:**
- If a placeholder has already been filled (grep returns no match for the placeholder), skip that replacement and note it. The file may have been manually edited.
- If a replacement introduces a formatting error (e.g., table misalignment), roll back with `git checkout -- .omp/memory/project/project.md` and re-edit with corrected alignment.
- If the frontmatter `updated:` field uses a different format (e.g., `updated: "2026-06-17"` with quotes), match the existing format.

### 1.2 Edit conventions.md — fill language table

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/conventions.md"]
estimated_minutes: 5
risk: Low
rollback: "git checkout -- .omp/memory/project/conventions.md"
pre_checks:
  - "grep '<project-name>' .omp/memory/project/conventions.md                    # Should match"
  - "grep '<TypeScript | Go | Rust | Python>' .omp/memory/project/conventions.md # Should match"
  - "grep '<Bash | Python | TypeScript>' .omp/memory/project/conventions.md       # Should match"
post_checks:
  - "grep '<TypeScript | Go | Rust | Python>' .omp/memory/project/conventions.md  # Should return nothing"
  - "grep 'N/A' .omp/memory/project/conventions.md                                 # Should match ≥2 times"
  - "grep 'Python.*init.*hydration' .omp/memory/project/conventions.md             # Should match once"
  - "grep 'OMP Beads Template' .omp/memory/project/conventions.md                  # Should match once"
```

**What this task does:** Replace the project name in the header and fill the "Languages by Purpose" table with actual values. Backend and Frontend rows become N/A (template repo). Scripts row becomes Python (init hydration script).

**Why this order:** Second task — completes the core identity pair. Project.md + conventions.md are the two files always loaded in agent context via OMP imports. Getting both done early means all subsequent agent context loads will see real identity.

**Before (Languages by Purpose table):**
```
| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | <TypeScript | Go | Rust | Python> | <strict? Bun? Deno?> |
| Frontend | <TypeScript | JavaScript> | <React? Svelte? plain?> |
| Scripts | <Bash | Python | TypeScript> | <CI, dev tooling, one-offs> |
```

**After (Languages by Purpose table):**
```
| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | N/A | Template repo — no backend runtime |
| Frontend | N/A | Template repo — provides design system assets only |
| Scripts | Python | `/init` hydration script |
```

**Steps:**

- [ ] Read `.omp/memory/project/conventions.md` — confirm "Languages by Purpose" table exists with placeholder rows as shown above
- [ ] Replace `# Conventions: <project-name>` → `# Conventions: OMP Beads Template`
- [ ] Replace Backend language cell: `<TypeScript | Go | Rust | Python>` → `N/A`
- [ ] Replace Backend notes cell: `<strict? Bun? Deno?>` → `Template repo — no backend runtime`
- [ ] Replace Frontend language cell: `<TypeScript | JavaScript>` → `N/A`
- [ ] Replace Frontend notes cell: `<React? Svelte? plain?>` → `Template repo — provides design system assets only`
- [ ] Replace Scripts language cell: `<Bash | Python | TypeScript>` → `Python`
- [ ] Replace Scripts notes cell: `<CI, dev tooling, one-offs>` → `` `/init` hydration script ``
- [ ] Update frontmatter `updated:` date to `2026-06-17`
- [ ] Verify: Agent instructions row is UNCHANGED (Markdown)
- [ ] Verify: Configuration row is UNCHANGED (JSON / YAML)
- [ ] Verify: `grep '<TypeScript | Go | Rust | Python>' .omp/memory/project/conventions.md` returns no output
- [ ] Verify: `grep '<Bash | Python | TypeScript>' .omp/memory/project/conventions.md` returns no output
- [ ] Verify: `grep -c 'N/A' .omp/memory/project/conventions.md` returns ≥2 (backend + frontend)
- [ ] Verify: `grep 'Python.*init.*hydration' .omp/memory/project/conventions.md` returns 1 match
- [ ] Verify: `grep 'OMP Beads Template' .omp/memory/project/conventions.md` returns 1 match (header)
- [ ] Verify: Read file — confirm table has 5 rows, all filled, consistent column alignment

**Error handling:**
- If the Backend/Frontend/Scripts rows use different cell separators or whitespace, match the existing format exactly.
- The "Notes" column may contain pipe characters (`|`) — ensure the table row uses proper escaping or avoids pipes in the Notes cell.
- If the file has additional rows in the table beyond the 5 documented rows, preserve them and only edit the 3 placeholder rows.

### 1.3 Edit tech-stack.md — fix craft table, fill placeholders

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/tech-stack.md"]
estimated_minutes: 10
risk: Low
rollback: "git checkout -- .omp/memory/project/tech-stack.md"
pre_checks:
  - "grep '<project-name>' .omp/memory/project/tech-stack.md                            # Should match"
  - "grep '<TypeScript | Python | Go | Rust>' .omp/memory/project/tech-stack.md         # Should match"
  - "grep '<tsc --noEmit | mypy | cargo check | go vet>' .omp/memory/project/tech-stack.md  # Should match"
  - "grep -c 'design/craft/' .omp/memory/project/tech-stack.md                          # Should be 7 (missing state-coverage)"
  - "ls design/craft/state-coverage.md                                                  # Should exist"
post_checks:
  - "grep '<TypeScript | Python | Go | Rust>' .omp/memory/project/tech-stack.md         # Should return nothing"
  - "grep '<tsc --noEmit' .omp/memory/project/tech-stack.md                              # Should return nothing"
  - "grep -c 'design/craft/' .omp/memory/project/tech-stack.md                          # Should be 8"
  - "grep 'N/A.*template repo' .omp/memory/project/tech-stack.md                         # Should match ≥5 times"
  - "grep 'OMP Beads Template' .omp/memory/project/tech-stack.md                         # Should match once"
```

**What this task does:** This is the most complex edit — it fixes the header, runtime table (3 rows), verification commands (5 placeholders), security audit (1 placeholder), AND the structurally broken craft table (merge 7+1 rows, move attribution).

**Why this order:** Third task — do this when you're familiar with the edit patterns from tasks 1.1 and 1.2. The craft table fix requires reading an additional file (`design/craft/state-coverage.md`) and structural table surgery.

**Required pre-read:** Before editing, read `design/craft/state-coverage.md` to extract a one-line purpose description for the craft table. The description should match the pattern of existing craft file descriptions (~5-10 words describing what the file covers).

**Steps — Part A: Header + Runtime Table:**

- [ ] Read `.omp/memory/project/tech-stack.md` — confirm placeholders and broken craft table
- [ ] Read `design/craft/state-coverage.md` — extract one-line purpose description
- [ ] Replace `# Tech Stack: <project-name>` → `# Tech Stack: OMP Beads Template`
- [ ] Replace Language row language cell: `<TypeScript | Python | Go | Rust>` → `N/A`
- [ ] Replace Language row version cell: `<version>` → `—`
- [ ] Replace Language row notes cell: `<strict mode? async? experimental flags?>` → `Template repo — no application language`
- [ ] Replace Runtime row runtime cell: `<Node.js | Bun | Deno | Python 3.x | Go 1.x>` → `N/A`
- [ ] Replace Runtime row version cell: `<version>` → `—`
- [ ] Replace Runtime row notes cell: `<LTS? latest?>` → `Template repo — no application runtime`
- [ ] Replace Package manager row manager cell: `<npm | pnpm | yarn | pip | cargo | go mod>` → `N/A`
- [ ] Replace Package manager row version cell: `<version>` → `—`

**Steps — Part B: Verification Commands:**

- [ ] Replace Typecheck placeholder: `<tsc --noEmit | mypy | cargo check | go vet>` → `N/A — template repo, no application code`
- [ ] Replace Lint placeholder: `<eslint | ruff | clippy | golangci-lint>` → `N/A — template repo, no application code`
- [ ] Replace Test placeholder: `<vitest run | pytest | cargo test | go test ./...>` → `N/A — template repo, no application code`
- [ ] Replace Build placeholder: `<tsup | pip install -e . | cargo build --release | go build>` → `N/A — template repo, no application code`
- [ ] Replace Dependency audit placeholder: `<npm audit | pip-audit | cargo audit | govulncheck>` → `N/A — template repo, no dependencies`

**Steps — Part C: Craft Table Fix:**

The current craft table has lines ~78-89 in this structure:

```
78: ## Craft References
79: | File | Purpose |
80: |------|---------|
81: | `design/craft/typography.md` | Type scale, ... |
82: | `design/craft/color.md` | Palette structure, ... |
83: | `design/craft/anti-ai-slop.md` | Seven cardinal sins, ... |
84: | `design/craft/animation-discipline.md` | When motion earns its place, ... |
85: (blank line)
86: Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
87: | `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, ... |
88: | `design/craft/form-validation.md` | Input state machine, ... |
89: | `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, ... |
```

The problem: lines 87-89 are orphan table rows (no header) because the attribution paragraph on line 86 breaks the table. Plus state-coverage.md is missing.

Fix: Merge into one contiguous table:

```
78: ## Craft References
79: | File | Purpose |
80: |------|---------|
81: | `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
82: | `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
83: | `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
84: | `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |
85: | `design/craft/state-coverage.md` | {purpose from reading the file} |
86: | `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
87: | `design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
88: | `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |
89:
90: Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
```

- [ ] Insert state-coverage.md row after animation-discipline.md (line 84)
- [ ] Merge orphan rows 87-89 into the table above (remove blank line 85, move attribution to line 90)
- [ ] Verify: `grep -c 'design/craft/' .omp/memory/project/tech-stack.md` returns 8
- [ ] Verify: Attribution paragraph ("Adapted from Open Design...") comes AFTER all 8 table rows, not between them

**Steps — Part D: Final Verification:**

- [ ] Update frontmatter `updated:` date to `2026-06-17`
- [ ] Verify: `grep '<TypeScript | Python | Go | Rust>' .omp/memory/project/tech-stack.md` returns no output
- [ ] Verify: `grep '<tsc --noEmit | mypy | cargo check | go vet>' .omp/memory/project/tech-stack.md` returns no output
- [ ] Verify: `grep '<npm audit | pip-audit | cargo audit | govulncheck>' .omp/memory/project/tech-stack.md` returns no output
- [ ] Verify: `grep -c 'N/A.*template repo' .omp/memory/project/tech-stack.md` returns ≥5
- [ ] Verify: `grep -c 'design/craft/' .omp/memory/project/tech-stack.md` returns 8
- [ ] Verify: `grep 'OMP Beads Template' .omp/memory/project/tech-stack.md` returns 1 match
- [ ] Verify: Read file — craft table is one contiguous table, attribution paragraph after, no code verification placeholder strings remain

**Error handling:**
- If `design/craft/state-coverage.md` doesn't exist or is empty, use a reasonable fallback: "Loading, empty, error, and edge-case state handling patterns"
- If the craft table has been restructured (different line numbers), adapt the fix to the current structure. The invariant is: all craft files in one table, attribution after.
- If the Runtime table has additional columns or different alignment, match the existing format.

### 1.4 Edit decisions.md — promote decisions to Decision Log

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/decisions.md"]
estimated_minutes: 5
risk: Low
rollback: "git checkout -- .omp/memory/project/decisions.md"
pre_checks:
  - "grep '<project-name>' .omp/memory/project/decisions.md       # Should match"
  - "grep '## Example' .omp/memory/project/decisions.md           # Should match"
  - "grep '<YYYY-MM>' .omp/memory/project/decisions.md            # Should match (placeholder in Decision Log)"
  - "grep 'br/bv for task tracking' .omp/memory/project/decisions.md  # Should match (in Example)"
post_checks:
  - "grep -c '^| [1-5] |' .omp/memory/project/decisions.md        # Should be 5"
  - "grep -c '## Example' .omp/memory/project/decisions.md        # Should be 0"
  - "grep -c '## Decision Log' .omp/memory/project/decisions.md   # Should be 1"
  - "grep -c '## How to Add a Decision' .omp/memory/project/decisions.md  # Should be 1"
  - "grep 'OMP Beads Template' .omp/memory/project/decisions.md   # Should match once"
```

**What this task does:** Promote 5 real architecture decisions from the "Example" section to the "Decision Log" section with sequential numbering. Remove the Example section and the Decision Log placeholder row.

**Why this order:** Fourth task — pure restructure with content preservation. After the complex tech-stack.md edit, this is straightforward.

**Before:**
```
## Decision Log
| # | Date | Decision | Rationale | Confidence |
|---|------|----------|-----------|------------|
| 1 | <YYYY-MM> | <what we decided> | <why> | <High | Medium | Low> |

## How to Add a Decision
...

## Example
| # | Date | Decision | Rationale | Confidence |
|---|------|----------|-----------|------------|
| 1 | 2026-06 | Use br/bv for task tracking... | ... | High |
| 2 | 2026-06 | Commands + skills only... | ... | High |
| 3 | 2026-06 | Bare command names... | ... | High |
| 4 | 2026-06 | `.omp/` as native project root... | ... | High |
| 5 | 2026-06 | Ergonomic tooling lives in separate... | ... | High |
```

**After:**
```
## Decision Log
| # | Date | Decision | Rationale | Confidence |
|---|------|----------|-----------|------------|
| 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator. Alternatives (linear, plain markdown) lack the graph query ability. | High |
| 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts and skill knowledge. Scripts add maintenance burden, platform dependencies, and hidden logic. | High |
| 3 | 2026-06 | Bare command names (`/create`, `/plan`) | OMP resolves commands by directory. Prefix would be noise. | High |
| 4 | 2026-06 | `.omp/` as native project root | OMP loads from `.omp/`. Parallel `.pi/` config creates confusion. | High |
| 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages. The beads template stays pure workflow — install providers separately. | High |

## How to Add a Decision
...
```

**Steps:**

- [ ] Read `.omp/memory/project/decisions.md` — confirm "Example" section has 5 decisions, "Decision Log" has one placeholder row
- [ ] Replace `# Decisions: <project-name>` → `# Decisions: OMP Beads Template`
- [ ] Read the 5 decision rows from "## Example" section — capture the EXACT text of each row (date, decision, rationale, confidence)
- [ ] Replace the placeholder row in "## Decision Log" (the row with `<YYYY-MM>`) with the 5 real rows, numbered 1-5
- [ ] Delete the entire "## Example" section heading and all its rows
- [ ] Confirm "## How to Add a Decision" section heading and content are untouched
- [ ] Update frontmatter `updated:` date to `2026-06-17`
- [ ] Verify: `grep -c '^| [1-5] |' .omp/memory/project/decisions.md` returns 5 (each decision has a number 1-5)
- [ ] Verify: `grep -c '## Example' .omp/memory/project/decisions.md` returns 0 (section removed)
- [ ] Verify: `grep -c '## Decision Log' .omp/memory/project/decisions.md` returns 1
- [ ] Verify: `grep -c '## How to Add a Decision' .omp/memory/project/decisions.md` returns 1
- [ ] Verify: `grep '<YYYY-MM>' .omp/memory/project/decisions.md` returns no output (placeholder removed)
- [ ] Verify: `grep '<what we decided>' .omp/memory/project/decisions.md` returns no output (placeholder removed)
- [ ] Verify: `grep 'OMP Beads Template' .omp/memory/project/decisions.md` returns 1 match (header)
- [ ] Verify: Each of the 5 decisions' text matches the original verbatim — compare with `git show HEAD:.omp/memory/project/decisions.md` if needed

**Content preservation critical check:**
The 5 decision rows must be VERBATIM copies from the Example section. Do not retype, rephrase, or edit the decisions. Use the exact text from the current file. If in doubt, use `git show HEAD:.omp/memory/project/decisions.md` to get the original text.

**Error handling:**
- If the Example section has more or fewer than 5 decisions (file modified since PRD), promote ALL decisions in the Example section. Use sequential numbering starting from 1.
- If the Decision Log section already has real rows (manually edited), merge the Example rows after the existing ones. Assign sequential numbers continuing from the last existing number.
- If "## How to Add a Decision" section is missing, it's a file corruption — restore from git.

### 1.5 Edit gotchas.md — separate template/project gotchas

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: [".omp/memory/project/gotchas.md"]
estimated_minutes: 5
risk: Low
rollback: "git checkout -- .omp/memory/project/gotchas.md"
pre_checks:
  - "grep '<project-name>' .omp/memory/project/gotchas.md                      # Should match"
  - "grep '<YYYY-MM>' .omp/memory/project/gotchas.md                           # Should match (Active Warnings placeholder)"
  - "grep -c '^| 2026-06 |' .omp/memory/project/gotchas.md                     # Should be 13"
  - "grep 'Memory templates waste tokens' .omp/memory/project/gotchas.md       # Should match once (in Template Bootstrap)"
post_checks:
  - "grep -c '## Active Warnings' .omp/memory/project/gotchas.md               # Should be 1"
  - "grep -c '## Template Bootstrap Gotchas' .omp/memory/project/gotchas.md    # Should be 1"
  - "grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md            # Should be 1"
  - "grep -c '^| 2026-06 |' .omp/memory/project/gotchas.md                     # Should be 13 (1 + 12)"
  - "grep 'OMP Beads Template' .omp/memory/project/gotchas.md                  # Should match once"
```

**What this task does:** Separate the 13 mixed gotchas into two categories: 1 project-specific gotcha in "Active Warnings" + 12 template-universal gotchas in "Template Bootstrap Gotchas" with a blockquote note.

**Why this order:** Fifth and simplest task — pure recategorization. One row moves between tables, one note changes format.

**Classification rule:**
- Project-specific = only applies to the OMP Beads Template's own maintenance → "Active Warnings"
- Template-universal = applies to any project using this template → "Template Bootstrap Gotchas"

The one project-specific gotcha: "Memory templates waste tokens if left as placeholders" — this is literally the problem this bead fixes. It's a meta-gotcha about the template repo's own maintenance.

**Steps:**

- [ ] Read `.omp/memory/project/gotchas.md` — confirm "Active Warnings" has placeholder row, "Template Bootstrap Gotchas" has 13 rows including the memory one
- [ ] Replace `# Gotchas: <project-name>` → `# Gotchas: OMP Beads Template`
- [ ] Replace Active Warnings placeholder row (`<YYYY-MM> | <area> | <what happens> | ...`) with the real gotcha: `| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session | Fill with real project content immediately. Delete placeholder gotchas when real ones exist. |`
- [ ] Remove the row `| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ...` from the "Template Bootstrap Gotchas" table (it's now in Active Warnings)
- [ ] Replace the introductory paragraph in Template Bootstrap Gotchas (the one saying "Replace with your project's actual gotchas as you discover them") with the blockquote: `> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.`
- [ ] Verify: The 12 remaining template gotchas are unchanged (same text, same dates, same areas)
- [ ] Update frontmatter `updated:` date to `2026-06-17`
- [ ] Verify: `grep -c '## Active Warnings' .omp/memory/project/gotchas.md` returns 1
- [ ] Verify: `grep -c '## Template Bootstrap Gotchas' .omp/memory/project/gotchas.md` returns 1
- [ ] Verify: `grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md` returns 1
- [ ] Verify: `grep -c '^| 2026-06 |' .omp/memory/project/gotchas.md` returns 13 (1 in Active Warnings + 12 in Template Bootstrap)
- [ ] Verify: `grep 'OMP Beads Template' .omp/memory/project/gotchas.md` returns 1 match
- [ ] Verify: `grep '<project-name>' .omp/memory/project/gotchas.md` returns no output
- [ ] Verify: Read file — "Active Warnings" has exactly 1 real row, "Template Bootstrap Gotchas" has blockquote + 12 rows, "How to Add a Gotcha" section is untouched

**Error handling:**
- If Active Warnings already has real rows (manually added), ADD the memory-template gotcha to the existing rows instead of replacing. Do not overwrite user content.
- If the "Memory templates waste tokens" row appears in a different format or with different text, match the exact text from the file when removing it from Template Bootstrap Gotchas.
- If the introductory paragraph in Template Bootstrap Gotchas has different text than documented, replace the entire paragraph with the blockquote.

## 2. Wave 2: Integration Verification

### 2.1 Run full verification

```yaml
depends_on: ["1.1", "1.2", "1.3", "1.4", "1.5"]
parallel: false
conflicts_with: []
files: []
estimated_minutes: 5
risk: Low
rollback: N/A (read-only)
```

**What this task does:** Run all 14 verification checks across all 5 files. This is a read-only task — no edits.

**Why this order:** After all Wave 1 tasks complete, confirm everything is correct before committing. Catches cross-file issues that individual task verifications might miss (e.g., inconsistent frontmatter dates, remaining placeholders).

**Steps:**

- [ ] Check 1: `grep -r '<project-name>' .omp/memory/project/` — expect no output (exit code 1)
- [ ] Check 2: `grep '<!-- TODO' .omp/memory/project/project.md` — expect no output (exit code 1)
- [ ] Check 3: `grep -c '^| [1-5] |' .omp/memory/project/decisions.md` — expect 5
- [ ] Check 4: `grep -c '## Example' .omp/memory/project/decisions.md` — expect 0
- [ ] Check 5: `grep -c 'design/craft/' .omp/memory/project/tech-stack.md` — expect 8
- [ ] Check 6: `grep -c '## Active Warnings' .omp/memory/project/gotchas.md` — expect 1
- [ ] Check 7: `grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md` — expect 1
- [ ] Check 8: `grep -c '^| 2026-06 |' .omp/memory/project/gotchas.md` — expect 13
- [ ] Check 9: `grep '<TypeScript | Go | Rust | Python>' .omp/memory/project/conventions.md` — expect no output
- [ ] Check 10: `grep '<tsc --noEmit | mypy | cargo check | go vet>' .omp/memory/project/tech-stack.md` — expect no output
- [ ] Check 11: `br list --status open --json` — expect valid JSON output, includes br-omp-backbone-skill-l3d
- [ ] Check 12: `bv --robot-triage --format json` — expect valid JSON output, no errors
- [ ] Check 13: `grep 'updated: 2026-06-17' .omp/memory/project/project.md` — expect 1 match
- [ ] Check 13 continued: Repeat for conventions.md, tech-stack.md, decisions.md, gotchas.md — expect 1 match each (5 total)
- [ ] Check 14: Read all 5 files end-to-end — confirm tables have consistent column counts, no orphan rows, no placeholders remain, all frontmatter dates are 2026-06-17
- [ ] Verify: ALL 14 checks pass. If any check fails, identify the file, fix it, and re-run all checks.

**If a check fails:**
1. Note which check failed and what file it's testing
2. Read that file to understand the issue
3. Fix the file with an edit
4. Re-run the specific check to confirm the fix
5. Re-run all 14 checks to confirm no regressions

## 3. Commit

### 3.1 Sync and commit

```yaml
depends_on: ["2.1"]
parallel: false
conflicts_with: []
files: [".omp/memory/project/project.md", ".omp/memory/project/conventions.md", ".omp/memory/project/tech-stack.md", ".omp/memory/project/decisions.md", ".omp/memory/project/gotchas.md"]
estimated_minutes: 2
risk: Low
rollback: "git reset HEAD~1"
```

**What this task does:** Sync bead state, stage all 5 edited files plus bead state, and create a single atomic commit.

**Why this order:** Final step — only after all Wave 1 edits are verified and Wave 2 checks pass. Atomic commit means either all 5 files are committed or none are.

**Steps:**

- [ ] Run `br sync --flush-only` — confirm "Nothing to export" or successful sync
- [ ] Run `git status --short` — confirm the 5 memory files show as modified, no unexpected changes
- [ ] Stage changed files: `git add .omp/memory/project/project.md .omp/memory/project/conventions.md .omp/memory/project/tech-stack.md .omp/memory/project/decisions.md .omp/memory/project/gotchas.md .beads/`
- [ ] Run `git commit -m "chore: hydrate memory files with project identity

- Fill project.md with real goal, success criteria, current phase
- Fill conventions.md language table (N/A for backend/frontend)
- Fix tech-stack.md broken craft table, fill verification commands
- Promote 5 real decisions from Example to Decision Log
- Separate template-universal from project-specific gotchas
- Remove all <project-name> and template placeholders"`
- [ ] Verify: `git log --oneline -1` shows the new commit with the message above
- [ ] Verify: `git diff HEAD~1 --stat` shows exactly 5 files changed in `.omp/memory/project/` plus `.beads/`
- [ ] Verify: `git status` shows working tree clean (no unstaged changes in the committed files)

## Task Dependency Graph

```
1.1 (project.md) ─┐
1.2 (conventions) ─┤
1.3 (tech-stack)  ─┼──→ 2.1 (verification) ──→ 3.1 (commit)
1.4 (decisions)   ─┤
1.5 (gotchas)     ─┘
```

All Wave 1 tasks are parallel. Wave 2 depends on all of Wave 1. Commit depends on Wave 2.

## Parallel Execution Strategy

All 5 Wave 1 tasks touch different files — no conflicts possible:

| Task | File | Can parallel with |
|------|------|-------------------|
| 1.1 | project.md | 1.2, 1.3, 1.4, 1.5 |
| 1.2 | conventions.md | 1.1, 1.3, 1.4, 1.5 |
| 1.3 | tech-stack.md | 1.1, 1.2, 1.4, 1.5 |
| 1.4 | decisions.md | 1.1, 1.2, 1.3, 1.5 |
| 1.5 | gotchas.md | 1.1, 1.2, 1.3, 1.4 |

If using subagents: spawn 5 parallel agents, one per task. Each reads its target file, edits it, and verifies its own grep checks. Wave 2 integration runs after all 5 report success.

If executing sequentially: follow the order 1.1 → 1.2 → 1.3 → 1.4 → 1.5 (recommended for sequential execution, per rationale above). Each task is self-contained.

## Verification Summary

| Check # | Command | Expected | Verifies |
|---------|---------|----------|----------|
| 1 | `grep -r '<project-name>' .omp/memory/project/` | No output | All files: no placeholder project names |
| 2 | `grep '<!-- TODO' .omp/memory/project/project.md` | No output | project.md: no TODO markers |
| 3 | `grep -c '^| [1-5] |' .omp/memory/project/decisions.md` | 5 | decisions.md: 5 promoted decisions |
| 4 | `grep -c '## Example' .omp/memory/project/decisions.md` | 0 | decisions.md: Example section removed |
| 5 | `grep -c 'design/craft/' .omp/memory/project/tech-stack.md` | 8 | tech-stack.md: all 8 craft files listed |
| 6 | `grep -c '## Active Warnings' .omp/memory/project/gotchas.md` | 1 | gotchas.md: Active Warnings section |
| 7 | `grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md` | 1 | gotchas.md: blockquote note |
| 8 | `grep -c '^| 2026-06 |' .omp/memory/project/gotchas.md` | 13 | gotchas.md: all 13 gotchas preserved |
| 9 | `grep '<TypeScript...>' .omp/memory/project/conventions.md` | No output | conventions.md: language table filled |
| 10 | `grep '<tsc...>' .omp/memory/project/tech-stack.md` | No output | tech-stack.md: verification filled |
| 11 | `br list --status open --json` | Valid JSON | br: bead database functional |
| 12 | `bv --robot-triage --format json` | Valid JSON | bv: graph analysis functional |
| 13 | `grep 'updated: 2026-06-17' .omp/memory/project/*.md` | 5 matches | All files: frontmatter updated |
| 14 | Manual read of all 5 files | No issues | Visual inspection of markdown structure |

All 14 checks must pass before the commit. If any check fails, fix the corresponding file and re-verify.

## Failure Recovery Matrix

| Scenario | Recovery | Impact |
|----------|----------|--------|
| Single file edit produces wrong output | `git checkout -- .omp/memory/project/<file>.md`, then re-edit | Only that task needs redo |
| Multiple files produce wrong output | `git checkout -- .omp/memory/project/`, then redo all Wave 1 | All Wave 1 tasks need redo |
| Verification check fails | Read the failing file, fix with edit, re-run all 14 checks | +5 minutes |
| br/bv broken after edits | This shouldn't happen (markdown files only, no code changes). If it does, full rollback: `git checkout -- .omp/memory/project/` | All Wave 1 needs redo |
| Commit created with wrong message | `git commit --amend -m "corrected message"` | 1 minute fix |
