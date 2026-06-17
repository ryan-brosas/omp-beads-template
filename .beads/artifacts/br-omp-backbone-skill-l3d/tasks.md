# Tasks: br-omp-backbone-skill-l3d

> **Execution note:** This task list is self-contained. Read each task's pre-read section before editing. Verify after each task before moving to the next. If a verification fails, fix only that task's file, re-verify, then continue. Do not move to the next task until the current task's verification passes entirely.

---

## 1. Hydrate project.md

### 1.1 Fill project identity, goal, success criteria, and current phase

```yaml
depends_on: []
parallel: false
conflicts_with: []
files: [".omp/memory/project/project.md"]
estimated_minutes: 10
```

**Pre-read:**
- [ ] 1.1.1 Read `.omp/memory/project/project.md` completely (all ~29 lines). Record the exact line number of every placeholder you'll replace. Confirm the file's current state matches the plan's Observable Truth #1:
  - Line 2: `updated: 2026-06-17`
  - Line 5: `# Project: <project-name>`
  - Lines 7-8: `Replace this with your actual project name.` followed by a blank line
  - Line 11: `<One sentence — what are we building and why?>`
  - Line 15: `1. **<Criterion 1>** — <measurable outcome>`
  - Line 16: `2. **<Criterion 2>** — <measurable outcome>`
  - Line 17: `3. **<Criterion 3>** — <measurable outcome>`
  - Lines ~18-20: `Keep to 3-5 criteria. Each must be verifiable...` (instruction paragraph — keep this)
  - Line 24: `- **Status:** <active | maintenance | paused>`
  - Line 25: `- **Milestone:** <what we're working toward right now>`
  - Line 26: `- **Next:** <the next concrete deliverable>`
  - Last lines: `Update this section after every milestone. An agent reading this must understand, within 3 seconds, what the project is doing right now.` (keep this)
- [ ] 1.1.2 Read `README.md` lines 1-5. Confirm the heading is `# OMP Beads Template` and the first paragraph describes an OMP-native project template with br and bv as the backbone. This confirms the project name and provides the basis for the goal text.
- [ ] 1.1.3 Read `.omp/AGENTS.md` — specifically the "Philosophy" section near the end. Note the 8 principles: YAGNI, Prune over pad, Graph-informed, Commands+skills only, Cognitive tools, Progressive disclosure, br is the backbone, bv is the brain, Agent-native. The goal text should incorporate these principles implicitly through the deliverables listed.
- [ ] 1.1.4 If any placeholder's line number differs from the plan's approximation, update your scratch note but proceed. The edits are content replacements, not line-number-dependent operations.

**Edits:**
- [ ] 1.1.5 Edit line 2: Change `updated: 2026-06-17` to `updated: 2026-06-18`. This is the frontmatter date update — it goes in all 5 files.
- [ ] 1.1.6 Edit line 5: Change `# Project: <project-name>` to `# Project: OMP Beads Template`. This is the canonical project name from README.md heading.
- [ ] 1.1.7 Edit lines ~7-8: Remove the instruction `Replace this with your actual project name.` (the line after the header). Keep one blank line between the header and `## The Goal` heading for markdown readability. Don't leave a gap that makes the file look broken.
- [ ] 1.1.8 Edit line ~11: Replace `<One sentence — what are we building and why?>` with: `An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating.`
- [ ] 1.1.9 Verify the goal text: It is one sentence. It names 4 concrete deliverables (task tracking, graph-informed planning, artifact generation, quality gating). All 4 are observable in the repo: `br` for task tracking, `bv` for graph-informed planning, `.omp/skills/` and `.omp/templates/` for artifact generation, `.omp/extensions/workflow-gate.ts` for quality gating. The phrase "OMP-native" matches the README. The phrase "br/bv-powered" matches the backbone philosophy in AGENTS.md.
- [ ] 1.1.10 Edit line ~15: Replace `1. **<Criterion 1>** — <measurable outcome>` with: `1. **Zero template placeholders** — No \`<project-name>\` or \`<!-- TODO\` markers in any \`.omp/memory/project/\` file. Verifiable with \`grep\`.`
- [ ] 1.1.11 Verify criterion 1: The criterion mentions the exact placeholder strings (`<project-name>`, `<!-- TODO`) so an agent knows what to grep for. The verification method (`grep`) is explicit. The scope (`.omp/memory/project/`) is explicit.
- [ ] 1.1.12 Edit line ~16: Replace `2. **<Criterion 2>** — <measurable outcome>` with: `2. **Valid markdown throughout** — Every memory file is valid markdown with correctly structured tables. Verifiable by reading each file.`
- [ ] 1.1.13 Verify criterion 2: "Valid markdown" means frontmatter is properly delimited, tables have consistent column counts, headings use proper `#` syntax. "Reading each file" is the verification method — an agent can visually inspect or use a markdown parser.
- [ ] 1.1.14 Edit line ~17: Replace `3. **<Criterion 3>** — <measurable outcome>` with: `3. **Agent comprehension within 3 seconds** — An agent loading this context can answer 'what is this project' immediately from project.md. Qualitative but observable.`
- [ ] 1.1.15 Verify criterion 3: This is the meta-criterion — it verifies that criteria 1 and 2 achieved their purpose. If an agent can read project.md and immediately understand what the project is, the hydration worked. It's qualitative (no number to measure) but observable (either the agent can answer or it can't).
- [ ] 1.1.16 Confirm the instruction paragraph after criterion 3 (`Keep to 3-5 criteria. Each must be verifiable — "good UX" is not verifiable. "Zero uncaught exceptions in prod for 30 days" is.`) is still present. If the edit accidentally removed it, re-insert it. This paragraph is meta-useful for template consumers who will customize their own criteria.
- [ ] 1.1.17 Edit line ~24: Replace `- **Status:** <active | maintenance | paused>` with: `- **Status:** active`
- [ ] 1.1.18 Verify status: "active" is correct — 8 beads closed in the last 7 days, design system scaffolded, commands and skills refined, Honcho memory workflow implemented, git-clean command added. The template is under active development.
- [ ] 1.1.19 Edit line ~25: Replace `- **Milestone:** <what we're working toward right now>` with: `- **Milestone:** Memory file hydration — project identity hardening`
- [ ] 1.1.20 Verify milestone: This bead IS the milestone. Naming it directly makes the project.md self-referential in a useful way — an agent reading this knows exactly what's happening right now.
- [ ] 1.1.21 Edit line ~26: Replace `- **Next:** <the next concrete deliverable>` with: `- **Next:** Audit command files for consistency with conventions`
- [ ] 1.1.22 Verify next: After memory files are authoritative (this bead), the natural next step is to verify that command files are consistent with the conventions they now reference. This is a suggested bead, not a commitment — but it's the concrete next deliverable.
- [ ] 1.1.23 Confirm the last paragraph (`Update this section after every milestone...`) is preserved. This is critical guidance for maintainers.
- [ ] 1.1.24 Confirm the frontmatter `---` delimiters are intact — lines 1 and 4 should still be `---`.
- [ ] 1.1.25 Confirm the frontmatter `purpose:` field on line 2 (`purpose: Project vision, goals, success criteria, and current phase`) is unchanged.

**Verification:**
- [ ] 1.1.26 Run: `grep '<project-name>' .omp/memory/project/project.md` — expect return code 1 (no matches). If return code 0 (match found): you missed the header edit. Re-check line 5.
- [ ] 1.1.27 Run: `grep '<!-- TODO' .omp/memory/project/project.md` — expect return code 1 (no matches). If a match: check if the goal or criteria placeholders still have `<!-- TODO: fill in -->` markers. Re-edit the corresponding line.
- [ ] 1.1.28 Run: `grep '<Criterion' .omp/memory/project/project.md` — expect return code 1. If match: one of the 3 criteria lines wasn't edited.
- [ ] 1.1.29 Run: `grep 'what we.re working toward' .omp/memory/project/project.md` — expect return code 1. If match: the milestone line wasn't edited.
- [ ] 1.1.30 Run: `grep 'OMP Beads Template' .omp/memory/project/project.md` — expect return code 0 (at least 1 match, the header). If no match: the header edit failed. Re-check line 5.
- [ ] 1.1.31 Run: `grep 'Memory file hydration' .omp/memory/project/project.md` — expect return code 0. If no match: the milestone line wasn't edited correctly.
- [ ] 1.1.32 Run: `grep 'Audit command files' .omp/memory/project/project.md` — expect return code 0. If no match: the next line wasn't edited.
- [ ] 1.1.33 Run: `grep 'updated: 2026-06-18' .omp/memory/project/project.md` — expect return code 0. If no match: the frontmatter date wasn't updated.
- [ ] 1.1.34 Run: `grep -c '^---$' .omp/memory/project/project.md` — expect exactly 2 (opening and closing frontmatter delimiters). If 0 or 1: the frontmatter was corrupted during editing. Re-read the file and fix.
- [ ] 1.1.35 Run: `grep '^# Project:' .omp/memory/project/project.md` — expect return code 0. The H1 heading must still exist.
- [ ] 1.1.36 Run: `grep '^## The Goal' .omp/memory/project/project.md` — expect return code 0. Section heading preserved.
- [ ] 1.1.37 Run: `grep '^## Success Criteria' .omp/memory/project/project.md` — expect return code 0. Section heading preserved.
- [ ] 1.1.38 Run: `grep '^## Current Phase' .omp/memory/project/project.md` — expect return code 0. Section heading preserved.
- [ ] 1.1.39 If ALL 14 verification checks (1.1.26 through 1.1.39) pass, Task 1.1 is complete. Record a PASS in your scratch note and proceed to Task 2.1.
- [ ] 1.1.40 If ANY check fails: identify which edit was wrong or missed, re-read the file to see current state, fix only the failing line, re-run just the failing check, then re-run all 14 checks.

---

## 2. Hydrate conventions.md

### 2.1 Fill project name header and Languages by Purpose table

```yaml
depends_on: ["1.1"]
parallel: false
conflicts_with: []
files: [".omp/memory/project/conventions.md"]
estimated_minutes: 10
```

**Pre-read:**
- [ ] 2.1.1 Read `.omp/memory/project/conventions.md` completely (all ~143 lines). The file is long — most of it stays unchanged. Focus on two areas: (a) the header on line ~6, (b) the "Languages by Purpose" table block starting around line ~15 with `| Purpose | Language | Notes |` and ending after the instruction paragraph "Fill in the actual languages for your project..."
- [ ] 2.1.2 Identify the exact line numbers for the 3 rows that need changing in the Languages table:
  - Backend row: Contains `<TypeScript | Go | Rust | Python>` in the Language column and `<strict? Bun? Deno?>` in the Notes column
  - Frontend row: Contains `<TypeScript | JavaScript>` in the Language column and `<React? Svelte? plain?>` in the Notes column
  - Scripts row: Contains `<Bash | Python | TypeScript>` in the Language column and `<CI, dev tooling, one-offs>` in the Notes column
- [ ] 2.1.3 Confirm that the Agent instructions row (`| Agent instructions | Markdown | Skills, commands, memory files |`) and Configuration row (`| Configuration | JSON / YAML | settings, manifests |`) already contain real content. These rows do NOT need editing. Note their line numbers to avoid accidentally touching them.
- [ ] 2.1.4 The file's remaining sections (`## Naming`, `## Skill Structure`, `## Command Structure`, `## Git`, `## Workflow`, `## Agent Conventions`, `## Honcho Memory`, `## Memory File Maintenance`, `## UI Design`) are large (~120 lines total) and must remain completely untouched. The edit scope is header + 3 table rows + frontmatter date only.

**Edits:**
- [ ] 2.1.5 Edit line 2: Change `updated: 2026-06-17` to `updated: 2026-06-18`.
- [ ] 2.1.6 Edit line ~6: Change `# Conventions: <project-name>` to `# Conventions: OMP Beads Template`.
- [ ] 2.1.7 Edit the Backend row: Replace `| Backend | <TypeScript | Go | Rust | Python> | <strict? Bun? Deno?> |` with `| Backend | N/A | Template repo — no backend runtime |`.
- [ ] 2.1.8 Rationale for Backend = N/A: This repo contains no `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`, `pyproject.toml`, or any runtime dependency manifest. It is a template that gets cloned and customized — the clone becomes a real project, but the template itself has no backend. The `/init` hydration script is Python but that's captured in the Scripts row, not Backend.
- [ ] 2.1.9 Edit the Frontend row: Replace `| Frontend | <TypeScript | JavaScript> | <React? Svelte? plain?> |` with `| Frontend | N/A | Template repo — provides design system assets only |`.
- [ ] 2.1.10 Rationale for Frontend = N/A: The repo provides `design/tokens.css`, `design/primitives.css`, `design/base.css`, and `design/craft/` as static design system assets. There is no frontend application code, no component library, no build pipeline for frontend assets. These assets are consumed by projects that clone the template — they are not a frontend application themselves.
- [ ] 2.1.11 Edit the Scripts row: Replace `| Scripts | <Bash | Python | TypeScript> | <CI, dev tooling, one-offs> |` with `| Scripts | Python | \`/init\` hydration script |`.
- [ ] 2.1.12 Rationale for Scripts = Python: The only executable code in this repo (outside OMP TypeScript extensions in `.omp/extensions/`) is the Python 3 hydration script embedded in `.omp/commands/init.md`. It uses stdlib only: `pathlib`, `json`, `os`, `re`, `subprocess`. No other scripting language has executable code in this repo. The notes field mentions `` `/init` `` specifically to guide agents to the right file.
- [ ] 2.1.13 Confirm the instruction paragraph after the language table is preserved: "Fill in the actual languages for your project. Agents use this to pick the right tool for the job." This paragraph is meta-useful — it tells template consumers what to do with this table. Do NOT remove it.
- [ ] 2.1.14 Confirm the "Languages by Purpose" section heading (`## Languages by Purpose`) is preserved. The heading is between line ~13-14.

**Verification:**
- [ ] 2.1.15 Run: `grep '<project-name>' .omp/memory/project/conventions.md` — expect return code 1. If match: header edit failed.
- [ ] 2.1.16 Run: `grep '<TypeScript' .omp/memory/project/conventions.md` — expect return code 1. If match: one of the language table rows still has an option-placeholder. Check which row (Backend, Frontend, or Scripts) and verify it was edited.
- [ ] 2.1.17 Run: `grep '<Bash' .omp/memory/project/conventions.md` — expect return code 1. Specifically the Scripts row placeholder.
- [ ] 2.1.18 Run: `grep '<JavaScript>' .omp/memory/project/conventions.md` — expect return code 1. Specifically the Frontend row placeholder.
- [ ] 2.1.19 Run: `grep '<Go' .omp/memory/project/conventions.md` — expect return code 1. Specifically the Backend row placeholder.
- [ ] 2.1.20 Run: `grep 'N/A' .omp/memory/project/conventions.md` — expect at least 2 matches. These should be the Backend and Frontend rows. If exactly 1 match: one of the two rows wasn't set to N/A. If 0 matches: neither was edited.
- [ ] 2.1.21 Run: `grep 'Backend.*N/A' .omp/memory/project/conventions.md` — expect return code 0. Backend row specifically has N/A.
- [ ] 2.1.22 Run: `grep 'Frontend.*N/A' .omp/memory/project/conventions.md` — expect return code 0. Frontend row specifically has N/A.
- [ ] 2.1.23 Run: `grep 'Scripts.*Python' .omp/memory/project/conventions.md` — expect return code 0. Scripts row says Python.
- [ ] 2.1.24 Run: `grep 'init.*hydration' .omp/memory/project/conventions.md` — expect return code 0. Scripts notes reference the init hydration script.
- [ ] 2.1.25 Run: `grep 'updated: 2026-06-18' .omp/memory/project/conventions.md` — expect return code 0.
- [ ] 2.1.26 Run: `grep -c '^---$' .omp/memory/project/conventions.md` — expect exactly 2.
- [ ] 2.1.27 Run: `grep '^# Conventions:' .omp/memory/project/conventions.md` — expect return code 0.
- [ ] 2.1.28 Run: `grep '^## Naming' .omp/memory/project/conventions.md` — expect return code 0. Major section preserved.
- [ ] 2.1.29 Run: `grep 'Agent instructions.*Markdown' .omp/memory/project/conventions.md` — expect return code 0. Agent instructions row unchanged.
- [ ] 2.1.30 Run: `grep 'Configuration.*JSON' .omp/memory/project/conventions.md` — expect return code 0. Configuration row unchanged.
- [ ] 2.1.31 Run: `grep 'Fill in the actual languages' .omp/memory/project/conventions.md` — expect return code 0. Instruction paragraph preserved.
- [ ] 2.1.32 Run: `grep -c '^## ' .omp/memory/project/conventions.md` — expect approximately 10 (all major section headings). If significantly fewer: sections were accidentally deleted. Re-read the file.
- [ ] 2.1.33 If ALL 18 verification checks pass, Task 2.1 is complete. Record PASS and proceed to Task 3.1.
- [ ] 2.1.34 If ANY check fails: re-read the file, fix only the failing line, re-run the failing check, then re-run all 18 checks.

---

## 3. Fix tech-stack.md

### 3.1 Fix header, verification commands, security commands, and broken craft references table

```yaml
depends_on: ["1.1", "2.1"]
parallel: false
conflicts_with: []
files: [".omp/memory/project/tech-stack.md", "design/craft/state-coverage.md"]
estimated_minutes: 15
```

**Pre-read:**
- [ ] 3.1.1 Read `.omp/memory/project/tech-stack.md` completely (all ~88 lines). Identify these sections and their line ranges:
  - Frontmatter: lines 1-4
  - Header: `# Tech Stack: <project-name>` (line ~6)
  - `## Runtime` table: approximately lines 8-17 (keep this — don't edit)
  - `## Key Dependencies` table: approximately lines 19-23 (keep this — don't edit)
  - `## Verification Commands` section: heading + bash code block with 5 placeholder commands (lines ~27-48)
  - `## Security` section: heading + bash code block with 2 placeholder commands (lines ~50-58)
  - `## Constraints` section: approximately lines 60-66 (keep this — don't edit)
  - `## Design Assets` table: approximately lines 68-76 (keep this — don't edit)
  - `## Craft References` section: heading + description + broken table (lines ~78-88) — THIS IS THE MAIN FIX
- [ ] 3.1.2 Note which sections are read-only (Runtime, Key Dependencies, Constraints, Design Assets) and which are edited (Header, Verification Commands, Security, Craft References). The read-only sections contain template patterns for consumers — they intentionally have `<option1 | option2>` placeholders. The PRD's `<project-name>` grep check verifies the header is fixed; the craft table fix verifies structure.
- [ ] 3.1.3 Read `design/craft/state-coverage.md`. This file exists on disk but is missing from the craft references table. Extract 3-5 keywords from its heading and first paragraph. If the file starts with a heading like `# State Coverage` or `# UI State Coverage`, use that. If it has a subtitle or introduction, extract the key concepts. Expected keywords based on the filename: states (rest, hover, focus, active, disabled, loading, empty, error), interactive elements, handling. Write down the purpose description you'll use in the table — it should be a concise, comma-separated keyword list matching the style of other craft files.
- [ ] 3.1.4 Run: `ls design/craft/` and confirm exactly 8 files exist: `accessibility-baseline.md`, `animation-discipline.md`, `anti-ai-slop.md`, `color.md`, `form-validation.md`, `state-coverage.md`, `typography.md`, `typography-hierarchy.md`. If there are more or fewer files, STOP — the plan assumes exactly 8 craft files. Report the discrepancy.

**Edits — Header:**
- [ ] 3.1.5 Edit line 2: Change `updated: 2026-06-17` to `updated: 2026-06-18`.
- [ ] 3.1.6 Edit line ~6: Change `# Tech Stack: <project-name>` to `# Tech Stack: OMP Beads Template`.

**Edits — Verification Commands bash block:**
- [ ] 3.1.7 Locate the line with `<tsc --noEmit | mypy | cargo check | go vet>`. Replace with `N/A — template repo, no compiled code`. Keep the `# Typecheck` comment line above it unchanged.
- [ ] 3.1.8 Locate the line with `<eslint | ruff | clippy | golangci-lint>`. Replace with `N/A — no linter configured for template files`. Keep the `# Lint` comment line unchanged.
- [ ] 3.1.9 Locate the line with `<vitest run | pytest | cargo test | go test ./...>`. Replace with `N/A — no test framework`. Keep the `# Test` comment line unchanged.
- [ ] 3.1.10 Locate the line with `<tsup | pip install -e . | cargo build --release | go build>`. Replace with `N/A — no build step`. Keep the `# Build` comment line unchanged.
- [ ] 3.1.11 Confirm the `# Graph state (always available)` section with `bv --robot-triage` and `br list --status open --status in_progress --json` is untouched. These commands are always valid.
- [ ] 3.1.12 If there's an instruction comment like `# Replace placeholders with your project's actual commands...` after the code block, keep it — it's useful for template consumers.

**Edits — Security Commands bash block:**
- [ ] 3.1.13 Locate the line with `<npm audit | pip-audit | cargo audit | govulncheck>`. Replace with `N/A — template repo, no runtime dependencies`. Keep the `# Dependency audit` comment line unchanged.
- [ ] 3.1.14 Locate the line with `<gitleaks detect | trufflehog filesystem .>`. Replace with `N/A — no secrets scanning configured`. Keep the `# Secrets scan (if configured)` comment line unchanged.

**Edits — Craft References table (the big fix):**
- [ ] 3.1.15 Identify the exact line range of the broken craft references block. Start: `## Craft References` heading. End: the last orphan table row (`| \`design/craft/typography-hierarchy.md\` | ... |`).
- [ ] 3.1.16 Before making this edit, copy the purpose descriptions for the existing 7 craft files into a scratch buffer so you don't lose them. The existing descriptions are:
  - typography: "Type scale, line-height, letter-spacing, font pairing, line length, weight discipline"
  - color: "Palette structure, accent discipline, contrast minimums, dark themes, semantic naming"
  - anti-ai-slop: "Seven cardinal sins, soft tells, polish tells, soul-injection rules"
  - animation-discipline: "When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits"
  - accessibility-baseline: "WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline"
  - form-validation: "Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene"
  - typography-hierarchy: "Entry points, hierarchy vectors, rhythm failure modes, controlled violations"
- [ ] 3.1.17 Replace the entire craft references block (from `## Craft References` through the last orphan row) with the unified alphabetical 8-row table + attribution paragraph. Use this exact content:

```
## Craft References

Brand-agnostic universal design rules that apply on top of any `DESIGN.md`:

| File | Purpose |
|------|---------|
| `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
| `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |
| `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
| `design/craft/state-coverage.md` | [Derived from reading the file — extract keywords from heading/intro, e.g., "UI state handling: rest, hover, focus, active, disabled, loading, empty, error"] |
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
```
- [ ] 3.1.18 For the `state-coverage.md` row: replace the bracketed placeholder `[Derived from reading the file...]` with the actual purpose description you derived in step 3.1.3. Match the style: concise, comma-separated keywords, lowercase except proper nouns.
- [ ] 3.1.19 Verify the attribution paragraph text: must contain "Adapted from Open Design's \`craft/\` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT)." — verbatim from the original file.
- [ ] 3.1.20 Verify the attribution paragraph is separated from the last table row by exactly one blank line. It should NOT be part of the table.

**Verification:**
- [ ] 3.1.21 Run: `grep '<project-name>' .omp/memory/project/tech-stack.md` — expect return code 1.
- [ ] 3.1.22 Run: `grep '<tsc' .omp/memory/project/tech-stack.md` — expect return code 1.
- [ ] 3.1.23 Run: `grep '<eslint' .omp/memory/project/tech-stack.md` — expect return code 1.
- [ ] 3.1.24 Run: `grep '<vitest' .omp/memory/project/tech-stack.md` — expect return code 1.
- [ ] 3.1.25 Run: `grep '<tsup' .omp/memory/project/tech-stack.md` — expect return code 1.
- [ ] 3.1.26 Run: `grep '<npm audit' .omp/memory/project/tech-stack.md` — expect return code 1.
- [ ] 3.1.27 Run: `grep '<gitleaks' .omp/memory/project/tech-stack.md` — expect return code 1.
- [ ] 3.1.28 Run: `grep 'N/A' .omp/memory/project/tech-stack.md` — expect at least 6 matches (typecheck, lint, test, build, dependency audit, secrets scan).
- [ ] 3.1.29 Run: `grep -c 'design/craft/' .omp/memory/project/tech-stack.md` — expect exactly 8 (one per craft file in the table).
- [ ] 3.1.30 Run: `grep 'state-coverage.md' .omp/memory/project/tech-stack.md` — expect return code 0 (the previously missing file is now listed).
- [ ] 3.1.31 Run: `grep 'Adapted from Open Design' .omp/memory/project/tech-stack.md` — expect return code 0 (attribution preserved).
- [ ] 3.1.32 Run the craft table contiguity check (Python):
```bash
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/tech-stack.md").read_text()
craft_start = text.index("## Craft References")
next_section = text.find("\n## ", craft_start + 10)
if next_section == -1: craft_block = text[craft_start:]
else: craft_block = text[craft_start:next_section]
# Check: all pipe lines are contiguous (no non-pipe/non-blank lines between them)
lines = craft_block.splitlines()
pipe_indices = [i for i, l in enumerate(lines) if l.startswith("|")]
for j in range(1, len(pipe_indices)):
    gap = pipe_indices[j] - pipe_indices[j-1]
    if gap > 1:
        between = [lines[k].strip() for k in range(pipe_indices[j-1]+1, pipe_indices[j])]
        if any(b and not b.startswith(">") for b in between):
            print(f"FAIL: non-pipe content between table rows: {between}")
            raise SystemExit(1)
# Check: attribution is AFTER the last table row
table_end = craft_block.rfind("\n|")
attr_start = craft_block.find("Adapted from Open Design")
assert attr_start != -1, "FAIL: missing attribution"
assert attr_start > table_end, f"FAIL: attribution at {attr_start} before table end at {table_end}"
print("PASS: tech-stack.md craft table structure correct")
PY
```
- [ ] 3.1.33 Run: `grep 'updated: 2026-06-18' .omp/memory/project/tech-stack.md` — expect return code 0.
- [ ] 3.1.34 Run: `grep '^## Runtime' .omp/memory/project/tech-stack.md` — expect return code 0 (section preserved).
- [ ] 3.1.35 Run: `grep '^## Key Dependencies' .omp/memory/project/tech-stack.md` — expect return code 0 (section preserved).
- [ ] 3.1.36 Run: `grep '^## Design Assets' .omp/memory/project/tech-stack.md` — expect return code 0 (section preserved).
- [ ] 3.1.37 Run: `grep '^## Constraints' .omp/memory/project/tech-stack.md` — expect return code 0 (section preserved).
- [ ] 3.1.38 Run: `grep 'bv --robot-triage' .omp/memory/project/tech-stack.md` — expect return code 0 (graph state commands preserved).
- [ ] 3.1.39 If ALL 17 verification checks pass, Task 3.1 is complete. Record PASS and proceed to Task 4.1.
- [ ] 3.1.40 If ANY check fails: re-read the file, fix only the failing section, re-run the failing check, then re-run all checks.

---

## 4. Restructure decisions.md

### 4.1 Promote 5 real decisions from Example to Decision Log, remove Example section, fix header

```yaml
depends_on: ["1.1", "2.1", "3.1"]
parallel: false
conflicts_with: []
files: [".omp/memory/project/decisions.md"]
estimated_minutes: 10
```

**Pre-read:**
- [ ] 4.1.1 Read `.omp/memory/project/decisions.md` completely (all ~34 lines). Identify these sections and their line ranges:
  - Frontmatter: lines 1-4
  - Header: `# Decisions: <project-name>` (line ~6)
  - Intro paragraph: "Every architecture decision..." (lines ~8-9)
  - `## Decision Log` heading: line ~11
  - Decision Log table header: `| # | Date | Decision | Rationale | Confidence |` (line ~12)
  - Separator: `|---|---|---|---|---|` (line ~13)
  - Placeholder row: `| 1 | <YYYY-MM> | <what we decided> | <why — tradeoffs, alternatives considered> | <High | Medium | Low> |` (line ~14)
  - Blank line(s): line ~15-16
  - `## How to Add a Decision` heading: line ~17
  - 5-step reference: lines ~18-23
  - Blank line(s): line ~24
  - `## Example` heading: line ~25
  - Example table header + separator + 5 rows: lines ~26-34
- [ ] 4.1.2 Before making ANY edits, copy the 5 decision rows from the Example section into a scratch buffer. These are the verbatim source texts. Do not paraphrase. Do not shorten. Do not "improve" the wording. Each row's text must survive character-for-character. The rows are:
  - Row 1: `| 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator. Alternatives (linear, plain markdown) lack the graph query ability. | High |`
  - Row 2: `| 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts and skill knowledge. Scripts add maintenance burden, platform dependencies, and hidden logic. | High |`
  - Row 3: `| 3 | 2026-06 | Bare command names (\`/create\`, \`/plan\`) | OMP resolves commands by directory. Prefix would be noise. | High |`
  - Row 4: `| 4 | 2026-06 | \`.omp/\` as native project root | OMP loads from \`.omp/\`. Parallel \`.pi/\` config creates confusion. | High |`
  - Row 5: `| 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages. The beads template stays pure workflow — install providers separately. | High |`
- [ ] 4.1.3 Verify each decision is real (not an example): Decision #1 matches AGENTS.md "br is the backbone / bv is the brain." Decision #2 matches AGENTS.md "Commands + skills only — no scripts, no machinery." Decision #3 is observable — all 9 commands in `.omp/commands/` are bare names. Decision #4 is observable — `.omp/` is the project root, no `.pi/` directory exists. Decision #5 is observable — `omp-makora-provider` is a separate package, not vendored in this template.
- [ ] 4.1.4 If any decision text in the file differs from what's recorded here, use the FILE'S text, not this task list's text. The file is authoritative. This task list's copies are for reference only.

**Edits:**
- [ ] 4.1.5 Edit line 2: Change `updated: 2026-06-17` to `updated: 2026-06-18`.
- [ ] 4.1.6 Edit line ~6: Change `# Decisions: <project-name>` to `# Decisions: OMP Beads Template`.
- [ ] 4.1.7 Keep the intro paragraph ("Every architecture decision that affects the shape of the project goes here. Use the table. Dates, rationale, and confidence are required.") unchanged. It's useful guidance.
- [ ] 4.1.8 In the Decision Log section: Remove the placeholder row. The table header (`| # | Date | Decision | Rationale | Confidence |`) and separator (`|---|---|---|---|---|`) stay. The placeholder row `| 1 | <YYYY-MM> | <what we decided> | ...` is deleted.
- [ ] 4.1.9 In the Decision Log section: Insert the 5 real decision rows (from step 4.1.2) after the separator row. They should appear as:
  - Row 1 (br/bv), Row 2 (commands+skills), Row 3 (bare names), Row 4 (.omp/ root), Row 5 (tooling separate)
  - Each on its own line. No blank lines between decision rows. One blank line after row 5 before the next section heading.
- [ ] 4.1.10 Check the numbering: The `# ` column should be 1, 2, 3, 4, 5 — sequential, starting from 1.
- [ ] 4.1.11 Remove the entire "## Example" section. Remove:
  - The `## Example` heading line
  - The example table header row (`| # | Date | Decision | Rationale | Confidence |`)
  - The separator row
  - All 5 decision rows (they're already in the Decision Log now)
  - Any trailing blank lines after the Example section
- [ ] 4.1.12 After removing the Example section, the document should flow: Decision Log table (header + separator + 5 rows) → one blank line → `## How to Add a Decision` heading → 5-step content. There should be exactly one blank line between the last Decision Log row and the How to Add heading.
- [ ] 4.1.13 Confirm the "## How to Add a Decision" section is present and its 5 steps are unchanged. The steps should be: (1) Assign next sequential #, (2) Date = month of decision, (3) Decision = one sentence, (4) Rationale = what we rejected/accepted/why, (5) Confidence = High/Medium/Low.
- [ ] 4.1.14 Verify there is no blank line between the Decision Log table header and separator, and no blank line between the separator and the first decision row. Markdown tables should be compact.

**Verification:**
- [ ] 4.1.15 Run: `grep '<project-name>' .omp/memory/project/decisions.md` — expect return code 1.
- [ ] 4.1.16 Run: `grep -c '^| [1-5] |' .omp/memory/project/decisions.md` — expect exactly 5. This counts decision rows 1-5.
- [ ] 4.1.17 Run: `grep '<YYYY-MM>' .omp/memory/project/decisions.md` — expect return code 1 (placeholder date removed).
- [ ] 4.1.18 Run: `grep '<what we decided>' .omp/memory/project/decisions.md` — expect return code 1 (placeholder decision removed).
- [ ] 4.1.19 Run: `grep '<why — tradeoffs' .omp/memory/project/decisions.md` — expect return code 1 (placeholder rationale removed).
- [ ] 4.1.20 Run: `grep '<High | Medium | Low>' .omp/memory/project/decisions.md` — expect return code 1 (placeholder confidence removed).
- [ ] 4.1.21 Run: `grep -c '## Example' .omp/memory/project/decisions.md` — expect exactly 0. The Example heading must be gone.
- [ ] 4.1.22 Run: `grep -c '## Decision Log' .omp/memory/project/decisions.md` — expect exactly 1. One Decision Log heading.
- [ ] 4.1.23 Run: `grep -c '## How to Add a Decision' .omp/memory/project/decisions.md` — expect exactly 1. One How to Add heading.
- [ ] 4.1.24 Run the decision content preservation check (Python):
```bash
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/decisions.md").read_text()
assert "Use br/bv for task tracking and graph intelligence" in text, "FAIL: decision 1"
assert "Commands + skills only, no scripts" in text, "FAIL: decision 2"
assert "Bare command names" in text, "FAIL: decision 3"
assert ".omp/ as native project root" in text, "FAIL: decision 4"
assert "Ergonomic tooling lives in separate template repos" in text, "FAIL: decision 5"
assert "Graph-informed workflow is the template's core differentiator" in text, "FAIL: rationale 1"
assert "Every gap solvable through better prompts and skill knowledge" in text, "FAIL: rationale 2"
assert "OMP resolves commands by directory" in text, "FAIL: rationale 3"
assert "OMP loads from `.omp/`" in text, "FAIL: rationale 4"
assert "omp-makora-provider" in text, "FAIL: rationale 5"
print("PASS: all 5 decisions and rationales preserved verbatim")
PY
```
- [ ] 4.1.25 Run: `grep 'updated: 2026-06-18' .omp/memory/project/decisions.md` — expect return code 0.
- [ ] 4.1.26 Run: `grep -c '^---$' .omp/memory/project/decisions.md` — expect exactly 2.
- [ ] 4.1.27 If ALL 12 verification checks pass, Task 4.1 is complete. Record PASS and proceed to Task 5.1.
- [ ] 4.1.28 If ANY check fails: re-read the file, fix only the failing section, re-run the failing check, then re-run all checks.

---

## 5. Restructure gotchas.md

### 5.1 Separate project-specific gotchas from template-universal gotchas, fix header

```yaml
depends_on: ["1.1", "2.1", "3.1", "4.1"]
parallel: false
conflicts_with: []
files: [".omp/memory/project/gotchas.md"]
estimated_minutes: 10
```

**Pre-read:**
- [ ] 5.1.1 Read `.omp/memory/project/gotchas.md` completely (all ~44 lines). Identify these sections and line ranges:
  - Frontmatter: lines 1-4
  - Header: `# Gotchas: <project-name>` (line ~6)
  - Intro paragraph: "Every entry must include impact and mitigation..." (lines ~8-9)
  - `## Active Warnings` heading: line ~11
  - Active Warnings description: "Every entry must include..." (line ~12)
  - Active Warnings table header: `| Date | Area | Gotcha | Impact | Mitigation |` (line ~13)
  - Separator: `|------|------|--------|--------|------------|` (line ~14)
  - Placeholder row: `| <YYYY-MM> | <area> | <what happens> | <why it matters> | <how to avoid or recover> |` (line ~15)
  - Blank line(s): lines ~16-17
  - `## Template Bootstrap Gotchas` heading: line ~18
  - Description paragraph: "These are the gotchas that come with the template itself..." (line ~19)
  - Table header + separator: lines ~20-21
  - 12 data rows: lines ~22-33 (the "memory templates waste tokens" row is one of these — identify which line number it is)
  - Blank line(s): lines ~34-35
  - `## How to Add a Gotcha` heading: line ~36
  - 5-step reference + "Remove entries" note: lines ~37-44
- [ ] 5.1.2 Identify exactly which row is the "memory templates waste tokens" entry. Its text is: `| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session | Fill with real project content immediately. Delete placeholder gotchas when real ones exist. |`. Note its line number — this is the row that will move to Active Warnings.
- [ ] 5.1.3 Verify the other 11 entries are template-universal. Skim each one: if it describes a gotcha that would apply to a fresh project cloning this template (workflow gate behavior, br/bv initialization, model variance, etc.), it's template-universal. The "memory templates waste tokens" entry is the only one that describes THIS repo's specific maintenance problem.

**Edits:**
- [ ] 5.1.4 Edit line 2: Change `updated: 2026-06-17` to `updated: 2026-06-18`.
- [ ] 5.1.5 Edit line ~6: Change `# Gotchas: <project-name>` to `# Gotchas: OMP Beads Template`.

**Edits — Active Warnings section:**
- [ ] 5.1.6 Remove the placeholder row from the Active Warnings table. Keep the table header and separator.
- [ ] 5.1.7 Insert the project-specific gotcha into Active Warnings. Use the exact text from the Template Bootstrap entry, but update the mitigation:
  - Date: `2026-06` (unchanged)
  - Area: `memory` (unchanged)
  - Gotcha: `Memory templates waste tokens if left as placeholders` (unchanged)
  - Impact: `~1KB of template text the agent reads every session — compounds across sessions` (unchanged except trailing description)
  - Mitigation: `Fill with real project content immediately. This bead (br-omp-backbone-skill-l3d) addresses the initial hydration. Audit memory files during /close.` (UPDATED — references this bead, removes "Delete placeholder gotchas when real ones exist" which is now redundant since the Active Warnings entry IS a real gotcha)
- [ ] 5.1.8 The Active Warnings table should now have: header row, separator row, 1 data row. No placeholder row.

**Edits — Template Bootstrap Gotchas section:**
- [ ] 5.1.9 After the description paragraph ("These are the gotchas that come with the template itself. Replace with your project's actual gotchas as you discover them."), insert a blockquote note on a new line:
```
> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.
```
- [ ] 5.1.10 Ensure there is a blank line between the description paragraph and the blockquote, and a blank line between the blockquote and the table header.
- [ ] 5.1.11 Remove the "memory templates waste tokens" row from the Template Bootstrap table. The table should now have header + separator + 11 data rows.
- [ ] 5.1.12 Confirm the remaining 11 entries are in their original order. Do not reorder them. The original order is:
  1. workflow gate only understands active bead
  2. gate blocks edit/write but shell bypasses
  3. implementing without bead or plan
  4. assuming requirements without reading PRD
  5. commands are prompt templates
  6. OMP loads from .omp/
  7. bv requires git history
  8. bv requires br data
  9. stale memory is worse than no memory
  10. lazy/small models skip steps
  11. loading domain-specific skills in wrong project
  (Note: entry #9 in the original was "memory templates waste tokens" — it's removed. The original #10 and #11 become #9 and #10 in the new table. The original #12 becomes #11.)

**Edits — How to Add a Gotcha section:**
- [ ] 5.1.13 Confirm this section is present entirely unchanged. It should have the heading `## How to Add a Gotcha` and 5 numbered steps plus the note "Remove entries once the underlying bug is fixed. Keep entries for ongoing design constraints."

**Verification:**
- [ ] 5.1.14 Run: `grep '<project-name>' .omp/memory/project/gotchas.md` — expect return code 1.
- [ ] 5.1.15 Run: `grep '<YYYY-MM>' .omp/memory/project/gotchas.md` — expect return code 1.
- [ ] 5.1.16 Run: `grep '<area>' .omp/memory/project/gotchas.md` — expect return code 1.
- [ ] 5.1.17 Run: `grep '<what happens>' .omp/memory/project/gotchas.md` — expect return code 1.
- [ ] 5.1.18 Run: `grep 'These gotchas ship with the OMP Beads Template' .omp/memory/project/gotchas.md` — expect return code 0.
- [ ] 5.1.19 Run: `grep 'br-omp-backbone-skill-l3d' .omp/memory/project/gotchas.md` — expect return code 0. This bead ID is referenced in the mitigation.
- [ ] 5.1.20 Run: `grep -c '## Active Warnings' .omp/memory/project/gotchas.md` — expect exactly 1.
- [ ] 5.1.21 Run: `grep -c '## Template Bootstrap Gotchas' .omp/memory/project/gotchas.md` — expect exactly 1.
- [ ] 5.1.22 Run: `grep -c '## How to Add a Gotcha' .omp/memory/project/gotchas.md` — expect exactly 1.
- [ ] 5.1.23 Run the gotcha content preservation check (Python):
```bash
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/gotchas.md").read_text()
phrases = [
    "workflow gate only understands the active bead",
    "shell-based mutation bypasses",
    "Implementing without a bead or plan",
    "Assuming requirements without reading PRD",
    "Commands are prompt templates",
    "OMP loads from `.omp/`",
    "bv requires git history",
    "bv requires br data",
    "Stale memory is worse than no memory",
    "Lazy/small models skip steps",
    "Loading domain-specific skills",
    "Memory templates waste tokens",
]
for phrase in phrases:
    assert phrase in text, f"FAIL: missing gotcha '{phrase[:40]}...'"
print("PASS: all 12 gotcha entries preserved")
PY
```
- [ ] 5.1.24 Run: `grep 'updated: 2026-06-18' .omp/memory/project/gotchas.md` — expect return code 0.
- [ ] 5.1.25 Run: `grep -c '^---$' .omp/memory/project/gotchas.md` — expect exactly 2.
- [ ] 5.1.26 Manually verify: The "memory templates waste tokens" entry appears exactly once in the file (in Active Warnings, not duplicated in Template Bootstrap). Skim both tables to confirm.
- [ ] 5.1.27 If ALL 13 verification checks pass, Task 5.1 is complete. Record PASS and proceed to Wave 6.
- [ ] 5.1.28 If ANY check fails: re-read the file, fix only the failing section, re-run the failing check, then re-run all checks.

---

## 6. Full Verification

### 6.1 End-to-end verification of all memory files

```yaml
depends_on: ["1.1", "2.1", "3.1", "4.1", "5.1"]
parallel: false
conflicts_with: []
files: [".omp/memory/project/project.md", ".omp/memory/project/conventions.md", ".omp/memory/project/tech-stack.md", ".omp/memory/project/decisions.md", ".omp/memory/project/gotchas.md"]
estimated_minutes: 10
```

This task runs the complete verification suite against all 5 files. It combines all per-wave checks plus cross-file checks. Every acceptance criterion from the PRD is covered.

**Cross-file identity check (AC7):**
- [ ] 6.1.1 Run: `grep -r '<project-name>' .omp/memory/project/` — expect return code 1 (no matches across ALL 5 files). If any match: identify which file still has the placeholder and re-run that file's task verification.

**Per-file re-verification (AC1-AC6):**
- [ ] 6.1.2 Run project.md checks (AC1): `grep '<project-name>\|<!-- TODO\|<Criterion' .omp/memory/project/project.md` — expect return code 1.
- [ ] 6.1.3 Run conventions.md checks (AC2): `grep '<TypeScript\|<Bash\|<JavaScript>\|<Go' .omp/memory/project/conventions.md` — expect return code 1.
- [ ] 6.1.4 Run tech-stack.md craft table contiguity check (AC3): Use Python script from 3.1.32.
- [ ] 6.1.5 Run tech-stack.md verification commands check (AC4): `grep '<tsc\|<eslint\|<vitest\|<tsup\|<npm audit\|<gitleaks' .omp/memory/project/tech-stack.md` — expect return code 1.
- [ ] 6.1.6 Run decisions.md structure check (AC5): Use Python script from 4.1.24.
- [ ] 6.1.7 Run gotchas.md structure check (AC6): `grep 'These gotchas ship with the OMP Beads Template' .omp/memory/project/gotchas.md` — expect return code 0. `grep 'br-omp-backbone-skill-l3d' .omp/memory/project/gotchas.md` — expect return code 0.

**Markdown validity check (AC8):**
- [ ] 6.1.8 Run markdown structure check (Python):
```bash
python3 - <<'PY'
from pathlib import Path
base = Path(".omp/memory/project")
for fname in ["project.md", "conventions.md", "tech-stack.md", "decisions.md", "gotchas.md"]:
    text = (base / fname).read_text()
    assert text.startswith("---"), f"FAIL: {fname} no frontmatter"
    end = text.find("---", 3)
    assert end != -1, f"FAIL: {fname} unclosed frontmatter"
    assert "# " in text, f"FAIL: {fname} no heading"
print("PASS: all memory files structurally valid")
PY
```

**Content preservation checks (AC9, AC10):**
- [ ] 6.1.9 Run decisions content preservation check (AC9): Use Python script from 4.1.24.
- [ ] 6.1.10 Run gotchas content preservation check (AC10): Use Python script from 5.1.23.

**br/bv health:**
- [ ] 6.1.11 Run: `ACTOR="${BR_ACTOR:-assistant}" br sync --flush-only` — expect no errors (nothing to export or successful sync).
- [ ] 6.1.12 Run: `br dep cycles --json` — expect empty output or `[]` (no cycles).

**Git diff scope check:**
- [ ] 6.1.13 Run: `git diff --stat .omp/memory/project/` — expect exactly 5 files changed, all starting with `.omp/memory/project/`. If more or fewer files: identify what else changed and why.
- [ ] 6.1.14 Run: `git diff -- .omp/commands/ .omp/templates/ .omp/skills/ .omp/AGENTS.md .omp/RULES.md DESIGN.md design/ README.md .gitignore` — expect empty output (no diff). If any diff: scope bleed detected. Identify the changed file and revert it with `git checkout -- <file>`.
- [ ] 6.1.15 Run: `wc -l .omp/memory/project/*.md` and compare against expected approximate sizes:
  - project.md: ~30 lines (was ~29, slight growth from goal text expansion)
  - conventions.md: ~143 lines (same — placeholder lengths were similar)
  - tech-stack.md: ~88 lines (same — restructured but same content volume)
  - decisions.md: ~30 lines (was ~34, slight reduction from removing Example section)
  - gotchas.md: ~46 lines (was ~44, slight growth from blockquote addition)
  - If any file is dramatically different (e.g., 10 lines or 200 lines), investigate.

**Final PASS/FAIL tally:**
- [ ] 6.1.16 Count all PASS results from checks 6.1.1 through 6.1.15. Expected: 15-16 PASS, 0 FAIL.
- [ ] 6.1.17 If ALL checks pass: the bead is ready for `/verify`. Record all PASS results for the completion-evidence.json.
- [ ] 6.1.18 If ANY check fails: identify the failing file(s), re-read each failing file, apply the fix, re-run the specific failing check, then re-run the full suite from 6.1.1.
- [ ] 6.1.19 Maximum 3 fix cycles. If a check still fails after 3 attempts, STOP and escalate — don't loop indefinitely.
