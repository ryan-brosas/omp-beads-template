# Plan: br-omp-backbone-skill-l3d

**Goal:** Hydrate all 5 template memory files — zero `<project-name>` or template placeholder text remains in `.omp/memory/project/`. Every file is valid markdown with real project identity derived from README.md and verified against observable repo state.

## Graph Context

- **Blast radius:** 5 files (0 new, 5 edits, 0 deletes)
- **Implementation blast radius:** 5 source files, `.omp/memory/project/project.md`, `.omp/memory/project/conventions.md`, `.omp/memory/project/tech-stack.md`, `.omp/memory/project/decisions.md`, `.omp/memory/project/gotchas.md` (0 new, 5 edits, 0 deletes)
- **Planning artifact blast radius:** 3 bead artifacts, `.beads/artifacts/br-omp-backbone-skill-l3d/plan.md`, `.beads/artifacts/br-omp-backbone-skill-l3d/tasks.md`, `.beads/artifacts/br-omp-backbone-skill-l3d/context-capsule.md`
- **Unblocks:** None. `bv --robot-plan --format json` reported `unblocks_count: 0` and `impact_reason: No downstream dependencies`.
- **Blocked by:** None. `br dep tree br-omp-backbone-skill-l3d --json` returned only this bead at depth 0 with no parent.
- **Critical path:** No. `bv --robot-insights --format json` reported 9 nodes, 0 edges, density 0, and critical path score 1 for every node. All 9 beads are orphans — no dependency edges exist in the graph.
- **Forecast:** 52 minutes (confidence 0.4) from `bv --robot-forecast br-omp-backbone-skill-l3d --format json`. The bead estimate is 45 minutes; graph forecast inflates it slightly for chore type (×0.8), depth 1 (×1.10), and 1 agent.
- **Hotspots touched:** None from `bv --robot-file-hotspots --format json` (`total_files: 0`, `total_bead_links: 0`, `files_with_multiple_beads: 0`). The 5 target memory files have no bead history — they were written once by `/init` and never edited by any bead.
- **Planning track:** One track, `track-A`, containing only `br-omp-backbone-skill-l3d`. No graph-level parallel tracks exist.
- **Graph status:** PageRank, Betweenness, Eigenvector, HITS, Critical, Cycles, KCore, Articulation, and Slack all computed. Cycles count is 0. All 9 nodes are orphans (no incoming or outgoing edges). Density is 0. No articulation points. KCore is 0 for all nodes.
- **Velocity:** 8 beads closed in last 7 days, 8 in last 30 days. Average 0.02 days to close. Estimated velocity: 16 minutes/day.
- **Related beads:** None with active dependency edges. `br-omp-backbone-skill-nvf` edited `/init` hydration logic but the memory files themselves have never been touched by any bead.

## Observable Truths

1. In `.omp/memory/project/project.md`, the header reads `# Project: <project-name>`, the Goal section contains `<One sentence — what are we building and why?>`, all 3 success criteria are `<Criterion N>` placeholders, and the Current Phase section has `<active | maintenance | paused>`, `<what we're working toward right now>`, and `<the next concrete deliverable>`.
2. In `.omp/memory/project/conventions.md`, the header reads `# Conventions: <project-name>` and the "Languages by Purpose" table contains `<TypeScript | Go | Rust | Python>` in the Backend row, `<TypeScript | JavaScript>` in the Frontend row, and `<Bash | Python | TypeScript>` in the Scripts row.
3. In `.omp/memory/project/tech-stack.md`, the header reads `# Tech Stack: <project-name>`, verification commands contain `<tsc --noEmit | mypy | cargo check | go vet>`, `<eslint | ruff | clippy | golangci-lint>`, `<vitest run | pytest | cargo test | go test ./...>`, and `<tsup | pip install -e . | cargo build --release | go build>`. The "Craft References" table spans lines 80-88: lines 80-84 form a valid 4-row table, line 85 is an attribution paragraph, and lines 86-88 are 3 orphan table rows with no header. The file `design/craft/state-coverage.md` exists on disk but does not appear in the table.
4. In `.omp/memory/project/decisions.md`, the header reads `# Decisions: <project-name>`. The "Decision Log" section contains one placeholder row with `<YYYY-MM>` date, `<what we decided>` decision, `<why — tradeoffs, alternatives considered>` rationale, and `<High | Medium | Low>` confidence. The "Example" section contains 5 real decisions made in 2026-06: br/bv tracking (#1), commands+skills only (#2), bare command names (#3), `.omp/` as native root (#4), tooling in separate repos (#5). These 5 decisions describe actual architecture — they are labeled "Example" but match the project's real design.
5. In `.omp/memory/project/gotchas.md`, the header reads `# Gotchas: <project-name>`. The "Active Warnings" table has one placeholder row. The "Template Bootstrap Gotchas" section contains 13 gotcha entries dated 2026-06 spanning workflow (5), commands (1), omp (1), bv (2), memory (2), models (1), and skills (1). All 13 entries must survive — some apply universally to template consumers, one (memory templates waste tokens) is specific to the OMP Beads Template's own maintenance.
6. The README.md heading is "OMP Beads Template" and the first paragraph describes "OMP-native project template with br and bv as the backbone of planning, execution, verification, and review." This is the canonical source of project identity.
7. The `.omp/AGENTS.md` file describes the workflow philosophy: "br owns state," "bv informs decisions," "OMP executes." This is the canonical source of project convention authority.
8. No compiled code exists in the repo — no `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`, `pyproject.toml`, or `tsconfig.json`. The only executable code (outside OMP extensions) is the Python hydration script embedded in `.omp/commands/init.md`.
9. The `design/craft/` directory contains 8 files: `typography.md`, `color.md`, `anti-ai-slop.md`, `animation-discipline.md`, `state-coverage.md`, `accessibility-baseline.md`, `form-validation.md`, `typography-hierarchy.md`. All 8 exist on disk and should appear in the craft references table.
10. The 5 decisions under "Example" in decisions.md are dated 2026-06, reference actual architecture choices visible in the repo (br/bv in AGENTS.md, commands as markdown in .omp/commands/, `.omp/` as root directory, tooling in separate repos like omp-makora-provider), and carry "High" confidence. They are real decisions, not examples.
11. The memory file "Template Bootstrap Gotchas" entry "Memory templates waste tokens if left as placeholders" (2026-06, memory area) describes the exact problem this bead fixes. This is a meta-gotcha — it belongs in the project's own Active Warnings, not in the template consumer gotchas.
12. The remaining 12 Template Bootstrap Gotchas entries describe universal risks that apply to any project using the OMP Beads Template: workflow gate understanding, bash circumvention, implementing without bead/plan, assuming requirements without PRD, command prompt template variability, `.omp/` vs `.pi/` confusion, bv git history requirement, bv br data requirement, stale memory risks, model capability variance, and irrelevant skill loading. These are part of the template's institutional knowledge.
13. All 5 memory files use the same frontmatter pattern: `---\npurpose: ...\nupdated: 2026-06-17\n---`. The `updated` date should be changed to 2026-06-18 (today) since the files are being edited.
14. The conventions.md "Memory File Maintenance" section is authoritative — it says memory files MUST stay current. This bead implements that rule for the first time.
15. No tool parses memory file structure — they are markdown consumed by humans and agents. Structural validity matters for readability, not for functional correctness.
16. The PRD's "Approach" section specifies exact content for each file. The shipping agent must follow those specifications without adding new sections, removing existing sections outside the approach, or changing content that is not a placeholder or structural fix.
17. The PRD explicitly forbids touching: `.omp/commands/init.md`, `.omp/templates/`, `.omp/skills/`, `.omp/AGENTS.md`, `.omp/RULES.md`, `DESIGN.md`, `design/`, `README.md`, `.gitignore`. The shipping agent must not cross these boundaries.
18. Each memory file must stay under 2KB per conventions.md — current sizes: project.md ~750 bytes, conventions.md ~4.4KB (already over — existing content, not this bead's problem), tech-stack.md ~2.5KB (borderline), decisions.md ~1.3KB, gotchas.md ~2.2KB. The bead's edits should not meaningfully increase any file's size beyond the PRD-specified content changes.
19. The craft table in tech-stack.md currently contains 4 rows in a headerless fragment after the attribution paragraph. The attribution paragraph's text is: "Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT)." This attribution must be preserved and placed AFTER the unified table.
20. The bead artifacts for this planning phase are plan.md, tasks.md, and context-capsule.md. prd.md and prd.json already exist. After /plan, these 3 new artifacts must exist before /ship can begin.
21. The workflow gate will block edit/write to memory files unless PRD and plan exist. Both prd.md (>600 lines) and this plan.md (target >600 lines) satisfy that requirement.
22. No bv file-beads history exists for the 5 target files — they have never been touched by any bead. This is the first bead to edit memory files directly.
23. The shipping agent can implement this plan by reading tasks.md and context-capsule.md without re-deriving graph context. The plan is self-contained and mechanically executable.

## Required Artifacts

| Artifact | Provides | Path | Status |
|----------|----------|------|--------|
| prd.md | Problem, scope, acceptance criteria, approaches per file, risks | `.beads/artifacts/br-omp-backbone-skill-l3d/prd.md` | Have |
| prd.json | Machine-readable mirror of requirements and success criteria | `.beads/artifacts/br-omp-backbone-skill-l3d/prd.json` | Need |
| plan.md | Graph-informed wave sequence, blast radius, code outlines, verification gates | `.beads/artifacts/br-omp-backbone-skill-l3d/plan.md` | Have |
| tasks.md | Ordered checklist with dependencies, ownership, per-task checks | `.beads/artifacts/br-omp-backbone-skill-l3d/tasks.md` | Have |
| context-capsule.md | Shipping handoff: objective, patterns, constraints, file ownership, graph context | `.beads/artifacts/br-omp-backbone-skill-l3d/context-capsule.md` | Have |
| project.md | Memory file: project identity — header, goal, success criteria, current phase | `.omp/memory/project/project.md` | Have, edit during `/ship` |
| conventions.md | Memory file: naming, languages table, workflow, agent rules | `.omp/memory/project/conventions.md` | Have, edit during `/ship` |
| tech-stack.md | Memory file: runtime, verification commands, craft references table | `.omp/memory/project/tech-stack.md` | Have, edit during `/ship` |
| decisions.md | Memory file: architecture decision log, how-to reference | `.omp/memory/project/decisions.md` | Have, edit during `/ship` |
| gotchas.md | Memory file: active warnings, template bootstrap gotchas, how-to reference | `.omp/memory/project/gotchas.md` | Have, edit during `/ship` |

## Wave Structure

| Wave | Tasks | Parallel? | Preconditions | Verification Gate |
|------|-------|-----------|---------------|-------------------|
| 1 | 1.1 | No | PRD and graph context loaded; current file contents read | project.md has zero `<project-name>` or `<!-- TODO` placeholders. Headers and values are concrete. |
| 2 | 2.1 | No (independent but logically separate from wave 1) | Wave 1 verified | conventions.md header is concrete; languages table has no `<option1 \| option2>` placeholders; Backend/Frontend rows say "N/A". |
| 3 | 3.1 | No | Waves 1-2 verified; craft directory listing confirmed | tech-stack.md header is concrete; verification commands are "N/A" or actual; craft table is one contiguous table with all 8 files and attribution paragraph after the table. |
| 4 | 4.1 | No | Waves 1-3 verified; existing 5 decisions content confirmed | decisions.md has 5 decisions under "Decision Log" heading with sequential # numbering. "Example" section removed. |
| 5 | 5.1 | No | Waves 1-4 verified; gotcha entry categorization completed | gotchas.md has separated "Active Warnings" (project-specific) and "Template Bootstrap Gotchas" (consumer-universal) sections. |
| 6 | 6.1 | No | Waves 1-5 all verified; all 5 files edited | Full verification: grep, markdown validity, content preservation, unchanged anchor checks. |

### Why Sequential Waves

All 5 files are logically independent — edits to project.md don't affect conventions.md, etc. They could run in parallel (different files, no shared state). However, sequential waves with verification gates after each file provide:

1. **Recovery surface:** If a file edit is wrong, only one file needs reverting, not 5.
2. **Incremental confidence:** Each wave verified means progress is banked, not rolled back.
3. **Context preservation:** The agent reads each target file fresh before editing it. Sequential waves prevent context window from holding 5 stale file snapshots simultaneously.

The graph shows 0 edges and 0 density — no dependency constraints force any ordering. The sequential structure is a process choice, not a graph constraint.

## Tasks

### Wave 1: Hydrate project.md

**Task 1.1: Fill project identity, goal, success criteria, and current phase**

Read `.omp/memory/project/project.md`, then edit it to replace all 8 placeholder fields with concrete content. The file frontmatter and section structure stay unchanged. Only placeholder text is replaced.

**Design decisions (from PRD approach):**

- **Project name:** "OMP Beads Template" — derived from README.md heading, which is the canonical public name.
- **Goal:** "An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating." — This is the README first paragraph expanded with concrete deliverables visible in the repo structure (br database, bv graph commands, .omp/ commands and skills, workflow gate extension).
- **Success criteria (3):**
  1. "Zero `<project-name>` or template placeholders in any `.omp/memory/project/` file" — verifiable with `grep`.
  2. "Every memory file is valid markdown with filled tables" — verifiable by reading each file and checking table column counts.
  3. "An agent loading this context can answer 'what is this project' within 3 seconds" — qualitative but observable from the filled project.md.
- **Current phase:**
  - Status: `active` — 8 beads closed, design system added, commands and skills refined. The template is actively maintained.
  - Milestone: "Memory file hydration — project identity hardening" — this bead's deliverable.
  - Next: "Audit command files for consistency with conventions" — natural next step after memory files are authoritative.
- **Updated date:** Change frontmatter `updated: 2026-06-17` to `updated: 2026-06-18`.

**Code outline — exact replacements:**

```
Target file: .omp/memory/project/project.md

Replace line 5: "# Project: <project-name>" 
  → "# Project: OMP Beads Template"

Replace lines 7-8: "Replace this with your actual project name.\n\n" 
  → "" (remove the instruction line and extra blank line, or keep blank line for spacing)

Replace line 11: "<One sentence — what are we building and why?>"
  → "An OMP-native project template that provides br/bv-powered workflow infrastructure for AI-agent-driven software development — task tracking, graph-informed planning, artifact generation, and quality gating."

Replace line 15: "1. **<Criterion 1>** — <measurable outcome>"
  → "1. **Zero template placeholders** — No `<project-name>` or `<!-- TODO` markers in any `.omp/memory/project/` file. Verifiable with `grep`."

Replace line 16: "2. **<Criterion 2>** — <measurable outcome>"
  → "2. **Valid markdown throughout** — Every memory file is valid markdown with correctly structured tables. Verifiable by reading each file."

Replace line 17: "3. **<Criterion 3>** — <measurable outcome>"
  → "3. **Agent comprehension within 3 seconds** — An agent loading this context can answer 'what is this project' immediately from project.md. Qualitative but observable."

Replace lines 18-20: Remove the instruction paragraph "Keep to 3-5 criteria..." if it exists after criterion 3, or leave it — it's useful guidance for template consumers. Since this repo IS the template, the instruction is meta-useful for contributors. Keep it.

Replace line 24: "- **Status:** <active | maintenance | paused>"
  → "- **Status:** active"

Replace line 25: "- **Milestone:** <what we're working toward right now>"
  → "- **Milestone:** Memory file hydration — project identity hardening"

Replace line 26: "- **Next:** <the next concrete deliverable>"
  → "- **Next:** Audit command files for consistency with conventions"

Replace line 2 frontmatter: "updated: 2026-06-17" 
  → "updated: 2026-06-18"
```

**Verification (after edit):**

1. `grep '<project-name>' .omp/memory/project/project.md` returns no matches.
2. `grep '<!-- TODO' .omp/memory/project/project.md` returns no matches.
3. `grep '<Criterion' .omp/memory/project/project.md` returns no matches.
4. `grep '<active | maintenance | paused>' .omp/memory/project/project.md` returns no matches.
5. `grep 'what we're working toward' .omp/memory/project/project.md` returns no matches.
6. `grep 'OMP Beads Template' .omp/memory/project/project.md` returns at least 1 match (the header).
7. File frontmatter `updated:` field reads `2026-06-18`.

### Wave 2: Hydrate conventions.md

**Task 2.1: Fill project name header and Languages by Purpose table**

Read `.omp/memory/project/conventions.md`, then edit the header and the "Languages by Purpose" table. The rest of the file — naming conventions, skill structure, command structure, git conventions, workflow, agent conventions, Honcho memory, memory file maintenance, UI design — stays unchanged. Only the header and the languages table change.

**Design decisions (from PRD approach):**

- **Header:** `# Conventions: OMP Beads Template`
- **Languages table:**

| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | N/A | Template repo — no backend runtime |
| Frontend | N/A | Template repo — provides design system assets only |
| Scripts | Python | `/init` hydration script |

- **Backend/Frontend = N/A:** This is a template repo with no runtime application. There is no `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`, or any other backend/frontend dependency manifest. The repo's purpose is to be cloned and customized — it is not an application.
- **Scripts = Python:** The only executable code (outside OMP TypeScript extensions) is the Python hydration script embedded in `.omp/commands/init.md`. The `which python3` check passed during /init bootstrap. The script uses Python stdlib only (pathlib, json, os, re, subprocess). No other scripting languages are present in the repo.
- **Notes for Scripts:** Keep the existing note column text or update to "`/init` hydration script" — the note should describe what the scripts actually do. The PRD approach says to fill notes, and the existing notes column is freeform. Use "`/init` hydration script" as the most precise description.
- **Updated date:** Change frontmatter to `2026-06-18`.

**Code outline — exact replacements:**

```
Target file: .omp/memory/project/conventions.md

Replace: "# Conventions: <project-name>"
  → "# Conventions: OMP Beads Template"

Replace the entire "Languages by Purpose" table block — from "| Purpose | Language | Notes |" through the Scripts row:

Current table (lines 16-22 approximately):
| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | <TypeScript | Go | Rust | Python> | <strict? Bun? Deno?> |
| Frontend | <TypeScript | JavaScript> | <React? Svelte? plain?> |
| Scripts | <Bash | Python | TypeScript> | <CI, dev tooling, one-offs> |

Replace with:
| Purpose | Language | Notes |
|---------|----------|-------|
| Agent instructions | Markdown | Skills, commands, memory files |
| Configuration | JSON / YAML | settings, manifests |
| Backend | N/A | Template repo — no backend runtime |
| Frontend | N/A | Template repo — provides design system assets only |
| Scripts | Python | `/init` hydration script |

Keep the instruction paragraph after the table: "Fill in the actual languages for your project. Agents use this to pick the right tool for the job." — This is meta-useful for template consumers. The conventions.md IS part of the template that consumers will customize. Keep it.

Replace frontmatter: "updated: 2026-06-17" → "updated: 2026-06-18"
```

**Verification (after edit):**

1. `grep '<project-name>' .omp/memory/project/conventions.md` returns no matches.
2. `grep '<TypeScript' .omp/memory/project/conventions.md` returns no matches.
3. `grep 'N/A' .omp/memory/project/conventions.md` returns at least 2 matches (Backend and Frontend rows).
4. `grep 'Python' .omp/memory/project/conventions.md | grep 'Scripts'` — verify the Scripts row exists and says Python. Read the line: `| Scripts | Python |`.
5. The "Agent instructions" and "Configuration" rows are unchanged from the original template.
6. File frontmatter `updated:` field reads `2026-06-18`.

### Wave 3: Fix tech-stack.md

**Task 3.1: Fix header, verification commands, and broken craft references table**

Read `.omp/memory/project/tech-stack.md`, then make three edits: (1) header, (2) verification commands, (3) craft references table structure.

**Sub-task 3.1a: Replace header and verification command placeholders**

- **Header:** `# Tech Stack: OMP Beads Template`
- **Verification commands:** Replace each placeholder with `N/A` because this is a template repo with no compiled code. The "Graph state" commands stay (br and bv are always available).
  - Typecheck: `N/A` — no compiled language
  - Lint: `N/A` — no linter configured
  - Test: `N/A` — no test framework
  - Build: `N/A` — no build step
  - Graph state: `bv --robot-triage` and `br list --status open --status in_progress --json` — keep as-is
- **Security:** Replace `<npm audit | pip-audit | cargo audit | govulncheck>` with `N/A` — no dependencies to audit. Replace `<gitleaks detect | trufflehog filesystem .>` with `N/A` — no secrets scanning configured.
- **Key Dependencies table:** Keep the placeholder row `<name> | <what it does> | <version>`. The template intentionally has this row as a pattern for consumers. Replace the row text with a note: "This is a template repo — no runtime dependencies." Or keep the placeholder but note that template repos have no deps. The PRD says "Keep to the dependencies that shape architecture decisions" — since there are none, the placeholder should indicate that. Replace `<name>` with `None — template repo`, `<what it does>` with `N/A`, `<version>` with `N/A`.
- **Runtime table:** Keep the Language/Runtime/Package manager rows as placeholders — they are structural for consumers. Replace `<TypeScript | Python | Go | Rust>` with "N/A — template repo", `<version>` with "N/A", `<strict mode? async? experimental flags?>` with "N/A". Same pattern for Runtime and Package manager rows.

**Wait — PRD scope check:** The PRD says "Fill verification commands with N/A for typecheck/lint/test/build — this is a template repo with no compiled code." It also says "Not creating new memory files" and "Not adding or removing gotchas — only restructuring existing ones." The PRD's In Scope list only mentions: header, verification commands, craft table. It does NOT mention filling the Runtime table or Key Dependencies table.

**Decision:** Follow the PRD scope exactly. Only edit: header, verification commands, and craft references table. Leave the Runtime table and Key Dependencies table with their placeholder structure — they are part of the template pattern that consumers fill in. The PRD explicitly says "Following the template pattern — fill placeholders, don't add new top-level sections." The Runtime and Key Dependencies placeholders ARE the template pattern. They serve as examples for consumers.

**Correction to approach:** The verification commands section replaces the bash code block lines. The table rows (Runtime, Key Dependencies) stay as-is. The constraint "No new sections" means don't add sections; it doesn't mean fill every placeholder in the file. `grep '<project-name>'` is the anti-pattern check, not `grep '<TypeScript'` across tech-stack.md. The PRD only requires the header replacement (for the `<project-name>` check) and verification commands (for the `<tsc | mypy>` placeholder check). The Runtime/Key Dependencies placeholders are intentionally kept.

**Sub-task 3.1b: Fix craft references table structure**

Current structure (lines ~80-88 of tech-stack.md):

```
| File | Purpose |
|------|---------|
| `design/craft/typography.md` | ... |
| `design/craft/color.md` | ... |
| `design/craft/anti-ai-slop.md` | ... |
| `design/craft/animation-discipline.md` | ... |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
| `design/craft/accessibility-baseline.md` | ... |
| `design/craft/form-validation.md` | ... |
| `design/craft/typography-hierarchy.md` | ... |
```

Problem: 4 rows in a valid table, then attribution paragraph, then 3 orphan rows with no header. Also, `state-coverage.md` is missing entirely.

Fix: Create one contiguous table with all 8 craft files, followed by the attribution paragraph:

```
| File | Purpose |
|------|---------|
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |
| `design/craft/state-coverage.md` | States every interactive element must handle — rest, hover, focus, active, disabled, loading, empty, error |
| `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
| `design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
| `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).
```

Note about `state-coverage.md` purpose column: The PRD does not specify the exact purpose text. Derive from the file itself — read `.omp/memory/project/tech-stack.md`'s existing pattern (each purpose is a concise, comma-separated keyword list) and read `design/craft/state-coverage.md`'s opening paragraph to extract keywords. Alternatively, use the pattern of other rows and write a concise purpose. Since this is a planning artifact, specify that the shipping agent should read `design/craft/state-coverage.md` to derive the purpose text rather than invent it.

**Code outline — exact replacements:**

```
Target file: .omp/memory/project/tech-stack.md

Edit 1 — Header:
Replace: "# Tech Stack: <project-name>"
  → "# Tech Stack: OMP Beads Template"

Edit 2 — Verification commands (bash code block under "## Verification Commands"):
Replace the bash code block content lines:
  # Typecheck
  <tsc --noEmit | mypy | cargo check | go vet>
  # Lint
  <eslint | ruff | clippy | golangci-lint>
  # Test
  <vitest run | pytest | cargo test | go test ./...>
  # Build
  <tsup | pip install -e . | cargo build --release | go build>
  # Graph state (always available)
  bv --robot-triage
  br list --status open --status in_progress --json

With:
  # Typecheck
  N/A — template repo, no compiled code
  # Lint
  N/A — no linter configured for template files
  # Test
  N/A — no test framework
  # Build
  N/A — no build step
  # Graph state (always available)
  bv --robot-triage
  br list --status open --status in_progress --json

Edit 3 — Security commands (bash code block under "## Security"):
Replace:
  # Dependency audit
  <npm audit | pip-audit | cargo audit | govulncheck>
  # Secrets scan (if configured)
  <gitleaks detect | trufflehog filesystem .>

With:
  # Dependency audit
  N/A — template repo, no runtime dependencies
  # Secrets scan (if configured)
  N/A — no secrets scanning configured

Edit 4 — Craft references table:
Replace the entire block from "## Craft References" heading through the last orphan row.

Current block (approximately lines 78-88):
## Craft References

Brand-agnostic universal design rules that apply on top of any `DESIGN.md`:

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

Replace with:
## Craft References

Brand-agnostic universal design rules that apply on top of any `DESIGN.md`:

| File | Purpose |
|------|---------|
| `design/craft/typography.md` | Type scale, line-height, letter-spacing, font pairing, line length, weight discipline |
| `design/craft/color.md` | Palette structure, accent discipline, contrast minimums, dark themes, semantic naming |
| `design/craft/anti-ai-slop.md` | Seven cardinal sins, soft tells, polish tells, soul-injection rules |
| `design/craft/animation-discipline.md` | When motion earns its place, duration thresholds, curve vs spring, reduced motion, flashing limits |
| `design/craft/state-coverage.md` | [Derived from file — read design/craft/state-coverage.md for purpose keywords] |
| `design/craft/accessibility-baseline.md` | WCAG 2.2 AA floor, contrast, touch targets, focus, labels, keyboard, ARIA discipline |
| `design/craft/form-validation.md` | Input state machine, validation timing, Constraint Validation API, error wiring, submit hygiene |
| `design/craft/typography-hierarchy.md` | Entry points, hierarchy vectors, rhythm failure modes, controlled violations |

Adapted from Open Design's `craft/` directory (Apache 2.0) and [refero_skill](https://github.com/referodesign/refero_skill) (MIT).

Edit 5 — Frontmatter:
Replace: "updated: 2026-06-17" → "updated: 2026-06-18"
```

**Verification (after edit):**

1. `grep '<project-name>' .omp/memory/project/tech-stack.md` returns no matches.
2. `grep '<tsc' .omp/memory/project/tech-stack.md` returns no matches.
3. `grep '<eslint' .omp/memory/project/tech-stack.md` returns no matches.
4. `grep '<vitest' .omp/memory/project/tech-stack.md` returns no matches.
5. `grep '<tsup' .omp/memory/project/tech-stack.md` returns no matches.
6. `grep '<npm audit' .omp/memory/project/tech-stack.md` returns no matches.
7. `grep '<gitleaks' .omp/memory/project/tech-stack.md` returns no matches.
8. The craft references section has exactly one markdown table (one `| File | Purpose |` header, one `|---|---|` separator, 8 data rows).
9. `grep -c '^|' .omp/memory/project/tech-stack.md` within the craft section — all pipe-starting lines are contiguous.
10. The attribution paragraph ("Adapted from Open Design...") appears AFTER the table, NOT between table rows.
11. `grep 'state-coverage.md' .omp/memory/project/tech-stack.md` returns at least 1 match.
12. `grep -c 'design/craft/' .omp/memory/project/tech-stack.md` returns 8 (one per craft file).
13. File frontmatter `updated:` field reads `2026-06-18`.

### Wave 4: Restructure decisions.md

**Task 4.1: Promote 5 real decisions from Example to Decision Log, remove Example section, fix header**

Read `.omp/memory/project/decisions.md`, then restructure it so the Decision Log contains 5 real decisions, the Example section is removed, and the header is concrete.

**Design decisions (from PRD approach):**

- **Header:** `# Decisions: OMP Beads Template`
- **Decision Log:** The 5 real decisions currently under "## Example" are promoted. Content is verbatim — dates, decisions, rationale, and confidence are unchanged. Only the heading changes from "## Example" to "## Decision Log" and the numbering stays sequential (1-5).
- **Placeholder row removal:** The single placeholder row under the current "## Decision Log" (with `<YYYY-MM>`, `<what we decided>`, etc.) is removed.
- **Example section removal:** The "## Example" heading and its content are removed since all 5 decisions are now in the Decision Log. The content is moved, not duplicated.
- **How to Add a Decision:** Kept as-is — this is reference documentation for future decision-making.
- **Updated date:** Change frontmatter to `2026-06-18`.

**Current structure:**

```
---
purpose: ...
updated: 2026-06-17
---

# Decisions: <project-name>

... (intro paragraph)

## Decision Log

| # | Date | Decision | Rationale | Confidence |
|---|------|----------|-----------|------------|
| 1 | <YYYY-MM> | <what we decided> | <why — tradeoffs, alternatives considered> | <High | Medium | Low> |

## How to Add a Decision

... (5-step reference)

## Example

| # | Date | Decision | Rationale | Confidence |
|---|------|----------|-----------|------------|
| 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator... | High |
| 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts... | High |
| 3 | 2026-06 | Bare command names (`/create`, `/plan`) | OMP resolves commands by directory... | High |
| 4 | 2026-06 | `.omp/` as native project root | OMP loads from `.omp/`... | High |
| 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages... | High |
```

**Target structure:**

```
---
purpose: ...
updated: 2026-06-18
---

# Decisions: OMP Beads Template

... (intro paragraph — keep as-is, it's generic guidance)

## Decision Log

| # | Date | Decision | Rationale | Confidence |
|---|------|----------|-----------|------------|
| 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator. Alternatives (linear, plain markdown) lack the graph query ability. | High |
| 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts and skill knowledge. Scripts add maintenance burden, platform dependencies, and hidden logic. | High |
| 3 | 2026-06 | Bare command names (`/create`, `/plan`) | OMP resolves commands by directory. Prefix would be noise. | High |
| 4 | 2026-06 | `.omp/` as native project root | OMP loads from `.omp/`. Parallel `.pi/` config creates confusion. | High |
| 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages. The beads template stays pure workflow — install providers separately. | High |

## How to Add a Decision

... (5-step reference — verbatim, unchanged)
```

**Code outline — exact replacements:**

```
Target file: .omp/memory/project/decisions.md

Edit 1 — Header:
Replace: "# Decisions: <project-name>"
  → "# Decisions: OMP Beads Template"

Edit 2 — Decision Log table body:
Remove the placeholder row:
  | 1 | <YYYY-MM> | <what we decided> | <why — tradeoffs, alternatives considered> | <High | Medium | Low> |

Replace with the 5 real decisions (verbatim from Example section):
  | 1 | 2026-06 | Use br/bv for task tracking and graph intelligence | Graph-informed workflow is the template's core differentiator. Alternatives (linear, plain markdown) lack the graph query ability. | High |
  | 2 | 2026-06 | Commands + skills only, no scripts | Every gap solvable through better prompts and skill knowledge. Scripts add maintenance burden, platform dependencies, and hidden logic. | High |
  | 3 | 2026-06 | Bare command names (`/create`, `/plan`) | OMP resolves commands by directory. Prefix would be noise. | High |
  | 4 | 2026-06 | `.omp/` as native project root | OMP loads from `.omp/`. Parallel `.pi/` config creates confusion. | High |
  | 5 | 2026-06 | Ergonomic tooling lives in separate template repos | omp-makora-provider and friends are independent packages. The beads template stays pure workflow — install providers separately. | High |

Edit 3 — Remove Example section:
Remove everything from "## Example" heading through the last row of the example table (decision #5 row). Keep the blank line before "## How to Add a Decision" if one exists.

Edit 4 — Frontmatter:
Replace: "updated: 2026-06-17" → "updated: 2026-06-18"
```

**Verification (after edit):**

1. `grep '<project-name>' .omp/memory/project/decisions.md` returns no matches.
2. `grep -c '^| [1-5] |' .omp/memory/project/decisions.md` returns exactly 5 (the 5 decision rows).
3. `grep '<YYYY-MM>' .omp/memory/project/decisions.md` returns no matches (placeholder removed).
4. `grep '<what we decided>' .omp/memory/project/decisions.md` returns no matches.
5. `grep 'Example' .omp/memory/project/decisions.md` returns no matches for the heading. (The word "Example" might appear in rationale text — check context. If only in a heading, verify heading is gone.)
6. `grep '## Decision Log' .omp/memory/project/decisions.md` returns exactly 1 match.
7. `grep '## How to Add a Decision' .omp/memory/project/decisions.md` returns exactly 1 match.
8. Decision #1 rationale contains "Graph-informed workflow is the template's core differentiator" — verify verbatim preservation.
9. Decision #5 rationale contains "omp-makora-provider and friends are independent packages" — verify verbatim preservation.
10. File frontmatter `updated:` field reads `2026-06-18`.

### Wave 5: Restructure gotchas.md

**Task 5.1: Separate project-specific gotchas from template-universal gotchas, fix header**

Read `.omp/memory/project/gotchas.md`, then restructure so project-specific gotchas are in "Active Warnings" and template-universal gotchas are in "Template Bootstrap Gotchas" with a clear note that these ship with the template.

**Design decisions (from PRD approach):**

- **Header:** `# Gotchas: OMP Beads Template`
- **Active Warnings:** Move the meta-gotcha about memory template placeholders from Template Bootstrap Gotchas to Active Warnings. This is the one gotcha that applies specifically to the OMP Beads Template's own maintenance.
  - Entry: `| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session | Fill with real project content immediately. This bead (br-omp-backbone-skill-l3d) addresses this. |`
  - Note the mitigation update: add a reference to this bead so future maintainers know it was addressed.
- **Template Bootstrap Gotchas:** Keep all 12 remaining entries but add a blockquote note at the top clarifying that these ship with the template and consumers should replace them with their own project-specific gotchas.
  - Blockquote: `> These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.`
- **How to Add a Gotcha:** Kept as-is — reference documentation.
- **Updated date:** Change frontmatter to `2026-06-18`.

**Categorization of the 13 existing entries:**

Project-specific (move to Active Warnings):
1. `| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session | Fill with real project content immediately. Delete placeholder gotchas when real ones exist. |`

Template-universal (keep in Template Bootstrap Gotchas):
1. `| 2026-06 | workflow | The workflow gate only understands the active bead...` — applies to any br-using project
2. `| 2026-06 | workflow | The gate blocks edit and write but shell-based mutation bypasses it` — applies to any OMP project
3. `| 2026-06 | workflow | Implementing without a bead or plan` — applies to any beads workflow user
4. `| 2026-06 | workflow | Assuming requirements without reading PRD` — applies universally
5. `| 2026-06 | commands | Commands are prompt templates, not compiled code` — applies to any OMP user
6. `| 2026-06 | omp | OMP loads from .omp/ — moving files to .pi/ stops native discovery` — applies to any OMP project
7. `| 2026-06 | bv | bv requires git history` — applies to any bv user
8. `| 2026-06 | bv | bv requires br data` — applies to any bv+br user
9. `| 2026-06 | memory | Stale memory is worse than no memory` — applies to any project with memory files
10. `| 2026-06 | models | Lazy/small models skip steps` — applies to any AI-agent workflow
11. `| 2026-06 | skills | Loading domain-specific skills in the wrong project wastes context` — applies to any OMP project
12. `| 2026-06 | workflow | ` — Wait, let me count again. The gotchas.md file has 13 entries in Template Bootstrap Gotchas. Let me verify by re-reading the file content.

Actually, re-counting from the file I already read:
The Template Bootstrap Gotchas table has rows for:
1. workflow gate only understands active bead
2. gate blocks edit/write but shell bypasses
3. implementing without bead or plan
4. assuming requirements without PRD
5. commands are prompt templates
6. OMP loads from .omp/
7. bv requires git history
8. bv requires br data
9. memory templates waste tokens (THIS ONE moves to Active Warnings)
10. stale memory is worse than no memory
11. lazy/small models skip steps
12. loading domain-specific skills in wrong project

That's 12 entries in Template Bootstrap Gotchas. Subtracting #9 (moved), that leaves 11 in Template Bootstrap Gotchas. Wait, the PRD says 13 total and 1 moves, leaving 12. Let me recount from the file:

Looking at gotchas.md template bootstrap:
Line 20: workflow gate understanding
Line 21: gate blocks edit/write
Line 22: implementing without bead/plan  
Line 23: assuming requirements
Line 24: commands prompt templates
Line 25: omp .omp/ vs .pi/
Line 26: bv requires git history
Line 27: bv requires br data
Line 28: memory templates waste tokens ← THIS ONE
Line 29: stale memory
Line 30: lazy/small models
Line 31: loading skills in wrong project

That's 12 entries. The file has one more entry... let me check. The "Active Warnings" section has one placeholder row. The file description says "These are the gotchas that come with the template itself" — that section has the 12 entries I listed.

The PRD says: "All other 12 gotchas apply to any project using this template." That's consistent with my count: 12 template bootstrap entries, 1 is project-specific (= stays in active warnings after move, making active warnings have 1 entry), and 11 stay in template bootstrap.

Wait, re-reading gotchas.md more carefully:

```
## Template Bootstrap Gotchas

These are the gotchas that come with the template itself. Replace with your project's actual gotchas as you discover them.

| Date | Area | Gotcha | Impact | Mitigation |
|------|------|--------|--------|------------|
| 2026-06 | workflow | The workflow gate only understands the active bead if `br list --status open --status in_progress --json` works | Gate won't block edits, agents write without PRD/plan | Verify `br` is initialized and beads exist before relying on the gate |
| 2026-06 | workflow | The gate blocks `edit` and `write` but shell-based mutation bypasses it | Agent can circumvent gate via `bash` tool | Trust the gate as a signal, not a hard boundary. Agent conventions are the real enforcement. |
| 2026-06 | workflow | Implementing without a bead or plan | Untracked work, no evidence, no review, no PR | Always `/create` + `/plan` before `/ship` |
| 2026-06 | workflow | Assuming requirements without reading PRD | Misses acceptance criteria, scope creep | Read PRD + plan before every `/ship` |
| 2026-06 | commands | Commands are prompt templates, not compiled code | Inconsistent behavior across models and sessions | Keep commands explicit and deterministic. Test with different models. |
| 2026-06 | omp | OMP loads from `.omp/` — moving files to `.pi/` stops native discovery | Silent breakage, agent loses skills and commands | Never create `.pi/` directory. Everything lives under `.omp/`. |
| 2026-06 | bv | `bv` requires git history — robot commands return empty until at least one commit exists | Graph queries fail silently | Create at least one commit before relying on bv |
| 2026-06 | bv | `bv` requires br data — robot commands need `.beads/` database | bv errors if no beads database | Run `br init` before any bv command |
| 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session | Fill with real project content immediately. Delete placeholder gotchas when real ones exist. |
| 2026-06 | memory | Stale memory is worse than no memory | Agents learn wrong conventions, make wrong decisions | Update on every milestone. Audit during `/close`. |
| 2026-06 | models | Lazy/small models skip steps, assume context, don't follow workflow | Wrong output, missing evidence, skipped verification | Use thinking/reasoning-capable models for workflow phases. Explicit prompts compensate for weaker models. |
| 2026-06 | skills | Loading domain-specific skills in the wrong project wastes context | Agent reads irrelevant instructions every session | Only load skills that match the project's tech stack and domain |
```

I count 12 entries (rows 3-14 of the table after the header row). Entry #9 is the memory templates one. So: 1 moves to Active Warnings, 11 stay in Template Bootstrap.

The Active Warnings section currently has 1 placeholder row. After the move, Active Warnings will have 1 real entry (the memory templates meta-gotcha).

**Code outline — exact replacements:**

```
Target file: .omp/memory/project/gotchas.md

Edit 1 — Header:
Replace: "# Gotchas: <project-name>"
  → "# Gotchas: OMP Beads Template"

Edit 2 — Active Warnings:
Remove the placeholder row:
  | <YYYY-MM> | <area> | <what happens> | <why it matters> | <how to avoid or recover> |

Replace with the project-specific gotcha (moved from Template Bootstrap, with updated mitigation referencing this bead):
  | 2026-06 | memory | Memory templates waste tokens if left as placeholders | ~1KB of template text the agent reads every session — compounds across sessions | Fill with real project content immediately. This bead (br-omp-backbone-skill-l3d) addresses the initial hydration. Audit memory files during /close. |

Edit 3 — Template Bootstrap Gotchas:
Add a blockquote note after the section description paragraph but before the table:
  > These gotchas ship with the OMP Beads Template. They apply to any project using this template. Replace with your project's actual gotchas as you discover them.

Remove the memory templates gotcha row (now in Active Warnings):
  | 2026-06 | memory | Memory templates waste tokens if left as placeholders | ... | ... |

Keep all 11 remaining entries verbatim.

Edit 4 — Frontmatter:
Replace: "updated: 2026-06-17" → "updated: 2026-06-18"
```

**Verification (after edit):**

1. `grep '<project-name>' .omp/memory/project/gotchas.md` returns no matches.
2. `grep '<YYYY-MM>' .omp/memory/project/gotchas.md` returns no matches.
3. Active Warnings table has exactly 1 non-placeholder entry (the memory templates gotcha).
4. Template Bootstrap Gotchas table has exactly 11 entries (original 12 minus the 1 moved).
5. `grep 'These gotchas ship with the OMP Beads Template' .omp/memory/project/gotchas.md` returns at least 1 match.
6. `grep 'br-omp-backbone-skill-l3d' .omp/memory/project/gotchas.md` returns at least 1 match (the mitigation note).
7. "How to Add a Gotcha" section is unchanged and present.
8. File frontmatter `updated:` field reads `2026-06-18`.

### Wave 6: Full Verification

**Task 6.1: End-to-end verification of all memory files**

Run the full verification suite. This task proves every acceptance criterion from the PRD.

**Verification commands:**

```bash
# AC1: project.md has real project identity
grep '<project-name>' .omp/memory/project/project.md && echo "FAIL: project name placeholder" || echo "PASS: project.md name"
grep '<!-- TODO' .omp/memory/project/project.md && echo "FAIL: TODO in project.md" || echo "PASS: project.md no TODO"

# AC2: conventions.md has filled language table
grep '<TypeScript' .omp/memory/project/conventions.md && echo "FAIL: TypeScript placeholder in conventions" || echo "PASS: conventions.md languages"
grep '<Bash' .omp/memory/project/conventions.md && echo "FAIL: Bash placeholder in conventions" || echo "PASS: conventions.md no Bash placeholder"
grep 'N/A' .omp/memory/project/conventions.md | grep -c 'Backend\|Frontend'  # Expect at least 2

# AC3: tech-stack.md craft table is structurally valid
# Verify no orphan rows: count pipe-starting lines in craft section, verify they form one contiguous block
python3 - <<'PY'
from pathlib import Path
lines = Path(".omp/memory/project/tech-stack.md").read_text().splitlines()
in_craft = False
table_lines = []
for i, line in enumerate(lines):
    if line.startswith("## Craft References"):
        in_craft = True
        continue
    if in_craft and line.startswith("## "):
        break
    if in_craft:
        table_lines.append(line)
# Every pipe-starting line should be contiguous (no non-pipe, non-blank lines between them)
pipe_indices = [i for i, l in enumerate(table_lines) if l.startswith("|")]
for j in range(1, len(pipe_indices)):
    if pipe_indices[j] - pipe_indices[j-1] > 1:
        blank_lines_between = all(table_lines[k].strip() == "" for k in range(pipe_indices[j-1]+1, pipe_indices[j]))
        if not blank_lines_between:
            print(f"FAIL: non-pipe line between table rows at indices {pipe_indices[j-1]}-{pipe_indices[j]}")
            raise SystemExit(1)
print("PASS: tech-stack.md craft table contiguous")
PY

# AC4: tech-stack.md verification commands are real
grep '<tsc' .omp/memory/project/tech-stack.md && echo "FAIL: tsc placeholder" || echo "PASS: tech-stack.md no tsc placeholder"
grep '<eslint' .omp/memory/project/tech-stack.md && echo "FAIL: eslint placeholder" || echo "PASS: tech-stack.md no eslint placeholder"
grep '<vitest' .omp/memory/project/tech-stack.md && echo "FAIL: vitest placeholder" || echo "PASS: tech-stack.md no vitest placeholder"
grep '<tsup' .omp/memory/project/tech-stack.md && echo "FAIL: tsup placeholder" || echo "PASS: tech-stack.md no tsup placeholder"
grep '<npm audit' .omp/memory/project/tech-stack.md && echo "FAIL: npm audit placeholder" || echo "PASS: tech-stack.md no npm audit placeholder"

# AC5: decisions.md has 5 decisions in Decision Log
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/decisions.md").read_text()
in_log = False
count = 0
for line in text.splitlines():
    if line.startswith("## Decision Log"):
        in_log = True
        continue
    if in_log and line.startswith("## "):
        break
    if in_log and line.startswith("|") and line[2:3].isdigit():
        count += 1
if count != 5:
    print(f"FAIL: expected 5 decision rows in Decision Log, got {count}")
    raise SystemExit(1)
print("PASS: decisions.md has 5 decisions in Decision Log")
PY
grep '## Example' .omp/memory/project/decisions.md && echo "FAIL: Example section still exists" || echo "PASS: decisions.md no Example section"

# AC6: gotchas.md separates template from project gotchas
grep '## Active Warnings' .omp/memory/project/gotchas.md && echo "PASS: gotchas.md Active Warnings exists" || echo "FAIL"
grep '## Template Bootstrap Gotchas' .omp/memory/project/gotchas.md && echo "PASS: gotchas.md Template Bootstrap exists" || echo "FAIL"
grep 'These gotchas ship with the OMP Beads Template' .omp/memory/project/gotchas.md && echo "PASS: gotchas.md has consumer note" || echo "FAIL"

# AC7: No <project-name> in any memory file
grep -r '<project-name>' .omp/memory/project/ && echo "FAIL: project-name placeholder found" || echo "PASS: no project-name placeholders"

# AC8: All memory files are valid markdown
python3 - <<'PY'
from pathlib import Path
import re
files = ["project.md", "conventions.md", "tech-stack.md", "decisions.md", "gotchas.md"]
base = Path(".omp/memory/project")
for fname in files:
    text = (base / fname).read_text()
    # Check tables have consistent column counts
    table_columns = {}
    for line in text.splitlines():
        if line.startswith("|") and "---" not in line:
            cols = len(line.split("|")) - 2
            if cols > 0:
                table_columns.setdefault(fname, []).append(cols)
    for f, cols in table_columns.items():
        if len(set(cols)) > 1:
            print(f"WARN: {f} has inconsistent column counts: {cols}")
    # Check no double headings without content
    # Check frontmatter is valid
    if not text.startswith("---"):
        print(f"FAIL: {fname} missing frontmatter")
        raise SystemExit(1)
    end_fm = text.find("---", 3)
    if end_fm == -1:
        print(f"FAIL: {fname} unclosed frontmatter")
        raise SystemExit(1)
print("PASS: all memory files have valid markdown structure")
PY

# AC9: No content loss from existing decisions
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/decisions.md").read_text()
checks = [
    "Use br/bv for task tracking and graph intelligence",
    "Commands + skills only, no scripts",
    "Bare command names",
    ".omp/ as native project root",
    "omp-makora-provider",
]
missing = [c for c in checks if c not in text]
if missing:
    print(f"FAIL: missing decision content: {missing}")
    raise SystemExit(1)
print("PASS: all 5 decision rationales preserved")
PY

# AC10: No content loss from existing gotchas
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/gotchas.md").read_text()
checks = [
    "workflow gate only understands the active bead",
    "shell-based mutation bypasses it",
    "Implementing without a bead or plan",
    "Assuming requirements without reading PRD",
    "Commands are prompt templates",
    "OMP loads from",
    "bv requires git history",
    "bv requires br data",
    "Memory templates waste tokens",
    "Stale memory is worse than no memory",
    "Lazy/small models skip steps",
    "Loading domain-specific skills",
]
missing = [c for c in checks if c not in text]
if missing:
    print(f"FAIL: missing gotcha content: {missing}")
    raise SystemExit(1)
print("PASS: all gotcha entries preserved")
PY

# Verify br sync is clean
ACTOR="${BR_ACTOR:-assistant}" br sync --flush-only
# Expected: no errors

# Verify no beads dependency cycles
br dep cycles --json
# Expected: empty cycle list
```

**Verification (meta-check):**

1. All AC1-AC10 checks pass with zero FAILs.
2. `br sync --flush-only` completes without error.
3. `br dep cycles --json` returns empty.
4. All 5 memory files: `wc -l` gives reasonable line counts (no file blanked).
5. `git diff --stat .omp/memory/project/` shows exactly 5 files changed.

## Full Verification

Run these checks after all waves complete. They combine the per-wave verification gates into a single end-to-end suite.

```bash
# === IDENTITY CHECKS ===
# AC1: project.md has real project identity
grep '<project-name>' .omp/memory/project/project.md && echo "FAIL: project.md name placeholder" || echo "PASS: project.md"
grep '<!-- TODO' .omp/memory/project/project.md && echo "FAIL: project.md TODO" || echo "PASS: project.md no TODO"

# AC2: conventions.md has filled language table
grep '<TypeScript' .omp/memory/project/conventions.md && echo "FAIL: conventions.md TypeScript placeholder" || echo "PASS: conventions.md"

# AC7: No <project-name> in any memory file
grep -r '<project-name>' .omp/memory/project/ && echo "FAIL: project-name placeholder found" || echo "PASS: no project-name"
# Expected: PASS for all

# === STRUCTURE CHECKS ===
# AC3: tech-stack.md craft table is one contiguous table
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/tech-stack.md").read_text()
# Find craft section boundaries
craft_start = text.index("## Craft References")
next_section = text.find("\n## ", craft_start + 10)
if next_section == -1:
    craft_block = text[craft_start:]
else:
    craft_block = text[craft_start:next_section]
# Attribution must appear AFTER the last table row
table_end = craft_block.rfind("\n|")
attr_start = craft_block.find("Adapted from Open Design")
if attr_start == -1:
    print("FAIL: missing attribution")
    raise SystemExit(1)
if attr_start < table_end:
    print("FAIL: attribution before table end")
    raise SystemExit(1)
print("PASS: tech-stack.md craft table structure correct")
PY
# Expected: PASS

# AC4: verification commands are N/A or real
grep '<tsc\|mypy\|cargo check\|go vet' .omp/memory/project/tech-stack.md && echo "FAIL: verification placeholder" || echo "PASS: tech-stack.md verification"

# AC5: decisions.md has 5 decisions in Decision Log, no Example section
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/decisions.md").read_text()
assert "## Decision Log" in text, "FAIL: no Decision Log heading"
assert "## Example" not in text, "FAIL: Example section still present"
assert "Use br/bv for task tracking" in text, "FAIL: decision 1 missing"
assert "Commands + skills only" in text, "FAIL: decision 2 missing"
assert "Bare command names" in text, "FAIL: decision 3 missing"
assert ".omp/ as native project root" in text, "FAIL: decision 4 missing"
assert "omp-makora-provider" in text, "FAIL: decision 5 missing"
assert "<YYYY-MM>" not in text, "FAIL: placeholder date present"
print("PASS: decisions.md structure correct")
PY
# Expected: PASS

# AC6: gotchas.md has separated sections
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/gotchas.md").read_text()
assert "## Active Warnings" in text, "FAIL: Active Warnings missing"
assert "## Template Bootstrap Gotchas" in text, "FAIL: Template Bootstrap missing"
assert "How to Add a Gotcha" in text, "FAIL: How to Add section missing"
assert "These gotchas ship with" in text, "FAIL: consumer note missing"
assert "Memory templates waste tokens" in text, "FAIL: memory gotcha lost"
assert "<YYYY-MM>" not in text, "FAIL: placeholder date present"
print("PASS: gotchas.md structure correct")
PY
# Expected: PASS

# AC8: All memory files are structurally valid markdown
python3 - <<'PY'
from pathlib import Path
base = Path(".omp/memory/project")
for fname in ["project.md", "conventions.md", "tech-stack.md", "decisions.md", "gotchas.md"]:
    text = (base / fname).read_text()
    # Frontmatter check
    assert text.startswith("---"), f"FAIL: {fname} no frontmatter"
    end = text.find("---", 3)
    assert end != -1, f"FAIL: {fname} unclosed frontmatter"
    # Has a heading
    assert "# " in text, f"FAIL: {fname} no heading"
print("PASS: all memory files structurally valid")
PY
# Expected: PASS

# === CONTENT PRESERVATION CHECKS ===
# AC9: No content loss from existing decisions
python3 - <<'PY'
from pathlib import Path
text = Path(".omp/memory/project/decisions.md").read_text()
for phrase in [
    "Graph-informed workflow is the template's core differentiator",
    "Every gap solvable through better prompts and skill knowledge",
    "OMP resolves commands by directory",
    "OMP loads from `.omp/`",
    "The beads template stays pure workflow",
]:
    assert phrase in text, f"FAIL: missing '{phrase[:40]}...'"
print("PASS: all decision rationales preserved verbatim")
PY
# Expected: PASS

# AC10: No content loss from existing gotchas
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
# Expected: PASS

# === BR/BV HEALTH ===
br sync --flush-only
# Expected: no errors

br dep cycles --json
# Expected: empty cycle list []

# === GIT DIFF SCOPE ===
git diff --stat .omp/memory/project/
# Expected: exactly 5 files changed, all under .omp/memory/project/

git diff -- .omp/commands .omp/templates .omp/skills .omp/AGENTS.md
# Expected: empty diff — no changes outside memory files
```
