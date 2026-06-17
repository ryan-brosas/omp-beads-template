# Context Capsule: br-omp-backbone-skill-l3d

> **Purpose:** Self-contained handoff for the `/ship` agent. Read this capsule first, then follow `tasks.md` for the step-by-step execution. Do not read the PRD during `/ship` — this capsule and the plan are complete.

---

## Objective

Hydrate the 5 template memory files under `.omp/memory/project/` with real project identity. These
files were written by `/init` with placeholder text (`<project-name>`, `<!-- TODO: fill in -->`,
`<option1 | option2>` markers) and have never been updated since template bootstrap. Every agent
session loads this placeholder noise — `grep -r '<project-name>' .omp/memory/project/` currently
returns 5 matches (one per file). The fix replaces all placeholders with concrete content derived
from README.md and observable repo state, fixes a broken markdown table in `tech-stack.md` (3 orphan
rows after an attribution paragraph plus a missing file entry), promotes 5 real architecture
decisions from an "Example" section to the actual "Decision Log" (removing the redundancy), and
separates project-specific gotchas from template-universal gotchas with a consumer-facing blockquote
note. After this bead, an agent loading the context can answer "what is this project" within 3
seconds — currently impossible because `project.md` literally says `<project-name>`.

The work is a chore (P2, 45-minute estimate, 52-minute bv forecast at confidence 0.4). No compiled
code changes. No dependencies in either direction — all 9 beads in the graph are orphans with
density 0. The blast radius is exactly 5 markdown files with no cross-file references. Each file is
edited independently in sequential waves (1 through 5) with per-wave verification gates, followed by
a full cross-file verification in wave 6.

### Why This Matters

The OMP Beads Template is the project that teaches other repos how to hydrate their memory files via
`/init`. But it hasn't dogfooded its own hydration. The gap widens with every new feature added to
the template — design system (19 files, 1,907 lines), Honcho memory workflow, git-clean command —
while its own memory files still claim it's `<project-name>`. Template consumers see this gap and
reasonably ask: "If the template can't dogfood its own hydration, why should I trust it?" This bead
closes that gap.

The PRD quantifies the impact: 19 discrete placeholder issues across 5 files (~330 tokens of noise
per agent session). At 10 sessions per repo lifetime, that's ~3,300 wasted tokens just from template
cruft — and each session typically involves multiple agent turns, each reloading the context.

---

## Key Patterns

### 1. Memory file frontmatter

Every memory file uses a YAML-style frontmatter block delimited by `---` on its own line. The block
has exactly two fields:
- `purpose:` — a one-line description of the file's role (e.g., "Project vision, goals, success
criteria, and current phase")
- `updated:` — a YYYY-MM-DD date of last modification

**Rule:** The `purpose` field must NOT change — it's the file's identity. The `updated` date MUST
change from `2026-06-17` to `2026-06-18` (today) in all 5 files. This is the only frontmatter
change.

**Reference:** `.omp/memory/project/project.md` lines 1-4 for the canonical frontmatter pattern. The
same pattern appears in all 5 files.

**Example:**
```
---
purpose: Project vision, goals, success criteria, and current phase
updated: 2026-06-18
---
```

### 2. Placeholder replacement, not section addition

The memory files serve a dual role: (1) they are this project's own documentation, and (2) they are
template examples for consumers who clone the repo. Because of role #2, the file structure
(headings, sections, instruction paragraphs) must survive intact. Template consumers need to see the
full structure to know what to fill in.

**Rule:** Replace placeholder text with concrete text in-place. Do NOT add new top-level sections
(no new `##` headings). Do NOT remove existing sections except where the PRD explicitly authorizes
removal (the "Example" section in decisions.md — because its content is migrated, not lost).
Instruction paragraphs like "Fill in the actual languages for your project" stay because they guide
template consumers.

**Anti-pattern:** "While I'm here, I'll add a section about X." Don't. The PRD scope is explicit.

**Reference:** `.omp/memory/project/project.md` for the section structure that must survive after editing.

### 3. README.md as canonical identity source

The project name and goal description are NOT invented. They are derived from the repo's own
README.md, which is the public-facing canonical description.

**Rule:** The project name is the README's first H1 heading: `# OMP Beads Template`. The goal
description incorporates the README's first paragraph ("OMP-native project template with br and bv
as the backbone of planning, execution, verification, and review") expanded with concrete
deliverables observable in the repo structure: task tracking (br database), graph-informed planning
(bv commands), artifact generation (.omp/skills/ and .omp/templates/), quality gating
(.omp/extensions/workflow-gate.ts).

**Anti-pattern:** Inventing a project name or goal that sounds better but doesn't match the README.
If the README says "OMP Beads Template," don't write "OMP Workflow Framework" because you think it
sounds more professional.

**Reference:** `README.md` lines 1-5 for the canonical heading and description.

### 4. Markdown table structure rules

Tables in these memory files use standard GitHub-Flavored Markdown pipe syntax:

```
| Header1 | Header2 | Header3 |
|---------|---------|---------|
| data1   | data2   | data3   |
```

**Critical rules for the tech-stack.md craft table fix:**
- A table is a contiguous block: header row, separator row, data rows. No non-table content between rows.
- Attribution paragraphs, descriptions, and notes that reference a table must appear BEFORE or AFTER
the table, never between data rows.
- All data rows must have the same number of columns as the header.
- An attribution paragraph is NOT a table row — it should not start with `|`.

**The bug being fixed:** The current craft table has 4 valid data rows, then an attribution
paragraph ("Adapted from Open Design..."), then 3 orphan data rows with no header. This renders as:
valid 4-row table, then a paragraph, then 3 lines of broken markdown that look like table rows but
aren't because there's no header above them.

**The fix:** Create exactly ONE contiguous table with header + separator + 8 data rows (alphabetical
order). Place the attribution paragraph AFTER the table, separated by a blank line.

**Reference:** `.omp/memory/project/tech-stack.md` lines 78-88 for the broken table.
`.omp/memory/project/conventions.md` "Languages by Purpose" table for a well-formed table example.

### 5. Decision log format

Each architecture decision is a table row with 5 columns:

```
| # | Date | Decision | Rationale | Confidence |
|---|------|----------|-----------|------------|
| 1 | 2026-06 | Use br/bv for task tracking... | Graph-informed workflow is... | High |
```

**Column meanings:**
- `#` — Sequential number starting from 1. When adding new decisions, use the next number.
- `Date` — Month of decision in `YYYY-MM` format. Month precision is sufficient for architecture decisions.
- `Decision` — One sentence. Concrete, not abstract. "Use br/bv for task tracking and graph
intelligence" not "Choose good tools."
- `Rationale` — What we rejected, what we accepted, and why. Enough detail that someone 6 months
later can follow the reasoning without asking. Include tradeoffs and alternatives considered.
- `Confidence` — One of: `High` (multiple sources confirmed), `Medium` (strong consensus but one
uncertainty), `Low` (experiment, subject to change).

**Rule:** The 5 decisions currently in the "Example" section are real. Their text, rationale, and
confidence are verbatim — copy character-for-character. Do not "improve" the wording. Do not add new
rationale. Do not change confidence levels. If the file's text differs from what the plan records,
the file is authoritative.

**Reference:** `.omp/memory/project/decisions.md` "Example" section for the exact 5 decision texts.
The "How to Add a Decision" section for the format specification.

### 6. Gotcha entry format

Each gotcha is a table row with 5 columns:

```
| Date | Area | Gotcha | Impact | Mitigation |
|------|------|--------|--------|------------|
| 2026-06 | memory | Memory templates waste tokens... | ~1KB of template text... | Fill with real project content... |
```

**Column meanings:**
- `Date` — When discovered (`YYYY-MM`).
- `Area` — The subsystem affected: `workflow`, `bv`, `br`, `memory`, `commands`, `skills`, `omp`,
`models`, `git`, or a project-specific component name.
- `Gotcha` — What happens. Be specific: "bv returns empty until at least one commit exists" not "bv is broken."
- `Impact` — Concrete consequence: "Graph queries fail silently" not "bad."
- `Mitigation` — Actionable: something the next person can DO. "Create at least one commit before
relying on bv" not "be careful."

**Rule:** The 12 existing gotcha entries must all survive. The "memory templates waste tokens" entry
moves from Template Bootstrap to Active Warnings. Its mitigation text is updated to reference this
bead ID (`br-omp-backbone-skill-l3d`). All other 11 entries are verbatim — no text changes, no
reordering.

**Reference:** `.omp/memory/project/gotchas.md` "Template Bootstrap Gotchas" table for the exact 12
entry texts. The "How to Add a Gotcha" section for the format specification.

### 7. Idempotency is not a concern

The memory files are static markdown, not generated code. No automated process regenerates them. The
`/init` command's Phase 2.5 (the Python hydration script) would regenerate them from templates IF
run again — but `/init` is only run once during project bootstrap. No CI pipeline, no git hook, no
scheduled job touches these files.

**Rule:** Do NOT run `/init` during `/ship`. It would regenerate placeholder-filled memory files and
undo this bead's work. There's no reason to run it — you're editing markdown, not re-initializing
the project.

**Anti-pattern:** "Let me run `/init` to make sure everything is consistent." No. `/init` writes
fresh templates with placeholders. Your edits would be overwritten.

**Reference:** `.omp/commands/init.md` Phase 2.5 for the `/init` hydration logic.

### 8. Scope boundary: memory files only

The blast radius is exactly 5 files under `.omp/memory/project/`. Your `edit` and `write` tool calls
must target only these 5 paths:

1. `.omp/memory/project/project.md`
2. `.omp/memory/project/conventions.md`
3. `.omp/memory/project/tech-stack.md`
4. `.omp/memory/project/decisions.md`
5. `.omp/memory/project/gotchas.md`

**Rule:** If a tool call would write to ANY other path, abort that call. The PRD explicitly
excludes: `.omp/commands/init.md`, `.omp/templates/`, `.omp/skills/`, `.omp/AGENTS.md`,
`.omp/RULES.md`, `DESIGN.md`, `design/`, `README.md`, `.gitignore`.

**Exception:** Reading `README.md` is allowed (for identity derivation). Reading
`design/craft/state-coverage.md` is allowed (for purpose description). Reading `.omp/AGENTS.md` is
allowed (for philosophy context). All other files outside `.omp/memory/project/` should only be read
if absolutely necessary for verification.

**Reference:** PRD "Out of Scope" section for the full exclusion list. Plan "Required Artifacts"
table for the file status.

### 9. Content preservation is mandatory

The 5 decisions in decisions.md and all 12 gotchas in gotchas.md are institutional knowledge. They
must survive the restructure unchanged except where the PRD explicitly authorizes modification.

**Decisions:** Copy verbatim from Example section to Decision Log. The content moves; it does not
change. Verify preservation with Python assertion checks (provided in tasks.md Wave 6).

**Gotchas:** The "memory templates waste tokens" entry moves from Template Bootstrap to Active
Warnings. Its mitigation text is updated from "Delete placeholder gotchas when real ones exist" to
"Fill with real project content immediately. This bead (br-omp-backbone-skill-l3d) addresses the
initial hydration. Audit memory files during /close." All other text in that entry (Date, Area,
Gotcha, Impact) is verbatim. The other 11 entries are entirely verbatim — no text changes, no
reordering, no "clarification" edits.

**Rule:** If you're tempted to "improve" a decision's rationale or "clarify" a gotcha's impact,
don't. The PRD scope is structure and identity, not content revision. Content revision is a separate
bead.

**Reference:** `.omp/memory/project/decisions.md` Example section. `.omp/memory/project/gotchas.md`
Template Bootstrap table.

### 10. Verification-first editing discipline

Before any edit to a file, read the file to anchor current line numbers. After the edit, run the
verification checks for that file before moving to the next file. The plan's "Observable Truths"
section describes the pre-edit state of each file — use it as a checklist to confirm you're editing
the right things.

**Rule:** Read → Confirm → Edit → Verify → Next. Never: Read once at the start and edit all 5 files
from memory. Line numbers shift between edits because you're inserting text longer than the
placeholders.

**Recovery rule:** If a verification check fails, fix only the file that failed. Re-run just that
check to confirm the fix. Then re-run all checks for that file. Then proceed to the next file.

**Reference:** Plan "Observable Truths" (items 1-5) for pre-edit state. Tasks.md per-task
verification steps for post-edit checks.

### 11. No new content creation

This bead fills placeholders and fixes structure. It does NOT:
- Add new gotchas (beyond the existing 12)
- Add new decisions (beyond the existing 5)
- Add new sections to any file
- Add new factual claims not verifiable in the repo
- Change the meaning of existing content

**Rule:** Every claim in the edited memory files has a verifiable source in the repo. The goal text
comes from README.md. The success criteria describe this bead's own outcome. The current phase
status ("active") is supported by 8 closed beads in 7 days. The milestone IS this bead. The next
deliverable (audit command files) is a natural next step.

**Anti-pattern:** "This project also does X, I'll add that to the goal." If it's not in the PRD
approach section, don't add it.

**Reference:** PRD "In Scope" for what this bead does. PRD "Out of Scope" for what it doesn't.

### 12. Sequential waves with rollback safety

The plan structures work into 6 waves:
- Wave 1: project.md
- Wave 2: conventions.md
- Wave 3: tech-stack.md
- Wave 4: decisions.md
- Wave 5: gotchas.md
- Wave 6: full verification

**Why sequential?** Each file is logically independent — no cross-file references exist between
memory files. They could run in parallel. But sequential waves provide:
1. **Recovery surface:** If a file edit is wrong, only one file needs reverting via `git checkout -- <file>`, not all 5.
2. **Incremental confidence:** Each wave verified means progress is banked. You never have to roll back all 5 files.
3. **Context preservation:** Reading and editing 5 files simultaneously risks holding stale
snapshots in the context window.

**Rule:** Do not skip ahead. Complete Wave 1 verification → Wave 2 → Wave 3 → Wave 4 → Wave 5 → Wave
6. If you discover that a later wave's edit depends on an earlier wave's content (it shouldn't —
they're independent), note it and continue.

**Reference:** Plan "Why Sequential Waves" for the design rationale.

### 13. Craft file table alphabetization

The tech-stack.md craft references table should list files in alphabetical order. This makes it easy
to check if a file is listed and easy to insert new craft files in the future.

**Rule:** The fixed table order is:
1. `design/craft/accessibility-baseline.md`
2. `design/craft/animation-discipline.md`
3. `design/craft/anti-ai-slop.md`
4. `design/craft/color.md`
5. `design/craft/form-validation.md`
6. `design/craft/state-coverage.md`
7. `design/craft/typography.md`
8. `design/craft/typography-hierarchy.md`

**Reference:** `ls design/craft/` output for the complete file listing.

### 14. Blockquote for consumer guidance

The gotchas.md "Template Bootstrap Gotchas" section needs a clear visual marker that these entries
ship with the template and should be replaced by consumers. Use a markdown blockquote (`> `).

**Rule:** Insert `> These gotchas ship with the OMP Beads Template. They apply to any project using
this template. Replace with your project's actual gotchas as you discover them.` between the
description paragraph and the table, with blank lines above and below.

**Reference:** The blockquote will be the only `>` line in any memory file. It introduces no new
markdown syntax that agents can't parse.

---

## Constraints

### MUST (20 items — hard boundaries, violations block `/review`)

1. MUST replace all `<project-name>` placeholders with "OMP Beads Template" across all 5 files.
Final check: `grep -r '<project-name>' .omp/memory/project/` returns zero matches.
2. MUST replace all `<!-- TODO: fill in -->` markers in project.md with concrete text. The goal, 3
success criteria, status, milestone, and next deliverable all get real text.
3. MUST fill the Languages by Purpose table in conventions.md: Backend = N/A, Frontend = N/A,
Scripts = Python. Agent instructions and Configuration rows are unchanged.
4. MUST fix the craft references table in tech-stack.md: one contiguous 8-row table (header +
separator + 8 data rows in alphabetical order), attribution paragraph AFTER the table.
5. MUST replace verification command placeholders in tech-stack.md: typecheck, lint, test, build →
"N/A — template repo, no compiled code" (and variants). Security: dependency audit, secrets scan →
"N/A — template repo, no runtime dependencies" / "N/A — no secrets scanning configured".
6. MUST keep `bv --robot-triage` and `br list --status open --status in_progress --json` in
tech-stack.md under "Graph state (always available)."
7. MUST move 5 decisions from Example section to Decision Log section in decisions.md. Content verbatim.
8. MUST remove the entire "## Example" section from decisions.md (heading, table header, separator, 5 rows).
9. MUST remove the placeholder row from the Decision Log table.
10. MUST move the "memory templates waste tokens" gotcha from Template Bootstrap to Active Warnings.
11. MUST add blockquote note in Template Bootstrap Gotchas: `> These gotchas ship with the OMP Beads
Template. They apply to any project using this template. Replace with your project's actual gotchas
as you discover them.`
12. MUST preserve all 5 decision texts, rationales, and confidence levels verbatim.
13. MUST preserve all 12 gotcha entries — 1 in Active Warnings (with updated mitigation), 11 in
Template Bootstrap (verbatim).
14. MUST update `updated:` frontmatter date to `2026-06-18` in all 5 files.
15. MUST keep every memory file as valid markdown: frontmatter delimited, headings present, tables
with consistent column counts, no orphan rows.
16. MUST keep "How to Add a Decision" section in decisions.md unchanged.
17. MUST keep "How to Add a Gotcha" section in gotchas.md unchanged.
18. MUST keep instruction/guidance paragraphs useful for template consumers.
19. MUST read each target file before editing it.
20. MUST read `design/craft/state-coverage.md` to derive its purpose description for the craft table.

### SHOULD (7 items — best practices, not blocking)

1. SHOULD verify each file immediately after editing before moving to the next wave.
2. SHOULD keep edits minimal — don't reformat unchanged sections.
3. SHOULD record line numbers edited for the diff scope check.
4. SHOULD derive goal text from README.md first paragraph.
5. SHOULD alphabetize the craft references table.
6. SHOULD update the meta-gotcha mitigation to reference this bead ID.
7. SHOULD NOT run `/init` during `/ship`.

### MUST NOT (20 items — violations are scope bleed)

1. MUST NOT edit `.omp/commands/init.md`
2. MUST NOT edit `.omp/templates/`
3. MUST NOT edit `.omp/skills/`
4. MUST NOT edit `.omp/AGENTS.md`
5. MUST NOT edit `.omp/RULES.md`
6. MUST NOT edit `DESIGN.md`
7. MUST NOT edit `design/` (except read `design/craft/state-coverage.md`)
8. MUST NOT edit `README.md`
9. MUST NOT edit `.gitignore`
10. MUST NOT add new top-level sections to any memory file
11. MUST NOT change existing decision rationale or confidence values
12. MUST NOT add new gotcha entries
13. MUST NOT delete any existing gotcha entry
14. MUST NOT add new memory files
15. MUST NOT change frontmatter `purpose:` field
16. MUST NOT reformat unchanged sections
17. MUST NOT run destructive commands on memory files
18. MUST NOT create `.pi/` directory or move files out of `.omp/`
19. MUST NOT modify Runtime table in tech-stack.md
20. MUST NOT modify Key Dependencies table in tech-stack.md

---

## File Ownership

| Task | Edit | Read | Forbidden |
|------|------|------|-----------|
| 1.1 | `.omp/memory/project/project.md` | `README.md`, `.omp/AGENTS.md` | All others |
| 2.1 | `.omp/memory/project/conventions.md` | — | All others |
| 3.1 | `.omp/memory/project/tech-stack.md` | `design/craft/state-coverage.md` | All others |
| 4.1 | `.omp/memory/project/decisions.md` | — | All others |
| 5.1 | `.omp/memory/project/gotchas.md` | — | All others |
| 6.1 | — | All 5 memory files | All non-memory files |

---

## Detailed File Edit Maps

### project.md (Task 1.1, ~10 min)

Pre-edit state: ~29 lines, ~750 bytes. Post-edit: ~30 lines, ~900 bytes.

| # | Where | From | To | Notes |
|---|-------|------|----|-------|
| 1 | Line 2 | `updated: 2026-06-17` | `updated: 2026-06-18` | Frontmatter date — do this in all 5 files |
| 2 | Line 5 | `# Project: <project-name>` | `# Project: OMP Beads Template` | Canonical name from README.md |
| 3 | Lines 7-8 | `Replace this with your actual project name.` + blank line | Remove the instruction line; keep one blank line | Don't leave a visual gap that makes the file look broken |
| 4 | Line 11 | `<One sentence — what are we building and why?>` | `An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating.` | Derived from README.md + repo-observable deliverables |
| 5 | Line 15 | `1. **<Criterion 1>** — <measurable outcome>` | `1. **Zero template placeholders** — No \`<project-name>\` or \`<!-- TODO\` markers in any \`.omp/memory/project/\` file. Verifiable with \`grep\`.` | Verifiable: grep returns 0 matches |
| 6 | Line 16 | `2. **<Criterion 2>** — <measurable outcome>` | `2. **Valid markdown throughout** — Every memory file is valid markdown with correctly structured tables. Verifiable by reading each file.` | Verifiable: visual inspection or markdown parser |
| 7 | Line 17 | `3. **<Criterion 3>** — <measurable outcome>` | `3. **Agent comprehension within 3 seconds** — An agent loading this context can answer 'what is this project' immediately from project.md. Qualitative but observable.` | Meta-criterion: did hydration work? |
| 8 | Lines 18-20 | `Keep to 3-5 criteria...` | UNCHANGED | Instruction paragraph for template consumers |
| 9 | Line 24 | `- **Status:** <active \| maintenance \| paused>` | `- **Status:** active` | 8 beads closed in 7 days = active |
| 10 | Line 25 | `- **Milestone:** <what we're working toward right now>` | `- **Milestone:** Memory file hydration — project identity hardening` | THIS bead is the milestone |
| 11 | Line 26 | `- **Next:** <the next concrete deliverable>` | `- **Next:** Audit command files for consistency with conventions` | Natural next step |
| 12 | Last para | `Update this section after every milestone...` | UNCHANGED | Critical maintainer guidance |

### conventions.md (Task 2.1, ~10 min)

Pre-edit: ~143 lines, ~4.4KB. Post-edit: ~143 lines, ~4.4KB. Most of the file is unchanged — only
header + 3 table rows change.

| # | Where | From | To | Notes |
|---|-------|------|----|-------|
| 1 | Line 2 | `updated: 2026-06-17` | `updated: 2026-06-18` | |
| 2 | Line ~6 | `# Conventions: <project-name>` | `# Conventions: OMP Beads Template` | |
| 3 | Backend row | `\| Backend \| <TypeScript \| Go \| Rust \| Python> \| <strict? Bun? Deno?> \|` | `\| Backend \| N/A \| Template repo — no backend runtime \|` | No runtime manifest in repo |
| 4 | Frontend row | `\| Frontend \| <TypeScript \| JavaScript> \| <React? Svelte? plain?> \|` | `\| Frontend \| N/A \| Template repo — provides design system assets only \|` | Design assets only, no app |
| 5 | Scripts row | `\| Scripts \| <Bash \| Python \| TypeScript> \| <CI, dev tooling, one-offs> \|` | `\| Scripts \| Python \| \`/init\` hydration script \|` | Only executable code is init.py |

**Unchanged sections (verify they're preserved):** `## Naming`, `## Skill Structure`, `## Command
Structure`, `## Git`, `## Workflow`, `## Agent Conventions`, `## Honcho Memory`, `## Memory File
Maintenance`, `## UI Design`. Also unchanged: Agent instructions and Configuration rows in the
language table.

### tech-stack.md (Task 3.1, ~15 min)

Pre-edit: ~88 lines, ~2.5KB. Post-edit: ~88 lines, ~2.5KB. Three areas change: header,
verification/security commands, craft table.

| # | Where | From | To |
|---|-------|------|----|
| 1 | Line 2 | `updated: 2026-06-17` | `updated: 2026-06-18` |
| 2 | Line ~6 | `# Tech Stack: <project-name>` | `# Tech Stack: OMP Beads Template` |
| 3 | Typecheck | `<tsc --noEmit \| mypy \| cargo check \| go vet>` | `N/A — template repo, no compiled code` |
| 4 | Lint | `<eslint \| ruff \| clippy \| golangci-lint>` | `N/A — no linter configured for template files` |
| 5 | Test | `<vitest run \| pytest \| cargo test \| go test ./...>` | `N/A — no test framework` |
| 6 | Build | `<tsup \| pip install -e . \| cargo build --release \| go build>` | `N/A — no build step` |
| 7 | Dep audit | `<npm audit \| pip-audit \| cargo audit \| govulncheck>` | `N/A — template repo, no runtime dependencies` |
| 8 | Secrets | `<gitleaks detect \| trufflehog filesystem .>` | `N/A — no secrets scanning configured` |
| 9 | Craft block | Broken: 4 rows + attribution + 3 orphans, missing state-coverage.md | Unified 8-row alphabetical table + attribution after |

**Craft table replacement text (copy exactly):**

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
| `design/craft/state-coverage.md` | [READ THE FILE to derive purpose — keywords from heading/intro text] |
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |

Adapted from Open Design's `craft/` directory (Apache 2.0) and
[refero_skill](https://github.com/referodesign/refero_skill) (MIT).
```

For the `[READ THE FILE...]` placeholder: read `design/craft/state-coverage.md`, extract 3-5
keywords from its H1 title and first paragraph, and construct a concise comma-separated purpose
matching the style of other rows. Example expected output: "UI state handling: rest, hover, focus,
active, disabled, loading, empty, error" — but use what the file actually says.

**Unchanged sections:** `## Runtime` table, `## Key Dependencies` table, `## Design Assets` table,
`## Constraints` section. The `bv --robot-triage` and `br list` commands under Graph state stay.

### decisions.md (Task 4.1, ~10 min)

Pre-edit: ~34 lines, ~1.3KB. Post-edit: ~30 lines, ~1.3KB.

| # | Where | From | To |
|---|-------|------|----|
| 1 | Line 2 | `updated: 2026-06-17` | `updated: 2026-06-18` |
| 2 | Line ~6 | `# Decisions: <project-name>` | `# Decisions: OMP Beads Template` |
| 3 | Decision Log body | Placeholder row | 5 real decision rows (verbatim from Example) |
| 4 | Example section | Entire `## Example` section | REMOVED (content is in Decision Log) |

**5 decision rows to insert (verbatim — copy from the Example section of the actual file, not from here):**

```
| 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator. Alternatives (linear, plain markdown) lack the graph query ability. | High |
| 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts and skill knowledge. Scripts add maintenance burden, platform dependencies, and hidden logic. | High |
| 3 | 2026-06 | Bare command names (`/create`, `/plan`) | OMP resolves commands by directory. Prefix would be noise. | High |
| 4 | 2026-06 | `.omp/` as native project root | OMP loads from `.omp/`. Parallel `.pi/` config creates confusion. | High |
| 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages. The beads template stays pure workflow — install providers separately. | High |
```

**Unchanged:** Intro paragraph, `## How to Add a Decision` section (all 5 steps).

### gotchas.md (Task 5.1, ~10 min)

Pre-edit: ~44 lines, ~2.2KB. Post-edit: ~46 lines, ~2.3KB.

| # | Where | From | To |
|---|-------|------|----|
| 1 | Line 2 | `updated: 2026-06-17` | `updated: 2026-06-18` |
| 2 | Line ~6 | `# Gotchas: <project-name>` | `# Gotchas: OMP Beads Template` |
| 3 | Active Warnings body | Placeholder row | 1 real entry: memory templates gotcha with updated mitigation |
| 4 | Template Bootstrap | (no blockquote) | Insert `> These gotchas ship with the OMP Beads Template...` after description paragraph |
| 5 | Template Bootstrap row | "memory templates waste tokens" row | REMOVED (moved to Active Warnings) |

**Active Warnings entry (updated mitigation):**

```
| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session — compounds across sessions | Fill with real project content immediately. This bead (br-omp-backbone-skill-l3d) addresses the initial hydration. Audit memory files during /close. |
```

**Blockquote to insert:**

```
> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.
```

**Unchanged:** The other 11 template-universal entries (verbatim, original order). `## How to Add a
Gotcha` section (all 5 steps + "Remove entries" note).

---

## Graph Context Summary

- **Blast radius:** 5 files (0 new, 5 edits, 0 deletes) — all under `.omp/memory/project/`
- **Graph:** 9 nodes, 0 edges, density 0. All beads are orphaned — no dependency relationships exist.
- **This bead:** No upstream blockers. No downstream dependents. Isolated housekeeping task.
- **File history:** Zero bead history on all 5 target files. `bv --robot-file-hotspots` reports 0
files, 0 links. These files have never been edited by any bead — they were written once by `/init`.
- **Hotspots:** None. No file in the repo has >3 bead history.
- **Forecast:** 52 minutes (confidence 0.4). Factors: chore ×0.8, depth 1 ×1.10, 1 agent, 16 min/day
velocity. ETA: 2026-06-21.
- **Key insight:** The graph is boring because this bead is boring — it's a standalone chore with no
structural coupling to any other work. This is correct and expected.

---

## What Could Go Wrong

1. **Wrong line numbers:** The plan gives approximate line numbers. If you edit from plan numbers
without reading the file first, you'll edit the wrong line. Always read before edit.
2. **Over-editing:** It's tempting to "fix" other things while editing — misaligned table columns,
inconsistent formatting, "while I'm here" cleanups. Don't. The diff scope check in Wave 6 will catch
these and they'll need reverting.
3. **Under-editing:** Missing a placeholder because you searched for `<project-name>` but forgot
that the conventions.md language table has `<TypeScript | Go | Rust | Python>` which is a different
placeholder pattern. The per-task verification catches these.
4. **Losing content:** Deleting a decision's rationale text instead of copying it, or accidentally
deleting a gotcha entry when restructuring. The content preservation Python checks in Wave 6 catch
these.
5. **Craft table structure error:** Putting the attribution paragraph inside the table (between
rows) instead of after it. The Python contiguity check in Wave 6 catches this.
6. **Frontmatter corruption:** Accidentally deleting a `---` delimiter or changing the `purpose:`
field. The markdown validity check catches this.
7. **Running `/init`:** If you run `/init` for any reason, it will regenerate placeholder-filled
memory files and undo all edits. Don't run it.
8. **Scope bleed:** Editing a file outside `.omp/memory/project/` because it "looks related." The
git diff scope check catches this.
9. **Paraphrasing decisions:** "Improving" the decision text to be clearer or more concise. The
content preservation check catches this — it looks for exact substring matches.
10. **Wrong alphabetical order in craft table:** Sorting case-sensitively (capital letters first)
instead of case-insensitively. The filenames are all lowercase, so this shouldn't matter, but be
consistent.

---

## Handoff Checklist

Before starting `/ship`, confirm:

- [ ] `prd.md` exists and is ≥600 lines (currently 600 lines)
- [ ] `plan.md` exists and is ≥600 lines (currently ~957 lines)
- [ ] `tasks.md` exists and is ≥600 lines
- [ ] `context-capsule.md` exists (this file, target ≥600 lines)
- [ ] `prd.json` exists (machine-readable requirements mirror)
- [ ] br bead status is `in_progress` (claimed at 2026-06-17T16:16:35Z)
- [ ] `br dep cycles --json` returns empty (acyclic — confirmed: 0 cycles)
- [ ] `bv --robot-plan --format json` shows this bead as the sole item in track-A
- [ ] `git status` is clean or shows known state (no uncommitted changes that conflict)

For the `/ship` agent:

1. **Read this capsule first** — it provides the full context: objective, patterns, constraints, file edit maps
2. **Read `tasks.md`** — it has the detailed step-by-step checklist with 160+ checkbox items across 6 waves
3. **Reference `plan.md` "Observable Truths"** (items 1-23) — confirm each truth before editing the corresponding file
4. **Reference "File Edit Maps"** (above) — what changes where, with approximate line numbers
5. **Edit in wave order: 1 → 2 → 3 → 4 → 5** — verify each file after editing it, before moving to the next
6. **Wave 6** runs the full cross-file verification suite. `plan.md` "Full Verification" section has
copypaste-ready Python and bash scripts
7. **Do NOT read the PRD during `/ship`** — the plan, tasks, and this capsule are self-contained.
The PRD is the requirements authority; the plan is the execution authority
8. **If unclear**, re-read the "Constraints" section above — the MUST/SHOULD/MUST NOT lists are the final authority
9. **Maximum 3 fix cycles** — if a verification check still fails after 3 attempts, escalate, don't loop
10. **After all waves pass**, the bead is ready for `/verify` (record evidence) and `/review` (5-agent parallel review)
