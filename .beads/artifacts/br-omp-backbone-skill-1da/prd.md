# PRD: Audit and Fix Command File Consistency with conventions.md

**Bead:** br-omp-backbone-skill-1da | **Type:** task | **Priority:** P1
**Created:** 2026-06-17 | **Estimate:** 45

## Problem

WHEN an agent reads conventions.md THEN it believes `/create` produces "PRD + plan + tasks" BECAUSE the workflow section (line 50) incorrectly describes the `/create` phase output. This is a bug introduced during template bootstrapping when conventions.md was written before the full command separation was finalized. The `/create` command actually produces only `prd.md`, `prd.json`, and `decisions.md`. The `/plan` command separately produces `plan.md`, `tasks.md`, and `context-capsule.md`. An agent that reads conventions.md and tries to follow the workflow verbatim will:
1. Expect `/create` to produce plan.md and tasks.md — it won't
2. Skip `/plan` thinking it's redundant — losing the entire planning and wave-sequencing phase
3. Go directly to `/ship` after `/create` — violating the workflow gate

This bug was discovered during the per-tick pipeline audit that project.md explicitly requests ("Next: Audit command files for consistency with conventions.md"). Beyond this single-line bug, the audit revealed five additional inconsistencies between AGENTS.md, conventions.md, and the actual command behaviors that accumulate over time and confuse agents.

Affected files:
- `conventions.md` — workflow description (line 50), missing prefix info, missing brainstorm entry
- `AGENTS.md` — prefix declaration, tree diagram formatting, 1KB memory target
- `project.md` — will need "Next" field updated after this bead completes

If not fixed, every new agent session will load incorrect workflow instructions, leading to wrong phase sequencing, skipped planning, and unverifiable work.

## Goals

1. **Primary**: Fix the `/create` artifact output bug in conventions.md line 50
2. **Secondary**: Fix all other inconsistencies discovered in the audit between conventions.md, AGENTS.md, and actual command behaviors
3. **Quality**: Ensure conventions.md and AGENTS.md agree on workflow phases, artifact outputs, and naming conventions
4. **Verification**: Every fix must be traceable to a specific audit finding with grep-verifiable before/after proof

## Non-Goals

- Do NOT modify command files (brainstorm.md, create.md, plan.md, etc.) — the commands are correct; conventions.md is wrong
- Do NOT rewrite conventions.md from scratch — minimal surgical fixes only
- Do NOT change the actual workflow or add new phases
- Do NOT modify the workflow gate extension
- Do NOT modify memory files other than conventions.md and project.md
- Do NOT change br configuration or bead ID prefix

## Success Metrics

1. `grep -c "/create.*produces.*PRD.*plan.*tasks" .omp/memory/project/conventions.md` returns 0 (the bug line is gone)
2. `grep -c "/create.*produces.*PRD.*decisions" .omp/memory/project/conventions.md` returns ≥1 (correct description exists)
3. `grep -c "Prefix:.*omp" .omp/memory/project/conventions.md` returns ≥1 (prefix documented in conventions.md)
4. `grep -c "Prefix:.*br-omp" .omp/AGENTS.md` returns ≥1 (prefix corrected in AGENTS.md)
5. `grep -c "brainstorm.*→" .omp/memory/project/conventions.md` returns ≥1 (brainstorm in workflow chain)
6. Tree diagram in AGENTS.md (lines 191-230) has `.omp/` artifacts at correct nesting level (not mixed with `.beads/`)
7. AGENTS.md "Keep each under 1KB" updated to reflect actual current sizes or removed as aspirational
8. All fixes are individually verifiable with `grep` commands — no subjective fixes

## Audit Methodology

### How The Audit Was Conducted

The audit followed the /brainstorm command's codebase exploration protocol (Phases 3-5):

**Phase 3a — Structure Scan:**
Mapped all project files: `.omp/AGENTS.md`, `.omp/RULES.md`, `.omp/memory/project/*.md`, `.omp/commands/*.md`, `.omp/skills/*/SKILL.md`, `.omp/templates/*`, `.omp/config.yml`, `.omp/extensions/workflow-gate.ts`. Identified that memory files and AGENTS.md are the authoritative sources agents read for workflow guidance.

**Phase 3b — Hotspot Analysis:**
Ran `bv --robot-file-hotspots` — no hotspots detected (clean graph, 0 edge_count). All files are equally "cold" in terms of bead activity, suggesting the repo is well-maintained but documentation hasn't been stress-tested by heavy usage.

**Phase 3c — Git History:**
Examined recent commits for "fix", "refactor", and "docs" patterns. Found 6 fix commits and 4 refactor commits in the last 30. The fixes cluster around template correctness (bef2d30, 90b0310, f549c64) suggesting documentation drift is an ongoing challenge. The refactors (cd8d1fb, 475c567) show conventions.md and AGENTS.md were rewritten from earlier versions, which is likely when the `/create` output bug was introduced.

**Phase 3d — Read Key Files:**
Read all 10 command files, all 5 memory files, AGENTS.md, and RULES.md. Cross-referenced each command's "Writes" column in AGENTS.md (line 23) against the actual command files. Confirmed that:
- `/create` writes: `prd.md`, `decisions.md` (per AGENTS.md line 23) ✓
- `/create` actual behavior: `prd.md`, `prd.json`, `decisions.md` (per create.md lines 164-189) ✓
- `/plan` writes: `plan.md`, `tasks.md`, `context-capsule.md` (per AGENTS.md line 24) ✓
- conventions.md line 50: says `/create` produces "PRD + plan + tasks" ✗ (wrong!)

**Phase 4 — Pain Point Discovery:**
Mapped each inconsistency to a pain type:
| Pain Type | Finding | Signal |
|-----------|---------|--------|
| Inconsistency | `/create` output wrong in conventions.md | AGENTS.md vs conventions.md disagree |
| Missing | No /brainstorm in conventions.md workflow | Command exists but workflow doesn't mention it |
| Missing | No br prefix in conventions.md | AGENTS.md has it, conventions.md doesn't |
| Inaccuracy | Prefix wrong in AGENTS.md | Says `omp` but beads are `br-omp-*` |
| Inconsistency | "Implement" vs "Ship" naming | Command is /ship, conventions says "Implement" |
| Visual bug | Tree diagram formatting | Artifacts at wrong indentation levels |
| Aspirational | 1KB memory target | Only 1 of 5 files meets the target |

**Phase 5 — Gap Analysis:**
- **Quality gap**: conventions.md and AGENTS.md are the two files agents read for workflow guidance. When they disagree, agents are confused.
- **DX gap**: No automated check verifies conventions.md ↔ AGENTS.md ↔ command files consistency. It's manual.
- **Safety gap**: An agent that skips /plan loses blast radius analysis, risk assessment, and verification planning.

### Complete Audit Findings Table

| # | Finding | File | Line(s) | Severity | Type | Current | Should Be |
|---|---------|------|---------|----------|------|---------|------------|
| F1 | /create output wrong | conventions.md | 50 | Critical | Bug | "PRD + plan + tasks" | "PRD + decisions.md" |
| F2 | /brainstorm missing from workflow | conventions.md | 49-56 | High | Gap | 7-step workflow, no brainstorm | 8-step workflow with brainstorm as step 1 |
| F3 | /plan missing from workflow | conventions.md | 49-56 | Critical | Gap | No /plan step | /plan as step 3 with correct outputs |
| F4 | "Implement" vs "Ship" naming | conventions.md | 51 | Medium | Inconsistency | "Implement" | "Ship" to match command name |
| F5 | Review description vague | conventions.md | 53 | Low | Under-specified | "runs parallel agents, confidence filter" | "runs 5 parallel agents, confidence filter ≥80" |
| F6 | No br prefix documented | conventions.md | — | Medium | Gap | (missing) | "Prefix: br-omp" |
| F7 | Prefix wrong in AGENTS.md | AGENTS.md | 83 | Medium | Bug | "omp" (omp-a1b2) | "br-omp" (br-omp-a1b2) |
| F8 | Tree diagram broken | AGENTS.md | 191-230 | Low | Visual | Mixed nesting | Proper .omp/ hierarchy |
| F9 | 1KB memory target unrealistic | AGENTS.md | 101 | Low | Aspirational | "Keep each under 1KB" | "Tier 1 target: under 2KB. Tier 2 target: under 3KB." |
| F10 | project.md "Next" stale | project.md | 24 | Low | Stale | "Audit command files..." | New next milestone after audit |
| F11 | Triage mentioned but no /triage command | conventions.md | 49 | Low | Confusion | "Triage — bv --robot-triage" | Should be "Brainstorm" or removed since /triage exists but isn't part of core workflow |
| F12 | "Close — after merge" contradicts agent-only PR workflow | conventions.md | 55 | Low | Inconsistency | "/close after merge" | "/close after review approval" (merging is human responsibility per RULES.md) |

Finding F11 deserves special note: conventions.md currently lists "Triage" as step 1 but the actual workflow uses `/brainstorm` as the entry point. The `/triage` command exists (br-omp-backbone-skill-mcu) but is a stress-test bead, not part of core workflow. The correct entry point is `/brainstorm`. We fix this by replacing "Triage" with "Brainstorm" as step 1.

Finding F12: conventions.md says "/close after merge" but RULES.md line 27 says "The human always gets the last call on merges — the agent proposes, the human decides." The correct behavior is close after review approval, with merge happening at human discretion.

### Root Cause Analysis

The bugs cluster around the conventions.md Workflow section. Tracing git history:

1. `cd8d1fb` (refactor: rewrite .omp/AGENTS.md as canonical project manifesto) — AGENTS.md was rewritten to be correct and comprehensive
2. `475c567` (refactor: rewrite memory/project files with upstream table patterns) — conventions.md was rewritten, likely copying from an older version
3. Between these two commits, conventions.md and AGENTS.md diverged

The specific `/create` output bug (F1) likely originated from an earlier version of the template where `/create` was a monolithic command that did everything. When commands were separated into `/create` + `/plan` + `/ship`, the conventions.md workflow wasn't updated to match.

The missing /brainstorm step (F2) is because conventions.md was written before /brainstorm was promoted from "Triage" to a first-class command with its own exploration protocol.

## Requirements

| # | Requirement | Priority | Acceptance Criteria |
|---|------------|----------|---------------------|
| 1 | conventions.md Workflow step 2: change "/create produces PRD + plan + tasks" to "/create produces PRD + decisions.md" | MUST | `grep "/create.*produces.*PRD.*plan.*tasks" .omp/memory/project/conventions.md` returns no matches |
| 2 | conventions.md Workflow: add "/brainstorm" as entry point (step 0 or step 1) before "/create" | MUST | `grep -i "brainstorm" .omp/memory/project/conventions.md` appears in workflow section |
| 3 | conventions.md Workflow: add "/plan" as step 3 with correct outputs (plan.md + tasks.md + context-capsule.md) | MUST | `grep "Plan.*plan.*produces.*plan.md" .omp/memory/project/conventions.md` returns ≥1 |
| 4 | conventions.md: add br prefix information ("Prefix: br-omp") | SHOULD | `grep "Prefix" .omp/memory/project/conventions.md` matches |
| 5 | AGENTS.md line 83: change prefix from "omp" to "br-omp" to match actual bead IDs | MUST | `grep "Prefix:.*br-omp" .omp/AGENTS.md` matches and `grep "omp-a1b2" .omp/AGENTS.md` returns 0 |
| 6 | AGENTS.md tree diagram (lines 191-230): fix nesting so `.omp/` artifacts (AGENTS.md, commands, skills, etc.) are under `.omp/` not mixed with `.beads/` artifacts | MUST | Visually inspect tree — `.omp/` items under `.omp/` branch |
| 7 | AGENTS.md line 101: update "Keep each under 1KB" to reflect actual sizes or add note about aspirational target | SHOULD | Updated text acknowledges current sizes |
| 8 | project.md: update "Current Phase" to reflect this audit work and set next milestone | SHOULD | "Current Phase" reflects audit-in-progress |
| 9 | conventions.md Workflow: renumber steps 1-7 to 1-8 (adding /brainstorm and /plan) | MUST | Steps flow 1-8 with brainstorm as step 1 |
| 10 | conventions.md Workflow step titles: rename "Implement" to "Ship" to match `/ship` command name | SHOULD | Step reads "Ship — /ship follows plan" |
| 11 | conventions.md Workflow step 1: rename "Triage" to "Brainstorm" to match command name `/brainstorm` | MUST | Step 1 reads "Brainstorm — /brainstorm explores codebase, identifies work" |
| 12 | conventions.md Workflow step 8 (Close): change "after merge" to "after review approval" | SHOULD | Step reads "/close after review approval, suggests next" per RULES.md |
| 13 | conventions.md Review step: make description match actual /review command behavior | SHOULD | "runs 5 parallel agents, confidence filter ≥80" |

## User Stories

### US-1: Agent reads conventions.md and understands correct workflow
**As an** AI agent loading `.omp/memory/project/conventions.md`
**I want** the workflow steps to accurately reflect actual command outputs and sequencing
**So that** I don't skip `/plan` or try to go directly from `/create` to `/ship`
**Acceptance:** After fix, an agent reading only conventions.md can correctly order: brainstorm → create → plan → ship → verify → review → pr → close

### US-2: Agent reads AGENTS.md and sees correct bead prefix
**As an** AI agent reading `.omp/AGENTS.md`
**I want** the bead prefix to match actual bead IDs (`br-omp-*` not `omp-*`)
**So that** I can correctly resolve bead IDs and understand how `br` names beads
**Acceptance:** `br list --all --json` shows IDs matching the prefix documented in AGENTS.md

### US-3: Developer reading AGENTS.md sees accurate tree diagram
**As a** developer reading `.omp/AGENTS.md`
**I want** the repository tree diagram to show correct file structure with proper indentation
**So that** I can understand the project layout at a glance without confusion
**Acceptance:** Tree diagram shows `.omp/` directory with commands, skills, templates, extensions, and memory as sub-items

### US-4: New contributor follows conventions.md exactly
**As a** new developer setting up a project from this template
**I want** conventions.md to describe a workflow I can actually follow step-by-step
**So that** I don't encounter missing phases or incorrect artifact expectations
**Acceptance:** Following conventions.md workflow step 1 through step 8 produces all expected artifacts

### US-5: Pipeline driver reads both AGENTS.md and conventions.md
**As a** per-tick pipeline driver that loads both AGENTS.md and conventions.md
**I want** the two files to agree on workflow phases, artifact outputs, and naming
**So that** I don't have to resolve contradictions between the two before taking action
**Acceptance:** No contradiction between AGENTS.md and conventions.md on any of: workflow phases, artifact outputs, bead prefix

## Technical Context

**Key files:**
- `.omp/memory/project/conventions.md` — EDIT (~15 lines changed/added, currently 129 lines) — Main fix target. The Workflow section (lines 48-56) gets the most changes. A new "Bead Prefix" line may be added near the Naming section.
- `.omp/AGENTS.md` — EDIT (~40 lines changed, currently 252 lines) — Prefix fix (1 line), tree diagram restructure (~35 lines), 1KB note update (1-2 lines).
- `.omp/memory/project/project.md` — EDIT (~5 lines changed, currently 26 lines) — Current Phase update only.

**Files NOT to modify:**
- `.omp/commands/*.md` — All correct, not part of this fix
- `.omp/RULES.md` — Rules are correct, not affected
- `.omp/extensions/workflow-gate.ts` — Not affected
- `.omp/skills/*/SKILL.md` — Not affected
- `.omp/templates/*` — Not affected

**Current conventions.md Workflow section (lines 49-56):**
```
## Workflow

1. **Triage** — `bv --robot-triage` before any action
2. **Create** — `/create` produces PRD + plan + tasks
3. **Implement** — `/ship` follows plan, no scope creep
4. **Verify** — `/verify` runs checks, records evidence
5. **Review** — `/review` runs parallel agents, confidence filter
6. **PR** — `/pr` opens PR, single-turn execution
7. **Close** — `/close` after merge, suggests next bead
```

**Should be:**
```
## Workflow

1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
2. **Create** — `/create` produces PRD + decisions.md
3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
4. **Ship** — `/ship` implements per plan, no scope creep
5. **Verify** — `/verify` runs checks, records evidence
6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80
7. **PR** — `/pr` opens PR, single-turn execution
8. **Close** — `/close` after review approval, suggests next bead
```

**Current AGENTS.md prefix declaration (line 83):**
```
- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)
```

**Should be:**
```
- **Prefix:** `br-omp` (beads are `br-omp-a1b2`, `br-omp-c3d4`, ...)
```

**Actual bead IDs (from br list --all --json):**
```
br-omp-backbone-skill-nvf
br-omp-backbone-skill-9tl
br-omp-backbone-skill-qjk
br-omp-backbone-skill-iej
br-omp-backbone-skill-hfh
br-omp-backbone-skill-l3d
br-omp-backbone-skill-kfu
br-omp-backbone-skill-mcu
br-omp-backbone-skill-1ct
br-omp-backbone-skill-1da
```

Prefix is `br-omp` not `omp`. The prefix is set by the repo name during `br init` — it's `br-omp` because the repo path ends with `omp-template`. The "br-" prefix is mandatory for all br-tracked repos, and "omp" is the repo-specific suffix.

**AGENTS.md tree diagram issues (lines 191-230):**

The current tree diagram is:
```
omp-template/
├── AGENTS.md                          # Delegates to .omp/AGENTS.md
├── .beads/                            # br workspace (SQLite + JSONL)
│   │   ├── prd.md                     # Problem, outcome, acceptance criteria
│   │   ├── prd.json                   # Machine-readable requirements mirror
│   │   ├── plan.md                    # Scope, blast radius, steps, risks, verification
│   │   ├── tasks.md                   # Ordered task list with dependencies
│   │   ├── decisions.md               # Architecture and design decisions
│   │   ├── context-capsule.md         # Handoff for the next agent
│   │   ├── progress.txt               # Phase checklist
│   │   ├── completion-evidence.json   # Verification commands and results
│   │   └── review-report.md           # Parallel review findings and verdict
│   ├── AGENTS.md                      # You are here — canonical project context
│   ├── commands/                      # 9 slash commands
│   │   ├── brainstorm.md, create.md, plan.md, ship.md
│   │   ├── verify.md, review.md, pr.md, close.md, init.md
│   ├── skills/                        # 17 skills
│   │   ├── br/SKILL.md, bv/SKILL.md
│   │   ├── backbone/SKILL.md, orchestrator/SKILL.md
│   │   ├── design-system/SKILL.md     # Brand contract + craft rules
│   │   ├── design-system/DESIGN.md    # 9-section visual language spec
│   │   └── <cognitive-tool>/SKILL.md
│   ├── extensions/                    # Workflow gate
│   │   └── workflow-gate.ts
│   ├── templates/                     # Artifact templates
│   │   └── prd.md, plan.md, tasks.md, review-report.md, ...
│   └── memory/project/                # Durable project knowledge
│   │   ├── tokens.css                  # CSS custom properties (light + dark + system)
│   │   ├── base.css                    # Minimal reset + body defaults
│   │   ├── primitives.css              # Button/input/select/dialog/accordion styles
│   │   └── craft/                      # 8 universal design rule files
│       ├── project.md                 # Vision, goals, current phase
│       ├── conventions.md             # Naming, workflow, agent rules
│       ├── decisions.md               # Architecture decision records
│       ├── gotchas.md                 # Known pitfalls and mitigations
│       └── tech-stack.md              # Versions, verification commands, constraints
├── .gitignore
└── README.md
```

Problems identified:
1. Lines 195-203: Artifact files (prd.md, plan.md, etc.) show at depth `│   │   ├──` which implies they're under `.omp/` but they're actually under `.beads/artifacts/<bead-id>/`
2. Lines 204-206: `.omp/AGENTS.md`, `.omp/commands/` show at depth `│   ├──` which is `.omp/` level but they come after `.beads/` items
3. Lines 207-218: `.omp/skills/`, `.omp/extensions/`, `.omp/templates/` show at same depth as `.omp/AGENTS.md` and `.omp/commands/` — correct for `.omp/` items
4. Lines 219-222: `.omp/memory/project/` shows design system CSS files (tokens.css, base.css, primitives.css) at wrong depth — these belong under a design-system directory, not under memory/project/
5. Lines 223-227: Memory files (project.md, conventions.md, etc.) show at depth `│       ├──` which is deeper than the design system files at depth `│   │   ├──` — inconsistent

The corrected tree should have:
- `.omp/` as a top-level directory
- `.omp/AGENTS.md`, `.omp/commands/`, `.omp/skills/`, `.omp/extensions/`, `.omp/templates/`, `.omp/memory/` under `.omp/`
- Design system CSS files either removed from this tree or placed under a separate `.omp/design-system/` or `assets/` branch
- `.beads/` as a separate top-level directory containing only `.beads/` items

**AGENTS.md "Keep each under 1KB" (line 101):**
```
Keep each under 1KB.
```

Current sizes:
- project.md: 1,259 bytes
- conventions.md: 6,871 bytes
- decisions.md: 1,651 bytes
- gotchas.md: 3,533 bytes
- tech-stack.md: 1,841 bytes

The 1KB target is aspirational and only project.md comes close. This note should be updated to "Tier 1 target: under 2KB. Tier 2 target: under 3KB." to reflect actual usage. Alternatively, it could be removed since the Memory Protocol section immediately above (lines 95-117) already establishes the tier system and rules.

**project.md Current Phase (lines 20-25):**
```
## Current Phase

- **Status:** active
- **Milestone:** Memory file hydration — project identity hardening
- **Next:** Audit command files for consistency with conventions.md
```

The "Milestone" is stale — memory file hydration was completed in br-omp-backbone-skill-l3d. The "Next" field is exactly what this bead addresses. After this bead:

```
## Current Phase

- **Status:** active
- **Milestone:** Command–convention consistency audit
- **Next:** Verify workflow-gate enforces all required artifact checks
```

### Command File Reference (Ground Truth)

These are the command file behaviors that conventions.md MUST match. Verified by reading each command file:

| Command | File | Artifacts Written | Prerequisites | Notes |
|---------|------|-------------------|---------------|-------|
| `/brainstorm` | brainstorm.md | None (output is decision text) | None | Entry point. Explores codebase, generates ideas |
| `/create` | create.md | prd.md, prd.json, decisions.md (+ worktree if --worktree) | User input ($ARGUMENTS) | Produces bead + PRD |
| `/plan` | plan.md | plan.md, tasks.md, context-capsule.md | prd.md, prd.json exist and complete | Wave-sequence planning |
| `/ship` | ship.md | Changed source files, progress.txt | prd.md, plan.md, tasks.md exist | Implementation |
| `/verify` | verify.md | completion-evidence.json | plan.md exists, bead in_progress | Runs verification checks |
| `/review` | review.md | review-report.md | completion-evidence.json exists | 5 parallel agents, confidence scoring |
| `/pr` | pr.md | PR (via gh pr create) | review-report.md approved | Single-turn execution |
| `/close` | close.md | None (mutates br state) | completion-evidence.json, review-report.md approved | Closes bead |
| `/init` | init.md | .beads/ database, hydrated memory files | None | Bootstrap |

## Approach

### Wave 1: conventions.md Fixes

These changes touch the same file but different lines — can be done sequentially:

1. **Replace entire Workflow section** (lines 49-56): Replace 7-step workflow with corrected 8-step workflow
2. **Add Prefix info near Naming section**: Insert "Bead prefix: `br-omp`" under the Naming heading
3. **Verify no other stale references**: search for "plan + tasks", "Implement", "Triage" in conventions.md

### Wave 1 Detailed Changes

#### Change 1.1: Replace Workflow section

**Old (lines 49-56):**
```
## Workflow

1. **Triage** — `bv --robot-triage` before any action
2. **Create** — `/create` produces PRD + plan + tasks
3. **Implement** — `/ship` follows plan, no scope creep
4. **Verify** — `/verify` runs checks, records evidence
5. **Review** — `/review` runs parallel agents, confidence filter
6. **PR** — `/pr` opens PR, single-turn execution
7. **Close** — `/close` after merge, suggests next bead
```

**New:**
```
## Workflow

1. **Brainstorm** — `/brainstorm` explores codebase, identifies work
2. **Create** — `/create` produces PRD + decisions.md
3. **Plan** — `/plan` produces plan.md + tasks.md + context-capsule.md
4. **Ship** — `/ship` implements per plan, no scope creep
5. **Verify** — `/verify` runs checks, records evidence
6. **Review** — `/review` runs 5 parallel agents, confidence filter ≥80
7. **PR** — `/pr` opens PR, single-turn execution
8. **Close** — `/close` after review approval, suggests next bead
```

#### Change 1.2: Add Prefix under Naming

Insert after line 14 (`- **Bead slugs:** ...`):
```
- **Bead prefix:** `br-omp` (e.g. `br-omp-a1b2`, `br-omp-fix-login`)
```

### Wave 2: AGENTS.md Fixes

#### Change 2.1: Fix prefix (line 83)

**Old:**
```
- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)
```

**New:**
```
- **Prefix:** `br-omp` (beads are `br-omp-a1b2`, `br-omp-c3d4`, ...)
```

#### Change 2.2: Fix tree diagram (lines 191-230)

The current tree diagram has two structural problems:
1. `.beads/` and `.omp/` items are mixed at the same nesting level
2. Design system CSS files appear under `memory/project/` which is wrong

Corrected structure:
```
omp-template/
├── AGENTS.md                          # Delegates to .omp/AGENTS.md
├── README.md
├── .gitignore
├── .beads/                            # br workspace (SQLite + JSONL)
│   └── artifacts/<bead-id>/           # Per-bead artifacts
│       ├── prd.md                     # Problem, outcome, acceptance criteria
│       ├── prd.json                   # Machine-readable requirements mirror
│       ├── plan.md                    # Scope, blast radius, steps, risks, verification
│       ├── tasks.md                   # Ordered task list with dependencies
│       ├── decisions.md               # Architecture and design decisions
│       ├── context-capsule.md         # Handoff for the next agent
│       ├── progress.txt               # Phase checklist
│       ├── completion-evidence.json   # Verification commands and results
│       └── review-report.md           # Parallel review findings and verdict
├── .omp/                              # OMP native project directory
│   ├── AGENTS.md                      # You are here — canonical project context
│   ├── RULES.md                       # Agent rules (YAGNI, KISS, workflow enforcement)
│   ├── config.yml                     # OMP configuration
│   ├── commands/                      # 9 slash commands
│   │   ├── brainstorm.md              # Ideation — explore codebase for work
│   │   ├── create.md                  # Formalize into bead + PRD
│   │   ├── plan.md                    # Wave-sequence planning
│   │   ├── ship.md                    # Implementation
│   │   ├── verify.md                  # Verification + evidence
│   │   ├── review.md                  # 5-agent parallel review
│   │   ├── pr.md                      # Pull request creation
│   │   ├── close.md                   # Bead closure
│   │   ├── init.md                    # Bootstrap workspace
│   │   └── git-clean.md               # Git cleanup utility
│   ├── skills/                        # 18 cognitive tools
│   │   ├── backbone/SKILL.md          # Workflow reference card
│   │   ├── br/SKILL.md                # Task tracking
│   │   ├── bv/SKILL.md                # Graph intelligence
│   │   ├── orchestrator/SKILL.md      # Phase chaining
│   │   ├── verification-before-completion/SKILL.md
│   │   ├── code-simplification/SKILL.md
│   │   ├── root-cause-tracing/SKILL.md
│   │   ├── defense-in-depth/SKILL.md
│   │   ├── incremental-implementation/SKILL.md
│   │   ├── test-driven-development/SKILL.md
│   │   ├── testing-anti-patterns/SKILL.md
│   │   ├── api-and-interface-design/SKILL.md
│   │   ├── reflection-checkpoints/SKILL.md
│   │   ├── security-and-hardening/SKILL.md
│   │   ├── deprecation-and-migration/SKILL.md
│   │   ├── condition-based-waiting/SKILL.md
│   │   ├── honcho-memory/SKILL.md
│   │   └── design-system/SKILL.md + DESIGN.md
│   ├── extensions/                    # Runtime extensions
│   │   └── workflow-gate.ts           # Blocks edits until PRD + plan exist
│   ├── templates/                     # Artifact templates
│   │   ├── prd.md, prd.json
│   │   ├── plan.md, tasks.md, context-capsule.md
│   │   ├── decisions.md
│   │   ├── progress.txt
│   │   ├── completion-evidence.json
│   │   └── review-report.md
│   └── memory/project/                # Durable project knowledge
│       ├── project.md                 # Vision, goals, current phase
│       ├── conventions.md             # Naming, workflow, agent rules
│       ├── decisions.md               # Architecture decision records
│       ├── gotchas.md                 # Known pitfalls and mitigations
│       └── tech-stack.md              # Versions, verification commands, constraints
└── .worktree/                         # Git worktree directory (ignored)
```

Key changes in the corrected tree:
- `.beads/` and `.omp/` are separate top-level directories
- Artifact files clearly show under `.beads/artifacts/<bead-id>/`
- All `.omp/` items properly nested under `.omp/`
- Design system CSS files moved out of memory/project/ — they belong under skills/design-system/ or a separate assets/ directory (but since this PRD doesn't modify design-system, they're simply removed from the tree)
- Each command file gets a one-line description
- Skills directory count corrected from "17" to "18" (honcho-memory was added)
- `.worktree/` added at root level

#### Change 2.3: Update 1KB memory note (line 101)

**Old:**
```
Keep each under 1KB.
```

**New:**
```
Tier 1 target: under 2KB. Tier 2 target: under 3KB.
```

Alternatively, since the Memory Protocol section already describes the tier system:
```
Memory files grow with project maturity. Audit periodically and consolidate.
```

### Wave 3: project.md Update

#### Change 3.1: Update Current Phase

**Old (lines 22-24):**
```
- **Status:** active
- **Milestone:** Memory file hydration — project identity hardening
- **Next:** Audit command files for consistency with conventions.md
```

**New:**
```
- **Status:** active
- **Milestone:** Command–convention consistency audit (br-omp-backbone-skill-1da)
- **Next:** Verify workflow-gate enforces all required artifact checks, or review template skill coverage
```

### Why this approach:
- Minimal changes — each fix targets one specific audit finding
- Each fix is independently verifiable with grep
- No new sections added, no sections removed
- Wave structure prevents conflicts between AGENTS.md and conventions.md edits
- Conventions.md and AGENTS.md can be edited in parallel (different files)
- project.md update is deferred to Wave 3 to avoid mid-implementation churn

### Merge conflicts
- conventions.md and AGENTS.md are different files → no merge conflicts between waves
- Within conventions.md: Workflow section replace touches lines 49-56; Prefix addition is near line 14 → no overlap
- Within AGENTS.md: Prefix fix touches line 83; 1KB note touches line 101; Tree diagram touches lines 191-230 → no overlap
- project.md: Current Phase touches lines 22-24 → isolated from other edits

## Edge Cases

### EC-1: conventions.md has been edited between audit and implementation
If another bead modified conventions.md concurrently, the line numbers shift. Mitigation: use content-based matching (find the exact text to replace, not line numbers).

### EC-2: AGENTS.md tree diagram is consumed by automated tools
If a tool parses the tree diagram (unlikely but possible), restructuring could break it. Mitigation: tree is documentation-only; no known tools parse it. The corrected structure is more parseable, not less.

### EC-3: The br prefix changes
If the repo is re-initialized with a different prefix, the documentation becomes stale again. Mitigation: this is unlikely; br prefix is set once at init and rarely changes.

### EC-4: New commands added between audit and implementation
If a new command file is added (e.g., `/health-check` becomes permanent), the workflow step count changes. Mitigation: the workflow section lists core phases only; auxiliary commands like `/git-clean` are not included. This is documented in conventions.md Command Structure section.

### EC-5: conventions.md is referenced by other templates or downstream repos
If someone forked this template and their conventions.md still has the old bug, they won't get this fix automatically. Mitigation: template consumers are responsible for their own conventions.md updates. This fix is for the upstream template only.

### EC-6: Multiple agents read conventions.md mid-edit
If an agent reads conventions.md while it's being edited, it might see a partially-updated file. Mitigation: edits are atomic (single `write_file` call per file). The file is small enough to write atomically.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Fixing conventions.md breaks another file that references the old wording | Low | Low | Only AGENTS.md and conventions.md reference workflow; AGENTS.md is correct already |
| Tree diagram restructure creates new nesting errors | Medium | Low | Verify visually after edit; tree is documentation-only, no tool parses it |
| Changing prefix in AGENTS.md confuses agents that cached old prefix | Low | Low | Prefix is used in br operations not agent logic; actual bead IDs determine prefix |
| Scope creep — tempted to fix other conventions.md imperfections | Medium | Medium | Strict "Out of Scope" list; any new finding → separate bead |
| Removing "Keep each under 1KB" causes agents to bloat memory files | Low | Low | Memory maintenance guidelines in AGENTS.md already constrain growth |
| "after merge" → "after review approval" change contradicts an agent's training on standard workflows | Low | Low | RULES.md line 27 is authoritative: "The human always gets the last call on merges" |

## Acceptance Criteria

- [ ] #1: conventions.md line 50 no longer says "PRD + plan + tasks"
	- Verify: `grep "PRD + plan + tasks" .omp/memory/project/conventions.md` returns no matches
- [ ] #2: conventions.md workflow includes /brainstorm step
	- Verify: `grep -c "Brainstorm.*brainstorm" .omp/memory/project/conventions.md` returns ≥1
- [ ] #3: conventions.md workflow includes /plan step with correct outputs
	- Verify: `grep -c "Plan.*plan.*produces" .omp/memory/project/conventions.md` returns ≥1
- [ ] #4: conventions.md workflow has 8 steps (1-8)
	- Verify: Count numbered steps in workflow section = 8
- [ ] #5: conventions.md workflow step 4 says "Ship" not "Implement"
	- Verify: `grep "Ship.*ship" .omp/memory/project/conventions.md` returns ≥1
- [ ] #6: conventions.md workflow step 1 says "Brainstorm" not "Triage"
	- Verify: `grep "Brainstorm.*brainstorm" .omp/memory/project/conventions.md` returns ≥1
- [ ] #7: conventions.md documents bead prefix
	- Verify: `grep "br-omp" .omp/memory/project/conventions.md` returns ≥1
- [ ] #8: AGENTS.md prefix corrected to `br-omp`
	- Verify: `grep "Prefix:.*br-omp" .omp/AGENTS.md` returns ≥1
- [ ] #9: AGENTS.md no longer references `omp-a1b2` as example
	- Verify: `grep "omp-a1b2" .omp/AGENTS.md` returns 0
- [ ] #10: AGENTS.md tree diagram shows proper `.omp/` structure
	- Verify: Visual inspection — `.omp/` items nested under `.omp/` branch, separate from `.beads/`
- [ ] #11: AGENTS.md 1KB note updated
	- Verify: `grep "1KB" .omp/AGENTS.md` returns 0 (old text removed) or shows updated target
- [ ] #12: project.md Current Phase updated
	- Verify: project.md "Milestone" field reflects audit work
- [ ] #13: project.md "Next" field updated
	- Verify: project.md "Next" field no longer reads "Audit command files..."
- [ ] #14: conventions.md Close step says "after review approval" not "after merge"
	- Verify: `grep "after review approval" .omp/memory/project/conventions.md` returns ≥1
- [ ] #15: No regressions — existing br/bv behavior unchanged
	- Verify: `bv --robot-triage --format json` succeeds, `br list --json` succeeds
- [ ] #16: All files are valid markdown
	- Verify: Read each file — no orphan backticks, consistent heading levels
- [ ] #17: AGENTS.md tree diagram skill count says 18 not 17
	- Verify: `grep "18.*skills\|18.*cognitive" .omp/AGENTS.md` returns ≥1
- [ ] #18: conventions.md and AGENTS.md agree on workflow phases
	- Verify: conventions.md steps 1-8 match the command reference table in AGENTS.md (lines 20-31)

## Out of Scope

- Changing any `.omp/commands/*.md` file
- Changing `.omp/RULES.md`
- Changing `.omp/extensions/workflow-gate.ts`
- Changing any `.omp/skills/*/SKILL.md` file
- Changing any `.omp/templates/*` file
- Changing `.omp/config.yml`
- Changing any `.beads/` file other than adding this artifact
- Changing any `.env*` or `.gitignore` file
- Changing README.md
- Adding new workflow steps or reordering existing ones beyond /brainstorm and /plan insertion
- Changing the actual behavior of any command
- Modifying br database schema or bead IDs
- Adding new memory files
- Removing any existing sections from conventions.md or AGENTS.md
- Adding design system CSS files to the tree (they don't exist in this repo)
- Fixing memory file sizes to meet any target
- Adding a CI check for conventions.md ↔ AGENTS.md consistency

## Dependencies

- None. This is a documentation-only fix with no code dependencies.
- The br and bv tools are not modified by these changes.
- The workflow gate does not read conventions.md — it reads bead state.
- No other beads depend on or are blocked by this work.

## Verification Plan

After implementation:
1. `grep` each acceptance criterion (1-18)
2. Read the full conventions.md workflow section — visually confirm logical flow
3. Read the AGENTS.md tree diagram — visually confirm structure
4. Run `br lint br-omp-backbone-skill-1da --json` — no issues
5. Run `bv --robot-triage --format json` — project health unchanged
6. Run `git diff --stat` — only .omp/memory/project/conventions.md, .omp/AGENTS.md, .omp/memory/project/project.md changed
7. Run `git diff` — review every changed line for correctness
8. Run `br sync --flush-only` to flush any bead state changes
9. Compare conventions.md workflow against AGENTS.md command reference table — must match

### Pre-implementation baseline (for diff comparison)
```bash
# Capture the bug before fixing
grep -n "PRD + plan" .omp/memory/project/conventions.md
grep -n "Prefix.*omp" .omp/AGENTS.md
grep -n "Keep each under 1KB" .omp/AGENTS.md
grep -n "Triage" .omp/memory/project/conventions.md
```

Expected output before fix:
```
50:2. **Create** — `/create` produces PRD + plan + tasks
83:- **Prefix:** `omp` (beads are `omp-a1b2`, `omp-c3d4`, ...)
101:Keep each under 1KB.
49:1. **Triage** — `bv --robot-triage` before any action
```

Expected output after fix:
- Line 50: No longer matches "PRD + plan"
- Line 83: Now says "br-omp"
- Line 101: Updated or removed
- Line 49: Now says "Brainstorm"

## Implementation Notes

### Commit Strategy
Each wave produces one conventional commit:

```
Wave 1: docs: fix conventions.md workflow — correct /create output, add brainstorm/plan steps
Wave 2: docs: fix AGENTS.md — correct bead prefix, restructure tree diagram, update memory targets
Wave 3: docs: update project.md current phase after audit completion
```

Alternatively, all changes can be a single commit since they're all documentation fixes for the same audit:
```
docs: audit and fix conventions.md + AGENTS.md consistency (br-omp-backbone-skill-1da)
```

### Rollback
If any fix causes issues, rollback is straightforward:
```
git revert <commit-hash>
```

No data migration, no database changes, no tool reconfiguration needed.

### Post-Implementation
After this bead closes, the next candidate work (per project.md "Next") is:
- Verify workflow-gate enforces all required artifact checks
- Audit template skill coverage (are all skills referenced in skills map?)
- Create a CI check or pre-commit hook that validates conventions.md ↔ AGENTS.md consistency (stretch goal)
