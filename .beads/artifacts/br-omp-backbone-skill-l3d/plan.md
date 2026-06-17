# Plan: br-omp-backbone-skill-l3d

**Goal:** Replace 19 template placeholders across 5 memory files with real project identity, fix 2 structural issues (broken craft table, mislabeled decisions section), and separate template-universal from project-specific gotchas.

## Graph Context

- **Blast radius:** 5 files (0 new, 5 edits, 0 deletes)
- **Unblocks:** None — this is a self-contained chore
- **Blocked by:** None — no dependencies on other beads
- **Critical path:** No — does not block other work
- **Forecast:** 30 minutes (confidence 0.95)
- **Hotspots touched:** None — memory files have no prior bead activity (0 beads touched each)

## Observable Truths

1. `grep -r '<project-name>' .omp/memory/project/` returns no matches in any file
2. `grep '<!-- TODO' .omp/memory/project/project.md` returns no matches
3. `grep -c '^| [1-5] |' .omp/memory/project/decisions.md` returns 5
4. `grep -c '## Example' .omp/memory/project/decisions.md` returns 0
5. `grep -c 'design/craft/' .omp/memory/project/tech-stack.md` returns 8
6. `grep -c '## Active Warnings' .omp/memory/project/gotchas.md` returns 1
7. `grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md` returns 1
8. All 5 files parse as valid markdown with consistent table column counts
9. The 5 decisions' text, rationale, and confidence match the original verbatim
10. All 13 gotcha entries are preserved — only categorization changed
11. `br list --status open --json` and `bv --robot-triage --format json` succeed after changes

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| project.md | Filled project identity (name, goal, criteria, phase) | `.omp/memory/project/project.md` | Edit needed |
| conventions.md | Filled language table, real project name | `.omp/memory/project/conventions.md` | Edit needed |
| tech-stack.md | Fixed craft table, real verification commands, real project name | `.omp/memory/project/tech-stack.md` | Edit needed |
| decisions.md | Decisions promoted to Decision Log, Example section removed | `.omp/memory/project/decisions.md` | Edit needed |
| gotchas.md | Separated template/project gotchas, real project name | `.omp/memory/project/gotchas.md` | Edit needed |
| prd.md | Problem, scope, requirements, approach, risks, acceptance criteria | `.beads/artifacts/br-omp-backbone-skill-l3d/prd.md` | Have |
| prd.json | Machine-readable requirements mirror | `.beads/artifacts/br-omp-backbone-skill-l3d/prd.json` | Have |
| decisions.md (bead) | Design decisions for this bead | `.beads/artifacts/br-omp-backbone-skill-l3d/decisions.md` | Have |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1 project.md, 1.2 conventions.md, 1.3 tech-stack.md, 1.4 decisions.md, 1.5 gotchas.md | Yes — all 5 files independent | PRD approved, bead open | Each file passes its individual grep check |
| 2 | 2.1 Integration verification | No | All Wave 1 tasks complete | All 11 observable truths confirmed; br + bv functional |

## Tasks

### Wave 1: File edits (parallel)

All 5 tasks can run in parallel — no file depends on another. Each task edits exactly one file. The order in the wave structure is for readability only; implementation can execute them in any order.

#### Task 1.1: Edit project.md — fill project identity

Edit `.omp/memory/project/project.md` to replace all 8 placeholder fields with real content. The file currently has these placeholders:

- Line ~6: `# Project: <project-name>` → `# Project: OMP Beads Template`
- Line ~12: `<One sentence — what are we building and why?>` → real goal
- Lines ~16-18: `<Criterion 1>`, `<Criterion 2>`, `<Criterion 3>` → 3 real criteria
- Lines ~16-18: `<measurable outcome>` (x3) → real measurable outcomes
- Line ~24: `<active | maintenance | paused>` → `active`
- Line ~25: `<what we're working toward right now>` → real milestone
- Line ~26: `<the next concrete deliverable>` → real next step
- Frontmatter: `updated: 2026-06-17`

**Code outline — the shape of the edit:**

```
Read .omp/memory/project/project.md
  → Identify 8 placeholder patterns
  → Each replacement is a literal string swap:
    1. "<project-name>" → "OMP Beads Template"
    2. "<One sentence — what are we building and why?>" → goal text
    3. "<Criterion 1>" → "Zero <project-name> or template placeholders in any .omp/memory/project/ file"
    4. "<Criterion 2>" → "Every memory file is valid markdown with filled tables"
    5. "<Criterion 3>" → "An agent loading this context can answer what this project is within 3 seconds"
    6. "<measurable outcome>" (first occurrence) → "grep -r '<project-name>' .omp/memory/project/ returns no matches"
    7. "<measurable outcome>" (second occurrence) → "Read each file — tables have consistent columns, no orphan rows"
    8. "<measurable outcome>" (third occurrence) → "project.md heading + goal is self-contained and understandable"
    9. "<active | maintenance | paused>" → "active"
   10. "<what we're working toward right now>" → "Memory file hydration — project identity hardening"
   11. "<the next concrete deliverable>" → "Audit command files for consistency with conventions.md"
   12. Frontmatter updated: → "2026-06-17"
  → Write result
  → Verify: grep '<project-name>' .omp/memory/project/project.md (expect 0)
  → Verify: grep '<!-- TODO' .omp/memory/project/project.md (expect 0)
  → Verify: read file — confirm all 11 replacements applied
```

**Goal text (from PRD):**
"An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating."

**Success criteria (from PRD):**
1. Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file — verifiable with `grep -r '<project-name>' .omp/memory/project/` returning no matches
2. Every memory file is valid markdown with filled tables — verifiable by reading each file; no orphan rows, consistent column counts
3. An agent loading this context can answer "what is this project" within 3 seconds — qualitative but observable: `project.md` heading + goal must be self-contained

**Current phase (from PRD):**
- Status: active (8 beads closed, design system scaffolded, Honcho workflow added, git-clean command added — active development)
- Milestone: "Memory file hydration — project identity hardening"
- Next: "Audit command files for consistency with conventions.md"

**Verification:**
```bash
grep '<project-name>' .omp/memory/project/project.md          # Expected: no output (exit 1)
grep '<!-- TODO' .omp/memory/project/project.md                # Expected: no output (exit 1)
grep 'OMP Beads Template' .omp/memory/project/project.md       # Expected: 1 match (header)
grep 'br/bv-powered workflow infrastructure' .omp/memory/project/project.md  # Expected: 1 match (goal)
```

#### Task 1.2: Edit conventions.md — fill language table

Edit `.omp/memory/project/conventions.md` to replace the project name and fill the "Languages by Purpose" table.

**Current state:**
- Line ~6: `# Conventions: <project-name>` → `# Conventions: OMP Beads Template`
- Languages table: Backend row has `<TypeScript | Go | Rust | Python>` as language and `<strict? Bun? Deno?>` as notes → replace both with "N/A"
- Languages table: Frontend row has `<TypeScript | JavaScript>` as language and `<React? Svelte? plain?>` as notes → replace both with "N/A"
- Languages table: Scripts row has `<Bash | Python | TypeScript>` as language and `<CI, dev tooling, one-offs>` as notes → replace with "Python" and "`/init` hydration script (`.omp/commands/init.md` Phase 2.5)"
- Frontmatter: `updated: 2026-06-17`

**Code outline — the shape of the edit:**

```
Read .omp/memory/project/conventions.md
  → Identify "Languages by Purpose" table (lines ~18-25)
  → Replace header: "<project-name>" → "OMP Beads Template"
  → Replace backend row:
      "| Backend | <TypeScript | Go | Rust | Python> | <strict? Bun? Deno?> |"
      → "| Backend | N/A | Template repo — no backend runtime |"
  → Replace frontend row:
      "| Frontend | <TypeScript | JavaScript> | <React? Svelte? plain?> |"
      → "| Frontend | N/A | Template repo — provides design system assets only |"
  → Replace scripts row:
      "| Scripts | <Bash | Python | TypeScript> | <CI, dev tooling, one-offs> |"
      → "| Scripts | Python | `/init` hydration script |"
  → Update frontmatter: "updated: 2026-06-17"
  → Write result
```

**Target table rows:**
| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | N/A | Template repo — no backend runtime |
| Frontend | N/A | Template repo — provides design system assets only |
| Scripts | Python | `/init` hydration script |

**Verification:**
```bash
grep '<TypeScript | Go | Rust | Python>' .omp/memory/project/conventions.md  # Expected: no output
grep 'N/A' .omp/memory/project/conventions.md                                # Expected: ≥2 matches (backend + frontend)
grep 'Python.*init.*hydration' .omp/memory/project/conventions.md             # Expected: 1 match
grep 'OMP Beads Template' .omp/memory/project/conventions.md                  # Expected: 1 match (header)
```

#### Task 1.3: Edit tech-stack.md — fix craft table, fill placeholders

Edit `.omp/memory/project/tech-stack.md` to fix the broken craft references table, replace placeholders in runtime/verification sections, and set the project name.

**Current state:**
- Line ~6: `# Tech Stack: <project-name>` → `# Tech Stack: OMP Beads Template`
- Runtime table: Language row has `<TypeScript | Python | Go | Rust>`, `<version>`, `<strict mode?>` → all N/A
- Runtime table: Runtime row has `<Node.js | Bun | Deno | Python 3.x | Go 1.x>`, `<version>`, `<LTS? latest?>` → all N/A
- Runtime table: Package manager row has `<npm | pnpm | yarn | pip | cargo | go mod>`, `<version>` → all N/A
- Verification commands: Typecheck, Lint, Test, Build all have `<tsc | mypy | ...>` → all N/A
- Security: Dependency audit has `<npm audit | pip-audit | ...>` → N/A
- Craft table: Lines 80-84 have 4 rows, line 85 is attribution, lines 86-88 are orphan rows → merge into one table, add state-coverage.md
- Frontmatter: `updated: 2026-06-17`

**Code outline — the shape of the edit:**

```
Read .omp/memory/project/tech-stack.md

Step 1: Replace header
  "<project-name>" → "OMP Beads Template"

Step 2: Replace runtime table rows (lines ~12-16)
  Language row: "| Language | <TypeScript | Python | Go | Rust> | <version> | <strict mode? async? experimental flags?> |"
    → "| Language | N/A | — | Template repo — no application language |"
  Runtime row: "| Runtime | <Node.js | Bun | Deno | Python 3.x | Go 1.x> | <version> | <LTS? latest?> |"
    → "| Runtime | N/A | — | Template repo — no application runtime |"
  Package manager row: "| Package manager | <npm | pnpm | yarn | pip | cargo | go mod> | <version> | |"
    → "| Package manager | N/A | — | Template repo — no dependencies |"

Step 3: Replace verification commands (lines ~28-44)
  Typecheck: "<tsc --noEmit | mypy | cargo check | go vet>" → "N/A — template repo, no application code"
  Lint: "<eslint | ruff | clippy | golangci-lint>" → "N/A — template repo, no application code"
  Test: "<vitest run | pytest | cargo test | go test ./...>" → "N/A — template repo, no application code"
  Build: "<tsup | pip install -e . | cargo build --release | go build>" → "N/A — template repo, no application code"

Step 4: Replace security commands (lines ~50-56)
  Dependency audit: "<npm audit | pip-audit | cargo audit | govulncheck>" → "N/A — template repo, no dependencies"

Step 5: Fix craft table (lines ~78-89)
  Read design/craft/state-coverage.md to extract purpose description
  Reconstruct lines 78-89 into:
    - One table with header row (| File | Purpose |) and 8 data rows
    - Attribution paragraph AFTER the table

  Target craft table:
  | File | Purpose |
  |------|---------|
  | `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
  | `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
  | `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
  | `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |
  | `design/craft/state-coverage.md` | {purpose derived from reading the file} |
  | `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
  | `design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
  | `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |

  Followed by: "Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT)."

Step 6: Update frontmatter
  "updated: 2026-06-17"

  → Write result
```

**Before editing tech-stack.md, read `design/craft/state-coverage.md` to extract the purpose:**
The file's first heading/paragraph should describe what it covers. Use that as the table Description.

**Verification:**
```bash
grep -c 'design/craft/' .omp/memory/project/tech-stack.md              # Expected: 8
grep '<TypeScript | Python | Go | Rust>' .omp/memory/project/tech-stack.md  # Expected: no output
grep '<tsc --noEmit | mypy | cargo check | go vet>' .omp/memory/project/tech-stack.md  # Expected: no output
grep 'N/A.*template repo' .omp/memory/project/tech-stack.md            # Expected: ≥5 matches
grep 'OMP Beads Template' .omp/memory/project/tech-stack.md            # Expected: 1 match
```

#### Task 1.4: Edit decisions.md — promote decisions to Decision Log

Edit `.omp/memory/project/decisions.md` to promote the 5 real decisions from "Example" to "Decision Log" and remove the placeholder row.

**Current state:**
- Line ~6: `# Decisions: <project-name>` → `# Decisions: OMP Beads Template`
- "## Decision Log" section: one placeholder row with `<YYYY-MM>`, `<what we decided>`, `<why>`, `<High | Medium | Low>` → replace with 5 real rows
- "## Example" section: 5 real decisions → remove entire section
- "## How to Add a Decision" section: keep as-is
- Frontmatter: `updated: 2026-06-17`

**Code outline — the shape of the edit:**

```
Read .omp/memory/project/decisions.md

Step 1: Replace header
  "<project-name>" → "OMP Beads Template"

Step 2: Replace Decision Log placeholder row
  Current: "| 1 | <YYYY-MM> | <what we decided> | <why — tradeoffs, alternatives considered> | <High | Medium | Low> |"
  → Delete that row, insert 5 real rows:
    "| 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator. Alternatives (linear, plain markdown) lack the graph query ability. | High |"
    "| 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts and skill knowledge. Scripts add maintenance burden, platform dependencies, and hidden logic. | High |"
    "| 3 | 2026-06 | Bare command names (`/create`, `/plan`) | OMP resolves commands by directory. Prefix would be noise. | High |"
    "| 4 | 2026-06 | `.omp/` as native project root | OMP loads from `.omp/`. Parallel `.pi/` config creates confusion. | High |"
    "| 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages. The beads template stays pure workflow — install providers separately. | High |"

Step 3: Remove "## Example" section
  Delete everything from "## Example" through the 5 example decision rows.
  The "## How to Add a Decision" section stays.

Step 4: Update frontmatter
  "updated: 2026-06-17"

  → Write result
```

**Content preservation check:** The 5 decision rows copied from the Example section must be VERBATIM — same text, same rationale, same confidence. Use the exact strings from the current file.

**Verification:**
```bash
grep -c '^| [1-5] |' .omp/memory/project/decisions.md               # Expected: 5
grep -c '## Example' .omp/memory/project/decisions.md                # Expected: 0
grep -c '## Decision Log' .omp/memory/project/decisions.md           # Expected: 1
grep -c '## How to Add a Decision' .omp/memory/project/decisions.md  # Expected: 1
grep 'OMP Beads Template' .omp/memory/project/decisions.md           # Expected: 1 match (header)
```

#### Task 1.5: Edit gotchas.md — separate template/project gotchas

Edit `.omp/memory/project/gotchas.md` to separate project-specific from template-universal gotchas and add a blockquote note.

**Current state:**
- Line ~6: `# Gotchas: <project-name>` → `# Gotchas: OMP Beads Template`
- "## Active Warnings" section: placeholder row with `<YYYY-MM>`, `<area>`, etc. → replace with 1 real project-specific gotcha
- "## Template Bootstrap Gotchas" section: 13 mixed gotchas → keep 12 template-universal, extract 1 project-specific
- The section note "Replace with your project's actual gotchas" → replace with blockquote note
- Frontmatter: `updated: 2026-06-17`

**Code outline — the shape of the edit:**

```
Read .omp/memory/project/gotchas.md

Step 1: Replace header
  "<project-name>" → "OMP Beads Template"

Step 2: Replace Active Warnings placeholder row
  Current: "| <YYYY-MM> | <area> | <what happens> | <why it matters> | <how to avoid or recover> |"
  → Replace with:
    "| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session | Fill with real project content immediately. Delete placeholder gotchas when real ones exist. |"

Step 3: Update Template Bootstrap Gotchas section
  Remove the row "| 2026-06 | memory | Memory templates waste tokens..." from this table (it's now in Active Warnings).
  Replace the introductory paragraph with a blockquote:
    "> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them."
  Keep all 12 remaining entries verbatim.

Step 4: Update frontmatter
  "updated: 2026-06-17"

  → Write result
```

**Gotcha classification — which rows move:**
- MOVE to Active Warnings: "Memory templates waste tokens if left as placeholders" (2026-06, area: memory)
- KEEP in Template Bootstrap Gotchas: all other 12 entries

**Verification:**
```bash
grep -c '## Active Warnings' .omp/memory/project/gotchas.md              # Expected: 1
grep -c '## Template Bootstrap Gotchas' .omp/memory/project/gotchas.md   # Expected: 1
grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md           # Expected: 1
grep 'OMP Beads Template' .omp/memory/project/gotchas.md                 # Expected: 1 match (header)
# Count total gotcha rows (table rows starting with | 2026-06):
grep -c '^| 2026-06 |' .omp/memory/project/gotchas.md                    # Expected: 13 (1 active + 12 template)
```

### Wave 2: Integration verification

#### Task 2.1: Integration verification

Run all verification checks across all 5 files and confirm br/bv still function.

```
Execute verification script (see Full Verification section below):
  1. grep -r '<project-name>' .omp/memory/project/ → expect no matches
  2. grep '<!-- TODO' .omp/memory/project/project.md → expect no matches
  3. grep -c '^| [1-5] |' .omp/memory/project/decisions.md → expect 5
  4. grep -c '## Example' .omp/memory/project/decisions.md → expect 0
  5. grep -c 'design/craft/' .omp/memory/project/tech-stack.md → expect 8
  6. grep -c '## Active Warnings' .omp/memory/project/gotchas.md → expect 1
  7. grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md → expect 1
  8. Read all 5 files → confirm tables have consistent column counts
  9. br list --status open --json → expect success
  10. bv --robot-triage --format json → expect success

  If all 10 checks pass → commit and report success
  If any check fails → fix the failing file and re-verify
```

**Verification:**
All 10 checks pass. No exceptions.

## Full Verification

```bash
# === Check 1: No <project-name> anywhere ===
grep -r '<project-name>' .omp/memory/project/
# Expected: no output (exit code 1)

# === Check 2: No TODO markers in project.md ===
grep '<!-- TODO' .omp/memory/project/project.md
# Expected: no output (exit code 1)

# === Check 3: 5 numbered decisions in Decision Log ===
grep -c '^| [1-5] |' .omp/memory/project/decisions.md
# Expected: 5

# === Check 4: No Example section in decisions.md ===
grep -c '## Example' .omp/memory/project/decisions.md
# Expected: 0

# === Check 5: 8 craft files in tech-stack.md table ===
grep -c 'design/craft/' .omp/memory/project/tech-stack.md
# Expected: 8

# === Check 6: Active Warnings section exists ===
grep -c '## Active Warnings' .omp/memory/project/gotchas.md
# Expected: 1

# === Check 7: Blockquote note in gotchas.md ===
grep -c '^> These gotchas ship' .omp/memory/project/gotchas.md
# Expected: 1

# === Check 8: 13 total gotcha rows preserved ===
grep -c '^| 2026-06 |' .omp/memory/project/gotchas.md
# Expected: 13

# === Check 9: No placeholder options in conventions.md ===
grep '<TypeScript | Go | Rust | Python>' .omp/memory/project/conventions.md
# Expected: no output (exit code 1)

# === Check 10: No placeholder verification commands in tech-stack.md ===
grep '<tsc --noEmit | mypy | cargo check | go vet>' .omp/memory/project/tech-stack.md
# Expected: no output (exit code 1)

# === Check 11: br functional ===
br list --status open --json
# Expected: valid JSON output, includes br-omp-backbone-skill-l3d

# === Check 12: bv functional ===
bv --robot-triage --format json
# Expected: valid JSON output, no errors

# === Check 13: All files have updated frontmatter ===
grep 'updated: 2026-06-17' .omp/memory/project/project.md
grep 'updated: 2026-06-17' .omp/memory/project/conventions.md
grep 'updated: 2026-06-17' .omp/memory/project/tech-stack.md
grep 'updated: 2026-06-17' .omp/memory/project/decisions.md
grep 'updated: 2026-06-17' .omp/memory/project/gotchas.md
# Expected: all 5 return matches

# === Check 14: Manual read of all 5 files ===
# Read each file end-to-end:
#   - project.md: header + goal + 3 criteria + phase → all filled
#   - conventions.md: header + 5 language rows → all filled
#   - tech-stack.md: header + runtime table + verification + craft table → all filled, no orphans
#   - decisions.md: header + 5 decision rows + How to Add → no Example section
#   - gotchas.md: header + 1 active + blockquote + 12 template + How to Add → all preserved
```

## Notes

- **All 5 Wave 1 tasks are independent** — they edit different files and can execute in any order or in parallel.
- **No code changes** — these are markdown documentation edits. No compilation, no tests, no breaking changes possible.
- **Verification is fast** — the full verification script takes <5 seconds to run. Run it after each file edit for fast feedback.
- **Commit after all 5 files pass** — single atomic commit: `chore: hydrate memory files with project identity`.
- **br sync before commit** — run `br sync --flush-only` before staging to ensure bead state is consistent.

## Edge Cases and Error Handling

### What if a file has been modified since the PRD was written?

Before editing each file, read the current content and confirm the placeholders documented in the PRD still exist. If a placeholder has already been filled (e.g., someone manually edited the file), skip that replacement. Only replace placeholders that still exist.

Check approach: for each file, grep for the placeholder patterns before editing. If a pattern doesn't match, the placeholder may already be filled. Read the file to confirm, then skip that replacement.

### What if the craft table structure differs from what's documented?

The PRD documents lines 80-89 of tech-stack.md as of 2026-06-17. If the file has been restructured (new craft files added, table reorganized), read the current structure and adapt. The invariant is: all craft files that exist in `design/craft/` must appear in a contiguous table in tech-stack.md with the attribution paragraph after the table.

### What if gotchas.md already has project-specific gotchas in Active Warnings?

The current file has a placeholder row in Active Warnings. If a real gotcha was added there, preserve it and ADD the memory-template one alongside it. Don't overwrite user-added content.

### What if decisions.md has a 6th decision in the Example section?

If a new decision was added to the Example section since the PRD was written, include it in the promotion. The count should be whatever is in Example, not hardcoded to 5. Use the sequential numbering — next number after the last existing one.

### What if a file has trailing whitespace or formatting differences?

Preserve the existing formatting. The edit tool does exact string replacement — only the placeholder text changes. Table alignment, line endings, and whitespace should remain unchanged. If a placeholder spans multiple tokens (e.g., `<TypeScript | Go | Rust | Python>` appears split across the language and notes cells), replace each cell independently.

### What if the token budget constraint is violated after edits?

The conventions.md is already ~3KB. This bead adds minimal content (~20 characters for the project name in headers, a few dozen characters for N/A explanations). If the budget is a hard constraint, the UI Design section (~70 lines) should be addressed in a separate bead — it's the primary contributor to the overshoot. This bead does not worsen the situation meaningfully.

## Rollback Strategy

### Per-file rollback

If a single file edit produces incorrect output:
```bash
git checkout -- .omp/memory/project/<file>.md
```

### Full rollback

If multiple files need reverting:
```bash
git checkout -- .omp/memory/project/
```

### State verification after rollback

After rolling back, confirm the files match their pre-edit state:
```bash
git diff .omp/memory/project/     # Should show no changes after rollback
```

### No database impact

These are markdown documentation files. Rolling back has zero impact on br state, bv graph, or workflow gate. No migration, no schema change, no data loss possible.

## Implementation Checklist

Before marking this plan as executed:

- [ ] All 5 Wave 1 tasks completed (files edited)
- [ ] Wave 2 integration verification passed (all 14 checks green)
- [ ] `br sync --flush-only` executed
- [ ] Single commit created: `chore: hydrate memory files with project identity`
- [ ] Bead status updated to reflect completion
- [ ] Plan artifacts (plan.md, tasks.md, context-capsule.md) ≥600 lines each

## Pre-edit File State Snapshots

### project.md — placeholders to replace (exact strings)

```
1. "<project-name>" → "OMP Beads Template"
2. "<One sentence — what are we building and why?>" → "An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating."
3. "<Criterion 1>" → "Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file"
4. "<Criterion 2>" → "Every memory file is valid markdown with filled tables"
5. "<Criterion 3>" → "An agent loading this context can answer what this project is within 3 seconds"
6. "<measurable outcome>" (first) → "`grep -r '<project-name>' .omp/memory/project/` returns no matches"
7. "<measurable outcome>" (second) → "Read each file — tables have consistent columns, no orphan rows"
8. "<measurable outcome>" (third) → "`project.md` heading + goal is self-contained and understandable"
9. "<active | maintenance | paused>" → "active"
10. "<what we're working toward right now>" → "Memory file hydration — project identity hardening"
11. "<the next concrete deliverable>" → "Audit command files for consistency with conventions.md"
```

### conventions.md — placeholders to replace (exact strings)

```
1. "<project-name>" → "OMP Beads Template"
2. Backend language cell: "<TypeScript | Go | Rust | Python>" → "N/A"
3. Backend notes cell: "<strict? Bun? Deno?>" → "Template repo — no backend runtime"
4. Frontend language cell: "<TypeScript | JavaScript>" → "N/A"
5. Frontend notes cell: "<React? Svelte? plain?>" → "Template repo — provides design system assets only"
6. Scripts language cell: "<Bash | Python | TypeScript>" → "Python"
7. Scripts notes cell: "<CI, dev tooling, one-offs>" → "`/init` hydration script"
```

### tech-stack.md — placeholders to replace (exact strings)

```
1. "<project-name>" → "OMP Beads Template"
2. Language cell: "<TypeScript | Python | Go | Rust>" → "N/A"
3. Language version: "<version>" → "—"
4. Language notes: "<strict mode? async? experimental flags?>" → "Template repo — no application language"
5. Runtime cell: "<Node.js | Bun | Deno | Python 3.x | Go 1.x>" → "N/A"
6. Runtime version: "<version>" → "—"
7. Runtime notes: "<LTS? latest?>" → "Template repo — no application runtime"
8. Package manager cell: "<npm | pnpm | yarn | pip | cargo | go mod>" → "N/A"
9. Package manager version: "<version>" → "—"
10. Typecheck: "<tsc --noEmit | mypy | cargo check | go vet>" → "N/A — template repo, no application code"
11. Lint: "<eslint | ruff | clippy | golangci-lint>" → "N/A — template repo, no application code"
12. Test: "<vitest run | pytest | cargo test | go test ./...>" → "N/A — template repo, no application code"
13. Build: "<tsup | pip install -e . | cargo build --release | go build>" → "N/A — template repo, no application code"
14. Dependency audit: "<npm audit | pip-audit | cargo audit | govulncheck>" → "N/A — template repo, no dependencies"
15. Craft table: structural fix (merge tables, add state-coverage.md, move attribution)
```

### decisions.md — changes (exact strings)

```
1. "<project-name>" → "OMP Beads Template"
2. Decision Log placeholder row → 5 real decision rows (verbatim from Example section)
3. Delete "## Example" section and all example rows
4. Keep "## How to Add a Decision" section unchanged
```

### gotchas.md — changes (exact strings)

```
1. "<project-name>" → "OMP Beads Template"
2. Active Warnings placeholder row → real row (memory templates waste tokens)
3. Remove same row from Template Bootstrap Gotchas
4. Replace section intro paragraph with blockquote note
5. Keep all other 12 gotchas verbatim
```

## Task Ownership

| Task | Files | Owner | Parallel Safe? |
|------|-------|-------|----------------|
| 1.1 project.md | `.omp/memory/project/project.md` | Any agent | Yes — isolated file |
| 1.2 conventions.md | `.omp/memory/project/conventions.md` | Any agent | Yes — isolated file |
| 1.3 tech-stack.md | `.omp/memory/project/tech-stack.md`, `design/craft/state-coverage.md` (read-only) | Any agent | Yes — isolated file |
| 1.4 decisions.md | `.omp/memory/project/decisions.md` | Any agent | Yes — isolated file |
| 1.5 gotchas.md | `.omp/memory/project/gotchas.md` | Any agent | Yes — isolated file |
| 2.1 Integration | All 5 edited files (read-only) | Any agent | No — depends on all Wave 1 |

## Commit Strategy

Single atomic commit after all Wave 1 tasks pass and Wave 2 verification is green:

```bash
br sync --flush-only
git add .omp/memory/project/project.md \
        .omp/memory/project/conventions.md \
        .omp/memory/project/tech-stack.md \
        .omp/memory/project/decisions.md \
        .omp/memory/project/gotchas.md \
        .beads/
git commit -m "chore: hydrate memory files with project identity

- Fill project.md with real goal, success criteria, current phase
- Fill conventions.md language table (N/A for backend/frontend)
- Fix tech-stack.md broken craft table, fill verification commands
- Promote 5 real decisions from Example to Decision Log
- Separate template-universal from project-specific gotchas
- Remove all <project-name> and template placeholders"
```

## Why This Plan is Safe

1. **No code changes** — all edits are to markdown documentation files. No compilation, no tests, no runtime behavior.
2. **No structural dependencies** — each file is independent. A mistake in one file doesn't affect the others.
3. **Verification is mechanical** — every check is a grep command or a file read. No interpretation needed.
4. **Rollback is trivial** — `git checkout -- .omp/memory/project/` reverts all changes.
5. **No blast radius** — these files are read by agents only. No tool, script, or CI process depends on their content.
6. **Content preservation** — the decisions.md and gotchas.md edits only restructure, they don't change text. The original content is preserved verbatim.
7. **Honest N/A values** — where a value doesn't apply, we say so. No fake detection, no made-up versions.

## What Could Go Wrong

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Placeholder already filled (file modified since PRD) | grep for placeholder before editing; if not found, skip | Read file, confirm it's already filled, move on |
| Table column misalignment after edit | Visual inspection of the file after edit | `git checkout -- <file>` and re-edit with correct alignment |
| Wrong decision text copied from Example | grep for decision keywords in the file | Compare with original decisions.md in git history |
| Gotcha miscategorized | Count rows in each section (should be 1 + 12) | Move row between tables with a follow-up edit |
| state-coverage.md has unexpected content | Read the file before using its purpose | If file is empty/unexpected, use a generic description: "Loading, empty, error, and edge-case state handling patterns" |
